"""The Spectrum-comparison track with the archive switched on (ticket 24).

Both archived steps are in play here: leapfrog's raw `output.h5` (keyed by
PJNZ + resolved ref SHA) and Spectrum's extracted modvars (keyed by PJNZ
identity alone). Build/run/import are counting fakes; the archive is
`FakeArchive`; the diff is a stand-in that reports which modvars it saw.
"""

from pathlib import Path

import numpy as np
import pytest
from fake_archive import FakeArchive
from typer.testing import CliRunner

from leapfrog_validate import archive as archive_module
from leapfrog_validate import git_utils, spectrum_archive, spectrum_extract, spectrum_track
from leapfrog_validate import model_run as model_run_module
from leapfrog_validate import params as params_module
from leapfrog_validate.build import BuildWorkspace
from leapfrog_validate.diff import Verdict
from leapfrog_validate.spectrum_track import app

runner = CliRunner()


class World:
    def __init__(self):
        self.archive = FakeArchive()
        self.builds = 0
        self.model_runs = 0
        self.imports = 0
        self.modvars_seen: list[dict] = []


@pytest.fixture
def world(monkeypatch):
    world = World()

    def fake_prepare_ref(repo_root, cache_dir, ref):
        del repo_root, cache_dir
        world.builds += 1
        return BuildWorkspace(worktree=Path(f"/fake/{ref}"), r_library=Path("/fake/lib"))

    def fake_build_params(workspace, pjnz, output):
        del pjnz
        _ = workspace.worktree
        output.write_bytes(b"params")

    def fake_run_model(workspace, params_path, output, configuration):
        del workspace, params_path, configuration
        world.model_runs += 1
        output.write_bytes(b"raw output")

    def fake_import(pjnz):
        del pjnz
        world.imports += 1
        return {"<A>": np.arange(6.0).reshape(1, 2, 3), "<B>": 1970}

    def fake_diff(name, output_h5, pjnz, pjnz_label=None, modvars=None):  # noqa: ARG001
        world.modvars_seen.append(modvars)
        return Verdict(indicator=name, passed=True, max_abs_diff=0.0, n_cells=1, n_failed=0)

    monkeypatch.setattr(git_utils, "resolve_ref", lambda _root, ref: ref.ljust(40, "0"))
    monkeypatch.setattr(spectrum_track, "_prepare_ref", fake_prepare_ref)
    monkeypatch.setattr(params_module, "build_params", fake_build_params)
    monkeypatch.setattr(model_run_module, "run_model", fake_run_model)
    monkeypatch.setattr(spectrum_extract, "import_modvars", fake_import)
    monkeypatch.setattr(spectrum_archive, "blessed_modvar_tags", lambda: ["<A>", "<B>"])
    monkeypatch.setattr(spectrum_track, "diff_spectrum_indicator", fake_diff)
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


def _run(tmp_path, corpus, ref="main", *, archived=True):
    args = ["--archive-root", "ignored-by-the-fake"] if archived else []
    return runner.invoke(
        app, ["run", ref, "--pjnz-dir", str(corpus), "--comment-out", str(tmp_path / "comment.md"), *args]
    )


def test_a_second_run_reuses_both_archived_steps(world, corpus, tmp_path):
    first = _run(tmp_path, corpus)
    after_first = (world.builds, world.model_runs, world.imports)

    second = _run(tmp_path, corpus)

    assert first.exit_code == 0, first.output
    assert second.exit_code == 0, second.output
    assert after_first == (1, 2, 2)  # one build, one model run and one import per PJNZ
    assert (world.builds, world.model_runs, world.imports) == after_first
    assert "archive hit: leapfrog_run a.PJNZ" in second.output
    assert "archive hit: spectrum_extract a.PJNZ" in second.output


def test_spectrum_packets_ignore_the_git_ref_but_leapfrog_packets_do_not(world, corpus, tmp_path):
    _run(tmp_path, corpus, ref="main")
    imports_after_first = world.imports
    runs_after_first = world.model_runs

    _run(tmp_path, corpus, ref="other-branch")

    assert world.imports == imports_after_first  # same PJNZs: Spectrum side reused across refs
    assert world.model_runs == runs_after_first + 2  # a new commit: leapfrog side recomputed


def test_the_diff_gets_archived_modvars_and_is_never_itself_archived(world, corpus, tmp_path):
    _run(tmp_path, corpus)
    _run(tmp_path, corpus)

    assert {report for report, *_ in world.archive.stores} == {"leapfrog_run", "spectrum_extract"}
    assert all(set(modvars) == {"<A>", "<B>"} for modvars in world.modvars_seen)  # raw modvars, no indicators


def test_without_archive_options_the_diff_imports_for_itself(world, corpus, tmp_path):
    result = _run(tmp_path, corpus, archived=False)

    assert result.exit_code == 0, result.output
    assert world.archive.fetches == []
    assert all(modvars is None for modvars in world.modvars_seen)
    assert world.imports == 0  # the (faked) diff does its own live import in this mode
    assert "archive hit" not in result.output
    assert "archive miss" not in result.output
