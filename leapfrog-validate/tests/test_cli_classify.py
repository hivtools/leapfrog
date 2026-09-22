"""CLI-level tests for `classify`, with `_prepare_ref` mocked.

`domain_tags` needs a real R environment (covered by
test_cli_integration.py's R-gated tests); the CLI wiring itself doesn't,
so it's tested here against a real, non-sensitive fixture with the build
step mocked out -- same boundary test_cli.py's `diff` tests draw around
what actually needs R.
"""

import json
from pathlib import Path
from unittest.mock import Mock, patch

from typer.testing import CliRunner

from leapfrog_validate import git_utils
from leapfrog_validate.cli import app

runner = CliRunner()

REPO_ROOT = git_utils.find_repo_root(Path(__file__).parent)
GOALS_FIXTURE = REPO_ROOT / "goals" / "tests" / "resources" / "SouthAfrica.PJNZ"


@patch("leapfrog_validate.cli._prepare_ref")
@patch("leapfrog_validate.classify.domain_tags")
def test_classify_prints_sorted_shape_and_domain_tags(mock_domain_tags, mock_prepare_ref):
    mock_prepare_ref.return_value = Mock()
    mock_domain_tags.return_value = frozenset({"has_pmtct"})

    result = runner.invoke(app, ["classify", "HEAD", str(GOALS_FIXTURE)])

    assert result.exit_code == 0
    assert result.stdout.splitlines() == ["goals", "has_pmtct"]


@patch("leapfrog_validate.cli._prepare_ref")
@patch("leapfrog_validate.classify.domain_tags")
def test_classify_merges_manifest_tags(mock_domain_tags, mock_prepare_ref, tmp_path):
    mock_prepare_ref.return_value = Mock()
    mock_domain_tags.return_value = frozenset()
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(json.dumps({"SouthAfrica.PJNZ": ["custom_made"]}))

    result = runner.invoke(app, ["classify", "HEAD", str(GOALS_FIXTURE), "--manifest", str(manifest_path)])

    assert result.exit_code == 0
    assert result.stdout.splitlines() == ["custom_made", "goals"]


def test_classify_rejects_a_nonexistent_manifest_path_instead_of_silently_ignoring_it(tmp_path):
    """Regression test: a typo'd --manifest path used to be silently treated as "no manifest"."""
    result = runner.invoke(
        app, ["classify", "HEAD", str(GOALS_FIXTURE), "--manifest", str(tmp_path / "does-not-exist.json")]
    )

    assert result.exit_code != 0
