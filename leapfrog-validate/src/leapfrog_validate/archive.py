"""The archive seam: keyed packets of raw artefacts (ticket 24, built on ticket 12's decision).

An archive stores one file per packet, under a report name, and finds it
again by an exact key (a flat mapping of string parameters). Everything
that decides *what* the key is, or *when* to look, lives elsewhere
(`archived_run`, `spectrum_archive`) -- this module only knows how to put a
file in and get it back out. That keeps the compute logic apart from the
storage, and lets a different backend replace `OrderlyArchive` without
touching either.

`OrderlyArchive` is the real backend: an Orderly2 root (the R package is
called `orderly` on CRAN, formerly `orderly2`), driven through
`r_scripts/archive.R`. The report sources it needs ship in
`orderly_project/`. A *remote* is an Orderly location (a shared path, an
HTTP outpack server, a Packit server...) that packets are pulled from when
missing locally and pushed to after a store, so CI runs and developer
machines share one history.
"""

from __future__ import annotations

import json
import os
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from leapfrog_validate.subprocess_utils import run_checked

_SCRIPT = Path(__file__).parent / "r_scripts" / "archive.R"
_PROJECT = Path(__file__).parent / "orderly_project"

# Environment variables read by `archive_from_settings`' callers (the CLI,
# the regression driver, and the Spectrum driver) as defaults for their
# archive options. Unset or empty means "no archive": everything runs live,
# exactly as before ticket 24.
ENV_ROOT = "LEAPFROG_VALIDATE_ARCHIVE_ROOT"
ENV_REMOTE = "LEAPFROG_VALIDATE_ARCHIVE_REMOTE"
ENV_REMOTE_PATH = "LEAPFROG_VALIDATE_ARCHIVE_REMOTE_PATH"


class ArchiveError(RuntimeError):
    """Raised when the archive backend itself fails (not when a key is simply absent)."""


class Archive(Protocol):
    """Keyed-packet storage for one raw artefact per packet."""

    def fetch(self, report: str, key: Mapping[str, str], artefact: str, dest: Path) -> bool:
        """Copy the newest packet's `artefact` at exactly `key` to `dest`; return whether one existed."""
        ...

    def store(self, report: str, key: Mapping[str, str], extra: Mapping[str, str], artefact: str, source: Path) -> None:
        """Archive `source` as a new packet under `key` (plus `extra`, stored but never matched on)."""
        ...


@dataclass(frozen=True)
class OrderlyArchive:
    """An Orderly2 root, optionally backed by a named remote location.

    `remote_path`, if given with `remote`, registers `remote` as a *path*
    location at that directory the first time it is needed (and creates the
    directory as an Orderly root if it is new). A remote of any other kind
    (HTTP, Packit, ...) must already be registered in `root` by whoever set
    the archive up; then `remote` alone is enough.
    """

    root: Path
    remote: str | None = None
    remote_path: Path | None = None

    def _run(self, *args: str) -> str:
        cmd = ["Rscript", str(_SCRIPT), args[0], str(_PROJECT), str(self.root.resolve()), *args[1:]]
        if self.remote is not None:
            cmd.append(f"--remote={self.remote}")
            if self.remote_path is not None:
                cmd.append(f"--remote-path={self.remote_path.resolve()}")
        return run_checked(cmd, cwd=Path.cwd(), error_cls=ArchiveError, error_context=f"archive {args[0]}").stdout

    def fetch(self, report: str, key: Mapping[str, str], artefact: str, dest: Path) -> bool:
        """See `Archive.fetch`."""
        dest = dest.resolve()
        dest.parent.mkdir(parents=True, exist_ok=True)
        out = self._run("fetch", report, _json(key), artefact, str(dest))
        return out.strip().endswith("HIT")

    def store(self, report: str, key: Mapping[str, str], extra: Mapping[str, str], artefact: str, source: Path) -> None:
        """See `Archive.store`. `artefact` must match the report's declared artefact name."""
        del artefact  # fixed by the report definition; kept in the signature for other backends
        self._run("store", report, _json(key), _json(extra), str(source.resolve()))


def _json(mapping: Mapping[str, str]) -> str:
    return json.dumps(dict(mapping))


def archive_from_settings(root: Path | None, remote: str | None, remote_path: Path | None) -> Archive | None:
    """Build the configured archive, or `None` when no root is configured (archiving off)."""
    if root is None:
        return None
    return OrderlyArchive(root=root, remote=remote or None, remote_path=remote_path)


def settings_from_env() -> tuple[Path | None, str | None, Path | None]:
    """`(root, remote, remote_path)` from the `LEAPFROG_VALIDATE_ARCHIVE_*` env vars; empty means unset."""
    root = os.environ.get(ENV_ROOT) or None
    remote = os.environ.get(ENV_REMOTE) or None
    remote_path = os.environ.get(ENV_REMOTE_PATH) or None
    return (Path(root) if root else None, remote, Path(remote_path) if remote_path else None)
