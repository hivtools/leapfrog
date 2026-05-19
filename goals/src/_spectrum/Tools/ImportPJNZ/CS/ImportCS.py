
import numpy as np
from src._spectrum.AvenirCommon.Util import gb_read_csv_sheet, GBRange, getAllTags, findTagRow

from SpectrumCommon.Modvars.GB.GBDefs import createProjectionParams

from SpectrumCommon.Const.GB import *
from SpectrumCommon.Modvars.GB.GBUtil import *
from SpectrumCommon.Const.DP import *
from SpectrumCommon.Const.CS import *
from SpectrumCommon.Const.PJ import *

from SpectrumCommon.Util.CS.CSUtil import *
from SpectrumCommon.Util.CS.CSDataUtil import *

def openCS(file, params : createProjectionParams, projection : dict):
    sheet = gb_read_csv_sheet(file)
    tags = getAllTags(sheet)
     
    for key, record in projection[CS_IVInfoTag].items():
        if key not in [CS_IV_ContraceptiveUse_MST_ID, 
                       CS_IV_ART_MST_ID, 
                       str(CS_MstBFPromotion)]:
            if "Coverage_ED" in record:
                if record["Coverage_ED"]:            
                    projection[CS_SelectedIVSetTag].append(int(key))
    
    for mstID in GBRange(CS_FirstFPMstID, CS_LastFPMstID):
        projection[CS_SelectedIVSetTag].append(mstID)
    
    projection[CS_SelectedIVSetTag].append(CS_FirstAMMstID)  
    projection[CS_SelectedIVSetTag].append(CS_MstPercOnART) 
    
    VariablesRW = import_VariablesRW(sheet, tags, params, projection)

    projection[CS_CovEntryModeTag] = CS_DirectEntryMode

    # Controls
    import_MenARecommended(sheet, tags, params, projection)
    import_IPTpCBChecked(sheet, tags, params, projection)
    import_FirstYearAtWork(sheet, tags, params, projection)
    import_LastYearAtWork(sheet, tags, params, projection)
    import_AbortCalcFamPlan(sheet, tags, params, projection)
    import_CalcCovFromInputs(sheet, tags, params, projection)
    import_EnterBFImproveData(sheet, tags, params, projection)
    import_BFPromoCBs(sheet, tags, params, projection)
    import_StuntMatrixOn(sheet, tags, params, projection)
    import_WasteMatrixOn(sheet, tags, params, projection)
    import_UseDetailedStuntMatrix(sheet, tags, params, projection)
    import_UseDetailedWasteMatrix(sheet, tags, params, projection)
    import_FertilityRisksMatrixOn(sheet, tags, params, projection)
    
    # Health status
    # Baseline child health status
    import_NutrDefic(sheet, tags, params, projection)
    import_VitADefInPW(sheet, tags, params, projection)
    import_StatusAtBirth(sheet, tags, params, projection)
    import_DiarrInc(sheet, tags, params, projection)
    import_SevereDiarrInc(sheet, tags, params, projection)
    import_PneumInc(sheet, tags, params, projection)
    import_MeninInc(sheet, tags, params, projection)
    
    # Baseline maternal health status
    import_MaternalAnemia(sheet, tags, params, projection)
    import_PercWom15t49LowBMI(sheet, tags, params, projection)
    import_SyphilisAmongWRA(sheet, tags, params, projection)
    import_PercExposedFalciparum(sheet, tags, params, projection)    
    
    import_PercWomenWithPrevPreEclamp(sheet, tags, params, projection)
    import_PercWomenWithChronicHypertension(sheet, tags, params, projection)
    import_FolicAcidDeficPrev(sheet, tags, params, projection)
    import_CongenitalDueToNTDsAF(sheet, tags, params, projection)
    
    # Nutrition status distributions
    import_StuntDistr(sheet, tags, params, projection)
    import_SingleStuntDistr(sheet, tags, params, projection)
    import_WasteDistr(sheet, tags, params, projection)
    import_SingleWasteDistr(sheet, tags, params, projection)
    
    # Pathogens
    import_DiarrPath(sheet, tags, params, projection)
    import_PneumPath(sheet, tags, params, projection)
    import_MeninPath(sheet, tags, params, projection)
    
    # Baseline child mortality
    import_BaselineMort(sheet, tags, params, projection)
    import_PercDthByCause(sheet, params, projection, VariablesRW)
    
    # Baseline adolescent mortality
    import_AdolMortRatio(sheet, tags, params, projection)
    import_PercAdolDeathsByCause(sheet, params, projection, VariablesRW)
    
    # Baseline maternal mortality
    import_MatMortRatio(sheet, tags, params, projection)
    import_PercMatDthByCause(sheet, params, projection, VariablesRW)
    
    # Abortion
    import_PercPregEndAbort(sheet, tags, params, projection)
    import_AbortIncRatio(sheet, tags, params, projection)
    
    # Stillbirth
    import_SBRate(sheet, tags, params, projection)
    import_SBCauses(sheet, params, projection, VariablesRW)
    
    # Household status
    import_PerCapitaInc(sheet, tags, params, projection)
    import_FoodInsecure(sheet, tags, params, projection)
    import_AvgHouseholdSize(sheet, tags, params, projection)
    
    # Economic status
    import_GNIPerCap(sheet, tags, params, projection)
    import_LaborForceParRate(sheet, tags, params, projection)
    import_LaborShareInc(sheet, tags, params, projection)
    
    # Coverage
    import_Coverage(sheet, params, projection, VariablesRW)
    import_BFPrev(sheet, tags, params, projection)
    import_EarlyInitBFPrev(sheet, tags, params, projection)
    import_RoutDetVaccCov(sheet, tags, params, projection)
    import_PentaDetVaccCov(sheet, tags, params, projection)
    import_AgeAndBirthOrderMatrix(sheet, tags, params, projection)
    import_BirthIntervalsMatrix(sheet, tags, params, projection)
    
    # Maternal, Stillbirth, and Child Efficacy
    import_MatEff(sheet, params, projection, VariablesRW)
    import_SBEff(sheet, params, projection, VariablesRW)
    import_ChildEff(sheet, params, projection, VariablesRW)
    import_DetVaccEff(sheet, params, projection, VariablesRW)
    
    # Effectiveness of interventions on incidence
    import_DiarrIncReduction(sheet, tags, params, projection)
    import_SevDiarrIncReduction(sheet, tags, params, projection)
    import_PneumIncReduction(sheet, tags, params, projection)
    import_MeninIncReduction(sheet, tags, params, projection)
    import_RelRisksDiarr(sheet, tags, params, projection)
    import_RelRisksPneum(sheet, tags, params, projection)
    import_RelRisksMenin(sheet, tags, params, projection)

    # Herd effectiveness of vaccines
    import_HerdVaccEff(sheet, params, projection, VariablesRW)

    # Impact on food security
    import_ImpOnFoodSecurity(sheet, tags, params, projection)

    # Effectiveness of nutrition interventions
    import_AgeAndBirthOrder(sheet, tags, params, projection)
    import_BirthIntervals(sheet, tags, params, projection)
    import_IntervForBO(sheet, tags, params, projection)
    import_ImpactOnStunt(sheet, tags, params, projection)
    import_ImpactOnWaste(sheet, tags, params, projection)
    import_ImpactOnMatAnemia(sheet, tags, params, projection)
    import_ImpactBFPromo(sheet, tags, params, projection)
    import_KMConBF(sheet, tags, params, projection)
    import_LBWF(sheet, tags, params, projection)
    import_ReducStunt(sheet, tags, params, projection)
    import_EducAttain(sheet, tags, params, projection)
    
    # Impact of under-nutrition on mortality
    import_RelRisksStunt(sheet, params, projection, VariablesRW)
    import_RelRisksWaste(sheet, params, projection, VariablesRW)
    import_ImpactBFOnMortNeoNat(sheet, tags, params, projection)
    import_ImpactBFOnMortPostNat(sheet, params, projection, VariablesRW)
    import_RelRisksIUGR_LBW(sheet, params, projection, VariablesRW)
    import_RelRisksAnemia(sheet, tags, params, projection)
        
    return True

# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# /////                                                                                                          /////
# /////                                                                                                          /////
# /////                                                                                                          /////
# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


def readYearData(destData, sheet, params, startCol, row, colOffset = 0):
    col = startCol
    for year in GBRange(params.firstYear, params.finalYear + colOffset):
        t = getYearIdx(year, params.firstYear)
        if col < len(sheet[row]):
            if not sheet[row, col] == '':
                destData[t] = float(sheet[row, col])
        col += 1

# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# /////                                                                                                          /////
# /////                                                                                                          /////
# /////                                                                                                          /////
# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def import_VariablesRW(sheet, tags, params, projection):
    def getNum(tag, rowOffset):
        modvarTagRow = findTagRow(sheet, tag, GB_RW_DescriptCol)
        num = int(sheet[modvarTagRow + rowOffset, GB_RW_DataStartCol])
        return num

    result = {
               'SBNumCauses'             : getNum('<SBNumCauses MV>', 2),
               'AdolNumCauses'           : getNum('<AdolNumCauses MV>', 2),
               'DetVaccBool'             : getNum('<DetVaccBools MV>', 2),
               'DetVaccNumEnteredBool'   : getNum('<DetVaccBools MV>', 4),
               'NumDetVaccTypes'         : getNum('<DetVaccBools MV>', 6),
               'FirstPNNDeath'           : getNum('<DetVaccBools MV>', 8),
               'LastPNNDeath'            : getNum('<DetVaccBools MV>', 9),
               'NumIntervs'              : getNum('<GeneralNumbers MV>', 2),
               'NumDeathCauses'          : getNum('<GeneralNumbers MV>', 4),
               'NumMatDeathCauses'       : getNum('<GeneralNumbers MV>', 6),
               'NumHerdVaccs'            : getNum('<GeneralNumbers MV>', 8),
               'NumPathogensDiarr'       : getNum('<Number of Pathogens - Diarrhea MV>', 1),
               'NumPathogensPneum'       : getNum('<Number of Pathogens - Pneumonia MV>', 1),
               'NumPathogensMenin'       : getNum('<Number of Pathogens - Meningitis MV>', 1),
               'MaxVaccDose'             : getNum('<Maximum Vaccine Dose MV>', 1),
    }

    return result

# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# /////                                                                                                          /////
# /////                                            Controls                                                      /////
# /////                                                                                                          /////
# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def import_MenARecommended(sheet, tags, params, projection):
    modvarTagRow = tags.get('<MenA recommended>', None)
    if modvarTagRow:
        projection[CS_MenARecommendedTag] = bool(int(sheet[modvarTagRow + 2, GB_RW_DataStartCol]))

def import_IPTpCBChecked(sheet, tags, params, projection):
    modvarTagRow = tags.get('<IPTpCBStatus MV2>', None)
    if modvarTagRow:
        projection[CS_IPTpCBCheckedTag] = bool(int(sheet[modvarTagRow + 2, GB_RW_DataStartCol]))

def import_FirstYearAtWork(sheet, tags, params, projection):
    modvarTagRow = tags.get('<First year at work MV>', None)
    if modvarTagRow:
        projection[CS_FirstYearAtWorkTag] = int(sheet[modvarTagRow + 2, GB_RW_DataStartCol])

def import_LastYearAtWork(sheet, tags, params, projection):
    modvarTagRow = tags.get('<Last year at work MV>', None)
    if modvarTagRow:
        projection[CS_LastYearAtWorkTag] = int(sheet[modvarTagRow + 2, GB_RW_DataStartCol])

def import_AbortCalcFamPlan(sheet, tags, params, projection):
    modvarTagRow = tags.get('<AbortCalcFamPlan MV2>', None)
    if modvarTagRow:
        projection[CS_AbortCalcFamPlanTag] = bool(int(sheet[modvarTagRow + 2, GB_RW_DataStartCol]))

def import_CalcCovFromInputs(sheet, tags, params, projection):    
    modvarTagRow = tags.get('<CalcCovFromInputs MV2>', None)

    if modvarTagRow:
        CalcCovFromInputs = []
    
        row = modvarTagRow + 2
        col = GB_RW_DataStartCol
        while not sheet[row, col] == '':
            CalcCovFromInputs.append(CSGetCurCCFI(int(sheet[row, col])))
            col+= 1
        
        projection[CS_CalcCovFromInputsTag] = list(set(CalcCovFromInputs))

def import_EnterBFImproveData(sheet, tags, params, projection):
    modvarTagRow = tags.get('<BFEntryMode MV3>', None)
    if modvarTagRow:
        projection[CS_EnterBFImproveDataTag] = int(sheet[modvarTagRow + 2, GB_RW_DataStartCol])    
        if projection[CS_EnterBFImproveDataTag] == CS_MstBFPrevMode:
            projection[CS_SelectedIVSetTag].append(CS_MstDirectEntryOfBF)    
        if projection[CS_EnterBFImproveDataTag] == CS_MstBFPromotionMode:
            projection[CS_SelectedIVSetTag].append(CS_MstBFPromotion)

def import_BFPromoCBs(sheet, tags, params, projection):
    modvarTagRow = tags.get('<Breastfeeding Promotion Checkboxes MV>', None)
    if modvarTagRow:
        for i in GBRange(CS_BFPromoHealthSystem, CS_BFPromoHomeComm):
            projection[CS_BFPromoCBsTag][i] = bool(int(sheet[modvarTagRow + i + 1, GB_RW_DataStartCol]))

def import_StuntMatrixOn(sheet, tags, params, projection):
    modvarTagRow = tags.get('<StuntingMatrixOn MV2>', None)
    if modvarTagRow:
        projection[CS_StuntMatrixOnTag] = bool(int(sheet[modvarTagRow + 2, GB_RW_DataStartCol]))
        if projection[CS_StuntMatrixOnTag]:
            projection[CS_SelectedIVSetTag].append(CS_MstDirectEntryOfStunting)

def import_WasteMatrixOn(sheet, tags, params, projection):
    modvarTagRow = tags.get('<WastingMatrixOn MV2>', None)
    if modvarTagRow:
        projection[CS_WasteMatrixOnTag] = bool(int(sheet[modvarTagRow + 2, GB_RW_DataStartCol]))
        if projection[CS_WasteMatrixOnTag]:
            projection[CS_SelectedIVSetTag].append(CS_MstDirectEntryOfWasting)

def import_UseDetailedStuntMatrix(sheet, tags, params, projection):
    modvarTagRow = tags.get('<Use Detailed Stunting Matrix MV>', None)
    if modvarTagRow:
        projection[CS_UseDetailedStuntMatrixTag] = bool(int(sheet[modvarTagRow + 2, GB_RW_DataStartCol]))

def import_UseDetailedWasteMatrix(sheet, tags, params, projection):
    modvarTagRow = tags.get('<Use Detailed Wasting Maxtrix MV>', None)
    if modvarTagRow:
        projection[CS_UseDetailedWasteMatrixTag] = bool(int(sheet[modvarTagRow + 2, GB_RW_DataStartCol]))

def import_FertilityRisksMatrixOn(sheet, tags, params, projection):
    modvarTagRow = tags.get('<FertilityRisksMatrixOn MV2>', None)
    if modvarTagRow:
        projection[CS_FertilityRisksMatrixOnTag] = bool(int(sheet[modvarTagRow + 2, GB_RW_DataStartCol]))
        if projection[CS_FertilityRisksMatrixOnTag]:
            projection[CS_SelectedIVSetTag].append(CS_MstMaternalAgeOfBirthOrder)

# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# /////                                                                                                          /////
# /////                                          Health status                                                   /////
# /////                                                                                                          /////
# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#########################################  Baseline child health status ##############################################

