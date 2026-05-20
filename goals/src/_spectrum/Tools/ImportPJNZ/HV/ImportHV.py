import numpy as np

from src._spectrum.AvenirCommon.Util import gb_read_csv_sheet, getAllTags

from SpectrumCommon.Modvars.GB.GBDefs import createProjectionParams
from SpectrumCommon.Const.GB import *
from src._spectrum.SpectrumCommon.Const.HV import *
from src._spectrum.SpectrumCommon.Const.RN import RN_AllVacc, RN_IDUDrugSub, RN_NoProt, RN_UnV



def openHV(file, params: createProjectionParams, projection: dict):
    sheet = gb_read_csv_sheet(file)
    tags = getAllTags(sheet)

    _import_tag_value(sheet, tags, projection, '<FirstYear MV>',           HV_FirstYearTag)
    _import_tag_value(sheet, tags, projection, '<FinalYear MV>',           HV_FinalYearTag)
    _import_tag_value(sheet, tags, projection, '<FinalIndex MV>',          HV_FinalIndexTag)
    _import_tag_value(sheet, tags, projection, '<DataChanged MV>',         HV_DataChangedTag)
    _import_tag_value(sheet, tags, projection, '<ProjectionValid MV>',     HV_ProjectionValidTag)
    _import_tag_value(sheet, tags, projection, '<projectionValidDate MV>', HV_ProjectionValidDateTag)
    _import_tag_value(sheet, tags, projection, '<FileName MV>',            HV_FileNameTag)
    import_Behavior(sheet, tags, params, projection)
    import_AgeFirstSex(sheet, tags, params, projection)
    import_ForceInf(sheet, tags, params, projection)
    import_Infectiousness(sheet, tags, params, projection)
    import_Prevalence(sheet, tags, params, projection)
    import_CondomPercent(sheet, tags, params, projection)
    _import_tag_value(sheet, tags, projection, '<TransMultSTI MV>', HV_TransMultSTITag)
    _import_tag_value(sheet, tags, projection, '<TransHIVF MV>',    HV_TransHIVFTag)
    _import_tag_value(sheet, tags, projection, '<TransMultM MV>',   HV_TransMultMTag)
    _import_tag_value(sheet, tags, projection, '<CondomEff MV>',    HV_CondomEffTag)
    import_NumPart(sheet, tags, params, projection)
    import_SexActs(sheet, tags, params, projection)
    import_STIPrev(sheet, tags, params, projection)
    import_EpidemicStYr(sheet, tags, params, projection)
    import_IncRecruitment(sheet, tags, params, projection)
    import_AllRiskOutput(sheet, tags, params, projection)
    import_MaxAllRisk(sheet, tags, params, projection)
    import_PercMarried(sheet, tags, params, projection)
    import_PerIDUsharing(sheet, tags, params, projection)
    import_InitialPulse(sheet, tags, params, projection)
    import_TransMultMSM(sheet, tags, params, projection)
    import_RedWHenCircum(sheet, tags, params, projection)
    import_InfectMultiplierOnART(sheet, tags, params, projection)
    import_BloodInfection(sheet, tags, params, projection)
    import_ARTReceive(sheet, tags, params, projection)
    import_MonthsInPrimaryStage(sheet, tags, params, projection)
    import_GoalsBaseYearIdx(sheet, tags, params, projection)
    import_GoalsTargetYearIdx(sheet, tags, params, projection)
    import_ImpactMatrix(sheet, tags, params, projection)
    import_ImpactMatrixCBIdx(sheet, tags, params, projection)
    _import_tag_value(sheet, tags, projection, '<ARTInputCoverageByRG MV>', HV_ARTInputCoverageByRGTag)
    import_NumMSMRiskGroups(sheet, tags, params, projection)
    import_BalanceSexActs(sheet, tags, params, projection)
    import_CondomUseRadioGroupIdx(sheet, tags, params, projection)
    import_CondomUseLogCurveParVal(sheet, tags, params, projection)
    import_CondomUseInterpolatedVal(sheet, tags, params, projection)
    import_CondomUseLogisticsVal(sheet, tags, params, projection)
    import_STIPrevRadioGroupIdx(sheet, tags, params, projection)
    import_STIPrevLogCurveParVal(sheet, tags, params, projection)
    import_STIPrevInterpolatedVal(sheet, tags, params, projection)
    import_STIPrevLogisticsVal(sheet, tags, params, projection)
    import_RiskGroupNames(sheet, tags, params, projection)
    import_EdHVSource(sheet, tags, params, projection)

    # import_CalcStateData(sheet, tags, params, projection)
    import_Adults(sheet, tags, params, projection)
    import_RiskGroupPercent(sheet, tags, params, projection)
    import_NonAIDSDeathRate(sheet, tags, params, projection)
    import_RateofAging(sheet, tags, params, projection)
    import_Populations(sheet, tags, params, projection)
    import_Vaccinated(sheet, tags, params, projection)
    import_TotalVaccinated(sheet, tags, params, projection)
    import_Unvaccinated(sheet, tags, params, projection)
    import_NewVaccinations(sheet, tags, params, projection)
    import_TotalNewVaccinations(sheet, tags, params, projection)
    import_TotalAdultsHIV(sheet, tags, params, projection)
    import_NewlyOnART(sheet, tags, params, projection)
    import_NewlyEligibleART(sheet, tags, params, projection)
    import_TotalAdultsART(sheet, tags, params, projection)
    import_RMultAll(sheet, tags, params, projection)
    import_CalcPrevalence(sheet, tags, params, projection)
    import_NewInfections(sheet, tags, params, projection)
    import_ExitRate(sheet, tags, params, projection)
    import_AIDSDeaths(sheet, tags, params, projection)
    import_AIDSDeathsART(sheet, tags, params, projection)
    import_TotalAIDSDeaths(sheet, tags, params, projection)
    import_TotalNewInfection(sheet, tags, params, projection)
    import_Incidence(sheet, tags, params, projection)
    import_IncSexRatio(sheet, tags, params, projection)
    import_PercentPop(sheet, tags, params, projection)
    import_InfectionsAverted(sheet, tags, params, projection)
    import_CumInfectionsAverted(sheet, tags, params, projection)
    import_DeathsAverted(sheet, tags, params, projection)
    import_CumDeathsAverted(sheet, tags, params, projection)
    import_ARTCoverageByRG(sheet, tags, params, projection)
    import_TotalARTCoverage(sheet, tags, params, projection)
    import_NewHIV(sheet, tags, params, projection)
    import_FitData(sheet, tags, params, projection)
    import_FitParamSet(sheet, tags, params, projection)
    import_FitControl(sheet, tags, params, projection)
    import_LowRiskCondomUseFromFP(sheet, tags, params, projection)

    return None

