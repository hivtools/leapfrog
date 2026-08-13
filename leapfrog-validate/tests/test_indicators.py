"""Pure-Python tests for the indicator registry's extractors.

Uses small synthetic output.h5 fixtures -- no R build needed, mirroring
test_diff.py's approach for the tolerance/rollup math.
"""

from pathlib import Path

import h5py
import numpy as np

from leapfrog_validate.diff import Tolerance
from leapfrog_validate.indicators import (
    INDICATORS,
    extract_aids_deaths_on_treatment,
    extract_aids_deaths_single_age,
    extract_hiv_population,
    extract_total_population,
    extract_treatment_population,
)


def _write_h5(path: Path, **datasets: np.ndarray) -> Path:
    with h5py.File(path, "w") as f:
        for name, array in datasets.items():
            f.create_dataset(name, data=array)
    return path


def _art_like(shape: tuple[int, int, int, int, int], fill: float) -> np.ndarray:
    return np.full(shape, fill, dtype=float)


def test_extract_total_population_reads_p_totpop(tmp_path):
    arr = np.arange(3 * 2 * 4, dtype=float).reshape(3, 2, 4)
    output = _write_h5(tmp_path / "output.h5", p_totpop=arr)
    np.testing.assert_array_equal(extract_total_population(output), arr)


def test_extract_hiv_population_reads_p_hivpop(tmp_path):
    arr = np.arange(3 * 2 * 4, dtype=float).reshape(3, 2, 4)
    output = _write_h5(tmp_path / "output.h5", p_hivpop=arr)
    np.testing.assert_array_equal(extract_hiv_population(output), arr)


def test_extract_aids_deaths_single_age_reads_p_hiv_deaths(tmp_path):
    arr = np.arange(3 * 2 * 4, dtype=float).reshape(3, 2, 4)
    output = _write_h5(tmp_path / "output.h5", p_hiv_deaths=arr)
    np.testing.assert_array_equal(extract_aids_deaths_single_age(output), arr)


def test_extract_treatment_population_sums_cd4_duration_and_concatenates_age_domains(tmp_path):
    n_year, n_sex = 2, 2
    # hc1AG=2 (ages 0-4 domain), hc2AG=3 (ages 5-14 domain), hAG=4 (adult domain)
    h_artpop = _art_like((n_year, n_sex, 4, 7, 3), fill=1.0)
    hc1_artpop = _art_like((n_year, n_sex, 2, 7, 3), fill=2.0)
    hc2_artpop = _art_like((n_year, n_sex, 3, 6, 3), fill=3.0)
    output = _write_h5(tmp_path / "output.h5", h_artpop=h_artpop, hc1_artpop=hc1_artpop, hc2_artpop=hc2_artpop)

    result = extract_treatment_population(output)

    assert result.shape == (n_year, n_sex, 2 + 3 + 4)
    # each cell is fill_value * n_cd4 * n_dur, summed over those two axes;
    # age-domain order must be hc1 (0-4), hc2 (5-14), h (15-80)
    np.testing.assert_allclose(result[..., :2], 2.0 * 7 * 3)
    np.testing.assert_allclose(result[..., 2:5], 3.0 * 6 * 3)
    np.testing.assert_allclose(result[..., 5:], 1.0 * 7 * 3)


def test_extract_aids_deaths_on_treatment_sums_cd4_duration_and_concatenates_age_domains(tmp_path):
    n_year, n_sex = 2, 2
    h = _art_like((n_year, n_sex, 4, 7, 3), fill=0.5)
    hc1 = _art_like((n_year, n_sex, 2, 7, 3), fill=0.25)
    hc2 = _art_like((n_year, n_sex, 3, 6, 3), fill=0.1)
    output = _write_h5(
        tmp_path / "output.h5",
        h_hiv_deaths_art=h,
        hc1_art_aids_deaths=hc1,
        hc2_art_aids_deaths=hc2,
    )

    result = extract_aids_deaths_on_treatment(output)

    assert result.shape == (n_year, n_sex, 2 + 3 + 4)
    np.testing.assert_allclose(result[..., :2], 0.25 * 7 * 3)
    np.testing.assert_allclose(result[..., 2:5], 0.1 * 6 * 3)
    np.testing.assert_allclose(result[..., 5:], 0.5 * 7 * 3)


def test_registry_has_all_five_blessed_indicators():
    assert set(INDICATORS) == {
        "total_population",
        "hiv_population",
        "treatment_population",
        "aids_deaths_single_age",
        "aids_deaths_on_treatment",
    }


def test_every_indicator_shares_the_common_registry_shape():
    for spec in INDICATORS.values():
        assert callable(spec["extract"])
        assert isinstance(spec["tolerance"], Tolerance)
        assert isinstance(spec["exclusions"], tuple)


def test_rtol_is_uniform_across_indicators():
    rtols = {spec["tolerance"].rtol for spec in INDICATORS.values()}
    assert len(rtols) == 1