def import_NutrDefic(sheet, tags, params, projection):
    modvarTagRow = tags.get('<Nutritional Deficiencies MV2>', None)
    if modvarTagRow:
        modvar = projection[CS_NutrDeficTag]
    
        numElements = int(sheet[modvarTagRow + 2, GB_RW_DataStartCol])
        
        row = modvarTagRow + 3
            
        for i in GBRange(1, numElements):
            currID = CSGetNutritionalDeficienciesCurrID(int(sheet[row, GB_RW_NotesCol]))
            modvar[currID] = float(sheet[row, GB_RW_DataStartCol])
            row += 1

def import_VitADefInPW(sheet, tags, params, projection):
    modvarTagRow = tags.get('<VitA deficiency in PW MV>', None)
    if modvarTagRow:
        projection[CS_VitADefInPWTag] = float(sheet[modvarTagRow + 2, GB_RW_DataStartCol])

def import_StatusAtBirth(sheet, tags, params, projection):
    modvarTagRow = tags.get('<Status At Birth MV>', None)
    if modvarTagRow:
        for i in GBRange(CS_PreTermSGA, CS_TermAGA):
            projection[CS_StatusAtBirthTag][i] = float(sheet[modvarTagRow + i + 1, GB_RW_DataStartCol])

def import_DiarrInc(sheet, tags, params, projection):
    modvarTagRow = tags.get('<DiarInc MV>', None)
    if modvarTagRow:
        for a in GBRange(CS_0t1months, CS_24t60months):
            projection[CS_DiarrIncTag][a] = float(sheet[modvarTagRow + 2, GB_RW_DataStartCol + a])

def import_SevereDiarrInc(sheet, tags, params, projection):
    modvarTagRow = tags.get('<SevereDiarInc MV>', None)
    if modvarTagRow:
        for a in GBRange(CS_0t1months, CS_24t60months):
            projection[CS_SevereDiarrIncTag][a] = float(sheet[modvarTagRow + 2, GB_RW_DataStartCol + a])

def import_PneumInc(sheet, tags, params, projection):
    modvarTagRow = tags.get('<Pneumonia Incidence MV>', None)
    if modvarTagRow:
        for a in GBRange(CS_0t1months, CS_24t60months):
            projection[CS_PneumIncTag][a] = float(sheet[modvarTagRow + 2, GB_RW_DataStartCol + a])

def import_MeninInc(sheet, tags, params, projection):
    modvarTagRow = tags.get('<Meningitis Incidence MV>', None)
    if modvarTagRow:
        for a in GBRange(CS_0t1months, CS_24t60months):
            projection[CS_MeninIncTag][a] = float(sheet[modvarTagRow + 2, GB_RW_DataStartCol + a])

#######################################  Baseline maternal health status ############################################

def import_MaternalAnemia(sheet, tags, params, projection):
    modvarTagRow = tags.get('<Maternal Anemia MV>', None)
    if modvarTagRow:
        for i in GBRange(CS_Preg_Anemia, CS_NonPreg_IronDeficAnemia):
            projection[CS_MaternalAnemiaTag][i] = float(sheet[modvarTagRow + i + 1, GB_RW_DataStartCol])

def import_PercWom15t49LowBMI(sheet, tags, params, projection):
    modvarTagRow = tags.get('<Percentage of women aged 15-49 with low BMI MV>', None)
    if modvarTagRow:
        projection[CS_PercWom15t49LowBMITag] = float(sheet[modvarTagRow + 2, GB_RW_DataStartCol])

def import_SyphilisAmongWRA(sheet, tags, params, projection):
    modvarTagRow = tags.get('<Syphilis among WRA MV>', None)
    if modvarTagRow:
        projection[CS_SyphilisAmongWRATag] = float(sheet[modvarTagRow + 2, GB_RW_DataStartCol])

def import_PercExposedFalciparum(sheet, tags, params, projection):
    modvarTagRow = tags.get('<Percent exposed to falciparum>', None)
    if modvarTagRow:
        projection[CS_PercExposedFalciparumTag] = float(sheet[modvarTagRow + 2, GB_RW_DataStartCol])

######################################################################################################################

def import_PercWomenWithPrevPreEclamp(sheet, tags, params, projection):
    modvarTagRow = tags.get('<Percent of women with previous pre-eclampsia>', None)
    if modvarTagRow:
        projection[CS_PercWomenWithPrevPreEclampTag] = float(sheet[modvarTagRow + 2, GB_RW_DataStartCol])

def import_PercWomenWithChronicHypertension(sheet, tags, params, projection):
    modvarTagRow = tags.get('<Percent of women with chronic hypertension>', None)
    if modvarTagRow:
        projection[CS_PercWomenWithChronicHypertensionTag] = float(sheet[modvarTagRow + 2, GB_RW_DataStartCol])

def import_FolicAcidDeficPrev(sheet, tags, params, projection):
    modvarTagRow = tags.get('<Folic acid deficient prevalence>', None)
    if modvarTagRow:
        projection[CS_FolicAcidDeficPrevTag] = float(sheet[modvarTagRow + 2, GB_RW_DataStartCol])

def import_CongenitalDueToNTDsAF(sheet, tags, params, projection):
    modvarTagRow = tags.get('<CongenitalDueToNTDsAF>', None)
    if modvarTagRow:
        projection[CS_CongenitalDueToNTDsAFTag] = float(sheet[modvarTagRow + 2, GB_RW_DataStartCol])

########################################  Nutrition status distributions #############################################

def import_StuntDistr(sheet, tags, params, projection):
    modvarTagRow = tags.get('<Stunting distribution MV>', None)
    if modvarTagRow:
        modvar = projection[CS_StuntDistrTag]

        row = modvarTagRow + 3
        
        for sd in GBRange(CS_GT1STD, CS_GT3STD):
            for a in GBRange(CS_0t1months, CS_24t60months):
                readYearData(modvar[sd][a], sheet, params, GB_RW_DataStartCol + 1, row)
                row += 1

def import_SingleStuntDistr(sheet, tags, params, projection):
    modvarTagRow = tags.get('<Single Stunting distribution MV>', None)
    if modvarTagRow:
        modvar = projection[CS_SingleStuntDistrTag]
        readYearData(modvar, sheet, params, GB_RW_DataStartCol + 1, modvarTagRow + 3)

def import_WasteDistr(sheet, tags, params, projection):
    modvarTagRow = tags.get('<Wasting distribution MV>', None)
    if modvarTagRow:
        modvar = projection[CS_WasteDistrTag]

        row = modvarTagRow + 3
        
        for sd in GBRange(CS_GT1STD, CS_GT3STD):
            for a in GBRange(CS_0t1months, CS_24t60months):
                readYearData(modvar[sd][a], sheet, params, GB_RW_DataStartCol + 1, row)
                row += 1

def import_SingleWasteDistr(sheet, tags, params, projection):
    modvarTagRow = tags.get('<Single Wasting distribution MV>', None)
    if modvarTagRow:
        modvar = projection[CS_SingleWasteDistrTag]
        readYearData(modvar, sheet, params, GB_RW_DataStartCol + 1, modvarTagRow + 3)

#################################################  Pathogens  ########################################################

def import_DiarrPath(sheet, tags, params, projection):
    modvarTagRow = tags.get('<Diarrhea pathogens MV2>', None)
    if modvarTagRow:
        modvar = projection[CS_DiarrPathTag]

        row = modvarTagRow + 2
        
        for s in GBRange(CS_Distr_All, CS_Distr_Fatal):
            for i in GBRange(1, CS_MaxPathDiar):
                for a in GBRange(CS_0t1months, CS_24t60months):
                    modvar[s][i][a] = float(sheet[row, GB_RW_DataStartCol + a])
                row += 1