############### Start reading in HV Modvars ######################################


def _parse_value(value):
    if value == '':
        return value

    text = str(value).strip()
    if text == '':
        return ''

    if text.isdigit() or (text.startswith('-') and text[1:].isdigit()):
        try:
            return int(text)
        except ValueError:
            pass

    try:
        return float(text)
    except ValueError:
        return value


def _import_tag_value(sheet, tags, projection, source_tag: str, projection_tag: str):
    modvarTagRow = tags.get(source_tag, None)
    if modvarTagRow is None:
        return

    row = modvarTagRow + 2
    projection[projection_tag] = _parse_value(sheet[row, GB_RW_DataStartCol])


def _to_float(value, default=0.0):
    if value == '' or value is None:
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _get_year_index_bounds(params, projection):
    calc_year_idx = max(0, int(params.firstYear) - GB_NativeYear)
    final_index = int(params.finalYear) - int(params.firstYear)
    final_index = max(calc_year_idx, int(final_index))
    return calc_year_idx, final_index


def _read_year_row_with_flatline(sheet, row: int, calc_year_idx: int, final_index: int,
                                 start_col: int = GB_RW_DataStartCol):
    values = [0.0] * (final_index + 1)
    col = start_col
    last_value = 0.0
    for t in range(calc_year_idx, final_index + 1):
        cell_value = sheet[row, col]
        if cell_value != '':
            last_value = _to_float(_parse_value(cell_value), last_value)
            col += 1
        else:
            pass
        values[t] = last_value
    return values


def import_Behavior(sheet, tags, params, projection):
    modvarTagRow = tags.get('<Behavior MV>', None)
    if modvarTagRow is None:
        return

    row = modvarTagRow + 4
    behavior = np.zeros((HV_IDU_F3 + 1, HV_AvgDur + 1))

    for i in range(HV_None, HV_MSMIDU + 1):
        row += 1
        for s in range(HV_PercPop, HV_AvgDur + 1):
            behavior[i, s] = _parse_value(sheet[row, GB_RW_DataStartCol + s])
        row += 1

    row += 1
    for i in range(HV_None_F3, HV_IDU_F3 + 1):
        row += 1
        for s in range(HV_PercPop, HV_AvgDur + 1):
            behavior[i, s] = _parse_value(sheet[row, GB_RW_DataStartCol + s])
        row += 1

    projection[HV_BehaviorTag] = behavior

def import_AgeFirstSex(sheet, tags, params, projection):
    modvarTagRow = tags.get('<AgeFirstSex MV>', None)
    if modvarTagRow is None:
        return

    # Delphi reads two rows: males at +2 and females at +4, then flatlines to final index.
    calc_year_idx, final_index = _get_year_index_bounds(params, projection)

    age_first_sex = np.zeros((HV_Female + 1, final_index + 1))

    for row_offset, sex in ((4, HV_Male), (6, HV_Female)):
        row = modvarTagRow + row_offset
        col = GB_RW_DataStartCol
        last_value = 0.0
        for t in range(calc_year_idx, final_index + 1):
            cell_value = sheet[row, col]
            if cell_value != '':
                last_value = _parse_value(cell_value)
                col += 1
            age_first_sex[sex, t] = last_value

    projection[HV_AgeFirstSexTag] = age_first_sex.tolist()

def import_ForceInf(sheet, tags, params, projection):
    modvarTagRow = tags.get('<ForceInf MV>', None)
    if modvarTagRow is None:
        return

    calc_year_idx, final_index = _get_year_index_bounds(params, projection)
    force_inf = np.zeros((HV_Adults_P + 1, final_index + 1))

    # Delphi reads males at tag+2 and females at tag+4 with flatline beyond imported years.
    for sex, row_offset in ((HV_Male, 4), (HV_Female, 6)):
        row_values = _read_year_row_with_flatline(sheet, modvarTagRow + row_offset, calc_year_idx, final_index)
        force_inf[sex] = row_values

    projection[HV_ForceInfTag] = force_inf.tolist()

def import_Infectiousness(sheet, tags, params, projection):
    modvarTagRow = tags.get('<Infectiousness MV>', None)
    if modvarTagRow is None:
        return

    infectiousness = np.zeros(HV_SympART + 1)
    row = modvarTagRow + 2

    for t in range(HV_PrimaryInf, HV_SympART + 1):
        row += 1
        infectiousness[t] = _to_float(_parse_value(sheet[row, GB_RW_DataStartCol]))
        row += 1

    projection[HV_InfectiousnessTag] = infectiousness.tolist()

def import_Prevalence(sheet, tags, params, projection):
    modvarTagRow = tags.get('<Prevalence MV>', None)
    if modvarTagRow is None:
        return

    calc_year_idx, final_index = _get_year_index_bounds(params, projection)
    prevalence = np.zeros((HV_Adults_P + 1, final_index + 1))

    row = modvarTagRow + 3
    for s in range(HV_Males_P, HV_Adults_P + 1):
        row += 1
        prevalence[s] = _read_year_row_with_flatline(sheet, row, calc_year_idx, final_index)
        row += 1

    projection[HV_PrevalenceTag] = prevalence.tolist()

def import_CondomPercent(sheet, tags, params, projection):
    modvarTagRow = tags.get('<CondomPercent MV>', None)
    if modvarTagRow is None:
        return

    calc_year_idx, final_index = _get_year_index_bounds(params, projection)
    condom_percent = np.zeros((HV_Adults_P + 1, final_index + 1))

    row = modvarTagRow + 3
    nrow = 1
    for r in range(HV_LRH, HV_MSMHR):
        nrow += 1
        if r == HV_IDU:
            nrow += 1
        row += 1
        condom_percent[nrow] = _read_year_row_with_flatline(sheet, row, calc_year_idx, final_index)
        row += 1

    projection[HV_CondomPercentTag] = condom_percent.tolist()

def import_NumPart(sheet, tags, params, projection):
    modvarTagRow = tags.get('<NumPart MV2>', None)
    if modvarTagRow is None:
        return

    calc_year_idx, final_index = _get_year_index_bounds(params, projection)
    num_part = np.zeros((HV_MSM_F3 + 1, final_index + 1))

    row = modvarTagRow + 3
    for r in range(HV_AllRisk, HV_MSM_F3 + 1):
        num_part[r] = _read_year_row_with_flatline(sheet, row, calc_year_idx, final_index)
        row += 1

    projection[HV_NumPartTag] = num_part.tolist()

