"""The "get output.h5 for this ref and PJNZ" seam (ticket 01's seam; ticket 24's archive behind it).

Every caller that needs a leapfrog `output.h5` -- `run`, `compare`, the
regression driver, the Spectrum driver -- goes through `obtain_output`. It
checks the archive for a packet at the exact key first and only builds
params and runs the model on a miss, then archives what it computed.

What is archived is the raw `output.h5` and nothing derived from it
(ticket 12): indicator extraction and the pass/fail `diff` stay live
functions of the archived bytes, so a tolerance or indicator change
re-judges history without re-running any model.

The exact key is `pjnz` (label) + `pjnz_sha256` + `ref_sha` +
`configuration`. Two deliberate additions to ticket 24's "PJNZ + resolved
SHA": the PJNZ *content* hash (so an edited file under the same name never
serves a stale packet) and the model configuration (a different
configuration is a different output). The ref as the caller gave it
(`ref_given`) is stored on the packet for `latest(...)` lookups but is not
part of the key: the same commit reached by another name is the same
output. A reused packet keeps the `ref_given` of whoever stored it first.
"""

from __future__ import annotations

import hashlib
from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from leapfrog_validate.archive import Archive, ArchiveError
from leapfrog_validate.subprocess_utils import summarize_error_reason

RUN_REPORT = "leapfrog_run"
OUTPUT_ARTEFACT = "output.h5"


class Origin(Enum):
    """Where an `output.h5` came from."""

    ARCHIVE = "archive"
    COMPUTED = "computed"


@dataclass(frozen=True)
class RefIdentity:
    """A committed ref as given, and the full commit SHA it resolved to."""

    given: str
    sha: str


def file_sha256(path: Path) -> str:
    """SHA-256 hex digest of `path`'s contents."""
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def run_key(ref: RefIdentity, pjnz: Path, pjnz_label: str, configuration: str) -> dict[str, str]:
    """Return the exact archive key for one run."""
    return {
        "pjnz": pjnz_label,
        "pjnz_sha256": file_sha256(pjnz),
        "ref_sha": ref.sha,
        "configuration": configuration,
    }


def obtain_output(  # noqa: PLR0913 - one seam, every input explicit; callers pass keywords
    *,
    archive: Archive | None,
    ref: RefIdentity | None,
    pjnz: Path,
    pjnz_label: str,
    output_path: Path,
    configuration: str,
    compute: Callable[[], None],
    log: Callable[[str], None] = print,
) -> Origin:
    """Write `output_path` for `pjnz` at `ref`: reuse the archived packet, or compute and archive it.

    `ref=None` means an uncommitted working tree, which has no SHA to key
    on and is never archived. `compute` does the real work on a miss and
    must leave the raw output at `output_path`; it is never called on a
    hit, so if it closes over a `build.LazyWorkspace`, a fully cached run
    never builds leapfrogr at all.

    An archive failure is a logged warning, not a crash: the cache is an
    optimisation and the comparison is still correct without it. The cost
    is that a broken archive degrades quietly to "everything recomputes",
    so the warning line is the signal to watch for in CI logs.
    """
    use_archive = archive is not None and ref is not None
    key: dict[str, str] = {}
    if use_archive:
        key = run_key(ref, pjnz, pjnz_label, configuration)
        try:
            if archive.fetch(RUN_REPORT, key, OUTPUT_ARTEFACT, output_path):
                log(f"archive hit: {RUN_REPORT} {pjnz_label}")
                return Origin.ARCHIVE
        except ArchiveError as e:
            log(
                f"archive WARNING: could not read {RUN_REPORT} {pjnz_label}; "
                f"computing instead ({summarize_error_reason(e)})"
            )
        else:
            log(f"archive miss: {RUN_REPORT} {pjnz_label}")

    compute()

    if use_archive:
        try:
            archive.store(RUN_REPORT, key, {"ref_given": ref.given}, OUTPUT_ARTEFACT, output_path)
            log(f"archive stored: {RUN_REPORT} {pjnz_label}")
        except ArchiveError as e:
            log(
                f"archive WARNING: could not write {RUN_REPORT} {pjnz_label}; "
                f"result not archived ({summarize_error_reason(e)})"
            )
    return Origin.COMPUTED
