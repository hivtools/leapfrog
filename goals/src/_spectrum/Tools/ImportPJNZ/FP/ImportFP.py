from src._spectrum.AvenirCommon.Util import gb_read_csv_sheet, GBRange, getAllTags

# from SpectrumCommon.Modvars.GB.GBDefs import createProjectionParams
from SpectrumCommon.Modvars.GB.GBDefs import createProjectionParams
from SpectrumCommon.Const.FP import *
from SpectrumCommon.Const.GB import *
from SpectrumCommon.Modvars.GB.GBUtil import *

def openFP(file, params : createProjectionParams, projection : dict):

    sheet = gb_read_csv_sheet(file)
    tags = getAllTags(sheet)

    
    read_single_int(sheet, tags, params, projection, FP_GoalTag, FP_TG_TGoal_MV) 
    read_single_int(sheet, tags, params, projection, FP_AbortionOptionTag, FP_TG_TAbortionOption_MV) 
    read_single_int(sheet, tags, params, projection, FP_AgeGroupOptionTag, FP_TG_TAgeGroupOption_MV) 
    read_single_int(sheet, tags, params, projection, FP_NeedOptionTag, FP_TG_TNeedOption_MV) 
     
    read_source_names(sheet, tags, params, projection)
    read_method_names(sheet, tags, params, projection)

    read_single_int(sheet, tags, params, projection, FP_NumSourcesTag, FP_TG_Tnum_of_sources_MV)  
    num_sources = projection[FP_NumSourcesTag]
    
    read_single_int(sheet, tags, params, projection, FP_NumNeedsTag, FP_TG_Tnum_of_needs_MV)  
    num_need = projection[FP_NumNeedsTag] 

    read_single_int(sheet, tags, params, projection, FP_NumCustomMethodsTag, FP_TG_TnumCustomMethods_MV) 
    num_cust_methods = projection[FP_NumCustomMethodsTag]
    num_methods = FP_LastDefMethod + num_cust_methods

    for cm in GBRange(1, FP_CustMethodMax):
        FP_MethodMstMap[FP_mstCustMethID+cm-1] = FP_LastDefMethod+cm

    active_methods = []
    read_active_methods(sheet, tags, params, projection, active_methods)
    read_year_age_need_methods(sheet, tags, params, projection, FP_MethodMixTag, FP_TG_TMethodMix_MV, num_need, active_methods)
    read_year_age_methods(sheet, tags, params, projection, FP_EffectivenessTag, FP_TG_Teffectiveness_MV, active_methods)

    read_method_set(sheet, tags, params, projection, FP_MethodPermTermTag, FP_TG_TmethodPermTerm_MV)
    read_method_set(sheet, tags, params, projection, FP_MethodLongTermTag, FP_TG_TmethodLongTerm_MV)
    read_method_set(sheet, tags, params, projection, FP_MethodshortTermTag, FP_TG_TmethodshortTerm_MV)
    
    read_year_methods(sheet, tags, params, projection, FP_UnitsPerCYPTag, FP_TG_TUnitsPerCYP_MV, active_methods)
    read_year_methods(sheet, tags, params, projection, FP_AverageAgeTag, FP_TG_TAverageAge_MV, active_methods)
    read_year_methods(sheet, tags, params, projection, FP_DurationOfUseTag, FP_TG_TDurationOfUse_MV, active_methods)
    read_year_methods(sheet, tags, params, projection, FP_DiscontinuationRateTag, FP_TG_TDiscontinuationRate_MV, active_methods)

    read_year_src_methods(sheet, tags, params, projection, FP_SourceMixTag, FP_TG_TSourceMix_MV, active_methods)
    read_year_src_methods(sheet, tags, params, projection, FP_CostPerUATag, FP_TG_TCostPerUA_MV, active_methods)
    read_year_src_methods(sheet, tags, params, projection, FP_FeesTag, FP_TG_TFees_MV, active_methods)
    read_year_src_methods(sheet, tags, params, projection, FP_GrossCostTag, FP_TG_TGrossCost_MV, active_methods)
    read_year_src_methods(sheet, tags, params, projection, FP_RevenueTag, FP_TG_TRevenue_MV, active_methods)
    read_year_src_methods(sheet, tags, params, projection, FP_NetCostTag, FP_TG_TNetCost_MV, active_methods)
    read_year_src_methods(sheet, tags, params, projection, FP_CommoditiesTag, FP_TG_TCommodities_MV, active_methods)

    
    
    read_single_float(sheet, tags, params, projection, FP_PregnancyRateTag, FP_TG_TPregnancyRate_MV) 
    read_single_float(sheet, tags, params, projection, FP_PercentPregWithMiscarriageTag, FP_TG_TPercentPregWithMiscarriage_MV) 
    read_single_float(sheet, tags, params, projection, FP_PropUnintendedPregEndInAbortTag, FP_TG_TPropUnintendedPregEndInAbort_MV) 
    read_single_float(sheet, tags, params, projection, FP_PropUnsafeAbortTag, FP_TG_TPropUnsafeAbort_MV) 
    read_single_float(sheet, tags, params, projection, FP_MortalityRateSafeAbortTag, FP_TG_TMortalityRateSafeAbort_MV) 
    read_single_float(sheet, tags, params, projection, FP_MortalityRateUnsafeAbortTag, FP_TG_TMortalityRateUnsafeAbort_MV) 

    read_single_float(sheet, tags, params, projection, FP_PropPregWantedLaterTag, FP_TG_TPropPregWantedLater_MV) 
    read_single_float(sheet, tags, params, projection, FP_PropPregUnwantedTag, FP_TG_TPropPregUnwanted_MV) 
    read_single_float(sheet, tags, params, projection, FP_MiscarriagePercentTag, FP_TG_TMiscarriagePercent_MV) 
    read_single_int(sheet, tags, params, projection, FP_CalcMethOptionTag, FP_TG_TCalcMethOption_MV) 

    # import_TFR(sheet, tags, params, projection)
    
    read_year_age(sheet, tags, params, projection, FP_PercentInUnionTag, FP_TG_TPercentInUnion_MV)
    read_year_age(sheet, tags, params, projection, FP_PPITag, FP_TG_TPPI_MV)
    read_year_age(sheet, tags, params, projection, FP_TARTag, FP_TG_TTAR_MV)
    read_year_age(sheet, tags, params, projection, FP_AbortionPercentTag, FP_TG_TAbortionPercent_MV)
    read_year_age(sheet, tags, params, projection, FP_SterilityTag, FP_TG_TSterility_MV)
    read_year_age(sheet, tags, params, projection, FP_PPIIndexTag, FP_TG_TPPIindex_MV)
    read_year_age(sheet, tags, params, projection, FP_AbortionIndexTag, FP_TG_TAbortionIndex_MV)

    read_year_age(sheet, tags, params, projection, FP_SterilityIndexTag, FP_TG_TSterilityIndex_MV)
    read_year_age(sheet, tags, params, projection, FP_PrevalenceIndexTag, FP_TG_TPrevalenceIndex_MV)
    read_year_age(sheet, tags, params, projection, FP_TFRTag, FP_TG_TTFR_MV)
    read_year_age(sheet, tags, params, projection, FP_WRATag, FP_TG_TWRA_MV)
    read_year_age(sheet, tags, params, projection, FP_MWRATag, FP_TG_TMWRA_MV)
    read_year_age(sheet, tags, params, projection, FP_MortalityRateTag, FP_TG_TMortalityRate_MV)
    
    read_year_age(sheet, tags, params, projection, FP_BirthsTag, FP_TG_TBirths_MV)
    read_year_age(sheet, tags, params, projection, FP_BirthsAvertedTag, FP_TG_TBirthsAverted_MV)
    read_year_age(sheet, tags, params, projection, FP_AbortionsTag, FP_TG_Tabortions_MV)

    read_year_age_need(sheet, tags, params, projection, FP_AverageEffectivenessTag, FP_TG_TAverageEffectiveness_MV, num_need)
    read_year_age_need(sheet, tags, params, projection, FP_PrevalenceTag, FP_TG_Tprevalence_MV, num_need)
    read_year_age_need(sheet, tags, params, projection, FP_MPrevalenceTag, FP_TG_TmPrevalence_MV, num_need)
    read_year_age_need(sheet, tags, params, projection, FP_AddMdrnUsersPrevTag, FP_TG_TaddMdrnUsersPrev_MV, num_need)
    read_year_age_need(sheet, tags, params, projection, FP_UnmetNeedTag, FP_TG_TUnmetNeed_MV, num_need)
    
    read_year_need(sheet, tags, params, projection, FP_UnmetNeedReductionTag, FP_TG_TUnmetNeedReduction_MV, num_need)


    read_age(sheet, tags, params, projection, FP_WantedTFRTag, FP_TG_TWantedTFR_MV)
    read_year(sheet, tags, params, projection, FP_TFRdifferenceTag, FP_TG_TTFRdifference_MV)
    read_year(sheet, tags, params, projection, FP_PregAvertedTag, FP_TG_TPreg_averted_MV)
    read_year(sheet, tags, params, projection, FP_MaternalDeathsAvertedTag, FP_TG_TMaternal_deaths_averted_MV)
    read_year(sheet, tags, params, projection, FP_UnsafeAbortionsAvertedTag, FP_TG_TUnsafe_abortions_averted_MV)

    read_unmet_need_prev(sheet, tags, params, projection)
    read_cost_regression(sheet, tags, params, projection)
    read_single_int(sheet, tags, params, projection, FP_ASFRInput_TFRGoalTag, FP_TG_TASFRInput_TFRGoal_MV)
    read_single_float(sheet, tags, params, projection, FP_LegalAbortNeedTreatTag, FP_TG_TLegalAbortNeedTreat_MV)
    read_lam_insusceptible(sheet, tags, params, projection)
    read_single_float(sheet, tags, params, projection, FP_EPSurveyYearTFRTag, FP_TG_TEPSurveyYearTFR_MV)

    read_age(sheet, tags, params, projection, FP_TFTag, FP_TG_TTF_MV, row_offset=5, col=3)
    read_age(sheet, tags, params, projection, FP_PRTag, FP_TG_TPR_MV, row_offset=5, col=3)

    read_child_survival_inputs(sheet, tags, params, projection)
    read_child_survival_outputs(sheet, tags, params, projection)

    read_pac_inputs(sheet, tags, params, projection)
    read_pac_outputs(sheet, tags, params, projection)

    read_year_age_pregnancies(sheet, tags, params, projection, FP_PregnanciesTag, FP_TG_Tpregnancies_MV)

    read_year_age_source_methods(sheet, tags, params, projection, FP_UsersTag, FP_TG_TUsers_MV, num_sources, active_methods)
    read_year_age_source_methods(sheet, tags, params, projection, FP_AcceptorsTag, FP_TG_TAcceptors_MV, num_sources, active_methods)
    read_year_age_source_methods(sheet, tags, params, projection, FP_GrowthRateTag, FP_TG_TGrowthRate_MV, num_sources, active_methods)
    
    read_FPGL_source_text(sheet, tags, params, projection)
 

    # read_year(sheet, params, projection, FP_AvgHouseholdTag, FP_TG_TavgHousehold_MV)
    read_relative_risks(sheet, tags, params, projection)
    pass
    # modvarTagRow = tags.get(tag, None)
    # tfr_mv = projection[FP_TFRTag]
    
    pass


