"""Tests for leapfrog_validate.manifest.

Per ticket 09's Answer: a manifest is reserved only for tags that aren't
derivable from a PJNZ's own contents at all (e.g. "custom-made for this
validation system" provenance) -- everything else comes from `classify`'s
zip peek / R import instead.
"""

import json
from pathlib import Path

import pytest

from leapfrog_validate import manifest


def _write(tmp_path: Path, content: str) -> Path:
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(content)
    return manifest_path


def test_load_manifest_returns_empty_dict_when_file_missing(tmp_path):
    assert manifest.load_manifest(tmp_path / "does-not-exist.json") == {}


def test_load_manifest_parses_filename_to_tags(tmp_path):
    manifest_path = _write(tmp_path, json.dumps({"foo.PJNZ": ["custom_made", "provenance:validation-system"]}))

    loaded = manifest.load_manifest(manifest_path)

    assert loaded == {"foo.PJNZ": frozenset({"custom_made", "provenance:validation-system"})}


def test_load_manifest_rejects_non_object_json(tmp_path):
    manifest_path = _write(tmp_path, json.dumps(["not", "an", "object"]))

    with pytest.raises(manifest.ManifestError):
        manifest.load_manifest(manifest_path)


def test_load_manifest_rejects_invalid_json(tmp_path):
    manifest_path = _write(tmp_path, "{not valid json,,,")

    with pytest.raises(manifest.ManifestError):
        manifest.load_manifest(manifest_path)


def test_load_manifest_rejects_a_bare_string_instead_of_a_tag_list(tmp_path):
    """Regression test: a bare string was silently exploded into one tag per character."""
    manifest_path = _write(tmp_path, json.dumps({"foo.PJNZ": "custom_made"}))

    with pytest.raises(manifest.ManifestError):
        manifest.load_manifest(manifest_path)


def test_load_manifest_rejects_non_string_items_in_tag_list(tmp_path):
    manifest_path = _write(tmp_path, json.dumps({"foo.PJNZ": ["ok", 123]}))

    with pytest.raises(manifest.ManifestError):
        manifest.load_manifest(manifest_path)


def test_manifest_tags_returns_empty_frozenset_for_unlisted_file(tmp_path):
    tags = manifest.manifest_tags({"other.PJNZ": frozenset({"x"})}, tmp_path / "foo.PJNZ")
    assert tags == frozenset()


def test_manifest_tags_looks_up_by_filename_not_full_path(tmp_path):
    loaded = {"foo.PJNZ": frozenset({"custom_made"})}

    tags = manifest.manifest_tags(loaded, tmp_path / "some" / "nested" / "dir" / "foo.PJNZ")

    assert tags == frozenset({"custom_made"})