def import_SexActs(sheet, tags, params, projection):
    modvarTagRow = tags.get('<SexActs MV2>', None)
    if modvarTagRow is None:
        return

    calc_year_idx, final_index = _get_year_index_bounds(params, projection)
    sex_acts = np.zeros((HV_MSM_F3 + 1, final_index + 1))

    row = modvarTagRow + 3
    for r in range(HV_AllRisk, HV_MSM_F3 + 1):
        sex_acts[r] = _read_year_row_with_flatline(sheet, row, calc_year_idx, final_index)
        row += 1

    projection[HV_SexActsTag] = sex_acts.tolist()

def import_STIPrev(sheet, tags, params, projection):
    modvarTagRow = tags.get('<STIPrev MV2>', None)
    if modvarTagRow is None:
        return

    calc_year_idx, final_index = _get_year_index_bounds(params, projection)
    sti_prev = np.zeros((HV_MSM_F3 + 1, final_index + 1))

    row = modvarTagRow + 3
    for r in range(HV_AllRisk, HV_MSM_F3 + 1):
        sti_prev[r] = _read_year_row_with_flatline(sheet, row, calc_year_idx, final_index)
        row += 1

    projection[HV_STIPrevTag] = sti_prev.tolist()

def import_EpidemicStYr(sheet, tags, params, projection):
    modvarTagRow = tags.get('<EpidemicStYr MV>', None)
    if modvarTagRow is None:
        return

    row = modvarTagRow + 2
    value = int(_to_float(_parse_value(sheet[row, GB_RW_DataStartCol]), 1980.0))
    if value < int(params.firstYear):
        value = 1980
    projection[HV_EpidemicStYrTag] = value

def import_IncRecruitment(sheet, tags, params, projection):
    modvarTagRow = tags.get('<IncRecruitment MV>', None)
    if modvarTagRow is None:
        return

    inc_recruitment = np.zeros((HV_Female + 1, HV_MSMIDU + 1))

    curr_row = modvarTagRow + 2
    curr_row += 1
    for s in range(HV_Male, HV_Female + 1):
        curr_row += 1
        for r in range(HV_None, HV_MSMIDU + 1):
            curr_row += 1
            inc_recruitment[s, r] = _to_float(_parse_value(sheet[curr_row, GB_RW_DataStartCol]))
            curr_row += 1

    projection[HV_IncRecruitmentTag] = inc_recruitment.tolist()

def import_AllRiskOutput(sheet, tags, params, projection):
    modvarTagRow = tags.get('<AllRiskOutput MV>', None)
    if modvarTagRow is None:
        return

    calc_year_idx, final_index = _get_year_index_bounds(params, projection)
    all_risk_output = np.zeros((HV_max_services, final_index + 1))

    row = modvarTagRow + 3
    for i in range(0, HV_max_services):
        all_risk_output[i] = _read_year_row_with_flatline(sheet, row, calc_year_idx, final_index)
        row += 1

    projection[HV_AllRiskOutputTag] = all_risk_output.tolist()

def import_MaxAllRisk(sheet, tags, params, projection):
    modvarTagRow = tags.get('<MaxAllRisk MV>', None)
    if modvarTagRow is None:
        return

    row = modvarTagRow + 2
    projection[HV_MaxAllRiskTag] = _to_float(_parse_value(sheet[row, GB_RW_DataStartCol]))

def import_PercMarried(sheet, tags, params, projection):
    modvarTagRow = tags.get('<PercMarried MV2>', None)
    if modvarTagRow is None:
        return

    perc_married = np.zeros(HV_MSM_F3 + 1)

    row = modvarTagRow + 3
    for r in range(HV_AllRisk, HV_MSM_F3 + 1):
        perc_married[r] = _to_float(_parse_value(sheet[row, GB_RW_DataStartCol]))
        row += 1

    projection[HV_PercMarriedTag] = perc_married.tolist()

def import_PerIDUsharing(sheet, tags, params, projection):
    modvarTagRow = tags.get('<PerIDUsharing MV>', None)
    if modvarTagRow is None:
        return

    calc_year_idx, final_index = _get_year_index_bounds(params, projection)
    row = modvarTagRow + 3
    projection[HV_PerIDUsharingTag] = _read_year_row_with_flatline(sheet, row, calc_year_idx, final_index)

def import_InitialPulse(sheet, tags, params, projection):
    modvarTagRow = tags.get('<InitialPulse MV>', None)
    if modvarTagRow is None:
        return

    row = modvarTagRow + 2
    projection[HV_InitialPulseTag] = _to_float(_parse_value(sheet[row, GB_RW_DataStartCol]))

def import_TransMultMSM(sheet, tags, params, projection):
    modvarTagRow = tags.get('<TransMultMSM MV>', None)
    if modvarTagRow is None:
        return

    row = modvarTagRow + 2
    projection[HV_TransMultMSMTag] = _to_float(_parse_value(sheet[row, GB_RW_DataStartCol]))

def import_RedWHenCircum(sheet, tags, params, projection):
    modvarTagRow = tags.get('<RedWHenCircum MV>', None)
    if modvarTagRow is None:
        return

    row = modvarTagRow + 2
    red_when_circum = np.zeros(HV_Infect + 1)
    for i in range(HV_Susceptibility, HV_Infect + 1):
        red_when_circum[i] = _to_float(_parse_value(sheet[row, GB_RW_DataStartCol + i]))
    projection[HV_RedWHenCircumTag] = red_when_circum.tolist()

def import_InfectMultiplierOnART(sheet, tags, params, projection):
    modvarTagRow = tags.get('<InfectMultiplierOnART MV>', None)
    if modvarTagRow is None:
        return

    calc_year_idx, final_index = _get_year_index_bounds(params, projection)
    row = modvarTagRow + 4
    projection[HV_InfectMultiplierOnARTTag] = _read_year_row_with_flatline(sheet, row, calc_year_idx, final_index)

def import_BloodInfection(sheet, tags, params, projection):
    modvarTagRow = tags.get('<BloodInfection MV>', None)
    if modvarTagRow is None:
        return

    calc_year_idx, final_index = _get_year_index_bounds(params, projection)
    row = modvarTagRow + 4
    projection[HV_BloodInfectionTag] = _read_year_row_with_flatline(sheet, row, calc_year_idx, final_index)

def import_ARTReceive(sheet, tags, params, projection):
    modvarTagRow = tags.get('<ARTReceive MV>', None)
    if modvarTagRow is None:
        return

    calc_year_idx, final_index = _get_year_index_bounds(params, projection)
    row = modvarTagRow + 3
    projection[HV_ARTReceiveTag] = _read_year_row_with_flatline(sheet, row, calc_year_idx, final_index)

