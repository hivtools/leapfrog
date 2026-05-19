import numpy as np

from src._spectrum.AvenirCommon.Util import gb_read_csv_sheet, getAllTags

from SpectrumCommon.Modvars.GB.GBDefs import createProjectionParams
from SpectrumCommon.Const.GB import *
from src._spectrum.SpectrumCommon.Const.RN import *




def openRN(file, params: createProjectionParams, projection: dict):
    sheet = gb_read_csv_sheet(file)
    tags = getAllTags(sheet)

    _import_tag_value(sheet, tags, projection, '<ProjectionValid MV2>',          RN_ProjectionValidTag)
    _import_tag_value(sheet, tags, projection, '<ProjectionValidDate MV>',       RN_ProjectionValidDateTag)
    _import_tag_value(sheet, tags, projection, '<Data Source MV>',               RN_DataSourceTag)
    _import_tag_value(sheet, tags, projection, '<VariablesRW MV>',               RN_VariablesRWTag)
    _import_tag_value(sheet, tags, projection, '<MaxInterventions MV>',          RN_MaxInterventionsTag)
    _import_tag_value(sheet, tags, projection, '<MaxPOPConstants MV>',           RN_MaxPOPConstantsTag)
    _import_tag_value(sheet, tags, projection, '<MaxPSConstants MV>',            RN_MaxPSConstantsTag)
    _import_tag_value(sheet, tags, projection, '<MaxSummaryTableConstants MV>',  RN_MaxSummaryTableConstantsTag)
    _import_tag_value(sheet, tags, projection, '<FirstYearOfEstimates MV>',      RN_FirstYearOfEstimatesTag)
    _import_tag_value(sheet, tags, projection, '<FirstYearOfEstimatesCBIdx MV>', RN_FirstYearOfEstimatesCBIdxTag)
    import_PopulationSizes(sheet, tags, params, projection)
    import_UserGeneralPop(sheet, tags, params, projection)
    import_UserMostAtRiskPop(sheet, tags, params, projection)
    import_Coverage(sheet, tags, params, projection)
    import_UserGeneralPopCoverage(sheet, tags, params, projection)
    import_UserMostAtRiskPopCoverage(sheet, tags, params, projection)
    import_UseRNMData(sheet, tags, params, projection)
    import_CurrencyForMitigationCBIdx(sheet, tags, params, projection)
    import_PrEPCoverage(sheet, tags, params, projection)
    import_PrEPEffectiveness(sheet, tags, params, projection)
    import_VaccineCovType(sheet, tags, params, projection)
    import_VacCoverage(sheet, tags, params, projection)
    import_VaccineEffectiveness(sheet, tags, params, projection)
    import_VaccineBehavEffect(sheet, tags, params, projection)
    import_TypeOfVaccine(sheet, tags, params, projection)
    import_VaccineTargeting(sheet, tags, params, projection)
    import_CureCovType(sheet, tags, params, projection)
    import_CureCoverage(sheet, tags, params, projection)
    import_CureEffectiveness(sheet, tags, params, projection)

    import_ADHTreatCov(sheet, tags, params, projection)
    import_ADHTreatReducMort(sheet, tags, params, projection)
    import_PointOfCare(sheet, tags, params, projection)
    import_POCEffect(sheet, tags, params, projection)
    import_UnitCosts(sheet, tags, params, projection)
    import_UserGeneralPopUnitCosts(sheet, tags, params, projection)
    import_UserMostAtRiskPopUnitCosts(sheet, tags, params, projection)
    import_CurrencyForUnitCostsCBIdx(sheet, tags, params, projection)
    import_PreTest(sheet, tags, params, projection)
    import_PostTest(sheet, tags, params, projection)
    import_PostNatal(sheet, tags, params, projection)
    import_Mother(sheet, tags, params, projection)
    import_PCRForInfantAfterBirth(sheet, tags, params, projection)
    import_InfantAfterBF(sheet, tags, params, projection)
    import_Nevirapine200(sheet, tags, params, projection)
    import_NevirapineInfant(sheet, tags, params, projection)
    import_AZT(sheet, tags, params, projection)
    import_ThreeTC(sheet, tags, params, projection)
    import_TripleTreatment(sheet, tags, params, projection)
    import_TripleProphylaxis(sheet, tags, params, projection)
    import_ServiceDelivery(sheet, tags, params, projection)
    import_Formula(sheet, tags, params, projection)
    import_FirstLineARTDrugs(sheet, tags, params, projection)
    import_SecondLineARTDrugs(sheet, tags, params, projection)
    import_AdditARTDrugCostsTBmale(sheet, tags, params, projection)
    import_AdditARTDrugCostsTBfemale(sheet, tags, params, projection)
    import_LabCostsARTTr(sheet, tags, params, projection)
    import_DrugLabCostsTrInf(sheet, tags, params, projection)
    import_CotrimProphylaxis(sheet, tags, params, projection)
    import_TBProphylaxis(sheet, tags, params, projection)
    import_NutritionSuppSixMo(sheet, tags, params, projection)
    import_ChildrenARVDrugs(sheet, tags, params, projection)
    import_ChildrenLabCostsARTTr(sheet, tags, params, projection)
    import_CostPerInpatientDay(sheet, tags, params, projection)
    import_CostPerOutpatientDay(sheet, tags, params, projection)
    import_ARTinpatientDays(sheet, tags, params, projection)
    import_ARToutpatientDays(sheet, tags, params, projection)
    import_OItreatmentInpatientDays(sheet, tags, params, projection)
    import_OItreatmentOutpatientDays(sheet, tags, params, projection)
    import_MigFirstToSecondLine(sheet, tags, params, projection)
    import_TestAndVisitSchedule(sheet, tags, params, projection)
    import_ARTUnitCosts(sheet, tags, params, projection)
    import_PercentOnART(sheet, tags, params, projection)
    import_CurrencyForProgramSupportCBIdx(sheet, tags, params, projection)
    import_ProgramSupport(sheet, tags, params, projection)
    import_UserProgramSupport(sheet, tags, params, projection)
    import_MitigationProgramsEntered(sheet, tags, params, projection)
    import_Mitigation(sheet, tags, params, projection)
    import_MethodMix(sheet, tags, params, projection)
    import_CurrencyDisplayedCBIdx(sheet, tags, params, projection)
    import_ResourcesRequired(sheet, tags, params, projection)
    import_NumberPeopleReached(sheet, tags, params, projection)
    import_PMTCTCosts(sheet, tags, params, projection)
    import_TotalCosts(sheet, tags, params, projection)
    import_OptimizerVars(sheet, tags, params, projection)
    return None


############### Start reading in RN Modvars ######################################


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


def _to_float(value, default=0.0):
    if value == '' or value is None:
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _import_tag_value(sheet, tags, projection, source_tag: str, projection_tag: str):
    modvarTagRow = tags.get(source_tag, None)
    if modvarTagRow is None:
        return
    try:
        row = modvarTagRow + 2
        projection[projection_tag] = _parse_value(sheet[row, GB_RW_DataStartCol])
    except Exception as e:
        print(f'Error importing {projection_tag} from tag {source_tag}: {e}')


def _get_rn_year_index_bounds(params):
    """Return (calc_year_idx, final_index) based on projection params.

    Mirrors Delphi's GetGBCalcYearIdx / GetGBFinalYearIdx: both are
    offsets from GB_NativeYear (1970).
    """
    calc_year_idx = max(0, int(params.firstYear) - GB_NativeYear)
    final_index = max(calc_year_idx, int(params.finalYear) - GB_NativeYear)
    return calc_year_idx, final_index


def _read_rn_year_row(sheet, row, calc_year_idx, final_index,
                      start_col=GB_RW_DataStartCol):
    """Read one row of year data into a list indexed [0..final_index].

    Cells are consumed sequentially from *start_col*; empty cells repeat
    the previous value (flatline), matching Delphi's t2+1..t3 extension.
    """
    values = [0.0] * (final_index + 1)
    col = start_col
    last_value = 0.0
    # print(sheet[row, col:])
    for t in range(calc_year_idx, final_index + 1):
        cell_value = sheet[row, col]
        if cell_value != '':
            last_value = _to_float(_parse_value(cell_value), last_value)
            col += 1
        else:
            pass
        values[t] = last_value
    return values


