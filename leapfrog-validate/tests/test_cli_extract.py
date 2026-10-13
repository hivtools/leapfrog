"""The `extract` primitive: a PJNZ's Spectrum modvars -> extract.h5, archive-aware (ticket 24)."""

import numpy as np
import pytest
from fake_archive import FakeArchive
from typer.testing import CliRunner

from leapfrog_validate import archive as archive_module
from leapfrog_validate import spectrum_archive, spectrum_extract
from leapfrog_validate.cli import app
from leapfrog_validate.spectrum_archive import read_extract_h5

runner = CliRunner()


@pytest.fixture
def world(monkeypatch):
    class World:
        archive = FakeArchive()
        imports = 0

    w = World()

    def fake_import(pjnz):
        del pjnz
        w.imports += 1
        return {"<A>": np.arange(4.0), "<B>": 1970, "<NOT-ARCHIVED>": np.zeros(2)}

    monkeypatch.setattr(spectrum_extract, "import_modvars", fake_import)
    monkeypatch.setattr(spectrum_archive, "blessed_modvar_tags", lambda: ["<A>", "<B>"])
    monkeypatch.setattr(
        archive_module, "archive_from_settings", lambda root, *_a, **_k: w.archive if root is not None else None
    )
    return w


def _extract(tmp_path, *, archived=True):
    pjnz = tmp_path / "a.PJNZ"
    pjnz.write_bytes(b"pjnz")
    out = tmp_path / "extract.h5"
    args = ["--archive-root", "x"] if archived else []
    return runner.invoke(app, [*args, "extract", str(pjnz), "-o", str(out)]), out


def test_extract_writes_the_blessed_modvars(world, tmp_path):
    result, out = _extract(tmp_path, archived=False)

    assert result.exit_code == 0, result.output
    assert set(read_extract_h5(out)) == {"<A>", "<B>"}
    assert world.imports == 1


def test_extract_reuses_the_archived_packet_on_the_second_call(world, tmp_path):
    _extract(tmp_path)
    second, out = _extract(tmp_path)

    assert second.exit_code == 0, second.output
    assert world.imports == 1
    assert "archive hit: spectrum_extract a.PJNZ" in second.output
    np.testing.assert_array_equal(read_extract_h5(out)["<A>"], np.arange(4.0))