def read_single_int(sheet, tags, params, projection, mv_tag, desktop_tag, row_offset=2, col=GB_RW_DataStartCol):
    modvarTagRow = tags.get(desktop_tag, None)
    if modvarTagRow is not None:
        row = row_offset+modvarTagRow
        projection[mv_tag] = int(sheet.values[row, col])
        pass   

def read_single_float(sheet, tags, params, projection, mv_tag, desktop_tag,  row_offset=2, col=GB_RW_DataStartCol):
    modvarTagRow = tags.get(desktop_tag, None)
    if modvarTagRow is not None:
        row = row_offset+modvarTagRow
        projection[mv_tag] = float(sheet.values[row, col])
        pass   

def read_year_age(sheet, tags, params, projection, mv_tag, desktop_tag):
    modvarTagRow = tags.get(desktop_tag, None)
    if modvarTagRow is not None:
        mv = projection[mv_tag]

        row = modvarTagRow + 4
        # values = modvar
        mv = mv*0
        for age in range(0, 8):
            row += 2
            values = mv[age]
            getRowOfYearVals(sheet, values, params, row)   
            pass
        
        projection[mv_tag] = mv
        pass

def read_year_age_need(sheet, tags, params, projection, mv_tag, desktop_tag, num_need):
    modvarTagRow = tags.get(desktop_tag, None)
    if modvarTagRow is not None:
        mv = projection[mv_tag]

        row = modvarTagRow + 6
        # values = modvar
        mv = mv*0
        for age in range(0, 8):
            for need in range(0, num_need+1):
                row += 2
                values = mv[age][need]
                getRowOfYearVals(sheet, values, params, row)   
                pass
        
        projection[mv_tag] = mv
        pass