def import_MonthsInPrimaryStage(sheet, tags, params, projection):
    modvarTagRow = tags.get('<MonthsInPrimaryStage MV>', None)
    if modvarTagRow is None:
        return

    row = modvarTagRow + 2
    projection[HV_MonthsInPrimaryStageTag] = _to_float(_parse_value(sheet[row, GB_RW_DataStartCol]))

def import_GoalsBaseYearIdx(sheet, tags, params, projection):
    modvarTagRow = tags.get('<GoalsBaseYearIdx MV2>', None)
    if modvarTagRow is None:
        return

    row = modvarTagRow + 2
    projection[HV_GoalsBaseYearIdxTag] = int(_to_float(_parse_value(sheet[row, GB_RW_DataStartCol]), 0.0))

def import_GoalsTargetYearIdx(sheet, tags, params, projection):
    modvarTagRow = tags.get('<GoalsTargetYearIdx MV>', None)
    if modvarTagRow is None:
        return

    row = modvarTagRow + 2
    projection[HV_GoalsTargetYearIdxTag] = int(_to_float(_parse_value(sheet[row, GB_RW_DataStartCol]), 0.0))

def import_ImpactMatrix(sheet, tags, params, projection):
    modvarTagRow = tags.get('<ImpactMatrix MV>', None)
    if modvarTagRow is None:
        return

    impact_matrix = np.zeros((HV_Data + 1, RN_IDUDrugSub + 1, HV_MaxRiskGroups + 1))

    row = modvarTagRow + 2
    for d in range(HV_Default, HV_Data + 1):
        for i in range(1, RN_IDUDrugSub + 1):
            for r in range(1, HV_MaxRiskGroups + 1):
                impact_matrix[d, i, r] = _to_float(_parse_value(sheet[row, GB_RW_DataStartCol + r]))
            row += 1

    projection[HV_ImpactMatrixTag] = impact_matrix.tolist()

def import_ImpactMatrixCBIdx(sheet, tags, params, projection):
    modvarTagRow = tags.get('<ImpactMatrixCBIdx MV>', None)
    if modvarTagRow is None:
        return

    row = modvarTagRow + 2
    projection[HV_ImpactMatrixCBIdxTag] = int(_to_float(_parse_value(sheet[row, GB_RW_DataStartCol]), 0.0))

def import_ARTInputCoverageByRG(sheet, tags, params, projection):
    modvarTagRow = tags.get('<ARTInputCoverageByRG MV>', None)
    if modvarTagRow is None:
        return

    row = modvarTagRow + 2
    projection[HV_ARTInputCoverageByRGTag] = _parse_value(sheet[row, GB_RW_DataStartCol])

def import_NumMSMRiskGroups(sheet, tags, params, projection):
    modvarTagRow = tags.get('<NumMSMRiskGroups MV>', None)
    if modvarTagRow is None:
        return

    row = modvarTagRow + 2
    projection[HV_NumMSMRiskGroupsTag] = int(_to_float(_parse_value(sheet[row, GB_RW_DataStartCol]), 0.0))

def import_BalanceSexActs(sheet, tags, params, projection):
    modvarTagRow = tags.get('<BalanceSexActs MV>', None)
    if modvarTagRow is None:
        return

    row = modvarTagRow + 2
    projection[HV_BalanceSexActsTag] = bool(int(_to_float(_parse_value(sheet[row, GB_RW_DataStartCol]), 0.0)))

def import_CondomUseRadioGroupIdx(sheet, tags, params, projection):
    modvarTagRow = tags.get('<CondomUseRadioGroupIdx MV>', None)
    if modvarTagRow is None:
        return

    row = modvarTagRow + 2
    projection[HV_CondomUseRadioGroupIdxTag] = int(_to_float(_parse_value(sheet[row, GB_RW_DataStartCol]), 0.0))

def import_CondomUseLogCurveParVal(sheet, tags, params, projection):
    modvarTagRow = tags.get('<CondomUseLogCurveParVal MV>', None)
    if modvarTagRow is None:
        return

    log_curve_par_val = np.zeros((HV_MSMHR + 1, HV_CU_Q + 1))

    row = modvarTagRow + 2
    for r in range(HV_LRH, HV_MSMHR + 1):
        for par in range(HV_CU_A, HV_CU_Q + 1):
            log_curve_par_val[r, par] = _to_float(_parse_value(sheet[row, GB_RW_DataStartCol + par]))
        row += 1

    projection[HV_CondomUseLogCurveParValTag] = log_curve_par_val.tolist()

def import_CondomUseInterpolatedVal(sheet, tags, params, projection):
    modvarTagRow = tags.get('<CondomUseInterpolatedVal MV>', None)
    if modvarTagRow is None:
        return

    calc_year_idx, final_index = _get_year_index_bounds(params, projection)
    interpolated_val = np.zeros((HV_MSMIDU + 1, final_index + 1))

    row = modvarTagRow + 3
    nrow = 1
    for r in range(HV_LRH, HV_MSMHR):
        nrow += 1
        if r == HV_IDU:
            nrow += 1
        row += 1
        interpolated_val[nrow] = _read_year_row_with_flatline(sheet, row, calc_year_idx, final_index)
        row += 1

    projection[HV_CondomUseInterpolatedValTag] = interpolated_val.tolist()

def import_CondomUseLogisticsVal(sheet, tags, params, projection):
    modvarTagRow = tags.get('<CondomUseLogisticsVal MV>', None)
    if modvarTagRow is None:
        return

    calc_year_idx, final_index = _get_year_index_bounds(params, projection)
    logistics_val = np.zeros((HV_MSMIDU + 1, final_index + 1))

    row = modvarTagRow + 2
    nrow = 1
    for r in range(HV_LRH, HV_MSMHR):
        nrow += 1
        if r == HV_IDU:
            nrow += 1
        row += 1
        logistics_val[nrow] = _read_year_row_with_flatline(sheet, row, calc_year_idx, final_index)
        row += 1

    projection[HV_CondomUseLogisticsValTag] = logistics_val.tolist()

def import_STIPrevRadioGroupIdx(sheet, tags, params, projection):
    modvarTagRow = tags.get('<STIPrevRadioGroupIdx MV>', None)
    if modvarTagRow is None:
        return

    row = modvarTagRow + 2
    projection[HV_STIPrevRadioGroupIdxTag] = int(_to_float(_parse_value(sheet[row, GB_RW_DataStartCol]), 0.0))