def _read_rn_year_row_contiguous(sheet, row, calc_year_idx, final_index,
                                 start_col=GB_RW_DataStartCol):
    """Read one row of contiguous year columns into [0..final_index]."""
    values = [0.0] * (final_index + 1)
    col = start_col
    for t in range(calc_year_idx, final_index + 1):
        values[t] = _to_float(_parse_value(sheet[row, col]))
        col += 1
    return values


def import_PopulationSizes(sheet, tags, params, projection):
    modvarTagRow = tags.get('<PopulationSizes MV2>', None)
    if modvarTagRow is None or modvarTagRow < 0:
        return

    calc_year_idx, final_index = _get_rn_year_index_bounds(params)

    # Row layout after the tag:
    #   tagRow+1  description row
    #   tagRow+2  header row (Name / Master ID / year labels)  <- Inc(currRow) in Delphi
    #   tagRow+3  first data row
    row = modvarTagRow + 3

    # Use MaxPOPConstants recorded by import_MaxPOPConstants if available,
    # otherwise fall back to the compiled-in constant.
    max_pop = projection.get(RN_MaxPOPConstantsTag, RN_POP_MaxPopulations)
    try:
        max_pop = int(max_pop)
    except (TypeError, ValueError):
        max_pop = RN_POP_MaxPopulations

    # Delphi stores Value[CurrID, t]; we key by MstID because Python has
    # no GetRN_POPConstantCurrID mapping.  Consumers look up by MstID.
    result = {}
    for _ in range(max_pop):
        mst_id = _parse_value(sheet[row, GB_RW_DataStartCol])
        if mst_id == '' or mst_id is None:
            break
        # c1 = GB_RW_DataStartCol + 1 (year data is one column to the right
        # of the Master ID column, matching Delphi's GetGBYearAndColIndices
        # call with GB_RW_DataStartCol + 1).
        year_data = _read_rn_year_row(sheet, row, calc_year_idx, final_index,
                                      start_col=GB_RW_DataStartCol + 1)
        result[int(mst_id)] = year_data
        row += 1

    projection[RN_PopulationSizesTag] = result


def import_UserGeneralPop(sheet, tags, params, projection):
    modvarTagRow = tags.get('<UserGeneralPop MV2>', None)
    if modvarTagRow is None or modvarTagRow < 0:
        return

    calc_year_idx, final_index = _get_rn_year_index_bounds(params)

    # Delphi layout after tag row:
    #   tagRow+1  count at GB_RW_DataStartCol           (Inc → read count)
    #   tagRow+2  (skipped)                             (Inc)
    #   tagRow+3  first object: name / PerNum / Value   (Inc → first obj)
    #   tagRow+4  ResourcesRequired year data
    #   tagRow+5  NumberPeopleReached year data
    #   (repeat for each subsequent object)
    count = _parse_value(sheet[modvarTagRow + 1, GB_RW_DataStartCol])
    try:
        count = int(count)
    except (TypeError, ValueError):
        count = 0

    row = modvarTagRow + 3
    result = []
    for _ in range(count):
        obj = {
            'UserGenPop': sheet[row, GB_RW_DataStartCol],
            'PerNum':     _parse_value(sheet[row, GB_RW_DataStartCol + 1]),
            'Value':      _to_float(_parse_value(sheet[row, GB_RW_DataStartCol + 2])),
        }
        row += 1
        obj['ResourcesRequired']  = _read_rn_year_row(sheet, row, calc_year_idx, final_index)
        row += 1
        obj['NumberPeopleReached'] = _read_rn_year_row(sheet, row, calc_year_idx, final_index)
        row += 1
        result.append(obj)

    projection[RN_UserGeneralPopTag] = result


def import_UserMostAtRiskPop(sheet, tags, params, projection):
    modvarTagRow = tags.get('<UserMostAtRiskPop MV2>', None)
    if modvarTagRow is None or modvarTagRow < 0:
        return

    calc_year_idx, final_index = _get_rn_year_index_bounds(params)

    # Identical layout to UserGeneralPop:
    #   tagRow+1  count at GB_RW_DataStartCol
    #   tagRow+2  (skipped - "Skip Text")
    #   tagRow+3  first object: UserMARPop / PerNum / Value
    #   tagRow+4  ResourcesRequired year data
    #   tagRow+5  NumberPeopleReached year data
    count = _parse_value(sheet[modvarTagRow + 1, GB_RW_DataStartCol])
    try:
        count = int(count)
    except (TypeError, ValueError):
        count = 0

    row = modvarTagRow + 3
    result = []
    for _ in range(count):
        obj = {
            'UserMARPop': sheet[row, GB_RW_DataStartCol],
            'PerNum':     _parse_value(sheet[row, GB_RW_DataStartCol + 1]),
            'Value':      _to_float(_parse_value(sheet[row, GB_RW_DataStartCol + 2])),
        }
        row += 1
        obj['ResourcesRequired']   = _read_rn_year_row(sheet, row, calc_year_idx, final_index)
        row += 1
        obj['NumberPeopleReached'] = _read_rn_year_row(sheet, row, calc_year_idx, final_index)
        row += 1
        result.append(obj)

    projection[RN_UserMostAtRiskPopTag] = result


def import_Coverage(sheet, tags, params, projection):
    modvarTagRow = tags.get('<Coverage MV>', None)
    if modvarTagRow is None or modvarTagRow < 0:
        return

    calc_year_idx, final_index = _get_rn_year_index_bounds(params)

    # Row layout:
    #   tagRow+1  description row
    #   tagRow+2  header strings row  <- Inc(currRow) in Delphi
    #   tagRow+3  first data row
    # Loop count: MaxInterventions - RN_NumIntervExcludedFromCov
    # MstID at GB_RW_DataStartCol (col 3); year data at GB_RW_DataStartCol+1 (col 4)
    max_interventions = projection.get(RN_MaxInterventionsTag, RN_MaxInterventions)
    try:
        max_interventions = int(max_interventions)
    except (TypeError, ValueError):
        max_interventions = RN_MaxInterventions

    count = max_interventions - len(RN_NotInCov)
    row = modvarTagRow + 3
    result = np.zeros((max_interventions + 1, final_index + 1))
    for _ in range(count):
        mst_id = _parse_value(sheet[row, GB_RW_DataStartCol])
        if mst_id != '' and mst_id is not None and mst_id != 0:
            year_data = _read_rn_year_row(sheet, row, calc_year_idx, final_index,
                                          start_col=GB_RW_DataStartCol + 1)
            result[int(mst_id)] = year_data
        row += 1

    projection[RN_CoverageTag] = result


def import_UserGeneralPopCoverage(sheet, tags, params, projection):
    modvarTagRow = tags.get('<UserGeneralPopCoverage MV>', None)
    if modvarTagRow is None or modvarTagRow < 0:
        return

    calc_year_idx, final_index = _get_rn_year_index_bounds(params)

    # Delphi layout after tag row:
    #   tagRow+1  count at GB_RW_DataStartCol
    #   tagRow+2  (skipped)
    #   tagRow+3  first data row: UserGenPop + year values
    count = _parse_value(sheet[modvarTagRow + 1, GB_RW_DataStartCol])
    try:
        count = int(count)
    except (TypeError, ValueError):
        count = 0

    row = modvarTagRow + 3
    result = []
    for _ in range(count):
        obj = {
            'UserGenPop': sheet[row, GB_RW_DataStartCol],
            'Value': _read_rn_year_row(sheet, row, calc_year_idx, final_index,
                                       start_col=GB_RW_DataStartCol + 1),
        }
        result.append(obj)
        row += 1

    projection[RN_UserGeneralPopCoverageTag] = result


