"""Spectrum's `extract` step, archived by PJNZ identity (ticket 24, built on ticket 12's decision).

Reading a PJNZ's Spectrum modvars does not depend on leapfrog's source at
all, so this packet is keyed by the PJNZ alone -- file label plus a hash of
its contents -- and never by a git ref. A hit skips the (slow, proprietary)
avenir importer.

What is archived are the *raw modvars* the five blessed indicators read
(plus the first/final year tags), not indicator arrays: the alignment to
leapfrog's year window, the sex totals, and the pass/fail diff all stay live
functions of the archived bytes (`spectrum_extract.extract_spectrum_*` take
them through their `modvars` argument). Ticket 12 described this artefact
as "indicator-shaped"; ticket 24's checklist says "extracted modvars" and
its never-archive-indicators rule decides it -- freezing indicator shapes
would pin history to today's indicator set.

The importer version is stored on the packet as provenance but is not part
of the key (the key is the PJNZ identity, per ticket 24). If a new importer
changes what it reads, clear or ignore the old packets.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from importlib import metadata
from pathlib import Path

import h5py
import numpy as np

from leapfrog_validate import spectrum_extract
from leapfrog_validate.archive import Archive, ArchiveError
from leapfrog_validate.archived_run import file_sha256
from leapfrog_validate.subprocess_utils import summarize_error_reason

EXTRACT_REPORT = "spectrum_extract"
EXTRACT_ARTEFACT = "extract.h5"

_IMPORTER_DISTRIBUTION = "avenir-spectrum-import-pjnz"


def blessed_modvar_tags() -> list[str]:
    """Every modvar tag the blessed Spectrum extractors read, plus the first/final year tags."""
    from SpectrumCommon.Const.AM.AMTags import (  # noqa: PLC0415
        AM_AIDSDeathsARTSingleAgeTag,
        AM_AIDSDeathsNoARTSingleAgeTag,
        AM_HIVBySingleAgeTag,
        AM_OnARTBySingleAgeTag,
    )
    from SpectrumCommon.Const.DP.DPTags import DP_BigPopTag  # noqa: PLC0415
    from SpectrumCommon.Const.PJ.PJNTags import PJN_FinalYearTag, PJN_FirstYearTag  # noqa: PLC0415

    return [
        PJN_FirstYearTag,
        PJN_FinalYearTag,
        DP_BigPopTag,
        AM_HIVBySingleAgeTag,
        AM_OnARTBySingleAgeTag,
        AM_AIDSDeathsARTSingleAgeTag,
        AM_AIDSDeathsNoARTSingleAgeTag,
    ]


def write_extract_h5(modvars: Mapping[str, object], path: Path) -> None:
    """Write each modvar as an HDF5 dataset named by its tag."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with h5py.File(path, "w") as f:
        for tag, value in modvars.items():
            f.create_dataset(tag, data=np.asarray(value))


def read_extract_h5(path: Path) -> dict:
    """Read an `extract.h5` back into a modvars dict (scalars as plain Python numbers)."""
    with h5py.File(path, "r") as f:
        return {tag: (f[tag][()].item() if f[tag].ndim == 0 else f[tag][()]) for tag in f}


def importer_version() -> str:
    """Installed version of the PJNZ importer, or "unknown"."""
    try:
        return metadata.version(_IMPORTER_DISTRIBUTION)
    except metadata.PackageNotFoundError:
        return "unknown"


def obtain_modvars(  # noqa: PLR0913 - one seam; callers pass keywords
    *,
    archive: Archive | None,
    pjnz: Path,
    pjnz_label: str,
    work_dir: Path,
    import_modvars: Callable[[Path], dict] | None = None,
    archived_tags: list[str] | None = None,
    log: Callable[[str], None] = print,
) -> dict:
    """Spectrum's modvars for `pjnz`: from the archive when present, imported live (and archived) otherwise.

    Without an archive this is just the live import, whole. With one, both a
    hit and a miss return the same archived subset of tags. An archive
    failure is a logged warning and falls back to the live import, same
    policy as `archived_run.obtain_output`. A failing import raises and
    archives nothing.
    """
    import_modvars = import_modvars or spectrum_extract.import_modvars
    if archive is None:
        return import_modvars(pjnz)

    key = {"pjnz": pjnz_label, "pjnz_sha256": file_sha256(pjnz)}
    extract_path = work_dir / EXTRACT_ARTEFACT
    try:
        if archive.fetch(EXTRACT_REPORT, key, EXTRACT_ARTEFACT, extract_path):
            log(f"archive hit: {EXTRACT_REPORT} {pjnz_label}")
            return read_extract_h5(extract_path)
    except ArchiveError as e:
        log(
            f"archive WARNING: could not read {EXTRACT_REPORT} {pjnz_label}; "
            f"importing instead ({summarize_error_reason(e)})"
        )
    else:
        log(f"archive miss: {EXTRACT_REPORT} {pjnz_label}")

    full = import_modvars(pjnz)
    tags = archived_tags if archived_tags is not None else blessed_modvar_tags()
    subset = {tag: full[tag] for tag in tags}
    write_extract_h5(subset, extract_path)
    try:
        archive.store(EXTRACT_REPORT, key, {"importer": importer_version()}, EXTRACT_ARTEFACT, extract_path)
        log(f"archive stored: {EXTRACT_REPORT} {pjnz_label}")
    except ArchiveError as e:
        log(
            f"archive WARNING: could not write {EXTRACT_REPORT} {pjnz_label}; result not archived "
            f"({summarize_error_reason(e)})"
        )
    return subset
