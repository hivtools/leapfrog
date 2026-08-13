import numpy as np
import pytest

from leapfrog_validate.diff import Tolerance, diff_indicator, hybrid_tolerance_pass_mask

DEFAULT_TOLERANCE = Tolerance(atol=1e-3, rtol=1e-6)


def test_identical_arrays_pass():
    a = np.array([1.0, 100.0, 1e6])
    b = a.copy()
    verdict = diff_indicator(a, b, "total_population", DEFAULT_TOLERANCE)
    assert verdict.passed
    assert verdict.n_failed == 0
    assert verdict.max_abs_diff == 0.0


def test_diff_within_atol_passes():
    # atol=1e-3 alone should absorb a diff of 5e-4 even where ref is 0
    a = np.array([0.0])
    b = np.array([5e-4])
    verdict = diff_indicator(a, b, "total_population", DEFAULT_TOLERANCE)
    assert verdict.passed


def test_diff_just_over_atol_fails_at_zero_ref():
    # at ref=0, rtol contributes nothing, so atol is the whole budget
    a = np.array([0.0])
    b = np.array([1e-3 + 1e-9])
    verdict = diff_indicator(a, b, "total_population", DEFAULT_TOLERANCE)
    assert not verdict.passed
    assert verdict.n_failed == 1


def test_diff_exactly_at_boundary_passes():
    # pass_cell uses <=, so exactly atol + rtol*|ref| should pass
    ref = 1000.0
    tolerance = DEFAULT_TOLERANCE
    budget = tolerance.atol + tolerance.rtol * abs(ref)
    a = np.array([ref])
    b = np.array([ref + budget])
    verdict = diff_indicator(a, b, "total_population", tolerance)
    assert verdict.passed


def test_large_ref_value_gets_rtol_scaled_budget():
    # a big population count should tolerate a proportionally bigger diff
    # via rtol, even though atol alone would reject it
    ref = 1_000_000.0
    a = np.array([ref])
    b = np.array([ref + 0.5])  # bigger than atol, within rtol*|ref| = 1.0
    verdict = diff_indicator(a, b, "total_population", DEFAULT_TOLERANCE)
    assert verdict.passed


def test_strict_max_rollup_one_bad_cell_fails_whole_indicator():
    a = np.zeros(10)
    b = np.zeros(10)
    b[7] = 1.0  # single deliberately large diff
    verdict = diff_indicator(a, b, "total_population", DEFAULT_TOLERANCE)
    assert not verdict.passed
    assert verdict.n_failed == 1
    assert verdict.n_cells == 10
    assert verdict.max_abs_diff == 1.0


def test_shape_mismatch_raises():
    a = np.zeros((81, 2))
    b = np.zeros((81, 2, 61))
    with pytest.raises(ValueError, match="Shape mismatch"):
        diff_indicator(a, b, "total_population", DEFAULT_TOLERANCE)


def test_hybrid_tolerance_pass_mask_is_elementwise():
    a = np.array([0.0, 10.0, 1000.0])
    b = np.array([0.002, 10.0, 1000.002])
    mask = hybrid_tolerance_pass_mask(a, b, DEFAULT_TOLERANCE)
    # first cell: diff 0.002 > atol 1e-3 (ref=0 contributes no rtol budget) -> fail
    # second cell: identical -> pass
    # third cell: diff 0.002 <= atol 1e-3 + rtol*1000 = 1e-3 + 1e-3 = 2e-3 -> pass
    assert list(mask) == [False, True, True]


def test_verdict_summary_reports_pass_and_fail():
    passing = diff_indicator(np.zeros(3), np.zeros(3), "total_population", DEFAULT_TOLERANCE)
    assert passing.summary().startswith("PASS")

    b = np.zeros(3)
    b[0] = 5.0
    failing = diff_indicator(np.zeros(3), b, "total_population", DEFAULT_TOLERANCE)
    assert failing.summary().startswith("FAIL")
    assert "1/3" in failing.summary()


def test_exclude_mask_makes_an_over_tolerance_cell_pass():
    a = np.zeros(5)
    b = np.zeros(5)
    b[2] = 1.0
    exclude = np.zeros(5, dtype=bool)
    exclude[2] = True
    verdict = diff_indicator(a, b, "total_population", DEFAULT_TOLERANCE, exclude=exclude)
    assert verdict.passed
    assert verdict.n_failed == 0
    assert verdict.n_excluded == 1


def test_exclude_mask_does_not_hide_other_failing_cells():
    a = np.zeros(5)
    b = np.zeros(5)
    b[1] = 1.0
    b[2] = 1.0
    exclude = np.zeros(5, dtype=bool)
    exclude[2] = True
    verdict = diff_indicator(a, b, "total_population", DEFAULT_TOLERANCE, exclude=exclude)
    assert not verdict.passed
    assert verdict.n_failed == 1
    assert verdict.n_excluded == 1


def test_exclude_mask_shape_mismatch_raises():
    a = np.zeros((2, 3))
    b = np.zeros((2, 3))
    exclude = np.zeros((2, 4), dtype=bool)
    with pytest.raises(ValueError, match="Exclusion mask shape mismatch"):
        diff_indicator(a, b, "total_population", DEFAULT_TOLERANCE, exclude=exclude)


def test_summary_reports_excluded_count_when_nonzero():
    a = np.zeros(3)
    b = np.zeros(3)
    exclude = np.array([True, False, False])
    verdict = diff_indicator(a, b, "total_population", DEFAULT_TOLERANCE, exclude=exclude)
    assert "1 excluded" in verdict.summary()


def test_summary_omits_excluded_count_when_zero():
    verdict = diff_indicator(np.zeros(3), np.zeros(3), "total_population", DEFAULT_TOLERANCE)
    assert "excluded" not in verdict.summary()