def import_UserMostAtRiskPopCoverage(sheet, tags, params, projection):
    modvarTagRow = tags.get('<UserMostAtRiskPopCoverage MV>', None)
    if modvarTagRow is None or modvarTagRow < 0:
        return

    calc_year_idx, final_index = _get_rn_year_index_bounds(params)

    # Delphi layout after tag row:
    #   tagRow+1  count at GB_RW_DataStartCol
    #   tagRow+2  (skipped)
    #   tagRow+3  first data row: UserMARPop + year values
    count = _parse_value(sheet[modvarTagRow + 1, GB_RW_DataStartCol])
    try:
        count = int(count)
    except (TypeError, ValueError):
        count = 0

    row = modvarTagRow + 3
    result = []
    for _ in range(count):
        obj = {
            'UserMARPop': sheet[row, GB_RW_DataStartCol],
            'Value': _read_rn_year_row(sheet, row, calc_year_idx, final_index,
                                       start_col=GB_RW_DataStartCol + 1),
        }
        result.append(obj)
        row += 1

    projection[RN_UserMostAtRiskPopCoverageTag] = result


def import_UseRNMData(sheet, tags, params, projection):
    modvarTagRow = tags.get('<UseRNMData MV>', None)
    if modvarTagRow is None or modvarTagRow < 0:
        return

    row = modvarTagRow + 2
    value = _parse_value(sheet[row, GB_RW_DataStartCol])
    if isinstance(value, str):
        normalized = value.strip().lower()
        projection[RN_UseRNMDataTag] = normalized in ('1', 'true', 'yes', 'y')
    else:
        projection[RN_UseRNMDataTag] = bool(value)


def import_CurrencyForMitigationCBIdx(sheet, tags, params, projection):
    modvarTagRow = tags.get('<CurrencyForMitigationCBIdx MV>', None)
    if modvarTagRow is None or modvarTagRow < 0:
        return

    row = modvarTagRow + 2
    value = _parse_value(sheet[row, GB_RW_DataStartCol])
    try:
        projection[RN_CurrencyForMitigationCBIdxTag] = int(value)
    except (TypeError, ValueError):
        projection[RN_CurrencyForMitigationCBIdxTag] = 0


def import_PrEPCoverage(sheet, tags, params, projection):
    modvarTagRow = tags.get('<PrEPCoverage MV>', None)
    if modvarTagRow is None or modvarTagRow < 0:
        return

    calc_year_idx, final_index = _get_rn_year_index_bounds(params)

    # Delphi starts with Inc(currRow), then reads male rows followed by female rows.
    row = modvarTagRow + 2
    result = np.zeros((RN_Female + 1, RN_MSMIDU + 1, final_index + 1))

    for r in range(RN_LRH, RN_MSMIDU + 1):
        result[RN_Male][r] = _read_rn_year_row_contiguous(
            sheet, row, calc_year_idx, final_index, start_col=GB_RW_DataStartCol
        )
        row += 1

    for r in range(RN_LRH, RN_IDU + 1):
        result[RN_Female][r] = _read_rn_year_row_contiguous(
            sheet, row, calc_year_idx, final_index, start_col=GB_RW_DataStartCol
        )
        row += 1

    projection[RN_PrEPCoverageTag] = result


def import_PrEPEffectiveness(sheet, tags, params, projection):
    tag_row_mv3 = tags.get('<PrEPEffectiveness MV3>', None)
    # tag_row_mv2 = tags.get('<PrEPEffectiveness MV2>', None)
    # tag_row_mv1 = tags.get('<PrEPEffectiveness MV>', None)

    result = np.zeros((RN_MaxInterventions + 1, RN_Duration + 1))

    tag_row_mv3 += 1
    if tag_row_mv3 is not None and tag_row_mv3 >= 0:
        row = tag_row_mv3 + 2
        while sheet[row, GB_RW_TagCol] != '<End>':
            mst_id = _parse_value(sheet[row, GB_RW_DataStartCol])
            if mst_id == '' or mst_id is None:
                break
            try:
                mst_id = int(mst_id)
            except (TypeError, ValueError):
                row += 1
                continue

            for e in range(RN_Effectiveness, RN_DurationMonths + 1):
                result[mst_id][e] = _to_float(_parse_value(sheet[row, GB_RW_DataStartCol + e]))
            row += 1

    # elif tag_row_mv2 is not None and tag_row_mv2 >= 0:
    #     row = tag_row_mv2 + 2
    #     while sheet[row, GB_RW_TagCol] != '<End>':
    #         mst_id = _parse_value(sheet[row, GB_RW_DataStartCol])
    #         if mst_id == '' or mst_id is None:
    #             break
    #         try:
    #             mst_id = int(mst_id)
    #         except (TypeError, ValueError):
    #             row += 1
    #             continue

    #         for e in range(RN_Effectiveness, RN_Substitution + 1):
    #             _set_eff(e, mst_id, _to_float(_parse_value(sheet[row, GB_RW_DataStartCol + e])))
    #         row += 1

    # elif tag_row_mv1 is not None and tag_row_mv1 >= 0:
    #     row = tag_row_mv1 + 2
    #     for e in range(RN_Effectiveness, RN_Adherence + 1):
    #         for m in (RN_PrEPOralDaily, RN_PrEPInject1Mo, RN_PrEPRing):
    #             _set_eff(e, m, _to_float(_parse_value(sheet[row, GB_RW_DataStartCol])))
    #             row += 1
    #             # Delphi skips deprecated gel row after Inject 1-month.
    #             if m == RN_PrEPInject1Mo:
    #                 row += 1

    else:
        return

    projection[RN_PrEPEffectivenessTag] = result


def import_VaccineCovType(sheet, tags, params, projection):
    modvarTagRow = tags.get('<VaccineCovType MV>', None)
    if modvarTagRow is None or modvarTagRow < 0:
        return

    row = modvarTagRow + 2
    value = _parse_value(sheet[row, GB_RW_DataStartCol])
    try:
        projection[RN_VaccineCovTypeTag] = int(value)
    except (TypeError, ValueError):
        projection[RN_VaccineCovTypeTag] = 0


def import_VacCoverage(sheet, tags, params, projection):
    modvarTagRow = tags.get('<VacCoverage MV>', None)
    if modvarTagRow is None or modvarTagRow < 0:
        return

    calc_year_idx, final_index = _get_rn_year_index_bounds(params)

    # Delphi skips one row, then reads RN_AllRisk..RN_MSM_F with an extra
    # row skip when crossing to female aggregate (RN_AllRisk_F).
    row = modvarTagRow + 3
    result = np.zeros((RN_MSM_F + 1, final_index + 1))
    for r in range(RN_AllRisk, RN_MSM_F + 1):
        if r == RN_AllRisk_F:
            row += 1
        result[r] = _read_rn_year_row_contiguous(
            sheet, row, calc_year_idx, final_index, start_col=GB_RW_DataStartCol
        )
        row += 1

    projection[RN_VacCoverageTag] = result


def import_VaccineEffectiveness(sheet, tags, params, projection):
    modvarTagRow = tags.get('<VaccineEffectiveness MV>', None)
    if modvarTagRow is None or modvarTagRow < 0:
        return

    # Delphi reads each parameter as: skip label row, then read value row.
    row = modvarTagRow + 1
    result = np.zeros(RN_Duration + 1)
    for r in range(RN_Efficacy, RN_Duration + 1):
        row += 1
        result[r] = _to_float(_parse_value(sheet[row, GB_RW_DataStartCol]))
        row += 1

    projection[RN_VaccineEffectivenessTag] = result


def import_VaccineBehavEffect(sheet, tags, params, projection):
    modvarTagRow = tags.get('<VaccineBehavEffect MV>', None)
    if modvarTagRow is None or modvarTagRow < 0:
        return

    row = modvarTagRow + 2
    projection[RN_VaccineBehavEffectTag] = {
        RN_AmongVacc: _to_float(_parse_value(sheet[row, GB_RW_DataStartCol])),
        RN_AmongAdults: _to_float(_parse_value(sheet[row + 1, GB_RW_DataStartCol])),
    }


def import_TypeOfVaccine(sheet, tags, params, projection):
    modvarTagRow = tags.get('<TypeOfVaccine MV>', None)
    if modvarTagRow is None or modvarTagRow < 0:
        return

    row = modvarTagRow + 2
    value = _parse_value(sheet[row, GB_RW_DataStartCol])
    try:
        projection[RN_TypeOfVaccineTag] = int(value)
    except (TypeError, ValueError):
        projection[RN_TypeOfVaccineTag] = 0


