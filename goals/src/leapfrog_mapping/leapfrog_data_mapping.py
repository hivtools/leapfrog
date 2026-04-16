import math
import numpy as np

from SpectrumCommon.Const.AM.AMTags import (
    AM_AdultAnnRateProgressLowerCD4Tag,
    AM_AdultDistNewInfectionsCD4Tag,
    AM_AdultMortByCD4NoARTTag,
    AM_AdultMortByCD4WithART0to6Tag,
    AM_AdultMortByCD4WithART7to12Tag,
    AM_AdultMortByCD4WithARTGT12Tag,
    AM_AdultNonAIDSExcessMortTag,
    AM_AgeHIVChildOnTreatmentTag,
    AM_ARVRegimenTag,
    AM_CD4ThreshHoldAdultsTag,
    AM_CD4ThreshHoldTag,
    AM_ChildAnnRateProgressLowerCD4Tag,
    AM_ChildARTByAgeGroupPerNumTag,
    AM_ChildARTDistTag,
    AM_ChildDistNewInfectionsCD4Tag,
    AM_ChildMortalityRatesTag,
    AM_ChildMortByCD4NoARTTag,
    AM_ChildMortByCD4WithART0to6PercTag,
    AM_ChildMortByCD4WithART0to6Tag,
    AM_ChildMortByCD4WithART7to12PercTag,
    AM_ChildMortByCD4WithART7to12Tag,
    AM_ChildMortByCD4WithARTGT12PercTag,
    AM_ChildMortByCD4WithARTGT12Tag,
    AM_ChildTreatInputsTag,
    AM_DistOfHIVTag,
    AM_EffectTreatChildTag,
    AM_EPPPopulationAgesTag,
    AM_FertCD4DiscountTag,
    AM_FRRbyLocationTag,
    AM_HAARTBySexPerNumTag,
    AM_HAARTBySexTag,
    AM_HIVSexRatioTag,
    AM_HIVTFRTag,
    AM_IncidenceByFitTag,
    AM_IncidenceOptionsTag,
    AM_InfantFeedingOptionsTag,
    AM_MortalityRatesMultiplierTag,
    AM_MortalityRatesTag,
    AM_NewARTPatAllocTag,
    AM_NosocomialInfectionsByAgeTag,
    AM_PatientsReallocatedTag,
    AM_PercentARTDeliveryTag,
    AM_PercInterruptedChildTag,
    AM_PercInterruptedTag,
    AM_PregTermAbortionPerNumTag,
    AM_PregTermAbortionTag,
    AM_RatioWomenOnARTTag,
    AM_TransEffAssumpTag,
)
from SpectrumCommon.Const.DP.DPConst import (
    DP_A0,
    DP_A14,
    DP_CD4_100_199,
    DP_CD4_15_24,
    DP_CD4_25_34,
    DP_CD4_35_44,
    DP_CD4_45_54,
    DP_CD4_50_99,
    DP_CD4_200_249,
    DP_CD4_250_349,
    DP_CD4_350_500,
    DP_CD4_GT500,
    DP_CD4_LT50,
    DP_A0t2,
    DP_A1t2,
    DP_A3t4,
    DP_A5t9,
    DP_A5t14,
    DP_A10t14,
    DP_AdvOpt_ART_ExpMort,
    DP_Age12to35Mths,
    DP_Age35to59Mths,
    DP_AgeGT5Years,
    DP_AgeLT11Mths,
    DP_AnnDropPostnatalProph,
    DP_ART0_12MthsBF,
    DP_ARTGT12MthsBF,
    DP_ARTStartDurPreg,
    DP_ARTStartDurPreg_Late,
    DP_ARTStartPrePreg,
    DP_BreastfeedingGE350,
    DP_BreastfeedingLT350,
    DP_CD4_0t4,
    DP_CD4_5t14,
    DP_CD4_Ped_200_349,
    DP_CD4_Ped_350_499,
    DP_CD4_Ped_500_749,
    DP_CD4_Ped_750_999,
    DP_CD4_Ped_GT1000,
    DP_CD4_Ped_LT200,
    DP_CD4_Per_5_10,
    DP_CD4_Per_11_15,
    DP_CD4_Per_16_20,
    DP_CD4_Per_21_25,
    DP_CD4_Per_26_30,
    DP_CD4_Per_GT30,
    DP_CD4_Per_LT5,
    DP_ChildEffNoART,
    DP_ChildEffWithART,
    DP_Data,
    DP_DualARV,
    DP_EPP_15t49,
    DP_InPMTCT,
    DP_MortRates_GT12Mo,
    DP_MortRates_LT12Mo,
    DP_NoProphExistInfCD4GT350,
    DP_NoProphExistInfCD4LT200,
    DP_NoProphExistInfCD4200_350,
    DP_NoProphIncidentInf,
    DP_NotInPMTCT,
    DP_NoTreat,
    DP_Number,
    DP_NumFertileAges,
    DP_OnART,
    DP_OnARTAtDelivery,
    DP_OptA,
    DP_OptB,
    DP_OptionA,
    DP_OptionB,
    DP_P_Perinatal,
    DP_Percent,
    DP_PerChildHIVPosCot,
    DP_PerChildHIVRecART,
    DP_PerChildHIVRecART0_4,
    DP_PerChildHIVRecART10_14,
    DP_Perinatal,
    DP_PrenatalProphylaxis,
    DP_SingleDoseNev,
    DP_SingleDoseNevir,
    DP_StartingARTAtDelivery,
    DP_TotalTreat,
    DP_TripleARTBefPreg,
    DP_TripleARTDurPreg,
    DP_TripleARTDurPreg_Late,
    DP_WHO2006DualARV,
    DP_FIRST_INDEX,
)
from SpectrumCommon.Const.DP.DPTags import (
    DP_ASFRTag,
    DP_BigPopTag,
    DP_MigrAgeDistTag,
    DP_MigrRateTag,
    DP_SexBirthRatioTag,
    DP_SurvRateTag,
    DP_TFRTag,
)
from SpectrumCommon.Const.GB.GBConst import (
    GB_A0_4,
    GB_A5_9,
    GB_A10_14,
    GB_A15_19,
    GB_A20_24,
    GB_A45_49,
    GB_A55_59,
    GB_A60_64,
    GB_A65_69,
    GB_A70_74,
    GB_A75_79,
    GB_A80_Up,
    GB_MAX_AGE,
    GB_AllAges,
    GB_Female,
    GB_Male,
    GB_MaxSingleAges,
    GB_NumSexes,
)

from SpectrumCommon.Const.HV.HVTags import (
    HVBehaviorTag,
    HVCondomPercentTag,
    HVInitialPulseTag,
)
from SpectrumCommon.Const.HV.HVConst import HV_MSMIDU, HV_MSM_F3, HV_AvgDur
from SpectrumCommon.Const.PJ.PJNTags import PJN_FirstYearTag, PJN_FinalYearTag

Modvars = dict[str, int | float | bool | np.ndarray | dict]

