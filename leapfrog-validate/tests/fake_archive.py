"""In-memory `Archive` double for tests of the code that *uses* the archive seam.

Same keyed-packet semantics as `OrderlyArchive` (exact key match, newest
wins, `extra` stored but never matched), with call recording so tests can
assert on hits, misses, and stores. Proves the seam is swappable: nothing
outside `archive.py` knows Orderly exists.
"""

import shutil
import subprocess
from collections.abc import Mapping
from dataclasses import dataclass, field
from pathlib import Path

import pytest


def _orderly_available() -> bool:
    if shutil.which("Rscript") is None:
        return False
    result = subprocess.run(["Rscript", "-e", "library(orderly)"], capture_output=True, text=True, check=False)
    return result.returncode == 0


requires_orderly = pytest.mark.skipif(not _orderly_available(), reason="R with the `orderly` package not available")


@dataclass
class FakeArchive:
    packets: list[tuple[str, dict[str, str], dict[str, str], bytes]] = field(default_factory=list)
    fetches: list[tuple[str, dict[str, str]]] = field(default_factory=list)
    stores: list[tuple[str, dict[str, str], dict[str, str]]] = field(default_factory=list)
    fail_fetch: Exception | None = None
    fail_store: Exception | None = None

    def fetch(self, report: str, key: Mapping[str, str], artefact: str, dest: Path) -> bool:
        del artefact
        self.fetches.append((report, dict(key)))
        if self.fail_fetch is not None:
            raise self.fail_fetch
        for packet_report, packet_key, _extra, content in reversed(self.packets):
            if packet_report == report and packet_key == dict(key):
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(content)
                return True
        return False

    def store(self, report: str, key: Mapping[str, str], extra: Mapping[str, str], artefact: str, source: Path) -> None:
        del artefact
        self.stores.append((report, dict(key), dict(extra)))
        if self.fail_store is not None:
            raise self.fail_store
        self.packets.append((report, dict(key), dict(extra), source.read_bytes()))