def import_VaccineTargeting(sheet, tags, params, projection):
    modvarTagRow = tags.get('<VaccineTargeting MV>', None)
    if modvarTagRow is None or modvarTagRow < 0:
        return

    row = modvarTagRow + 2
    value = _parse_value(sheet[row, GB_RW_DataStartCol])
    try:
        projection[RN_VaccineTargetingTag] = int(value)
    except (TypeError, ValueError):
        projection[RN_VaccineTargetingTag] = 0


def import_CureCovType(sheet, tags, params, projection):
    modvarTagRow = tags.get('<CureCovType MV>', None)
    if modvarTagRow is None or modvarTagRow < 0:
        return

    row = modvarTagRow + 2
    value = _parse_value(sheet[row, GB_RW_DataStartCol])
    try:
        projection[RN_CureCovTypeTag] = int(value)
    except (TypeError, ValueError):
        projection[RN_CureCovTypeTag] = 0


def import_CureCoverage(sheet, tags, params, projection):
    modvarTagRow = tags.get('<CureCoverage MV>', None)
    if modvarTagRow is None or modvarTagRow < 0:
        return

    calc_year_idx, final_index = _get_rn_year_index_bounds(params)

    # Same Delphi layout/pattern as vaccine coverage.
    row = modvarTagRow + 3
    result = np.zeros((RN_MSM_F + 1, final_index + 1))
    for r in range(RN_AllRisk, RN_MSM_F + 1):
        if r == RN_AllRisk_F:
            row += 1
        result[r] = _read_rn_year_row_contiguous(
            sheet, row, calc_year_idx, final_index, start_col=GB_RW_DataStartCol
        )
        row += 1

    projection[RN_CureCoverageTag] = result


def import_CureEffectiveness(sheet, tags, params, projection):
    modvarTagRow = tags.get('<CureEffectiveness MV>', None)
    if modvarTagRow is None or modvarTagRow < 0:
        return

    # Same Delphi layout/pattern as vaccine effectiveness.
    row = modvarTagRow + 1
    result = np.zeros(RN_Duration + 1)
    for r in range(RN_Efficacy, RN_Duration + 1):
        row += 1
        result[r] = _to_float(_parse_value(sheet[row, GB_RW_DataStartCol]))
        row += 1

    projection[RN_CureEffectivenessTag] = result


def import_ADHTreatCov(sheet, tags, params, projection):
    modvarTagRow = tags.get('<ADHTreatCov MV>', None)
    if modvarTagRow is None or modvarTagRow < 0:
        return

    calc_year_idx, final_index = _get_rn_year_index_bounds(params)

    row = modvarTagRow + 2
    projection[RN_ADHTreatCovTag] = _read_rn_year_row_contiguous(
        sheet, row, calc_year_idx, final_index, start_col=GB_RW_DataStartCol
    )


def import_ADHTreatReducMort(sheet, tags, params, projection):
    modvarTagRow = tags.get('<ADHTreatReducMort MV>', None)
    if modvarTagRow is None or modvarTagRow < 0:
        return

    row = modvarTagRow + 2
    projection[RN_ADHTreatReducMortTag] = _to_float(_parse_value(sheet[row, GB_RW_DataStartCol]))


def import_PointOfCare(sheet, tags, params, projection):
    modvarTagRow = tags.get('<PointOfCare MV>', None)
    if modvarTagRow is None or modvarTagRow < 0:
        return

    calc_year_idx, final_index = _get_rn_year_index_bounds(params)

    # Delphi POCCoverage reads two rows: CD4 and VL, each with year values.
    row = modvarTagRow + 2
    result = np.zeros((RN_POC_VL + 1, final_index + 1))
    for r in range(RN_POC_CD4, RN_POC_VL + 1):
        result[r] = _read_rn_year_row_contiguous(
            sheet, row, calc_year_idx, final_index, start_col=GB_RW_DataStartCol
        )
        row += 1

    projection[RN_PointOfCareTag] = result


def import_POCEffect(sheet, tags, params, projection):
    modvarTagRow = tags.get('<POCEffect MV>', None)
    if modvarTagRow is None or modvarTagRow < 0:
        return

    row = modvarTagRow + 2
    # Delphi stores this as value[POCType, effectCol], with effectCol fixed at 1.
    projection[RN_POCEffectTag] = {
        RN_POC_CD4: _to_float(_parse_value(sheet[row, GB_RW_DataStartCol])),
        RN_POC_VL: _to_float(_parse_value(sheet[row + 1, GB_RW_DataStartCol])),
    }


def import_UnitCosts(sheet, tags, params, projection):
    modvarTagRow = tags.get('<UnitCosts MV>', None)
    if modvarTagRow is None or modvarTagRow < 0:
        return

    calc_year_idx, final_index = _get_rn_year_index_bounds(params)

    # Delphi skips header row, then loops MaxInterventionsRW - excluded-from-UC.
    max_interventions = projection.get(RN_MaxInterventionsTag, RN_MaxInterventions)
    try:
        max_interventions = int(max_interventions)
    except (TypeError, ValueError):
        max_interventions = RN_MaxInterventions

    count = max_interventions - RN_NumIntervExcludedFromUC
    row = modvarTagRow + 3
    result = {}
    for _ in range(count):
        mst_id = _parse_value(sheet[row, GB_RW_DataStartCol])
        if mst_id != '' and mst_id is not None:
            try:
                key = int(mst_id)
            except (TypeError, ValueError):
                key = mst_id
            result[key] = _read_rn_year_row_contiguous(
                sheet, row, calc_year_idx, final_index, start_col=GB_RW_DataStartCol + 1
            )
        row += 1

    projection[RN_UnitCostsTag] = result


def import_UserGeneralPopUnitCosts(sheet, tags, params, projection):
    modvarTagRow = tags.get('<UserGeneralPopUnitCosts MV>', None)
    if modvarTagRow is None or modvarTagRow < 0:
        return

    calc_year_idx, final_index = _get_rn_year_index_bounds(params)

    # Delphi layout after tag row:
    #   tagRow+1  count
    #   tagRow+2  skipped
    #   tagRow+3  first data row: UserGenPop + year values
    count = _parse_value(sheet[modvarTagRow + 1, GB_RW_DataStartCol])
    try:
        count = int(count)
    except (TypeError, ValueError):
        count = 0

    row = modvarTagRow + 3
    result = []
    for _ in range(count):
        obj = {
            'UserGenPop': sheet[row, GB_RW_DataStartCol],
            'Value': _read_rn_year_row_contiguous(
                sheet, row, calc_year_idx, final_index, start_col=GB_RW_DataStartCol + 1
            ),
        }
        result.append(obj)
        row += 1

    projection[RN_UserGeneralPopUnitCostsTag] = result


def import_UserMostAtRiskPopUnitCosts(sheet, tags, params, projection):
    modvarTagRow = tags.get('<UserMostAtRiskPopUnitCosts MV>', None)
    if modvarTagRow is None or modvarTagRow < 0:
        return

    calc_year_idx, final_index = _get_rn_year_index_bounds(params)

    count = _parse_value(sheet[modvarTagRow + 1, GB_RW_DataStartCol])
    try:
        count = int(count)
    except (TypeError, ValueError):
        count = 0

    row = modvarTagRow + 3
    result = []
    for _ in range(count):
        obj = {
            'UserMARPop': sheet[row, GB_RW_DataStartCol],
            'Value': _read_rn_year_row_contiguous(
                sheet, row, calc_year_idx, final_index, start_col=GB_RW_DataStartCol + 1
            ),
        }
        result.append(obj)
        row += 1

    projection[RN_UserMostAtRiskPopUnitCostsTag] = result


def import_CurrencyForUnitCostsCBIdx(sheet, tags, params, projection):
    modvarTagRow = tags.get('<CurrencyForUnitCostsCBIdx MV>', None)
    if modvarTagRow is None or modvarTagRow < 0:
        return

    row = modvarTagRow + 2
    value = _parse_value(sheet[row, GB_RW_DataStartCol])
    try:
        projection[RN_CurrencyForUnitCostsCBIdxTag] = int(value)
    except (TypeError, ValueError):
        projection[RN_CurrencyForUnitCostsCBIdxTag] = 0