def import_STIPrevLogCurveParVal(sheet, tags, params, projection):
    modvarTagRow = tags.get('<STIPrevLogCurveParVal MV2>', None)
    if modvarTagRow is None:
        return

    log_curve_par_val = np.zeros((HV_MSM_F3 + 1, HV_CU_Q + 1))

    row = modvarTagRow + 2
    for r in range(HV_AllRisk, HV_MSM_F3 + 1):
        for par in range(HV_CU_A, HV_CU_Q + 1):
            log_curve_par_val[r, par] = _to_float(_parse_value(sheet[row, GB_RW_DataStartCol + par]))
        row += 1

    projection[HV_STIPrevLogCurveParValTag] = log_curve_par_val.tolist()

def import_STIPrevInterpolatedVal(sheet, tags, params, projection):
    modvarTagRow = tags.get('<STIPrevInterpolatedVal MV2>', None)
    if modvarTagRow is None:
        return

    calc_year_idx, final_index = _get_year_index_bounds(params, projection)
    interpolated_val = np.zeros((HV_MSM_F3 + 1, final_index + 1))

    row = modvarTagRow + 3
    for r in range(HV_AllRisk, HV_MSM_F3 + 1):
        interpolated_val[r] = _read_year_row_with_flatline(sheet, row, calc_year_idx, final_index)
        row += 1

    projection[HV_STIPrevInterpolatedValTag] = interpolated_val.tolist()

def import_STIPrevLogisticsVal(sheet, tags, params, projection):
    modvarTagRow = tags.get('<STIPrevLogisticsVal MV2>', None)
    if modvarTagRow is None:
        return

    calc_year_idx, final_index = _get_year_index_bounds(params, projection)
    logistics_val = np.zeros((HV_MSM_F3 + 1, final_index + 1))

    row = modvarTagRow + 3
    for r in range(HV_AllRisk, HV_MSM_F3 + 1):
        logistics_val[r] = _read_year_row_with_flatline(sheet, row, calc_year_idx, final_index)
        row += 1

    projection[HV_STIPrevLogisticsValTag] = logistics_val.tolist()

def import_RiskGroupNames(sheet, tags, params, projection):
    modvarTagRow = tags.get('<RiskGroupNames MV>', None)
    if modvarTagRow is None:
        return

    row = modvarTagRow + 2
    count = int(_to_float(_parse_value(sheet[row, GB_RW_DataStartCol]), 0.0))
    names = []
    for s in range(1, count + 1):
        names.append(sheet[row, GB_RW_DataStartCol + s])
    projection[HV_RiskGroupNamesTag] = names

def import_EdHVSource(sheet, tags, params, projection):
    modvarTagRow = tags.get('<EdHVSource MV>', None)
    if modvarTagRow is None:
        return

    row = modvarTagRow + 2
    count = int(_to_float(_parse_value(sheet[row, GB_RW_DataStartCol]), 0.0))
    sources = []
    for s in range(1, count + 1):
        sources.append(sheet[row, GB_RW_DataStartCol + s])
    projection[HV_EdHVSourceTag] = sources

# def import_CalcStateData(sheet, tags, params, projection):
#     modvarTagRow = tags.get('<CalcStateData MV2>', None)
#     if modvarTagRow is None:
#         return

#     row = modvarTagRow + 2
#     projection[HV_CalcStateDataTag] = _parse_value(sheet[row, GB_RW_DataStartCol])

def import_Adults(sheet, tags, params, projection):
    modvarTagRow = tags.get('<Adults MV>', None)
    if modvarTagRow is None:
        return

    calc_year_idx, final_index = _get_year_index_bounds(params, projection)
    adults = np.zeros((HV_Female + 1, HV_MSMIDU + 1, HV_AllHIV + 1, RN_NoProt + 1, final_index + 1))

    row = modvarTagRow + 2
    for s in range(HV_BothSexes, HV_Female + 1):
        row += 1
        for r in range(HV_AllRisk, HV_MSMIDU + 1):
            for h in range(HV_Negative, HV_AllHIV + 1):
                for v in range(RN_AllVacc, RN_NoProt + 1):
                    adults[s, r, h, v] = _read_year_row_with_flatline(
                        sheet, row, calc_year_idx, final_index,
                        start_col=GB_RW_DataStartCol + 2
                    )
                    row += 1

    projection[HV_AdultsTag] = adults.tolist()

def import_RiskGroupPercent(sheet, tags, params, projection):
    modvarTagRow = tags.get('<RiskGroupPercent MV>', None)
    if modvarTagRow is None:
        return

    risk_group_percent = np.zeros(HV_MSM_F3 + 1)

    curr_row = modvarTagRow + 2
    for s in range(HV_AllRisk, HV_MSM_F3 + 1):
        curr_row += 1
        risk_group_percent[s] = _to_float(_parse_value(sheet[curr_row, GB_RW_DataStartCol]))
        curr_row += 1

    projection[HV_RiskGroupPercentTag] = risk_group_percent.tolist()

def import_NonAIDSDeathRate(sheet, tags, params, projection):
    modvarTagRow = tags.get('<NonAIDSDeathRate MV>', None)
    if modvarTagRow is None:
        return

    calc_year_idx, final_index = _get_year_index_bounds(params, projection)
    non_aids_death_rate = np.zeros((HV_Female + 1, final_index + 1))

    row = modvarTagRow + 2
    for i in range(HV_BothSexes, HV_Female):
        non_aids_death_rate[i] = _read_year_row_with_flatline(sheet, row, calc_year_idx, final_index)
        row += 1

    projection[HV_NonAIDSDeathRateTag] = non_aids_death_rate.tolist()

def import_RateofAging(sheet, tags, params, projection):
    modvarTagRow = tags.get('<RateofAging MV>', None)
    if modvarTagRow is None:
        return

    calc_year_idx, final_index = _get_year_index_bounds(params, projection)
    rate_of_aging = np.zeros((HV_Female + 1, final_index + 1))

    row = modvarTagRow + 2
    for i in range(HV_BothSexes, HV_Female):
        rate_of_aging[i] = _read_year_row_with_flatline(sheet, row, calc_year_idx, final_index)
        row += 1

    projection[HV_RateofAgingTag] = rate_of_aging.tolist()

def import_Populations(sheet, tags, params, projection):
    modvarTagRow = tags.get('<Populations MV>', None)
    if modvarTagRow is None:
        return

    calc_year_idx, final_index = _get_year_index_bounds(params, projection)
    populations = np.zeros((HV_Female + 1, final_index + 1))

    curr_row = modvarTagRow + 2
    for s in range(HV_BothSexes, HV_Female + 1):
        curr_row += 1
        populations[s] = _read_year_row_with_flatline(sheet, curr_row, calc_year_idx, final_index)
        curr_row += 1

    projection[HV_PopulationsTag] = populations.tolist()

