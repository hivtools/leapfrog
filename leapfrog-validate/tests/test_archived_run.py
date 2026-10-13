"""`archived_run.obtain_output`: the "get output.h5 for (ref, PJNZ)" seam (tickets 01 + 24).

The archive is `FakeArchive`; "compute" is a counting stand-in for
build-params + run. What matters here is the decision logic: when the
archive is consulted, what the exact key is, and that a hit skips compute.
"""

from pathlib import Path

import pytest
from fake_archive import FakeArchive

from leapfrog_validate.archive import ArchiveError, file_sha256
from leapfrog_validate.archived_run import Origin, RefIdentity, obtain_output

SHA = "a" * 40
MAIN = RefIdentity(given="main", sha=SHA)


class Compute:
    """A counting `compute` callback that writes a configuration-dependent output."""

    def __init__(self, output_path: Path, configuration: str = "Spectrum"):
        self.calls = 0
        self._output_path = output_path
        self._configuration = configuration

    def __call__(self) -> None:
        self.calls += 1
        self._output_path.write_bytes(f"output-{self._configuration}".encode())


def _pjnz(tmp_path: Path, content: bytes = b"pjnz bytes") -> Path:
    path = tmp_path / "a.PJNZ"
    path.write_bytes(content)
    return path


def _obtain(  # noqa: PLR0913, PLR0917 - test helper with optional knobs
    tmp_path, archive, ref=MAIN, pjnz=None, configuration="Spectrum", out="out.h5"
):
    logged: list[str] = []
    compute = Compute(tmp_path / out, configuration)
    origin = obtain_output(
        archive=archive,
        ref=ref,
        pjnz=pjnz or _pjnz(tmp_path),
        pjnz_label="a.PJNZ",
        output_path=tmp_path / out,
        configuration=configuration,
        compute=compute,
        log=logged.append,
    )
    return origin, compute, logged


def test_without_an_archive_it_always_computes(tmp_path):
    origin, compute, _ = _obtain(tmp_path, archive=None)

    assert origin is Origin.COMPUTED
    assert compute.calls == 1
    assert (tmp_path / "out.h5").read_bytes() == b"output-Spectrum"


def test_a_miss_computes_and_archives_the_raw_output(tmp_path):
    archive = FakeArchive()

    origin, compute, _ = _obtain(tmp_path, archive)

    assert origin is Origin.COMPUTED
    assert compute.calls == 1
    assert len(archive.stores) == 1
    report, key, extra = archive.stores[0]
    assert report == "leapfrog_run"
    assert key == {
        "pjnz": "a.PJNZ",
        "pjnz_sha256": file_sha256(tmp_path / "a.PJNZ"),
        "ref_sha": SHA,
        "configuration": "Spectrum",
    }
    assert extra == {"ref_given": "main"}
    assert archive.packets[0][3] == b"output-Spectrum"


def test_a_hit_reuses_the_packet_and_skips_compute(tmp_path):
    archive = FakeArchive()
    _obtain(tmp_path, archive)
    (tmp_path / "out.h5").unlink()

    origin, compute, _ = _obtain(tmp_path, archive)

    assert origin is Origin.ARCHIVE
    assert compute.calls == 0
    assert (tmp_path / "out.h5").read_bytes() == b"output-Spectrum"
    assert len(archive.stores) == 1  # nothing new archived on a hit


def test_the_same_commit_reached_by_another_ref_name_is_a_hit(tmp_path):
    archive = FakeArchive()
    _obtain(tmp_path, archive, ref=RefIdentity(given="my-branch", sha=SHA))

    origin, compute, _ = _obtain(tmp_path, archive, ref=RefIdentity(given=SHA, sha=SHA))

    assert origin is Origin.ARCHIVE
    assert compute.calls == 0


@pytest.mark.parametrize(
    ("ref", "pjnz_content", "configuration"),
    [
        (RefIdentity(given="main", sha="b" * 40), b"pjnz bytes", "Spectrum"),
        (MAIN, b"edited pjnz bytes", "Spectrum"),
        (MAIN, b"pjnz bytes", "Goals"),
    ],
    ids=["other-commit", "same-name-but-edited-pjnz", "other-configuration"],
)
def test_any_key_difference_recomputes(tmp_path, ref, pjnz_content, configuration):
    archive = FakeArchive()
    _obtain(tmp_path, archive)

    origin, compute, _ = _obtain(
        tmp_path, archive, ref=ref, pjnz=_pjnz(tmp_path, pjnz_content), configuration=configuration, out="out2.h5"
    )

    assert origin is Origin.COMPUTED
    assert compute.calls == 1


def test_an_uncommitted_working_tree_is_never_archived(tmp_path):
    archive = FakeArchive()

    origin, compute, _ = _obtain(tmp_path, archive, ref=None)

    assert origin is Origin.COMPUTED
    assert compute.calls == 1
    assert archive.fetches == []
    assert archive.stores == []


def test_an_archive_read_failure_falls_back_to_computing_and_says_so(tmp_path):
    archive = FakeArchive(fail_fetch=ArchiveError("remote unreachable"))

    origin, compute, logged = _obtain(tmp_path, archive)

    assert origin is Origin.COMPUTED
    assert compute.calls == 1
    assert any("WARNING" in line and "read" in line for line in logged)


def test_an_archive_write_failure_keeps_the_computed_output_and_says_so(tmp_path):
    archive = FakeArchive(fail_store=ArchiveError("disk full"))

    origin, _, logged = _obtain(tmp_path, archive)

    assert origin is Origin.COMPUTED
    assert (tmp_path / "out.h5").read_bytes() == b"output-Spectrum"
    assert any("WARNING" in line and "write" in line for line in logged)


def test_log_lines_name_the_packet_and_file_never_a_number(tmp_path):
    archive = FakeArchive()
    _, _, miss_log = _obtain(tmp_path, archive)
    _, _, hit_log = _obtain(tmp_path, archive)

    assert miss_log == ["archive miss: leapfrog_run a.PJNZ", "archive stored: leapfrog_run a.PJNZ"]
    assert hit_log == ["archive hit: leapfrog_run a.PJNZ"]