def import_PreTest(sheet, tags, params, projection):
    modvarTagRow = tags.get('<PreTest MV>', None)
    if modvarTagRow is None or modvarTagRow < 0:
        return

    calc_year_idx, final_index = _get_rn_year_index_bounds(params)

    row = modvarTagRow + 2
    projection[RN_PreTestTag] = _read_rn_year_row_contiguous(
        sheet, row, calc_year_idx, final_index, start_col=GB_RW_DataStartCol
    )


def import_PostTest(sheet, tags, params, projection):
    modvarTagRow = tags.get('<PostTest MV>', None)
    if modvarTagRow is None or modvarTagRow < 0:
        return

    calc_year_idx, final_index = _get_rn_year_index_bounds(params)

    row = modvarTagRow + 2
    projection[RN_PostTestTag] = _read_rn_year_row_contiguous(
        sheet, row, calc_year_idx, final_index, start_col=GB_RW_DataStartCol
    )


def import_PostNatal(sheet, tags, params, projection):
    modvarTagRow = tags.get('<PostNatal MV>', None)
    if modvarTagRow is None or modvarTagRow < 0:
        return

    calc_year_idx, final_index = _get_rn_year_index_bounds(params)

    row = modvarTagRow + 2
    projection[RN_PostNatalTag] = _read_rn_year_row_contiguous(
        sheet, row, calc_year_idx, final_index, start_col=GB_RW_DataStartCol
    )


def import_Mother(sheet, tags, params, projection):
    modvarTagRow = tags.get('<Mother MV>', None)
    if modvarTagRow is None or modvarTagRow < 0:
        return

    calc_year_idx, final_index = _get_rn_year_index_bounds(params)

    row = modvarTagRow + 2
    projection[RN_MotherTag] = _read_rn_year_row_contiguous(
        sheet, row, calc_year_idx, final_index, start_col=GB_RW_DataStartCol
    )


def import_PCRForInfantAfterBirth(sheet, tags, params, projection):
    modvarTagRow = tags.get('<PCRForInfantAfterBirth MV>', None)
    if modvarTagRow is None or modvarTagRow < 0:
        return

    calc_year_idx, final_index = _get_rn_year_index_bounds(params)

    row = modvarTagRow + 2
    projection[RN_PCRForInfantAfterBirthTag] = _read_rn_year_row_contiguous(
        sheet, row, calc_year_idx, final_index, start_col=GB_RW_DataStartCol
    )


def import_InfantAfterBF(sheet, tags, params, projection):
    modvarTagRow = tags.get('<InfantAfterBF MV>', None)
    if modvarTagRow is None or modvarTagRow < 0:
        return

    calc_year_idx, final_index = _get_rn_year_index_bounds(params)

    row = modvarTagRow + 2
    projection[RN_InfantAfterBFTag] = _read_rn_year_row_contiguous(
        sheet, row, calc_year_idx, final_index, start_col=GB_RW_DataStartCol
    )


def import_Nevirapine200(sheet, tags, params, projection):
    modvarTagRow = tags.get('<Nevirapine200 MV>', None)
    if modvarTagRow is None or modvarTagRow < 0:
        return

    calc_year_idx, final_index = _get_rn_year_index_bounds(params)

    row = modvarTagRow + 2
    projection[RN_Nevirapine200Tag] = _read_rn_year_row_contiguous(
        sheet, row, calc_year_idx, final_index, start_col=GB_RW_DataStartCol
    )


def import_NevirapineInfant(sheet, tags, params, projection):
    modvarTagRow = tags.get('<NevirapineInfant MV>', None)
    if modvarTagRow is None or modvarTagRow < 0:
        return

    calc_year_idx, final_index = _get_rn_year_index_bounds(params)

    row = modvarTagRow + 2
    projection[RN_NevirapineInfantTag] = _read_rn_year_row_contiguous(
        sheet, row, calc_year_idx, final_index, start_col=GB_RW_DataStartCol
    )


def import_AZT(sheet, tags, params, projection):
    modvarTagRow = tags.get('<AZT MV>', None)
    if modvarTagRow is None or modvarTagRow < 0:
        return

    calc_year_idx, final_index = _get_rn_year_index_bounds(params)

    row = modvarTagRow + 2
    projection[RN_AZTTag] = _read_rn_year_row_contiguous(
        sheet, row, calc_year_idx, final_index, start_col=GB_RW_DataStartCol
    )


def import_ThreeTC(sheet, tags, params, projection):
    modvarTagRow = tags.get('<ThreeTC MV>', None)
    if modvarTagRow is None or modvarTagRow < 0:
        return

    calc_year_idx, final_index = _get_rn_year_index_bounds(params)

    row = modvarTagRow + 2
    projection[RN_ThreeTCTag] = _read_rn_year_row_contiguous(
        sheet, row, calc_year_idx, final_index, start_col=GB_RW_DataStartCol
    )


def import_TripleTreatment(sheet, tags, params, projection):
    modvarTagRow = tags.get('<TripleTreatment MV>', None)
    if modvarTagRow is None or modvarTagRow < 0:
        return

    calc_year_idx, final_index = _get_rn_year_index_bounds(params)

    row = modvarTagRow + 2
    projection[RN_TripleTreatmentTag] = _read_rn_year_row_contiguous(
        sheet, row, calc_year_idx, final_index, start_col=GB_RW_DataStartCol
    )


def import_TripleProphylaxis(sheet, tags, params, projection):
    modvarTagRow = tags.get('<TripleProphylaxis MV>', None)
    if modvarTagRow is None or modvarTagRow < 0:
        return

    calc_year_idx, final_index = _get_rn_year_index_bounds(params)

    row = modvarTagRow + 2
    projection[RN_TripleProphylaxisTag] = _read_rn_year_row_contiguous(
        sheet, row, calc_year_idx, final_index, start_col=GB_RW_DataStartCol
    )


def import_ServiceDelivery(sheet, tags, params, projection):
    modvarTagRow = tags.get('<ServiceDelivery MV>', None)
    if modvarTagRow is None or modvarTagRow < 0:
        return

    calc_year_idx, final_index = _get_rn_year_index_bounds(params)

    row = modvarTagRow + 2
    projection[RN_ServiceDeliveryTag] = _read_rn_year_row_contiguous(
        sheet, row, calc_year_idx, final_index, start_col=GB_RW_DataStartCol
    )


def import_Formula(sheet, tags, params, projection):
    modvarTagRow = tags.get('<Formula MV>', None)
    if modvarTagRow is None or modvarTagRow < 0:
        return

    calc_year_idx, final_index = _get_rn_year_index_bounds(params)

    row = modvarTagRow + 2
    projection[RN_FormulaTag] = _read_rn_year_row_contiguous(
        sheet, row, calc_year_idx, final_index, start_col=GB_RW_DataStartCol
    )


def import_FirstLineARTDrugs(sheet, tags, params, projection):
    modvarTagRow = tags.get('<FirstLineARTDrugs MV>', None)
    if modvarTagRow is None or modvarTagRow < 0:
        return

    calc_year_idx, final_index = _get_rn_year_index_bounds(params)

    row = modvarTagRow + 2
    projection[RN_FirstLineARTDrugsTag] = _read_rn_year_row_contiguous(
        sheet, row, calc_year_idx, final_index, start_col=GB_RW_DataStartCol
    )


def import_SecondLineARTDrugs(sheet, tags, params, projection):
    modvarTagRow = tags.get('<SecondLineARTDrugs MV>', None)
    if modvarTagRow is None or modvarTagRow < 0:
        return

    calc_year_idx, final_index = _get_rn_year_index_bounds(params)

    row = modvarTagRow + 2
    projection[RN_SecondLineARTDrugsTag] = _read_rn_year_row_contiguous(
        sheet, row, calc_year_idx, final_index, start_col=GB_RW_DataStartCol
    )


def import_AdditARTDrugCostsTBmale(sheet, tags, params, projection):
    modvarTagRow = tags.get('<AdditARTDrugCostsTBmale MV>', None)
    if modvarTagRow is None or modvarTagRow < 0:
        return

    calc_year_idx, final_index = _get_rn_year_index_bounds(params)

    row = modvarTagRow + 2
    projection[RN_AdditARTDrugCostsTBmaleTag] = _read_rn_year_row_contiguous(
        sheet, row, calc_year_idx, final_index, start_col=GB_RW_DataStartCol
    )