def import_Vaccinated(sheet, tags, params, projection):
    modvarTagRow = tags.get('<Vaccinated MV>', None)
    if modvarTagRow is None:
        return

    calc_year_idx, final_index = _get_year_index_bounds(params, projection)
    vaccinated = np.zeros((HV_Female + 1, HV_MSMIDU + 1, HV_AllHIV + 1, final_index + 1))

    row = modvarTagRow + 2
    for s in range(HV_BothSexes, HV_Female):
        for r in range(HV_AllRisk, HV_MSMIDU):
            for h in range(HV_Negative, HV_AllHIV):
                vaccinated[s, r, h] = _read_year_row_with_flatline(sheet, row, calc_year_idx, final_index)
                row += 1

    projection[HV_VaccinatedTag] = vaccinated.tolist()

def import_TotalVaccinated(sheet, tags, params, projection):
    modvarTagRow = tags.get('<TotalVaccinated MV>', None)
    if modvarTagRow is None:
        return

    calc_year_idx, final_index = _get_year_index_bounds(params, projection)
    total_vaccinated = np.zeros((HV_Female + 1, final_index + 1))

    curr_row = modvarTagRow + 2
    for s in range(HV_BothSexes, HV_Female + 1):
        curr_row += 1
        total_vaccinated[s] = _read_year_row_with_flatline(sheet, curr_row, calc_year_idx, final_index)
        curr_row += 1

    projection[HV_TotalVaccinatedTag] = total_vaccinated.tolist()

def import_Unvaccinated(sheet, tags, params, projection):
    modvarTagRow = tags.get('<Unvaccinated MV>', None)
    if modvarTagRow is None:
        return

    calc_year_idx, final_index = _get_year_index_bounds(params, projection)
    row = modvarTagRow + 2
    projection[HV_UnvaccinatedTag] = _read_year_row_with_flatline(sheet, row, calc_year_idx, final_index)

def import_NewVaccinations(sheet, tags, params, projection):
    modvarTagRow = tags.get('<NewVaccinations MV>', None)
    if modvarTagRow is None:
        return

    calc_year_idx, final_index = _get_year_index_bounds(params, projection)
    new_vaccinations = np.zeros((HV_Female + 1, HV_MSMIDU + 1, final_index + 1))

    curr_row = modvarTagRow + 2
    for s in range(HV_Male, HV_Female + 1):
        curr_row += 1
        for r in range(HV_None, HV_MSMIDU + 1):
            curr_row += 1
            new_vaccinations[s, r] = _read_year_row_with_flatline(sheet, curr_row, calc_year_idx, final_index)
            curr_row += 1
    curr_row += 1

    projection[HV_NewVaccinationsTag] = new_vaccinations.tolist()

def import_TotalNewVaccinations(sheet, tags, params, projection):
    modvarTagRow = tags.get('<TotalNewVaccinations MV>', None)
    if modvarTagRow is None:
        return

    calc_year_idx, final_index = _get_year_index_bounds(params, projection)

    curr_row = modvarTagRow + 3
    projection[HV_TotalNewVaccinationsTag] = _read_year_row_with_flatline(
        sheet,
        curr_row,
        calc_year_idx,
        final_index,
    )

def import_TotalAdultsHIV(sheet, tags, params, projection):
    modvarTagRow = tags.get('<TotalAdultsHIV MV>', None)
    if modvarTagRow is None:
        return

    calc_year_idx, final_index = _get_year_index_bounds(params, projection)
    total_adults_hiv = np.zeros((HV_Female + 1, final_index + 1))

    curr_row = modvarTagRow + 2
    for s in range(HV_Male, HV_Female + 1):
        curr_row += 1
        total_adults_hiv[s] = _read_year_row_with_flatline(sheet, curr_row, calc_year_idx, final_index)
        curr_row += 1

    projection[HV_TotalAdultsHIVTag] = total_adults_hiv.tolist()

def import_NewlyOnART(sheet, tags, params, projection):
    modvarTagRow = tags.get('<NewlyOnART MV>', None)
    if modvarTagRow is None:
        return

    calc_year_idx, final_index = _get_year_index_bounds(params, projection)
    newly_on_art = np.zeros((HV_Female + 1, HV_CD4_LT50_ART + 1, final_index + 1))

    row = modvarTagRow + 2
    for s in range(HV_BothSexes, HV_Female + 1):
        for h in range(HV_CD4_GT500_ART, HV_CD4_LT50_ART + 1):
            newly_on_art[s, h] = _read_year_row_with_flatline(sheet, row, calc_year_idx, final_index)
            row += 1

    projection[HV_NewlyOnARTTag] = newly_on_art.tolist()

def import_NewlyEligibleART(sheet, tags, params, projection):
    modvarTagRow = tags.get('<NewlyEligibleART MV>', None)
    if modvarTagRow is None:
        return

    calc_year_idx, final_index = _get_year_index_bounds(params, projection)
    newly_eligible_art = np.zeros((HV_Female + 1, HV_CD4_LT50_ART + 1, final_index + 1))

    row = modvarTagRow + 2
    for s in range(HV_BothSexes, HV_Female + 1):
        for h in range(HV_CD4_GT500_ART, HV_CD4_LT50_ART + 1):
            newly_eligible_art[s, h] = _read_year_row_with_flatline(sheet, row, calc_year_idx, final_index)
            row += 1

    projection[HV_NewlyEligibleARTTag] = newly_eligible_art.tolist()

def import_TotalAdultsART(sheet, tags, params, projection):
    modvarTagRow = tags.get('<TotalAdultsART MV>', None)
    if modvarTagRow is None:
        return

    calc_year_idx, final_index = _get_year_index_bounds(params, projection)
    total_adults_art = np.zeros((HV_Female + 1, final_index + 1))

    curr_row = modvarTagRow + 2
    for s in range(HV_Male, HV_Female + 1):
        curr_row += 1
        total_adults_art[s] = _read_year_row_with_flatline(sheet, curr_row, calc_year_idx, final_index)
        curr_row += 1

    projection[HV_TotalAdultsARTTag] = total_adults_art.tolist()

