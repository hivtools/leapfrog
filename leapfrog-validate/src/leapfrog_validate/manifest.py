"""Manifest of tags that can't be derived from a PJNZ's own contents.

Per ticket 09's Answer, reserved only for tags that aren't derivable at
all from what's inside the file -- e.g. "custom-made for this validation
system" provenance/purpose. Everything else comes from `classify`'s zip
peek / R import instead, so this stays deliberately small: a flat JSON
object mapping filename -> extra tags, not a general PJNZ database.

Known limitation: keyed by bare filename, not a corpus-relative path. The
real uploaded corpus has subfolders (e.g. `.../ETH/`), so two files
sharing a basename in different subfolders aren't distinguishable here --
acceptable for now since manifest entries are expected to be rare, but
worth revisiting (path-relative-to-corpus-root keys) if that collides in
practice or when ticket 20 wires a corpus root into the CLI.
"""

import json
from pathlib import Path


class ManifestError(RuntimeError):
    """Raised when a manifest file isn't a JSON object of filename -> tags."""


def load_manifest(manifest_path: Path) -> dict[str, frozenset[str]]:
    """Load a JSON manifest: `{"<pjnz filename>": ["tag1", "tag2"]}`.

    A missing file is treated as an empty manifest -- most corpora won't
    need one at all.
    """
    try:
        text = manifest_path.read_text()
    except FileNotFoundError:
        return {}

    try:
        raw = json.loads(text)
    except json.JSONDecodeError as e:
        msg = f"{manifest_path}: invalid JSON ({e})"
        raise ManifestError(msg) from e

    if not isinstance(raw, dict):
        msg = f"{manifest_path}: expected a JSON object of filename -> tags, got {type(raw).__name__}"
        raise ManifestError(msg)

    for filename, tags in raw.items():
        if not isinstance(tags, list) or not all(isinstance(tag, str) for tag in tags):
            msg = f"{manifest_path}: '{filename}' must map to a list of tag strings, got {tags!r}"
            raise ManifestError(msg)

    return {filename: frozenset(tags) for filename, tags in raw.items()}


def manifest_tags(manifest: dict[str, frozenset[str]], pjnz: Path) -> frozenset[str]:
    """Look up `pjnz`'s manifest tags by filename (not full path)."""
    return manifest.get(pjnz.name, frozenset())
