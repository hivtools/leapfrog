import numpy as np
from deepdiff import DeepDiff

from leapfrog_goals import (
    read_h5_file,
    run_goals,
    simple_sum,
)


def assert_equal(obj1, obj2):
    assert len(DeepDiff(obj1, obj2, ignore_nan_inequality=True)) == 0


def test_goals_model():
    assert 5==simple_sum(2, 3)
    parameters = read_h5_file(
        "../leapfrogr/tests/testthat/testdata/child_parms_full.h5"
    )
    parameters["ex_input"] = np.full((81, 2), 1)
    ret = run_goals(parameters)
    returned_vars = list(ret.keys())
    expected_vars = [
        "p_totpop",
        "births",
        "p_deaths_background_totpop",
        "p_hivpop",
        "p_deaths_background_hivpop",
        "h_hivpop",
        "h_artpop",
        "h_hiv_deaths_no_art",
        "p_infections",
        "h_hiv_deaths_art",
        "h_art_initiation",
        "h_deaths_excess_nonaids_no_art",
        "h_deaths_excess_nonaids_on_art",
        "p_deaths_excess_nonaids",
        "p_hiv_deaths",
        "p_net_migration_hivpop",
        "hiv_births",
        "hiv_births_by_mat_age",
        "prevalence_15to49_hts",
        "incidence_15to49_hts",
        "artcoverage_15to49_hts",
        "hc1_hivpop",
        "hc2_hivpop",
        "hc1_artpop",
        "hc2_artpop",
        "hc1_noart_aids_deaths",
        "hc2_noart_aids_deaths",
        "hc1_art_aids_deaths",
        "hc2_art_aids_deaths",
        "hc_art_init",
        "hc_art_need_init",
        "ctx_need",
        "infection_by_type",
        "mtct_by_source_tr",
        "mtct_by_source_women",
        "mtct_by_source_hc_infections",
        "pmtct_coverage_at_delivery",
        "ex_output",
    ]
    returned_vars.sort()
    expected_vars.sort()
    assert_equal(returned_vars, expected_vars)
