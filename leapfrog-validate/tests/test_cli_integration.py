"""Integration tests driving the CLI/library primitives end-to-end.

Per the PRD's Testing Decisions, the primary seam is process/run/diff
invoked against small, non-sensitive PJNZ fixtures, asserting on the
resulting pass/fail verdict -- not on any one indicator extractor's
internals. This actually builds leapfrogr (R + the C++ core it wraps) at
a real git ref, so it needs R and network access to CRAN/r-universe; it's
skipped when Rscript isn't on PATH rather than faked with a mock.
"""

import shutil
import subprocess
from pathlib import Path

import pytest

from leapfrog_validate import build, classify, git_utils, model_run, params
from leapfrog_validate.diff import diff_indicator
from leapfrog_validate.indicators import INDICATORS

requires_r = pytest.mark.skipif(shutil.which("Rscript") is None, reason="R is not installed")

REPO_ROOT = git_utils.find_repo_root(Path(__file__).parent)
FIXTURE_PJNZ = REPO_ROOT / "leapfrogr" / "inst" / "pjnz" / "france_default.PJNZ"
_PJNZ_DIR = REPO_ROOT / "leapfrogr" / "inst" / "pjnz"
BWA_ADULT_FIXTURE = _PJNZ_DIR / "bwa_aim-adult-art-no-special-elig_v6.13_2022-04-18.PJNZ"
BWA_NUMPMTCT_FIXTURE = _PJNZ_DIR / "bwa_aim-no-special-elig-numpmtct.PJNZ"
GOALS_FIXTURE = REPO_ROOT / "goals" / "tests" / "resources" / "SouthAfrica.PJNZ"


@pytest.fixture(scope="module")
def head_sha():
    return git_utils.resolve_ref(REPO_ROOT, "HEAD")


@pytest.fixture(scope="module")
def head_worktree(head_sha, tmp_path_factory):
    cache_dir = tmp_path_factory.mktemp("leapfrog-validate-cache")
    worktree = git_utils.ensure_worktree(REPO_ROOT, head_sha, cache_dir)
    yield worktree
    subprocess.run(
        ["git", "-C", str(REPO_ROOT), "worktree", "remove", "--force", str(worktree)],
        check=False,
    )


@pytest.fixture(scope="module")
def head_workspace(head_worktree):
    return build.build_leapfrogr(head_worktree)


@requires_r
def test_build_params_produces_a_readable_h5(head_workspace, tmp_path):
    output = tmp_path / "params.h5"
    params.build_params(head_workspace, FIXTURE_PJNZ, output)
    assert output.exists()
    assert output.stat().st_size > 0


@requires_r
def test_build_params_relative_output_resolves_against_caller_cwd(head_workspace, tmp_path, monkeypatch):
    """Regression test.

    A relative -o path must land next to where the user ran the command,
    not inside the cached build worktree the Rscript subprocess happens to
    run from (see params.build_params).
    """
    monkeypatch.chdir(tmp_path)
    params.build_params(head_workspace, FIXTURE_PJNZ, Path("relative_params.h5"))

    assert (tmp_path / "relative_params.h5").exists()
    assert not (head_workspace.worktree / "relative_params.h5").exists()


@requires_r
def test_run_relative_output_resolves_against_caller_cwd(head_workspace, tmp_path, monkeypatch):
    """Same regression as above, for run's --output (see model_run.run_model)."""
    params_path = tmp_path / "params.h5"
    params.build_params(head_workspace, FIXTURE_PJNZ, params_path)

    monkeypatch.chdir(tmp_path)
    model_run.run_model(head_workspace, params_path, Path("relative_output.h5"), "Spectrum")

    assert (tmp_path / "relative_output.h5").exists()
    assert not (head_workspace.worktree / "relative_output.h5").exists()


@requires_r
def test_run_then_diff_of_a_ref_against_itself_passes(head_workspace, tmp_path):
    """The walking-skeleton acceptance case: same ref twice must PASS.

    This exercises build-params -> run -> diff exactly as a developer would
    invoke them, and pins down the "identical refs never falsely fail"
    correctness property the tolerance formula depends on.
    """
    params_path = tmp_path / "params.h5"
    params.build_params(head_workspace, FIXTURE_PJNZ, params_path)

    output_a = tmp_path / "output-a.h5"
    output_b = tmp_path / "output-b.h5"
    model_run.run_model(head_workspace, params_path, output_a, "Spectrum")
    model_run.run_model(head_workspace, params_path, output_b, "Spectrum")

    spec = INDICATORS["total_population"]
    arr_a = spec["extract"](output_a)
    arr_b = spec["extract"](output_b)
    verdict = diff_indicator(arr_a, arr_b, "total_population", spec["tolerance"])

    assert verdict.passed, verdict.summary()
    assert verdict.max_abs_diff == 0.0


@requires_r
@pytest.mark.parametrize("pjnz", [FIXTURE_PJNZ, BWA_ADULT_FIXTURE, BWA_NUMPMTCT_FIXTURE])
def test_domain_tags_for_aim_only_fixtures(head_workspace, pjnz):
    """Ground truth verified empirically: all three AIM-only fixtures carry non-zero PMTCT/cotrim inputs."""
    assert classify.domain_tags(head_workspace, pjnz) == frozenset({"has_pmtct", "has_cotrim"})


@requires_r
def test_domain_tags_raises_for_goals_fixture_with_current_process_pjnz_limitation(head_workspace):
    """Regression-locking, not a desired outcome.

    `leapfrog::process_pjnz()` currently errors on this Goals-enabled PJNZ
    inside `process_pjnz_ha` (unrelated to this classifier -- see ticket
    16's comments). `domain_tags` surfaces that as `ClassifyError` rather
    than guessing tags, which is the correct behaviour either way; this
    pins down that it fails loudly instead of silently.
    """
    with pytest.raises(classify.ClassifyError):
        classify.domain_tags(head_workspace, GOALS_FIXTURE)


@requires_r
def test_classify_combines_shape_and_domain_tags_for_a_real_fixture(head_workspace):
    assert classify.classify(head_workspace, FIXTURE_PJNZ) == frozenset({"aim_only", "has_pmtct", "has_cotrim"})