def import_AdditARTDrugCostsTBfemale(sheet, tags, params, projection):
    modvarTagRow = tags.get('<AdditARTDrugCostsTBfemale MV>', None)
    if modvarTagRow is None or modvarTagRow < 0:
        return

    calc_year_idx, final_index = _get_rn_year_index_bounds(params)

    row = modvarTagRow + 2
    projection[RN_AdditARTDrugCostsTBfemaleTag] = _read_rn_year_row_contiguous(
        sheet, row, calc_year_idx, final_index, start_col=GB_RW_DataStartCol
    )


def import_LabCostsARTTr(sheet, tags, params, projection):
    modvarTagRow = tags.get('<LabCostsARTTr MV>', None)
    if modvarTagRow is None or modvarTagRow < 0:
        return

    calc_year_idx, final_index = _get_rn_year_index_bounds(params)

    row = modvarTagRow + 2
    projection[RN_LabCostsARTTrTag] = _read_rn_year_row_contiguous(
        sheet, row, calc_year_idx, final_index, start_col=GB_RW_DataStartCol
    )


def import_DrugLabCostsTrInf(sheet, tags, params, projection):
    modvarTagRow = tags.get('<DrugLabCostsTrInf MV>', None)
    if modvarTagRow is None or modvarTagRow < 0:
        return

    calc_year_idx, final_index = _get_rn_year_index_bounds(params)

    row = modvarTagRow + 2
    projection[RN_DrugLabCostsTrInfTag] = _read_rn_year_row_contiguous(
        sheet, row, calc_year_idx, final_index, start_col=GB_RW_DataStartCol
    )


def import_CotrimProphylaxis(sheet, tags, params, projection):
    modvarTagRow = tags.get('<CotrimProphylaxis MV>', None)
    if modvarTagRow is None or modvarTagRow < 0:
        return

    calc_year_idx, final_index = _get_rn_year_index_bounds(params)

    row = modvarTagRow + 2
    projection[RN_CotrimProphylaxisTag] = _read_rn_year_row_contiguous(
        sheet, row, calc_year_idx, final_index, start_col=GB_RW_DataStartCol
    )


def import_TBProphylaxis(sheet, tags, params, projection):
    modvarTagRow = tags.get('<TBProphylaxis MV>', None)
    if modvarTagRow is None or modvarTagRow < 0:
        return

    calc_year_idx, final_index = _get_rn_year_index_bounds(params)

    row = modvarTagRow + 2
    projection[RN_TBProphylaxisTag] = _read_rn_year_row_contiguous(
        sheet, row, calc_year_idx, final_index, start_col=GB_RW_DataStartCol
    )


def import_NutritionSuppSixMo(sheet, tags, params, projection):
    modvarTagRow = tags.get('<NutritionSuppSixMo MV>', None)
    if modvarTagRow is None or modvarTagRow < 0:
        return

    calc_year_idx, final_index = _get_rn_year_index_bounds(params)

    row = modvarTagRow + 2
    projection[RN_NutritionSuppSixMoTag] = _read_rn_year_row_contiguous(
        sheet, row, calc_year_idx, final_index, start_col=GB_RW_DataStartCol
    )


def import_ChildrenARVDrugs(sheet, tags, params, projection):
    modvarTagRow = tags.get('<ChildrenARVDrugs MV>', None)
    if modvarTagRow is None or modvarTagRow < 0:
        return

    calc_year_idx, final_index = _get_rn_year_index_bounds(params)

    row = modvarTagRow + 2
    projection[RN_ChildrenARVDrugsTag] = _read_rn_year_row_contiguous(
        sheet, row, calc_year_idx, final_index, start_col=GB_RW_DataStartCol
    )


def import_ChildrenLabCostsARTTr(sheet, tags, params, projection):
    modvarTagRow = tags.get('<ChildrenLabCostsARTTr MV>', None)
    if modvarTagRow is None or modvarTagRow < 0:
        return

    calc_year_idx, final_index = _get_rn_year_index_bounds(params)

    row = modvarTagRow + 2
    projection[RN_ChildrenLabCostsARTTrTag] = _read_rn_year_row_contiguous(
        sheet, row, calc_year_idx, final_index, start_col=GB_RW_DataStartCol
    )


def import_CostPerInpatientDay(sheet, tags, params, projection):
    modvarTagRow = tags.get('<CostPerInpatientDay MV>', None)
    if modvarTagRow is None or modvarTagRow < 0:
        return

    calc_year_idx, final_index = _get_rn_year_index_bounds(params)

    row = modvarTagRow + 2
    projection[RN_CostPerInpatientDayTag] = _read_rn_year_row_contiguous(
        sheet, row, calc_year_idx, final_index, start_col=GB_RW_DataStartCol
    )


def import_CostPerOutpatientDay(sheet, tags, params, projection):
    modvarTagRow = tags.get('<CostPerOutpatientDay MV>', None)
    if modvarTagRow is None or modvarTagRow < 0:
        return

    calc_year_idx, final_index = _get_rn_year_index_bounds(params)

    row = modvarTagRow + 2
    projection[RN_CostPerOutpatientDayTag] = _read_rn_year_row_contiguous(
        sheet, row, calc_year_idx, final_index, start_col=GB_RW_DataStartCol
    )


def import_ARTinpatientDays(sheet, tags, params, projection):
    modvarTagRow = tags.get('<ARTinpatientDays MV>', None)
    if modvarTagRow is None or modvarTagRow < 0:
        return

    calc_year_idx, final_index = _get_rn_year_index_bounds(params)

    row = modvarTagRow + 2
    projection[RN_ARTinpatientDaysTag] = _read_rn_year_row_contiguous(
        sheet, row, calc_year_idx, final_index, start_col=GB_RW_DataStartCol
    )


def import_ARToutpatientDays(sheet, tags, params, projection):
    modvarTagRow = tags.get('<ARToutpatientDays MV>', None)
    if modvarTagRow is None or modvarTagRow < 0:
        return

    calc_year_idx, final_index = _get_rn_year_index_bounds(params)

    row = modvarTagRow + 2
    projection[RN_ARToutpatientDaysTag] = _read_rn_year_row_contiguous(
        sheet, row, calc_year_idx, final_index, start_col=GB_RW_DataStartCol
    )


def import_OItreatmentInpatientDays(sheet, tags, params, projection):
    modvarTagRow = tags.get('<OItreatmentInpatientDays MV>', None)
    if modvarTagRow is None or modvarTagRow < 0:
        return

    calc_year_idx, final_index = _get_rn_year_index_bounds(params)

    row = modvarTagRow + 2
    projection[RN_OItreatmentInpatientDaysTag] = _read_rn_year_row_contiguous(
        sheet, row, calc_year_idx, final_index, start_col=GB_RW_DataStartCol
    )


def import_OItreatmentOutpatientDays(sheet, tags, params, projection):
    modvarTagRow = tags.get('<OItreatmentOutpatientDays MV>', None)
    if modvarTagRow is None or modvarTagRow < 0:
        return

    calc_year_idx, final_index = _get_rn_year_index_bounds(params)

    row = modvarTagRow + 2
    projection[RN_OItreatmentOutpatientDaysTag] = _read_rn_year_row_contiguous(
        sheet, row, calc_year_idx, final_index, start_col=GB_RW_DataStartCol
    )


def import_MigFirstToSecondLine(sheet, tags, params, projection):
    modvarTagRow = tags.get('<MigFirstToSecondLine MV>', None)
    if modvarTagRow is None or modvarTagRow < 0:
        return

    calc_year_idx, final_index = _get_rn_year_index_bounds(params)

    # Delphi does an initial Inc(currRow) before reading this year row.
    row = modvarTagRow + 3
    projection[RN_MigFirstToSecondLineTag] = _read_rn_year_row_contiguous(
        sheet, row, calc_year_idx, final_index, start_col=GB_RW_DataStartCol
    )


