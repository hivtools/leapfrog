"""`compare` with the run archive switched on (ticket 24).

Drives the real `compare` command with `FakeArchive` behind the archive
seam and counting fakes for build/run. The acceptance criteria these pin:

- a second identical comparison reuses archived packets: the model runner is
  not called again, and leapfrogr is not even built (lazy workspaces);
- the diff verdict is never archived: tightening or loosening a tolerance
  changes the verdict for an already-archived run with no model re-run;
- an uncommitted working tree is never archived.
"""

from pathlib import Path

import h5py
import numpy as np
import pytest
from fake_archive import FakeArchive, requires_orderly
from typer.testing import CliRunner

from leapfrog_validate import archive as archive_module
from leapfrog_validate import cli, git_utils, indicators
from leapfrog_validate.archive import OrderlyArchive
from leapfrog_validate.build import BuildWorkspace
from leapfrog_validate.cli import app

runner = CliRunner()


def _write_output_h5(path: Path, scale: float) -> None:
    n_year, n_sex = 2, 2
    hc1_age, hc2_age, h_age = 2, 3, 4
    total_age = hc1_age + hc2_age + h_age

    with h5py.File(path, "w") as f:
        f.create_dataset("p_totpop", data=np.full((n_year, n_sex, total_age), 100.0 * scale))
        f.create_dataset("p_hivpop", data=np.full((n_year, n_sex, total_age), 10.0 * scale))
        f.create_dataset("p_hiv_deaths", data=np.full((n_year, n_sex, total_age), 1.0 * scale))
        f.create_dataset("h_artpop", data=np.full((n_year, n_sex, h_age, 7, 3), 1.0 * scale))
        f.create_dataset("hc1_artpop", data=np.full((n_year, n_sex, hc1_age, 7, 3), 1.0 * scale))
        f.create_dataset("hc2_artpop", data=np.full((n_year, n_sex, hc2_age, 6, 3), 1.0 * scale))
        f.create_dataset("h_hiv_deaths_art", data=np.full((n_year, n_sex, h_age, 7, 3), 0.1 * scale))
        f.create_dataset("hc1_art_aids_deaths", data=np.full((n_year, n_sex, hc1_age, 7, 3), 0.1 * scale))
        f.create_dataset("hc2_art_aids_deaths", data=np.full((n_year, n_sex, hc2_age, 6, 3), 0.1 * scale))


class World:
    """Counters and knobs for the faked build/run, plus the archive under test."""

    def __init__(self):
        self.archive = FakeArchive()
        self.prepared_refs: list[str] = []
        self.model_runs = 0
        self.scale_by_ref = {"main": 1.0, "candidate-branch": 1.0, git_utils.WORKING_TREE: 1.0}


@pytest.fixture
def world(monkeypatch):
    world = World()

    def fake_resolve_ref(repo_root, ref):
        del repo_root
        return ref.ljust(40, "0")

    def fake_prepare_ref(repo_root, cache_dir, ref):
        del repo_root, cache_dir
        world.prepared_refs.append(ref)
        worktree = Path(f"/fake/{ref}")
        return BuildWorkspace(worktree=worktree, r_library=worktree / "r-library")

    def fake_build_params(workspace, pjnz, output):
        del pjnz
        output.write_text(str(workspace.worktree.name))  # remember which ref built it

    def fake_run_model(workspace, params_path, output, configuration):
        del params_path, configuration
        world.model_runs += 1
        ref = workspace.worktree.name.rstrip("0") or workspace.worktree.name
        _write_output_h5(output, scale=world.scale_by_ref[ref])

    monkeypatch.setattr(git_utils, "resolve_ref", fake_resolve_ref)
    monkeypatch.setattr(cli, "_prepare_ref", fake_prepare_ref)
    monkeypatch.setattr(cli.params, "build_params", fake_build_params)
    monkeypatch.setattr(cli.model_run, "run_model", fake_run_model)
    # Same contract as the real factory: no root configured means no archive.
    monkeypatch.setattr(
        archive_module, "archive_from_settings", lambda root, *_a, **_k: world.archive if root is not None else None
    )
    return world


@pytest.fixture
def corpus(tmp_path):
    pjnz_dir = tmp_path / "corpus"
    pjnz_dir.mkdir()
    (pjnz_dir / "a.PJNZ").write_text("a")
    (pjnz_dir / "b.PJNZ").write_text("b")
    return pjnz_dir


def _compare(corpus: Path, ref="main", candidate="candidate-branch", *, archived=True):
    args = ["--archive-root", "ignored-by-the-fake"] if archived else []
    return runner.invoke(app, [*args, "compare", ref, candidate, "--pjnz-dir", str(corpus)])


