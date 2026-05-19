# fmt: off
from os import environ
import numpy as np
from datetime import datetime

from src._spectrum.AvenirCommon.Util import gb_read_csv_sheet, GBRange, dateTime_fromDelphi, getAllTags


from SpectrumCommon.Modvars.GB.GBDefs import createProjectionParams
from SpectrumCommon.Const.GB import *
from SpectrumCommon.Modvars.GB.GBUtil import *
from SpectrumCommon.Const.DP import *
from SpectrumCommon.Const.AM.AMTags import *
from SpectrumCommon.Modvars.AM.AMUtil import getCustomSAPDataDict
from SpectrumCommon.Modvars.AM.AMModvarDef import HIVSexRatio_Meta_Init
from SpectrumCommon.Const.PJ import *

from src._spectrum.Tools.ImportPJNZ.ImportUtil import getRowOfYearVals, getRowOfYearValsInt, getFloatValue


def getPathInfoDict(IsTotal, FullName):
    return {
        'IsTotal': IsTotal,
        'FullName': FullName,
    }


    
def openDP(file, params : createProjectionParams, projection : dict):

    sheet = gb_read_csv_sheet(file)
    tags = getAllTags(sheet)
    # sheet = _read_csv_sheet(file)
    import_CustomFileYears(sheet, tags, params, projection)
    import_CustomPopStopRescalingYear(sheet, tags, params, projection)
    import_EdAdSource(sheet, tags, params, projection)
    import_ChangesLog(sheet, tags, params, projection)
    import_EdDmSource(sheet, tags, params, projection)
    import_DPSources(sheet, tags, params, projection)

    import_DefaultUPDLE(sheet, tags, params, projection)
    import_DefaultUPDIMR(sheet, tags, params, projection)
    import_DefaultUPDCMR(sheet, tags, params, projection)
    import_DefaultUPDSurvRate(sheet, tags, params, projection)
    import_BigPop(sheet, tags, params, projection)
    import_TFR(sheet, tags, params, projection)
    import_ASFR(sheet, tags, params, projection)
    import_UNPopASFR(sheet, tags, params, projection)
    import_ASFRNum(sheet, tags, params, projection)
    import_ASFRCustomFlag(sheet, tags, params, projection)
    import_SexBirthRatio(sheet, tags, params, projection)
    import_LE(sheet, tags, params, projection)
    import_MigrRate(sheet, tags, params, projection)
    import_MigrAgeDist(sheet, tags, params, projection)
    import_ModelLifeFileName(sheet, tags, params, projection)
    import_UseFYrSingleAges(sheet, tags, params, projection)
    import_RegionalAdjustPopData(sheet, tags, params, projection)
    import_RegionalAdjustPopCBState(sheet, tags, params, projection)
    import_RegionalAdjustPopFName(sheet, tags, params, projection)
    import_RegionalAdjustPopFDate(sheet, tags, params, projection)
    import_LifeTableNum(sheet, tags, params, projection)
    import_SurvRate(sheet, tags, params, projection)
    
    # AM
    if GB_AM in params.modules:
        import_CD4ThreshHold(sheet, tags, params, projection)
        import_PopsEligTreat(sheet, tags, params, projection)
        import_AgeHIVChildOnTreatment(sheet, tags, params, projection)
        import_CD4ThreshHoldAdults(sheet, tags, params, projection)
        import_InfantFeedingOptions(sheet, tags, params, projection)
        import_ARVRegimen(sheet, tags, params, projection)
        import_PatientsReallocated(sheet, tags, params, projection)
        import_PercentARTDelivery(sheet, tags, params, projection)
        import_PregTermAbortionPerNum(sheet, tags, params, projection)
        import_PregTermAbortion(sheet, tags, params, projection)
        import_MedCD4CountInit(sheet, tags, params, projection)
        import_PercLostFollowup(sheet, tags, params, projection)
        import_NumberInitTreatmentReinit(sheet, tags, params, projection)
        import_NumNewlyInitART(sheet, tags, params, projection)
        import_PercLostFollowupChild(sheet, tags, params, projection)
        import_NumberInitTreatmentReinitsChild(sheet, tags, params, projection)
        import_NumNewlyInitARTChild(sheet, tags, params, projection)
        import_HAARTBySex(sheet, tags, params, projection)
        import_HAARTBySexPerNum(sheet, tags, params, projection)
        import_AdultARTAdjFactor(sheet, tags, params, projection)
        import_AdultPatsAllocToFromOtherRegion(sheet, tags, params, projection)
        import_AdultARTAdjFactorFlag(sheet, tags, params, projection)   
        import_CD4Coverage(sheet, tags, params, projection)
        import_ARTByAgeInputType(sheet, tags, params, projection)
        import_ARTByAge5YearAG(sheet, tags, params, projection)
        import_ARTByAgeGAMAG(sheet, tags, params, projection)
        import_CovPopsEligTreat(sheet, tags, params, projection)
        import_ChildTreatInputs(sheet, tags, params, projection)
        import_ChildARTAdjFactor(sheet, tags, params, projection)
        import_ChildARTAdjFactorFlag(sheet, tags, params, projection)
        import_ChildARTByAgeGroupPerNum(sheet, tags, params, projection)
        import_ANCTestingValues(sheet, tags, params, projection)
        # import_NewInfectionsLessImmigrants(sheet, tags, params, projection)
        import_HIVTesting(sheet, tags, params, projection)
        import_HIVTestingHTSTestsByAge(sheet, tags, params, projection)
        import_Shiny90SurveyData(sheet, tags, params, projection)
        import_Shiny90ProgramData(sheet, tags, params, projection)
        import_Shiny90AIDSDeathsFYear(sheet, tags, params, projection)
        import_Shiny90Pop(sheet, tags, params, projection)
        import_Shiny90NumTests(sheet, tags, params, projection)
        import_Shiny90NumTested12M(sheet, tags, params, projection)
        import_Shiny90TotalTests(sheet, tags, params, projection)
        import_Shiny90EverTested(sheet, tags, params, projection)
        import_Shiny90Diagnosed(sheet, tags, params, projection)
        import_Shiny90NumAware(sheet, tags, params, projection)
        import_Shiny90NumDiagnoses(sheet, tags, params, projection)
        import_Shiny90NumDiagnosesMod(sheet, tags, params, projection)
        import_Shiny90NumLateDiagnoses(sheet, tags, params, projection)
        import_Shiny90NotDiagHIV1Yr(sheet, tags, params, projection)
        import_Shiny90NumReTestHIVNeg(sheet, tags, params, projection)
        import_Shiny90NumFirstTestHIVNeg(sheet, tags, params, projection)
        import_Shiny90NumRetestPLHIVOnART(sheet, tags, params, projection)
        import_Shiny90NumRetestPLHIVNoART(sheet, tags, params, projection)
        import_Shiny90NumNewDiagnoses(sheet, tags, params, projection)
        import_Shiny90PosRate(sheet, tags, params, projection)
        import_Shiny90YieldNewDiagn(sheet, tags, params, projection)
        import_Shiny90IsFitted(sheet, tags, params, projection)
        import_KnowledgeOfStatusInputType(sheet, tags, params, projection)
        import_KnowledgeOfStatusInput(sheet, tags, params, projection)
        import_KnowledgeOfStatusFileTitle(sheet, tags, params, projection)
        import_ViralSuppressionInputType(sheet, tags, params, projection)
        import_ViralSuppressionInput(sheet, tags, params, projection)
        import_ViralSuppressionThreshold(sheet, tags, params, projection)
        import_ChildAnnRateProgressLowerCD4(sheet, tags, params, projection)
        import_ChildDistNewInfectionsCD4(sheet, tags, params, projection)
        import_ChildMortByCD4NoART(sheet, tags, params, projection)
        import_ChildMortalityRates(sheet, tags, params, projection)
        import_ChildMortalityRatesMultiplier(sheet, tags, params, projection)
        import_ChildMortByCD4WithART0to6(sheet, tags, params, projection)
        import_ChildMortByCD4WithART7to12(sheet, tags, params, projection)
        import_ChildMortByCD4WithARTGT12(sheet, tags, params, projection)
        import_ChildARTDist(sheet, tags, params, projection)
        import_EffectTreatChild(sheet, tags, params, projection)
        import_ChildWeightBands(sheet, tags, params, projection)
        import_AdultAnnRateProgressLowerCD4(sheet, tags, params, projection)
        import_AdultDistNewInfectionsCD4(sheet, tags, params, projection)
        import_AdultMortByCD4NoART(sheet, tags, params, projection)
        import_AdultInfectReduc(sheet, tags, params, projection)
        import_MortalityRates(sheet, tags, params, projection)
        import_MortalityRatesMultiplier(sheet, tags, params, projection)
        import_AdultMortByCD4WithART0to6(sheet, tags, params, projection)
        import_AdultMortByCD4WithART7to12(sheet, tags, params, projection)
        import_AdultMortByCD4WithARTGT12(sheet, tags, params, projection)
        import_TFRRegion(sheet, tags, params, projection)
        import_HIVTFRCustomFlag(sheet, tags, params, projection)
        import_HIVTFR(sheet, tags, params, projection)
        import_TFRInputType(sheet, tags, params, projection)
        import_FertCD4Discount(sheet, tags, params, projection)
        import_RatioWomenOnART(sheet, tags, params, projection)
        import_FRRFitInput(sheet, tags, params, projection)
        import_FRRbyLocation(sheet, tags, params, projection)
        import_TransEffAssump(sheet, tags, params, projection)
        import_DALYDisabilityWeights(sheet, tags, params, projection)
        import_NewARTPatAlloc(sheet, tags, params, projection)
        import_NewARTPatAllocationMethod(sheet, tags, params, projection)
        import_RiskPopOrphans(sheet, tags, params, projection)
        import_ECDCValues(sheet, tags, params, projection)
        import_ECDCFQName(sheet, tags, params, projection)
        import_NosocomialInfectionsByAge(sheet, tags, params, projection)
        import_HIVMigrantsByAgeSex(sheet, tags, params, projection)
        import_IncidenceInput1970(sheet, tags, params, projection)
        import_CSAVRInputAIDSDeathsSource(sheet, tags, params, projection)
        import_CSAVRInputAIDSDeathsSourceName(sheet, tags, params, projection)
        import_CSAVRInputAIDSDeaths(sheet, tags, params, projection)
        import_CSAVRInputAIDSDeathsBySex(sheet, tags, params, projection)
        import_CSAVRInputAIDSDeathsBySexAge(sheet, tags, params, projection)
        import_CSAVRInputNewDiagnoses(sheet, tags, params, projection)
        import_CSAVRInputNewDiagnosesBySex(sheet, tags, params, projection)
        import_CSAVRInputNewDiagnosesBySexAge(sheet, tags, params, projection)
        import_CSAVRInputNewDiagnosesBySexAgeCD4(sheet, tags, params, projection)
        import_CSAVRInputCD4DistAtDiag(sheet, tags, params, projection)
        import_FitIncidencePopulationValue(sheet, tags, params, projection)
        import_AIDSMortalityAllAges(sheet, tags, params, projection)
        import_AnnualInterruptionRate(sheet, tags, params, projection)
        import_IncreasedLikelihoodOfReinit(sheet, tags, params, projection)
        import_OffARTMortRateMultiplier(sheet, tags, params, projection)
        import_ChildAnnualInterruptionRate(sheet, tags, params, projection)
        import_ChildIncreasedLikelihoodOfReinit(sheet, tags, params, projection)
        import_ChildOffARTMortRateMultiplier(sheet, tags, params, projection)
        import_CSAVRFitOptions(sheet, tags, params, projection)
        import_FitIncidenceParameters(sheet, tags, params, projection)
        import_FitIncidenceIncScaleParameters(sheet, tags, params, projection)
        import_FitIncidenceUncertaintyParams(sheet, tags, params, projection)
        import_CSAVRConstrainPLHIVGTNumART(sheet, tags, params, projection)
        import_FitIncidenceTypeOfFit(sheet, tags, params, projection)
        import_CSAVRAdjustIRRs(sheet, tags, params, projection)
        # import_FitIncidenceFitMethod(sheet, tags, params, projection)
        import_CSAVRMetaData(sheet, tags, params, projection)
        import_MeanCD4atDiagnosis(sheet, tags, params, projection)
        import_MeanCD4atDiagnosisByAgeSex(sheet, tags, params, projection)
        import_TimeInfToDiag(sheet, tags, params, projection)
        import_PropOfDiagnosed(sheet, tags, params, projection)
        import_PropOfDiagnosedNoART(sheet, tags, params, projection)
        import_PropofDiagnosedByAgeSexCD4(sheet, tags, params, projection)
        import_CSAVRNumPLHIV(sheet, tags, params, projection)
        import_CSAVRNumPLHIVByAgeSexCD4(sheet, tags, params, projection)
        import_CSAVRNumDiagnosed(sheet, tags, params, projection)
        import_CSAVRNumDiagnosedByAgeSexCD4(sheet, tags, params, projection)
        import_CSAVRAIDSDeaths(sheet, tags, params, projection)
        import_CSAVRAIDSDeathsByAgeSex(sheet, tags, params, projection)
        import_CSAVRNumNewInfections(sheet, tags, params, projection)
        import_CSAVRIncidenceByFit(sheet, tags, params, projection)
        import_HIVSexRatio(sheet, tags, params, projection)
        import_CSAVRHIVSexRatio(sheet, tags, params, projection)
        import_DistOfHIV(sheet, tags, params, projection)
        import_CSAVRDistOfHIV(sheet, tags, params, projection)

        import_SAPFittingValues(sheet, tags, params, projection)
        
        # import_FittingAICData(sheet, tags, params, projection)
        # import_IRRFittingValues(sheet, tags, params, projection)
        # import_HIVSexRatioFittingValues(sheet, tags, params, projection)

        # import_ARTTreatFittingData(sheet, tags, params, projection)
        # import_ARTTreatFitDistOfHIV(sheet, tags, params, projection)
        # import_ARTTreatFitHIVSexRatio(sheet, tags, params, projection)
        
        import_AIDS45q15(sheet, tags, params, projection)
        import_NonAIDS45q15(sheet, tags, params, projection)
        import_Total45q15(sheet, tags, params, projection)
        import_Under5MortRate(sheet, tags, params, projection)
        import_PMTCTProgEstNeed(sheet, tags, params, projection)
        import_NumberOnART(sheet, tags, params, projection)
        import_ARTCovByAge(sheet, tags, params, projection)
        import_KeyPops(sheet, tags, params, projection)
        import_KeyPopsYear(sheet, tags, params, projection)
        import_KeyPopsFName(sheet, tags, params, projection)
        import_PregWomenPrevRoutineTest(sheet, tags, params, projection)
        import_PregWomenPrev(sheet, tags, params, projection)
        import_PrevSurveyData(sheet, tags, params, projection)
        import_PrevSurveyUsed(sheet, tags, params, projection)
        import_PrevSurveyName(sheet, tags, params, projection)
        import_PrevSurveyYear(sheet, tags, params, projection)
        import_ARTCovSurveyData(sheet, tags, params, projection)
        import_ARTCovSurveyUsed(sheet, tags, params, projection)
        import_ARTCovSurveyName(sheet, tags, params, projection)
        import_ARTCovSurveyYear(sheet, tags, params, projection)
        import_MortRateByAge(sheet, tags, params, projection)
        import_AllCauseMortality(sheet, tags, params, projection)
        import_AIDSMortality(sheet, tags, params, projection)
        import_NumberOnARTByAge(sheet, tags, params, projection)
        import_NewlyStartingART(sheet, tags, params, projection)
        import_AdultsChildrenStartingART(sheet, tags, params, projection)
        import_PercentOfPop(sheet, tags, params, projection)
        import_FirstYearOfEpidemic(sheet, tags, params, projection)
        import_ARTCoverageSelection(sheet, tags, params, projection)
        import_BFYearsRGIdx(sheet, tags, params, projection)
        import_BFArvRGIdx(sheet, tags, params, projection)
        import_ChildHIVMortARTRegion(sheet, tags, params, projection)
        import_ChildHIVMortARTCustomFlag(sheet, tags, params, projection)
        import_ChildARTDistRegion(sheet, tags, params, projection)
        import_ChildARTDistCustomFlag(sheet, tags, params, projection)
        import_AdultProgressRatesRegion(sheet, tags, params, projection)
        import_AdultProgressRatesCustomFlag(sheet, tags, params, projection)
        import_AdultHIVMortNoARTRegion(sheet, tags, params, projection)
        import_AdultHIVMortNoARTCustomFlag(sheet, tags, params, projection)
        import_AdultHIVMortARTRegion(sheet, tags, params, projection)
        import_AdultHIVMortARTCustomFlag(sheet, tags, params, projection)
        import_DALYBaseYear(sheet, tags, params, projection)
        import_DALYDiscountRate(sheet, tags, params, projection)
        import_DALYUseStandardLifeTable(sheet, tags, params, projection)
        import_OrphansRegionalPattern(sheet, tags, params, projection)
        import_IncidenceInput1970Bool(sheet, tags, params, projection)
        import_IncidenceOptions(sheet, tags, params, projection)
        import_IncidenceByFit(sheet, tags, params, projection)
        import_FourDecPlaceID(sheet, tags, params, projection)
        import_EPPPrevAdj(sheet, tags, params, projection)
        import_EPPMaxAdjFactor(sheet, tags, params, projection)
        import_EPPPopulationAges(sheet, tags, params, projection)
        import_CustomSAPDataIndex(sheet, tags, params, projection)
        import_IncEpidemicCustomFlagIdx(sheet, tags, params, projection)
        import_SexRatioFromEPP(sheet, tags, params, projection)
        import_HIVSexRatioFromEPP(sheet, tags, params, projection)
        import_EpidemicTypeFromEPP(sheet, tags, params, projection)
        import_AdultPrevalence(sheet, tags, params, projection)
        import_NumOfEPPEpidemics(sheet, tags, params, projection)
        import_EPPCountryName(sheet, tags, params, projection)
        import_EPPEpiName(sheet, tags, params, projection)
        import_EPPEpidemic(sheet, tags, params, projection)
        import_EPPPrevData(sheet, tags, params, projection)
        import_EPPIncData(sheet, tags, params, projection)
        import_EPPPopData(sheet, tags, params, projection)
        import_EPPSexRatio(sheet, tags, params, projection)
        import_EPPBaseYrPop(sheet, tags, params, projection)
        import_EPPIDUMortality(sheet, tags, params, projection)
        import_EPPPathInfo(sheet, tags, params, projection)
        import_EppAgeRange(sheet, tags, params, projection)
        import_YrPtPrevalence_WB(sheet, tags, params, projection)
        import_AIDSDeathsAmongIDU(sheet, tags, params, projection)
        import_PropIDU_WB(sheet, tags, params, projection)
        import_NonAIDSDeathsAmongIDU(sheet, tags, params, projection)
        import_SexuallyActive15to19(sheet, tags, params, projection)
        import_AIDSMortAllAgesFYrAdjIdx(sheet, tags, params, projection)
        import_ValidationAllCauseDeathsART(sheet, tags, params, projection)
        import_AdvOptsMeningitis(sheet, tags, params, projection)
        import_PrevNeedFirstTime(sheet, tags, params, projection)
        has_prev_need = not projection.get(AM_PreventionNeedsFirstTimeTag, True)
        if has_prev_need:
            import_PrevNeedShowVMMC(sheet, tags, params, projection)
            import_PrevNeedKeyPop(sheet, tags, params, projection)
            import_PrevNeedVMMC(sheet, tags, params, projection)
            import_PrevNeedCondoms(sheet, tags, params, projection)
            import_PrevNeedPrEP_V2(sheet, tags, params, projection)
            import_PrevNeedPrEP_V3(sheet, tags, params, projection)
        # remove the first time flag because data will be loaded
        if AM_PreventionNeedsFirstTimeTag in projection:
            del projection[AM_PreventionNeedsFirstTimeTag]
        import_PrEPParameters(sheet, tags, params, projection)
        import_PrEPForPregnantWomen(sheet, tags, params, projection)
        import_KOSNewDiagnosesAdults15Plus(sheet, tags, params, projection)
        import_KOSNewDiagnosesChildren0to14(sheet, tags, params, projection)
        import_KOSNewDiagnosesRecCD4Test(sheet, tags, params, projection)
    
    # DP_TGX_PrEPParameters_MV                  = '<PrEPParameters MV>';
    # DP_TGX_PrEPForPregnantWomen_MV            = '<PrEPForPregnantWomen MV>';
# AM_PMTCTPrEPParametersTag = '<AM_PMTCTPrEPParameters_V1>'
# AM_PMTCTReceivingOralPrEPTag = '<AM_PMTCTReceivingOralPrEP_V1>'
# AM_PMTCTReceivingLongActingPrEPTag = '<AM_PMTCTReceivingLongActingPrEP_V1>'

    return True

def import_CustomFileYears(sheet, tags, params, projection):
    modvarTagRow = tags.get('<CustomFileYears MV>', None)
    if modvarTagRow is None: return
    modvar = projection[DP_CustomFileYearsTag]

    row = modvarTagRow + 2
    modvar['DP_CPopFirstYr'] = int(sheet[row, GB_RW_DataStartCol])
    modvar['DP_CPopFinalYr'] = int(sheet[row, GB_RW_DataStartCol + 1])

def import_CustomPopStopRescalingYear(sheet, tags, params, projection):
    modvarTagRow = tags.get('<CustomPopStopRescalingYear MV>', None)
    if modvarTagRow is None: return

    row = modvarTagRow + 2
    projection[DP_CustomPopStopRescalingYearTag] = int(sheet[row, GB_RW_DataStartCol])

def import_EdAdSource(sheet, tags, params, projection):
    modvarTagRow = tags.get('<EdAdSource MV>', None)
    if modvarTagRow is None: return
    # projection[AM_EdAdSourceTag] = []
    modvar = projection[PJN_UserSourceTag]

    row = modvarTagRow + 2
    sourceCount = int(sheet[row, GB_RW_DataStartCol])
    sourceCount = min(sourceCount, len(sheet[row]) - 1)
    for col in GBRange(GB_RW_DataStartCol+1, GB_RW_DataStartCol+sourceCount):
        if col <= len(sheet[row]) - 1:
            modvar.append(str(sheet[row, col]))