def import_TestAndVisitSchedule(sheet, tags, params, projection):
    modvarTagRow = tags.get('<TestAndVisitSchedule MV>', None)
    if modvarTagRow is None or modvarTagRow < 0:
        return

    row = modvarTagRow + 3
    result = np.zeros((RN_PregnantWomen + 1, RN_EID + 1))

    for i in range(RN_PatientsInitiatingART, RN_PregnantWomen + 1):
        for j in range(RN_CD4Test, RN_EID + 1):
            is_preg_excluded = i == RN_PregnantWomen and j in (
                RN_CD4Test, RN_ViralLoadTests, RN_DrugDelivAdherenceVisits
            )
            is_eid_excluded = (
                RN_PatientsInitiatingART <= i <= RN_PatientsNotVirallySuppressed
                and j == RN_EID
            )
            if is_preg_excluded or is_eid_excluded:
                continue

            result[i][j] = _to_float(_parse_value(sheet[row, GB_RW_DataStartCol]))
            row += 1

    projection[RN_TestAndVisitScheduleTag] = result


def import_ARTUnitCosts(sheet, tags, params, projection):
    modvarTagRow = tags.get('<ARTUnitCosts MV2>', None)
    if modvarTagRow is None or modvarTagRow < 0:
        return

    calc_year_idx, final_index = _get_rn_year_index_bounds(params)

    row = modvarTagRow + 3
    result = np.zeros((RN_CostOfThirdLineARVs + 1, final_index + 1))
    for i in range(RN_CostPerCD4Test, RN_CostOfThirdLineARVs + 1):
        result[i] = _read_rn_year_row_contiguous(
            sheet, row, calc_year_idx, final_index, start_col=GB_RW_DataStartCol
        )
        row += 1

    projection[RN_ARTUnitCostsTag] = result


def import_PercentOnART(sheet, tags, params, projection):
    modvarTagRow = tags.get('<PercentOnART MV>', None)
    if modvarTagRow is None or modvarTagRow < 0:
        return

    calc_year_idx, final_index = _get_rn_year_index_bounds(params)

    row = modvarTagRow + 3
    result = np.zeros((RN_PercentPatientsThirdLine + 1, final_index + 1))
    for i in range(RN_PercentPatientsSecondLine, RN_PercentPatientsThirdLine + 1):
        result[i] = _read_rn_year_row_contiguous(
            sheet, row, calc_year_idx, final_index, start_col=GB_RW_DataStartCol
        )
        row += 1

    projection[RN_PercentOnARTTag] = result


def import_CurrencyForProgramSupportCBIdx(sheet, tags, params, projection):
    modvarTagRow = tags.get('<CurrencyForProgramSupportCBIdx MV>', None)
    if modvarTagRow is None or modvarTagRow < 0:
        return

    row = modvarTagRow + 2
    value = _parse_value(sheet[row, GB_RW_DataStartCol])
    try:
        projection[RN_CurrencyForProgramSupportCBIdxTag] = int(value)
    except (TypeError, ValueError):
        projection[RN_CurrencyForProgramSupportCBIdxTag] = 0


def import_ProgramSupport(sheet, tags, params, projection):
    modvarTagRow = tags.get('<ProgramSupport MV>', None)
    if modvarTagRow is None or modvarTagRow < 0:
        return

    calc_year_idx, final_index = _get_rn_year_index_bounds(params)

    max_ps_constants = projection.get(RN_MaxPSConstantsTag, RN_PS_MaxProgramSupport)
    try:
        max_ps_constants = int(max_ps_constants)
    except (TypeError, ValueError):
        max_ps_constants = RN_PS_MaxProgramSupport

    row = modvarTagRow + 3
    values = {}
    options = {}

    for k in range(RN_Number, RN_Percent + 1):
        for i in range(1, max_ps_constants + 1):
            support_id = _parse_value(sheet[row, GB_RW_DataStartCol])
            try:
                support_id = int(support_id)
            except (TypeError, ValueError):
                support_id = i

            option_val = _parse_value(sheet[row, GB_RW_DataStartCol + 1])
            try:
                options[support_id] = int(option_val)
            except (TypeError, ValueError):
                options[support_id] = RN_Percent

            if support_id not in values:
                values[support_id] = {}

            values[support_id][k] = _read_rn_year_row_contiguous(
                sheet, row, calc_year_idx, final_index, start_col=GB_RW_DataStartCol + 2
            )
            row += 1

    projection[RN_ProgramSupportTag] = {
        'Values': values,
        'Options': options,
    }


def import_UserProgramSupport(sheet, tags, params, projection):
    modvarTagRow = tags.get('<UserProgramSupport MV>', None)
    if modvarTagRow is None or modvarTagRow < 0:
        return

    calc_year_idx, final_index = _get_rn_year_index_bounds(params)

    count = _parse_value(sheet[modvarTagRow + 2, GB_RW_DataStartCol])
    try:
        count = int(count)
    except (TypeError, ValueError):
        count = 0

    row = modvarTagRow + 4
    result = []

    for k in range(RN_Number, RN_Percent + 1):
        for i in range(count):
            if k == RN_Number:
                support_function = sheet[row, GB_RW_DataStartCol]
                obj = {
                    'SupportFunction': support_function,
                    'Value': {},
                    'Option': RN_Percent,
                }
                result.append(obj)
            else:
                obj = result[i]

            obj['Value'][k] = _read_rn_year_row_contiguous(
                sheet, row, calc_year_idx, final_index, start_col=GB_RW_DataStartCol + 1
            )
            row += 1

    row += 1
    for i in range(count):
        option_value = RN_Percent
        for t in range(calc_year_idx, final_index + 1):
            parsed = _parse_value(sheet[row, GB_RW_DataStartCol + 1 + (t - calc_year_idx)])
            try:
                option_value = int(parsed)
            except (TypeError, ValueError):
                pass
        result[i]['Option'] = option_value
        row += 1

    projection[RN_UserProgramSupportTag] = result


def import_MitigationProgramsEntered(sheet, tags, params, projection):
    modvarTagRow = tags.get('<MitigationProgramsEntered MV>', None)
    if modvarTagRow is None or modvarTagRow < 0:
        return

    row = modvarTagRow + 2
    value = _parse_value(sheet[row, GB_RW_DataStartCol])
    if isinstance(value, str):
        projection[RN_MitigationProgramsEnteredTag] = value.strip().lower() in ('1', 'true', 'yes', 'y')
    else:
        projection[RN_MitigationProgramsEnteredTag] = bool(value)


def import_Mitigation(sheet, tags, params, projection):
    modvarTagRow = tags.get('<Mitigation MV>', None)
    if modvarTagRow is None or modvarTagRow < 0:
        return

    calc_year_idx, final_index = _get_rn_year_index_bounds(params)

    count = _parse_value(sheet[modvarTagRow + 1, GB_RW_DataStartCol])
    try:
        count = int(count)
    except (TypeError, ValueError):
        count = 0

    programs_entered = bool(projection.get(RN_MitigationProgramsEnteredTag, False))

    row = modvarTagRow + 3
    result = []
    for _ in range(count):
        obj = {
            'MitProgram': sheet[row, GB_RW_DataStartCol],
        }
        if programs_entered:
            obj['Value'] = _read_rn_year_row_contiguous(
                sheet, row, calc_year_idx, final_index, start_col=GB_RW_DataStartCol + 1
            )
        result.append(obj)
        row += 1

    projection[RN_MitigationTag] = result


def import_MethodMix(sheet, tags, params, projection):
    modvarTagRow = tags.get('<MethodMix MV5>', None)
    if modvarTagRow is None or modvarTagRow < 0:
        return

    calc_year_idx, final_index = _get_rn_year_index_bounds(params)

    row = modvarTagRow + 2
    result = np.zeros((RN_Female + 1, RN_MSMIDU + 1, RN_PrEP_PEP + 1, final_index + 1))

    for risk_group in range(RN_LRH, RN_MSMIDU + 1):
            row += 1
            for method in (RN_PrEPOralDaily, RN_PrEPInject1Mo):
                    result[RN_Male][risk_group][method] = _read_rn_year_row_contiguous(
                            sheet, row, calc_year_idx, final_index, start_col=GB_RW_DataStartCol
                    )
                    row += 1

    for risk_group in range(RN_LRH, RN_IDU + 1):
            row += 1
            for method in (RN_PrEPOralDaily, RN_PrEPInject1Mo, RN_PrEPRing):
                    result[RN_Female][risk_group][method] = _read_rn_year_row_contiguous(
                            sheet, row, calc_year_idx, final_index, start_col=GB_RW_DataStartCol
                    )
                    row += 1
                    if method == RN_PrEPInject1Mo:
                            row += 1

    projection[RN_MethodMixTag] = result