def read_year_need(sheet, tags, params, projection, mv_tag, desktop_tag, num_need):
    modvarTagRow = tags.get(desktop_tag, None)
    if modvarTagRow is not None:
        mv = projection[mv_tag]

        row = modvarTagRow + 4
        # values = modvar
        mv = mv*0
        for need in range(0, num_need+1):
            row += 2
            values = mv[need]
            getRowOfYearVals(sheet, values, params, row)   
            pass
        
        projection[mv_tag] = mv
        pass

def read_year_age_need_methods(sheet, tags, params, projection, mv_tag, desktop_tag, num_need, active_methods):
    modvarTagRow = tags.get(desktop_tag, None)
    if modvarTagRow is not None:
        mv = projection[mv_tag]

        row = modvarTagRow + 9
        # values = modvar
        mv = mv*0
        for age in range(0, 8):
            for need in range(0, num_need+1):
                for method in active_methods:
                    row += 2
                    values = mv[age][method][need]
                    getRowOfYearVals(sheet, values, params, row)   
                    pass
        
        projection[mv_tag] = mv
        pass

def read_year_age_source_methods(sheet, tags, params, projection, mv_tag, desktop_tag, num_sources, active_methods):
    modvarTagRow = tags.get(desktop_tag, None)
    if modvarTagRow is not None:
        mv = projection[mv_tag]

        row = modvarTagRow + 8
        # values = modvar
        mv = mv*0
        for age in range(0, 8):
            for src in range(0, num_sources+1):
                for method in active_methods:
                    row += 2
                    values = mv[method][age][src]
                    getRowOfYearVals(sheet, values, params, row)   
                    pass
        
        projection[mv_tag] = mv
        pass

def read_year_age_methods(sheet, tags, params, projection, mv_tag, desktop_tag, active_methods):
    modvarTagRow = tags.get(desktop_tag, None)
    if modvarTagRow is not None:
        mv = projection[mv_tag]

        row = modvarTagRow + 6
        # values = modvar
        mv = mv*0
        for age in range(0, 8):
            for method in active_methods:
                row += 2
                values = mv[age][method]
                getRowOfYearVals(sheet, values, params, row)   
                pass
        
        projection[mv_tag] = mv
        pass