def import_ChangesLog(sheet, tags, params, projection):  
    modvarTagRow = tags.get('<ChangesLog MV>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_ChangesLogTag]
    
    row = modvarTagRow + 2
    count = int(sheet[row, GB_RW_DataStartCol])
    for s in GBRange(1, count):
        if (GB_RW_DataStartCol + s) < len(sheet[row]):
            modvar.append(str(sheet[row, GB_RW_DataStartCol + s]))

def import_EdDmSource(sheet, tags, params, projection):
    modvarTagRow = tags.get('<EdDmSource MV>', None)
    if modvarTagRow is None: return
    # projection[DP_EdDmSourceTag] = []
    modvar = projection[PJN_UserSourceTag]

    row = modvarTagRow + 2
    sourceCount = int(sheet[row, GB_RW_DataStartCol])
    sourceCount = min(sourceCount, len(sheet[row]) - 1)
    for col in GBRange(GB_RW_DataStartCol+1, GB_RW_DataStartCol+sourceCount):
        if col <= len(sheet[row]) - 1:
            modvar.append(str(sheet[row, col]))

def import_DPSources(sheet, tags, params, projection):
    modvarTagRow = tags.get('<DPSources MV>', None)
    if modvarTagRow is None: return
    modvar = projection[DP_DPSourcesTag]

    row = modvarTagRow + 2
    modvar['Provider'] = sheet[row, GB_RW_DataStartCol]
    modvar['VersionNum'] = sheet[row + 1, GB_RW_DataStartCol]
    
    row += 2
    for i in GBRange(DP_UPD_Pop, DP_UPD_Migration):
      modvar['Sources'][i]['Name'] = sheet[row, GB_RW_DataStartCol]
      modvar['Sources'][i]['Summary'] = sheet[row, GB_RW_DataStartCol + 1]
      modvar['Sources'][i]['Source'] = sheet[row, GB_RW_DataStartCol + 2]
      modvar['Sources'][i]['Date'] = sheet[row, GB_RW_DataStartCol + 3]
      row += 1

def import_Sources(sheet, tags, params, projection):
    modvarTagRow = tags.get('<Sources MV>', None)
    if modvarTagRow is None: return

    row = modvarTagRow + 2

    projection[DP_DataSourceTag] = str(sheet[row, GB_RW_DataStartCol + 1])
    projection[AM_DataSourceTag] = str(sheet[row + 1, GB_RW_DataStartCol + 1])


def import_DefaultUPDLE(sheet, tags, params, projection):    
    modvarTagRow = tags.get('<DefaultUPDLE MV>', None)
    if modvarTagRow is None: return
    modvar = projection[DP_DefaultUPDLETag]

    row = modvarTagRow + 4
    for sex in GBRange(GB_Male, GB_Female):
        values = modvar[sex]
        getRowOfYearVals(sheet, values, params, row)    
        row += 1

def import_DefaultUPDIMR(sheet, tags, params, projection):    
    modvarTagRow = tags.get('<DefaultUPDIMR MV>', None)
    if modvarTagRow is None: return
    modvar = projection[DP_DefaultUPDIMRTag]

    row = modvarTagRow + 4
    for sex in GBRange(GB_Male, GB_Female):
        values = modvar[sex]
        getRowOfYearVals(sheet, values, params, row)    
        row += 1

def import_DefaultUPDCMR(sheet, tags, params, projection):   
    modvarTagRow = tags.get('<DefaultUPDCMR MV>', None)
    if modvarTagRow is None: return
    modvar = projection[DP_DefaultUPDCMRTag]

    row = modvarTagRow + 4
    for sex in GBRange(GB_Male, GB_Female):
        values = modvar[sex]
        getRowOfYearVals(sheet, values, params, row)    
        row += 1

def import_DefaultUPDSurvRate(sheet, tags, params, projection):    
    modvarTagRow = tags.get('<DefaultUPDSurvRate MV>', None)
    if modvarTagRow is None: return
    modvar = projection[DP_DefaultUPDSurvRateTag]

    row = modvarTagRow + 3
    sStart = int(sheet[row, GB_RW_DataStartCol])
    sEnd = int(sheet[row, GB_RW_DataStartCol + 1])
    row += 1
    aStart = int(sheet[row, GB_RW_DataStartCol])
    aEnd = int(sheet[row, GB_RW_DataStartCol + 1])
    row += 1

    for age in GBRange(aStart, aEnd):
        for sex in GBRange(sStart, sEnd):
            values = modvar[age][sex]
            getRowOfYearVals(sheet, values, params, row)    
            row += 1

def import_BigPop(sheet, tags, params, projection):    
    modvarTagRow = tags.get('<BigPop MV3>', None)
    if modvarTagRow is None: return
    modvar = projection[DP_BigPopTag]

    row = modvarTagRow + 3
    
    for sex in GBRange(GB_Male, GB_Female):
        for age in GBRange(0, DP_MaxSingleAges):
            values = modvar[sex][age]
            getRowOfYearVals(sheet, values, params, row, rowIncludesFirstYear = True)    
            row += 1
    
    for age in GBRange(0, DP_MaxSingleAges):
        for year in GBRange(params.firstYear, params.finalYear):
            t = getYearIdx(year, params.firstYear)
            modvar[GB_BothSexes][age][t] = modvar[GB_Male][age][t] + modvar[GB_Female][age][t]

def import_TFR(sheet, tags, params, projection):
    modvarTagRow = tags.get('<TFR MV>', None)
    if modvarTagRow is None: return
    modvar = projection[DP_TFRTag]

    row = modvarTagRow + 2
    values = modvar
    getRowOfYearVals(sheet, values, params, row)    

def import_ASFR(sheet, tags, params, projection):
    modvarTagRow = tags.get('<ASFR MV>', None)
    if modvarTagRow is None: return
    modvar = projection[DP_ASFRTag]

    for year in GBRange(params.firstYear, params.finalYear):
        t = getYearIdx(year, params.firstYear)
        modvar[DP_AllAges][t] = 0

    row = modvarTagRow + 3
    for age in GBRange(DP_A15_19, DP_A45_49):
        values = modvar[age]
        getRowOfYearVals(sheet, values, params, row)  
        row += 1  
        
    for year in GBRange(params.firstYear, params.finalYear):
        t = getYearIdx(year, params.firstYear)
        modvar[DP_AllAges][t] = modvar[DP_AllAges][t] + values[t]

def import_UNPopASFR(sheet, tags, params, projection):
    modvarTagRow = tags.get('<UNPopASFR MV>', None)
    if modvarTagRow is None: return
    modvar = projection[DP_UNPopASFRTag]

    for year in GBRange(params.firstYear, params.finalYear):
        t = getYearIdx(year, params.firstYear)
        modvar[DP_AllAges][t] = 0

    row = modvarTagRow + 3
    for age in GBRange(DP_A15_19, DP_A45_49):
        values = modvar[age]
        getRowOfYearVals(sheet, values, params, row)  
        row += 1  
        
    for year in GBRange(params.firstYear, params.finalYear):
        t = getYearIdx(year, params.firstYear)
        modvar[DP_AllAges][t] = modvar[DP_AllAges][t] + values[t]

def import_ASFRTables(sheet, tags, params, projection):
    modvarTagRow = tags.get('<ASFRTables MV>', None)
    if modvarTagRow is None: return
    modvar = projection[DP_ASFRTablesTag]

    row = modvarTagRow + 2
    for m in GBRange(DP_ASFR_UNAfrica, DP_ASFR_Average):
        for r in GBRange(1, DP_ASFR_NumRows):
            for c in GBRange(1, DP_ASFR_NumCols):
                modvar[m, c, r] = float(sheet[row, GB_RW_DataStartCol + c - 1])
            row += 1

def import_ASFRNum(sheet, tags, params, projection):
    modvarTagRow = tags.get('<ASFRNum MV>', None)
    if modvarTagRow is None: return
    # modvar = projection[DP_ASFRNumTag]
    
    row = modvarTagRow + 2
    value = int(sheet[row, GB_RW_DataStartCol])
    if value != DP_INPUTTED_TABLE:
        projection[DP_ASFRNumTag] = value
            
def import_ASFRCustomFlag(sheet, tags, params, projection):
    modvarTagRow = tags.get('<ASFRCustomFlag MV>', None)
    if modvarTagRow is None: return
    # modvar = projection[DP_ASFRCustomFlagTag]
    
    row = modvarTagRow + 2
    projection[DP_ASFRCustomFlagTag] = bool(int(sheet[row, GB_RW_DataStartCol]))

def import_SexBirthRatio(sheet, tags, params, projection):
    modvarTagRow = tags.get('<SexBirthRatio MV>', None)
    if modvarTagRow is None: return
    modvar = projection[DP_SexBirthRatioTag]

    row = modvarTagRow + 2
    values = modvar
    getRowOfYearVals(sheet, values, params, row)    

def import_LE(sheet, tags, params, projection):   
    modvarTagRow = tags.get('<LE MV2>', None)
    if modvarTagRow is None: return
    modvar = projection[DP_LETag]

    row = modvarTagRow + 3
    for sex in GBRange(GB_Male, GB_Female):
        values = modvar[sex]
        getRowOfYearVals(sheet, values, params, row)    
        row += 1

def import_MigrRate(sheet, tags, params, projection):    
    modvarTagRow = tags.get('<MigrRate MV2>', None)
    if modvarTagRow is None: return
    modvar = projection[DP_MigrRateTag]

    row = modvarTagRow + 4
    values = modvar[GB_Male][DP_AllAges]
    getRowOfYearVals(sheet, values, params, row)    
    
    row += 2
    values = modvar[GB_Female][DP_AllAges]
    getRowOfYearVals(sheet, values, params, row)  

def import_MigrAgeDist(sheet, tags, params, projection):    
    modvarTagRow = tags.get('<MigrAgeDist MV2>', None)
    if modvarTagRow is None: return
    modvar = projection[DP_MigrAgeDistTag]

    row = modvarTagRow + 3
    
    for sex in GBRange(GB_Male, GB_Female):
        for age in GBRange(DP_A0_4, DP_MAX_AGE):
            values = modvar[sex][age]
            getRowOfYearVals(sheet, values, params, row)    
            row += 1

def import_ModelLifeFileName(sheet, tags, params, projection):   
    modvarTagRow = tags.get('<ModelLifeFileName MV2>', None)
    if modvarTagRow is None: return
    # modvar = projection[DP_ModelLifeFileNameTag]

    row = modvarTagRow + 3
    projection[DP_ModelLifeFileNameTag] = str(sheet[row, GB_RW_DataStartCol])

def import_UseFYrSingleAges(sheet, tags, params, projection):   
    modvarTagRow = tags.get('<UseFYrSingleAges MV2>', None)
    if modvarTagRow is None: return
    # modvar = projection[DP_UseFYrSingleAgesTag]

    row = modvarTagRow + 3
    projection[DP_UseFYrSingleAgesTag] = bool(int(sheet[row, GB_RW_DataStartCol]))

def import_RegionalAdjustPopData(sheet, tags, params, projection):    
    modvarTagRow = tags.get('<RegionalAdjustPopData MV2>', None)
    if modvarTagRow is None: return
    modvar = projection[DP_RegionalAdjustPopDataTag]

    row = modvarTagRow + 3
    
    for sex in GBRange(GB_Male, GB_Female):  
        for age in GBRange(0, 80):
            values = modvar[sex][age]
            getRowOfYearVals(sheet, values, params, row)    
            row += 1
        row += 1 # skip total row
    pass

def import_RegionalAdjustPopCBState(sheet, tags, params, projection):   
    modvarTagRow = tags.get('<RegionalAdjustPopCBState MV>', None)
    if modvarTagRow is None: return
    # modvar = projection[DP_RegionalAdjustPopCBStateTag]

    row = modvarTagRow + 2
    projection[DP_RegionalAdjustPopCBStateTag] = bool(int(sheet[row, GB_RW_DataStartCol]))

def import_RegionalAdjustPopFName(sheet, tags, params, projection):   
    modvarTagRow = tags.get('<RegionalAdjustPopFName MV>', None)
    if modvarTagRow is None: return
    # modvar = projection[DP_RegionalAdjustPopFNameTag]

    row = modvarTagRow + 2
    projection[DP_RegionalAdjustPopFNameTag] = str(sheet[row, GB_RW_DataStartCol])

def import_RegionalAdjustPopFDate(sheet, tags, params, projection):   
    modvarTagRow = tags.get('<RegionalAdjustPopFDate MV>', None)
    if modvarTagRow is None: return
    # modvar = projection[DP_RegionalAdjustPopFDateTag]

    row = modvarTagRow + 2
    projection[DP_RegionalAdjustPopFDateTag] = str(sheet[row, GB_RW_DataStartCol])

def import_LifeTableNum(sheet, tags, params, projection):   
    modvarTagRow = tags.get('<LifeTableNum MV2>', None)
    if modvarTagRow is None: return
    # modvar = projection[DP_LifeTableNumTag]

    row = modvarTagRow + 3
    projection[DP_LifeTableNumTag] = int(sheet[row, GB_RW_DataStartCol])

def import_SurvRate(sheet, tags, params, projection):   
    modvarTagRow = tags.get('<SurvRate MV2>', None)
    if modvarTagRow is None: return
    modvar = projection[DP_SurvRateTag]

    row = modvarTagRow + 3
    for sex in GBRange(GB_Male, GB_Female):
        for sr in GBRange(1, 82):
            values = modvar[sr][sex]
            getRowOfYearVals(sheet, values, params, row)    
            row += 1

# AM

def import_CD4ThreshHold(sheet, tags, params, projection):    
    modvarTagRow = tags.get('<CD4ThreshHold MV>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_CD4ThreshHoldTag]

    row = modvarTagRow + 2
    
    for pernum in GBRange(DP_Number, DP_Percent):
        for age in GBRange(DP_AgeLT11Mths, DP_AgeGT5Years):
            values = modvar[pernum][age]
            getRowOfYearVals(sheet, values, params, row)    
            row += 1

def import_PopsEligTreat(sheet, tags, params, projection):    
    modvarTagRow = tags.get('<PopsEligTreat MV>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_PopsEligTreatTag]

    row = modvarTagRow + 3
    
    for pop in GBRange(1, DP_EligTreatPopsMax):
            modvar[pop]['Eligible'] = bool(int(sheet[row, GB_RW_DataStartCol]))
            modvar[pop]['PercentHIV'] = float(sheet[row, GB_RW_DataStartCol + 1])
            modvar[pop]['Year'] = int(sheet[row, GB_RW_DataStartCol + 2])
            row += 1
            
def import_AgeHIVChildOnTreatment(sheet, tags, params, projection):
    modvarTagRow = tags.get('<AgeHIVChildOnTreatment MV>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_AgeHIVChildOnTreatmentTag]

    row = modvarTagRow + 2
    values = modvar
    getRowOfYearVals(sheet, values, params, row)   
            
def import_CD4ThreshHoldAdults(sheet, tags, params, projection):
    modvarTagRow = tags.get('<CD4ThreshHoldAdults MV>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_CD4ThreshHoldAdultsTag]

    row = modvarTagRow + 2
    values = modvar
    getRowOfYearVals(sheet, values, params, row)   

def import_InfantFeedingOptions(sheet, tags, params, projection):    
    modvarTagRow = tags.get('<InfantFeedingOptions MV>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_InfantFeedingOptionsTag]

    row = modvarTagRow + 2
    
    for id in GBRange(DP_NotInPMTCT, DP_InPMTCT):
        for r in GBRange(1, DP_InfantFeedingMths):
            values = modvar[r][id]
            getRowOfYearVals(sheet, values, params, row)    
            row += 1
    pass

def import_ARVRegimen(sheet, tags, params, projection):    
    modvarTagRow = tags.get('<ARVRegimen MV3>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_ARVRegimenTag]
    
    row = modvarTagRow + 2

    #   (* No prophylaxis *)
    values = modvar[DP_PrenatalProphylaxis][DP_NoProphylaxis][DP_Percent]
    getRowOfYearVals(sheet, values, params, row, startCol = GB_RW_DataStartCol + 1)    
    row += 1

    #   (* Single dose nevir *)
    values = modvar[DP_PrenatalProphylaxis][DP_SingleDoseNevir][DP_Number]
    getRowOfYearVals(sheet, values, params, row, startCol = GB_RW_DataStartCol + 1)    
    row += 1
    values = modvar[DP_PrenatalProphylaxis][DP_SingleDoseNevir][DP_Percent]
    getRowOfYearVals(sheet, values, params, row, startCol = GB_RW_DataStartCol + 1)    
    row += 1
    
    #   (* Dual ARV *)
    values = modvar[DP_PrenatalProphylaxis][DP_DualARV][DP_Number]
    getRowOfYearVals(sheet, values, params, row, startCol = GB_RW_DataStartCol + 1)    
    row += 1
    values = modvar[DP_PrenatalProphylaxis][DP_DualARV][DP_Percent]
    getRowOfYearVals(sheet, values, params, row, startCol = GB_RW_DataStartCol + 1)    
    row += 1

    #   (* Option A - maternal *)
    values = modvar[DP_PrenatalProphylaxis][DP_OptA][DP_Number]
    getRowOfYearVals(sheet, values, params, row, startCol = GB_RW_DataStartCol + 1)    
    row += 1
    values = modvar[DP_PrenatalProphylaxis][DP_OptA][DP_Percent]
    getRowOfYearVals(sheet, values, params, row, startCol = GB_RW_DataStartCol + 1)    
    row += 1

    #   (* Option B - triple prophylaxis from 14 weeks *)
    values = modvar[DP_PrenatalProphylaxis][DP_OptB][DP_Number]
    getRowOfYearVals(sheet, values, params, row, startCol = GB_RW_DataStartCol + 1)    
    row += 1
    values = modvar[DP_PrenatalProphylaxis][DP_OptB][DP_Percent]
    getRowOfYearVals(sheet, values, params, row, startCol = GB_RW_DataStartCol + 1)    
    row += 1
    
    #   (* Triple ART started before pregnancy *)
    values = modvar[DP_PrenatalProphylaxis][DP_TripleARTBefPreg][DP_Number]
    getRowOfYearVals(sheet, values, params, row, startCol = GB_RW_DataStartCol + 1)    
    row += 1
    values = modvar[DP_PrenatalProphylaxis][DP_TripleARTBefPreg][DP_Percent]
    getRowOfYearVals(sheet, values, params, row, startCol = GB_RW_DataStartCol + 1)    
    row += 1
    
    #   (* Triple ART started during pregnancy *)
    values = modvar[DP_PrenatalProphylaxis][DP_TripleARTDurPreg][DP_Number]
    getRowOfYearVals(sheet, values, params, row, startCol = GB_RW_DataStartCol + 1)    
    row += 1
    values = modvar[DP_PrenatalProphylaxis][DP_TripleARTDurPreg][DP_Percent]
    getRowOfYearVals(sheet, values, params, row, startCol = GB_RW_DataStartCol + 1)    
    row += 1
   
    #   (* Triple ART started during pregnancy - Late *)
    values = modvar[DP_PrenatalProphylaxis][DP_TripleARTDurPreg_Late][DP_Number]
    getRowOfYearVals(sheet, values, params, row, startCol = GB_RW_DataStartCol + 1)    
    row += 1
    values = modvar[DP_PrenatalProphylaxis][DP_TripleARTDurPreg_Late][DP_Percent]
    getRowOfYearVals(sheet, values, params, row, startCol = GB_RW_DataStartCol + 1)    
    row += 1
    
    #   (* Total *)
    values = modvar[DP_PrenatalProphylaxis][DP_TotalTreat][DP_Number]
    getRowOfYearVals(sheet, values, params, row, startCol = GB_RW_DataStartCol + 1)    
    row += 1
    
    #   (* Postnatal prophylaxis *)
    
    #   (* No prophylaxis *)
    values = modvar[DP_PostnatalProphylaxis][DP_NoProphylaxis][DP_Percent]
    getRowOfYearVals(sheet, values, params, row, startCol = GB_RW_DataStartCol + 1)    
    row += 1
    
    #   (* Option A *)
    values = modvar[DP_PostnatalProphylaxis][DP_OptA][DP_Number]
    getRowOfYearVals(sheet, values, params, row, startCol = GB_RW_DataStartCol + 1)    
    row += 1
    values = modvar[DP_PostnatalProphylaxis][DP_OptA][DP_Percent]
    getRowOfYearVals(sheet, values, params, row, startCol = GB_RW_DataStartCol + 1)    
    row += 1
    
    #   (* Option B *)
    values = modvar[DP_PostnatalProphylaxis][DP_OptB][DP_Number]
    getRowOfYearVals(sheet, values, params, row, startCol = GB_RW_DataStartCol + 1)    
    row += 1
    values = modvar[DP_PostnatalProphylaxis][DP_OptB][DP_Percent]
    getRowOfYearVals(sheet, values, params, row, startCol = GB_RW_DataStartCol + 1)    
    row += 1
    
    #   (* Total *)
    values = modvar[DP_PostnatalProphylaxis][DP_TotalTreat][DP_Number]
    getRowOfYearVals(sheet, values, params, row, startCol = GB_RW_DataStartCol + 1)    
    row += 1

    #   (* Option A *)
    values = modvar[DP_AnnDropPostnatalProph][DP_OptA][DP_Percent]
    getRowOfYearVals(sheet, values, params, row, startCol = GB_RW_DataStartCol + 1)    
    row += 1

    #   (* Option B *)
    values = modvar[DP_AnnDropPostnatalProph][DP_OptB][DP_Percent]
    getRowOfYearVals(sheet, values, params, row, startCol = GB_RW_DataStartCol + 1)    
    row += 1
    
    #   (* ART 0-12 months BF *)
    values = modvar[DP_AnnDropPostnatalProph][DP_ART0_12MthsBF][DP_Percent]
    getRowOfYearVals(sheet, values, params, row, startCol = GB_RW_DataStartCol + 1)    
    row += 1

    #   (* ART 12+ months BF *)
    values = modvar[DP_AnnDropPostnatalProph][DP_ARTGT12MthsBF][DP_Percent]
    getRowOfYearVals(sheet, values, params, row, startCol = GB_RW_DataStartCol + 1)    
    row += 1

def import_PatientsReallocated(sheet, tags, params, projection):
    modvarTagRow = tags.get('<DP_TGX_PatientsReallocated_MV>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_PatientsReallocatedTag]

    row = modvarTagRow + 2
    values = modvar
    getRowOfYearVals(sheet, values, params, row)  

def import_PercentARTDelivery(sheet, tags, params, projection):    
    modvarTagRow = tags.get('<PercentARTDelivery MV>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_PercentARTDeliveryTag]

    row = modvarTagRow + 2
    
    for i in GBRange(DP_OnARTAtDelivery, DP_StartingARTAtDelivery):
        values = modvar[i]
        getRowOfYearVals(sheet, values, params, row)    
        row += 1

def import_PregTermAbortionPerNum(sheet, tags, params, projection):
    modvarTagRow = tags.get('<PregTermAbortionPerNum MV2>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_PregTermAbortionPerNumTag]

    row = modvarTagRow + 2
    values = modvar
    getRowOfYearValsInt(sheet, values, params, row)  

def import_PregTermAbortion(sheet, tags, params, projection):
    modvarTagRow = tags.get('<PregTermAbortion MV3>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_PregTermAbortionTag]

    row = modvarTagRow + 2
    values = modvar
    getRowOfYearVals(sheet, values, params, row)  

def import_MedCD4CountInit(sheet, tags, params, projection):
    modvarTagRow = tags.get('<MedCD4CountInit MV>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_MedCD4CountInitTag]

    row = modvarTagRow + 2
    values = modvar
    getRowOfYearVals(sheet, values, params, row)  

def import_PercLostFollowup(sheet, tags, params, projection):
    modvarTagRow = tags.get('<PercLostFollowup MV>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_PercInterruptedTag]

    row = modvarTagRow + 2
    values = modvar
    getRowOfYearVals(sheet, values, params, row)   

def import_NumberInitTreatmentReinit(sheet, tags, params, projection):
    modvarTagRow = tags.get('<NumberInitTreatmentReinits MV>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_NumberInitTreatmentReinitsTag]

    row = modvarTagRow + 2
    values = modvar
    getRowOfYearVals(sheet, values, params, row)  
    
    for year in GBRange(params.firstYear, DP_FirstYearOfART - 1):
        t = getYearIdx(year, params.firstYear)
        values[t] = 0

def import_NumNewlyInitART(sheet, tags, params, projection):   
    modvarTagRow = tags.get('<NumNewlyInitART MV>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_NumNewlyInitARTTag]

    row = modvarTagRow + 2
    for sex in GBRange(GB_Male, GB_Female):
        values = modvar[sex]
        getRowOfYearVals(sheet, values, params, row)    
        row += 1

def import_PercLostFollowupChild(sheet, tags, params, projection):
    modvarTagRow = tags.get('<PercLostFollowupChild MV>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_PercInterruptedChildTag]

    row = modvarTagRow + 2
    values = modvar
    getRowOfYearVals(sheet, values, params, row)  
    
    for year in GBRange(params.firstYear, DP_FirstYearOfART - 1):
        t = getYearIdx(year, params.firstYear)
        values[t] = 0

def import_NumberInitTreatmentReinitsChild(sheet, tags, params, projection):
    modvarTagRow = tags.get('<NumberInitTreatmentReinitsChild MV>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_NumberInitTreatmentReinitsChildTag]

    row = modvarTagRow + 2
    values = modvar
    getRowOfYearVals(sheet, values, params, row)  
    
    for year in GBRange(params.firstYear, DP_FirstYearOfART - 1):
        t = getYearIdx(year, params.firstYear)
        values[t] = 0

def import_NumNewlyInitARTChild(sheet, tags, params, projection):
    modvarTagRow = tags.get('<NumNewlyInitARTChild MV>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_NumNewlyInitARTChildTag]

    row = modvarTagRow + 2
    values = modvar
    getRowOfYearVals(sheet, values, params, row)  
    
    for year in GBRange(params.firstYear, DP_FirstYearOfART - 1):
        t = getYearIdx(year, params.firstYear)
        values[t] = 0

def import_HAARTBySex(sheet, tags, params, projection):
    modvarTagRow = tags.get('<HAARTBySex MV>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_HAARTBySexTag]

    row = modvarTagRow + 3
    for sex in GBRange(GB_BothSexes, GB_Female):
        values = modvar[sex]
        getRowOfYearVals(sheet, values, params, row)  
        
        for year in GBRange(params.firstYear, DP_FirstYearOfART - 1):
            t = getYearIdx(year, params.firstYear)
            values[t] = 0
        row += 1

def import_HAARTBySexPerNum(sheet, tags, params, projection):
    modvarTagRow = tags.get('<HAARTBySexPerNum MV>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_HAARTBySexPerNumTag]

    row = modvarTagRow + 3
    for sex in GBRange(GB_BothSexes, GB_Female):
        values = modvar[sex]
        getRowOfYearVals(sheet, values, params, row)  
        
        for year in GBRange(params.firstYear, DP_FirstYearOfART - 1):
            t = getYearIdx(year, params.firstYear)
            values[t] = 0 # desktop does not do this.
        row += 1

def import_AdultARTAdjFactor(sheet, tags, params, projection):   
    modvarTagRow = tags.get('<AdultARTAdjFactor>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_AdultARTAdjFactorTag]

    row = modvarTagRow + 3
    for sex in GBRange(GB_Male, GB_Female):
        values = modvar[sex]
        getRowOfYearVals(sheet, values, params, row)    
        row += 1
        
def import_AdultPatsAllocToFromOtherRegion(sheet, tags, params, projection):   
    modvarTagRow = tags.get('<AdultPatsAllocToFromOtherRegion>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_AdultPatsAllocToFromOtherRegionTag]

    row = modvarTagRow + 3
    for sex in GBRange(GB_Male, GB_Female):
        values = modvar[sex]
        getRowOfYearVals(sheet, values, params, row)    
        row += 1

        
        
def import_AdultARTAdjFactorFlag(sheet, tags, params, projection):  
    try: 
        modvarTagRow = tags.get('<AdultARTAdjFactorFlag>', None)
        # modvar = projection[AM_AdultARTAdjFactorFlagTag]
        row = modvarTagRow + 2
        projection[AM_AdultARTAdjFactorFlagTag] = bool(int(sheet[row, GB_RW_DataStartCol]))
    except Exception as e:
        print(f"Error importing AdultARTAdjFactorFlag: {e}")

def import_CD4Coverage(sheet, tags, params, projection):   
    modvarTagRow = tags.get('<CD4Coverage MV2>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_CD4CoverageTag]
    
    row = modvarTagRow + 3

    for perNum in GBRange(DP_CD4Percent, DP_CD4Number):
        for i in GBRange(DP_CD4_GT500, DP_CD4_LT50):
            values = modvar[perNum][i]
            getRowOfYearVals(sheet, values, params, row)    
            row += 1

            for year in GBRange(params.firstYear, DP_FirstYearOfART - 1):
                t = getYearIdx(year, params.firstYear)
                values[t] = 0
        row += 1

def import_ARTByAgeInputType(sheet, tags, params, projection):   
    modvarTagRow = tags.get('<ARTByAgeInputType MV>', None)
    if modvarTagRow is None: return
    # modvar = projection[AM_ARTByAgeInputTypeTag]

    row = modvarTagRow + 2
    projection[AM_ARTByAgeInputTypeTag] = int(sheet[row, GB_RW_DataStartCol])

def import_ARTByAge5YearAG(sheet, tags, params, projection):   
    modvarTagRow = tags.get('<ARTByAge5YearAG MV>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_ARTByAge5YearAGTag]

    row = modvarTagRow + 3
    for sex in GBRange(GB_Male, GB_Female):
        for age in GBRange(DP_A0_4, DP_A80_Up):
            values = modvar[sex][age]
            getRowOfYearVals(sheet, values, params, row)    
            row += 1

            for year in GBRange(params.firstYear, DP_FirstYearOfART - 1):
                t = getYearIdx(year, params.firstYear)
                values[t] = 0

def import_ARTByAgeGAMAG(sheet, tags, params, projection):   
    modvarTagRow = tags.get('<ARTByAgeGAMAG MV>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_ARTByAgeGAMAGTag]

    row = modvarTagRow + 3
    for sex in GBRange(GB_Male, GB_Female):
        for age in GBRange(DP_A0_4, DP_GAMAG_A50Plus):
            values = modvar[sex][age]
            getRowOfYearVals(sheet, values, params, row)    
            row += 1

            for year in GBRange(params.firstYear, DP_FirstYearOfART - 1):
                t = getYearIdx(year, params.firstYear)
                values[t] = 0

def import_CovPopsEligTreat(sheet, tags, params, projection):
    modvarTagRow = tags.get('<CovPopsEligTreat MV>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_CovPopsEligTreatTag]

    row = modvarTagRow + 3
    for pop in GBRange(DP_EligTreatPregnantWomen, DP_EligTreatPopsMax):
        values = modvar[pop]
        getRowOfYearVals(sheet, values, params, row)    
        row += 1

def import_ChildTreatInputs(sheet, tags, params, projection):
    modvarTagRow = tags.get('<ChildTreatInputs MV3>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_ChildTreatInputsTag]

    initValues = modvar.copy()
    row = modvarTagRow + 2
    for id in GBRange(DP_PerChildHIVPosCot, DP_PerChildHIVRecART10_14):
        values = modvar[id]
        getRowOfYearVals(sheet, values, params, row)    
        row += 1

def import_ChildARTAdjFactor(sheet, tags, params, projection):
    modvarTagRow = tags.get('<ChildARTAdjFactor MV>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_ChildARTAdjFactorTag]

    row = modvarTagRow + 2
    values = modvar
    getRowOfYearVals(sheet, values, params, row)  

def import_ChildARTAdjFactorFlag(sheet, tags, params, projection):  
    try: 
        modvarTagRow = tags.get('<ChildARTAdjFactorFlag>', None)

        row = modvarTagRow + 2
        projection[AM_ChildARTAdjFactorFlagTag] = bool(int(sheet[row, GB_RW_DataStartCol]))
    except Exception as e:
        print(f"Error importing ChildARTAdjFactorFlag: {e}")

def import_ChildARTByAgeGroupPerNum(sheet, tags, params, projection):
    modvarTagRow = tags.get('<ChildARTByAgeGroupPerNum MV2>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_ChildARTByAgeGroupPerNumTag]

    row = modvarTagRow + 2
    for id in GBRange(DP_PerChildHIVPosCot, DP_PerChildHIVRecART10_14):
        values = modvar[id]
        getRowOfYearVals(sheet, values, params, row)    
        row += 1

def import_ANCTestingValues(sheet, tags, params, projection):
    modvarTagRow = tags.get('<ANCTestingValues MV4>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_ANCTestingValuesTag]

    row = modvarTagRow + 2
    for id in GBRange(DP_FirstANCVisits, DP_HIVNegFirstANCVisit):
        values = modvar[id]
        getRowOfYearVals(sheet, values, params, row)    
        row += 1

# def import_NewInfectionsLessImmigrants(sheet, tags, params, projection):   
#     modvarTagRow = tags.get('<NewInfectionsLessImmigrants MV>', None)
#     if modvarTagRow is None: return
#     modvar = projection[AM_NewInfectionsLessImmigrantsTag]

#     row = modvarTagRow + 3
#     for sex in GBRange(GB_BothSexes, GB_Female):
#         values = np.zeros(params.finalYear - params.firstYear + 1).tolist()  #old all single-ages sum row
#         getRowOfYearVals(sheet, values, params, row)    
#         row += 1

#         for age in GBRange(0, 80):
#             values = modvar[sex][age]
#             getRowOfYearVals(sheet, values, params, row)    
#             row += 1
            
def import_HIVTesting(sheet, tags, params, projection):   
    # It was requested that we support both V2 and V3 for this modvar when importing desktop projections
    try:
        modvarTagRowV2 = tags.get('<HIVTesting MV2>', None)
        modvar = projection[AM_HIVTestingTag]

        row = modvarTagRowV2 + 2
                                                #non-calcstate projection or no 'first-year' values imported
        col = 3
        for year in GBRange(params.firstYear, params.finalYear):
            t = getYearIdx(year, params.firstYear)
            if not sheet[row, col] == '':
                modvar[t]['DiagTests'] = getFloatValue(sheet, row, col, DPNotAvail)
                modvar[t]['PosTests'] = getFloatValue(sheet, row + 1, col, DPNotAvail)
                modvar[t]['HTSTests'] = getFloatValue(sheet, row + 2, col, DPNotAvail)
                modvar[t]['PosHTSTests'] = getFloatValue(sheet, row + 3, col, DPNotAvail)
                modvar[t]['ANCTests'] = getFloatValue(sheet, row + 4, col, DPNotAvail)
                modvar[t]['PosANCTests'] = getFloatValue(sheet, row + 5, col, DPNotAvail)
                modvar[t]['SelfTests'] = getFloatValue(sheet, row + 6, col, DPNotAvail)
                # Old fields which are no longer supported
                # modvar[t]['AssistedSelfTests'] = getFloatValue(sheet, row + 7, col, DPNotAvail)
                # modvar[t]['UnassistedSelfTests'] = getFloatValue(sheet, row + 8, col, DPNotAvail)
                # modvar[t]['AssistedPosReactiveSelfTests'] = getFloatValue(sheet, row + 9, col, DPNotAvail)
                # modvar[t]['PrimarySelfTests'] = getFloatValue(sheet, row + 10, col, DPNotAvail)
                # modvar[t]['SecondarySelfTests'] = getFloatValue(sheet, row + 11, col, DPNotAvail)
                # modvar[t]['PosHTSTestsWPrevReactiveSelfTest'] = getFloatValue(sheet, row + 12, col, DPNotAvail)
                # modvar[t]['IndexPartnerTests'] = getFloatValue(sheet, row + 13, col, DPNotAvail)
                # modvar[t]['PosIndexPartnerTests'] = getFloatValue(sheet, row + 14, col, DPNotAvail)
            col += 1
    except Exception as e:
        print(f"Error importing HIVTesting MV2: {e}")
    
    modvarTagRowV3 = tags.get('<HIVTesting MV3>', None)
    if (modvarTagRowV3 ==None): return
    modvar = projection[AM_HIVTestingTag]

    row = modvarTagRowV3 + 3
                                              #non-calcstate projection or no 'first-year' values imported
    col = 3
    for year in GBRange(params.firstYear, params.finalYear):
        t = getYearIdx(year, params.firstYear)
        if not sheet[row, col] == '':
            modvar[t]['DiagTests'] = getFloatValue(sheet, row, col, DPNotAvail)
            modvar[t]['PosTests'] = getFloatValue(sheet, row + 1, col, DPNotAvail)
            modvar[t]['HTSTests'] = getFloatValue(sheet, row + 2, col, DPNotAvail)
            modvar[t]['PosHTSTests'] = getFloatValue(sheet, row + 3, col, DPNotAvail)
            modvar[t]['ANCTests'] = getFloatValue(sheet, row + 4, col, DPNotAvail)
            modvar[t]['PosANCTests'] = getFloatValue(sheet, row + 5, col, DPNotAvail)
            modvar[t]['CommunityBasedTests'] = getFloatValue(sheet, row + 6, col, DPNotAvail)
            modvar[t]['CommunityBasedTestsHIVPos'] = getFloatValue(sheet, row + 7, col, DPNotAvail)
            modvar[t]['SelfTests'] = getFloatValue(sheet, row + 8, col, DPNotAvail)
            modvar[t]['TestsChild0t14'] = getFloatValue(sheet, row + 9, col, DPNotAvail)
            modvar[t]['TestsMen15Plus'] = getFloatValue(sheet, row + 10, col, DPNotAvail)
            modvar[t]['TestsFemale15Plus'] = getFloatValue(sheet, row + 11, col, DPNotAvail)
            modvar[t]['TestsTrans15Plus'] = getFloatValue(sheet, row + 12, col, DPNotAvail)
            modvar[t]['TestsHIVPosChild0t14'] = getFloatValue(sheet, row + 13, col, DPNotAvail)
            modvar[t]['TestsHIVPosMen15Plus'] = getFloatValue(sheet, row + 14, col, DPNotAvail)
            modvar[t]['TestsHIVPosFemale15Plus'] = getFloatValue(sheet, row + 15, col, DPNotAvail)
            modvar[t]['TestsHIVPosTrans15Plus'] = getFloatValue(sheet, row + 16, col, DPNotAvail)
        col += 1
    pass

def import_HIVTestingHTSTestsByAge(sheet, tags, params, projection):   
    modvarTagRow = tags.get('<HIVTestingHTSTestsByAge MV>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_HIVTestingHTSTestsByAgeTag]

    row = modvarTagRow + 3

    for s in GBRange(GB_Male, GB_Female):
        for a in GBRange(DP_AllAges, DP_GAMAG_A50Plus):
            values = modvar[s][a]
            getRowOfYearVals(sheet, values, params, row)    
            row += 1

def import_Shiny90SurveyData(sheet, tags, params, projection):
    modvarTagRow = tags.get('<Shiny90SurveyData MV>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_Shiny90SurveyDataTag]
    emptyEntry = projection[AM_Shiny90SurveyData_MetaTag]['default']
    
    row = modvarTagRow + 2
    count = int(sheet[row, GB_RW_NotesCol])
    row += 1
    for s in GBRange(1, count):
        modvar.append(emptyEntry.copy())
        modvar[-1]['isUsed']        = bool(int(sheet[row, 1]))
        modvar[-1]['surveyID']      = sheet[row, 2]
        modvar[-1]['year']          = int(sheet[row, 3])
        modvar[-1]['ageGroup']      = int(sheet[row, 4])
        modvar[-1]['sex']           = int(sheet[row, 5])
        modvar[-1]['HIVStatus']     = int(sheet[row, 6])
        modvar[-1]['estimate']      = float(sheet[row, 7])
        modvar[-1]['standardError'] = float(sheet[row, 8])
        modvar[-1]['lowerBound']    = float(sheet[row, 9])
        modvar[-1]['upperBound']    = float(sheet[row, 10])
        modvar[-1]['count']         = int(sheet[row, 11])
        row += 1

def import_Shiny90ProgramData(sheet, tags, params, projection):
    modvarTagRow = tags.get('<Shiny90ProgramData MV>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_Shiny90ProgramDataTag]
    emptyEntry = projection[AM_Shiny90ProgramData_MetaTag]['default']
    
    row = modvarTagRow + 2
    count = int(sheet[row, GB_RW_NotesCol])
    row += 1
    for s in GBRange(1, count):
        modvar.append(emptyEntry.copy())
        modvar[-1]['isUsed']            = bool(int(sheet[row, 1]))
        modvar[-1]['year']              = int(sheet[row, 2])
        modvar[-1]['sex']               = int(sheet[row, 3])
        modvar[-1]['totalTests']        = int(sheet[row, 4])
        modvar[-1]['totalPosTests']     = float(sheet[row, 5])
        modvar[-1]['totalHTCTests']     = float(sheet[row, 6])
        modvar[-1]['totalPosHTCTests']  = float(sheet[row, 7])
        modvar[-1]['totalANCTests']     = float(sheet[row, 8])
        modvar[-1]['totalPosANCTests']  = int(sheet[row, 9])
        row += 1

def import_Shiny90AIDSDeathsFYear(sheet, tags, params, projection):   
    modvarTagRow = tags.get('<Shiny90AIDSDeathsFYear MV>', None)
    if modvarTagRow is None: return

    row = modvarTagRow + 2
    projection[AM_Shiny90AIDSDeathsFYearTag] = int(sheet[row, GB_RW_DataStartCol])

def import_Shiny90Pop(sheet, tags, params, projection):
    modvarTagRow = tags.get('<Shiny90Pop MV>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_Shiny90PopTag]

    row = modvarTagRow + 2
    for HIV in GBRange(DP_D_All, DP_D_HIVPos):
        for sex in GBRange(GB_BothSexes, GB_Female):
            for age in GBRange(DP_S90_15_24, DP_S90_15Plus):
                for dataType in GBRange(DP_Number, DP_UpperBound):
                    values = modvar[HIV][sex][age][dataType]
                    getRowOfYearVals(sheet, values, params, row)    
                    row += 1

def import_Shiny90NumTests(sheet, tags, params, projection):
    modvarTagRow = tags.get('<Shiny90NumTests MV>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_Shiny90NumTestsTag]

    row = modvarTagRow + 2
    for HIV in GBRange(DP_D_All, DP_D_HIVPos):
        for sex in GBRange(GB_BothSexes, GB_Female):
            for age in GBRange(DP_S90_15_24, DP_S90_15Plus):
                for dataType in GBRange(DP_Number, DP_UpperBound):
                    values = modvar[HIV][sex][age][dataType]
                    getRowOfYearVals(sheet, values, params, row)    
                    row += 1

def import_Shiny90NumTested12M(sheet, tags, params, projection):
    modvarTagRow = tags.get('<Shiny90NumTested12M MV>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_Shiny90NumTested12MTag]

    row = modvarTagRow + 2
    for HIV in GBRange(DP_D_All, DP_D_HIVPos):
        for sex in GBRange(GB_BothSexes, GB_Female):
            for age in GBRange(DP_S90_15_24, DP_S90_15Plus):
                for dataType in GBRange(DP_Number, DP_UpperBound):
                    values = modvar[HIV][sex][age][dataType]
                    getRowOfYearVals(sheet, values, params, row)    
                    row += 1

def import_Shiny90TotalTests(sheet, tags, params, projection):
    modvarTagRow = tags.get('<Shiny90TotalTests MV>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_Shiny90TotalTestsTag]

    row = modvarTagRow + 2
    for HIV in GBRange(DP_D_All, DP_D_HIVPos):
        for sex in GBRange(GB_BothSexes, GB_Female):
            for age in GBRange(DP_S90_15_24, DP_S90_15Plus):
                for dataType in GBRange(DP_Number, DP_UpperBound):
                    values = modvar[HIV][sex][age][dataType]
                    getRowOfYearVals(sheet, values, params, row)    
                    row += 1

def import_Shiny90EverTested(sheet, tags, params, projection):
    modvarTagRow = tags.get('<Shiny90EverTested MV>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_Shiny90EverTestedTag]

    row = modvarTagRow + 2
    for HIV in GBRange(DP_D_All, DP_D_HIVPos):
        for sex in GBRange(GB_BothSexes, GB_Female):
            for age in GBRange(DP_S90_15_24, DP_S90_15Plus):
                for dataType in GBRange(DP_Number, DP_UpperBound):
                    values = modvar[HIV][sex][age][dataType]
                    getRowOfYearVals(sheet, values, params, row)    
                    row += 1

def import_Shiny90Diagnosed(sheet, tags, params, projection):
    modvarTagRow = tags.get('<Shiny90Diagnosed MV>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_Shiny90DiagnosedTag]

    row = modvarTagRow + 2
    for HIV in GBRange(DP_D_All, DP_D_HIVPos):
        for sex in GBRange(GB_BothSexes, GB_Female):
            for age in GBRange(DP_S90_15_24, DP_S90_15Plus):
                for dataType in GBRange(DP_Number, DP_UpperBound):
                    values = modvar[HIV][sex][age][dataType]
                    getRowOfYearVals(sheet, values, params, row)    
                    row += 1

def import_Shiny90NumAware(sheet, tags, params, projection):
    modvarTagRow = tags.get('<Shiny90NumberAware MV>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_Shiny90NumAwareTag]

    row = modvarTagRow + 2
    for HIV in GBRange(DP_D_All, DP_D_HIVPos):
        for sex in GBRange(GB_BothSexes, GB_Female):
            for age in GBRange(DP_S90_15_24, DP_S90_15Plus):
                for dataType in GBRange(DP_Number, DP_UpperBound):
                    values = modvar[HIV][sex][age][dataType]
                    getRowOfYearVals(sheet, values, params, row)    
                    row += 1

def import_Shiny90NumDiagnoses(sheet, tags, params, projection):
    modvarTagRow = tags.get('<Shiny90NumDiagnoses MV>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_Shiny90NumDiagnosesTag]

    row = modvarTagRow + 2
    for HIV in GBRange(DP_D_All, DP_D_HIVPos):
        for sex in GBRange(GB_BothSexes, GB_Female):
            for age in GBRange(DP_S90_15_24, DP_S90_15Plus):
                for dataType in GBRange(DP_Number, DP_UpperBound):
                    values = modvar[HIV][sex][age][dataType]
                    getRowOfYearVals(sheet, values, params, row)    
                    row += 1

def import_Shiny90NumDiagnosesMod(sheet, tags, params, projection):
    modvarTagRow = tags.get('<Shiny90NumDiagnosesMod MV>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_Shiny90NumDiagnosesModTag]

    row = modvarTagRow + 2
    for HIV in GBRange(DP_D_All, DP_D_HIVPos):
        for sex in GBRange(GB_BothSexes, GB_Female):
            for age in GBRange(DP_S90_15_24, DP_S90_15Plus):
                for dataType in GBRange(DP_Number, DP_UpperBound):
                    values = modvar[HIV][sex][age][dataType]
                    getRowOfYearVals(sheet, values, params, row)    
                    row += 1

def import_Shiny90NumLateDiagnoses(sheet, tags, params, projection):
    modvarTagRow = tags.get('<Shiny90NumLateDiagnoses MV>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_Shiny90NumLateDiagnosesTag]

    row = modvarTagRow + 2
    for HIV in GBRange(DP_D_All, DP_D_HIVPos):
        for sex in GBRange(GB_BothSexes, GB_Female):
            for age in GBRange(DP_S90_15_24, DP_S90_15Plus):
                for dataType in GBRange(DP_Number, DP_UpperBound):
                    values = modvar[HIV][sex][age][dataType]
                    getRowOfYearVals(sheet, values, params, row)    
                    row += 1

def import_Shiny90NotDiagHIV1Yr(sheet, tags, params, projection):
    modvarTagRow = tags.get('<Shiny90NotDiagHIV1Yr MV>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_Shiny90NotDiagHIV1YrTag]

    row = modvarTagRow + 2
    for HIV in GBRange(DP_D_All, DP_D_HIVPos):
        for sex in GBRange(GB_BothSexes, GB_Female):
            for age in GBRange(DP_S90_15_24, DP_S90_15Plus):
                for dataType in GBRange(DP_Number, DP_UpperBound):
                    values = modvar[HIV][sex][age][dataType]
                    getRowOfYearVals(sheet, values, params, row)    
                    row += 1

def import_Shiny90NumReTestHIVNeg(sheet, tags, params, projection):
    modvarTagRow = tags.get('<Shiny90NumReTestHIVNeg MV>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_Shiny90NumReTestHIVNeg_Tag]

    row = modvarTagRow + 2
    for HIV in GBRange(DP_D_All, DP_D_HIVPos):
        for sex in GBRange(GB_BothSexes, GB_Female):
            for age in GBRange(DP_S90_15_24, DP_S90_15Plus):
                for dataType in GBRange(DP_Number, DP_UpperBound):
                    values = modvar[HIV][sex][age][dataType]
                    getRowOfYearVals(sheet, values, params, row)    
                    row += 1

def import_Shiny90NumFirstTestHIVNeg(sheet, tags, params, projection):
    modvarTagRow = tags.get('<Shiny90NumFirstTestHIVNeg MV>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_Shiny90NumFirstTestHIVNeg_Tag]

    row = modvarTagRow + 2
    for HIV in GBRange(DP_D_All, DP_D_HIVPos):
        for sex in GBRange(GB_BothSexes, GB_Female):
            for age in GBRange(DP_S90_15_24, DP_S90_15Plus):
                for dataType in GBRange(DP_Number, DP_UpperBound):
                    values = modvar[HIV][sex][age][dataType]
                    getRowOfYearVals(sheet, values, params, row)    
                    row += 1


def import_Shiny90NumRetestPLHIVOnART(sheet, tags, params, projection):
    modvarTagRow = tags.get('<Shiny90NumRetestPLHIVOnART MV>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_Shiny90NumRetestPLHIVOnART_Tag]

    row = modvarTagRow + 2
    for HIV in GBRange(DP_D_All, DP_D_HIVPos):
        for sex in GBRange(GB_BothSexes, GB_Female):
            for age in GBRange(DP_S90_15_24, DP_S90_15Plus):
                for dataType in GBRange(DP_Number, DP_UpperBound):
                    values = modvar[HIV][sex][age][dataType]
                    getRowOfYearVals(sheet, values, params, row)    
                    row += 1


def import_Shiny90NumRetestPLHIVNoART(sheet, tags, params, projection):
    modvarTagRow = tags.get('<Shiny90NumRetestPLHIVNoART MV>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_Shiny90NumRetestPLHIVNoART_Tag]

    row = modvarTagRow + 2
    for HIV in GBRange(DP_D_All, DP_D_HIVPos):
        for sex in GBRange(GB_BothSexes, GB_Female):
            for age in GBRange(DP_S90_15_24, DP_S90_15Plus):
                for dataType in GBRange(DP_Number, DP_UpperBound):
                    values = modvar[HIV][sex][age][dataType]
                    getRowOfYearVals(sheet, values, params, row)    
                    row += 1


def import_Shiny90NumNewDiagnoses(sheet, tags, params, projection):
    modvarTagRow = tags.get('<Shiny90NumNewDiagnoses MV>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_Shiny90NumNewDiagnoses_Tag]

    row = modvarTagRow + 2
    for HIV in GBRange(DP_D_All, DP_D_HIVPos):
        for sex in GBRange(GB_BothSexes, GB_Female):
            for age in GBRange(DP_S90_15_24, DP_S90_15Plus):
                for dataType in GBRange(DP_Number, DP_UpperBound):
                    values = modvar[HIV][sex][age][dataType]
                    getRowOfYearVals(sheet, values, params, row)    
                    row += 1


def import_Shiny90PosRate(sheet, tags, params, projection):
    modvarTagRow = tags.get('<Shiny90PosRate MV>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_Shiny90PosRate_Tag]

    row = modvarTagRow + 2
    for HIV in GBRange(DP_D_All, DP_D_HIVPos):
        for sex in GBRange(GB_BothSexes, GB_Female):
            for age in GBRange(DP_S90_15_24, DP_S90_15Plus):
                for dataType in GBRange(DP_Number, DP_UpperBound):
                    values = modvar[HIV][sex][age][dataType]
                    getRowOfYearVals(sheet, values, params, row)    
                    row += 1


def import_Shiny90YieldNewDiagn(sheet, tags, params, projection):
    modvarTagRow = tags.get('<Shiny90YieldNewDiagn MV>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_Shiny90YieldNewDiagn_Tag]

    row = modvarTagRow + 2
    for HIV in GBRange(DP_D_All, DP_D_HIVPos):
        for sex in GBRange(GB_BothSexes, GB_Female):
            for age in GBRange(DP_S90_15_24, DP_S90_15Plus):
                for dataType in GBRange(DP_Number, DP_UpperBound):
                    values = modvar[HIV][sex][age][dataType]
                    getRowOfYearVals(sheet, values, params, row)    
                    row += 1

def import_Shiny90IsFitted(sheet, tags, params, projection):   
    modvarTagRow = tags.get('<Shiny90IsFitted MV>', None)
    if modvarTagRow is None: return

    row = modvarTagRow + 2
    projection[AM_Shiny90IsFittedTag] = bool(int(sheet[row, GB_RW_DataStartCol]))

def import_KnowledgeOfStatusInputType(sheet, tags, params, projection):   
    modvarTagRow = tags.get('<KnowledgeOfStatusInputType MV2>', None)
    if modvarTagRow is None: return
    # modvar = projection[AM_KnowledgeOfStatusInputTypeTag]

    row = modvarTagRow + 2
    projection[AM_KnowledgeOfStatusInputTypeTag] = int(sheet[row, GB_RW_DataStartCol])

def import_KnowledgeOfStatusInput(sheet, tags, params, projection):   
    modvarTagRow = tags.get('<KnowledgeOfStatusInput MV4>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_KnowledgeOfStatusInputTag]

    row = modvarTagRow + 2
    for ageGroup in GBRange(DP_Cas_AG_Child, DP_Cas_AG_AdultFemale):
        values = modvar[ageGroup]
        getRowOfYearVals(sheet, values, params, row)    
        # for year in GBRange(DP_Cas_2010, DP_Cas_2025):
        #     modvar[ageGroup][year] = float(sheet[row, GB_RW_DataStartCol + year])
        row += 1

def import_KnowledgeOfStatusFileTitle(sheet, tags, params, projection):   
    modvarTagRow = tags.get('<KnowledgeOfStatusFileTitle MV>', None)
    if modvarTagRow is None: return
    # modvar = projection[AM_KnowledgeOfStatusFileTitleTag]

    row = modvarTagRow + 2
    projection[AM_KnowledgeOfStatusFileTitleTag] = str(sheet[row, GB_RW_DataStartCol])

def import_ViralSuppressionInputType(sheet, tags, params, projection):   
    modvarTagRow = tags.get('<ViralSuppressionInputType MV2>', None)
    if modvarTagRow is None: return
    # modvar = projection[AM_ViralSuppressionInputTypeTag]

    row = modvarTagRow + 2
    projection[AM_ViralSuppressionInputTypeTag] = int(sheet[row, GB_RW_DataStartCol])

def import_ViralSuppressionInput(sheet, tags, params, projection):   
    modvarTagRow = tags.get('<ViralSuppressionInput MV4>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_ViralSuppressionInputTag]

    row = modvarTagRow + 2
    for ageGroup in GBRange(DP_Cas_AG_Child, DP_Cas_AG_AdultFemale):
        for dataType in GBRange(DP_VS_NumOnART, DP_VS_PLHIVSuppressed):
            values = modvar[ageGroup][dataType]
            getRowOfYearVals(sheet, values, params, row)    
            # for year in GBRange(DP_Cas_2010, DP_Cas_2025):
            #     modvar[ageGroup][dataType][year] = float(sheet[row, GB_RW_DataStartCol + year])
            row += 1

def import_ViralSuppressionThreshold(sheet, tags, params, projection):   
    modvarTagRow = tags.get('<ViralSuppressionThreshold MV4>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_ViralSuppressionThresholdTag]

    row = modvarTagRow + 2
    values = modvar
    getRowOfYearVals(sheet, values, params, row)  
    # for year in GBRange(DP_Cas_2010, DP_Cas_2025):
    #     modvar[year] = float(sheet[row, GB_RW_DataStartCol + year])

def import_ChildAnnRateProgressLowerCD4(sheet, tags, params, projection):   
    modvarTagRow = tags.get('<ChildAnnRateProgressLowerCD4 MV2>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_ChildAnnRateProgressLowerCD4Tag]

    row = modvarTagRow + 3
    for sex in GBRange(GB_Male, GB_Female):
        col = 0
        for a in GBRange(DP_A0t2, DP_A5t14):
            for c in GBRange(DP_CD4_Per_GT30, DP_CD4_Per_5_10):
                modvar[DP_Data][sex][a][c] = float(sheet[row, GB_RW_DataStartCol + col])
                col += 1
        row += 1

def import_ChildDistNewInfectionsCD4(sheet, tags, params, projection):   
    modvarTagRow = tags.get('<ChildDistNewInfectionsCD4 MV>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_ChildDistNewInfectionsCD4Tag]

    row = modvarTagRow + 2
    col = 0
    for c in GBRange(DP_CD4_Per_GT30, DP_CD4_Per_LT5):
        modvar[DP_Data][c] = float(sheet[row, GB_RW_DataStartCol + col])
        col += 1

def import_ChildMortByCD4NoART(sheet, tags, params, projection):   
    modvarTagRow = tags.get('<ChildMortByCD4NoART MV2>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_ChildMortByCD4NoARTTag]

    row = modvarTagRow + 2
    for a in GBRange(DP_A0t2, DP_A5t14):
        for b in GBRange(DP_P_Perinatal, DP_P_BF12):
            col = 0
            for c in GBRange(DP_CD4_Per_GT30, DP_CD4_Per_LT5):
                modvar[DP_Data][a][b][c] = float(sheet[row, GB_RW_DataStartCol + col])
                col += 1
            row += 1

def import_ChildMortalityRates(sheet, tags, params, projection):   
    modvarTagRow = tags.get('<ChildMortalityRates MV2>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_ChildMortalityRatesTag]

    row = modvarTagRow + 2
    for age in GBRange(DP_CD4_0t4, DP_CD4_5t14):
        for timePeriod in GBRange(DP_MortRates_LT12Mo, DP_MortRates_GT12Mo):
            values = modvar[DP_Data][age][timePeriod]
            getRowOfYearVals(sheet, values, params, row)    
            row += 1

def import_ChildMortalityRatesMultiplier(sheet, tags, params, projection):   
    modvarTagRow = tags.get('<ChildMortalityRatesMultiplier MV>', None)
    if modvarTagRow is None: return
    # modvar = projection[AM_ChildMortalityRatesMultiplierTag]

    row = modvarTagRow + 2
    projection[AM_ChildMortalityRatesMultiplierTag] = float(sheet[row, GB_RW_DataStartCol])

def import_ChildMortByCD4WithART0to6(sheet, tags, params, projection):   
    modvarTagRow = tags.get('<ChildMortByCD4WithART0to6 MV2>', None)
    if modvarTagRow is None: return
    modvarCount = projection[AM_ChildMortByCD4WithART0to6Tag]
    modvarPerc = projection[AM_ChildMortByCD4WithART0to6PercTag]

    row = modvarTagRow + 2
    for sex in GBRange(GB_Male, GB_Female):
        col = 0
        for a in GBRange(DP_A0, DP_A3t4):
            for c in GBRange(DP_CD4_Per_GT30, DP_CD4_Per_LT5):
                modvarPerc[DP_Data][sex][a][c] = float(sheet[row, GB_RW_DataStartCol + col])
                col += 1
        for a in GBRange(DP_A5t9, DP_A10t14):
            for c in GBRange(DP_CD4_Ped_Top, DP_CD4_Ped_LT200):
                modvarCount[DP_Data][sex][a][c] = float(sheet[row, GB_RW_DataStartCol + col])
                col += 1
        row += 1


def import_ChildMortByCD4WithART7to12(sheet, tags, params, projection):   
    modvarTagRow = tags.get('<ChildMortByCD4WithART7to12 MV>', None)
    if modvarTagRow is None: return
    modvarCount = projection[AM_ChildMortByCD4WithART7to12Tag]
    modvarPerc = projection[AM_ChildMortByCD4WithART7to12PercTag]

    row = modvarTagRow + 3
    for sex in GBRange(GB_Male, GB_Female):
        col = 0
        for a in GBRange(DP_A0, DP_A3t4):
            for c in GBRange(DP_CD4_Per_GT30, DP_CD4_Per_LT5):
                modvarPerc[DP_Data][sex][a][c] = float(sheet[row, GB_RW_DataStartCol + col])
                col += 1
        for a in GBRange(DP_A5t9, DP_A10t14):
            for c in GBRange(DP_CD4_Ped_Top, DP_CD4_Ped_LT200):
                modvarCount[DP_Data][sex][a][c] = float(sheet[row, GB_RW_DataStartCol + col])
                col += 1
        row += 1

def import_ChildMortByCD4WithARTGT12(sheet, tags, params, projection):   
    modvarTagRow = tags.get('<ChildMortByCD4WithARTGT12 MV>', None)
    if modvarTagRow is None: return
    modvarCount = projection[AM_ChildMortByCD4WithARTGT12Tag]
    modvarPerc = projection[AM_ChildMortByCD4WithARTGT12PercTag]

    row = modvarTagRow + 3
    for sex in GBRange(GB_Male, GB_Female):
        col = 0
        for a in GBRange(DP_A0, DP_A3t4):
            for c in GBRange(DP_CD4_Per_GT30, DP_CD4_Per_LT5):
                modvarPerc[DP_Data][sex][a][c] = float(sheet[row, GB_RW_DataStartCol + col])
                col += 1
        for a in GBRange(DP_A5t9, DP_A10t14):
            for c in GBRange(DP_CD4_Ped_Top, DP_CD4_Ped_LT200):
                modvarCount[DP_Data][sex][a][c] = float(sheet[row, GB_RW_DataStartCol + col])
                col += 1
        row += 1

def import_ChildARTDist(sheet, tags, params, projection):   
    modvarTagRow = tags.get('<ChildARTDist MV>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_ChildARTDistTag]

    row = modvarTagRow + 2
    for a in GBRange(0, 14):
        values = modvar[DP_Data][a]
        getRowOfYearVals(sheet, values, params, row)    
        row += 1

def import_EffectTreatChild(sheet, tags, params, projection):   
    modvarTagRow = tags.get('<EffectTreatChild MV>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_EffectTreatChildTag]

    row = modvarTagRow + 2
    for eff in GBRange(DP_Cotrim, DP_ChildEffWithART):
        col = GB_RW_DataStartCol
        for t in GBRange(1, DP_MaxChildTreatmentYears):
            modvar[DP_Data][eff][t] = float(sheet[row, col])
            col += 1 
        row += 1

def import_ChildWeightBands(sheet, tags, params, projection):   
    modvarTagRow = tags.get('<ChildWeightBands MV>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_ChildWeightBandsTag]

    row = modvarTagRow + 2
    for sex in GBRange(GB_Male, GB_Female):
        row += 1
        for a in GBRange(DP_A6Months, DP_A14):
            col = 0
            for b in GBRange(DP_Kgs_3_5pt9, DP_Kgs_35_Plus):
                modvar[DP_Data][sex][a][b] = float(sheet[row, GB_RW_DataStartCol + col])
                col += 1
            row += 1

def import_AdultAnnRateProgressLowerCD4(sheet, tags, params, projection):   
    modvarTagRow = tags.get('<AdultAnnRateProgressLowerCD4 MV>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_AdultAnnRateProgressLowerCD4Tag]

    row = modvarTagRow + 3
    for sex in GBRange(GB_Male, GB_Female):
        col = 0
        for a in GBRange(DP_CD4_15_24, DP_CD4_45_54):
            for c in GBRange(DP_CD4_GT500, DP_CD4_LT50):
                modvar[DP_Data][sex][a][c] = float(sheet[row, GB_RW_DataStartCol + col])
                col += 1
        row += 1

def import_AdultDistNewInfectionsCD4(sheet, tags, params, projection):   
    modvarTagRow = tags.get('<AdultDistNewInfectionsCD4 MV>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_AdultDistNewInfectionsCD4Tag]

    row = modvarTagRow + 3
    for sex in GBRange(GB_Male, GB_Female):
        col = 0
        for a in GBRange(DP_CD4_15_24, DP_CD4_45_54):
            for c in GBRange(DP_CD4_GT500, DP_CD4_LT50):
                modvar[DP_Data][sex][a][c] = float(sheet[row, GB_RW_DataStartCol + col])
                col += 1
        row += 1

def import_AdultMortByCD4NoART(sheet, tags, params, projection):   
    modvarTagRow = tags.get('<AdultMortByCD4NoART MV>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_AdultMortByCD4NoARTTag]

    row = modvarTagRow + 3
    for sex in GBRange(GB_Male, GB_Female):
        col = 0
        for a in GBRange(DP_CD4_15_24, DP_CD4_45_54):
            for c in GBRange(DP_CD4_GT500, DP_CD4_LT50):
                modvar[DP_Data][sex][a][c] = float(sheet[row, GB_RW_DataStartCol + col])
                col += 1
        row += 1

def import_AdultInfectReduc(sheet, tags, params, projection):   
    modvarTagRow = tags.get('<AdultInfectReduc MV>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_AdultInfectReducTag]

    row = modvarTagRow + 2 
    modvar[DP_Data] = float(sheet[row, GB_RW_DataStartCol])

def import_MortalityRates(sheet, tags, params, projection):   
    modvarTagRow = tags.get('<MortalityRates MV2>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_MortalityRatesTag]

    row = modvarTagRow + 2
    for timePeriod in GBRange(DP_MortRates_LT12Mo, DP_MortRates_GT12Mo):
        values = modvar[DP_Data][timePeriod]
        getRowOfYearVals(sheet, values, params, row)    
        row += 1

def import_MortalityRatesMultiplier(sheet, tags, params, projection):   
    modvarTagRow = tags.get('<MortalityRatesMultiplier MV>', None)
    if modvarTagRow is None: return
    # modvar = projection[AM_MortalityRatesMultiplierTag]

    row = modvarTagRow + 2
    projection[AM_MortalityRatesMultiplierTag] = float(sheet[row, GB_RW_DataStartCol])

def import_AdultMortByCD4WithART0to6(sheet, tags, params, projection):   
    modvarTagRow = tags.get('<AdultMortByCD4WithART0to6 MV2>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_AdultMortByCD4WithART0to6Tag]

    row = modvarTagRow + 2
    for sex in GBRange(GB_Male, GB_Female):
        col = 0
        for a in GBRange(DP_CD4_15_24, DP_CD4_45_54):
            for c in GBRange(DP_CD4_GT500, DP_CD4_LT50):
                modvar[DP_Data][sex][a][c] = float(sheet[row, GB_RW_DataStartCol + col])
                col += 1
        row += 1

def import_AdultMortByCD4WithART7to12(sheet, tags, params, projection):   
    modvarTagRow = tags.get('<AdultMortByCD4WithART7to12 MV2>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_AdultMortByCD4WithART7to12Tag]

    row = modvarTagRow + 2
    for sex in GBRange(GB_Male, GB_Female):
        col = 0
        for a in GBRange(DP_CD4_15_24, DP_CD4_45_54):
            for c in GBRange(DP_CD4_GT500, DP_CD4_LT50):
                modvar[DP_Data][sex][a][c] = float(sheet[row, GB_RW_DataStartCol + col])
                col += 1
        row += 1

def import_AdultMortByCD4WithARTGT12(sheet, tags, params, projection):   
    modvarTagRow = tags.get('<AdultMortByCD4WithARTGt12 MV2>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_AdultMortByCD4WithARTGT12Tag]

    row = modvarTagRow + 2
    for sex in GBRange(GB_Male, GB_Female):
        col = 0
        for a in GBRange(DP_CD4_15_24, DP_CD4_45_54):
            for c in GBRange(DP_CD4_GT500, DP_CD4_LT50):
                modvar[DP_Data][sex][a][c] = float(sheet[row, GB_RW_DataStartCol + col])
                col += 1
        row += 1

def import_TFRRegion(sheet, tags, params, projection):   
    modvarTagRow = tags.get('<TFRRegion MV>', None)
    if modvarTagRow is None: return
    # modvar = projection[AM_TFRRegionTag]

    row = modvarTagRow + 2
    if int(sheet[row, GB_RW_DataStartCol]) not in [0, DP_Custom]:
        projection[AM_TFRRegionTag] = int(sheet[row, GB_RW_DataStartCol])
            
def import_HIVTFRCustomFlag(sheet, tags, params, projection):
    modvarTagRow = tags.get('<HIVTFRCustomFlag MV>', None)
    if modvarTagRow is None: return
    # modvar = projection[AM_HIVTFRCustomFlagTag]
    
    row = modvarTagRow + 2
    projection[AM_HIVTFRCustomFlagTag] = bool(int(sheet[row, GB_RW_DataStartCol]))

def import_HIVTFR(sheet, tags, params, projection):
    modvarTagRow = tags.get('<HIVTFR MV4>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_HIVTFRTag]

    row = modvarTagRow + 2
    for a in GBRange(DP_A15_19, DP_A45_49):
        values = modvar[DP_Data][a]
        getRowOfYearVals(sheet, values, params, row)    
        row += 1

def import_TFRInputType(sheet, tags, params, projection):   
    modvarTagRow = tags.get('<TFRInputType MV>', None)
    if modvarTagRow is None: return
    # modvar = projection[AM_TFRInputTypeTag]

    row = modvarTagRow + 2
    projection[AM_TFRInputTypeTag] = int(sheet[row, GB_RW_DataStartCol])
    
def import_FertCD4Discount(sheet, tags, params, projection):   
    modvarTagRow = tags.get('<FertCD4Discount MV>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_FertCD4DiscountTag]

    row = modvarTagRow + 2
    for cd4 in GBRange(DP_CD4_GT500, DP_CD4_LT50):
        modvar[DP_Data][cd4] = float(sheet[row, GB_RW_DataStartCol + cd4 - 1])

def import_RatioWomenOnART(sheet, tags, params, projection):
    modvarTagRow = tags.get('<RatioWomenOnART MV2>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_RatioWomenOnARTTag]

    row = modvarTagRow + 2
    col = GB_RW_DataStartCol
    for a in GBRange(DP_A15_19, DP_A45_49):
        modvar[DP_Data][a] = float(sheet[row, col]) 
        col += 1

def import_FRRFitInput(sheet, tags, params, projection):
    modvarTagRow = tags.get('<FRRFitInput MV>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_FRRFitInputTag]

    row = modvarTagRow + 2
    for i in GBRange(DP_Number, DP_Percent):
        values = modvar[i]
        getRowOfYearVals(sheet, values, params, row)    
        row += 1

def import_FRRbyLocation(sheet, tags, params, projection):   
    modvarTagRow = tags.get('<FRRbyLocation MV>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_FRRbyLocationTag]

    row = modvarTagRow + 2
    # modvar[DP_Data] = float(sheet[row, GB_RW_DataStartCol])
    modvar[DP_Data] = float(sheet[row, GB_RW_DataStartCol])

def import_TransEffAssump(sheet, tags, params, projection):
    modvarTagRow = tags.get('<TransEffAssump MV>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_TransEffAssumpTag]

    row = modvarTagRow + 2
    for regimen in GBRange(DP_NoProphExistInfCD4LT200, DP_ARTStartDurPreg_Late):
        for stage in GBRange(DP_Perinatal, DP_BreastfeedingGE350):
            modvar[DP_Data][regimen][stage] = float(sheet[row, GB_RW_DataStartCol + stage - 1])
        row += 1

def import_DALYDisabilityWeights(sheet, tags, params, projection):
    modvarTagRow = tags.get('<DALYDisabilityWeights MV>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_DALYDisabilityWeightsTag]

    row = modvarTagRow + 2
    for r in GBRange(DP_DALY_CD4CountGE200, DP_DALY_OnART):
        for c in GBRange(DP_Adult, DP_Child):
            modvar[r][c] = float(sheet[row, GB_RW_DataStartCol + c - 1])
        row += 1

def import_NewARTPatAlloc(sheet, tags, params, projection):
    modvarTagRow = tags.get('<NewARTPatAlloc MV>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_NewARTPatAllocTag]

    row = modvarTagRow + 2
    for i in GBRange(DP_AdvOpt_ART_ExpMort, DP_AdvOpt_ART_PropElig):
        modvar[i] = float(sheet[row, GB_RW_DataStartCol + i - DP_AdvOpt_ART_ExpMort])

def import_NewARTPatAllocationMethod(sheet, tags, params, projection):   
    modvarTagRow = tags.get('<NewARTPatAllocationMethod MV2>', None)
    if modvarTagRow is None: return
    # modvar = projection[AM_NewARTPatAllocMethodTag]

    row = modvarTagRow + 2
    projection[AM_NewARTPatAllocMethodTag] = int(sheet[row, GB_RW_DataStartCol])

def import_RiskPopOrphans(sheet, tags, params, projection):
    modvarTagRow = tags.get('<RiskPopOrphans MV2>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_RiskPopOrphansTag]

    row = modvarTagRow + 2
    for c in GBRange(DP_PercAIDSDeaths, DP_PercMarried):
        col = GB_RW_DataStartCol
        for g in GBRange(DP_InjectingDrugUsers, DP_LowerRiskGenPop):
            modvar[g][c] = float(sheet[row, col])
            col += 1
        row += 1

def import_ECDCValues(sheet, tags, params, projection):
    modvarTagRow = tags.get('<ECDCValues MV>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_ECDCValuesTag]

    row = modvarTagRow + 2
    for i in GBRange(DP_Number, DP_UpperBound):
        values = modvar[i]
        getRowOfYearVals(sheet, values, params, row)    
        row += 1

def import_ECDCFQName(sheet, tags, params, projection):   
    modvarTagRow = tags.get('<ECDCFQName MV>', None)
    if modvarTagRow is None: return
    # modvar = projection[AM_ECDCFQNameTag]

    row = modvarTagRow + 2
    projection[AM_ECDCFQNameTag] = str(sheet[row, GB_RW_DataStartCol])

def import_NosocomialInfectionsByAge(sheet, tags, params, projection):
    modvarTagRow = tags.get('<NosocomialInfectionsByAge MV>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_NosocomialInfectionsByAgeTag]

    row = modvarTagRow + 2
    for a in GBRange(DP_A0_4, DP_A10_14):
        values = modvar[a]
        getRowOfYearVals(sheet, values, params, row)    
        row += 1

def import_HIVMigrantsByAgeSex(sheet, tags, params, projection):
    modvarTagRow = tags.get('<HIVMigrantsByAgeSex MV>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_HIVMigrantsBySexAgeTag]

    row = modvarTagRow + 3
    for sex in GBRange(GB_Male, GB_Female):
        for a in GBRange(DP_A0_4, DP_MAX_AGE):
            values = modvar[sex][a]
            getRowOfYearVals(sheet, values, params, row)    
            row += 1

def import_IncidenceInput1970(sheet, tags, params, projection):
    modvarTagRow = tags.get('<IncidenceInput1970 MV>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_IncidenceInput1970Tag]

    row = modvarTagRow + 2
    values = modvar
    getRowOfYearVals(sheet, values, params, row)  

def import_CSAVRInputAIDSDeathsSource(sheet, tags, params, projection):   
    modvarTagRow = tags.get('<CSAVRInputAIDSDeathsSource MV>', None)
    if modvarTagRow is None: return

    row = modvarTagRow + 2
    projection[AM_CSAVRInputAIDSDeathsSourceTag] = int(sheet[row, GB_RW_DataStartCol])

def import_CSAVRInputAIDSDeathsSourceName(sheet, tags, params, projection):   
    modvarTagRow = tags.get('<CSAVRInputAIDSDeathsSourceName MV>', None)
    if modvarTagRow is None: return

    row = modvarTagRow + 2
    for i in GBRange(CSAVRSource1, CSAVRSource3):
        projection[AM_CSAVRInputAIDSDeathsSourceNameTag][i] = str(sheet[row, GB_RW_DataStartCol+i])

def import_CSAVRInputAIDSDeaths(sheet, tags, params, projection):
    modvarTagRow = tags.get('<CSAVRInputAIDSDeaths MV2>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_CSAVRInputAIDSDeathsTag]

    row = modvarTagRow + 2
    for i in GBRange(CSAVRSource1, CSAVRSource3):
        for j in GBRange(CSAVRNumReported, CSAVRNumNotReported):
            values = modvar[i][j]
            getRowOfYearVals(sheet, values, params, row)    
            row += 1

def import_CSAVRInputAIDSDeathsBySex(sheet, tags, params, projection):
    modvarTagRow = tags.get('<CSAVRInputAIDSDeathsBySex MV2>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_CSAVRInputAIDSDeathsBySexTag]

    row = modvarTagRow + 2
    for i in GBRange(CSAVRSource1, CSAVRSource3):
        for sex in GBRange(GB_Male, GB_Female):
            for j in GBRange(CSAVRNumReported, CSAVRNumNotReported):
                values = modvar[i][sex][j]
                getRowOfYearVals(sheet, values, params, row)    
                row += 1    

def import_CSAVRInputAIDSDeathsBySexAge(sheet, tags, params, projection):
    modvarTagRow = tags.get('<CSAVRInputAIDSDeathsBySexAge MV2>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_CSAVRInputAIDSDeathsBySexAgeTag]

    row = modvarTagRow + 2
    for i in GBRange(CSAVRSource1, CSAVRSource3):
        for sex in GBRange(GB_Male, GB_Female):
            for a in GBRange(DP_A15_19, DP_A50Plus):
                values = modvar[i][sex][a]
                getRowOfYearVals(sheet, values, params, row)    
                row += 1

def import_CSAVRInputNewDiagnoses(sheet, tags, params, projection):
    modvarTagRow = tags.get('<CSAVRInputNewDiagnoses MV>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_CSAVRInputNewDiagnosesTag]

    row = modvarTagRow + 2
    for i in GBRange(CSAVRNumReported, CSAVRNumNotReported):
        values = modvar[i]
        getRowOfYearVals(sheet, values, params, row)    
        row += 1

def import_CSAVRInputNewDiagnosesBySex(sheet, tags, params, projection):
    modvarTagRow = tags.get('<CSAVRInputNewDiagnosesBySex MV>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_CSAVRInputNewDiagnosesBySexTag]

    row = modvarTagRow + 2
    for sex in GBRange(GB_Male, GB_Female):
        for i in GBRange(CSAVRNumReported, CSAVRNumNotReported):
            values = modvar[sex][i]
            getRowOfYearVals(sheet, values, params, row)    
            row += 1    

def import_CSAVRInputNewDiagnosesBySexAge(sheet, tags, params, projection):
    modvarTagRow = tags.get('<CSAVRInputNewDiagnosesBySexAge MV>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_CSAVRInputNewDiagnosesBySexAgeTag]

    row = modvarTagRow + 2
    for sex in GBRange(GB_Male, GB_Female):
        for a in GBRange(DP_A15_19, DP_A50Plus):
            values = modvar[sex][a]
            getRowOfYearVals(sheet, values, params, row)    
            row += 1

def import_CSAVRInputNewDiagnosesBySexAgeCD4(sheet, tags, params, projection):
    modvarTagRow = tags.get('<CSAVRInputNewDiagnosesBySexAgeCD4 MV>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_CSAVRInputNewDiagnosesBySexAgeCD4Tag]

    row = modvarTagRow + 2
    for sex in GBRange(GB_Male, GB_Female):
        for a in GBRange(DP_A15_19, DP_A50Plus):
            for cd4 in GBRange(CSAVR_CD4_LT200, CSAVR_CD4_500Plus):
                values = modvar[sex][a][cd4]
                getRowOfYearVals(sheet, values, params, row)    
                row += 1

def import_CSAVRInputCD4DistAtDiag(sheet, tags, params, projection):
    modvarTagRow = tags.get('<CSAVRInputCD4DistAtDiag MV>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_CSAVRInputCD4DistAtDiagTag]

    row = modvarTagRow + 2
    for cd4 in GBRange(CSAVR_CD4_LT200, CSAVR_CD4_500Plus):
        values = modvar[cd4]
        getRowOfYearVals(sheet, values, params, row)    
        row += 1

def import_FitIncidencePopulationValue(sheet, tags, params, projection):   
    modvarTagRow = tags.get('<FitIncidencePopulationValue_MV>', None)
    if modvarTagRow is None: return

    row = modvarTagRow + 2
    projection[AM_CSAVRPopulationValueTag] = int(sheet[row, GB_RW_DataStartCol])

def import_AIDSMortalityAllAges(sheet, tags, params, projection):
    modvarTagRow = tags.get('<AIDSMortalityAllAges MV2>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_AIDSMortalityAllAgesTag]

    row = modvarTagRow + 3
    for n in GBRange(DP_Median, DP_UnderCount):
        values = modvar[n]
        getRowOfYearVals(sheet, values, params, row)    
        row += 1

# dead on desktop (checked 2026-02-01)
def import_AnnualInterruptionRate(sheet, tags, params, projection):   
    try:
        modvarTagRow = tags.get('<AnnualInterruptionRate MV>', None)

        row = modvarTagRow + 2
        projection[AM_AnnualInterruptionRateTag] = float(sheet[row, GB_RW_DataStartCol])
    except Exception as e:
        print(f'Error importing AnnualInterruptionRate: {e}')


def import_IncreasedLikelihoodOfReinit(sheet, tags, params, projection):   
    modvarTagRow = tags.get('<IncreasedLikelihoodOfReinit MV>', None)
    if modvarTagRow is None: return

    row = modvarTagRow + 2
    projection[AM_IncreasedLikelihoodOfReinitTag] = float(sheet[row, GB_RW_DataStartCol])

def import_OffARTMortRateMultiplier(sheet, tags, params, projection):   
    modvarTagRow = tags.get('<OffARTMortRateMultiplier MV>', None)
    if modvarTagRow is None: return

    row = modvarTagRow + 2
    projection[AM_OffARTMortRateMultiplierTag] = float(sheet[row, GB_RW_DataStartCol])

# dead on desktop (checked 2026-02-01)
def import_ChildAnnualInterruptionRate(sheet, tags, params, projection):   
    try:
        modvarTagRow = tags.get('<ChildAnnualInterruptionRate MV>', None)

        row = modvarTagRow + 2
        projection[AM_ChildAnnualInterruptionRateTag] = float(sheet[row, GB_RW_DataStartCol])
    except Exception as e:
        print(f'Error importing ChildAnnualInterruptionRate: {e}')

def import_ChildIncreasedLikelihoodOfReinit(sheet, tags, params, projection):   
    modvarTagRow = tags.get('<ChildIncreasedLikelihoodOfReinit MV>', None)
    if modvarTagRow is None: return

    row = modvarTagRow + 2
    projection[AM_ChildIncreasedLikelihoodOfReinitTag] = float(sheet[row, GB_RW_DataStartCol])

def import_ChildOffARTMortRateMultiplier(sheet, tags, params, projection):   
    modvarTagRow = tags.get('<ChildOffARTMortRateMultiplier MV>', None)
    if modvarTagRow is None: return

    row = modvarTagRow + 2
    projection[AM_ChildOffARTMortRateMultiplierTag] = float(sheet[row, GB_RW_DataStartCol])

def import_CSAVRFitOptions(sheet, tags, params, projection):
    modvarTagRow = tags.get('<CSAVRFitOptions MV3>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_CSAVRFitOptionsTag]

    row = modvarTagRow + 2
    for i in GBRange(DP_PLHIV, DP_CD4DistAtDiag):
        modvar[i] = bool(int(sheet[row, GB_RW_DataStartCol + i]))

def import_FitIncidenceParameters(sheet, tags, params, projection):
    modvarTagRow = tags.get('<FitIncidenceParameters MV7>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_CSAVRParametersTag]

    row = modvarTagRow + 3

    for fit in GBRange(DP_DoubleLogistic, DP_CSAVRMaxFit):
        col = GB_RW_DataStartCol
        count = int(sheet[row, col])                                  #count in the file
        row += 1
        for i in GBRange(1, count):
            for j, value in modvar[str(fit)].items():
                if modvar[str(fit)][j]['mstID'] == int(sheet[row, col]): #mstID
                    value = sheet[row + 1, col]
                    if value != '':
                        modvar[str(fit)][j]['value'] = float(value)   #value
            col += 1
        row += 2

def import_FitIncidenceIncScaleParameters(sheet, tags, params, projection):
    modvarTagRow = tags.get('<FitIncidenceIncScaleParameters MV2>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_CSAVRIncScaleParametersTag]

    row = modvarTagRow + 3

    for fit in GBRange(DP_DoubleLogistic, DP_CSAVRMaxFit):
        col = GB_RW_DataStartCol
        count = int(sheet[row, col])                                   #count in the file
        row += 1
        for i in GBRange(1, count):
            for j, value in modvar[str(fit)].items():
                if modvar[str(fit)][j]['mstID'] == int(sheet[row, col]): #mstID
                    value = sheet[row + 1, col]
                    if value != '':
                        modvar[str(fit)][j]['value'] = float(value)   #value
            col += 1
        row += 2

def import_FitIncidenceUncertaintyParams(sheet, tags, params, projection):
    modvarTagRow = tags.get('<FitIncidenceUncertaintyParams MV3>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_CSAVRUncertaintyParamsTag]

    row = modvarTagRow + 3
    for fit in GBRange(DP_DoubleLogistic, DP_rLogistic):
        for i in GBRange(CSAVR_Unc_BurnIn, CSAVR_Unc_NumSamples):
            if not (i == CSAVR_Unc_BurnIn):
                modvar[fit][i] = float(sheet[row, GB_RW_DataStartCol + i])
        row += 1
    
def import_CSAVRConstrainPLHIVGTNumART(sheet, tags, params, projection):
    modvarTagRow = tags.get('<CSAVRConstrainPLHIVGTNumART MV3>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_CSAVRConstrainPLHIVGTNumARTTag]

    row = modvarTagRow + 2
    for fit in GBRange(DP_DoubleLogistic, DP_CSAVRMaxFit):
        modvar[fit] = bool(int(sheet[row, GB_RW_DataStartCol + fit]))

def import_FitIncidenceTypeOfFit(sheet, tags, params, projection):   
    modvarTagRow = tags.get('<FitIncidenceTypeOfFit MV2>', None)
    if modvarTagRow is None: return

    row = modvarTagRow + 2
    projection[AM_CSAVRTypeOfFitTag] = int(sheet[row, GB_RW_DataStartCol])

def import_CSAVRAdjustIRRs(sheet, tags, params, projection):
    modvarTagRow = tags.get('<CSAVRAdjustIRRs MV4>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_CSAVRAdjustIRRsTag]

    row = modvarTagRow + 2
    for fitType in GBRange(DP_DoubleLogistic, DP_CSAVRMaxFit):
        values = modvar[fitType]
        values[DP_CSAVR_SexRatio] = bool(int(sheet[row, GB_RW_DataStartCol]))
        values[DP_CSAVR_DistOfHIV] = bool(int(sheet[row, GB_RW_DataStartCol + 1]))
        row += 1

# def import_FitIncidenceFitMethod(sheet, tags, params, projection):
#     modvarTagRow = tags.get('<FitIncidenceFitMethod MV2>', None)
#     if modvarTagRow is None: return
#     modvar = projection[AM_CSAVRFitMethodTag]

#     row = modvarTagRow + 2
#     for fitType in GBRange(DP_DoubleLogistic, DP_CSAVRMaxFit):
#         modvar[fitType] = int(sheet[row, GB_RW_DataStartCol + fitType])

def import_CSAVRMetaData(sheet, tags, params, projection):
    modvarTagRow = tags.get('<CSAVRMetaData MV2>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_CSAVRMetaDataTag]

    row = modvarTagRow + 2
    for fitType in GBRange(DP_DoubleLogistic, DP_CSAVRMaxFit):
        modvar[fitType]['AIC'] = float(sheet[row, GB_RW_DataStartCol])
        modvar[fitType]['isFitted'] =  bool(int(sheet[row, GB_RW_DataStartCol + 1]))
        if float(sheet[row, GB_RW_DataStartCol + 2]) > 0:
            modvar[fitType]['date'] = datetime.strftime(dateTime_fromDelphi(float(sheet[row, GB_RW_DataStartCol + 2])), GB_DateTime_Format)
        else:
            modvar[fitType]['date'] = float(sheet[row, GB_RW_DataStartCol + 2])
        row += 1

def import_MeanCD4atDiagnosis(sheet, tags, params, projection):
    modvarTagRow = tags.get('<MeanCD4atDiagnosis MV5>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_CSAVRMeanCD4atDiagnosisTag]

    row = modvarTagRow + 2
    for fitType in GBRange(DP_DoubleLogistic, DP_CSAVRMaxFit):
        for sex in GBRange(GB_BothSexes, GB_Female):
            for dataType in GBRange(DP_Number, DP_UpperBound):
                values = modvar[fitType][sex][dataType]
                getRowOfYearVals(sheet, values, params, row)      
                row += 1  

def import_MeanCD4atDiagnosisByAgeSex(sheet, tags, params, projection):
    modvarTagRow = tags.get('<MeanCD4atDiagnosisByAgeSex MV2>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_CSAVRMeanCD4atDiagnosisByAgeSexTag]

    row = modvarTagRow + 2
    for fitType in GBRange(DP_DoubleLogistic, DP_CSAVRMaxFit):
        for sex in GBRange(GB_BothSexes, GB_Female):
            for age in GBRange(DP_AllAges, DP_A50Plus):
                for dataType in GBRange(DP_Number, DP_UpperBound):
                    values = modvar[fitType][sex][age][dataType]
                    getRowOfYearVals(sheet, values, params, row)      
                    row += 1  

def import_TimeInfToDiag(sheet, tags, params, projection):
    modvarTagRow = tags.get('<TimeInfToDiag MV5>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_CSAVRTimeInfToDiagTag]

    row = modvarTagRow + 2
    for fitType in GBRange(DP_DoubleLogistic, DP_CSAVRMaxFit):
        for sex in GBRange(GB_BothSexes, GB_Female):
            for dataType in GBRange(DP_Number, DP_UpperBound):
                values = modvar[fitType][sex][dataType]
                getRowOfYearVals(sheet, values, params, row)      
                row += 1  

def import_PropOfDiagnosed(sheet, tags, params, projection):
    modvarTagRow = tags.get('<PropOfDiagnosed MV5>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_CSAVRPropOfDiagnosedTag]

    row = modvarTagRow + 2
    for fitType in GBRange(DP_DoubleLogistic, DP_CSAVRMaxFit):
        for sex in GBRange(GB_BothSexes, GB_Female):
            for dataType in GBRange(DP_Number, DP_UpperBound):
                values = modvar[fitType][sex][dataType]
                getRowOfYearVals(sheet, values, params, row)      
                row += 1  

def import_PropOfDiagnosedNoART(sheet, tags, params, projection):
    modvarTagRow = tags.get('<PropOfDiagnosedNoART MV2>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_CSAVRPropOfDiagnosedNoARTTag]

    row = modvarTagRow + 2
    for fitType in GBRange(DP_DoubleLogistic, DP_CSAVRMaxFit):
        for sex in GBRange(GB_BothSexes, GB_Female):
            for dataType in GBRange(DP_Number, DP_UpperBound):
                values = modvar[fitType][sex][dataType]
                getRowOfYearVals(sheet, values, params, row)      
                row += 1  

def import_PropofDiagnosedByAgeSexCD4(sheet, tags, params, projection):
    modvarTagRow = tags.get('<PropOfDiagnosedByAgeSexCD4 MV2>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_CSAVRPropOfDiagnosedByAgeSexCD4Tag]

    row = modvarTagRow + 2
    for fitType in GBRange(DP_DoubleLogistic, DP_CSAVRMaxFit):
        for sex in GBRange(GB_BothSexes, GB_Female):
            for age in GBRange(DP_AllAges, DP_A50Plus):
                for cd4 in GBRange(CSAVR_CD4_LT200, CSAVR_CD4_All):
                    for dataType in GBRange(DP_Number, DP_UpperBound):
                        values = modvar[fitType][sex][age][cd4][dataType]
                        getRowOfYearVals(sheet, values, params, row)      
                        row += 1  

def import_CSAVRNumPLHIV(sheet, tags, params, projection):
    modvarTagRow = tags.get('<CSAVRNumPLHIV MV3>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_CSAVRNumPLHIVTag]

    row = modvarTagRow + 2
    for fitType in GBRange(DP_DoubleLogistic, DP_CSAVRMaxFit):
        for sex in GBRange(GB_BothSexes, GB_Female):
            for dataType in GBRange(DP_Number, DP_UpperBound):
                values = modvar[fitType][sex][dataType]
                getRowOfYearVals(sheet, values, params, row)      
                row += 1  

def import_CSAVRNumPLHIVByAgeSexCD4(sheet, tags, params, projection):
    modvarTagRow = tags.get('<CSAVRNumPLHIVByAgeSexCD4 MV2>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_CSAVRNumPLHIVByAgeSexCD4Tag]

    row = modvarTagRow + 2
    for fitType in GBRange(DP_DoubleLogistic, DP_CSAVRMaxFit):
        for sex in GBRange(GB_BothSexes, GB_Female):
            for age in GBRange(DP_AllAges, DP_A50Plus):
                for cd4 in GBRange(CSAVR_CD4_LT200, CSAVR_CD4_All):
                    for dataType in GBRange(DP_Number, DP_UpperBound):
                        values = modvar[fitType][sex][age][cd4][dataType]
                        getRowOfYearVals(sheet, values, params, row)      
                        row += 1  

def import_CSAVRNumDiagnosed(sheet, tags, params, projection):
    modvarTagRow = tags.get('<CSAVRNumDiagnosed MV3>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_CSAVRNumDiagnosedTag]

    row = modvarTagRow + 2
    for fitType in GBRange(DP_DoubleLogistic, DP_CSAVRMaxFit):
        for sex in GBRange(GB_BothSexes, GB_Female):
            for dataType in GBRange(DP_Number, DP_UpperBound):
                values = modvar[fitType][sex][dataType]
                getRowOfYearVals(sheet, values, params, row)      
                row += 1  

def import_CSAVRNumDiagnosedByAgeSexCD4(sheet, tags, params, projection):
    modvarTagRow = tags.get('<CSAVRNumDiagnosedByAgeSexCD4 MV2>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_CSAVRNumDiagnosedByAgeSexCD4Tag]

    row = modvarTagRow + 2
    for fitType in GBRange(DP_DoubleLogistic, DP_CSAVRMaxFit):
        for sex in GBRange(GB_BothSexes, GB_Female):
            for age in GBRange(DP_AllAges, DP_A50Plus):
                for cd4 in GBRange(CSAVR_CD4_LT200, CSAVR_CD4_All):
                    for dataType in GBRange(DP_Number, DP_UpperBound):
                        values = modvar[fitType][sex][age][cd4][dataType]
                        getRowOfYearVals(sheet, values, params, row)      
                        row += 1    

def import_CSAVRAIDSDeaths(sheet, tags, params, projection):
    modvarTagRow = tags.get('<CSAVRAIDSDeaths MV3>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_CSAVRAIDSDeathsTag]

    row = modvarTagRow + 2
    for fitType in GBRange(DP_DoubleLogistic, DP_CSAVRMaxFit):
        for sex in GBRange(GB_BothSexes, GB_Female):
            for dataType in GBRange(DP_Number, DP_UpperBound):
                values = modvar[fitType][sex][dataType]
                getRowOfYearVals(sheet, values, params, row)      
                row += 1  

def import_CSAVRAIDSDeathsByAgeSex(sheet, tags, params, projection):
    modvarTagRow = tags.get('<CSAVRAIDSDeathsByAgeSex MV2>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_CSAVRAIDSDeathsByAgeSexTag]

    row = modvarTagRow + 2
    for fitType in GBRange(DP_DoubleLogistic, DP_CSAVRMaxFit):
        for sex in GBRange(GB_BothSexes, GB_Female):
            for age in GBRange(DP_AllAges, DP_A50Plus):
                for dataType in GBRange(DP_Number, DP_UpperBound):
                    values = modvar[fitType][sex][age][dataType]
                    getRowOfYearVals(sheet, values, params, row)      
                    row += 1 

def import_CSAVRNumNewInfections(sheet, tags, params, projection):
    modvarTagRow = tags.get('<CSAVRNumNewInfections MV3>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_CSAVRNumNewInfectionsTag]

    row = modvarTagRow + 2
    for fitType in GBRange(DP_DoubleLogistic, DP_CSAVRMaxFit):
        for sex in GBRange(GB_BothSexes, GB_Female):
            for dataType in GBRange(DP_Number, DP_UpperBound):
                values = modvar[fitType][sex][dataType]
                getRowOfYearVals(sheet, values, params, row)      
                row += 1   

def import_CSAVRIncidenceByFit(sheet, tags, params, projection):
    modvarTagRow = tags.get('<CSAVRIncidenceByFit MV2>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_CSAVRIncidenceByFitTag]

    row = modvarTagRow + 2
    for fitType in GBRange(DP_DoubleLogistic, DP_CSAVRMaxFit):
        row += 1   
        values = modvar[fitType]
        getRowOfYearVals(sheet, values, params, row)      
                
def import_HIVSexRatio(sheet, tags, params, projection):
    modvarTagRow = tags.get('<HIVSexRatio MV>', None)
    if modvarTagRow is None: return
    getRowOfYearVals(sheet, projection[AM_HIVSexRatioTag], params, modvarTagRow + 3)
                
def import_CSAVRHIVSexRatio(sheet, tags, params, projection):
    modvarTagRow = tags.get('<CSAVRHIVSexRatio MV3', None)
    if modvarTagRow is None: return
    modvar = projection[AM_CSAVRHIVSexRatioTag]

    row = modvarTagRow + 3
    for fitType in GBRange(DP_DoubleLogistic, DP_CSAVRMaxFit):
        values = modvar[fitType]
        getRowOfYearVals(sheet, values, params, row)     
        row += 1
                
# def import_HIVSexRatioFittingValues(sheet, tags, params, projection):
#     modvarTagRow = tags.get('<HIVSexRatioFittingValues MV>', None)
#     if modvarTagRow is None: return
#     modvar = projection[AM_HIVSexRatioFittingValuesTag]

#     row = modvarTagRow + 3
#     for i in GBRange(DP_SAP_FixedIROverTime, DP_SAP_TimeDependentIR):
#         values = modvar[i]
#         getRowOfYearVals(sheet, values, params, row)     
#         row += 1   
                
# def import_ARTTreatFitHIVSexRatio(sheet, tags, params, projection):
#     modvarTagRow = tags.get('<ARTTreatFitHIVSexRatio MV>', None)
#     if modvarTagRow is None: return
#     modvar = projection[AM_ARTTreatFitHIVSexRatioTag]

#     row = modvarTagRow + 3
#     values = modvar
#     getRowOfYearVals(sheet, values, params, row)

def import_SAPFittingValues(sheet, tags, params, projection):
    projection[AM_CustomSAPDataTag] = []

    # CSAVR
    distOfHIVRow = tags.get('<CSAVRDistOfHIV MV2>', None)
    typeOfFitRow = tags.get('<FitIncidenceTypeOfFit MV2>', None)
    CSAVRSexRatioRow = tags.get('<CSAVRHIVSexRatio MV3', None)
    CSAVRMetaRow = tags.get('<CSAVRMetaData MV2>', None)

    typeOfFit = int(sheet[typeOfFitRow + 2, GB_RW_DataStartCol])
    csavr_sex_ratio = []
    
    csavr_sex_ratio = projection[AM_CSAVRHIVSexRatioTag].copy()

    row = CSAVRSexRatioRow + 3
    for fitType in GBRange(DP_DoubleLogistic, DP_CSAVRMaxFit):
        getRowOfYearVals(sheet, csavr_sex_ratio[fitType], params, row)     
        row += 1
                
    
    csavr_dist_of_hiv = projection[AM_CSAVRDistOfHIVTag].copy()

    row = distOfHIVRow + 3
   
    for fitType in GBRange(DP_DoubleLogistic, DP_CSAVRMaxFit): 
        for sex in GBRange(GB_Male, GB_Female):
            for age in GBRange(DP_A0_4, DP_MAX_AGE):
                getRowOfYearVals(sheet, csavr_dist_of_hiv[fitType][sex][age], params, row)    
                row += 1             
        row += 1
    
    csavr_meta = projection[AM_CSAVRMetaDataTag].copy()

    row = CSAVRMetaRow + 2
    for fitType in GBRange(DP_DoubleLogistic, DP_CSAVRMaxFit):
        csavr_meta[fitType]['AIC'] = float(sheet[row, GB_RW_DataStartCol])
        csavr_meta[fitType]['isFitted'] =  bool(int(sheet[row, GB_RW_DataStartCol + 1]))
        if float(sheet[row, GB_RW_DataStartCol + 2]) > 0:
            csavr_meta[fitType]['date'] = datetime.strftime(dateTime_fromDelphi(float(sheet[row, GB_RW_DataStartCol + 2])), GB_DateTime_Format)
        else:
            csavr_meta[fitType]['date'] = float(sheet[row, GB_RW_DataStartCol + 2])
        row += 1
    
    dataDict = getCustomSAPDataDict(getYearIdx(params.finalYear, params.firstYear) + 1)
    dataDict['id'] =  DP_PatternFromCSAVR_Index
    dataDict['dataSource'] = DP_PatternFromCSAVR_Index
    dataDict['name'] = "Pattern from CSAVR"
    dataDict['HIVSexRatio'] = csavr_sex_ratio[typeOfFit]
    dataDict['DistOfHIV'] = csavr_dist_of_hiv[typeOfFit]
    dataDict['AIC'] = csavr_meta[typeOfFit]['AIC']

    projection[AM_CustomSAPDataTag].append(dataDict)



    # HIV Prev
    fittingTagRow = tags.get('<FittingAICData MV>', None)
    distOfHIVTagRow = tags.get('<IRRFittingValues MV>', None)
    sexRatioTagRow = tags.get('<HIVSexRatioFittingValues MV>', None)


    if (fittingTagRow and distOfHIVTagRow and sexRatioTagRow) is not None:
        fittingRow = fittingTagRow + 2

        sexRatioTagFound = sexRatioTagRow > 0
        sexRatioRow = sexRatioTagRow + 3

        distOfHIVTagFound = distOfHIVTagRow > 0
        distOfHIVRow = distOfHIVTagRow + 3
        
        for prevModel in GBRange(DP_SAP_FixedIROverTime, DP_SAP_TimeDependentIR):
            isFitted = bool(int(sheet[fittingRow, GB_RW_DataStartCol + 1]))

            if isFitted:
                dataDict = getCustomSAPDataDict(getYearIdx(params.finalYear, params.firstYear) + 1)
                dataDict['name'] = 'HIV prevalence by age'
                if prevModel == DP_SAP_FixedIROverTime:
                    dataDict['name'] += ': Fixed incidence ratios over time'
                else:
                    dataDict['name'] += ': Time dependent incidence ratios'
                dataDict['fitType'] = DP_SAP_HIVPrevByAge
                dataDict['HIVPrevModel'] = prevModel
                dataDict['AIC'] = float(sheet[fittingRow, GB_RW_DataStartCol])
                
                HIVSexRatio = np.zeros(getYearIdx(params.finalYear, params.firstYear) + 1).tolist()
                if sexRatioTagFound:
                    getRowOfYearVals(sheet, HIVSexRatio, params, sexRatioRow)       
                dataDict['HIVSexRatio'] = HIVSexRatio

                DistOfHIV = np.zeros((GB_Female + 1, DP_MAX_AGE + 1, getYearIdx(params.finalYear, params.firstYear) + 1))
                if distOfHIVTagFound:
                    for sex in GBRange(GB_Male, GB_Female):
                        for age in GBRange(DP_A0_4, DP_MAX_AGE):
                            values = DistOfHIV[sex][age]
                            getRowOfYearVals(sheet, values, params, distOfHIVRow)    
                            distOfHIVRow += 1
                dataDict['DistOfHIV'] = DistOfHIV.tolist()
                if prevModel == DP_SAP_FixedIROverTime:
                    dataDict['dataSource'] = DP_HIVPrevFixed_Index 
                else:
                    dataDict['dataSource'] = DP_HIVPrevTime_Index
                projection[AM_CustomSAPDataTag].append(dataDict)
            
            fittingRow += 1
            sexRatioRow += 1 
            distOfHIVRow += 1
            
    # ART
    fittingTagRow = tags.get('<ARTTreatFittingData MV>', None)
    distOfHIVTagRow = tags.get('<ARTTreatFit MV>', None)
    sexRatioTagRow = tags.get('<ARTTreatFitHIVSexRatio MV>', None)

    if (fittingTagRow and distOfHIVTagRow and sexRatioTagRow) is not None:
        fittingRow = fittingTagRow + 2

        sexRatioTagFound = sexRatioTagRow > 0
        sexRatioRow = sexRatioTagRow + 3

        distOfHIVTagFound = distOfHIVTagRow > 0
        distOfHIVRow = distOfHIVTagRow + 3

        isFitted = bool(int(sheet[fittingRow, GB_RW_DataStartCol + 1]))

        if isFitted:
            dataDict = getCustomSAPDataDict(getYearIdx(params.finalYear, params.firstYear) + 1)
            dataDict['name'] = 'ART by age'
            dataDict['fitType'] = DP_SAP_ARTByAge
            dataDict['HIVPrevModel'] = 'N/A'
            dataDict['AIC'] = float(sheet[fittingRow, GB_RW_DataStartCol])
                
            HIVSexRatio = np.zeros(getYearIdx(params.finalYear, params.firstYear) + 1).tolist()
            if sexRatioTagFound:
                getRowOfYearVals(sheet, HIVSexRatio, params, sexRatioRow)       
            dataDict['HIVSexRatio'] = HIVSexRatio

            DistOfHIV = np.zeros((GB_Female + 1, DP_MAX_AGE + 1, getYearIdx(params.finalYear, params.firstYear) + 1))
            if distOfHIVTagFound:
                for sex in GBRange(GB_Male, GB_Female):
                    for age in GBRange(DP_A0_4, DP_MAX_AGE):
                        values = DistOfHIV[sex][age]
                        getRowOfYearVals(sheet, values, params, distOfHIVRow)    
                        distOfHIVRow += 1
            dataDict['DistOfHIV'] = DistOfHIV.tolist()
            dataDict['dataSource'] = DP_FittedToART_Index
            projection[AM_CustomSAPDataTag].append(dataDict)
            
    # index things
    SAPFitTypeTagRow = tags.get('<SAPFitType MV>', None)
    HIVPrevModelTagRow = tags.get('<HIVPrevModel MV>', None)
    if (SAPFitTypeTagRow >= 0) and (HIVPrevModelTagRow >= 0):
        SAPFitTypeRow = SAPFitTypeTagRow + 2
        HIVPrevModelRow = HIVPrevModelTagRow + 2
        SAPFitType = int(sheet[SAPFitTypeRow, GB_RW_DataStartCol])
        HIVPrevModel = int(sheet[HIVPrevModelRow, GB_RW_DataStartCol])

        for i, dataDict in enumerate(projection[AM_CustomSAPDataTag]):    
            if dataDict['fitType'] == SAPFitType:
                if (SAPFitType == DP_SAP_HIVPrevByAge):
                    if (dataDict['HIVPrevModel'] == HIVPrevModel):
                        projection[AM_CustomSAPDataIndexTag] = i
                else:
                    projection[AM_CustomSAPDataIndexTag] = i
    pass

    # if len(projection[AM_CustomSAPDataTag]) == 0:
    #     dataDict = getCustomSAPDataDict(getYearIdx(params.finalYear, params.firstYear) + 1)
    #     projection[AM_CustomSAPDataTag].append(dataDict)


# def import_FittingAICData(sheet, tags, params, projection):
#     modvarTagRow = tags.get('<FittingAICData MV>', None)
#     if modvarTagRow is None: return
#     modvar = projection[AM_FittingDataTag]

#     row = modvarTagRow + 2
#     for i in GBRange(DP_SAP_FixedIROverTime, DP_SAP_TimeDependentIR):
#         modvar[i]['AIC'] = float(sheet[row, GB_RW_DataStartCol])
#         modvar[i]['isFitted'] = bool(int(sheet[row, GB_RW_DataStartCol + 1]))
#         row += 1

# def import_ARTTreatFittingData(sheet, tags, params, projection):
#     modvarTagRow = tags.get('<ARTTreatFittingData MV>', None)
#     if modvarTagRow is None: return
#     modvar = projection[AM_ARTTreatFittingDataTag]

#     row = modvarTagRow + 2
#     modvar['AIC'] = float(sheet[row, GB_RW_DataStartCol])
#     modvar['isFitted'] = bool(int(sheet[row, GB_RW_DataStartCol + 1]))

def import_DistOfHIV(sheet, tags, params, projection):    
    modvarTagRow = tags.get('<DistOfHIV MV2>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_DistOfHIVTag]

    row = modvarTagRow + 3
    
    for sex in GBRange(GB_Male, GB_Female):
        for age in GBRange(DP_A0_4, DP_MAX_AGE):
            values = modvar[sex][age]
            getRowOfYearVals(sheet, values, params, row)    
            row += 1
    pass

def import_CSAVRDistOfHIV(sheet, tags, params, projection):    
    modvarTagRow = tags.get('<CSAVRDistOfHIV MV2>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_CSAVRDistOfHIVTag]

    row = modvarTagRow + 3
   
    for fitType in GBRange(DP_DoubleLogistic, DP_CSAVRMaxFit): 
        for sex in GBRange(GB_Male, GB_Female):
            for age in GBRange(DP_A0_4, DP_MAX_AGE):
                values = modvar[fitType][sex][age]
                getRowOfYearVals(sheet, values, params, row)    
                row += 1             
        row += 1

# def import_IRRFittingValues(sheet, tags, params, projection):    
#     modvarTagRow = tags.get('<IRRFittingValues MV>', None)
#     if modvarTagRow is None: return
#     modvar = projection[AM_IRRFittingValuesTag]

#     row = modvarTagRow + 3
    
#     for i in GBRange(DP_SAP_FixedIROverTime, DP_SAP_TimeDependentIR):
#         for sex in GBRange(GB_Male, GB_Female):
#             for age in GBRange(DP_A0_4, DP_MAX_AGE):
#                 values = modvar[i][sex][age]
#                 getRowOfYearVals(sheet, values, params, row)    
#                 row += 1
#         row += 1

# def import_ARTTreatFitDistOfHIV(sheet, tags, params, projection):    
#     modvarTagRow = tags.get('<ARTTreatFit MV>', None)
#     if modvarTagRow is None: return
#     modvar = projection[AM_ARTTreatFitDistOfHIVTag]

#     row = modvarTagRow + 3
    
#     for sex in GBRange(GB_Male, GB_Female):
#         for age in GBRange(DP_A0_4, DP_MAX_AGE):
#             values = modvar[sex][age]
#             getRowOfYearVals(sheet, values, params, row)    
#             row += 1

def import_AIDS45q15(sheet, tags, params, projection):
    modvarTagRow = tags.get('<AIDS45q15 MV>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_AIDS45q15Tag]

    row = modvarTagRow + 2
    values = modvar
    getRowOfYearVals(sheet, values, params, row)

def import_NonAIDS45q15(sheet, tags, params, projection):
    modvarTagRow = tags.get('<NonAIDS45q15 MV>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_NonAIDS45q15Tag]

    row = modvarTagRow + 2
    values = modvar
    getRowOfYearVals(sheet, values, params, row)

def import_Total45q15(sheet, tags, params, projection):
    modvarTagRow = tags.get('<Total45q15 MV>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_Total45q15Tag]

    row = modvarTagRow + 2
    values = modvar
    getRowOfYearVals(sheet, values, params, row)

def import_Under5MortRate(sheet, tags, params, projection):
    modvarTagRow = tags.get('<Under5MortRate MV>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_Under5MortRateTag]

    row = modvarTagRow + 2
    values = modvar
    getRowOfYearVals(sheet, values, params, row)

def import_PMTCTProgEstNeed(sheet, tags, params, projection):
    modvarTagRow = tags.get('<PMTCTProgEstNeed MV>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_PMTCTProgEstNeedTag]

    row = modvarTagRow + 2
    values = modvar
    getRowOfYearVals(sheet, values, params, row)

def import_NumberOnART(sheet, tags, params, projection):
    modvarTagRow = tags.get('<NumberOnART MV>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_NumberOnARTTag]

    row = modvarTagRow + 2
    values = modvar
    getRowOfYearVals(sheet, values, params, row)

def import_ARTCovByAge(sheet, tags, params, projection):    
    modvarTagRow = tags.get('<ARTCovByAge MV>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_ARTCovByAgeTag]

    row = modvarTagRow + 3
    
    for sex in GBRange(GB_BothSexes, GB_Female):
        for age in GBRange(DP_A0_4, DP_MAX_AGE):
            values = modvar[sex][age]
            getRowOfYearVals(sheet, values, params, row)    
            row += 1

def import_KeyPops(sheet, tags, params, projection):
    modvarTagRow = tags.get('<KeyPops MV>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_KeyPopsTag]
    
    row = modvarTagRow + 2
    for ind in GBRange(DP_KP_PSE, DP_KP_NewInfs):
        for pop in GBRange(DP_KP_FSW, DP_KP_TG):
            modvar['data'][ind][pop] = float(sheet[row, GB_RW_DataStartCol + pop])
        row += 1

def import_KeyPopsYear(sheet, tags, params, projection):   
    modvarTagRow = tags.get('<KeyPopsYear MV>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_KeyPopsTag]

    row = modvarTagRow + 2
    modvar['year'] = int(sheet[row, GB_RW_DataStartCol])

def import_KeyPopsFName(sheet, tags, params, projection):   
    modvarTagRow = tags.get('<KeyPopsFName MV>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_KeyPopsTag]

    row = modvarTagRow + 2
    modvar['fName'] = str(sheet[row, GB_RW_DataStartCol])

def import_PregWomenPrevRoutineTest(sheet, tags, params, projection):   
    modvarTagRow = tags.get('<PregWomenPrevRoutineTest MV>', None)
    if modvarTagRow is None: return
    # modvar = projection[AM_PregWomenPrevRoutineTestTag]

    row = modvarTagRow + 2
    projection[AM_PregWomenPrevRoutineTestTag] = float(sheet[row, GB_RW_DataStartCol])

def import_PregWomenPrev(sheet, tags, params, projection):
    modvarTagRow = tags.get('<PregWomenPrev MV>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_PregWomenPrevTag]

    row = modvarTagRow + 2
    values = modvar
    getRowOfYearVals(sheet, values, params, row)

def import_PrevSurveyData(sheet, tags, params, projection):    
    modvarTagRow = tags.get('<PrevSurveyData MV5>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_PrevSurveyTag]

    row = modvarTagRow + 4
    
    for survey in GBRange(DP_PrevSurvey1, DP_PrevSurvey8):
        for sex in GBRange(GB_BothSexes, GB_Female):
            for age in GBRange(DP_A2_4, DP_MAX_AGE):
                for dt in GBRange(DP_Number, DP_WeightedSampleSize):
                    modvar[survey]['data'][sex][dt][age] = float(sheet[row, GB_RW_DataStartCol + dt])
                row += 1
        row += 1

def import_PrevSurveyUsed(sheet, tags, params, projection):    
    modvarTagRow = tags.get('<PrevSurveyUsed MV3>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_PrevSurveyTag]

    row = modvarTagRow + 2
    
    for survey in GBRange(DP_PrevSurvey1, DP_PrevSurvey8):
        modvar[survey]['used'] = bool(int(sheet[row, GB_RW_DataStartCol + survey - 1]))

def import_PrevSurveyName(sheet, tags, params, projection):    
    modvarTagRow = tags.get('<PrevSurveyName MV3>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_PrevSurveyTag]

    row = modvarTagRow + 2
    
    for survey in GBRange(DP_PrevSurvey1, DP_PrevSurvey8):
        modvar[survey]['name'] = str(sheet[row, GB_RW_DataStartCol + survey - 1])

def import_PrevSurveyYear(sheet, tags, params, projection):    
    modvarTagRow = tags.get('<PrevSurveyYear MV3>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_PrevSurveyTag]

    row = modvarTagRow + 2
    
    for survey in GBRange(DP_PrevSurvey1, DP_PrevSurvey8):
        modvar[survey]['year'] = int(sheet[row, GB_RW_DataStartCol + survey - 1])

def import_ARTCovSurveyData(sheet, tags, params, projection):    
    modvarTagRow = tags.get('<ARTCovSurveyData MV2>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_ARTCovSurveyTag]

    row = modvarTagRow + 4
    
    for survey in GBRange(DP_PrevSurvey1, DP_PrevSurvey8):
        for sex in GBRange(GB_BothSexes, GB_Female):
            for age in GBRange(DP_A0_4, DP_Val_A50Plus):
                for dt in GBRange(DP_Number, DP_WeightedSampleSize):
                    modvar[survey]['data'][sex][dt][age] = float(sheet[row, GB_RW_DataStartCol + dt])
                row += 1
        row += 1

def import_ARTCovSurveyUsed(sheet, tags, params, projection):    
    modvarTagRow = tags.get('<ARTCovSurveyUsed MV2>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_ARTCovSurveyTag]

    row = modvarTagRow + 2
    
    for survey in GBRange(DP_PrevSurvey1, DP_PrevSurvey8):
        modvar[survey]['used'] = bool(int(sheet[row, GB_RW_DataStartCol + survey - 1]))

def import_ARTCovSurveyName(sheet, tags, params, projection):    
    modvarTagRow = tags.get('<ARTCovSurveyName MV2>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_ARTCovSurveyTag]

    row = modvarTagRow + 2
    
    for survey in GBRange(DP_PrevSurvey1, DP_PrevSurvey8):
        modvar[survey]['name'] = str(sheet[row, GB_RW_DataStartCol + survey - 1])

def import_ARTCovSurveyYear(sheet, tags, params, projection):    
    modvarTagRow = tags.get('<ARTCovSurveyYear MV2>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_ARTCovSurveyTag]

    row = modvarTagRow + 2
    
    for survey in GBRange(DP_PrevSurvey1, DP_PrevSurvey8):
        modvar[survey]['year'] = int(sheet[row, GB_RW_DataStartCol + survey - 1])

def import_MortRateByAge(sheet, tags, params, projection):    
    modvarTagRow = tags.get('<MortRateByAge MV2>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_MortRateByAgeTag]

    row = modvarTagRow + 3
    
    for sex in GBRange(GB_Male, GB_Female):
        for age in GBRange(DP_A0_4, DP_MAX_AGE):
            values = modvar[sex][age]
            getRowOfYearVals(sheet, values, params, row)    
            row += 1

def import_AllCauseMortality(sheet, tags, params, projection):    
    modvarTagRow = tags.get('<AllCauseMortality MV2>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_AllCauseMortalityTag]

    row = modvarTagRow + 3
    
    for sex in GBRange(GB_Male, GB_Female):
        for age in GBRange(DP_A0_4, DP_MAX_AGE):
            values = modvar[sex][age]
            getRowOfYearVals(sheet, values, params, row)    
            row += 1

def import_AIDSMortality(sheet, tags, params, projection):    
    modvarTagRow = tags.get('<AIDSMortality MV2>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_AIDSMortalityTag]

    row = modvarTagRow + 3
    
    for sex in GBRange(GB_Male, GB_Female):
        for age in GBRange(DP_A0_4, DP_MAX_AGE):
            values = modvar[sex][age]
            getRowOfYearVals(sheet, values, params, row)    
            row += 1

def import_NumberOnARTByAge(sheet, tags, params, projection):    
    modvarTagRow = tags.get('<NumberOnARTByAge MV2>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_NumberOnARTByAgeTag]

    row = modvarTagRow + 3
    
    for sex in GBRange(GB_BothSexes, GB_Female):
        for age in GBRange(DP_A0_4, DP_MAX_AGE):
            values = modvar[sex][age]
            getRowOfYearVals(sheet, values, params, row)    
            row += 1

def import_NewlyStartingART(sheet, tags, params, projection):    
    modvarTagRow = tags.get('<NewlyStartingART MV>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_NewlyStartingARTTag]

    row = modvarTagRow + 3
    
    for sex in GBRange(GB_BothSexes, GB_Female):
        for age in GBRange(DP_A0_4, DP_MAX_AGE):
            values = modvar[sex][age]
            getRowOfYearVals(sheet, values, params, row)    
            row += 1

def import_AdultsChildrenStartingART(sheet, tags, params, projection):    
    modvarTagRow = tags.get('<AdultsChildrenStartingART MV>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_AdultsChildrenStartingARTTag]

    row = modvarTagRow + 3
    
    for sex in GBRange(GB_Male, GB_Female):
        for age in GBRange(DP_AllAges, DP_MAX_AGE):
            values = modvar[sex][age]
            getRowOfYearVals(sheet, values, params, row)    
            row += 1

    for age in GBRange(DP_AllAges, DP_MAX_AGE):
        for year in GBRange(params.firstYear, params.finalYear):
            t = getYearIdx(year, params.firstYear)
            modvar[GB_BothSexes][age][t] = modvar[GB_Male][age][t] + modvar[GB_Female][age][t]

def import_PercentOfPop(sheet, tags, params, projection):
    modvarTagRow = tags.get('<PercentOfPop MV>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_PercentOfPopTag]

    row = modvarTagRow + 2
    values = modvar
    getRowOfYearVals(sheet, values, params, row)

def import_FirstYearOfEpidemic(sheet, tags, params, projection):   
    modvarTagRow = tags.get('<FirstYearOfEpidemic MV>', None)
    if modvarTagRow is None: return

    row = modvarTagRow + 2
    epidemic_start_year = int(sheet[row, GB_RW_DataStartCol])

    # Need to reset the Sex ratio defaults  to the new first year of epidemic
    if ((epidemic_start_year != projection[AM_FirstYearOfEpidemicTag]) 
      and (GB_SPECT_MOD_DATA_CONN_ENV in environ)): 
        AMGlobalData = GB_get_db_json(environ.get(GB_SPECT_MOD_DATA_CONN_ENV, None), 
                                      'aim', 
                                      formatCountryFName('AM_Global', AMDatabaseVersion)) 
        sr_defaults = HIVSexRatio_Meta_Init({
            'firstYr': params.firstYear,
            'finalYr': params.finalYear,
            'finalYrIdx': getYearIdx(params.finalYear, params.firstYear),
            'epidemicStartYr': epidemic_start_year,
        }, AMGlobalData)
        projection[AM_HIVSexRatio_MetaTag] = {'default': sr_defaults} 

    projection[AM_FirstYearOfEpidemicTag]   = epidemic_start_year
   

def import_ARTCoverageSelection(sheet, tags, params, projection):   
    modvarTagRow = tags.get('<ARTCoverageSelection MV>', None)
    if modvarTagRow is None: return
    # modvar = projection[AM_ARTCoverageSelectionTag]

    row = modvarTagRow + 2
    projection[AM_ARTCoverageSelectionTag] = int(sheet[row, GB_RW_DataStartCol])

def import_BFYearsRGIdx(sheet, tags, params, projection):   
    modvarTagRow = tags.get('<BFYearsRGIdx MV>', None)
    if modvarTagRow is None: return
    # modvar = projection[AM_BFYearsRGIdxTag]

    row = modvarTagRow + 2
    projection[AM_BFYearsRGIdxTag] = int(sheet[row, GB_RW_DataStartCol])

def import_BFArvRGIdx(sheet, tags, params, projection):   
    modvarTagRow = tags.get('<BFArvRGIdx MV>', None)
    if modvarTagRow is None: return
    # modvar = projection[AM_BFArvRGIdxTag]

    row = modvarTagRow + 2
    projection[AM_BFArvRGIdxTag] = int(sheet[row, GB_RW_DataStartCol])

def import_ChildHIVMortARTRegion(sheet, tags, params, projection):   
    modvarTagRow = tags.get('<ChildHIVMortARTRegion MV>', None)
    if modvarTagRow is None: return
    # modvar = projection[AM_ChildHIVMortARTRegionTag]

    row = modvarTagRow + 2
    if int(sheet[row, GB_RW_DataStartCol]) not in [0, DP_Custom]:
        projection[AM_ChildHIVMortARTRegionTag] = int(sheet[row, GB_RW_DataStartCol])
            
def import_ChildHIVMortARTCustomFlag(sheet, tags, params, projection):
    modvarTagRow = tags.get('<ChildHIVMortARTCustomFlag MV>', None)
    if modvarTagRow is None: return
    # modvar = projection[AM_ChildHIVMortARTCustomFlagTag]
    
    row = modvarTagRow + 2
    projection[AM_ChildHIVMortARTCustomFlagTag] = bool(int(sheet[row, GB_RW_DataStartCol]))

def import_ChildARTDistRegion(sheet, tags, params, projection):   
    modvarTagRow = tags.get('<ChildARTDistRegion MV2>', None)
    if modvarTagRow is None: return
    # modvar = projection[AM_ChildARTDistRegionTag]

    row = modvarTagRow + 2
    if int(sheet[row, GB_RW_DataStartCol]) not in [0, DP_Custom]:
        projection[AM_ChildARTDistRegionTag] = int(sheet[row, GB_RW_DataStartCol])
            
def import_ChildARTDistCustomFlag(sheet, tags, params, projection):
    modvarTagRow = tags.get('<ChildARTDistCustomFlag MV>', None)
    if modvarTagRow is None: return
    # modvar = projection[AM_ChildARTDistCustomFlagTag]
    
    row = modvarTagRow + 2
    projection[AM_ChildARTDistCustomFlagTag] = bool(int(sheet[row, GB_RW_DataStartCol]))

def import_AdultProgressRatesRegion(sheet, tags, params, projection):   
    modvarTagRow = tags.get('<AdultProgressRatesRegion MV2>', None)
    if modvarTagRow is None: return
    # modvar = projection[AM_AdultProgressRatesRegionTag]

    row = modvarTagRow + 2
    if int(sheet[row, GB_RW_DataStartCol]) not in [0, DP_Custom]:
        projection[AM_AdultProgressRatesRegionTag] = int(sheet[row, GB_RW_DataStartCol])
            
def import_AdultProgressRatesCustomFlag(sheet, tags, params, projection):
    modvarTagRow = tags.get('<AdultProgressRatesCustomFlag MV>', None)
    if modvarTagRow is None: return
    # modvar = projection[AM_AdultProgressRatesCustomFlagTag]
    
    row = modvarTagRow + 2
    projection[AM_AdultProgressRatesCustomFlagTag] = bool(int(sheet[row, GB_RW_DataStartCol]))

def import_AdultHIVMortNoARTRegion(sheet, tags, params, projection):   
    modvarTagRow = tags.get('<AdultHIVMortNoARTRegion MV2>', None)
    if modvarTagRow is None: return
    # modvar = projection[AM_AdultHIVMortNoARTRegionTag]

    row = modvarTagRow + 2
    if int(sheet[row, GB_RW_DataStartCol]) not in [0, DP_Custom]:
        projection[AM_AdultHIVMortNoARTRegionTag] = int(sheet[row, GB_RW_DataStartCol])
            
def import_AdultHIVMortNoARTCustomFlag(sheet, tags, params, projection):
    modvarTagRow = tags.get('<AdultHIVMortNoARTCustomFlag MV>', None)
    if modvarTagRow is None: return
    # modvar = projection[AM_AdultHIVMortNoARTCustomFlagTag]
    
    row = modvarTagRow + 2
    projection[AM_AdultHIVMortNoARTCustomFlagTag] = bool(int(sheet[row, GB_RW_DataStartCol]))

def import_AdultHIVMortARTRegion(sheet, tags, params, projection):   
    modvarTagRow = tags.get('<HIV Mortality with ART Country or Region MV>', None)
    if modvarTagRow is None: return
    # modvar = projection[AM_AdultHIVMortARTRegionTag]

    row = modvarTagRow + 2
    if int(sheet[row, GB_RW_DataStartCol]) not in [0, DP_Custom]:
        projection[AM_AdultHIVMortARTRegionTag] = int(sheet[row, GB_RW_DataStartCol])
            
def import_AdultHIVMortARTCustomFlag(sheet, tags, params, projection):
    modvarTagRow = tags.get('<AdultHIVMortARTCustomFlag MV>', None)
    if modvarTagRow is None: return
    # modvar = projection[AM_AdultHIVMortARTCustomFlagTag]
    
    row = modvarTagRow + 2
    projection[AM_AdultHIVMortARTCustomFlagTag] = bool(int(sheet[row, GB_RW_DataStartCol]))

def import_DALYBaseYear(sheet, tags, params, projection):   
    modvarTagRow = tags.get('<DALYBaseYear MV>', None)
    if modvarTagRow is None: return
    # modvar = projection[AM_DALYBaseYearTag]

    row = modvarTagRow + 2
    projection[AM_DALYBaseYearTag] = int(sheet[row, GB_RW_DataStartCol])

def import_DALYDiscountRate(sheet, tags, params, projection):   
    modvarTagRow = tags.get('<DALYDiscountRate MV>', None)
    if modvarTagRow is None: return
    # modvar = projection[AM_DALYDiscountRateTag]

    row = modvarTagRow + 2
    projection[AM_DALYDiscountRateTag] = float(sheet[row, GB_RW_DataStartCol])
            
def import_DALYUseStandardLifeTable(sheet, tags, params, projection):
    modvarTagRow = tags.get('<DALYUseStandardLifeTable MV>', None)
    if modvarTagRow is None: return
    # modvar = projection[AM_DALYUseStandardLifeTableTag]
    
    row = modvarTagRow + 2
    projection[AM_DALYUseStandardLifeTableTag] = bool(int(sheet[row, GB_RW_DataStartCol]))

def import_OrphansRegionalPattern(sheet, tags, params, projection):   
    modvarTagRow = tags.get('<OrphansRegionalPattern MV>', None)
    if modvarTagRow is None: return
    # modvar = projection[AM_OrphansRegionalPatternTag]

    row = modvarTagRow + 2
    projection[AM_OrphansRegionalPatternTag] = int(sheet[row, GB_RW_DataStartCol])
            
def import_IncidenceInput1970Bool(sheet, tags, params, projection):
    modvarTagRow = tags.get('<IncidenceInput1970Bool MV>', None)
    if modvarTagRow is None: return
    # modvar = projection[AM_IncidenceInput1970BoolTag]
    
    row = modvarTagRow + 2
    projection[AM_IncidenceInput1970BoolTag] = bool(int(sheet[row, GB_RW_DataStartCol]))

def import_IncidenceOptions(sheet, tags, params, projection):   
    modvarTagRow = tags.get('<IncidenceOptions MV>', None)
    if modvarTagRow is None: return
    # modvar = projection[AM_IncidenceOptionsTag]

    row = modvarTagRow + 2
    projection[AM_IncidenceOptionsTag] = int(sheet[row, GB_RW_DataStartCol])

def import_IncidenceByFit(sheet, tags, params, projection):   
    modvarTagRow = tags.get('<IncidenceByFit MV4>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_IncidenceByFitTag]

    row = modvarTagRow + 2
    for i in GBRange(DP_DirectIncidenceInputOpt, DP_ECDCOpt):
        values = modvar[i]
        getRowOfYearVals(sheet, values, params, row)    
        row += 1

def import_FourDecPlaceID(sheet, tags, params, projection):   
    modvarTagRow = tags.get('<FourDecPlaceID MV2>', None)
    if modvarTagRow is None: return
    # modvar = projection[AM_FourDecPlaceIDTag]

    row = modvarTagRow + 3
    projection[AM_FourDecPlaceIDTag] = bool(int(sheet[row, GB_RW_DataStartCol]))
            
def import_EPPPrevAdj(sheet, tags, params, projection):
    modvarTagRow = tags.get('<EPPPrevAdj MV>', None)
    if modvarTagRow is None: return
    # modvar = projection[AM_EPPPrevAdjTag]
    
    row = modvarTagRow + 2
    projection[AM_EPPPrevAdjTag] = bool(int(sheet[row, GB_RW_DataStartCol]))
            
def import_EPPMaxAdjFactor(sheet, tags, params, projection):
    modvarTagRow = tags.get('<EPPMaxAdjFactor MV>', None)
    if modvarTagRow is None: return
    # modvar = projection[AM_EPPMaxAdjFactorTag]
    
    row = modvarTagRow + 2
    projection[AM_EPPMaxAdjFactorTag] = float(sheet[row, GB_RW_DataStartCol])
            
def import_EPPPopulationAges(sheet, tags, params, projection):
    modvarTagRow = tags.get('<EPPPopulationAges MV>', None)
    if modvarTagRow is None: return
    # modvar = projection[AM_EPPPopulationAgesTag]
    
    row = modvarTagRow + 2
    projection[AM_EPPPopulationAgesTag] = int(sheet[row, GB_RW_DataStartCol])
            
def import_CustomSAPDataIndex(sheet, tags, params, projection):
    DP_FittedPattern            = 6
    DP_CSAVRPattern             = 7

    modvarTagRow = tags.get('<IncEpidemicRGIdx MV>', None)
    if modvarTagRow is None: return
    # modvar = projection[AM_IncEpidemicRGIdxTag]
    
    row = modvarTagRow + 2
    projection[AM_CustomSAPDataIndexTag] = int(sheet[row, GB_RW_DataStartCol])

    if projection[AM_CustomSAPDataIndexTag] == DP_FittedPattern:
        # index things
        SAPFitTypeTagRow = tags.get('<SAPFitType MV>', None)
        HIVPrevModelTagRow = tags.get('<HIVPrevModel MV>', None)
        if (SAPFitTypeTagRow >= 0) and (HIVPrevModelTagRow >= 0):
            SAPFitTypeRow = SAPFitTypeTagRow + 2
            HIVPrevModelRow = HIVPrevModelTagRow + 2
            SAPFitType = int(sheet[SAPFitTypeRow, GB_RW_DataStartCol])
            HIVPrevModel = int(sheet[HIVPrevModelRow, GB_RW_DataStartCol])

            if (SAPFitType == DP_SAP_HIVPrevByAge):
                if (HIVPrevModel == DP_SAP_FixedIROverTime):
                    projection[AM_CustomSAPDataIndexTag] = DP_HIVPrevFixed_Index
                else:
                    projection[AM_CustomSAPDataIndexTag] = DP_HIVPrevTime_Index
            else:
                projection[AM_CustomSAPDataIndexTag] = DP_FittedToART_Index
    elif projection[AM_CustomSAPDataIndexTag] == DP_CSAVRPattern:
        projection[AM_CustomSAPDataIndexTag] = DP_PatternFromCSAVR_Index



            
def import_IncEpidemicCustomFlagIdx(sheet, tags, params, projection):
    modvarTagRow = tags.get('<IncEpidemicCustomFlagIdx MV>', None)
    if modvarTagRow is None: return
    # modvar = projection[AM_IncEpidemicCustomFlagTag]
    
    row = modvarTagRow + 2
    projection[AM_IncEpidemicCustomFlagTag] = bool(int(sheet[row, GB_RW_DataStartCol]))
            
def import_SexRatioFromEPP(sheet, tags, params, projection):
    modvarTagRow = tags.get('<SexRatioFromEPP MV>', None)
    if modvarTagRow is None: return
    # modvar = projection[AM_SexRatioFromEPPTag]
    
    row = modvarTagRow + 2
    projection[AM_SexRatioFromEPPTag] = bool(int(sheet[row, GB_RW_DataStartCol]))

def import_HIVSexRatioFromEPP(sheet, tags, params, projection):
    modvarTagRow = tags.get('<HIVSexRatioFromEPP MV>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_HIVSexRatioFromEPPTag]

    row = modvarTagRow + 2
    values = modvar
    getRowOfYearVals(sheet, values, params, row)  
            
def import_EpidemicTypeFromEPP(sheet, tags, params, projection):
    modvarTagRow = tags.get('<EpidemicTypeFromEPP MV>', None)
    if modvarTagRow is None: return
    # modvar = projection[AM_EpidemicTypeFromEPPTag]
    
    row = modvarTagRow + 2
    projection[AM_EpidemicTypeFromEPPTag] = str(sheet[row, GB_RW_DataStartCol])

def import_AdultPrevalence(sheet, tags, params, projection):
    modvarTagRow = tags.get('<AdultPrevalence MV>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_AdultPrevalenceTag]

    row = modvarTagRow + 2
    values = modvar
    getRowOfYearVals(sheet, values, params, row)  
    
            
def import_NumOfEPPEpidemics(sheet, tags, params, projection):
    modvarTagRow = tags.get('<NumOfEPPEpidemics MV>', None)
    if modvarTagRow is None: return
    # modvar = projection[AM_NumOfEPPEpidemicsTag]
    
    row = modvarTagRow + 2
    projection[AM_NumOfEPPEpidemicsTag] = int(sheet[row, GB_RW_DataStartCol])
            
def import_EPPCountryName(sheet, tags, params, projection):
    modvarTagRow = tags.get('<EPPCountryName MV>', None)
    if modvarTagRow is None: return
    # modvar = projection[AM_EPPCountryNameTag]
    
    row = modvarTagRow + 2
    projection[AM_EPPCountryNameTag] = str(sheet[row, GB_RW_DataStartCol])
            
def import_EPPEpiName(sheet, tags, params, projection):
    modvarTagRow = tags.get('<EPPEpiName MV>', None)
    if modvarTagRow is None: return
    epi_name_mv = ['']# np.full((projection[AM_NumOfEPPEpidemicsTag]+1,getYearIdx(params.finalYear, params.firstYear)+1), '')
    
    numEpidemics = projection[AM_NumOfEPPEpidemicsTag]
    
    row = modvarTagRow + 2
    for epi in GBRange(DP_MinEpidemic, numEpidemics):
        epi_name = str(sheet[row, GB_RW_DataStartCol])
        if epi_name != '':
            epi_name_mv.append(epi_name)
        row += 1
    projection[AM_EPPEpiNameTag] = epi_name_mv
    pass
            
def import_EPPEpidemic(sheet, tags, params, projection):
    modvarTagRow = tags.get('<EPPEpidemic MV>', None)
    if modvarTagRow is None: return
    projection[AM_EPPEpidemicTag] = ['']
    modvar = projection[AM_EPPEpidemicTag]

    numEpidemics = projection[AM_NumOfEPPEpidemicsTag]
    
    row = modvarTagRow + 2
    for epi in GBRange(DP_MinEpidemic, numEpidemics):
        modvar.append(sheet[row, GB_RW_DataStartCol])
        row += 1
    pass
            
def import_EPPPrevData(sheet, tags, params, projection):
    modvarTagRow = tags.get('<EPPPrevData MV>', None)
    if modvarTagRow is None: return
    projection[AM_EPPPrevDataTag] = np.zeros((projection[AM_NumOfEPPEpidemicsTag]+1,getYearIdx(params.finalYear, params.firstYear)+1))
    modvar = projection[AM_EPPPrevDataTag]

    numEpidemics = projection[AM_NumOfEPPEpidemicsTag]
    
    row = modvarTagRow + 2
    for epi in GBRange(DP_MinEpidemic, numEpidemics):
        values = modvar[epi]
        getRowOfYearVals(sheet, values, params, row)  
        row += 1
            
def import_EPPIncData(sheet, tags, params, projection):
    modvarTagRow = tags.get('<EPPIncData MV>', None)
    if modvarTagRow is None: return
    projection[AM_EPPIncDataTag] = np.zeros((projection[AM_NumOfEPPEpidemicsTag]+1,getYearIdx(params.finalYear, params.firstYear)+1))
    modvar = projection[AM_EPPIncDataTag]

    numEpidemics = projection[AM_NumOfEPPEpidemicsTag]
    
    row = modvarTagRow + 2
    for epi in GBRange(DP_MinEpidemic, numEpidemics):
        values = modvar[epi]
        getRowOfYearVals(sheet, values, params, row)  
        row += 1
            
def import_EPPPopData(sheet, tags, params, projection):
    modvarTagRow = tags.get('<EPPPopData MV>', None)
    if modvarTagRow is None: return
    projection[AM_EPPPopDataTag] = np.zeros((projection[AM_NumOfEPPEpidemicsTag]+1,getYearIdx(params.finalYear, params.firstYear)+1))
    modvar = projection[AM_EPPPopDataTag]

    numEpidemics = projection[AM_NumOfEPPEpidemicsTag]
    
    row = modvarTagRow + 2
    for epi in GBRange(DP_MinEpidemic, numEpidemics):
        values = modvar[epi]
        getRowOfYearVals(sheet, values, params, row)  
        row += 1
            
def import_EPPSexRatio(sheet, tags, params, projection):
    modvarTagRow = tags.get('<EPPSexRatio MV>', None)
    if modvarTagRow is None: return
    projection[AM_EPPSexRatioTag] = np.zeros((projection[AM_NumOfEPPEpidemicsTag]+1,getYearIdx(params.finalYear, params.firstYear)+1))
    modvar = projection[AM_EPPSexRatioTag]
    
    row = modvarTagRow + 3
    for epi in GBRange(DP_MinEpidemic, projection[AM_NumOfEPPEpidemicsTag]):
        values = modvar[epi]
        getRowOfYearVals(sheet, values, params, row)  
        row += 1
            
def import_EPPBaseYrPop(sheet, tags, params, projection):
    modvarTagRow = tags.get('<EPPBaseYrPop MV>', None)
    if modvarTagRow is None: return
    projection[AM_EPPBaseYrPopTag] = np.zeros((projection[AM_NumOfEPPEpidemicsTag]+1))
    modvar = projection[AM_EPPBaseYrPopTag]

    numEpidemics = projection[AM_NumOfEPPEpidemicsTag]
    
    row = modvarTagRow + 2
    if numEpidemics>0:
        for epi in GBRange(DP_CountryID, numEpidemics):
            modvar[epi] = float(sheet[row, GB_RW_DataStartCol + epi - DP_CountryID])
    pass
            
def import_EPPIDUMortality(sheet, tags, params, projection):
    modvarTagRow = tags.get('<EPPIDUMortality MV>', None)
    if modvarTagRow is None: return
    projection[AM_EPPIDUMortalityTag] = np.zeros(projection[AM_NumOfEPPEpidemicsTag]+1)
    modvar = projection[AM_EPPIDUMortalityTag]

    numEpidemics = projection[AM_NumOfEPPEpidemicsTag]
    
    row = modvarTagRow + 2
    if numEpidemics>0:
        for epi in GBRange(DP_CountryID, numEpidemics):
            modvar[epi] = float(sheet[row, GB_RW_DataStartCol + epi - DP_CountryID])
            
def import_EPPPathInfo(sheet, tags, params, projection):
    modvarTagRow = tags.get('<EPPPathInfo MV>', None)
    if modvarTagRow is None: return
    projection[AM_EPPPathInfoTag] = np.full(projection[AM_NumOfEPPEpidemicsTag]+1, getPathInfoDict(False, ''))
    modvar = projection[AM_EPPPathInfoTag]

    numEpidemics = projection[AM_NumOfEPPEpidemicsTag]
    
    row = modvarTagRow + 2
    if numEpidemics>0:
        for epi in GBRange(DP_MinEpidemic, numEpidemics):
            modvar[epi]['IsTotal'] = bool(int(sheet[row, GB_RW_DataStartCol]))
            modvar[epi]['FullName'] = str(sheet[row, GB_RW_DataStartCol + 1])
            row += 1

def import_EppAgeRange(sheet, tags, params, projection):   
    modvarTagRow = tags.get('<EppAgeRange MV>', None)
    if modvarTagRow is None: return
    # modvar = projection[AM_EppAgeRangeTag]

    row = modvarTagRow + 2
    projection[AM_EPPAgeRangeTag] = int(sheet[row, GB_RW_DataStartCol])

def import_YrPtPrevalence_WB(sheet, tags, params, projection):   
    modvarTagRow = tags.get('<YrPtPrevalence_WB MV2>', None)
    if modvarTagRow is None: return
    # modvar = projection[AM_YrPtPrevalence_WBTag]

    row = modvarTagRow + 2
    value = str(sheet[row, GB_RW_DataStartCol])
    projection[AM_YrPtPrevalence_WBTag] = value if value != 'None' else ''

def import_AIDSDeathsAmongIDU(sheet, tags, params, projection):
    modvarTagRow = tags.get('<AIDSDeathsAmongIDU MV>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_AIDSDeathsAmongIDUTag]

    row = modvarTagRow + 2
    values = modvar
    getRowOfYearVals(sheet, values, params, row)  
            
def import_PropIDU_WB(sheet, tags, params, projection):
    modvarTagRow = tags.get('<PropIDU_WB MV>', None)
    if modvarTagRow is None: return
    projection[AM_PropIDU_WBTag] = np.zeros((projection[AM_NumOfEPPEpidemicsTag]+1,getYearIdx(params.finalYear, params.firstYear)+1))
    modvar = projection[AM_PropIDU_WBTag]

    numEpidemics = projection[AM_NumOfEPPEpidemicsTag]
    
    row = modvarTagRow + 3
    if numEpidemics>0:
        for epi in GBRange(DP_CountryID, projection[AM_NumOfEPPEpidemicsTag]):
            values = modvar[epi]
            getRowOfYearVals(sheet, values, params, row)  
            row += 1
            
def import_NonAIDSDeathsAmongIDU(sheet, tags, params, projection):
    modvarTagRow = tags.get('<NonAIDSDeathsAmongIDU MV>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_NonAIDSDeathsAmongIDUTag]
    
    row = modvarTagRow + 2
    values = modvar
    getRowOfYearVals(sheet, values, params, row)  

def import_SexuallyActive15to19(sheet, tags, params, projection):    
    modvarTagRow = tags.get('<SexuallyActive15to19 MV2>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_SexuallyActive15to19Tag]

    row = modvarTagRow + 3
    
    modvar['value'] = float(sheet[row, GB_RW_DataStartCol])
    modvar['str'] = str(sheet[row, GB_RW_DataStartCol + 1])
            
def import_AIDSMortAllAgesFYrAdjIdx(sheet, tags, params, projection):   
    modvarTagRow = tags.get('<AIDSMortAllAgesFYrAdjIdx MV>', None)
    if modvarTagRow is None: return
    # modvar = projection[AM_AIDSMortAllAgesFYrAdjIdxTag]

    row = modvarTagRow + 2
    projection[AM_AIDSMortAllAgesFYrAdjIdxTag] = int(sheet[row, GB_RW_DataStartCol])

def import_ValidationAllCauseDeathsART(sheet, tags, params, projection):
    modvarTagRow = tags.get('<AllCauseDeathsARTValidation MV>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_ValidationAllCauseDeathsARTTag]

    row = modvarTagRow + 2
    values = modvar
    getRowOfYearVals(sheet, values, params, row)  

def import_AdvOptsMeningitis(sheet, tags, params, projection):
    modvarTagRow = tags.get('<AdvOptsMeningitis MV>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_AdvOptsMeningitis_Tag]

    row = modvarTagRow + 2
    modvar['progInCare'] = float(sheet[row, GB_RW_DataStartCol])
    modvar['progNotInCare'] = float(sheet[row, GB_RW_DataStartCol + 1])
    modvar['progWithFluconazole'] = float(sheet[row, GB_RW_DataStartCol + 2])
    modvar['mortRateCMInCare'] = float(sheet[row, GB_RW_DataStartCol + 3])
    modvar['mortRateCMNotInCare'] = float(sheet[row, GB_RW_DataStartCol + 4])
    

def import_PrevNeedFirstTime(sheet, tags, params, projection):   
    modvarTagRow = tags.get('<PreventionNeeds_FirstTime MV>', None)
    if modvarTagRow is None: return

    row = modvarTagRow + 2
    projection[AM_PreventionNeedsFirstTimeTag] = bool(int(sheet[row, GB_RW_DataStartCol]))
    pass

def import_PrevNeedShowVMMC(sheet, tags, params, projection):   
    modvarTagRow = tags.get('<PreventionNeeds_ShowVMMCTab MV>', None)
    if modvarTagRow is None: return

    row = modvarTagRow + 2
    projection[AM_PreventionNeedsShowVMMCTabTag] = bool(int(sheet[row, GB_RW_DataStartCol]))
    pass
    # modvar['showVMMC'] = bool(int(sheet[row, GB_RW_DataStartCol + 1]))
    pass


def import_PrevNeedKeyPop(sheet, tags, params, projection):   
    modvarTagRow = tags.get('<PreventionNeeds_KeyPops MV>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_PreventionNeedsKeyPopsTag]

    row = modvarTagRow + 3
    if 'data' not in modvar:
        modvar['data'] = [{
                'population': 0.0,
                'coverage': 0.0,
                'ratio': 0.0,
                'source': '',
                'userCoverage': 0.0
        } for _ in range(len(DP_TKeyPopType))]  
    
    # populations
    for kp in range(len(DP_TKeyPopType)):
        modvar['data'][kp]['population'] = float(sheet[row, GB_RW_DataStartCol])
        row += 1

    # coverages
    for kp in range(len(DP_TKeyPopType)):
        modvar['data'][kp]['coverage'] = float(sheet[row, GB_RW_DataStartCol])
        row += 1

    # ratio
    modvar['ratio'] = float(sheet[row, GB_RW_DataStartCol])
    row += 1

    # sources
    for kp in range(len(DP_TKeyPopType)):
        modvar['data'][kp]['source'] = sheet[row, GB_RW_DataStartCol]
        row += 1

    # user coverages
    for kp in range(len(DP_TKeyPopType)):
        modvar['data'][kp]['userCoverage'] = float(sheet[row, GB_RW_DataStartCol])
        row += 1
    pass


def import_PrevNeedVMMC(sheet, tags, params, projection):   
    modvarTagRow = tags.get('<PreventionNeeds_VMMC MV>', None)
    if modvarTagRow is None: return
    # modvar = projection[AM_PreventionNeedsVMMCTag]

    row = modvarTagRow + 3
    areas = []
    while not (sheet[row, GB_RW_TagCol] == '<End>'):

        regionName = sheet[row, GB_RW_DescriptCol]
        areaName   = sheet[row, GB_RW_NotesCol]

        # Skip completely empty rows (no region, no area, no data)
        if( (regionName == '') and (areaName == '') ):
            row += 1
            continue
        # Fill area data
        newArea={}
        newArea['name'] = areaName
        newArea['region'] = regionName
        newArea['popFirstYear'] = float(sheet[row, GB_RW_DataStartCol])
        newArea['popFinalYear'] = float(sheet[row, GB_RW_DataStartCol+1])
        newArea['covFirstYear'] = float(sheet[row, GB_RW_DataStartCol+2])
        newArea['targetCov'] = float(sheet[row, GB_RW_DataStartCol+3])
        newArea['tradCircum'] = float(sheet[row, GB_RW_DataStartCol+4])
        newArea['percAged15'] = float(sheet[row, GB_RW_DataStartCol+5])
        newArea['percAged29'] = float(sheet[row, GB_RW_DataStartCol+6])


        # Only create a new region if the regionName is not empty
        # if (regionName <> '') and
        # ((Length(vValue.Regions) = 0) or
        #     (vValue.Regions[High(vValue.Regions)].Name <> regionName)) then
        # begin
        #     newRegion.Name := regionName;
        #     SetLength(newRegion.Areas, 0);
        #     SetLength(vValue.Regions, Length(vValue.Regions)+1);
        #     vValue.Regions[High(vValue.Regions)] := newRegion;
        # end;

        # Append area to the last region if there is a region
        # if Length(vValue.Regions) > 0 then
        # begin
        # SetLength(vValue.Regions[High(vValue.Regions)].Areas,
        #             Length(vValue.Regions[High(vValue.Regions)].Areas)+1);
        # vValue.Regions[High(vValue.Regions)].Areas[
        #     High(vValue.Regions[High(vValue.Regions)].Areas)
        # ] := newArea;
        # end;
        areas.append(newArea)
        row += 1
    projection[AM_PreventionNeedsVMMCTag] = areas
    # pass


def import_PrevNeedCondoms(sheet, tags, params, projection):   
    modvarTagRow = tags.get('<PreventionNeeds_Condoms MV>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_PreventionNeedsCondomsTag]

    if 'data' not in modvar:
        modvar['data'] = [{
                'popFirstYear': 0.0,
                'popFinalYear': 0.0,
                'baselineCov': 0.0,
                'targetCov': 0.0,
                'sexActs': 0.0,
                'wastage': 0.0
        } for _ in range(len(DP_TCondomType))]  
    row = modvarTagRow + 3
    # Population first year
    for condom in range(len(DP_TCondomType)):
      modvar['data'][condom]['popFirstYear'] = float(sheet[row, GB_RW_DataStartCol])
      row += 1

    # Population final year
    for condom in range(len(DP_TCondomType)):
      modvar['data'][condom]['popFinalYear'] = float(sheet[row, GB_RW_DataStartCol])
      row += 1

    # Baseline coverage
    for condom in range(len(DP_TCondomType)):
      modvar['data'][condom]['baselineCov'] = float(sheet[row, GB_RW_DataStartCol])
      row += 1

    # Target coverage
    for condom in range(len(DP_TCondomType)):
      modvar['data'][condom]['targetCov'] = float(sheet[row, GB_RW_DataStartCol])
      row += 1

    # Sex acts
    for condom in range(len(DP_TCondomType)):
      modvar['data'][condom]['sexActs'] = float(sheet[row, GB_RW_DataStartCol])
      row += 1

    # Wastage
    for condom in range(len(DP_TCondomType)):
      modvar['data'][condom]['wastage'] = float(sheet[row, GB_RW_DataStartCol])
      row += 1
    pass


def import_PrevNeedPrEP_V2(sheet, tags, params, projection):   
    modvarTagRow = tags.get('<PreventionNeeds_PrEP MV2>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_PreventionNeedsPrEPTag]

    if 'data' not in modvar:
        modvar['data'] = [{
                'popFirstYear': 0.0,
                'popFinalYear': 0.0,
                'PrEPCov': 0.0,
                'TargetCov': 0.0,
                'Oral': [0.0] * DP_PreventionNeeds_PrEPYearLen,
                'Ring': [0.0] * DP_PreventionNeeds_PrEPYearLen,
                'TwoMonth': [0.0] * DP_PreventionNeeds_PrEPYearLen,
                'SixMonth': [0.0] * DP_PreventionNeeds_PrEPYearLen
        } for _ in range(len(DP_TPrEPType))]  
    row = modvarTagRow + 3
    
    # Population first year
    for PP in range(len(DP_TPrEPType)):
        modvar['data'][PP]['PopFirstYear'] = float(sheet[row, GB_RW_DataStartCol+2])
        row += 1

    # Population final year
    for PP in range(len(DP_TPrEPType)):
        modvar['data'][PP]['PopFinalYear'] = float(sheet[row, GB_RW_DataStartCol+2])
        row += 1

    # PrEP coverage
    for PP in range(len(DP_TPrEPType)):
        modvar['data'][PP]['PrEPCov'] = float(sheet[row, GB_RW_DataStartCol+2])
        row += 1

    # Target coverage
    for PP in range(len(DP_TPrEPType)):
        modvar['data'][PP]['TargetCov'] = float(sheet[row, GB_RW_DataStartCol+2])
        row += 1

    # Oral
    for pr in range(DP_PreventionNeeds_PrEPYearLen):
        for PP in range(len(DP_TPrEPType)):
            modvar['data'][PP]['Oral'][pr] = float(sheet[row, GB_RW_DataStartCol+3])
            row += 1

    # Ring
    for pr in range(DP_PreventionNeeds_PrEPYearLen):
        for PP in range(len(DP_TPrEPType)):
            modvar['data'][PP]['Ring'][pr] = float(sheet[row, GB_RW_DataStartCol+3])
            row += 1

    # Two month
    for pr in range(DP_PreventionNeeds_PrEPYearLen):
        for PP in range(len(DP_TPrEPType)):
            modvar['data'][PP]['TwoMonth'][pr] = float(sheet[row, GB_RW_DataStartCol+3])
            row += 1

    # Six month
    for pr in range(DP_PreventionNeeds_PrEPYearLen):
        for PP in range(len(DP_TPrEPType)):
            modvar['data'][PP]['SixMonth'][pr] = float(sheet[row, GB_RW_DataStartCol+3])
            row += 1
    pass

def import_PrevNeedPrEP_V3(sheet, tags, params, projection):   
    modvarTagRow = tags.get('<PreventionNeeds_PrEP MV3>', None)
    if modvarTagRow is None: return
    modvar = projection[AM_PreventionNeedsPrEPTag]

    if 'data' not in modvar:
        modvar['data'] = [{
                'popFirstYear': 0.0,
                'popFinalYear': 0.0,
                'Prev': 0.0,
                'PrEPCov': 0.0,
                'TargetCov': 0.0,
                'Oral': [0.0] * DP_PreventionNeeds_PrEPYearLen,
                'Ring': [0.0] * DP_PreventionNeeds_PrEPYearLen,
                'TwoMonth': [0.0] * DP_PreventionNeeds_PrEPYearLen,
                'SixMonth': [0.0] * DP_PreventionNeeds_PrEPYearLen
        } for _ in range(len(DP_TPrEPType))]
    row = modvarTagRow + 3
    
    # Population first year
    for PP in range(len(DP_TPrEPType)):
        modvar['data'][PP]['PopFirstYear'] = float(sheet[row, GB_RW_DataStartCol+2])
        row += 1

    # Population final year
    for PP in range(len(DP_TPrEPType)):
        modvar['data'][PP]['PopFinalYear'] = float(sheet[row, GB_RW_DataStartCol+2])
        row += 1

    # Prevalence 
    for PP in range(len(DP_TPrEPType)):
        modvar['data'][PP]['Prev'] = float(sheet[row, GB_RW_DataStartCol+2])
        row += 1

    # PrEP coverage
    for PP in range(len(DP_TPrEPType)):
        modvar['data'][PP]['PrEPCov'] = float(sheet[row, GB_RW_DataStartCol+2])
        row += 1

    # Target coverage
    for PP in range(len(DP_TPrEPType)):
        modvar['data'][PP]['TargetCov'] = float(sheet[row, GB_RW_DataStartCol+2])
        row += 1

    # Oral
    for pr in range(DP_PreventionNeeds_PrEPYearLen):
        for PP in range(len(DP_TPrEPType)):
            modvar['data'][PP]['Oral'][pr] = float(sheet[row, GB_RW_DataStartCol+3])
            row += 1

    # Ring
    for pr in range(DP_PreventionNeeds_PrEPYearLen):
        for PP in range(len(DP_TPrEPType)):
            modvar['data'][PP]['Ring'][pr] = float(sheet[row, GB_RW_DataStartCol+3])
            row += 1

    # Two month
    for pr in range(DP_PreventionNeeds_PrEPYearLen):
        for PP in range(len(DP_TPrEPType)):
            modvar['data'][PP]['TwoMonth'][pr] = float(sheet[row, GB_RW_DataStartCol+3])
            row += 1

    # Six month
    for pr in range(DP_PreventionNeeds_PrEPYearLen):
        for PP in range(len(DP_TPrEPType)):
            modvar['data'][PP]['SixMonth'][pr] = float(sheet[row, GB_RW_DataStartCol+3])
            row += 1
    pass


def import_PrEPParameters(sheet, tags, params, projection):
    modvarTagRow = tags.get('<PrEPParameters MV>', None)
    if modvarTagRow is None: return

    row = modvarTagRow + 3 
    modvar = projection[AM_PMTCTPrEPParametersTag]
    if modvar == None:
        modvar = {}
        projection[AM_PMTCTPrEPParametersTag] = modvar
        
    if ( modvar == {}):
        modvar['adherence'] = {'oral': 0.0, 'injectable': 0.0}
        modvar['selection'] = {'incidenceRatio': 0.0}
        modvar['personYearsPrEP'] = {'oral': 0.0, 'injectable': 0.0}

    modvar['adherence']['oral'] = float(sheet[row, GB_RW_DataStartCol])
    modvar['adherence']['injectable'] = float(sheet[row+1, GB_RW_DataStartCol])
    modvar['selection']['incidenceRatio'] = float(sheet[row+2, GB_RW_DataStartCol])
    modvar['personYearsPrEP']['oral'] = float(sheet[row+3, GB_RW_DataStartCol])
    modvar['personYearsPrEP']['injectable'] = float(sheet[row+4, GB_RW_DataStartCol])
    pass
        
def import_PrEPForPregnantWomen(sheet, tags, params, projection):
    modvarTagRow = tags.get('<PrEPForPregnantWomen MV>', None)
    if modvarTagRow is None: return

    row = modvarTagRow + 2 
    getRowOfYearVals(sheet, projection[AM_PMTCTReceivingOralPrEPTag], params, row)  
    getRowOfYearVals(sheet, projection[AM_PMTCTReceivingInjectablePrEPTag], params, row+1)  
    pass


def import_KOSNewDiagnosesAdults15Plus(sheet, tags, params, projection):
    modvarTagRow = tags.get('<KOSNewDiagnosesAdults15Plus MV>', None)
    if modvarTagRow is None: return

    row = modvarTagRow + 2 
    getRowOfYearVals(sheet, projection[AM_KOSNewDiagnosesAdults15PlusTag], params, row)  
    pass


def import_KOSNewDiagnosesChildren0to14(sheet, tags, params, projection):
    modvarTagRow = tags.get('<KOSNewDiagnosesChildren0_14 MV>', None)
    if modvarTagRow is None: return

    row = modvarTagRow + 2 
    getRowOfYearVals(sheet, projection[AM_KOSNewDiagnosesChildren0t14Tag], params, row)  
    pass


def import_KOSNewDiagnosesRecCD4Test(sheet, tags, params, projection):
    modvarTagRow = tags.get('<KOSNewDiagnosesRecCD4Test MV>', None)
    if modvarTagRow is None: return

    row = modvarTagRow + 2 
    getRowOfYearVals(sheet, projection[AM_KOSNewDiagnosesRecCD4TestTag], params, row)  
    pass
