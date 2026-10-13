"""The regression track with the run archive switched on (ticket 24).

CI's main use of the archive: the base ref (`main`) is the same commit on
most PR pushes, so its packets are reused instead of re-running the model.
"""

import hashlib
from pathlib import Path

import h5py
import numpy as np
import pytest
from fake_archive import FakeArchive

from leapfrog_validate import archive as archive_module
from leapfrog_validate import cli, git_utils
from leapfrog_validate.build import BuildWorkspace
from leapfrog_validate.report_regression import _build_arg_parser, compute_regression_report


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
    def __init__(self):
        self.model_runs = 0
        self.builds = 0
        self.ref_scale = {}


@pytest.fixture
def world(monkeypatch):
    world = World()

    def fake_resolve_ref(repo_root, ref):
        del repo_root
        return hashlib.sha256(ref.encode()).hexdigest()[:40]

    def fake_prepare_ref(repo_root, cache_dir, ref):
        del repo_root, cache_dir
        world.builds += 1
        return BuildWorkspace(worktree=Path(f"/fake/{ref}"), r_library=Path("/fake/lib"))

    def fake_build_params(workspace, pjnz, output):
        del pjnz
        output.write_text(workspace.worktree.name)

    def fake_run_model(workspace, params_path, output, configuration):
        del configuration
        world.model_runs += 1
        built_at = params_path.read_text()
        _write_output_h5(output, scale=world.ref_scale.get(built_at, 1.0))
        _ = workspace

    monkeypatch.setattr(git_utils, "resolve_ref", fake_resolve_ref)
    monkeypatch.setattr(cli, "_prepare_ref", fake_prepare_ref)
    monkeypatch.setattr(cli.params, "build_params", fake_build_params)
    monkeypatch.setattr(cli.model_run, "run_model", fake_run_model)
    return world


def _corpus(tmp_path: Path) -> Path:
    pjnz_dir = tmp_path / "corpus"
    pjnz_dir.mkdir()
    (pjnz_dir / "a.PJNZ").write_text("a")
    return pjnz_dir


def _compute(tmp_path, archive, ref, log):
    return compute_regression_report(
        repo_root=tmp_path,
        cache_dir=tmp_path / "cache",
        ref=ref,
        candidate="main",
        pjnz_dir=_corpus(tmp_path) if not (tmp_path / "corpus").exists() else tmp_path / "corpus",
        archive=archive,
        log=log,
    )


def test_the_unchanged_base_ref_is_reused_across_pr_pushes(world, tmp_path):
    archive = FakeArchive()
    log: list[str] = []

    _compute(tmp_path, archive, "pr-push-1", log.append)
    runs_after_first_push = world.model_runs
    _compute(tmp_path, archive, "pr-push-2", log.append)

    assert runs_after_first_push == 2  # PR head + main, one PJNZ
    assert world.model_runs == runs_after_first_push + 1  # second push: only the new PR head runs
    assert "archive hit: leapfrog_run a.PJNZ" in log  # main's packet


def test_an_identical_rerun_computes_nothing_and_builds_nothing(world, tmp_path):
    archive = FakeArchive()
    _compute(tmp_path, archive, "pr-head", print)
    runs, builds = world.model_runs, world.builds

    report = _compute(tmp_path, archive, "pr-head", print)

    assert (world.model_runs, world.builds) == (runs, builds)
    assert report.overall_passed is True


@pytest.mark.usefixtures("world")
def test_archive_log_lines_contain_no_digits_beyond_the_file_label(tmp_path):
    archive = FakeArchive()
    log: list[str] = []
    _compute(tmp_path, archive, "pr-head", log.append)
    _compute(tmp_path, archive, "pr-head", log.append)

    archive_lines = [line for line in log if line.startswith("archive")]
    assert archive_lines
    assert all(not any(ch.isdigit() for ch in line) for line in archive_lines)


def test_the_cli_reads_archive_settings_from_the_environment(monkeypatch, tmp_path):
    monkeypatch.setenv(archive_module.ENV_ROOT, str(tmp_path / "root"))
    monkeypatch.setenv(archive_module.ENV_REMOTE, "shared")

    args = _build_arg_parser().parse_args(["--ref", "x", "--out", "y"])

    assert args.archive_root == tmp_path / "root"
    assert args.archive_remote == "shared"
    assert args.archive_remote_path is None