# Lepafrog runs with single-ages, use this to transfer from spectrum stored HIV age group to
# single year ages. Each item represents an index for single-year from 15 to 80+
transf_cd4_ag = [
    DP_CD4_15_24,
    DP_CD4_15_24,
    DP_CD4_15_24,
    DP_CD4_15_24,
    DP_CD4_15_24,
    DP_CD4_15_24,
    DP_CD4_15_24,
    DP_CD4_15_24,
    DP_CD4_15_24,
    DP_CD4_15_24,
    DP_CD4_25_34,
    DP_CD4_25_34,
    DP_CD4_25_34,
    DP_CD4_25_34,
    DP_CD4_25_34,
    DP_CD4_25_34,
    DP_CD4_25_34,
    DP_CD4_25_34,
    DP_CD4_25_34,
    DP_CD4_25_34,
    DP_CD4_35_44,
    DP_CD4_35_44,
    DP_CD4_35_44,
    DP_CD4_35_44,
    DP_CD4_35_44,
    DP_CD4_35_44,
    DP_CD4_35_44,
    DP_CD4_35_44,
    DP_CD4_35_44,
    DP_CD4_35_44,
    DP_CD4_45_54,
    DP_CD4_45_54,
    DP_CD4_45_54,
    DP_CD4_45_54,
    DP_CD4_45_54,
    DP_CD4_45_54,
    DP_CD4_45_54,
    DP_CD4_45_54,
    DP_CD4_45_54,
    DP_CD4_45_54,
    DP_CD4_45_54,
    DP_CD4_45_54,
    DP_CD4_45_54,
    DP_CD4_45_54,
    DP_CD4_45_54,
    DP_CD4_45_54,
    DP_CD4_45_54,
    DP_CD4_45_54,
    DP_CD4_45_54,
    DP_CD4_45_54,
    DP_CD4_45_54,
    DP_CD4_45_54,
    DP_CD4_45_54,
    DP_CD4_45_54,
    DP_CD4_45_54,
    DP_CD4_45_54,
    DP_CD4_45_54,
    DP_CD4_45_54,
    DP_CD4_45_54,
    DP_CD4_45_54,
    DP_CD4_45_54,
    DP_CD4_45_54,
    DP_CD4_45_54,
    DP_CD4_45_54,
    DP_CD4_45_54,
    DP_CD4_45_54,
]
transf_cd4_ds = [
    DP_CD4_GT500,
    DP_CD4_350_500,
    DP_CD4_250_349,
    DP_CD4_200_249,
    DP_CD4_100_199,
    DP_CD4_50_99,
    DP_CD4_LT50,
]


def modvars_to_leapfrog(modvars: Modvars, ss: dict):

    first_year = modvars[PJN_FirstYearTag]
    final_year = modvars[PJN_FinalYearTag]
    final_year_idx = final_year - first_year

    opts = _get_leapfrog_opts(modvars, final_year_idx)

    dp_modvars = _dp_modvars_leapfrog(modvars, final_year_idx)

    adult_modvars = _hiv_adult_modvars_leapfrog(modvars, final_year_idx, ss)

    child_modvars = _hiv_child_modvars_leapfrog(modvars, final_year_idx, ss)

    hv_modvars = _hv_modvars_leapfrog(modvars, final_year_idx)
    rn_modvars = _rn_modvars_leapfrog(modvars, final_year_idx)

    return {
        **opts,
        **dp_modvars,
        **adult_modvars,
        **child_modvars,
        **hv_modvars,
        **rn_modvars,
    }


def _get_t_art_start(modvars, final_year_idx):
    for t in range(final_year_idx + 1):
        if any(modvars[AM_HAARTBySexTag][GB_Male : GB_Female + 1, t] != 0):
            return t
    # There is no ART start date, so ensure we use a time later than the final
    # index so ART not run in leapfrog
    return final_year_idx + 1


def _get_leapfrog_opts(modvars, final_year_idx):
    t_art_start = _get_t_art_start(modvars, final_year_idx)

    return {
        "t_ART_start": t_art_start,
        "hts_per_year": 10,
        "projection_start_year": modvars[PJN_FirstYearTag],
        "projection_period": "calendar",
    }


def _dp_modvars_leapfrog(modvars: Modvars, final_year_idx: int):
    ## TODO: This get first year bigpop, is that right? What if we're running
    ## from 1980, not 1970. What index do we have in the data here vs
    ## We have first year above, but what idx will this correspond to?
    ## Does bigpop get truncated or does it always have 61 years? Look into this
    base_pop = modvars[DP_BigPopTag][
        GB_Male : (GB_Female + 1), : (GB_MaxSingleAges + 1), 0
    ].T.copy(order="F")

    ## MaxSingleAges + 3 because this is the probability of survival moving from
    ## age birth to end of year, 0 to 1, 1 to 2, ..., 79 to 80, 80-80+, 80+ to 80+
    ## So MaxSingleAges is 80, +1 for 80-80+ and + 1 for 80+ to 80+ and +1 for numpy indexing
    ## Starts counting at index 1 for this modvar
    survival_prob = modvars[DP_SurvRateTag][
        1 : (GB_MaxSingleAges + 3), GB_Male : (GB_Female + 1), : (final_year_idx + 1)
    ].copy(order="F")

    net_migration = np.zeros(
        (GB_MaxSingleAges + 1, GB_NumSexes, final_year_idx + 1), order="F"
    )

    # TODO: this is really messy, but we probably have to refactor
    # calc_single_ages to make it nicer
    for t in range(final_year_idx + 1):
        for s_idx, s in enumerate([GB_Male, GB_Female]):
            # Calc_Single_Ages is expecting to index a length 18 array, so we need to use
            # all ages here, even though Calc_Single_Ages doesn't use it
            migr_age_dist = modvars[DP_MigrAgeDistTag][
                s, GB_AllAges : (GB_MAX_AGE + 1), t
            ]
            migr_rate = modvars[DP_MigrRateTag][s, GB_AllAges, t]
            net_migr_5 = (migr_age_dist / 100) * migr_rate

            # TODO: Calc_Single_Ages reads really weird, why don't we have it return the
            # created list?
            net_migr = np.full((GB_MaxSingleAges + 1), 0).tolist()
            Calc_Single_Ages(modvars, net_migr_5.tolist(), net_migr, s)

            net_migration[:, s_idx, t] = net_migr

    asfr = _get_leapfrog_asfr(modvars, final_year_idx)

    births_sex_prop = np.zeros((GB_NumSexes, final_year_idx + 1), order="F")
    for t in range(final_year_idx + 1):
        births_sex_prop[GB_Male - GB_Male, t] = getSexBirthRatioPercent(
            modvars, GB_Male, t
        )
        births_sex_prop[GB_Female - GB_Male, t] = getSexBirthRatioPercent(
            modvars, GB_Female, t
        )

    tfr = modvars[DP_TFRTag]

    return {
        "basepop": base_pop,
        "Sx": survival_prob,
        "netmigr_adj": net_migration,
        "asfr": asfr,
        "births_sex_prop": births_sex_prop,
        "tfr": tfr,
    }