def read_method_set(sheet, tags, params, projection, mv_tag, desktop_tag):
    modvarTagRow = tags.get(desktop_tag, None)

    if modvarTagRow is not None:
        row = modvarTagRow + 5
        mv = []
        col = GB_RW_DataStartCol
        for offset in range(1, FP_Max_Methods+1):
            method = int(sheet.values[row, col+offset])
            if method!=0:
                mv.append(method)

            pass
        
        projection[mv_tag] = mv
        pass


def read_year_src_methods(sheet, tags, params, projection, mv_tag, desktop_tag, active_methods):
    modvarTagRow = tags.get(desktop_tag, None)
    if modvarTagRow is not None:
        mv = projection[mv_tag]

        row = modvarTagRow + 6
        # values = modvar
        # mv = mv*0 //Jared 1.26.24, this was causing problems when calculating (CheckInputmodvars in FPProj, Check Source Mix)
        for src in range(0, 9):
            for method in active_methods:
                row += 2
                values = mv[method][src]
                getRowOfYearVals(sheet, values, params, row)   
                pass
        
        projection[mv_tag] = mv
        pass

def read_year_methods(sheet, tags, params, projection, mv_tag, desktop_tag, active_methods):
    modvarTagRow = tags.get(desktop_tag, None)
    if modvarTagRow is not None:
        mv = projection[mv_tag]

        row = modvarTagRow + 4
        # values = modvar
        mv = mv*0
        for method in active_methods:
            row += 2
            values = mv[method]
            getRowOfYearVals(sheet, values, params, row)   
            pass
        
        projection[mv_tag] = mv
        pass

def read_year(sheet, tags, params, projection, mv_tag, desktop_tag):
    modvarTagRow = tags.get(desktop_tag, None)
    if modvarTagRow is not None:
        mv = projection[mv_tag]

        row = modvarTagRow + 3
        # values = modvar
        mv = mv*0
        values = mv
        getRowOfYearVals(sheet, values, params, row)   

        projection[mv_tag] = mv
        pass

def read_age(sheet, tags, params, projection, mv_tag, desktop_tag, row_offset=3, col=2):
    modvarTagRow = tags.get(desktop_tag, None)
    if modvarTagRow is not None:
        mv = projection[mv_tag]

        row = modvarTagRow + row_offset
        # values = modvar
        for age in range(0, 8):
            mv[age] = float(sheet.values[row, col])
            col += 1

        projection[mv_tag] = mv
        pass
                

def read_year_age_pregnancies(sheet, tags, params, projection, mv_tag, desktop_tag):
    modvarTagRow = tags.get(desktop_tag, None)
    if modvarTagRow is not None:
        mv = projection[mv_tag]

        row = modvarTagRow + 6
        # values = modvar
        mv = mv*0
        for age in range(0, 8):
            for ms in range(FP_all_PREG, FP_mistimed+1):
                row += 2
                values = mv[age][ms]
                getRowOfYearVals(sheet, values, params, row)   
                pass
        
        projection[mv_tag] = mv
        pass                                      
###############################################################################
###############################################################################
###############################################################################
def read_active_methods(sheet, tags, params, projection, active_methods):
    modvarTagRow = tags.get(FP_TG_TActiveMethods_MV, None)
    if modvarTagRow is not None:
        modvar = projection[FP_ActiveMethodsTag]

        row = modvarTagRow + 3
        col = GB_RW_DataStartCol
        for m in range (1, FP_Max_Methods+1):
            active = sheet.values[row, col]=='1'
            real_m = FP_MethodMstMap[m]            
            modvar[real_m] = active 
            if active:
                active_methods.append(real_m)


            col += 1
        pass

def read_source_names(sheet, tags, params, projection):
    modvarTagRow = tags.get(FP_TG_TSources_MV, None)
    if modvarTagRow is not None:
        src_mv = ['All']

        row = modvarTagRow + 3
        
        col = GB_RW_DataStartCol
        num_sources = int(sheet.values[row, col])
        for m in range (1, num_sources+1):
            col += 1
            src_mv.append(sheet.values[row, col])
        projection[FP_SourcesTag] = src_mv
        pass

def read_method_names(sheet, tags, params, projection):
    modvarTagRow = tags.get(FP_TG_TMethodName_MV, None)
    if modvarTagRow is not None:
        meth_names_mv = ['']

        
        col = GB_RW_DataStartCol
        num_methods = int(sheet.values[modvarTagRow+5, col])
        num_methods += int(sheet.values[modvarTagRow+7, col]) 
        for m in range (1, num_methods+1):
            col += 1
            meth_names_mv.append(sheet.values[modvarTagRow+8, col])
        projection[FP_MethodNameTag] = meth_names_mv
        pass

