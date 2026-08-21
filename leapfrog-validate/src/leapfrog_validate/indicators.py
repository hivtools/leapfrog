"""Indicator registry: leapfrog output.h5 variable(s) -> comparable array.

The five blessed indicators (per `.scratch/leapfrog-validation/PRD.md` and
ticket 02's `research/indicator-mapping` findings), each defined through one
common shape: a leapfrog extractor, the regression-track `atol`/`rtol` per
ticket 07's hybrid formula, and an optional exclusion list (ticket 08's
registry pattern). Three indicators read a single output.h5 array directly;
the other two (`treatment_population`, `aids_deaths_on_treatment`) have no
`p_`-level array and are reconstructed by summing the adult (`h_`) and child
(`hc1_`/`hc2_`) arrays over CD4/duration and concatenating their age domains.

All extracted arrays share one (year, sex, age=81) shape, which
`leapfrog_validate.exclusions.exclusion_mask` relies on.
"""

from collections.abc import Callable
from pathlib import Path
from typing import TypedDict

import h5py
import numpy as np

from leapfrog_validate.diff import Tolerance
from leapfrog_validate.exclusions import Exclusion

# Regression-track rtol is uniform across indicators (ticket 07's Answer).
RTOL = 1e-6

# h_/hc1_/hc2_ arrays are (year, sex, age, cd4, duration) -- summing the last
# two axes collapses CD4 stage and treatment-duration stage, leaving the same
# (year, sex, age) shape the four direct indicators already have.
_CD4_DURATION_AXES = (-2, -1)


def extract_total_population(output_h5: Path) -> np.ndarray:
    """Read the p_totpop array (year x sex x age) out of a raw output.h5."""
    with h5py.File(output_h5, "r") as f:
        return f["p_totpop"][()]


def extract_hiv_population(output_h5: Path) -> np.ndarray:
    """Read the p_hivpop array (year x sex x age) out of a raw output.h5.

    Covers adult and pediatric ages alike -- the child model updates
    `p_hivpop` directly at child single-year ages (ticket 02's Answer).
    """
    with h5py.File(output_h5, "r") as f:
        return f["p_hivpop"][()]


def extract_aids_deaths_single_age(output_h5: Path) -> np.ndarray:
    """Read the p_hiv_deaths array (year x sex x age) out of a raw output.h5.

    Already combines adult + child, on-ART + off-ART deaths (ticket 02's
    Answer) -- no reconstruction needed, unlike `aids_deaths_on_treatment`.
    """
    with h5py.File(output_h5, "r") as f:
        return f["p_hiv_deaths"][()]


def _extract_summed_by_age_domain(
    output_h5: Path,
    adult_var: str,
    child_0_4_var: str,
    child_5_14_var: str,
) -> np.ndarray:
    """Sum one adult (h_) and two child (hc1_/hc2_) arrays into one (year, sex, age=81) array.

    No `p_`-level array exists for these indicators, so the three age
    domains -- ages 0-4 (`hc1AG`=5), 5-14 (`hc2AG`=10), 15-80 (`hAG`=66) --
    are summed over CD4/duration and concatenated in increasing-age order to
    span the same 81 single-year ages as the direct indicators (ticket 02's
    `research/indicator-mapping` findings).
    """
    with h5py.File(output_h5, "r") as f:
        adult = f[adult_var][()]
        child_0_4 = f[child_0_4_var][()]
        child_5_14 = f[child_5_14_var][()]

    return np.concatenate(
        [
            child_0_4.sum(axis=_CD4_DURATION_AXES),
            child_5_14.sum(axis=_CD4_DURATION_AXES),
            adult.sum(axis=_CD4_DURATION_AXES),
        ],
        axis=2,
    )


def extract_treatment_population(output_h5: Path) -> np.ndarray:
    """Sum h_artpop + hc1_artpop + hc2_artpop across CD4/duration -> (year, sex, age=81)."""
    return _extract_summed_by_age_domain(output_h5, "h_artpop", "hc1_artpop", "hc2_artpop")


def extract_aids_deaths_on_treatment(output_h5: Path) -> np.ndarray:
    """Sum h_hiv_deaths_art + hc1_art_aids_deaths + hc2_art_aids_deaths -> (year, sex, age=81)."""
    return _extract_summed_by_age_domain(output_h5, "h_hiv_deaths_art", "hc1_art_aids_deaths", "hc2_art_aids_deaths")


class IndicatorSpec(TypedDict):
    """A leapfrog extractor plus the tolerance and exclusions it's judged against."""

    extract: Callable[[Path], np.ndarray]
    tolerance: Tolerance
    exclusions: tuple[Exclusion, ...]


INDICATORS: dict[str, IndicatorSpec] = {
    "total_population": {
        "extract": extract_total_population,
        "tolerance": Tolerance(atol=1e-3, rtol=RTOL),
        "exclusions": (),
    },
    "hiv_population": {
        "extract": extract_hiv_population,
        "tolerance": Tolerance(atol=1e-3, rtol=RTOL),
        "exclusions": (),
    },
    "treatment_population": {
        "extract": extract_treatment_population,
        "tolerance": Tolerance(atol=1e-3, rtol=RTOL),
        "exclusions": (),
    },
    "aids_deaths_single_age": {
        "extract": extract_aids_deaths_single_age,
        "tolerance": Tolerance(atol=1e-4, rtol=RTOL),
        "exclusions": (),
    },
    "aids_deaths_on_treatment": {
        "extract": extract_aids_deaths_on_treatment,
        "tolerance": Tolerance(atol=1e-4, rtol=RTOL),
        "exclusions": (),
    },
}