def _hiv_adult_modvars_leapfrog(modvars: Modvars, final_year_idx: int, ss: dict):
    incidence_option = modvars[AM_IncidenceOptionsTag]
    input_adult_incidence_rate = (
        modvars[AM_IncidenceByFitTag][incidence_option, : (final_year_idx + 1)] / 100
    ).copy(order="F")

    incrr_age_5year = (
        modvars[AM_DistOfHIVTag][
            GB_Male : (GB_Female + 1),
            GB_AllAges : (GB_MAX_AGE + 1),
            : (final_year_idx + 1),
        ]
        .transpose(2, 0, 1)
        .copy(order="F")
    )

    incrr_age_single = np.zeros(
        (final_year_idx + 1, GB_NumSexes, GB_MaxSingleAges + 1), order="F"
    )

    for t in range(final_year_idx + 1):
        for s_idx, s in enumerate([GB_Male, GB_Female]):
            incrr_age_slice = incrr_age_5year[t, s_idx, :].tolist()
            incrr_age_single_year = np.full((GB_MaxSingleAges + 1), 0.0).tolist()
            Calc_Single_Ages(modvars, incrr_age_slice, incrr_age_single_year, s)
            incrr_age_single[t, s_idx, :] = incrr_age_single_year

    incidence_rate_ratio_age = np.clip(
        incrr_age_single[:, :, ss["p_idx_hiv_first_adult"] :].transpose(2, 1, 0),
        0,
        None,
    ).copy(order="F")

    incidence_rate_ratio_sex = modvars[AM_HIVSexRatioTag][: (final_year_idx + 1)].copy(
        order="F"
    )

    # TODO: This has weird values for the first disease stage
    #  It has low negative values instead of 0s. Other than that the values
    # look quite good.
    cd4_mortality = np.zeros((ss["hDS"], ss["hAG"], ss["NS"]), order="F")
    for ds in range(ss["hDS"]):
        for a in range(ss["hAG"]):
            cd4_mortality[ds, a, :] = modvars[AM_AdultMortByCD4NoARTTag][
                DP_Data, GB_Male : (GB_Female + 1), transf_cd4_ag[a], transf_cd4_ds[ds]
            ]

    cd4_progression = np.zeros((ss["hDS"] - 1, ss["hAG"], ss["NS"]), order="F")
    for ds in range(ss["hDS"] - 1):
        for a in range(ss["hAG"]):
            rate = modvars[AM_AdultAnnRateProgressLowerCD4Tag][
                DP_Data, GB_Male : (GB_Female + 1), transf_cd4_ag[a], transf_cd4_ds[ds]
            ]
            cd4_progression[ds, a, :] = (
                1 - np.exp(-rate / ss["HIV_STEPS_PER_YEAR"])
            ) * ss["HIV_STEPS_PER_YEAR"]

    cd4_init_dist = np.zeros((ss["hDS"], ss["hAG"], ss["NS"]), order="F")
    for ds in range(ss["hDS"]):
        for a in range(ss["hAG"]):
            cd4_init_dist[ds, a, :] = (
                modvars[AM_AdultDistNewInfectionsCD4Tag][
                    DP_Data,
                    GB_Male : (GB_Female + 1),
                    transf_cd4_ag[a],
                    transf_cd4_ds[ds],
                ]
                / 100
            )

    cd4_thresholds = modvars[AM_CD4ThreshHoldAdultsTag][: (final_year_idx + 1)]
    idx_hm_elig = get_cd4_threshold_adult_idx(cd4_thresholds) - DP_CD4_GT500

    art_mortality = np.zeros((ss["hTS"], ss["hDS"], ss["hAG"], ss["NS"]), order="F")

    for ds in range(ss["hDS"]):
        cd4_cat = transf_cd4_ds[ds]
        for a in range(ss["hAG"]):
            age_group = transf_cd4_ag[a]
            art_mortality[0, ds, a, :] = modvars[AM_AdultMortByCD4WithART0to6Tag][
                DP_Data, GB_Male : (GB_Female + 1), age_group, cd4_cat
            ]
            art_mortality[1, ds, a, :] = modvars[AM_AdultMortByCD4WithART7to12Tag][
                DP_Data, GB_Male : (GB_Female + 1), age_group, cd4_cat
            ]
            art_mortality[2, ds, a, :] = modvars[AM_AdultMortByCD4WithARTGT12Tag][
                DP_Data, GB_Male : (GB_Female + 1), age_group, cd4_cat
            ]

    multiplier = modvars[AM_MortalityRatesMultiplierTag]
    mort_lt12 = modvars[AM_MortalityRatesTag][
        DP_Data, DP_MortRates_LT12Mo, : (final_year_idx + 1)
    ]
    mort_gt12 = modvars[AM_MortalityRatesTag][
        DP_Data, DP_MortRates_GT12Mo, : (final_year_idx + 1)
    ]

    art_mortality_time_rate_ratio = np.stack(
        [mort_lt12 * multiplier, mort_lt12 * multiplier, mort_gt12 * multiplier], axis=0
    ).copy(order="F")

    cd4_nonaids_excess_mort = np.zeros((ss["hDS"], ss["hAG"], ss["NS"]), order="F")
    art_nonaids_excess_mort = np.zeros(
        (ss["hTS"], ss["hDS"], ss["hAG"], ss["NS"]), order="F"
    )
    for ds in range(ss["hDS"]):
        for a in range(ss["hAG"]):
            cd4_nonaids_excess_mort[ds, a, :] = modvars[AM_AdultNonAIDSExcessMortTag][
                DP_Data,
                GB_Male : (GB_Female + 1),
                transf_cd4_ag[a],
                transf_cd4_ds[ds],
                DP_NoTreat,
            ]
            for ts in range(ss["hTS"]):
                art_nonaids_excess_mort[ts, ds, a, :] = modvars[
                    AM_AdultNonAIDSExcessMortTag
                ][
                    DP_Data,
                    GB_Male : (GB_Female + 1),
                    transf_cd4_ag[a],
                    transf_cd4_ds[ds],
                    DP_OnART,
                ]

    dropout_rate = -np.log(
        1.0 - modvars[AM_PercInterruptedTag][: (final_year_idx + 1)] / 100
    ).copy(order="F")

    adults_on_art = np.zeros((ss["NS"], final_year_idx + 1), order="F")
    adults_on_art_is_percent = np.zeros(
        (ss["NS"], final_year_idx + 1), dtype=np.int32, order="F"
    )

    for s_idx, s in enumerate([GB_Male, GB_Female]):
        is_percent = modvars[AM_HAARTBySexPerNumTag][s, : (final_year_idx + 1)]
        haart_values = modvars[AM_HAARTBySexTag][s, : (final_year_idx + 1)]

        adults_on_art_is_percent[s_idx, :] = is_percent
        adults_on_art[s_idx, :] = np.where(
            is_percent == DP_Percent, haart_values / 100, haart_values
        )

    h_art_stage_dur = np.full(ss["hTS"] - 1, 0.5, dtype=np.float64, order="F")

    initiation_mortality_weight = modvars[AM_NewARTPatAllocTag][DP_AdvOpt_ART_ExpMort]

    pag_incidpop = (
        ss["p_fertility_age_groups"]
        if modvars[AM_EPPPopulationAgesTag] == DP_EPP_15t49
        else ss["hAG"]
    )

    fert_mult_by_age = np.zeros((DP_NumFertileAges, final_year_idx + 1), order="F")
    fert_mult_on_art = np.zeros(DP_NumFertileAges, order="F")

    for a in range(DP_NumFertileAges):
        five_year_age_group = (a // 5) + GB_A15_19
        fert_mult_on_art[a] = modvars[AM_RatioWomenOnARTTag][
            DP_Data, five_year_age_group
        ]
        fert_mult_by_age[a, :] = modvars[AM_HIVTFRTag][
            DP_Data, five_year_age_group, : (final_year_idx + 1)
        ]

    fert_mult_off_art = modvars[AM_FertCD4DiscountTag][
        DP_Data, DP_CD4_GT500 : (DP_CD4_LT50 + 1)
    ].copy(order="F")

    local_adj_factor = modvars[AM_FRRbyLocationTag][DP_Data]

    return {
        "incidence_model_choice": 0,  # Turn off the incidence model
        "incidinput": input_adult_incidence_rate,
        "transmission_rate_hts": np.full(
            (final_year_idx + 1) * ss["HIV_STEPS_PER_YEAR"], 0.0
        ),  # Only used by incidence model
        "initial_incidence": 0.0,  # Only used by incidence model
        "epidemic_start_hts": (final_year_idx + 1)
        * ss["HIV_STEPS_PER_YEAR"],  # Only used by incidence model
        "relative_infectiousness_art": 0.1,  # Only used by incidence model
        "incrr_age": incidence_rate_ratio_age,
        "incrr_sex": incidence_rate_ratio_sex,
        "cd4_mort": cd4_mortality,
        "cd4_prog": cd4_progression,
        "cd4_initdist": cd4_init_dist,
        "scale_cd4_mort": 1,  # Always 1
        "artcd4elig_idx": idx_hm_elig,
        "art_mort": art_mortality,
        "artmx_timerr": art_mortality_time_rate_ratio,
        "cd4_nonaids_excess_mort": cd4_nonaids_excess_mort,
        "art_nonaids_excess_mort": art_nonaids_excess_mort,
        "art_dropout_recover_cd4": 1,  # Always 1
        "art_dropout_rate": dropout_rate,
        "art15plus_num": adults_on_art,
        "art15plus_isperc": adults_on_art_is_percent,
        "art_alloc_mxweight": initiation_mortality_weight,
        "h_art_stage_dur": h_art_stage_dur,
        "pAG_INCIDPOP": pag_incidpop,
        "pIDX_INCIDPOP": 15,  # Always 15
        "fert_rat": fert_mult_by_age,
        "cd4fert_rat": fert_mult_off_art,
        "frr_art6mos": fert_mult_on_art,
        "frr_scalar": local_adj_factor,
    }


def _hiv_child_modvars_leapfrog(modvars: Modvars, final_year_idx: int, ss: dict):
    hc_nosocomial = modvars[AM_NosocomialInfectionsByAgeTag][
        GB_A0_4, : (final_year_idx + 1)
    ].copy(order="F")

    hc1_cd4_dist = (
        modvars[AM_ChildDistNewInfectionsCD4Tag][
            DP_Data, DP_CD4_Per_GT30 : (DP_CD4_Per_LT5 + 1)
        ]
        / 100
    ).copy(order="F")

    hc1_cd4_mort = np.zeros((ss["hc1DS"], ss["hcTT"], ss["hc1AG"]), order="F")
    age_mapping_hc1 = [DP_A0t2, DP_A0t2, DP_A0t2, DP_A3t4, DP_A3t4]
    for c in range(ss["hc1DS"]):
        cd4_cat = c + DP_CD4_Per_GT30
        for d in range(ss["hcTT"]):
            trans_type = d + DP_P_Perinatal
            for a in range(ss["hc1AG"]):
                age_group = age_mapping_hc1[a]
                hc1_cd4_mort[c, d, a] = modvars[AM_ChildMortByCD4NoARTTag][
                    DP_Data, age_group, trans_type, cd4_cat
                ]

    hc2_cd4_mort = np.zeros((ss["hc2DS"], ss["hcTT"], ss["hc2AG"]), order="F")
    for c in range(ss["hc2DS"]):
        cd4_cat = c + DP_CD4_Ped_GT1000
        for d in range(ss["hcTT"]):
            trans_type = d + DP_P_Perinatal
            for a in range(ss["hc2AG"]):
                hc2_cd4_mort[c, d, a] = modvars[AM_ChildMortByCD4NoARTTag][
                    DP_Data, DP_A5t14, trans_type, cd4_cat
                ]

    hc1_cd4_prog = np.zeros((ss["hc1DS"], ss["hc1AG_c"], ss["NS"]), order="F")
    for a_idx in range(ss["hc1AG_c"]):
        age_group = a_idx + DP_A0t2
        for s_idx, s in enumerate([GB_Male, GB_Female]):
            for c in range(ss["hc1DS"] - 1):
                cd4_cat = c + DP_CD4_Per_GT30
                hc1_cd4_prog[c, a_idx, s_idx] = modvars[
                    AM_ChildAnnRateProgressLowerCD4Tag
                ][DP_Data, s, age_group, cd4_cat]

    hc2_cd4_prog = np.zeros((ss["hc2DS"], ss["hc2AG_c"], ss["NS"]), order="F")
    for s_idx, s in enumerate([GB_Male, GB_Female]):
        for c in range(ss["hc2DS"] - 1):
            cd4_cat = c + DP_CD4_Ped_GT1000
            hc2_cd4_prog[c, 0, s_idx] = modvars[AM_ChildAnnRateProgressLowerCD4Tag][
                DP_Data, s, DP_A5t14, cd4_cat
            ]

    ctx_val = np.zeros(final_year_idx + 1, order="F")
    ctx_val_is_percent = np.zeros(final_year_idx + 1, dtype=np.int32, order="F")
    hc_art_val = np.zeros((ss["hcAG_coarse"], final_year_idx + 1), order="F")
    hc_art_is_percent = np.zeros(final_year_idx + 1, dtype=np.int32, order="F")
    hc_art_is_age_spec = np.zeros(final_year_idx + 1, dtype=np.int32, order="F")

    hc_art_start = 0

    for t in range(final_year_idx + 1):
        ctx_val_is_percent[t] = int(
            modvars[AM_ChildARTByAgeGroupPerNumTag][DP_PerChildHIVPosCot, t]
        )
        ctx_value = modvars[AM_ChildTreatInputsTag][DP_PerChildHIVPosCot, t]
        if ctx_val_is_percent[t] == DP_Percent:
            ctx_val[t] = ctx_value / 100
        else:
            ctx_val[t] = ctx_value

        hc_art_is_percent[t] = int(
            modvars[AM_ChildARTByAgeGroupPerNumTag][DP_PerChildHIVRecART, t]
        )
        hc_art_has_value = False
        for a in range(DP_PerChildHIVRecART, DP_PerChildHIVRecART10_14 + 1):
            value = modvars[AM_ChildTreatInputsTag][a, t]

            if value != -9999:  # -9999 is used as NA value
                if hc_art_is_percent[t] == DP_Percent:
                    hc_art_val[a - DP_PerChildHIVRecART, t] = value / 100
                else:
                    hc_art_val[a - DP_PerChildHIVRecART, t] = value
                hc_art_has_value = hc_art_has_value or (value > 0)
            else:
                hc_art_val[a - DP_PerChildHIVRecART, t] = 0

        if modvars[AM_ChildTreatInputsTag][DP_PerChildHIVRecART0_4, t] != -9999:
            hc_art_is_age_spec[t] = 1
        else:
            hc_art_is_age_spec[t] = 0

        if hc_art_start == 0 and hc_art_has_value:
            hc_art_start = t

    ctx_effect = np.zeros(3, order="F")
    ctx_effect[0] = np.mean(
        modvars[AM_EffectTreatChildTag][DP_Data, DP_ChildEffNoART, 1:6]
    )
    ctx_effect[1] = modvars[AM_EffectTreatChildTag][DP_Data, DP_ChildEffWithART, 1]
    ctx_effect[2] = np.mean(
        modvars[AM_EffectTreatChildTag][DP_Data, DP_ChildEffWithART, 2:6]
    )

    hc_art_elig_age = (
        (modvars[AM_AgeHIVChildOnTreatmentTag][: (final_year_idx + 1)] // 12)
        .astype(np.int32)
        .copy(order="F")
    )

    hc_art_elig_cd4 = np.zeros(
        (ss["p_idx_hiv_first_adult"], final_year_idx + 1), dtype=np.int32, order="F"
    )

    for a in range(ss["p_idx_hiv_first_adult"]):
        # Determine age group and percent/number
        if a == 0:
            a1 = DP_AgeLT11Mths
            p = DP_Percent
        elif a in [1, 2]:
            a1 = DP_Age12to35Mths
            p = DP_Percent
        elif a in [3, 4]:
            a1 = DP_Age35to59Mths
            p = DP_Percent
        else:  # 5-14
            a1 = DP_AgeGT5Years
            p = DP_Number

        for t in range(final_year_idx + 1):
            threshold = modvars[AM_CD4ThreshHoldTag][p, a1, t]
            cd4_idx = get_cd4_threshold_child_idx(threshold, p)

            if p == DP_Number:
                hc_art_elig_cd4[a, t] = cd4_idx - DP_CD4_Ped_GT1000
            else:
                hc_art_elig_cd4[a, t] = cd4_idx - DP_CD4_Per_GT30

    hc_art_mort_rr = np.zeros(
        (ss["hTS"], ss["p_idx_hiv_first_adult"], final_year_idx + 1), order="F"
    )
    for a in range(ss["p_idx_hiv_first_adult"]):
        if a <= 4:
            a2 = DP_CD4_0t4
        else:
            a2 = DP_CD4_5t14

        for t in range(final_year_idx + 1):
            mort_lt12 = modvars[AM_ChildMortalityRatesTag][
                DP_Data, a2, DP_MortRates_LT12Mo, t
            ]
            mort_gt12 = modvars[AM_ChildMortalityRatesTag][
                DP_Data, a2, DP_MortRates_GT12Mo, t
            ]

            hc_art_mort_rr[0, a, t] = mort_lt12
            hc_art_mort_rr[1, a, t] = mort_lt12
            hc_art_mort_rr[2, a, t] = mort_gt12

    hc1_art_mort = np.zeros((ss["hc1DS"], ss["hTS"], ss["hc1AG"]), order="F")
    age_mapping_hc1_art = [DP_A0, DP_A1t2, DP_A1t2, DP_A3t4, DP_A3t4]
    for c in range(ss["hc1DS"]):
        cd4_cat = c + DP_CD4_Per_GT30
        for a in range(ss["hc1AG"]):
            age_group = age_mapping_hc1_art[a]
            hc1_art_mort[c, 0, a] = modvars[AM_ChildMortByCD4WithART0to6PercTag][
                DP_Data, GB_Male, age_group, cd4_cat
            ]
            hc1_art_mort[c, 1, a] = modvars[AM_ChildMortByCD4WithART7to12PercTag][
                DP_Data, GB_Male, age_group, cd4_cat
            ]
            hc1_art_mort[c, 2, a] = modvars[AM_ChildMortByCD4WithARTGT12PercTag][
                DP_Data, GB_Male, age_group, cd4_cat
            ]

    hc2_art_mort = np.zeros((ss["hc2DS"], ss["hTS"], ss["hc2AG"]), order="F")
    for c in range(ss["hc2DS"]):
        cd4_cat = c + DP_CD4_Ped_GT1000
        for a in range(5, 15):  # Ages 5-14
            # Map to age group
            if a <= 9:
                age_group = DP_A5t9
            else:
                age_group = DP_A10t14

            a_idx = a - 5
            hc2_art_mort[c, 0, a_idx] = modvars[AM_ChildMortByCD4WithART0to6Tag][
                DP_Data, GB_Male, age_group, cd4_cat
            ]
            hc2_art_mort[c, 1, a_idx] = modvars[AM_ChildMortByCD4WithART7to12Tag][
                DP_Data, GB_Male, age_group, cd4_cat
            ]
            hc2_art_mort[c, 2, a_idx] = modvars[AM_ChildMortByCD4WithARTGT12Tag][
                DP_Data, GB_Male, age_group, cd4_cat
            ]

    hc_art_init_dist = modvars[AM_ChildARTDistTag][
        DP_Data, DP_A0 : (DP_A14 + 1), : (final_year_idx + 1)
    ].copy(order="F")

    # Shape: (hDS+1, hVT) where hDS=7 adult CD4 categories + 1 for incident
    vertical_transmission_rate = np.zeros((ss["hDS"] + 1, ss["hVT"]), order="F")

    vt_mapping = [
        # CD4 categories for existing infections (indices 0-6)
        (DP_NoProphExistInfCD4GT350, DP_Perinatal, DP_BreastfeedingGE350),
        (DP_NoProphExistInfCD4GT350, DP_Perinatal, DP_BreastfeedingGE350),
        (DP_NoProphExistInfCD4200_350, DP_Perinatal, DP_BreastfeedingLT350),
        (DP_NoProphExistInfCD4200_350, DP_Perinatal, DP_BreastfeedingLT350),
        (DP_NoProphExistInfCD4LT200, DP_Perinatal, DP_BreastfeedingLT350),
        (DP_NoProphExistInfCD4LT200, DP_Perinatal, DP_BreastfeedingLT350),
        (DP_NoProphExistInfCD4LT200, DP_Perinatal, DP_BreastfeedingLT350),
    ]

    for idx, (cd4_status, peri_type, bf_type) in enumerate(vt_mapping):
        vertical_transmission_rate[idx, 0] = (
            modvars[AM_TransEffAssumpTag][DP_Data, cd4_status, peri_type] / 100
        )
        vertical_transmission_rate[idx, 1] = (
            modvars[AM_TransEffAssumpTag][DP_Data, cd4_status, bf_type] / 100
        )

    # Incident infections (index 7)
    vertical_transmission_rate[7, 0] = (
        modvars[AM_TransEffAssumpTag][DP_Data, DP_NoProphIncidentInf, DP_Perinatal]
        / 100
    )
    vertical_transmission_rate[7, 1] = (
        modvars[AM_TransEffAssumpTag][
            DP_Data, DP_NoProphIncidentInf, DP_BreastfeedingLT350
        ]
        / 100
    )

    pmtct_dropout = np.zeros(
        (ss["hPS"], ss["hVT_dropout"], final_year_idx + 1), order="F"
    )
    pmtct_dropout[:, 0, :] = 1

    for t in range(final_year_idx + 1):
        pmtct_dropout[4, 0, t] = (
            modvars[AM_PercentARTDeliveryTag][DP_OnARTAtDelivery, t] / 100
        )
        pmtct_dropout[5, 0, t] = (
            modvars[AM_PercentARTDeliveryTag][DP_StartingARTAtDelivery, t] / 100
        )
        dropout_0_12 = (
            modvars[AM_ARVRegimenTag][
                DP_AnnDropPostnatalProph, DP_ART0_12MthsBF, DP_Percent, t
            ]
            / 100
        )
        dropout_gt12 = (
            modvars[AM_ARVRegimenTag][
                DP_AnnDropPostnatalProph, DP_ARTGT12MthsBF, DP_Percent, t
            ]
            / 100
        )

        for strat in [0, 1, 4, 5, 6]:
            pmtct_dropout[strat, 1, t] = dropout_0_12
            pmtct_dropout[strat, 2, t] = dropout_gt12

    pmtct = np.zeros((ss["hPS"], final_year_idx + 1), order="F")
    pmtct_input_is_percent = np.zeros(final_year_idx + 1, dtype=np.int32, order="F")

    pmtct_options = [
        DP_OptA,
        DP_OptB,
        DP_SingleDoseNevir,
        DP_DualARV,
        DP_TripleARTBefPreg,
        DP_TripleARTDurPreg,
        DP_TripleARTDurPreg_Late,
    ]

    for t in range(final_year_idx + 1):
        total_number = modvars[AM_ARVRegimenTag][
            DP_PrenatalProphylaxis, DP_TotalTreat, DP_Number, t
        ]

        if total_number > 0:
            pmtct_input_is_percent[t] = 0
            p_type = DP_Number
        else:
            pmtct_input_is_percent[t] = 1
            p_type = DP_Percent

        for idx, option in enumerate(pmtct_options):
            value = modvars[AM_ARVRegimenTag][DP_PrenatalProphylaxis, option, p_type, t]
            pmtct[idx, t] = value if p_type == DP_Percent else value

    pmtct_transmission_rate = np.zeros((ss["hDS"], ss["hPS"], ss["hVT"]), order="F")

    pmtct_trans_options = [
        DP_OptionA,
        DP_OptionB,
        DP_SingleDoseNev,
        DP_WHO2006DualARV,
        DP_ARTStartPrePreg,
        DP_ARTStartDurPreg,
        DP_ARTStartDurPreg_Late,
    ]

    for cd4_cat in range(DP_CD4_GT500, DP_CD4_LT50 + 1):  # CD4 categories
        c_idx = cd4_cat - DP_CD4_GT500

        # Perinatal transmission (all strategies)
        for strat_idx, strat in enumerate(pmtct_trans_options):
            pmtct_transmission_rate[c_idx, strat_idx, 0] = (
                modvars[AM_TransEffAssumpTag][DP_Data, strat, DP_Perinatal] / 100
            )

        # Breastfeeding transmission
        # DualARV same for all CD4
        pmtct_transmission_rate[c_idx, 3, 1] = (
            modvars[AM_TransEffAssumpTag][
                DP_Data, DP_WHO2006DualARV, DP_BreastfeedingLT350
            ]
            / 100
        )

        if cd4_cat <= DP_CD4_350_500:
            # High CD4 (>350)
            pmtct_transmission_rate[c_idx, 0, 1] = 0
            pmtct_transmission_rate[c_idx, 1, 1] = 0
            pmtct_transmission_rate[c_idx, 2, 1] = (
                modvars[AM_TransEffAssumpTag][
                    DP_Data, DP_SingleDoseNev, DP_BreastfeedingLT350
                ]
                / 100
            )
            pmtct_transmission_rate[c_idx, 4, 1] = 0
            pmtct_transmission_rate[c_idx, 5, 1] = 0
            pmtct_transmission_rate[c_idx, 6, 1] = 0
        else:
            # Low CD4 (<350)
            pmtct_transmission_rate[c_idx, 0, 1] = (
                modvars[AM_TransEffAssumpTag][
                    DP_Data, DP_OptionA, DP_BreastfeedingGE350
                ]
                / 100
            )
            pmtct_transmission_rate[c_idx, 1, 1] = (
                modvars[AM_TransEffAssumpTag][
                    DP_Data, DP_OptionB, DP_BreastfeedingGE350
                ]
                / 100
            )
            pmtct_transmission_rate[c_idx, 2, 1] = (
                modvars[AM_TransEffAssumpTag][
                    DP_Data, DP_SingleDoseNev, DP_BreastfeedingGE350
                ]
                / 100
            )
            # Note: Using LT350 for ART strategies (matches comment in Delphi)
            pmtct_transmission_rate[c_idx, 4, 1] = (
                modvars[AM_TransEffAssumpTag][
                    DP_Data, DP_ARTStartPrePreg, DP_BreastfeedingLT350
                ]
                / 100
            )
            pmtct_transmission_rate[c_idx, 5, 1] = (
                modvars[AM_TransEffAssumpTag][
                    DP_Data, DP_ARTStartDurPreg, DP_BreastfeedingLT350
                ]
                / 100
            )
            pmtct_transmission_rate[c_idx, 6, 1] = (
                modvars[AM_TransEffAssumpTag][
                    DP_Data, DP_ARTStartDurPreg_Late, DP_BreastfeedingLT350
                ]
                / 100
            )

    breastfeeding_duration_art = (
        modvars[AM_InfantFeedingOptionsTag][1:19, DP_InPMTCT, : (final_year_idx + 1)]
        / 100
    ).copy(order="F")

    breastfeeding_duration_no_art = (
        modvars[AM_InfantFeedingOptionsTag][1:19, DP_NotInPMTCT, : (final_year_idx + 1)]
        / 100
    ).copy(order="F")

    abortion = np.stack(
        [
            modvars[AM_PregTermAbortionTag][: (final_year_idx + 1)],
            modvars[AM_PregTermAbortionPerNumTag][: (final_year_idx + 1)],
        ],
        axis=0,
    ).copy(order="F")

    patients_reallocated = modvars[AM_PatientsReallocatedTag][
        : (final_year_idx + 1)
    ].copy(order="F")

    hc_art_ltfu = (
        modvars[AM_PercInterruptedChildTag][: (final_year_idx + 1)] / 100
    ).copy(order="F")

    # Only used when running the paed model standalone
    adult_female_hivnpop = np.zeros(
        (ss["p_fertility_age_groups"], final_year_idx + 1), order="F"
    )

    hc_age_specific_fertility_rate = _get_leapfrog_asfr(modvars, final_year_idx)

    # Direct input parameters (set to 0/empty - not used in normal operation)
    mat_prev_input = np.zeros(final_year_idx + 1, dtype=np.int32, order="F")
    mat_hiv_births = np.zeros(final_year_idx + 1, order="F")
    prop_lt200 = np.zeros(final_year_idx + 1, order="F")
    prop_gte350 = np.zeros(final_year_idx + 1, order="F")
    adult_female_infections = np.zeros(
        (ss["p_fertility_age_groups"], final_year_idx + 1), order="F"
    )
    total_births = np.zeros(final_year_idx + 1, order="F")
    infant_pop = np.zeros((ss["hc_infant"], ss["NS"], final_year_idx + 1), order="F")

    return {
        "hc_nosocomial": hc_nosocomial,
        "hc1_cd4_dist": hc1_cd4_dist,
        "hc1_cd4_mort": hc1_cd4_mort,
        "hc2_cd4_mort": hc2_cd4_mort,
        "hc1_cd4_prog": hc1_cd4_prog,
        "hc2_cd4_prog": hc2_cd4_prog,
        "ctx_val": ctx_val,
        "hc_art_elig_age": hc_art_elig_age,
        "hc_art_elig_cd4": hc_art_elig_cd4,
        "hc_art_mort_rr": hc_art_mort_rr,
        "hc1_art_mort": hc1_art_mort,
        "hc2_art_mort": hc2_art_mort,
        "hc_art_isperc": hc_art_is_percent,
        "hc_art_val": hc_art_val,
        "hc_art_init_dist": hc_art_init_dist,
        "PMTCT": pmtct,
        "vertical_transmission_rate": vertical_transmission_rate,
        "PMTCT_transmission_rate": pmtct_transmission_rate,
        "PMTCT_dropout": pmtct_dropout,
        "PMTCT_input_is_percent": pmtct_input_is_percent,
        "breastfeeding_duration_art": breastfeeding_duration_art,
        "breastfeeding_duration_no_art": breastfeeding_duration_no_art,
        "infant_pop": infant_pop,
        "mat_hiv_births": mat_hiv_births,
        "mat_prev_input": mat_prev_input,
        "prop_lt200": prop_lt200,
        "prop_gte350": prop_gte350,
        "ctx_val_is_percent": ctx_val_is_percent,
        "hc_art_is_age_spec": hc_art_is_age_spec,
        "abortion": abortion,
        "patients_reallocated": patients_reallocated,
        "hc_art_ltfu": hc_art_ltfu,
        "adult_female_infections": adult_female_infections,
        "adult_female_hivnpop": adult_female_hivnpop,
        "total_births": total_births,
        "ctx_effect": ctx_effect,
        "hc_art_start": hc_art_start,
        "hc_age_specific_fertility_rate": hc_age_specific_fertility_rate,
    }


def _hv_modvars_leapfrog(modvars: Modvars, final_year_idx: int):

    epi_initial_pulse = float(modvars[HVInitialPulseTag])

    # array[HV_None..HV_MSMIDU] of HV_TDoubleDynYearArray;
    b_condom_prop = modvars[HVCondomPercentTag][
        : (HV_MSMIDU + 1), : (final_year_idx + 1)
    ].copy(order="F")

    # array [HV_AllRisk..HV_MSM_F3,HV_PercPop..HV_AvgDur] of Double;
    b_behav = modvars[HVBehaviorTag][: (HV_MSM_F3 + 1), : (HV_AvgDur + 1)].copy(
        order="F"
    )

    return {
        "epi_initial_pulse": epi_initial_pulse,
        "b_condom_prop": b_condom_prop,
        "b_behav": b_behav,
    }


def _rn_modvars_leapfrog(modvars: Modvars, final_year_idx: int):

    return {}


def _get_leapfrog_asfr(modvars: Modvars, final_index: int) -> np.ndarray:
    """
    Get age-specific fertility rates in Leapfrog format.

    Args:
        modvars: Dictionary containing modvar data
        final_index: Number of time periods

    Returns:
        Array of shape (DP_NumFertileAges, final_index)
    """
    result = np.zeros((DP_NumFertileAges, final_index + 1), order="F")

    # Get ASFR data for 5-year age groups (15-19 to 45-49)
    asfr_5year = modvars[DP_ASFRTag][GB_A15_19 : GB_A45_49 + 1, : (final_index + 1)]
    asfr_sum = asfr_5year.sum(axis=0)

    # Distribute each 5-year rate across 5 single-year ages
    for a in range(DP_NumFertileAges):
        five_year_age_group = a // 5
        result[a, :] = (modvars[DP_TFRTag] * asfr_5year[five_year_age_group, :]) / (
            5.0 * asfr_sum
        )

    return result


def get_cd4_threshold_adult_idx(threshold: np.ndarray) -> np.ndarray:
    """
    Map CD4 threshold value(s) to CD4 category index/indices for adults.

    Args:
        threshold: Single threshold value or numpy array of thresholds

    Returns:
        Array of indices corresponding to CD4 categories
    """
    out = np.full_like(threshold, DP_CD4_GT500, dtype=np.int32, order="F")
    out[threshold <= 500] = DP_CD4_350_500
    out[threshold <= 350] = DP_CD4_250_349
    out[threshold <= 250] = DP_CD4_200_249
    # Update eligibility threshold from CD4<200 to CD4<250 to account for
    # additional proportion eligible with WHO Stage 3/4
    out[threshold <= 200] = DP_CD4_200_249
    out[threshold <= 100] = DP_CD4_50_99
    out[threshold <= 50] = DP_CD4_LT50

    return out


def get_cd4_threshold_child_idx(threshold: np.ndarray, p_type: int) -> np.ndarray:
    """
    Map CD4 threshold value(s) to CD4 category index/indices for children.

    Args:
        threshold: Single threshold value or numpy array of thresholds
        p_type: DP_Percent or DP_Number

    Returns:
        Array of indices corresponding to CD4 categories
    """
    if p_type == DP_Percent:
        out = np.full_like(threshold, DP_CD4_Per_GT30, dtype=np.int32, order="F")
        out[threshold <= 30] = DP_CD4_Per_26_30
        out[threshold <= 26] = DP_CD4_Per_21_25
        out[threshold <= 21] = DP_CD4_Per_16_20
        out[threshold <= 16] = DP_CD4_Per_11_15
        out[threshold <= 11] = DP_CD4_Per_5_10
        out[threshold <= 5] = DP_CD4_Per_LT5
    else:
        out = np.full_like(threshold, DP_CD4_Ped_GT1000, dtype=np.int32, order="F")
        out[threshold <= 1000] = DP_CD4_Ped_750_999
        out[threshold <= 750] = DP_CD4_Ped_500_749
        out[threshold <= 500] = DP_CD4_Ped_350_499
        out[threshold <= 350] = DP_CD4_Ped_200_349
        out[threshold <= 200] = DP_CD4_Ped_LT200

    return out


def Calc_Single_Ages(
    requiredModvars: dict = {}, p5: list = [], sa: list = [], sex: int = GB_Male
):
    """
    Splits the five year age group population data (p5) into single age population (sa).

        Parameters:
            requiredModvars (dict): All MVs required to run this function (tag = key, MV = value)
                DP_SurvRateTag

            p5 (list) : Five year age group population (sex x age)
            sa (list) : Single year age population
            sex (int) : Male vs female

        Returns:
            Nothing.
    """

    def SplitFirstGroup(requiredModvars, p1, p2, p3, p4, p5, sex):
        a0 = requiredModvars[DP_SurvRateTag][1][sex][DP_FIRST_INDEX] * 2 * 1000
        a1 = requiredModvars[DP_SurvRateTag][2][sex][DP_FIRST_INDEX] * a0
        a2 = requiredModvars[DP_SurvRateTag][3][sex][DP_FIRST_INDEX] * a1
        a3 = requiredModvars[DP_SurvRateTag][4][sex][DP_FIRST_INDEX] * a2
        a4 = requiredModvars[DP_SurvRateTag][5][sex][DP_FIRST_INDEX] * a3

        aSum = a0 + a1 + a2 + a3 + a4

        if aSum > 0:
            a0 = a0 / aSum * p1
            a1 = a1 / aSum * p1
            a2 = a2 / aSum * p1
            a3 = a3 / aSum * p1
            a4 = a4 / aSum * p1
        else:
            a0 = 0.3333 * p1 - 0.1636 * p2 - 0.0210 * p3 + 0.0796 * p4 - 0.0283 * p5
            a1 = 0.2595 * p1 - 0.0780 * p2 + 0.0130 * p3 + 0.0100 * p4 - 0.0045 * p5
            a2 = 0.1924 * p1 + 0.0064 * p2 + 0.0184 * p3 - 0.0256 * p4 + 0.0084 * p5
            a3 = 0.1329 * p1 + 0.0844 * p2 + 0.0054 * p3 - 0.0356 * p4 + 0.0129 * p5
            a4 = 0.0819 * p1 + 0.1508 * p2 - 0.0158 * p3 - 0.0284 * p4 + 0.0115 * p5

        return a0, a1, a2, a3, a4

    def SplitSecondGroup(p1, p2, p3, p4, p5):
        a5 = 0.0404 * p1 + 0.2000 * p2 - 0.0344 * p3 - 0.0128 * p4 + 0.0068 * p5
        a6 = 0.0093 * p1 + 0.2268 * p2 - 0.0402 * p3 + 0.0028 * p4 + 0.0013 * p5
        a7 = -0.0108 * p1 + 0.2272 * p2 - 0.0248 * p3 + 0.0112 * p4 - 0.0028 * p5
        a8 = -0.0198 * p1 + 0.1992 * p2 + 0.0172 * p3 + 0.0072 * p4 - 0.0038 * p5
        a9 = -0.0191 * p1 + 0.1468 * p2 + 0.0822 * p3 - 0.0084 * p4 - 0.0015 * p5
        return a5, a6, a7, a8, a9

    def SplitMiddleGroup(p1, p2, p3, p4, p5):
        a1 = -0.0117 * p1 + 0.0804 * p2 + 0.1570 * p3 - 0.0284 * p4 + 0.0027 * p5
        a2 = -0.0020 * p1 + 0.0160 * p2 + 0.2200 * p3 - 0.0400 * p4 + 0.0060 * p5
        a3 = 0.0050 * p1 - 0.0280 * p2 + 0.2460 * p3 - 0.0280 * p4 + 0.0050 * p5
        a4 = 0.0060 * p1 - 0.0400 * p2 + 0.2200 * p3 + 0.0160 * p4 - 0.0020 * p5
        a5 = 0.0027 * p1 - 0.0284 * p2 + 0.1570 * p3 + 0.0804 * p4 - 0.0117 * p5
        return a1, a2, a3, a4, a5

    def SplitPenultimateGroup(p1, p2, p3, p4, p5):
        a1 = -0.0015 * p1 - 0.0084 * p2 + 0.0822 * p3 + 0.1468 * p4 - 0.0191 * p5
        a2 = -0.0038 * p1 + 0.0072 * p2 + 0.0172 * p3 + 0.1992 * p4 - 0.0198 * p5
        a3 = -0.0028 * p1 + 0.0112 * p2 - 0.0248 * p3 + 0.2272 * p4 - 0.0108 * p5
        a4 = 0.0013 * p1 + 0.0028 * p2 - 0.0402 * p3 + 0.2268 * p4 + 0.0093 * p5
        a5 = 0.0068 * p1 - 0.0128 * p2 - 0.0344 * p3 + 0.2000 * p4 + 0.0404 * p5
        return a1, a2, a3, a4, a5

    def SplitLastGroup(p1, p2, p3, p4, p5):
        a1 = 0.0115 * p1 - 0.0284 * p2 - 0.0158 * p3 + 0.1508 * p4 + 0.0819 * p5
        a2 = 0.0129 * p1 - 0.0356 * p2 + 0.0054 * p3 + 0.0844 * p4 + 0.1329 * p5
        a3 = 0.0084 * p1 - 0.0256 * p2 + 0.0184 * p3 + 0.0064 * p4 + 0.1924 * p5
        a4 = -0.0045 * p1 + 0.0100 * p2 + 0.0130 * p3 - 0.0780 * p4 + 0.2595 * p5
        a5 = -0.0283 * p1 + 0.0796 * p2 - 0.0210 * p3 - 0.1636 * p4 + 0.3333 * p5
        return a1, a2, a3, a4, a5

    sa[0], sa[1], sa[2], sa[3], sa[4] = SplitFirstGroup(
        requiredModvars,
        p5[GB_A0_4],
        p5[GB_A5_9],
        p5[GB_A10_14],
        p5[GB_A15_19],
        p5[GB_A20_24],
        sex,
    )
    sa[5], sa[6], sa[7], sa[8], sa[9] = SplitSecondGroup(
        p5[GB_A0_4], p5[GB_A5_9], p5[GB_A10_14], p5[GB_A15_19], p5[GB_A20_24]
    )
    sa[70], sa[71], sa[72], sa[73], sa[74] = SplitPenultimateGroup(
        p5[GB_A55_59], p5[GB_A60_64], p5[GB_A65_69], p5[GB_A70_74], p5[GB_A75_79]
    )
    sa[75], sa[76], sa[77], sa[78], sa[79] = SplitLastGroup(
        p5[GB_A55_59], p5[GB_A60_64], p5[GB_A65_69], p5[GB_A70_74], p5[GB_A75_79]
    )

    sa[80] = p5[GB_A80_Up]

    age = 10

    while age < GB_MaxSingleAges - 10:
        f, i = math.modf(age / 5)
        k = int(i) + 1
        sa[age], sa[age + 1], sa[age + 2], sa[age + 3], sa[age + 4] = SplitMiddleGroup(
            p5[k - 2], p5[k - 1], p5[k], p5[k + 1], p5[k + 2]
        )
        age = age + 5


def getSexBirthRatioPercent(data, s, t):
    sexBirthRatio = data[DP_SexBirthRatioTag]

    value = 0
    if s == GB_Male:
        value = sexBirthRatio[t] / (sexBirthRatio[t] + 100)
    else:
        value = 1 - (sexBirthRatio[t] / (sexBirthRatio[t] + 100))

    return value