def import_CurrencyDisplayedCBIdx(sheet, tags, params, projection):
    modvarTagRow = tags.get('<CurrencyDisplayedCBIdx MV>', None)
    if modvarTagRow is None or modvarTagRow < 0:
        return

    row = modvarTagRow + 2
    value = _parse_value(sheet[row, GB_RW_DataStartCol])
    try:
        projection[RN_CurrencyDisplayedCBIdxTag] = int(value)
    except (TypeError, ValueError):
        projection[RN_CurrencyDisplayedCBIdxTag] = 0


def import_ResourcesRequired(sheet, tags, params, projection):
    modvarTagRow = tags.get('<ResourcesRequired MV>', None)
    if modvarTagRow is None or modvarTagRow < 0:
        return

    calc_year_idx, final_index = _get_rn_year_index_bounds(params)

    max_summary = projection.get(RN_MaxSummaryTableConstantsTag, RN_ST_MaxSummaryTable)
    try:
        max_summary = int(max_summary)
    except (TypeError, ValueError):
        max_summary = RN_ST_MaxSummaryTable

    row = modvarTagRow + 3
    result = {}
    for _ in range(max_summary):
        mst_id = _parse_value(sheet[row, GB_RW_DataStartCol])
        try:
            mst_id = int(mst_id)
        except (TypeError, ValueError):
            row += 1
            continue

        result[mst_id] = _read_rn_year_row_contiguous(
            sheet, row, calc_year_idx, final_index, start_col=GB_RW_DataStartCol + 1
        )
        row += 1

    projection[RN_ResourcesRequiredTag] = result


def import_NumberPeopleReached(sheet, tags, params, projection):
    modvarTagRow = tags.get('<NumberPeopleReached MV>', None)
    if modvarTagRow is None or modvarTagRow < 0:
        return

    calc_year_idx, final_index = _get_rn_year_index_bounds(params)

    max_summary = projection.get(RN_MaxSummaryTableConstantsTag, RN_ST_MaxSummaryTable)
    try:
        max_summary = int(max_summary)
    except (TypeError, ValueError):
        max_summary = RN_ST_MaxSummaryTable

    row = modvarTagRow + 3
    result = {}
    for _ in range(max_summary):
        mst_id = _parse_value(sheet[row, GB_RW_DataStartCol])
        try:
            mst_id = int(mst_id)
        except (TypeError, ValueError):
            row += 1
            continue

        result[mst_id] = _read_rn_year_row_contiguous(
            sheet, row, calc_year_idx, final_index, start_col=GB_RW_DataStartCol + 1
        )
        row += 1

    projection[RN_NumberPeopleReachedTag] = result


def import_PMTCTCosts(sheet, tags, params, projection):
    modvarTagRow = tags.get('<PMTCTCosts MV>', None)
    if modvarTagRow is None or modvarTagRow < 0:
        return

    calc_year_idx, final_index = _get_rn_year_index_bounds(params)

    row = modvarTagRow + 2
    projection[RN_PMTCTCostsTag] = _read_rn_year_row_contiguous(
        sheet, row, calc_year_idx, final_index, start_col=GB_RW_DataStartCol
    )


def import_TotalCosts(sheet, tags, params, projection):
    modvarTagRow = tags.get('<TotalCosts MV>', None)
    if modvarTagRow is None or modvarTagRow < 0:
        return

    calc_year_idx, final_index = _get_rn_year_index_bounds(params)

    row = modvarTagRow + 2
    projection[RN_TotalCostsTag] = _read_rn_year_row_contiguous(
        sheet, row, calc_year_idx, final_index, start_col=GB_RW_DataStartCol
    )


def import_OptimizerVars(sheet, tags, params, projection):
    modvarTagRow = tags.get('<OptimizerVars MV2>', None)
    if modvarTagRow is None or modvarTagRow < 0:
        return

    calc_year_idx, final_index = _get_rn_year_index_bounds(params)

    row = modvarTagRow + 2
    result = {}
    result['StartYearIndex'] = int(_to_float(_parse_value(sheet[row, GB_RW_DataStartCol])))
    row += 1
    result['TargetYearIndex'] = int(_to_float(_parse_value(sheet[row, GB_RW_DataStartCol])))
    row += 1
    result['FinalYearIndex'] = int(_to_float(_parse_value(sheet[row, GB_RW_DataStartCol])))
    row += 1
    result['GoalIndex'] = int(_to_float(_parse_value(sheet[row, GB_RW_DataStartCol])))
    row += 1
    result['DiscountRate'] = int(_to_float(_parse_value(sheet[row, GB_RW_DataStartCol])))
    row += 1

    load_default_raw = _parse_value(sheet[row, GB_RW_DataStartCol])
    if isinstance(load_default_raw, str):
        result['LoadDefaultValues'] = load_default_raw.strip().lower() in ('1', 'true', 'yes', 'y')
    else:
        result['LoadDefaultValues'] = bool(load_default_raw)
    row += 1

    coverages = {
        RN_MinCov: {},
        RN_MaxCov: {},
    }
    for iv in range(1, RN_OP_MaxOptimize + 1):
        coverages[RN_MinCov][iv] = _to_float(_parse_value(sheet[row, GB_RW_NotesCol + iv]))
    row += 1
    for iv in range(1, RN_OP_MaxOptimize + 1):
        coverages[RN_MaxCov][iv] = _to_float(_parse_value(sheet[row, GB_RW_NotesCol + iv]))
    row += 1

    funding_amnts = [0.0] * (final_index + 1)
    multiplier = 0
    for t in range(1, final_index + 1):
        if t % RN_OP_MaxOptimize == 0:
            row += 1
            multiplier += 1
        offset = t - multiplier * RN_OP_MaxOptimize
        if multiplier > 0:
            offset += 1
        funding_amnts[t] = _to_float(_parse_value(sheet[row, GB_RW_NotesCol + offset]))

    row += 1
    cea_available_raw = _parse_value(sheet[row, GB_RW_DataStartCol])
    if isinstance(cea_available_raw, str):
        cea_available = cea_available_raw.strip().lower() in ('1', 'true', 'yes', 'y')
    else:
        cea_available = bool(cea_available_raw)
    row += 1

    use_prior_raw = _parse_value(sheet[row, GB_RW_DataStartCol])
    if isinstance(use_prior_raw, str):
        use_prior_cea = use_prior_raw.strip().lower() in ('1', 'true', 'yes', 'y')
    else:
        use_prior_cea = bool(use_prior_raw)
    row += 1

    cost_infections_averted = {}
    for i in range(RN_ComMob, RN_MaxCEA + 1):
        cost_infections_averted[i] = _to_float(_parse_value(sheet[row, GB_RW_NotesCol + i]))
    row += 1

    cost_aids_deaths_averted = {}
    for i in range(RN_ComMob, RN_MaxCEA + 1):
        cost_aids_deaths_averted[i] = _to_float(_parse_value(sheet[row, GB_RW_NotesCol + i]))
    row += 1

    cost_dalys_averted = {}
    for i in range(RN_ComMob, RN_MaxCEA + 1):
        cost_dalys_averted[i] = _to_float(_parse_value(sheet[row, GB_RW_NotesCol + i]))

    result['Coverages'] = coverages
    result['FundingAmnts'] = funding_amnts
    result['CEAValuesAvailable'] = cea_available
    result['UsePriorCEAValues'] = use_prior_cea
    result['CostInfectionsAverted'] = cost_infections_averted
    result['CostAIDSDeathsAverted'] = cost_aids_deaths_averted
    result['CostDALYsAverted'] = cost_dalys_averted

    projection[RN_OptimizerVarsTag] = result