def read_lam_insusceptible(sheet, tags, params, projection):
    modvarTagRow = tags.get(FP_TG_TLAMinsusceptible_MV, None)
    if modvarTagRow is not None:
        row = modvarTagRow+3
        col = GB_RW_DataStartCol

        projection[FP_LAMinsusceptibleTag][FP_LAM0_1] = float(sheet.values[row, col])
        projection[FP_LAMinsusceptibleTag][FP_LAM2_3] = float(sheet.values[row, col+1])
        projection[FP_LAMinsusceptibleTag][FP_LAM4_5] = float(sheet.values[row, col+2])

def read_FPGL_source_text(sheet, tags, params, projection):
    src = ''

    modvarTagRow = tags.get(FP_TG_TEdFPSource_MV, None)
    if modvarTagRow is not None:
        row = modvarTagRow+2
        col = GB_RW_DataStartCol
        num_notes = int(sheet.values[row, col])
        for i in range(1, num_notes+1):
            src += sheet.values[row, col+i]
        
        projection[FP_SourceTag]['main'] = src
        
        src = ''

    modvarTagRow = tags.get(FP_TG_TEdGLSource_MV, None)
    if modvarTagRow is not None:
        row = modvarTagRow+2
        num_notes = int(sheet.values[row, col])
        for i in range(1, num_notes+1):
            src += sheet.values[row, col+i]

        projection[FP_SourceTag]['goal'] = src

def read_unmet_need_prev(sheet, tags, params, projection):
    modvarTagRow = tags.get(FP_TG_TestUnmetNeedFromPrev_MV, None)
    if modvarTagRow is not None:
        row = modvarTagRow+3
        col = GB_RW_DataStartCol

        projection[FP_TestUnmetNeedFromPrevTag] = sheet.values[row, col]=="1"

def read_cost_regression(sheet, tags, params, projection):
    modvarTagRow = tags.get(FP_TG_TCalcCostRegression_MV, None)
    if modvarTagRow is not None:
        row = modvarTagRow+2
        col = GB_RW_DataStartCol

        projection[FP_CalcCostRegressionTag] = sheet.values[row, col]=="1"
    
def read_child_survival_inputs(sheet, tags, params, projection):
    modvarTagRow = tags.get(FP_TG_TChildSurvInputs_MV, None)
    if modvarTagRow is not None:
        row = modvarTagRow+3
        col = GB_RW_DataStartCol

        projection[FP_ChildSurvInputsTag][FP_PerBirthRisk] = float(sheet.values[row, col])
        projection[FP_ChildSurvInputsTag][FP_FertAdjIMR] = float(sheet.values[row, col+1])
        projection[FP_ChildSurvInputsTag][FP_FertAdjU5MR] = float(sheet.values[row, col+2])

def read_child_survival_outputs(sheet, tags, params, projection):
    modvarTagRow = tags.get(FP_TG_TChildSurvOutputs_MV, None)
    if modvarTagRow is not None:
        row = modvarTagRow+3
        mv = projection[FP_ChildSurvOutputsTag]

        row = modvarTagRow + 4
        # values = modvar
        mv = mv*0
        for i in range(FP_PerBirthRisk, FP_FertAdjU5MR+1):
            row += 2
            values = mv[i]
            getRowOfYearVals(sheet, values, params, row)   
            pass
        
        projection[FP_ChildSurvOutputsTag] = mv

def read_pac_inputs(sheet, tags, params, projection):
    modvarTagRow = tags.get(FP_TG_TPACInputs_MV, None)
    if modvarTagRow is not None:
        row = modvarTagRow+3
        mv = projection[FP_PACInputsTag]

        row = modvarTagRow + 4
        # values = modvar
        mv = mv*0
        for i in range(FP_PerAbortLegal, FP_CostCounServCase+1):
            row += 2
            values = mv[i]
            getRowOfYearVals(sheet, values, params, row)   
            pass
        
        projection[FP_PACInputsTag] = mv


def read_pac_outputs(sheet, tags, params, projection):
    modvarTagRow = tags.get(FP_TG_TPACOutputs_MV, None)
    if modvarTagRow is not None:
        row = modvarTagRow+3
        mv = projection[FP_PACOutputsTag]

        row = modvarTagRow + 4
        # values = modvar
        mv = mv*0
        for i in range(FP_WantedPreg, FP_CostPerMaternDeathAvert+1):
            row += 2
            values = mv[i]
            getRowOfYearVals(sheet, values, params, row)   
            pass
        
        projection[FP_PACOutputsTag] = mv
    