def import_RMultAll(sheet, tags, params, projection):
    modvarTagRow = tags.get('<rMultAll MV>', None)
    if modvarTagRow is None:
        return

    calc_year_idx, final_index = _get_year_index_bounds(params, projection)
    r_mult_all = np.zeros((HV_Female + 1, HV_MSMIDU + 1, final_index + 1))

    curr_row = modvarTagRow + 2
    curr_row += 1
    for s in range(HV_Male, HV_Female + 1):
        for r in range(HV_None, HV_MSMIDU + 1):
            r_mult_all[s, r] = _read_year_row_with_flatline(sheet, curr_row, calc_year_idx, final_index)
            curr_row += 1

    projection[HV_RMultAllTag] = r_mult_all.tolist()

def import_CalcPrevalence(sheet, tags, params, projection):
    modvarTagRow = tags.get('<CalcPrevalence MV>', None)
    if modvarTagRow is None:
        return

    calc_year_idx, final_index = _get_year_index_bounds(params, projection)
    calc_prevalence = np.zeros((HV_Female + 1, HV_MSMIDU + 1, final_index + 1))

    curr_row = modvarTagRow + 2
    curr_row += 1
    for s in range(HV_Male, HV_Female + 1):
        curr_row += 1
        for r in range(HV_None, HV_MSMIDU + 1):
            curr_row += 1
            calc_prevalence[s, r] = _read_year_row_with_flatline(sheet, curr_row, calc_year_idx, final_index)
            curr_row += 1

    projection[HV_CalcPrevalenceTag] = calc_prevalence.tolist()

def import_NewInfections(sheet, tags, params, projection):
    modvarTagRow = tags.get('<NewInfections MV>', None)
    if modvarTagRow is None:
        return

    calc_year_idx, final_index = _get_year_index_bounds(params, projection)
    new_infections = np.zeros((HV_Female + 1, HV_MSMIDU + 1, RN_NoProt + 1, final_index + 1))

    curr_row = modvarTagRow + 2
    for s in range(HV_Male, HV_Female + 1):
        curr_row += 1
        for r in range(HV_None, HV_MSMIDU + 1):
            curr_row += 1
            for v in range(RN_AllVacc, RN_NoProt + 1):
                curr_row += 1
                new_infections[s, r, v] = _read_year_row_with_flatline(sheet, curr_row, calc_year_idx, final_index)
                curr_row += 1

    projection[HV_NewInfectionsTag] = new_infections.tolist()

def import_ExitRate(sheet, tags, params, projection):
    modvarTagRow = tags.get('<ExitRate MV>', None)
    if modvarTagRow is None:
        return

    calc_year_idx, final_index = _get_year_index_bounds(params, projection)
    exit_rate = np.zeros((HV_Female + 1, HV_MSMIDU + 1, HV_CD4_LT50 + 1, final_index + 1))

    row = modvarTagRow + 2
    for s in range(HV_BothSexes, HV_Female):
        for r in range(HV_AllRisk, HV_MSMIDU):
            for h in range(HV_Primary, HV_CD4_LT50):
                exit_rate[s, r, h] = _read_year_row_with_flatline(sheet, row, calc_year_idx, final_index)
                row += 1

    projection[HV_ExitRateTag] = exit_rate.tolist()

def import_AIDSDeaths(sheet, tags, params, projection):
    modvarTagRow = tags.get('<AIDSDeaths MV>', None)
    if modvarTagRow is None:
        return

    calc_year_idx, final_index = _get_year_index_bounds(params, projection)
    aids_deaths = np.zeros((HV_Female + 1, HV_MSMIDU + 1, RN_NoProt + 1, final_index + 1))

    curr_row = modvarTagRow + 2
    for s in range(HV_Male, HV_Female + 1):
        curr_row += 1
        for r in range(HV_None, HV_MSMIDU + 1):
            curr_row += 1
            for v in range(RN_UnV, RN_NoProt + 1):
                curr_row += 1
                aids_deaths[s, r, v] = _read_year_row_with_flatline(sheet, curr_row, calc_year_idx, final_index)
                curr_row += 1

    projection[HV_AIDSDeathsTag] = aids_deaths.tolist()

def import_AIDSDeathsART(sheet, tags, params, projection):
    modvarTagRow = tags.get('<AIDSDeathsART MV>', None)
    if modvarTagRow is None:
        return

    calc_year_idx, final_index = _get_year_index_bounds(params, projection)
    aids_deaths_art = np.zeros((HV_Female + 1, HV_MSMIDU + 1, final_index + 1))

    row = modvarTagRow + 2
    for s in range(HV_BothSexes, HV_Female + 1):
        for r in range(HV_AllRisk, HV_MSMIDU + 1):
            aids_deaths_art[s, r] = _read_year_row_with_flatline(sheet, row, calc_year_idx, final_index)
            row += 1

    projection[HV_AIDSDeathsARTTag] = aids_deaths_art.tolist()

def import_TotalAIDSDeaths(sheet, tags, params, projection):
    modvarTagRow = tags.get('<TotalAIDSDeaths MV>', None)
    if modvarTagRow is None:
        return

    calc_year_idx, final_index = _get_year_index_bounds(params, projection)

    curr_row = modvarTagRow + 3
    projection[HV_TotalAIDSDeathsTag] = _read_year_row_with_flatline(sheet, curr_row, calc_year_idx, final_index)

def import_TotalNewInfection(sheet, tags, params, projection):
    modvarTagRow = tags.get('<TotalNewInfection MV>', None)
    if modvarTagRow is None:
        return

    calc_year_idx, final_index = _get_year_index_bounds(params, projection)

    curr_row = modvarTagRow + 3
    projection[HV_TotalNewInfectionTag] = _read_year_row_with_flatline(sheet, curr_row, calc_year_idx, final_index)

def import_Incidence(sheet, tags, params, projection):
    modvarTagRow = tags.get('<Incidence MV>', None)
    if modvarTagRow is None:
        return

    calc_year_idx, final_index = _get_year_index_bounds(params, projection)

    curr_row = modvarTagRow + 3
    projection[HV_IncidenceTag] = _read_year_row_with_flatline(sheet, curr_row, calc_year_idx, final_index)

def import_IncSexRatio(sheet, tags, params, projection):
    modvarTagRow = tags.get('<IncSexRatio MV>', None)
    if modvarTagRow is None:
        return

    calc_year_idx, final_index = _get_year_index_bounds(params, projection)
    row = modvarTagRow + 2
    projection[HV_IncSexRatioTag] = _read_year_row_with_flatline(sheet, row, calc_year_idx, final_index)

def import_PercentPop(sheet, tags, params, projection):
    modvarTagRow = tags.get('<PercentPop MV>', None)
    if modvarTagRow is None:
        return

    calc_year_idx, final_index = _get_year_index_bounds(params, projection)
    data = np.zeros((HV_Female + 1, final_index + 1))
    curr_row = modvarTagRow + 2
    for s in range(HV_Male, HV_Female + 1):
        curr_row += 1
        data[s] = _read_year_row_with_flatline(sheet, curr_row, calc_year_idx, final_index)
        curr_row += 1
    projection[HV_PercentPopTag] = data.tolist()

