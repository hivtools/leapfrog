"""Hybrid atol + rtol*|ref| per-cell tolerance and strict-max rollup.

pass_cell(a, b, ref) = |a - b| <= atol + rtol * |ref|

`a` is treated as the reference value that `rtol` scales against (the
first artifact given to `diff`, conventionally the base ref being compared
against). Rollup is strict max: any single cell over tolerance fails the
whole indicator -- no fraction/percentile fuzzing.
"""

from dataclasses import dataclass

import numpy as np


@dataclass
class Verdict:
    indicator: str
    passed: bool
    max_abs_diff: float
    n_cells: int
    n_failed: int

    def summary(self) -> str:
        status = "PASS" if self.passed else "FAIL"
        return (
            f"{status}  {self.indicator}: max|delta|={self.max_abs_diff:.6g}, "
            f"{self.n_failed}/{self.n_cells} cells over tolerance"
        )


def hybrid_tolerance_pass_mask(a: np.ndarray, b: np.ndarray, atol: float, rtol: float) -> np.ndarray:
    """Per-cell pass mask for the hybrid atol + rtol*|ref| formula, ref=a."""
    return np.abs(a - b) <= atol + rtol * np.abs(a)


def diff_indicator(a: np.ndarray, b: np.ndarray, indicator: str, atol: float, rtol: float) -> Verdict:
    if a.shape != b.shape:
        msg = f"Shape mismatch for indicator '{indicator}': {a.shape} vs {b.shape}"
        raise ValueError(msg)

    pass_mask = hybrid_tolerance_pass_mask(a, b, atol, rtol)
    n_cells = pass_mask.size
    n_failed = n_cells - int(np.count_nonzero(pass_mask))
    max_abs_diff = float(np.max(np.abs(a - b))) if n_cells else 0.0

    return Verdict(
        indicator=indicator,
        passed=n_failed == 0,
        max_abs_diff=max_abs_diff,
        n_cells=n_cells,
        n_failed=n_failed,
    )
