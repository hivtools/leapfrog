"""The `run` primitive with the run archive switched on (ticket 24).

`run` takes a ready params.h5, which does not say which PJNZ it came from,
so the archive key needs `--pjnz` to name it.
"""

from pathlib import Path

import pytest
from fake_archive import FakeArchive
from typer.testing import CliRunner

from leapfrog_validate import archive as archive_module
from leapfrog_validate import cli, git_utils
from leapfrog_validate.build import BuildWorkspace
from leapfrog_validate.cli import app

runner = CliRunner()


@pytest.fixture
def world(monkeypatch):
    class World:
        archive = FakeArchive()
        model_runs = 0
        builds = 0

    w = World()

    def fake_prepare_ref(repo_root, cache_dir, ref):
        del repo_root, cache_dir
        w.builds += 1
        return BuildWorkspace(worktree=Path(f"/fake/{ref}"), r_library=Path("/fake/lib"))

    def fake_run_model(workspace, params_path, output, configuration):
        del params_path, configuration
        _ = workspace.worktree  # the real runner uses the workspace, which is what triggers a lazy build
        w.model_runs += 1
        output.write_bytes(b"raw output")

    monkeypatch.setattr(git_utils, "resolve_ref", lambda _root, ref: ref.ljust(40, "0"))
    monkeypatch.setattr(cli, "_prepare_ref", fake_prepare_ref)
    monkeypatch.setattr(cli.model_run, "run_model", fake_run_model)
    monkeypatch.setattr(
        archive_module, "archive_from_settings", lambda root, *_a, **_k: w.archive if root is not None else None
    )
    return w


def _invoke(tmp_path, *extra, archived=True):
    params_path = tmp_path / "params.h5"
    params_path.write_bytes(b"params")
    pjnz = tmp_path / "a.PJNZ"
    pjnz.write_bytes(b"pjnz")
    out = tmp_path / "output.h5"
    args = ["--archive-root", "x"] if archived else []
    return runner.invoke(app, [*args, "run", "main", str(params_path), "-o", str(out), *extra]), out


def test_run_with_an_archive_reuses_a_packet_on_the_second_call(world, tmp_path):
    pjnz = str(tmp_path / "a.PJNZ")
    first, out = _invoke(tmp_path, "--pjnz", pjnz)
    out.unlink()
    second, _ = _invoke(tmp_path, "--pjnz", pjnz)

    assert first.exit_code == 0, first.output
    assert second.exit_code == 0, second.output
    assert world.model_runs == 1
    assert world.builds == 1  # the second call never built leapfrogr
    assert out.read_bytes() == b"raw output"


def test_run_with_an_archive_requires_pjnz_to_name_the_key(world, tmp_path):
    result, _ = _invoke(tmp_path)

    assert result.exit_code == 2
    assert "--pjnz" in result.output
    assert world.model_runs == 0


def test_run_without_an_archive_ignores_pjnz_and_always_runs(world, tmp_path):
    _invoke(tmp_path, archived=False)
    _invoke(tmp_path, archived=False)

    assert world.model_runs == 2


def test_pjnz_label_names_the_key_so_run_can_share_compares_packets(world, tmp_path):
    pjnz = str(tmp_path / "a.PJNZ")

    result, _ = _invoke(tmp_path, "--pjnz", pjnz, "--pjnz-label", "ETH/a.PJNZ")

    assert result.exit_code == 0, result.output
    assert world.archive.stores[0][1]["pjnz"] == "ETH/a.PJNZ"
    assert "archive stored: leapfrog_run ETH/a.PJNZ" in result.output