def test_a_second_identical_comparison_reuses_every_packet(world, corpus):
    first = _compare(corpus)
    runs_after_first = world.model_runs
    builds_after_first = len(world.prepared_refs)

    second = _compare(corpus)

    assert first.exit_code == 0, first.output
    assert second.exit_code == 0, second.output
    assert runs_after_first == 4  # 2 PJNZ x 2 refs
    assert world.model_runs == runs_after_first  # the second run computes nothing
    assert len(world.prepared_refs) == builds_after_first  # ...and never even builds leapfrogr
    assert "archive hit: leapfrog_run a.PJNZ" in second.output
    assert "archive miss" not in second.output


def test_a_changed_tolerance_flips_the_verdict_of_an_archived_run_without_a_rerun(world, corpus, monkeypatch):
    world.scale_by_ref["candidate-branch"] = 1.5  # candidate differs from main by 50%
    first = _compare(corpus)
    runs_after_first = world.model_runs
    assert first.exit_code == 1, first.output  # fails at the real, tight tolerance

    for spec in indicators.INDICATORS.values():
        monkeypatch.setitem(spec, "tolerance", indicators.Tolerance(atol=1000.0, rtol=0.0))
    second = _compare(corpus)

    assert second.exit_code == 0, second.output  # same archived bytes, new verdict
    assert world.model_runs == runs_after_first  # no model was run to get it
    assert "archive hit" in second.output


def test_tightening_a_tolerance_also_re_judges_archived_history(world, corpus, monkeypatch):
    world.scale_by_ref["candidate-branch"] = 1.0 + 1e-3
    for spec in indicators.INDICATORS.values():
        monkeypatch.setitem(spec, "tolerance", indicators.Tolerance(atol=1000.0, rtol=0.0))
    loose = _compare(corpus)
    runs_after_first = world.model_runs
    assert loose.exit_code == 0, loose.output

    for spec in indicators.INDICATORS.values():
        monkeypatch.setitem(spec, "tolerance", indicators.Tolerance(atol=0.0, rtol=0.0))
    tight = _compare(corpus)

    assert tight.exit_code == 1, tight.output
    assert world.model_runs == runs_after_first


def test_only_raw_output_is_archived_never_a_verdict(world, corpus):
    _compare(corpus)

    assert {report for report, *_ in world.archive.stores} == {"leapfrog_run"}
    for _report, _key, extra in world.archive.stores:
        assert set(extra) == {"ref_given"}  # provenance of the ref, nothing about the diff
    for *_, content in world.archive.packets:
        assert content.startswith(b"\x89HDF")  # the raw output.h5 bytes themselves


def test_keys_use_the_resolved_sha_and_store_the_ref_as_given(world, corpus):
    _compare(corpus)

    keys = {(key["ref_sha"], extra["ref_given"]) for _report, key, extra in world.archive.stores}
    assert keys == {("main".ljust(40, "0"), "main"), ("candidate-branch".ljust(40, "0"), "candidate-branch")}


def test_the_working_tree_is_never_archived_but_the_other_side_still_is(world, corpus):
    result = _compare(corpus, ref=git_utils.WORKING_TREE, candidate="main")

    assert result.exit_code == 0, result.output
    assert {key["ref_sha"] for _report, key, _extra in world.archive.stores} == {"main".ljust(40, "0")}
    assert all(key["ref_sha"] != git_utils.WORKING_TREE for _report, key in world.archive.fetches)


def test_without_archive_options_nothing_changes(world, corpus):
    result = _compare(corpus, archived=False)

    assert result.exit_code == 0, result.output
    assert world.archive.fetches == []
    assert world.archive.stores == []
    assert world.prepared_refs == ["main", "candidate-branch"]  # still built eagerly, up front
    assert "archive" not in result.output


@requires_orderly
def test_the_same_flow_against_a_real_orderly_root(world, corpus, tmp_path, monkeypatch):
    """The acceptance flow once more with real Orderly2 packets behind the seam (model still faked)."""
    world.archive = OrderlyArchive(root=tmp_path / "archive")
    world.scale_by_ref["candidate-branch"] = 1.5

    first = _compare(corpus)
    runs_after_first = world.model_runs
    second = _compare(corpus)
    for spec in indicators.INDICATORS.values():
        monkeypatch.setitem(spec, "tolerance", indicators.Tolerance(atol=1000.0, rtol=0.0))
    third = _compare(corpus)

    assert (first.exit_code, second.exit_code, third.exit_code) == (1, 1, 0)
    assert runs_after_first == 4
    assert world.model_runs == 4  # runs 2 and 3 computed nothing
    assert "archive hit: leapfrog_run a.PJNZ" in third.output