def read_relative_risks(sheet, tags, params, projection):
    modvarTagRow = tags.get(FP_TG_TrelativeRisks_MV, None)
    if modvarTagRow is not None:
        row = modvarTagRow+2
        mv = projection[FP_RelativeRisksTag]
        bo_result = projection[FP_RRAgeBirthOrderResultTag]
        bi_result = projection[FP_RRBirthIntervalResultTag]
        

        maxBirthOrder = int(sheet.values[row, GB_RW_DataStartCol])
        row += 1
        
        maxAgeOrder = int(sheet.values[row, GB_RW_DataStartCol])
        row += 1
        
        for i in GBRange(1, maxBirthOrder):
            row += 1
            for ma in GBRange(1, maxAgeOrder):
                if not sheet.values[row, GB_RW_DataStartCol + ma] == '':        
                    mv['ageBirthOrder'][i][ma] = float(sheet.values[row, GB_RW_DataStartCol + ma])
            row += 1
        row += 1

        maxBirthInterval = int(sheet.values[row, GB_RW_DataStartCol])
        row += 1
        for i in GBRange(1, maxBirthInterval):
            if not sheet.values[row, GB_RW_DataStartCol] == '':        
                mv['birthInterval'][i] = float(sheet.values[row, GB_RW_DataStartCol])
            row += 1
        row += 1

        c1 = GB_RW_DataStartCol
        t1 = 0
        t2 = getYearIdx(params.finalYear, params.firstYear)    
        
        maxBirthOrder = int(sheet.values[row, GB_RW_DataStartCol])
        row += 1
        maxAgeOrder = int(sheet.values[row, GB_RW_DataStartCol])
        row += 1
        for i in GBRange(1, maxBirthOrder):    
            row += 1
            for ma in GBRange(1, maxAgeOrder):   
                c = c1
                for t in GBRange(t1, t2):  
                    if not sheet.values[row, c] == '':
                        bo_result[i][ma][t] = float(sheet.values[row, c])
                    c += 1
                row += 1
        row += 1

        maxBirthInterval = int(sheet.values[row, GB_RW_DataStartCol])
        row += 1
        for i in GBRange(1, maxBirthInterval):
            c = c1
            for t in GBRange(t1, t2):  
                if not sheet.values[row, c] == '':        
                    bi_result[i][t] = float(sheet.values[row, c])
                c += 1
            row += 1
        row += 2

        maxOrder = int(sheet.values[row, GB_RW_DataStartCol])
        row += 1
        
        maxMAge = int(sheet.values[row, GB_RW_DataStartCol])
        row += 1
        
        maxC2 = int(sheet.values[row, GB_RW_DataStartCol])
        row += 1
        
        maxExtra = int(sheet.values[row, GB_RW_DataStartCol])
        row += 1
        
        maxExtraBirthInterval = int(sheet.values[row, GB_RW_DataStartCol])
        row += 1
        
        for i in GBRange(1, maxOrder):    
            row += 1
            for ma in GBRange(1, maxMAge): 
                for c in GBRange(1, maxC2): 
                    if not sheet.values[row, GB_RW_DataStartCol + c] == '':        
                        mv['ageBirthAdv'][c][i][ma] = float(sheet.values[row, GB_RW_DataStartCol + c])
                row += 1
            row += 1    
        
        row += 3
        for i in GBRange(1, maxExtra):    
            for c in GBRange(1, maxC2):    
                if not sheet.values[row, GB_RW_DataStartCol + c] == '':        
                    mv['birthOrderAdv'][c][i] = float(sheet.values[row, GB_RW_DataStartCol + c])
            row += 1
        
        row += 2
        for i in GBRange(1, maxExtraBirthInterval):    
            for c in GBRange(1, maxC2):    
                if not sheet.values[row, GB_RW_DataStartCol + c] == '':        
                    mv['birthIntAdv'][c][i] = float(sheet.values[row, GB_RW_DataStartCol + c])
            row += 1

    # temp = sheet.values[row, GB_RW_DataStartCol]
    # temp = GBReplaceCharacter(temp,#29,#$D);
    # temp = GBReplaceCharacter(temp,#26,#$A);
    # value.yearSrc = temp
    # row += 1
    # value.year =  int(sheet.values[row, GB_RW_DataStartCol])

###############################################################################
###############################################################################
###############################################################################
###############################################################################

#Old Delphi Tags
## Not Needed for online version
# FP_TG_TFirstYear_MV                         = 'FirstYear MV'#Done
# FP_TG_TFinalYear_MV                         = 'FinalYear MV'#Done
# FP_TG_TFirstIndex_MV                        = 'FirstIndex MV'#Done
# FP_TG_TFinalIndex_MV                        = 'FinalIndex MV'#Done
# FP_TG_TDataChanged_MV                       = 'DataChanged MV'#Done
# FP_TG_TProjectionValid_MV                   = 'ProjectionValid MV'#Done
# FP_TG_TprojectionValidDate_MV               = 'projectionValidDate MV'#Done
# FP_TG_TFileName_MV                          = 'FileName MV'#Done
# FP_TG_TedFmHighlight_MV                     = 'edFmHighlight MV'#Done

FP_TG_TAgeGroupOption_MV                    = 'AgeGroupOption MV' #Done

FP_TG_TGoal_MV                              = 'Goal MV' #Done
FP_TG_TAbortionOption_MV                    = 'AbortionOption MV' #Done
FP_TG_TNeedOption_MV                        = 'NeedOption MV' #Done 
FP_TG_TActiveMethods_MV                     = 'ActiveMethods MV' #Done
FP_TG_TSources_MV                           = 'Sources MV'#Done
FP_TG_TMethodName_MV                        = 'MethodName MV'#Done 
FP_TG_Tnum_of_sources_MV                    = 'num_of_sources MV' #Done
FP_TG_Tnum_of_needs_MV                      = 'num_of_needs MV' #Done
FP_TG_TnumCustomMethods_MV                  = 'numCustomMethods MV' #Done
FP_TG_TPregnancyRate_MV                     = 'PregnancyRate MV'#Done

