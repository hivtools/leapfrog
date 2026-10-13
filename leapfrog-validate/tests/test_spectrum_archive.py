"""`spectrum_archive.obtain_modvars`: Spectrum's extract step, archived by PJNZ identity (ticket 24).

The decision logic is tested with a fake importer and `FakeArchive`. One
round-trip test uses the real avenir importer on a public fixture PJNZ to
prove the archived modvars give exactly the live indicator arrays.
"""

from pathlib import Path

import numpy as np
import pytest
from fake_archive import FakeArchive

from leapfrog_validate import spectrum_extract
from leapfrog_validate.archive import ArchiveError, file_sha256
from leapfrog_validate.spectrum_archive import (
    EXTRACT_REPORT,
    obtain_modvars,
    read_extract_h5,
    write_extract_h5,
)

FIXTURE_PJNZ = Path(__file__).parents[2] / "leapfrogr" / "inst" / "pjnz" / "france_default.PJNZ"

MODVARS = {
    "<PJN_FirstYear_V1>": 1970,
    "<PJN_FinalYear_V1>": 2032,
    "<DP_BigPop_V1>": np.arange(3 * 4 * 5, dtype=float).reshape(3, 4, 5),
}


class CountingImporter:
    def __init__(self):
        self.calls = 0

    def __call__(self, pjnz: Path) -> dict:
        del pjnz
        self.calls += 1
        return dict(MODVARS)


def _pjnz(tmp_path: Path, content: bytes = b"pjnz") -> Path:
    path = tmp_path / "a.PJNZ"
    path.write_bytes(content)
    return path


def _obtain(tmp_path, archive, importer, pjnz=None):
    logged: list[str] = []
    modvars = obtain_modvars(
        archive=archive,
        pjnz=pjnz or _pjnz(tmp_path),
        pjnz_label="a.PJNZ",
        work_dir=tmp_path / "work",
        import_modvars=importer,
        archived_tags=list(MODVARS),
        log=logged.append,
    )
    return modvars, logged


def test_h5_round_trip_keeps_scalars_and_arrays_exactly(tmp_path):
    write_extract_h5(MODVARS, tmp_path / "extract.h5")

    back = read_extract_h5(tmp_path / "extract.h5")

    assert set(back) == set(MODVARS)
    assert back["<PJN_FirstYear_V1>"] == 1970
    np.testing.assert_array_equal(back["<DP_BigPop_V1>"], MODVARS["<DP_BigPop_V1>"])


def test_without_an_archive_it_imports_every_time(tmp_path):
    importer = CountingImporter()

    _obtain(tmp_path, None, importer)
    _obtain(tmp_path, None, importer)

    assert importer.calls == 2


def test_a_miss_imports_and_archives_by_pjnz_identity_only(tmp_path):
    archive = FakeArchive()
    importer = CountingImporter()

    _obtain(tmp_path, archive, importer)

    assert importer.calls == 1
    assert len(archive.stores) == 1
    report, key, extra = archive.stores[0]
    assert report == EXTRACT_REPORT == "spectrum_extract"
    assert key == {"pjnz": "a.PJNZ", "pjnz_sha256": file_sha256(tmp_path / "a.PJNZ")}  # no git ref anywhere
    assert set(extra) == {"importer"}


def test_a_hit_skips_the_importer_and_returns_the_same_modvars(tmp_path):
    archive = FakeArchive()
    importer = CountingImporter()
    first, _ = _obtain(tmp_path, archive, importer)

    second, logged = _obtain(tmp_path, archive, importer)

    assert importer.calls == 1
    assert len(archive.stores) == 1
    np.testing.assert_array_equal(second["<DP_BigPop_V1>"], first["<DP_BigPop_V1>"])
    assert logged == ["archive hit: spectrum_extract a.PJNZ"]


def test_an_edited_pjnz_under_the_same_name_is_a_miss(tmp_path):
    archive = FakeArchive()
    importer = CountingImporter()
    _obtain(tmp_path, archive, importer)

    _obtain(tmp_path, archive, importer, pjnz=_pjnz(tmp_path, b"edited"))

    assert importer.calls == 2


def test_archive_failures_degrade_to_a_live_import_with_a_warning(tmp_path):
    importer = CountingImporter()

    _, read_log = _obtain(tmp_path, FakeArchive(fail_fetch=ArchiveError("down")), importer)
    _, write_log = _obtain(tmp_path, FakeArchive(fail_store=ArchiveError("down")), importer)

    assert importer.calls == 2
    assert any("WARNING" in line and "read" in line for line in read_log)
    assert any("WARNING" in line and "write" in line for line in write_log)


def test_a_failing_import_is_never_archived(tmp_path):
    archive = FakeArchive()

    def broken(pjnz):
        raise spectrum_extract.SpectrumExtractError(str(pjnz))

    with pytest.raises(spectrum_extract.SpectrumExtractError):
        _obtain(tmp_path, archive, broken)

    assert archive.stores == []


@pytest.mark.skipif(not FIXTURE_PJNZ.exists(), reason="public fixture PJNZ not present")
def test_archived_modvars_give_exactly_the_live_indicator_arrays(tmp_path):
    archive = FakeArchive()
    live = {
        name: fn(FIXTURE_PJNZ)
        for name, fn in {
            "total_population": spectrum_extract.extract_spectrum_total_population,
            "aids_deaths_single_age": spectrum_extract.extract_spectrum_aids_deaths_single_age,
        }.items()
    }

    obtain_modvars(archive=archive, pjnz=FIXTURE_PJNZ, pjnz_label="france_default.PJNZ", work_dir=tmp_path / "w1")
    archived = obtain_modvars(
        archive=archive, pjnz=FIXTURE_PJNZ, pjnz_label="france_default.PJNZ", work_dir=tmp_path / "w2"
    )

    assert len(archive.stores) == 1  # the second call was a hit
    np.testing.assert_array_equal(
        spectrum_extract.extract_spectrum_total_population(FIXTURE_PJNZ, modvars=archived), live["total_population"]
    )
    np.testing.assert_array_equal(
        spectrum_extract.extract_spectrum_aids_deaths_single_age(FIXTURE_PJNZ, modvars=archived),
        live["aids_deaths_single_age"],
    )
