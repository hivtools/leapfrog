"""`OrderlyArchive` against a real, local Orderly root (ticket 24).

Needs R and the `orderly` R package; skipped when either is missing. The
archive seam's keyed-packet semantics are what these tests pin down: an
exact-key hit returns the stored bytes, any key difference is a miss, the
as-given ref is queryable, and a remote location carries packets between
two otherwise unrelated local roots.
"""

import subprocess
from pathlib import Path

import pytest
from fake_archive import requires_orderly

from leapfrog_validate.archive import ArchiveError, OrderlyArchive

REPORT = "leapfrog_run"
KEY = {"pjnz": "a.PJNZ", "pjnz_sha256": "abc", "ref_sha": "d" * 40, "configuration": "Spectrum"}
EXTRA = {"ref_given": "main"}


def _write(path: Path, content: bytes) -> Path:
    path.write_bytes(content)
    return path


@requires_orderly
def test_store_then_fetch_returns_the_stored_bytes(tmp_path):
    archive = OrderlyArchive(root=tmp_path / "archive")
    source = _write(tmp_path / "in.h5", b"model output")

    archive.store(REPORT, KEY, EXTRA, "output.h5", source)
    hit = archive.fetch(REPORT, KEY, "output.h5", tmp_path / "out.h5")

    assert hit is True
    assert (tmp_path / "out.h5").read_bytes() == b"model output"


@requires_orderly
def test_fetch_misses_on_an_empty_archive(tmp_path):
    archive = OrderlyArchive(root=tmp_path / "archive")

    hit = archive.fetch(REPORT, KEY, "output.h5", tmp_path / "out.h5")

    assert hit is False
    assert not (tmp_path / "out.h5").exists()


@requires_orderly
@pytest.mark.parametrize(
    "changed",
    [{"ref_sha": "e" * 40}, {"pjnz_sha256": "other"}, {"pjnz": "b.PJNZ"}, {"configuration": "Goals"}],
)
def test_any_key_difference_is_a_miss(tmp_path, changed):
    archive = OrderlyArchive(root=tmp_path / "archive")
    archive.store(REPORT, KEY, EXTRA, "output.h5", _write(tmp_path / "in.h5", b"x"))

    hit = archive.fetch(REPORT, {**KEY, **changed}, "output.h5", tmp_path / "out.h5")

    assert hit is False


@requires_orderly
def test_the_as_given_ref_is_not_part_of_the_exact_key(tmp_path):
    archive = OrderlyArchive(root=tmp_path / "archive")
    archive.store(REPORT, KEY, {"ref_given": "main"}, "output.h5", _write(tmp_path / "in.h5", b"x"))

    # Fetch takes the key only, so a caller that reached the same SHA via a
    # different ref name still reuses the packet.
    assert archive.fetch(REPORT, KEY, "output.h5", tmp_path / "out.h5") is True


@requires_orderly
def test_the_as_given_ref_is_stored_for_latest_lookups(tmp_path):
    root = tmp_path / "archive"
    archive = OrderlyArchive(root=root)
    archive.store(REPORT, KEY, {"ref_given": "my-branch"}, "output.h5", _write(tmp_path / "in.h5", b"x"))

    script = (
        f"cat(orderly::orderly_search('latest(parameter:ref_given == \"my-branch\")', "
        f'name = "{REPORT}", root = "{root}"))'
    )
    result = subprocess.run(["Rscript", "-e", script], capture_output=True, text=True, check=True)

    assert result.stdout.strip()  # a packet id, not NA


@requires_orderly
def test_the_newest_packet_wins_when_a_key_is_stored_twice(tmp_path):
    archive = OrderlyArchive(root=tmp_path / "archive")
    archive.store(REPORT, KEY, EXTRA, "output.h5", _write(tmp_path / "one.h5", b"first"))
    archive.store(REPORT, KEY, EXTRA, "output.h5", _write(tmp_path / "two.h5", b"second"))

    archive.fetch(REPORT, KEY, "output.h5", tmp_path / "out.h5")

    assert (tmp_path / "out.h5").read_bytes() == b"second"


@requires_orderly
def test_a_remote_carries_packets_between_unrelated_roots(tmp_path):
    remote_dir = tmp_path / "remote"
    writer = OrderlyArchive(root=tmp_path / "writer", remote="shared", remote_path=remote_dir)
    writer.store(REPORT, KEY, EXTRA, "output.h5", _write(tmp_path / "in.h5", b"from CI"))

    reader = OrderlyArchive(root=tmp_path / "reader", remote="shared", remote_path=remote_dir)
    hit = reader.fetch(REPORT, KEY, "output.h5", tmp_path / "out.h5")

    assert hit is True
    assert (tmp_path / "out.h5").read_bytes() == b"from CI"


@requires_orderly
def test_without_a_remote_two_roots_do_not_share_packets(tmp_path):
    OrderlyArchive(root=tmp_path / "one").store(REPORT, KEY, EXTRA, "output.h5", _write(tmp_path / "in.h5", b"x"))

    assert OrderlyArchive(root=tmp_path / "two").fetch(REPORT, KEY, "output.h5", tmp_path / "out.h5") is False


@requires_orderly
def test_an_unregistered_remote_without_a_path_is_a_clear_error(tmp_path):
    archive = OrderlyArchive(root=tmp_path / "archive", remote="nowhere")

    with pytest.raises(ArchiveError, match="nowhere"):
        archive.fetch(REPORT, KEY, "output.h5", tmp_path / "out.h5")