FP_TG_TPercentPregWithMiscarriage_MV        = 'PercentPregWithMiscarriage MV'#Done
FP_TG_TPropUnintendedPregEndInAbort_MV      = 'PropUnintendedPregEndInAbort MV'#Done
FP_TG_TPropUnsafeAbort_MV                   = 'PropUnsafeAbort MV'#Done
FP_TG_TMortalityRateSafeAbort_MV            = 'MortalityRateSafeAbort MV'#Done
# FP_TG_TMortalityRateUnsafeAbortMMR_MV       = 'MortalityRateUnsafeAbortMMR MV' # no longer used
FP_TG_TMortalityRateUnsafeAbort_MV          = 'MortalityRateUnsafeAbort MV'#Done
FP_TG_TPropPregWantedLater_MV               = 'PropPregWantedLater MV'#Done
FP_TG_TPropPregUnwanted_MV                  = 'PropPregUnwanted MV'#Done
FP_TG_TMiscarriagePercent_MV                = 'Miscarriage Percent MV'#Done
FP_TG_TCalcMethOption_MV                    = 'CalcMethOption MV' #Done
FP_TG_TMethodMix_MV                         = 'MethodMix MV'#Done
FP_TG_TmethodPermTerm_MV                    = 'methodPermTerm MV'#Done
FP_TG_TmethodLongTerm_MV                    = 'methodLongTerm MV'#Done
FP_TG_TmethodshortTerm_MV                   = 'methodshortTerm MV'#Done
FP_TG_Teffectiveness_MV                     = 'effectiveness MV' #Done
FP_TG_TUnitsPerCYP_MV                       = 'UnitsPerCYP MV'#Done
FP_TG_TAverageAge_MV                        = 'AverageAge MV'#Done
FP_TG_TDurationOfUse_MV                     = 'DurationOfUse MV'#Done
FP_TG_TSourceMix_MV                         = 'SourceMix MV'#Done
FP_TG_TCostPerUA_MV                         = 'CostPerUA MV'#Done
FP_TG_TFees_MV                              = 'Fees MV'#Done
FP_TG_TGrossCost_MV                         = 'GrossCost MV'#Done
FP_TG_TRevenue_MV                           = 'Revenue MV'#Done
FP_TG_TNetCost_MV                           = 'NetCost MV'#Done
FP_TG_TCommodities_MV                       = 'Commodities MV'#Done
FP_TG_TPercentInUnion_MV                    = 'PercentInUnion MV' #Done
FP_TG_TPPI_MV                               = 'PPI MV' #Done
FP_TG_TTAR_MV                               = 'TAR MV' #Done
FP_TG_TAbortionPercent_MV                   = 'AbortionPercent MV' #Done
FP_TG_TSterility_MV                         = 'Sterility MV' #Done
FP_TG_TMarriageIndex_MV                     = 'MarriageIndex MV' #Done
FP_TG_TPPIindex_MV                          = 'PPIindex MV' #Done
FP_TG_TAbortionIndex_MV                     = 'AbortionIndex MV' #Done

FP_TG_TSterilityIndex_MV                    = 'SterilityIndex MV' #Done
FP_TG_TPrevalenceIndex_MV                   = 'PrevalenceIndex MV' #Done
FP_TG_TTFR_MV                               = 'TFR MV' #Done
FP_TG_TWRA_MV                               = 'WRA MV' #Done
FP_TG_TMWRA_MV                              = 'MWRA MV' #Done
FP_TG_TMortalityRate_MV                     = 'MortalityRate MV' #Done
FP_TG_TBirths_MV                            = 'Births MV' #Done
FP_TG_TBirthsAverted_MV                     = 'BirthsAverted MV' #Done
FP_TG_Tabortions_MV                         = 'abortions MV' #Done
FP_TG_TAverageEffectiveness_MV              = 'AverageEffectiveness MV'#Done

FP_TG_Tprevalence_MV                        = 'prevalence MV'#Done
FP_TG_TmPrevalence_MV                       = 'mPrevalence MV'#Done
FP_TG_TaddMdrnUsersPrev_MV                  = 'addMdrnUsersPrev MV'#Done
FP_TG_TUnmetNeed_MV                         = 'UnmetNeed MV'#Done
FP_TG_TUnmetNeedReduction_MV                = 'UnmetNeedReduction MV'#Done
FP_TG_TWantedTFR_MV                         = 'WantedTFR MV'#Done
FP_TG_TTFRdifference_MV                     = 'TFRdifference MV'#Done
FP_TG_TestUnmetNeedFromPrev_MV              = 'estUnmetNeedFromPrev MV' #Done
FP_TG_TCalcCostRegression_MV                = 'CalcCostRegression MV'#Done
FP_TG_TASFRInput_TFRGoal_MV                 = 'ASFRInput_TFRGoal MV'#Done

