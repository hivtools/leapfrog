from deepdiff import DeepDiff

from leapfrog_goals import (
    get_goals_ss,
    run_goals,
)
from SpectrumCommon.Util.LeapfrogDataMapping import modvars_to_leapfrog
from SpectrumCommon.Util.ConvertNumpy import modvars_to_numpy
from Tools.ImportPJNZ.Importer import GB_ImportProjectionFromFile
from SpectrumCommon.Const.PJ.PJNTags import PJN_FirstYearTag, PJN_FinalYearTag


def assert_equal(obj1, obj2):
    assert len(DeepDiff(obj1, obj2, ignore_nan_inequality=True)) == 0


def test_goals_model(test_data):
    modvars, _param, _epp, _shiny90 = GB_ImportProjectionFromFile(
        test_data / "SouthAfrica.PJNZ"
    )
    modvars = modvars_to_numpy(modvars)
    ss = get_goals_ss()
    lf_data = modvars_to_leapfrog(modvars, ss, "Goals")

    ret = run_goals(
        lf_data,
        output_years=range(modvars[PJN_FirstYearTag], modvars[PJN_FinalYearTag] + 1),
    )

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
        "hc_art_init_total",
        "hc_art_need_init",
        "ctx_need",
        "infection_by_type",
        "mtct_by_source_tr",
        "mtct_by_source_women",
        "mtct_by_source_hc_infections",
        "pmtct_coverage_at_delivery",
        "p_deaths_nonaids_artpop",
        "p_deaths_nonaids_hivpop",
        "p_excess_deaths_nonaids_on_art",
        "p_excess_deaths_nonaids_no_art",
    ]
    present = [var in returned_vars for var in expected_vars]
    assert(all(present))