def import_InfectionsAverted(sheet, tags, params, projection):
    modvarTagRow = tags.get('<InfectionsAverted MV>', None)
    if modvarTagRow is None:
        return

    calc_year_idx, final_index = _get_year_index_bounds(params, projection)
    row = modvarTagRow + 2
    projection[HV_InfectionsAvertedTag] = _read_year_row_with_flatline(sheet, row, calc_year_idx, final_index)

def import_CumInfectionsAverted(sheet, tags, params, projection):
    modvarTagRow = tags.get('<CumInfectionsAverted MV>', None)
    if modvarTagRow is None:
        return

    calc_year_idx, final_index = _get_year_index_bounds(params, projection)
    row = modvarTagRow + 2
    projection[HV_CumInfectionsAvertedTag] = _read_year_row_with_flatline(sheet, row, calc_year_idx, final_index)

def import_DeathsAverted(sheet, tags, params, projection):
    modvarTagRow = tags.get('<DeathsAverted MV>', None)
    if modvarTagRow is None:
        return

    calc_year_idx, final_index = _get_year_index_bounds(params, projection)
    row = modvarTagRow + 2
    projection[HV_DeathsAvertedTag] = _read_year_row_with_flatline(sheet, row, calc_year_idx, final_index)

def import_CumDeathsAverted(sheet, tags, params, projection):
    modvarTagRow = tags.get('<CumDeathsAverted MV>', None)
    if modvarTagRow is None:
        return

    calc_year_idx, final_index = _get_year_index_bounds(params, projection)
    row = modvarTagRow + 2
    projection[HV_CumDeathsAvertedTag] = _read_year_row_with_flatline(sheet, row, calc_year_idx, final_index)

def import_ARTCoverageByRG(sheet, tags, params, projection):
    modvarTagRow = tags.get('<ARTCoverageByRG MV>', None)
    if modvarTagRow is None:
        return

    calc_year_idx, final_index = _get_year_index_bounds(params, projection)
    data = np.zeros((HV_Female + 1, HV_MSMIDU + 1, final_index + 1))
    curr_row = modvarTagRow + 2
    for s in range(HV_BothSexes, HV_Female + 1):
        for r in range(HV_None, HV_MSMIDU + 1):
            data[s, r] = _read_year_row_with_flatline(sheet, curr_row, calc_year_idx, final_index)
            curr_row += 1
    projection[HV_ARTCoverageByRGTag] = data.tolist()

def import_TotalARTCoverage(sheet, tags, params, projection):
    modvarTagRow = tags.get('<TotalARTCoverage MV>', None)
    if modvarTagRow is None:
        return

    calc_year_idx, final_index = _get_year_index_bounds(params, projection)
    data = np.zeros((HV_Female + 1, final_index + 1))
    curr_row = modvarTagRow + 2
    for s in range(HV_BothSexes, HV_Female + 1):
        data[s] = _read_year_row_with_flatline(sheet, curr_row, calc_year_idx, final_index)
        curr_row += 1
    projection[HV_TotalARTCoverageTag] = data.tolist()

def import_NewHIV(sheet, tags, params, projection):
    modvarTagRow = tags.get('<NewHIV MV>', None)
    if modvarTagRow is None:
        return

    calc_year_idx, final_index = _get_year_index_bounds(params, projection)
    data = np.zeros((HV_Female + 1, final_index + 1))
    curr_row = modvarTagRow + 2
    for i in range(HV_BothSexes, HV_Female + 1):
        data[i] = _read_year_row_with_flatline(sheet, curr_row, calc_year_idx, final_index)
        curr_row += 1
    projection[HV_NewHIVTag] = data.tolist()

def import_FitData(sheet, tags, params, projection):
    modvarTagRow = tags.get('<FitData MV2>', None)
    if modvarTagRow is None:
        return

    curr_row = modvarTagRow + 2
    count = int(sheet[curr_row, GB_RW_NotesCol])
    curr_row += 1
    records = []
    for i in range(count):
        records.append({
            'pop':    int(sheet[curr_row, 1]),
            'sex':    int(sheet[curr_row, 2]),
            'year':   int(sheet[curr_row, 3]),
            'value':  float(sheet[curr_row, 4]),
            'lower':  float(sheet[curr_row, 5]),
            'upper':  float(sheet[curr_row, 6]),
            'ssize':  float(sheet[curr_row, 7]),
            'use':    bool(int(sheet[curr_row, 8])),
            'source': str(sheet[curr_row, 9]),
        })
        curr_row += 1
    projection[HV_FitDataTag] = records

def import_FitParamSet(sheet, tags, params, projection):
    modvarTagRow = tags.get('<FitParamSet MV>', None)
    if modvarTagRow is None:
        return

    curr_row = modvarTagRow + 2
    curr_row += 1  # header row with count
    count = min(int(sheet[curr_row, GB_RW_NotesCol]), HV_MaxFitParams)
    curr_row += 1  # blank separator row
    param_set = {}
    for i in range(count):
        curr_row += 1
        index = int(sheet[curr_row, 1])
        param_set[index] = {
            'prior':  int(sheet[curr_row, 2]),
            'init':   float(sheet[curr_row, 3]),
            'mu':     float(sheet[curr_row, 4]),
            'sd':     float(sheet[curr_row, 5]),
            'value':  float(sheet[curr_row, 6]),
            'use':    bool(int(sheet[curr_row, 7])),
            'fitted': bool(int(sheet[curr_row, 8])),
        }
    projection[HV_FitParamSetTag] = param_set

def import_FitControl(sheet, tags, params, projection):
    modvarTagRow = tags.get('<FitControl MV>', None)
    if modvarTagRow is None:
        return

    curr_row = modvarTagRow + 2
    curr_row += 1  # data row
    projection[HV_FitControlTag] = {
        'MaxIterations':  int(sheet[curr_row, 1]),
        'ErrorTolerance': float(sheet[curr_row, 2]),
        'PrevWeight':     int(sheet[curr_row, 3]),
    }

def import_LowRiskCondomUseFromFP(sheet, tags, params, projection):
    modvarTagRow = tags.get('<lowRiskCondomUseFromFP MV>', None)
    if modvarTagRow is None:
        return

    row = modvarTagRow + 2
    projection[HV_LowRiskCondomUseFromFPTag] = bool(_parse_value(sheet[row, GB_RW_DataStartCol]))


