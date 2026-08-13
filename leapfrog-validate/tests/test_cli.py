"""CLI-level tests for `diff`, using small synthetic output.h5 fixtures.

`diff` only reads already-produced output.h5 files, so these don't need R --
unlike test_cli_integration.py's build-params/run coverage.
"""

from pathlib import Path

import h5py
import numpy as np
from typer.testing import CliRunner

from leapfrog_validate import indicators
from leapfrog_validate.cli import app
from leapfrog_validate.exclusions import Exclusion

runner = CliRunner()

ALL_INDICATOR_NAMES = [
    "total_population",
    "hiv_population",
    "treatment_population",
    "aids_deaths_single_age",
    "aids_deaths_on_treatment",
]


def _write_output_h5(path: Path, scale: float = 1.0) -> Path:
    n_year, n_sex = 2, 2
    hc1_age, hc2_age, h_age = 2, 3, 4
    total_age = hc1_age + hc2_age + h_age

    with h5py.File(path, "w") as f:
        f.create_dataset("p_totpop", data=np.full((n_year, n_sex, total_age), 100.0 * scale))
        f.create_dataset("p_hivpop", data=np.full((n_year, n_sex, total_age), 10.0 * scale))
        f.create_dataset("p_hiv_deaths", data=np.full((n_year, n_sex, total_age), 1.0 * scale))
        f.create_dataset("h_artpop", data=np.full((n_year, n_sex, h_age, 7, 3), 1.0 * scale))
        f.create_dataset("hc1_artpop", data=np.full((n_year, n_sex, hc1_age, 7, 3), 1.0 * scale))
        f.create_dataset("hc2_artpop", data=np.full((n_year, n_sex, hc2_age, 6, 3), 1.0 * scale))
        f.create_dataset("h_hiv_deaths_art", data=np.full((n_year, n_sex, h_age, 7, 3), 0.1 * scale))
        f.create_dataset("hc1_art_aids_deaths", data=np.full((n_year, n_sex, hc1_age, 7, 3), 0.1 * scale))
        f.create_dataset("hc2_art_aids_deaths", data=np.full((n_year, n_sex, hc2_age, 6, 3), 0.1 * scale))
    return path


def test_diff_all_indicators_pass_for_identical_artifacts(tmp_path):
    a = _write_output_h5(tmp_path / "a.h5")
    b = _write_output_h5(tmp_path / "b.h5")

    result = runner.invoke(app, ["diff", str(a), str(b)])

    assert result.exit_code == 0
    for name in ALL_INDICATOR_NAMES:
        assert f"PASS  {name}" in result.stdout


def test_diff_single_indicator_via_option(tmp_path):
    a = _write_output_h5(tmp_path / "a.h5")
    b = _write_output_h5(tmp_path / "b.h5")

    result = runner.invoke(app, ["diff", str(a), str(b), "--indicator", "hiv_population"])

    assert result.exit_code == 0
    assert "hiv_population" in result.stdout
    assert "total_population" not in result.stdout


def test_diff_invalid_indicator_errors(tmp_path):
    a = _write_output_h5(tmp_path / "a.h5")
    b = _write_output_h5(tmp_path / "b.h5")

    result = runner.invoke(app, ["diff", str(a), str(b), "--indicator", "nonsense"])

    assert result.exit_code == 2
    assert "Invalid indicator" in result.output


def test_diff_fails_overall_when_one_indicator_diverges(tmp_path):
    a = _write_output_h5(tmp_path / "a.h5", scale=1.0)
    b = _write_output_h5(tmp_path / "b.h5", scale=1.5)

    result = runner.invoke(app, ["diff", str(a), str(b)])

    assert result.exit_code == 1
    assert "FAIL" in result.stdout


def test_diff_pjnz_with_known_exclusion_passes_despite_out_of_tolerance_cell(tmp_path, monkeypatch):
    """Ticket 17's acceptance case.

    diff against a PJNZ with a known, reviewed exclusion passes despite a
    cell that is technically out of tolerance -- and the same diff without
    --pjnz (or with the wrong one) still fails, so the exclusion doesn't
    loosen tolerance for anyone else.
    """
    n_year, n_sex, n_age = 2, 2, 3
    a, b = tmp_path / "a.h5", tmp_path / "b.h5"
    arr_a = np.zeros((n_year, n_sex, n_age))
    arr_b = np.zeros((n_year, n_sex, n_age))
    arr_b[0, 0, 1] = 5.0  # deliberately out-of-tolerance cell at age index 1

    with h5py.File(a, "w") as f:
        f.create_dataset("p_totpop", data=arr_a)
    with h5py.File(b, "w") as f:
        f.create_dataset("p_totpop", data=arr_b)

    exclusion = Exclusion(
        pjnz="kenya",
        reason="known upstream rounding discrepancy at this age",
        link="https://github.com/hivtools/leapfrog/issues/999",
        age=(1, 1),
    )
    patched = dict(indicators.INDICATORS)
    patched["total_population"] = {**patched["total_population"], "exclusions": (exclusion,)}
    monkeypatch.setattr(indicators, "INDICATORS", patched)

    no_pjnz = runner.invoke(app, ["diff", str(a), str(b), "--indicator", "total_population"])
    assert no_pjnz.exit_code == 1

    wrong_pjnz = runner.invoke(app, ["diff", str(a), str(b), "--indicator", "total_population", "--pjnz", "uganda"])
    assert wrong_pjnz.exit_code == 1

    right_pjnz = runner.invoke(app, ["diff", str(a), str(b), "--indicator", "total_population", "--pjnz", "kenya"])
    assert right_pjnz.exit_code == 0
    # age index 1 excluded across all (year, sex) combinations: 2 years * 2 sexes = 4 cells
    assert "4 excluded" in right_pjnz.stdout