FP_TG_TChildSurvInputs_MV                   = 'ChildSurvInputs MV'#Done
FP_TG_TPACInputs_MV                         = 'PACInputs MV'#Done
FP_TG_TLegalAbortNeedTreat_MV               = 'LegalAbortNeedTreat MV'#Done
FP_TG_TPACOutputs_MV                        = 'PACOutputs MV'#Done
FP_TG_TLAMinsusceptible_MV                  = 'LAMinsusceptible MV'#Done
# FP_TG_TEPCalibration_MV                     = 'EPCalibration MV' #Done
# FP_TG_TEPSurveyYear_MV                      = 'EPSurveyYear MV' #Done
FP_TG_TEPSurveyYearTFR_MV                   = 'EPSurveyYearTFR MV'#Done
FP_TG_TTF_MV                                = 'TF MV'#Done
FP_TG_TPR_MV                                = 'PR MV'#Done
FP_TG_TDiscontinuationRate_MV               = 'DiscontinuationRate MV'#Done

FP_TG_TUsers_MV                             = 'Users MV'#Done
FP_TG_TAcceptors_MV                         = 'Acceptors MV'#Done
FP_TG_TGrowthRate_MV                        = 'GrowthRate MV'#Done
FP_TG_Tpregnancies_MV                       = 'pregnancies MV'#Done
FP_TG_TChildSurvOutputs_MV                  = 'ChildSurvOutputs MV'#Done
FP_TG_TPreg_averted_MV                      = 'Preg_averted MV'#Done
FP_TG_TMaternal_deaths_averted_MV           = 'Maternal_deaths_averted MV'#Done
FP_TG_TUnsafe_abortions_averted_MV          = 'Unsafe_abortions_averted MV'#Done
FP_TG_TrelativeRisks_MV                     = 'relativeRisks MV'#Done
FP_TG_TEdFPSource_MV                        = 'EdFPSource MV'#Done
FP_TG_TEdGLSource_MV                        = 'EdGLSource MV'#Done

FP_TG_TavgHousehold_MV                      = 'avgHousehold MV'#Done

#Method Master IDs
FP_mstall_methods    = 0
FP_mstcondom         = 1
FP_mstfster          = 2
FP_mstinjectable     = 3
FP_mstIUD            = 4
FP_mstmster          = 5
FP_mstImplant        = 6
FP_mstpill           = 7
FP_mstrhythm         = 8
FP_msttraditional    = 9
FP_mstvag_barrier    = 10
FP_mstVFT            = 11
FP_mstwithdrawal     = 12
FP_mstother          = 13
FP_mstLAM            = 14
FP_mstSDM            = 15
FP_mstcondomFM       = 16
FP_mstcondomML       = 17
FP_mstinj3month      = 18
FP_mstinj2month      = 19
FP_mstinj1month      = 20
FP_mstinj6month      = 21
FP_mstUninject       = 22
FP_mstImplanon       = 23
FP_mstJadelle        = 24
FP_mstSino_Implant   = 25
FP_mstStandardPill   = 26
FP_mstProgestin      = 27
FP_mstPeri_coital    = 28
FP_mstIUDCopper      = 29
FP_mstIUDLngIus      = 30
FP_mstCustMethID     = 31
#next master id is 43, since there are 12 custom methods*)
FP_mstFertilAware    = 43
FP_Mst_Max_Methods   = 43



FP_MethodMstMap = {
    FP_mstall_methods    : FP_all_methods,
    FP_mstcondom         : FP_CondomML,
    FP_mstfster          : FP_fster,
    FP_mstinjectable     : FP_inj3month,
    FP_mstIUD            : FP_IUDCopper,
    FP_mstmster          : FP_mster,
    FP_mstImplant        : FP_Jadelle,
    FP_mstpill           : FP_StandardPill,
    FP_mstrhythm         : FP_PerAbst,
    FP_msttraditional    : FP_Traditional,
    FP_mstvag_barrier    : FP_vag_barrier,
    FP_mstVFT            : FP_VFT,
    FP_mstwithdrawal     : FP_withdrawal,
    FP_mstother          : FP_other,
    FP_mstLAM            : FP_LAM,
    FP_mstSDM            : FP_SDM,
    FP_mstcondomFM       : FP_CondomFM,
    FP_mstcondomML       : FP_CondomML,
    FP_mstinj3month      : FP_inj3month,
    FP_mstinj2month      : FP_inj2month,
    FP_mstinj1month      : FP_inj1month,
    FP_mstinj6month      : FP_inj6month,
    FP_mstUninject       : FP_Uninject,
    FP_mstImplanon       : FP_Implanon,
    FP_mstJadelle        : FP_Jadelle,
    FP_mstSino_Implant   : FP_Sino_Implant,

    FP_mstStandardPill   : FP_StandardPill,
    FP_mstProgestin      : FP_Progestin,
    FP_mstPeri_coital    : FP_Peri_coital,
    FP_mstIUDCopper      : FP_IUDCopper,
    FP_mstIUDLngIus      : FP_IUDLngIus,
    # FP_mstCustMethID     : ,
    #next master id is 43, since there are 12 custom methods*)
    FP_mstFertilAware: 0#,FP_FertilAware it was 0 in delphi
}