def import_PneumPath(sheet, tags, params, projection):
    modvarTagRow = tags.get('<Pneumonia pathogens MV>', None)
    if modvarTagRow:
        modvar = projection[CS_PneumPathTag]

        row = modvarTagRow + 2
        
        for s in GBRange(CS_Distr_Sevr, CS_Distr_Fatal):
            for i in GBRange(1, CS_MaxPathPneum):
                for a in GBRange(CS_0t1months, CS_24t60months):
                    modvar[s][i][a] = float(sheet[row, GB_RW_DataStartCol + a])
                row += 1

def import_MeninPath(sheet, tags, params, projection):
    modvarTagRow = tags.get('<Meningitis pathogens MV>', None)
    if modvarTagRow:
        modvar = projection[CS_MeninPathTag]

        row = modvarTagRow + 2
        
        for s in GBRange(CS_Distr_Sevr, CS_Distr_Fatal):
            for i in GBRange(1, CS_MaxPathMenin):
                for a in GBRange(CS_0t1months, CS_24t60months):
                    modvar[s][i][a] = float(sheet[row, GB_RW_DataStartCol + a])
                row += 1

###########################################  Baseline child mortality ################################################

def import_BaselineMort(sheet, tags, params, projection):
    modvarTagRow = tags.get('<BaselineMort MV>', None)
    if modvarTagRow:
        modvar = projection[CS_BaselineMortTag]
    
        for i in GBRange(1, CS_MaxBaselineMort):           
            modvar[i] = float(sheet[modvarTagRow + 2, GB_RW_DataStartCol + i])

def import_PercDthByCause(sheet, params, projection, VariablesRW):    
    modvarTagRow = tags.get('<PercDthByCause MV2>', None)
    if modvarTagRow:
        modvar = projection[CS_PercDthByCauseTag]
    
        row = modvarTagRow + 3
        
        for id in GBRange(CS_DxC_Default, CS_DxC_NoAIDS):
            for d in GBRange(1, VariablesRW['NumDeathCauses']):
                mstID = int(sheet[row, GB_RW_DataStartCol])
                currID = CSGetCurDeathID(mstID)
                if not currID == 0:            
                    for a in GBRange(CS_0t1months, CS_24t60months):
                        modvar[id][currID][a] = float(sheet[row, GB_RW_DataStartCol + a])
                row += 1

#########################################  Baseline adolescent mortality ##############################################

def import_AdolMortRatio(sheet, tags, params, projection):
    modvarTagRow = tags.get('<AdolMortRatio MV2>', None)
    if modvarTagRow:
        if not sheet[modvarTagRow + 2, GB_RW_DataStartCol] == '':
            projection[CS_AdolMortRatioTag] = float(sheet[modvarTagRow + 2, GB_RW_DataStartCol])

def import_PercAdolDeathsByCause(sheet, params, projection, VariablesRW):
    modvarTagRow = tags.get('<PercAdolDeathsByCause MV2>', None)
    if modvarTagRow:
        modvar = projection[CS_PercAdolDeathsByCauseTag]
    
        row = modvarTagRow + 2
        
        for d in GBRange(1, VariablesRW['AdolNumCauses']):
            mstID = int(sheet[row, GB_RW_DataStartCol])
            currID = CSGetAdol_CurDeathID(mstID)
            if not currID == 0:            
                for s in GBRange(GB_Male, GB_Female):
                    for a in GBRange(CS_5yrs_9yrs, CS_15yrs_19yrs):
                        colOffset = ((s - 1) * CS_15yrs_19yrs) + a
                        modvar[currID][s][a] = float(sheet[row, GB_RW_DataStartCol + colOffset])
            row += 1

##########################################  Baseline maternal mortality ###############################################

def import_MatMortRatio(sheet, tags, params, projection):
    modvarTagRow = tags.get('<MatMortRatio MV2>', None)
    if modvarTagRow:
        projection[CS_MatMortRatioTag] = float(sheet[modvarTagRow + 2, GB_RW_DataStartCol])

def import_PercMatDthByCause(sheet, params, projection, VariablesRW):
    modvarTagRow = tags.get('<PercMatDeathsByCause MV>', None)
    if modvarTagRow:
        modvar = projection[CS_PercMatDthByCauseTag]
    
        col = GB_RW_DataStartCol + 1
        for d in GBRange(1, VariablesRW['NumMatDeathCauses']):
            mstID = int(sheet[modvarTagRow + 2, col])
            currID = CSGetMat_CurDeathID(mstID)
            if not currID == 0:            
                modvar[currID] = float(sheet[modvarTagRow + 3, col])
            col += 1

###################################################  Abortion  #######################################################

def import_PercPregEndAbort(sheet, tags, params, projection):
    modvarTagRow = tags.get('<PercPregEndAbort MV2>', None)
    if modvarTagRow:
        projection[CS_PercPregEndAbortTag] = float(sheet[modvarTagRow + 2, GB_RW_DataStartCol])

def import_AbortIncRatio(sheet, tags, params, projection):
    modvarTagRow = tags.get('<AbortIncRatio MV 2>', None)
    if modvarTagRow:
        modvar = projection[CS_AbortIncRatioTag]
        readYearData(modvar, sheet, params, GB_RW_DataStartCol, modvarTagRow + 3)

##################################################  Stillbirth  ######################################################

def import_SBRate(sheet, tags, params, projection):
    modvarTagRow = tags.get('<SBRate MV2>', None)
    if modvarTagRow:
        projection[CS_SBRateTag] = float(sheet[modvarTagRow + 2, GB_RW_DataStartCol])

def import_SBCauses(sheet, params, projection, VariablesRW):
    modvarTagRow = tags.get('<SBCauses MV>', None)
    if modvarTagRow:
        modvar = projection[CS_SBCausesTag]
    
        row = modvarTagRow + 2
        for d in GBRange(1, VariablesRW['SBNumCauses']):
            mstID = int(sheet[row, GB_RW_DataStartCol])
            currID = CSGetSB_CurCauseID(mstID)
            if not currID == 0:            
                modvar[currID] = float(sheet[row + 1, GB_RW_DataStartCol])
            row += 2

###############################################  Household status ##################################################

def import_PerCapitaInc(sheet, tags, params, projection):
    modvarTagRow = tags.get('<PerCapitaInc MV>', None)
    if modvarTagRow:
        modvar = projection[CS_PerCapitaIncTag]
        readYearData(modvar, sheet, params, GB_RW_NotesCol, modvarTagRow + 2)

def import_FoodInsecure(sheet, tags, params, projection):
    modvarTagRow = tags.get('<FoodInsecure MV>', None)
    if modvarTagRow:
        modvar = projection[CS_FoodInsecureTag]
        readYearData(modvar, sheet, params, GB_RW_NotesCol, modvarTagRow + 2)

def import_AvgHouseholdSize(sheet, tags, params, projection):
    modvarTagRow = tags.get('<Average Household Size MV>', None)
    if modvarTagRow:
        modvar = projection[CS_AvgHouseholdSizeTag]
        readYearData(modvar, sheet, params, GB_RW_DataStartCol, modvarTagRow + 2)

###############################################  Economic status ##################################################

def import_GNIPerCap(sheet, tags, params, projection):
    modvarTagRow = tags.get('<GNIPerCap MV>', None)
    if modvarTagRow:
        modvar = projection[CS_AnnualPercGrowthRateTag]
        readYearData(modvar, sheet, params, GB_RW_NotesCol, modvarTagRow + 2, CS_MaxFinalYrAtWork)

def import_LaborForceParRate(sheet, tags, params, projection):
    modvarTagRow = tags.get('<LaborForceParRate MV>', None)
    if modvarTagRow:
        modvar = projection[CS_LaborForceParRateTag]
        readYearData(modvar, sheet, params, GB_RW_NotesCol, modvarTagRow + 2, CS_MaxFinalYrAtWork)

def import_LaborShareInc(sheet, tags, params, projection):
    modvarTagRow = tags.get('<LaborShareInc MV>', None)
    if modvarTagRow:
        modvar = projection[CS_PercGDPAllocWageTag]
        readYearData(modvar, sheet, params, GB_RW_NotesCol, modvarTagRow + 2, CS_MaxFinalYrAtWork)

# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# /////                                                                                                          /////
# /////                                             Coverage                                                     /////
# /////                                                                                                          /////
# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def import_Coverage(sheet, params, projection, VariablesRW):
    
    def ReadData(projection, row, mstID, c1, Tag = ''):
        if mstID in projection[CS_IVInfoTag]:
            if (not CSIsVaccine(mstID)):            
                t1 = 0
                t2 = getYearIdx(params.finalYear, params.firstYear)
                
                # If there is data other than zeros (zeros tag does not exist) then read in the data
                if not sheet[row, c1] == '<ZEROS>':
                    c = c1 + 1

                    # Starting at column F, all four retro years are written out first for coverage, 
                    # then coverage from calcYear and above is written out.
                    # For Quality, data from calcYear and above starts at column F.
                    
                    if Tag == '': 
                        c += CS_DetVaccRetroOffset
                        record = GetCoveragePtr(projection, mstID, CS_Coverage)
                        for t in GBRange(t1, t2):
                            if not sheet[row, c] == '':
                                record[t] = float(sheet[row, c])
                            c += 1

                    if Tag == '<Quality>': 
                        record = GetCoveragePtr(projection, mstID, CS_Quality)
                        if not record == None:
                            for t in GBRange(t1, t2):                
                                if not sheet[row, c] == '':
                                    record[t] = float(sheet[row, c])
                                c += 1
    
    modvarTagRow = tags.get('<Coverage MV3>', None)
    if modvarTagRow:
        row = modvarTagRow + 5
        c1 = GB_RW_DataStartCol + 1
        
        for i in GBRange(1, VariablesRW['NumIntervs']):
            mstID = sheet[row, GB_RW_DataStartCol]
            ReadData(projection, row, mstID, c1)
            row += 1
            if sheet[row, c1] == '<Quality>':
                ReadData(projection, row, mstID, c1, '<Quality>')
                row += 1

def import_BFPrev(sheet, tags, params, projection):
    modvarTagRow = tags.get('<Breastfeeding Prevalence MV>', None)
    if modvarTagRow:
        modvar = projection[CS_BFPrevTag]    

        row = modvarTagRow + 2
        
        for bf in GBRange(CS_ExclusiveBF, CS_NotBF):
            for a in GBRange(CS_0t1months, CS_12t24months):
                readYearData(modvar[bf][a], sheet, params, GB_RW_DataStartCol, row)
                row += 1
            row += 1

def import_EarlyInitBFPrev(sheet, tags, params, projection):
    modvarTagRow = tags.get('<Early Initiation BF prevalence MV2>', None)
    if modvarTagRow:
        modvar = projection[CS_EarlyInitBFPrevTag]    

        row = modvarTagRow + 2
        
        for a in GBRange(CS_AgeSummary, CS_24t60months):
            readYearData(modvar[a], sheet, params, GB_RW_DataStartCol, row)
            row += 1

def import_RoutDetVaccCov(sheet, tags, params, projection):
    modvarTagRow = tags.get('<RoutDetVaccCov MV3>', None)
    if modvarTagRow:
        modvar = projection[CS_RoutDetVaccCovTag]
        retro = projection[CS_RoutDetVaccCovMetaTag]['retro']

        row = modvarTagRow + 4
                
        LastDetVaccRW = int(sheet[row, GB_RW_DataStartCol])
        
        row += 2
        
        c1 = GB_RW_DataStartCol + 2        
        t1 = 0
        t2 = getYearIdx(params.finalYear, params.firstYear)
                
        for vt in GBRange(1, LastDetVaccRW):
            # Write the id and data
            mstID = sheet[row, GB_RW_DataStartCol]

            # Retrieve master intervention id
            row += 2

            for dose in GBRange(1, CS_MaxVaccDose):
                c = c1

                if mstID in projection[CS_IVInfoTag]:        
                    if (CSIsVaccine(int(mstID))):
                        currID = CSGetVaccCurrID(int(mstID))
                        
                        # Retro - the retro years should be located before the normal
                        # coverage data. Note that t=1 is not in the retro buffer, but we
                        # are putting it in this loop to keep the regular t loop consistant
                        # with that of other variables.
                        for t in GBRange(CS_DetVacc1YrsRetro, CS_DetVacc4YrsRetro):
                            # Make sure values don't go below 0 (Bug in 5.28)
                            val = float(sheet[row, c])
                            if val < 0:
                                val = 0
                            retro[currID][dose][t] = val
                            c += 1

                        # Non-retro
                        for t in GBRange(t1, t2):
                            # Make sure values don't go below 0 (Bug in 5.28)
                            if not sheet[row, c] == '':
                                val = float(sheet[row, c])
                                if val < 0:
                                    val = 0
                                modvar[currID][dose][t] = val
                            c += 1

                row += 1

def import_PentaDetVaccCov(sheet, tags, params, projection):
    modvarTagRow = tags.get('<PentavalentDetVaccCov MV>', None)
    if modvarTagRow:
        modvar = projection[CS_PentaDetVaccCovTag]
        retro = projection[CS_PentaDetVaccCovMetaTag]['retro']

        row = modvarTagRow + 5
        
        c1 = GB_RW_DataStartCol + 2        
        t1 = 0
        t2 = getYearIdx(params.finalYear, params.firstYear)
               
        c = c1
        # Retro - the retro years should be located before the normal
        # coverage data. Note that t=1 is not in the retro buffer, but we
        # are putting it in this loop to keep the regular t loop consistant
        # with that of other variables. 
        for t in GBRange(CS_DetVacc1YrsRetro, CS_DetVacc4YrsRetro):
            # Make sure values don't go below 0 (Bug in 5.28)
            val = float(sheet[row, c])
            if val < 0:
                val = 0
            retro[t] = val
            c += 1
        
        # Non-retro
        for t in GBRange(t1, t2):
            # Make sure values don't go below 0 (Bug in 5.28)
            if not sheet[row, c] == '':                                
                val = float(sheet[row, c])
                if val < 0:
                    val = 0
                modvar[t] = val
            c += 1

def import_AgeAndBirthOrderMatrix(sheet, tags, params, projection):
    modvarTagRow = tags.get('<Age And Birth Order Matrix MV2>', None)
    if modvarTagRow:
        modvar = projection[CS_AgeAndBirthOrderMatrixTag]  

        row = modvarTagRow + 3
        
        for ma in GBRange(CS_AllYrs, CS_35_49Yrs):
            for bo in GBRange(CS_FirstBirth, CS_GTThirdBirth):
                readYearData(modvar[ma][bo], sheet, params, GB_RW_DataStartCol + 1, row)
                row += 1

def import_BirthIntervalsMatrix(sheet, tags, params, projection):
    modvarTagRow = tags.get('<Birth Intervals Matrix MV2>', None)
    if modvarTagRow:
        modvar = projection[CS_BirthIntervalsMatrixTag]  

        row = modvarTagRow + 2
        
        for i in GBRange(CS_FirstBirth, CS_GE24Mths):
            readYearData(modvar[i], sheet, params, GB_RW_DataStartCol + 1, row)
            row += 1

# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# /////                                                                                                          /////
# /////                             Maternal, Stillbirth, and Child Efficacy                                     /////
# /////                                                                                                          /////
# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def import_MatEff(sheet, params, projection, VariablesRW):
    modvarTagRow = tags.get('<Maternal Efficacy MV3>', None)
    if modvarTagRow:
        modvar = projection[CS_MatEffTag]
    
        row = modvarTagRow + 3

        for i in GBRange(1, VariablesRW['NumIntervs']):
            for aff in GBRange(CS_Efficacy, CS_AffecFract): 
                for j in GBRange(1, VariablesRW['NumMatDeathCauses']): 
                    ivMstID = sheet[row, GB_RW_DataStartCol]
                    dMstID = int(sheet[row, GB_RW_DataStartCol + 1])
                    dCurrID = CSGetMat_CurDeathID(dMstID)

                    if ivMstID in projection[CS_IVInfoTag] and not dCurrID == 0:
                        currID = projection[CS_IVInfoTag][ivMstID]['currID']
                        modvar[CS_Data][aff][currID][dCurrID] = float(sheet[row, GB_RW_DataStartCol + 2])
                    
                    row += 1

