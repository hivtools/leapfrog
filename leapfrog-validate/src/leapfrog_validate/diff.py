"""Hybrid atol + rtol*|ref| per-cell tolerance and strict-max rollup.

pass_cell(a, b, ref) = |a - b| <= atol + rtol * |ref|

`a` is treated as the reference value that `rtol` scales against (the
first artifact given to `diff`, conventionally the base ref being compared
against). Rollup is strict max: any single cell over tolerance fails the
whole indicator -- no fraction/percentile fuzzing.
"""

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class Tolerance:
    """The atol + rtol pair driving one indicator's hybrid pass_cell formula."""

    atol: float
    rtol: float


@dataclass
class Verdict:
    """Pass/fail result of diffing one indicator between two artifacts."""

    indicator: str
    passed: bool
    max_abs_diff: float
    n_cells: int
    n_failed: int
    n_excluded: int = 0

    def summary(self) -> str:
        """One-line PASS/FAIL report suitable for CLI output."""
        status = "PASS" if self.passed else "FAIL"
        excluded = f", {self.n_excluded} excluded" if self.n_excluded else ""
        return (
            f"{status}  {self.indicator}: max|delta|={self.max_abs_diff:.6g}, "
            f"{self.n_failed}/{self.n_cells} cells over tolerance{excluded}"
        )


def hybrid_tolerance_pass_mask(a: np.ndarray, b: np.ndarray, tolerance: Tolerance) -> np.ndarray:
    """Per-cell pass mask for the hybrid atol + rtol*|ref| formula, ref=a."""
    return np.abs(a - b) <= tolerance.atol + tolerance.rtol * np.abs(a)


def diff_indicator(
    a: np.ndarray,
    b: np.ndarray,
    indicator: str,
    tolerance: Tolerance,
    exclude: np.ndarray | None = None,
) -> Verdict:
    """Diff two same-shaped indicator arrays and roll up to a single Verdict.

    `exclude`, if given, is a same-shaped boolean mask of cells carved out by
    a reviewed `Exclusion` entry (see `leapfrog_validate.exclusions`) -- those
    cells always count as passing, regardless of the tolerance formula.
    """
    if a.shape != b.shape:
        msg = f"Shape mismatch for indicator '{indicator}': {a.shape} vs {b.shape}"
        raise ValueError(msg)
    if exclude is not None and exclude.shape != a.shape:
        msg = f"Exclusion mask shape mismatch for indicator '{indicator}': {exclude.shape} vs {a.shape}"
        raise ValueError(msg)

    pass_mask = hybrid_tolerance_pass_mask(a, b, tolerance)
    if exclude is not None:
        pass_mask = pass_mask | exclude
    n_cells = pass_mask.size
    n_failed = n_cells - int(np.count_nonzero(pass_mask))
    n_excluded = int(np.count_nonzero(exclude)) if exclude is not None else 0
    max_abs_diff = float(np.max(np.abs(a - b))) if n_cells else 0.0

    return Verdict(
        indicator=indicator,
        passed=n_failed == 0,
        max_abs_diff=max_abs_diff,
        n_cells=n_cells,
        n_failed=n_failed,
        n_excluded=n_excluded,
    )
