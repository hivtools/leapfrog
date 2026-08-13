"""Indicator registry: leapfrog output.h5 variable -> comparable array.

This is the walking-skeleton slice of the full five-indicator registry
described in the PRD (`.scratch/leapfrog-validation/PRD.md`) -- only
total_population is wired up here. Each entry carries a leapfrog extractor
plus the starting atol/rtol placeholders for the regression track
(rtol uniform across indicators, atol per-indicator).
"""

from collections.abc import Callable
from pathlib import Path
from typing import TypedDict

import h5py
import numpy as np


def extract_total_population(output_h5: Path) -> np.ndarray:
    """Read the p_totpop array (age x sex x year) out of a raw output.h5."""
    with h5py.File(output_h5, "r") as f:
        return f["p_totpop"][()]


class IndicatorSpec(TypedDict):
    """A leapfrog extractor plus the tolerance it's judged against."""

    extract: Callable[[Path], np.ndarray]
    atol: float
    rtol: float


INDICATORS: dict[str, IndicatorSpec] = {
    "total_population": {
        "extract": extract_total_population,
        "atol": 1e-3,
        "rtol": 1e-6,
    },
}