def import_SBEff(sheet, params, projection, VariablesRW):
    modvarTagRow = -1
    
    row = tags.get('<SBEfficacy MV2>', None)
    if row > -1:
        modvarTagRow = row
        lastIndex = CS_AffecFract
    
    row = tags.get('<SBEfficacy MV3>', None)
    if row > -1:
        modvarTagRow = row
        lastIndex = CS_AdjustedRR
    
    if modvarTagRow:
        modvar = projection[CS_SBEffTag]
    
        row = modvarTagRow + 3

        for i in GBRange(1, VariablesRW['NumIntervs']):
            ivMstID = sheet[row, GB_RW_DataStartCol]
            if not sheet[row, GB_RW_DataStartCol + 1] == '<ZEROS AND ONES>':
                row += 1
                for j in GBRange(1, VariablesRW['SBNumCauses']): 
                    dMstID = int(sheet[row, GB_RW_DataStartCol])
                    dCurrID = CSGetSB_CurCauseID(dMstID)

                    if ivMstID in projection[CS_IVInfoTag] and not dCurrID == 0:
                        currID = projection[CS_IVInfoTag][ivMstID]['currID']
                        for aff in GBRange(CS_Efficacy, lastIndex): 
                            modvar[CS_Data][aff][currID][dCurrID] = float(sheet[row, GB_RW_DataStartCol + aff])
                    
                    row += 1
            else:
                row += 1

def import_ChildEff(sheet, params, projection, VariablesRW):
    modvarTagRow = tags.get('<Efficacy MV2>', None)
    if modvarTagRow:
        modvar = projection[CS_ChildEffTag]
    
        row = modvarTagRow + 3

        for i in GBRange(1, VariablesRW['NumIntervs']):
            ivMstID = sheet[row, GB_RW_DataStartCol]
            if not sheet[row, GB_RW_DataStartCol + 1] == '<ZEROS AND ONES>':
                count = int(sheet[row, GB_RW_DataStartCol + 1])
                row += 1
                for j in GBRange(1, count): 
                    dMstID = int(sheet[row, GB_RW_DataStartCol])
                    dCurrID = CSGetCurDeathID(dMstID)
                    row += 1

                    for k in GBRange(CS_Efficacy, CS_AffecFract):                   
                        if ivMstID in projection[CS_IVInfoTag] and not dCurrID == 0:
                            currID = projection[CS_IVInfoTag][ivMstID]['currID']
                            for a in GBRange(CS_AgeSummary, CS_24t60months): 
                                modvar[CS_Data][k][currID][dCurrID][a] = float(sheet[row, GB_RW_DataStartCol + a + 1])
                        row += 1
            else:
                row += 1

def import_DetVaccEff(sheet, params, projection, VariablesRW):
    modvarTagRow = tags.get('<DetVaccEff MV2>', None)
    if modvarTagRow:
        modvar = projection[CS_DetVaccEffTag]
    
        row = modvarTagRow + 3
        LastVacc_Det = int(sheet[row, GB_RW_DataStartCol])
        row += 1
        
        for vt in GBRange(1, LastVacc_Det):
            vaccCurrID = CSGetVaccCurrID(int(sheet[row, GB_RW_DataStartCol]))
            if not sheet[row, GB_RW_DataStartCol + 1] == '<ZEROS AND ONES>':
                count = int(sheet[row, GB_RW_DataStartCol + 1])
                row += 1
                for j in GBRange(1, count): 
                    dMstID = int(sheet[row, GB_RW_DataStartCol + 1])
                    dCurrID = CSGetCurDeathID(dMstID)
                    row += 1
                    
                    for dose in GBRange(1, CS_MaxVaccDose):                    
                        for k in GBRange(CS_Efficacy, CS_AffecFract):                   
                            if vaccCurrID and not dCurrID == 0:
                                for a in GBRange(CS_AgeSummary, CS_24t60months): 
                                    modvar[CS_Data][k][vaccCurrID][dCurrID][dose][a] = float(sheet[row, GB_RW_DataStartCol + a + 2])
                            row += 1
            else:
                row += 1

# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# /////                                                                                                          /////
# /////                           Effectiveness of interventions on incidence                                    /////
# /////                                                                                                          /////
# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def import_DiarrIncReduction(sheet, tags, params, projection):
    modvarTagRow = tags.get('<DiarrIncReduction MV3>', None)
    if modvarTagRow:
        modvar = projection[CS_DiarrIncReductionTag]
        
        row = modvarTagRow + 2

        i = CSGetDiarIntervCurrID(int(sheet[row, GB_RW_NotesCol]))
        
        while not i == 0:
            for j in GBRange(CS_Efficacy, CS_AffecFract):                   
                for a in GBRange(CS_0t1months, CS_24t60months): 
                    modvar[CS_Data][i][j][a] = float(sheet[row, GB_RW_DataStartCol + a])
                row += 1
            
            i = 0
            mstID = sheet[row, GB_RW_NotesCol]
            if mstID.isdigit():
                i = CSGetDiarIntervCurrID(int(mstID))

def import_IncReduction(modvarTagRow, sheet, modvar, firstInterv, NumIntervs):
    row = modvarTagRow + 2
        
    for i in GBRange(firstInterv, NumIntervs):                   
        for j in GBRange(CS_Efficacy, CS_AffecFract):                   
            for a in GBRange(CS_0t1months, CS_24t60months): 
                modvar[CS_Data][i][j][a] = float(sheet[row, GB_RW_DataStartCol + a])
            row += 1

def import_SevDiarrIncReduction(sheet, tags, params, projection):
    modvarTagRow = tags.get('<Severe Diarrhea Incidence Reduction>', None)
    if modvarTagRow:
        modvar = projection[CS_SevDiarrIncReductionTag]        
        import_IncReduction(modvarTagRow, sheet, modvar, CS_FirstSevDiarInterv, CS_NumSevDiarIntervs)

def import_PneumIncReduction(sheet, tags, params, projection):
    modvarTagRow = tags.get('<Pneumonia Incidence Reduction MV>', None)
    if modvarTagRow:
        modvar = projection[CS_PneumIncReductionTag]        
        import_IncReduction(modvarTagRow, sheet, modvar, CS_FirstPneumInterv, CS_NumPneumIntervs)

def import_MeninIncReduction(sheet, tags, params, projection):
    modvarTagRow = tags.get('<Meningitis Incidence Reduction MV>', None)
    if modvarTagRow:
        modvar = projection[CS_MeninIncReductionTag]        
        import_IncReduction(modvarTagRow, sheet, modvar, CS_FirstMeningInterv, CS_NumMeningIntervs)

def import_RelRisks(modvarTagRow, sheet, modvar):  
    row = modvarTagRow + 2
    
    for i in GBRange(CS_Efficacy, CS_AffecFract):                   
        for j in GBRange(CS_ExclusiveBF, CS_NotBF):                   
            for a in GBRange(CS_0t1months, CS_24t60months): 
                modvar[CS_Data][i][j][a] = float(sheet[row, GB_RW_DataStartCol + a - 1])
            row += 1

def import_RelRisksDiarr(sheet, tags, params, projection):
    modvarTagRow = tags.get('<RelRisksDiarrhea MV2>', None)
    if modvarTagRow:
        modvar = projection[CS_RelRisksDiarrTag]
        import_RelRisks(modvarTagRow, sheet, modvar)

def import_RelRisksPneum(sheet, tags, params, projection):
    modvarTagRow = tags.get('<RelRisksPneumonia MV2>', None)
    if modvarTagRow:
        modvar = projection[CS_RelRisksPneumTag]
        import_RelRisks(modvarTagRow, sheet, modvar)

def import_RelRisksMenin(sheet, tags, params, projection):
    modvarTagRow = tags.get('<RelRisksMeningitis MV2>', None)
    if modvarTagRow:
        modvar = projection[CS_RelRisksMeninTag]
        import_RelRisks(modvarTagRow, sheet, modvar)

# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# /////                                                                                                          /////
# /////                                Herd effectiveness of vaccines                                            /////
# /////                                                                                                          /////
# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def import_HerdVaccEff(sheet, params, projection, VariablesRW):
    modvarTagRow = tags.get('<Custom herd vaccine efficacy MV 3>', None)
    if modvarTagRow:
        modvar = projection[CS_HerdVaccEffTag]
        
        row = modvarTagRow + 3
        
        LastHerdVaccRW = int(sheet[row, GB_RW_DataStartCol])
        
        row += 1

        for i in GBRange(1, LastHerdVaccRW):
            ID = int(sheet[row, GB_RW_DataStartCol])
            
            # If this is a regular HERD vaccine, the ID must correspond to a regular
            # HERD intervention, and is therefore a master ID.  Get the current ID
            # from it, if the intervention still exists.  If the intervention no
            # longer exists, vt will be zero.
            if i <= VariablesRW['NumHerdVaccs']:
                vt = CSGetHerdVaccCurrID(ID)
            
                # If there is data other than zeros (zeros tag does not exist) then read in the data
                if sheet[row, GB_RW_DataStartCol+1] != '<ZEROS>':
                    count = int(sheet[row, GB_RW_DataStartCol+1])
                    row += 1

                    for d in GBRange(1, count):
                        # Retrieve master death id
                        DtMstID = int(sheet[row, GB_RW_DataStartCol+1])
                        DtCurrID = CSGetCurDeathID(DtMstID)
                        
                        row += 1
                        
                        for pc in GBRange(CS_MinPercCov, CS_MaxPercCov):
                            if DtCurrID != 0:
                                for a in GBRange(CS_0t1months, CS_24t60months):
                                    if (vt > 0):
                                        value = float(sheet[row, GB_RW_DataStartCol + 1 + a])
                                        modvar[CS_Data][vt][DtCurrID][pc][a] = value
                            row += 1
                else:
                    row += 1

# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# /////                                                                                                          /////
# /////                                      Impact on food security                                             /////
# /////                                                                                                          /////
# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def import_ImpOnFoodSecurity(sheet, tags, params, projection):
    modvarTagRow = tags.get('<ImpOnFoodSecurity>', None)
    if modvarTagRow:
        modvar = projection[CS_ImpOnFoodSecurityTag]
        
        row = modvarTagRow + 3
        
        numIntervs = int(sheet[row, GB_RW_DataStartCol])
        row += 1

        for r in GBRange(CS_Efficacy, CS_AffecFract):                
            for i in GBRange(CS_FirstIntervForFI, numIntervs + 20):  
                mstID = int(sheet[row, GB_RW_DescriptCol])
                # Used to include Food Shock but no longer
                if mstID != CS_MstFoodShock:
                    curID = CSGetIntervForFICurIdFromMstID(mstID)
                    if curID > 0:
                        modvar[CS_Data][r][curID] = float(sheet[row, GB_RW_DataStartCol])
                row += 1
        
# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# /////                                                                                                          /////
# /////                             Effectiveness of nutrition interventions                                     /////
# /////                                                                                                          /////
# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def import_AgeAndBirthOrder(sheet, tags, params, projection):
    modvarTagRow = tags.get('<Age And Birth Order MV2>', None)
    if modvarTagRow:
        modvar = projection[CS_AgeAndBirthOrderTag]
        row = modvarTagRow + 3
        for r in GBRange(CS_RelRisk, CS_AffecFract):
            for ma in GBRange(CS_AllYrs, CS_35_49Yrs):
                for birthOrder in GBRange(CS_FirstBirth, CS_GTThirdBirth):
                    for term in GBRange(CS_PreTermSGA, CS_TermAGA):
                        modvar[CS_Data][r][ma][birthOrder][term] = float(sheet[row, GB_RW_DataStartCol])
                        row += 1

def import_BirthIntervals(sheet, tags, params, projection):
    modvarTagRow = tags.get('<Birth Intervals MV2>', None)
    if modvarTagRow:
        modvar = projection[CS_BirthIntervalsTag]   
        row = modvarTagRow + 3
        for r in GBRange(CS_RelRisk, CS_AffecFract):
            for i in GBRange(CS_FirstBirth, CS_GE24Mths):
                for term in GBRange(CS_PreTermSGA, CS_TermAGA):
                    modvar[CS_Data][r][i][term] = float(sheet[row, GB_RW_DataStartCol])
                    row += 1

def import_IntervForBO(sheet, tags, params, projection):
    modvarTagRow = tags.get('<Maternal Nutrition MV7>', None)
    if modvarTagRow:
        modvar = projection[CS_IntervForBOTag]
        row = modvarTagRow + 3
        numIntervs = int(sheet[row, GB_RW_DataStartCol])
        row += 1
        for r in GBRange(CS_Efficacy, CS_AdjustedRR):
            for i in GBRange(CS_IPTp, numIntervs + 20):
                curID = CSGetIntervForBOCurIdFromMstID(int(sheet[row, GB_RW_DescriptCol]))
                if i <= numIntervs:
                    for term in GBRange(CS_PreTermSGA, CS_TermAGA):
                        if curID > 0:
                            modvar[CS_Data][r][curID][term] = float(sheet[row, GB_RW_DataStartCol])
                        row += 1
                else:
                    row += 4

def import_ImpactOnStunt(sheet, tags, params, projection):
    modvarTagRow = tags.get('<Impacts On Stunting MV>', None)
    if modvarTagRow:
        modvar = projection[CS_ImpactOnStuntTag]
        row = modvarTagRow + 2
        for i in GBRange(CS_ImpactsOnStuntingFirst, CS_ImpactsOnStuntingFinal):  
            for j in GBRange(CS_OddsRatio, CS_AffecFract):
                for a in GBRange(CS_0t1months, CS_24t60months):
                    modvar[CS_Data][i][j][a] = float(sheet[row, GB_RW_DescriptCol+a])
                row += 1
            row += 1

def import_ImpactOnWaste(sheet, tags, params, projection):
    modvarTagRow = tags.get('<Impacts On Wasting MV4>', None)
    if modvarTagRow:
        modvar = projection[CS_ImpactOnWasteTag]
        row = modvarTagRow + 3
        for i in GBRange(CS_ImpactsOnWaste_Therafeed, CS_ImpactsOnWaste_MAX):           
            for j in GBRange(CS_Efficacy, CS_AffecFract):
                for a in GBRange(CS_0t1months, CS_24t60months):
                    modvar[CS_Data][i][j][a] = float(sheet[row, GB_RW_DataStartCol+a])
                row += 1
            
def import_ImpactOnMatAnemia(sheet, tags, params, projection):
    modvarTagRow = tags.get('<Impacts On Maternal Anemia MV3>', None)
    if modvarTagRow:
        modvar = projection[CS_ImpactOnMatAnemiaTag]
        row = modvarTagRow + 3
        for n in GBRange(CS_Preg, CS_NonPreg):
            for i in GBRange(CS_IronFolatePW_MatAnemia, CS_MAX_MatAnemia):           
                for j in GBRange(CS_Efficacy, CS_AffecFract):
                    modvar[CS_Data][n][i][j] = float(sheet[row, GB_RW_DataStartCol + j - 1])
                row += 1
            
def import_ImpactBFPromo(sheet, tags, params, projection):
    modvarTagRow = tags.get('<ImpactsBFPromotion MV3>', None)
    if modvarTagRow:
        modvar = projection[CS_ImpactBFPromoTag]
        row = modvarTagRow + 3
        for i in GBRange(CS_ImpactPromoBF, CS_ImpactPromoEarlyBF):
            for opt in GBRange(CS_BFPromoHealthSystem, CS_BFPromoBoth):
                for j in GBRange(CS_OddsRatio, CS_AffecFract):
                    for a in GBRange(CS_0t1months, CS_24t60months):
                        modvar[CS_Data][i][opt][j][a] = float(sheet[row, GB_RW_NotesCol+a])
                    row += 1
                
def import_KMConBF(sheet, tags, params, projection):
    modvarTagRow = tags.get('<Kangaroo Mother Care on Breastfeeding MV>', None)
    if modvarTagRow:
        modvar = projection[CS_KMConBFTag]
        row = modvarTagRow + 2
        for j in GBRange(CS_OddsRatio, CS_AffecFract):
            for a in GBRange(CS_0t1months, CS_24t60months):
                modvar[CS_Data][j][a] = float(sheet[row, GB_RW_NotesCol+a])
            row += 1

def import_LBWF(sheet, tags, params, projection):
    modvarTagRow = tags.get('<Low birth weight factor MV2>', None)
    if modvarTagRow:
        modvar = projection[CS_LBWFTag]
        row = modvarTagRow + 3
        for i in GBRange(1, CS_TermAGA):
            modvar[CS_Data][i] = float(sheet[row, GB_RW_NotesCol + i])

def import_ReducStunt(sheet, tags, params, projection):
    modvarTagRow = tags.get('<ReducStunt MV>', None)
    if modvarTagRow:
        modvar = projection[CS_ReducStuntTag]
        row = modvarTagRow + 3
        for j in GBRange(CS_Efficacy, CS_AffecFract):
            modvar[CS_Data][j] = float(sheet[row, GB_RW_DataStartCol])
            row += 1

def import_EducAttain(sheet, tags, params, projection):
    modvarTagRow = tags.get('<EducationAttain MV>', None)
    if modvarTagRow:
        modvar = projection[CS_EducAttainTag]
        row = modvarTagRow + 3
        for j in GBRange(CS_Efficacy, CS_AffecFract):
            modvar[CS_Data][j] = float(sheet[row, GB_RW_DataStartCol])
            row += 1

# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# /////                                                                                                          /////
# /////                              Impact of under-nutrition on mortality                                      /////
# /////                                                                                                          /////
# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def import_RelRisksStunt(sheet, params, projection, VariablesRW):
    modvarTagRow = tags.get('<RelRisksStunting MV>', None)
    if modvarTagRow:
        modvar = projection[CS_RelRisksStuntTag]
        row = modvarTagRow + 2
        for i in GBRange(1, VariablesRW['NumDeathCauses']):
            # Retrieve master death id
            mstID = int(sheet[row, GB_RW_DataStartCol])
            currID = CSGetCurDeathID(mstID)

            row += 1
            for j in GBRange(CS_RelRisk, CS_AffecFract):
                for k in GBRange(CS_GT1STD, CS_GT3STD):                
                    if currID > 0:
                        for a in GBRange(CS_0t1months, CS_24t60months):
                            modvar[CS_Data][currID][j][k][a] = float(sheet[row, GB_RW_DataStartCol+a])
                    row += 1
                row += 1

def import_RelRisksWaste(sheet, params, projection, VariablesRW):
    modvarTagRow = tags.get('<RelRisksWasting MV>', None)
    if modvarTagRow:
        modvar = projection[CS_RelRisksWasteTag]
        row = modvarTagRow + 3
        for i in GBRange(1, VariablesRW['NumDeathCauses']):
            # Retrieve master death id
            mstID = int(sheet[row, GB_RW_DescriptCol])
            currID = CSGetCurDeathID(mstID)

            row += 1
            for j in GBRange(CS_RelRisk, CS_AffecFract):
                for k in GBRange(CS_GT1STD, CS_GT3STD):                
                    if currID > 0:
                        for a in GBRange(CS_0t1months, CS_24t60months):
                            modvar[CS_Data][currID][j][k][a] = float(sheet[row, GB_RW_DescriptCol+a])
                    row += 1

def import_ImpactBFOnMortNeoNat(sheet, tags, params, projection):
    modvarTagRow = tags.get('<ImpactBFOnMortNeoNat MV>', None)
    if modvarTagRow:
        modvar = projection[CS_ImpactBFOnMortNeoNatTag]
        row = modvarTagRow + 2
        for d in GBRange(1, CS_FinalNNDeath):
            # Retrieve master death id
            mstID = int(sheet[row, GB_RW_DataStartCol])
            currID = CSGetCurDeathID(mstID)
            row += 1

            for i in GBRange(CS_RelRisk, CS_AffecFract):
                col = GB_RW_DataStartCol + 1
                for j in GBRange(CS_EarlyInitBF, CS_LateInitBF):
                    for bft in GBRange(CS_ExclusiveBF, CS_NotBF):
                        if currID != 0:
                            val = float(sheet[row, col])
                            # Efficacy values cannot be less than 1. If they are (as is
                            # the case somehow for older projections), set them to 1.
                            if val >= 1:
                                modvar[CS_Data][currID][i][j][bft] = val
                            col += 1
                row += 1

def import_ImpactBFOnMortPostNat(sheet, params, projection, VariablesRW):
    modvarTagRow = tags.get('<ImpactBFOnMort MV>', None)
    if modvarTagRow:
        modvar = projection[CS_ImpactBFOnMortPostNatTag]
        row = modvarTagRow + 2
        for d in GBRange(1, VariablesRW['NumDeathCauses']):
            # Retrieve master death id
            mstID = int(sheet[row, GB_RW_DataStartCol])
            currID = CSGetCurDeathID(mstID)
            row += 1

            for i in GBRange(CS_RelRisk, CS_AffecFract):
                for j in GBRange(CS_ExclusiveBF, CS_NotBF):
                    for a in GBRange(CS_1t6months, CS_24t60months):
                        if currID != 0:
                            val = float(sheet[row, GB_RW_DataStartCol+a])
                            # Efficacy values cannot be less than 1. If they are (as is
                            # the case somehow for older projections), set them to 1.
                            if val >= 1:
                                modvar[CS_Data][currID][i][j][a] = val
                    row += 1

def import_RelRisksIUGR_LBW(sheet, params, projection, VariablesRW):
    modvarTagRow = tags.get('<RelRisksIUGR_LBW MV>', None)
    if modvarTagRow:
        modvar = projection[CS_RelRisksIUGR_LBWTag]
        row = modvarTagRow + 3
        for d in GBRange(1, VariablesRW['NumDeathCauses']):
            # Retrieve master death id
            mstID = int(sheet[row, GB_RW_DescriptCol])
            currID = CSGetCurDeathID(mstID)
            row += 1

            if currID != 0:
                for r in GBRange(CS_PreTermSGA, CS_TermAGA):
                    modvar[CS_Data][currID][r] = float(sheet[row, GB_RW_DataStartCol+r])

def import_RelRisksAnemia(sheet, tags, params, projection):
    modvarTagRow = tags.get('<RelRisksAnemia MV2>', None)
    if modvarTagRow:
        modvar = projection[CS_RelRisksAnemiaTag]
        row = modvarTagRow + 3
        for d in GBRange(CS_Mat_MinDeathCauses, CS_Mat_MaxDeathCauses):
            # Retrieve master death id
            mstID = int(sheet[row, GB_RW_DescriptCol])
            currID = CSGetMat_CurDeathID(mstID)
            row += 1
            for an in GBRange(CS_Mat_NotAnemic, CS_Mat_Anemic):
                if currID > 0:
                    for j in GBRange(CS_RelRisk, CS_AffecFract):
                        modvar[CS_Data][d][an][j] = float(sheet[row, GB_RW_DataStartCol+j-1])
                row += 1