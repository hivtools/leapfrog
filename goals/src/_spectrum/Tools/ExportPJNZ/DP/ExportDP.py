# fmt: off
import numpy as np
from datetime import datetime
from SpectrumCommon.Modvars.GB.GBDefs import createProjectionParams
from AvenirCommon.Util import GBRange, dateTime_toDelphi
from SpectrumCommon.Const.GB import *
from SpectrumCommon.Modvars.GB.GBUtil import *
from SpectrumCommon.Const.AM import *
from SpectrumCommon.Const.DP import *
from SpectrumCommon.Const.PJ import *
from src._spectrum.Tools.ExportPJNZ.ExportUtil import *

def writeDP(params = createProjectionParams(), projection : dict = {}):
    # sheet = GBSheet()
    PJNZParams = createPJNZParams()

    # sheet(23040,  (params.finalYear-params.firstYear+4), '<EstimatedEnd>')
    sheet = []
    writeHeaders(sheet, PJNZParams)    
    
    # DP
    export_SurvRate1970(sheet, params, PJNZParams, projection)  
    export_FirstYear(sheet, params, PJNZParams, projection)
    export_FinalYear(sheet, params, PJNZParams, projection)
    export_CustomFileYears(sheet, params, PJNZParams, projection)
    export_CustomPopStopRescalingYear(sheet, params, PJNZParams, projection)
    export_ProjectionValid(sheet, params, PJNZParams, projection)
    export_EdAdSource(sheet, params, PJNZParams, projection)
    # export_EdDmSource(sheet, params, PJNZParams, projection) # This is just a copy of EdAdSource. The confusion between PJN global sources vs desktop serparated sources.
    export_DPSources(sheet, params, PJNZParams, projection)
    # Sources
    # DefaultDataSource
    export_DefaultUPDLE(sheet, params, PJNZParams, projection)
    export_DefaultUPDIMR(sheet, params, PJNZParams, projection)
    export_DefaultUPDCMR(sheet, params, PJNZParams, projection)
    export_DefaultUPDSurvRate(sheet, params, PJNZParams, projection)
    export_BigPop(sheet, params, PJNZParams, projection)
    export_TFR(sheet, params, PJNZParams, projection)
    export_ASFR(sheet, params, PJNZParams, projection)
    export_UNPopASFR(sheet, params, PJNZParams, projection)
    export_ASFRTables(sheet, params, PJNZParams, projection)
    export_ASFRNum(sheet, params, PJNZParams, projection)
    export_ASFRCustomFlag(sheet, params, PJNZParams, projection)
    export_SexBirthRatio(sheet, params, PJNZParams, projection)
    export_LE(sheet, params, PJNZParams, projection)
    export_MigrRate(sheet, params, PJNZParams, projection)
    export_MigrAgeDist(sheet, params, PJNZParams, projection)
    # COVID19DeathRate
    # COVID19DeathAgeDist
    export_ModelLifeFileName(sheet, params, PJNZParams, projection)
    export_UseFYrSingleAges(sheet, params, PJNZParams, projection)
    # DP_MV_TEnterCOVID19Deaths
    # DP_MV_TUseLeapfrog
    export_RegionalAdjustPopData(sheet, params, PJNZParams, projection)
    export_RegionalAdjustPopCBState(sheet, params, PJNZParams, projection)
    export_RegionalAdjustPopFName(sheet, params, PJNZParams, projection)
    export_RegionalAdjustPopFDate(sheet, params, PJNZParams, projection)
    export_LifeTableNum(sheet, params, PJNZParams, projection)
    export_SurvRate(sheet, params, PJNZParams, projection)
    
    # AM
    if GB_AM in params.modules:
        export_PopsEligTreat(sheet, params, PJNZParams, projection)
        export_AgeHIVChildOnTreatment(sheet, params, PJNZParams, projection)
        export_CD4ThreshHold(sheet, params, PJNZParams, projection)
        export_CD4ThreshHoldAdults(sheet, params, PJNZParams, projection)
        export_InfantFeedingOptions(sheet, params, PJNZParams, projection)
        export_ARVRegimen(sheet, params, PJNZParams, projection)
        export_PatientsReallocated(sheet, params, PJNZParams, projection)
        export_PercentARTDelivery(sheet, params, PJNZParams, projection)
        export_PrEPForPregnantWomen(sheet, params, PJNZParams, projection)
        export_PregTermAbortionPerNum(sheet, params, PJNZParams, projection)
        export_PregTermAbortion(sheet, params, PJNZParams, projection)
        export_MedCD4CountInit(sheet, params, PJNZParams, projection)
        export_PercLostFollowup(sheet, params, PJNZParams, projection)
        export_NumberInitTreatmentReinit(sheet, params, PJNZParams, projection)
        export_NumNewlyInitART(sheet, params, PJNZParams, projection)
        export_PercLostFollowupChild(sheet, params, PJNZParams, projection)
        export_NumberInitTreatmentReinitsChild(sheet, params, PJNZParams, projection)
        export_NumNewlyInitARTChild(sheet, params, PJNZParams, projection)
        export_HAARTBySex(sheet, params, PJNZParams, projection)
        export_HAARTBySexPerNum(sheet, params, PJNZParams, projection)
        export_AdultARTAdjFactor(sheet, params, PJNZParams, projection)
        export_AdultPatsAllocToFromOtherRegion(sheet, params, PJNZParams, projection)
        # export_AdultARTAdjFactorFlag(sheet, params, PJNZParams, projection) # dead on desktop
        export_CD4Coverage(sheet, params, PJNZParams, projection)
        export_ARTByAgeInputType(sheet, params, PJNZParams, projection)
        export_ARTByAge5YearAG(sheet, params, PJNZParams, projection)
        export_ARTByAgeGAMAG(sheet, params, PJNZParams, projection)
        export_CovPopsEligTreat(sheet, params, PJNZParams, projection)
        export_ChildTreatInputs(sheet, params, PJNZParams, projection)
        export_ChildARTAdjFactor(sheet, params, PJNZParams, projection)
        # export_ChildARTAdjFactorFlag(sheet, params, PJNZParams, projection) # dead on desktop
        export_ChildARTByAgeGroupPerNum(sheet, params, PJNZParams, projection)
        export_ANCTestingValues(sheet, params, PJNZParams, projection)
        export_PrEPParameters(sheet, params, PJNZParams, projection)
        # export_NewInfectionsLessImmigrants(sheet, params, PJNZParams, projection)
        export_HIVTesting(sheet, params, PJNZParams, projection)
        export_HIVTestingHTSTestsByAge(sheet, params, PJNZParams, projection)
        export_KnowledgeOfStatusInputType(sheet, params, PJNZParams, projection)
        export_KnowledgeOfStatusInput(sheet, params, PJNZParams, projection)
        export_KnowledgeOfStatusFileTitle(sheet, params, PJNZParams, projection)
        export_KOSNewDiagnosesAdults15Plus(sheet, params, PJNZParams, projection)
        export_KOSNewDiagnosesChildren0to14(sheet, params, PJNZParams, projection)  
        export_KOSNewDiagnosesRecCD4Test(sheet, params, PJNZParams, projection)
        export_Shiny90AIDSDeathsFYear(sheet, params, PJNZParams, projection)
        # missing Shiny90DataSource
        export_Shiny90IsFitted(sheet, params, PJNZParams, projection)
        export_Shiny90SurveyData(sheet, params, PJNZParams, projection)
        export_Shiny90ProgramData(sheet, params, PJNZParams, projection)
        export_Shiny90Pop(sheet, params, PJNZParams, projection)
        export_Shiny90NumTests(sheet, params, PJNZParams, projection)
        export_Shiny90NumTested12M(sheet, params, PJNZParams, projection)
        export_Shiny90TotalTests(sheet, params, PJNZParams, projection)
        export_Shiny90EverTested(sheet, params, PJNZParams, projection)
        export_Shiny90Diagnosed(sheet, params, PJNZParams, projection)
        export_Shiny90NumAware(sheet, params, PJNZParams, projection)
        export_Shiny90NumDiagnoses(sheet, params, PJNZParams, projection)
        export_Shiny90NumDiagnosesMod(sheet, params, PJNZParams, projection)
        export_Shiny90NumLateDiagnoses(sheet, params, PJNZParams, projection)
        export_Shiny90NotDiagHIV1Yr(sheet, params, PJNZParams, projection)
        export_Shiny90NumFirstTestHIVNeg(sheet, params, PJNZParams, projection)
        export_Shiny90NumReTestHIVNeg(sheet, params, PJNZParams, projection)
        export_Shiny90NumRetestPLHIVOnART(sheet, params, PJNZParams, projection)
        export_Shiny90NumRetestPLHIVNoART(sheet, params, PJNZParams, projection)
        export_Shiny90NumNewDiagnoses(sheet, params, PJNZParams, projection)
        export_Shiny90PosRate(sheet, params, PJNZParams, projection)
        export_Shiny90YieldNewDiagn(sheet, params, PJNZParams, projection)
        export_ViralSuppressionInputType(sheet, params, PJNZParams, projection)
        export_ViralSuppressionInput(sheet, params, PJNZParams, projection)
        export_ViralSuppressionThreshold(sheet, params, PJNZParams, projection)
        export_ChildAnnRateProgressLowerCD4(sheet, params, PJNZParams, projection)
        export_ChildDistNewInfectionsCD4(sheet, params, PJNZParams, projection)
        export_ChildMortByCD4NoART(sheet, params, PJNZParams, projection)
        export_ChildMortalityRates(sheet, params, PJNZParams, projection)
        export_ChildMortalityRatesMultiplier(sheet, params, PJNZParams, projection)
        export_ChildMortByCD4WithART0to6(sheet, params, PJNZParams, projection)
        export_ChildMortByCD4WithART7to12(sheet, params, PJNZParams, projection)
        export_ChildMortByCD4WithARTGT12(sheet, params, PJNZParams, projection)
        export_ChildARTDist(sheet, params, PJNZParams, projection)
        export_EffectTreatChild(sheet, params, PJNZParams, projection)
        export_ChildWeightBands(sheet, params, PJNZParams, projection)
        export_AdultAnnRateProgressLowerCD4(sheet, params, PJNZParams, projection)
        export_AdultDistNewInfectionsCD4(sheet, params, PJNZParams, projection)
        export_AdultMortByCD4NoART(sheet, params, PJNZParams, projection)
        export_AdultInfectReduc(sheet, params, PJNZParams, projection)
        export_MortalityRates(sheet, params, PJNZParams, projection)
        export_MortalityRatesMultiplier(sheet, params, PJNZParams, projection)
        export_AdultMortByCD4WithART0to6(sheet, params, PJNZParams, projection)
        export_AdultMortByCD4WithART7to12(sheet, params, PJNZParams, projection)
        export_AdultMortByCD4WithARTGT12(sheet, params, PJNZParams, projection)
        export_TFRRegion(sheet, params, PJNZParams, projection)
        export_HIVTFRCustomFlag(sheet, params, PJNZParams, projection)
        export_HIVTFR(sheet, params, PJNZParams, projection)
        export_TFRInputType(sheet, params, PJNZParams, projection)
        export_FertCD4Discount(sheet, params, PJNZParams, projection)
        export_RatioWomenOnART(sheet, params, PJNZParams, projection)
        export_FRRFitInput(sheet, params, PJNZParams, projection)
        export_FRRbyLocation(sheet, params, PJNZParams, projection)
        export_TransEffAssump(sheet, params, PJNZParams, projection)
        export_DALYDisabilityWeights(sheet, params, PJNZParams, projection)
        export_NewARTPatAlloc(sheet, params, PJNZParams, projection)
        export_NewARTPatAllocationMethod(sheet, params, PJNZParams, projection)
        export_RiskPopOrphans(sheet, params, PJNZParams, projection)
        export_ECDCValues(sheet, params, PJNZParams, projection)
        export_ECDCFQName(sheet, params, PJNZParams, projection)
        export_NosocomialInfectionsByAge(sheet, params, PJNZParams, projection)
        export_HIVMigrantsByAgeSex(sheet, params, PJNZParams, projection)
        export_IncidenceInput1970(sheet, params, PJNZParams, projection)
        export_CSAVRInputAIDSDeathsSource(sheet, params, PJNZParams, projection)
        export_CSAVRInputAIDSDeathsSourceName(sheet, params, PJNZParams, projection)
        export_CSAVRInputAIDSDeaths(sheet, params, PJNZParams, projection)
        export_CSAVRInputAIDSDeathsBySex(sheet, params, PJNZParams, projection)
        export_CSAVRInputAIDSDeathsBySexAge(sheet, params, PJNZParams, projection)
        export_CSAVRInputNewDiagnoses(sheet, params, PJNZParams, projection)
        export_CSAVRInputNewDiagnosesBySex(sheet, params, PJNZParams, projection)
        export_CSAVRInputNewDiagnosesBySexAge(sheet, params, PJNZParams, projection)
        export_CSAVRInputNewDiagnosesBySexAgeCD4(sheet, params, PJNZParams, projection)
        export_CSAVRInputCD4DistAtDiag(sheet, params, PJNZParams, projection)
        export_AIDSMortalityAllAges(sheet, params, PJNZParams, projection)
    #     export_AnnualInterruptionRate(sheet, params, PJNZParams, projection)
        export_IncreasedLikelihoodOfReinit(sheet, params, PJNZParams, projection)
        export_OffARTMortRateMultiplier(sheet, params, PJNZParams, projection)
        # export_ChildAnnualInterruptionRate(sheet, params, PJNZParams, projection)
        export_ChildIncreasedLikelihoodOfReinit(sheet, params, PJNZParams, projection)
        export_ChildOffARTMortRateMultiplier(sheet, params, PJNZParams, projection)
        export_CSAVRFitOptions(sheet, params, PJNZParams, projection)
        export_FitIncidenceParameters(sheet, params, PJNZParams, projection)
        export_FitIncidenceIncScaleParameters(sheet, params, PJNZParams, projection)
        export_FitIncidenceUncertaintyParams(sheet, params, PJNZParams, projection)
        export_CSAVRConstrainPLHIVGTNumART(sheet, params, PJNZParams, projection)
        export_FitIncidenceTypeOfFit(sheet, params, PJNZParams, projection)
        export_CSAVRAdjustIRRs(sheet, params, PJNZParams, projection)
        # export_FitIncidenceFitMethod(sheet, params, PJNZParams, projection)
        export_CSAVRMetaData(sheet, params, PJNZParams, projection)
        export_MeanCD4atDiagnosis(sheet, params, PJNZParams, projection)
        export_MeanCD4atDiagnosisByAgeSex(sheet, params, PJNZParams, projection)
        export_TimeInfToDiag(sheet, params, PJNZParams, projection)
        export_PropOfDiagnosed(sheet, params, PJNZParams, projection)
        export_PropOfDiagnosedNoART(sheet, params, PJNZParams, projection)
        export_PropofDiagnosedByAgeSexCD4(sheet, params, PJNZParams, projection)
        export_CSAVRNumPLHIV(sheet, params, PJNZParams, projection)
        export_CSAVRNumPLHIVByAgeSexCD4(sheet, params, PJNZParams, projection)
        export_CSAVRNumDiagnosed(sheet, params, PJNZParams, projection)
        export_CSAVRNumDiagnosedByAgeSexCD4(sheet, params, PJNZParams, projection)
        export_CSAVRAIDSDeaths(sheet, params, PJNZParams, projection)
        export_CSAVRAIDSDeathsByAgeSex(sheet, params, PJNZParams, projection)
        export_CSAVRNumNewInfections(sheet, params, PJNZParams, projection)
        export_CSAVRIncidenceByFit(sheet, params, PJNZParams, projection)
        export_FitIncidencePopulationValue(sheet, params, PJNZParams, projection)
        export_FittingAICData(sheet, params, PJNZParams, projection)
        export_ARTTreatFittingData(sheet, params, PJNZParams, projection)
        export_HIVSexRatio(sheet, params, PJNZParams, projection)
        export_CSAVRHIVSexRatio(sheet, params, PJNZParams, projection)
        export_HIVSexRatioFittingValues(sheet, params, PJNZParams, projection)
        export_ARTTreatFitHIVSexRatio(sheet, params, PJNZParams, projection)
        export_AIDS45q15(sheet, params, PJNZParams, projection)
        export_NonAIDS45q15(sheet, params, PJNZParams, projection)
        export_Total45q15(sheet, params, PJNZParams, projection)
        export_Under5MortRate(sheet, params, PJNZParams, projection)
        export_PMTCTProgEstNeed(sheet, params, PJNZParams, projection)
        export_NumberOnART(sheet, params, PJNZParams, projection)
        export_ARTCovByAge(sheet, params, PJNZParams, projection)
        export_KeyPops(sheet, params, PJNZParams, projection)
        export_KeyPopsYear(sheet, params, PJNZParams, projection)
        export_KeyPopsFName(sheet, params, PJNZParams, projection)
        export_PregWomenPrevRoutineTest(sheet, params, PJNZParams, projection)
        export_PregWomenPrev(sheet, params, PJNZParams, projection)
        export_ValidationAllCauseDeathsART(sheet, params, PJNZParams, projection)
        export_PrevSurveyData(sheet, params, PJNZParams, projection)
        export_PrevSurveyUsed(sheet, params, PJNZParams, projection)
        export_PrevSurveyName(sheet, params, PJNZParams, projection)
        export_PrevSurveyYear(sheet, params, PJNZParams, projection)
        export_ARTCovSurveyData(sheet, params, PJNZParams, projection)
        export_ARTCovSurveyUsed(sheet, params, PJNZParams, projection)
        export_ARTCovSurveyName(sheet, params, PJNZParams, projection)
        export_ARTCovSurveyYear(sheet, params, PJNZParams, projection)
        export_MortRateByAge(sheet, params, PJNZParams, projection)
        export_AllCauseMortality(sheet, params, PJNZParams, projection)
        export_AIDSMortality(sheet, params, PJNZParams, projection)
        export_NumberOnARTByAge(sheet, params, PJNZParams, projection)
        export_NewlyStartingART(sheet, params, PJNZParams, projection)
        export_AdultsChildrenStartingART(sheet, params, PJNZParams, projection)
        export_PercentOfPop(sheet, params, PJNZParams, projection)
        export_FirstYearOfEpidemic(sheet, params, PJNZParams, projection)
        export_ARTCoverageSelection(sheet, params, PJNZParams, projection)
        export_BFYearsRGIdx(sheet, params, PJNZParams, projection)
        export_BFArvRGIdx(sheet, params, PJNZParams, projection)
        export_ChildHIVMortARTRegion(sheet, params, PJNZParams, projection)
        export_ChildHIVMortARTCustomFlag(sheet, params, PJNZParams, projection)
        export_ChildARTDistRegion(sheet, params, PJNZParams, projection)
        export_ChildARTDistCustomFlag(sheet, params, PJNZParams, projection)
        export_AdultProgressRatesRegion(sheet, params, PJNZParams, projection)
        export_AdultProgressRatesCustomFlag(sheet, params, PJNZParams, projection)
        export_AdultHIVMortNoARTRegion(sheet, params, PJNZParams, projection)
        export_AdultHIVMortNoARTCustomFlag(sheet, params, PJNZParams, projection)
        export_AdultHIVMortARTRegion(sheet, params, PJNZParams, projection)
        export_AdultHIVMortARTCustomFlag(sheet, params, PJNZParams, projection)
        export_DALYBaseYear(sheet, params, PJNZParams, projection)
        export_DALYDiscountRate(sheet, params, PJNZParams, projection)
        export_DALYUseStandardLifeTable(sheet, params, PJNZParams, projection)
        export_OrphansRegionalPattern(sheet, params, PJNZParams, projection)
        export_IncidenceInput1970Bool(sheet, params, PJNZParams, projection)
        export_IncidenceOptions(sheet, params, PJNZParams, projection)
        export_IncidenceByFit(sheet, params, PJNZParams, projection)
        export_FourDecPlaceID(sheet, params, PJNZParams, projection)
        export_EPPPrevAdj(sheet, params, PJNZParams, projection)
        export_EPPMaxAdjFactor(sheet, params, PJNZParams, projection)
        export_EPPPopulationAges(sheet, params, PJNZParams, projection)
        export_IncEpidemicRGIdx(sheet, params, PJNZParams, projection)
        export_IncEpidemicCustomFlagIdx(sheet, params, PJNZParams, projection)
        export_SAPFitType(sheet, params, PJNZParams, projection)
        export_HIVPrevModel(sheet, params, PJNZParams, projection)
        export_DistOfHIV(sheet, params, PJNZParams, projection)
        export_CSAVRDistOfHIV(sheet, params, PJNZParams, projection)
        export_IRRFittingValues(sheet, params, PJNZParams, projection)
        export_ARTTreatFitDistOfHIV(sheet, params, PJNZParams, projection)
        export_SexRatioFromEPP(sheet, params, PJNZParams, projection)
        export_HIVSexRatioFromEPP(sheet, params, PJNZParams, projection)
        export_EpidemicTypeFromEPP(sheet, params, PJNZParams, projection)
        export_ChangesLog(sheet, params, PJNZParams, projection)
        export_AdultPrevalence(sheet, params, PJNZParams, projection)
        export_NumOfEPPEpidemics(sheet, params, PJNZParams, projection)
        export_EPPCountryName(sheet, params, PJNZParams, projection)
        export_EPPEpiName(sheet, params, PJNZParams, projection)
        export_EPPEpidemic(sheet, params, PJNZParams, projection)
        export_EPPPrevData(sheet, params, PJNZParams, projection)
        export_EPPIncData(sheet, params, PJNZParams, projection)
        export_EPPPopData(sheet, params, PJNZParams, projection)
        export_EPPSexRatio(sheet, params, PJNZParams, projection)
        export_EPPBaseYrPop(sheet, params, PJNZParams, projection)
        export_EPPIDUMortality(sheet, params, PJNZParams, projection)
        export_EPPPathInfo(sheet, params, PJNZParams, projection)
        export_EppAgeRange(sheet, params, PJNZParams, projection)
        export_YrPtPrevalence_WB(sheet, params, PJNZParams, projection)
        export_AIDSDeathsAmongIDU(sheet, params, PJNZParams, projection)
        export_PropIDU_WB(sheet, params, PJNZParams, projection)
        export_NonAIDSDeathsAmongIDU(sheet, params, PJNZParams, projection)
        export_PrevNeedFirstTime(sheet, params, PJNZParams, projection)
        if 'data' in projection[AM_PreventionNeedsKeyPopsTag]:
            export_PrevNeedShowVMMC(sheet, params, PJNZParams, projection)
            export_PrevNeedKeyPop(sheet, params, PJNZParams, projection)
            export_PrevNeedVMMC(sheet, params, PJNZParams, projection)
            export_PrevNeedCondoms(sheet, params, PJNZParams, projection)
            export_PrevNeedPrEP(sheet, params, PJNZParams, projection)
        export_SexuallyActive15to19(sheet, params, PJNZParams, projection)
        export_AIDSMortAllAgesFYrAdjIdx(sheet, params, PJNZParams, projection)

        export_AIDSDeaths(sheet, params, PJNZParams, projection)
        export_AIDSDeathsART(sheet, params, PJNZParams, projection)
        export_AIDSDeathsARTSingleAge(sheet, params, PJNZParams, projection)
        export_AIDSDeathsNoART(sheet, params, PJNZParams, projection)
        export_AIDSDeathsNoARTSingleAge(sheet, params, PJNZParams, projection)
        export_AdultNonAIDSExcessMort(sheet, params, PJNZParams, projection)
        export_AidsDeathsByAge(sheet, params, PJNZParams, projection)
        export_Births(sheet, params, PJNZParams, projection)
        export_ChAged14ByCD4Cat(sheet, params, PJNZParams, projection)
        export_ChildARTCalc(sheet, params, PJNZParams, projection)
        export_ChildNeedPMTCT(sheet, params, PJNZParams, projection)
        export_ChildPatsAllocToFromOtherRegion(sheet, params, PJNZParams, projection)
        export_Deaths(sheet, params, PJNZParams, projection)
        export_DeathsByAge(sheet, params, PJNZParams, projection)
        export_HIV(sheet, params, PJNZParams, projection)
        export_HIVBySingleAge(sheet, params, PJNZParams, projection)
        export_NeedART(sheet, params, PJNZParams, projection)
        export_NeedARTDec31(sheet, params, PJNZParams, projection)
        export_NewInfections(sheet, params, PJNZParams, projection)
        export_NewInfectionsBySingleAge(sheet, params, PJNZParams, projection)
        export_NonAIDSExcessDeathsSingleAge(sheet, params, PJNZParams, projection)
        export_OnART(sheet, params, PJNZParams, projection)
        export_OnARTBySingleAge(sheet, params, PJNZParams, projection)
        export_PerinatalTransmission(sheet, params, PJNZParams, projection)
        export_ValidDate(sheet, params, PJNZParams, projection)
        export_ValidVersion(sheet, params, PJNZParams, projection)
        export_ValidVersion2(sheet, params, PJNZParams, projection)

    return sheet

########################################################################
#                                                                      #
#                            Get Labels                                #
#                                                                      #
########################################################################

def getASFRName(m):    
    ASFR_Names = {
        DP_ASFR_UNAfrica : 'UN sub-Saharan Africa',
        DP_ASFR_UNArab : 'UN Arab',
        DP_ASFR_UNAsia : 'UN Asia',
        DP_ASFR_Average : 'Average',
    }
    return ASFR_Names[m]

def GetAgeName(age): 
    AgeNames = {
        DP_A0_4    : 'age: 0-4',
        DP_A5_9    : 'age: 5-9',
        DP_A10_14  : 'age: 10-14',
        DP_A15_19  : 'age: 15-19',
        DP_A20_24  : 'age: 20-24',
        DP_A25_29  : 'age: 25-29',
        DP_A30_34  : 'age: 30-34',
        DP_A35_39  : 'age: 35-39',
        DP_A40_44  : 'age: 40-44',
        DP_A45_49  : 'age: 45-49',
        DP_A50_54  : 'age: 50-54',
        DP_A55_59  : 'age: 55-59',
        DP_A60_64  : 'age: 60-64',
        DP_A65_69  : 'age: 65-69',
        DP_A70_74  : 'age: 70-74',
        DP_A75_79  : 'age: 75-79',
        DP_A80_Up  : 'age: 80-Up'
    }

    return AgeNames[age]

def GetAgeName2(age): 
    AgeNames = {
        DP_AllAges : 'Age: All ages',
        DP_A0_4    : 'Age: 0-4',
        DP_A5_9    : 'Age: 5-9',
        DP_A10_14  : 'Age: 10-14',
        DP_A15_19  : 'Age: 15-19',
        DP_A20_24  : 'Age: 20-24',
        DP_A25_29  : 'Age: 25-29',
        DP_A30_34  : 'Age: 30-34',
        DP_A35_39  : 'Age: 35-39',
        DP_A40_44  : 'Age: 40-44',
        DP_A45_49  : 'Age: 45-49',
        DP_A50_54  : 'Age: 50-54',
        DP_A55_59  : 'Age: 55-59',
        DP_A60_64  : 'Age: 60-64',
        DP_A65_69  : 'Age: 65-69',
        DP_A70_74  : 'Age: 70-74',
        DP_A75_79  : 'Age: 75-79',
        DP_A80_Up  : 'Age: 80+'
    }

    return AgeNames[age]

########################################################################
#                                                                      #
#                       Formats / Structures                           #
#                                                                      #
########################################################################

def format1(sheet, params, PJNZParams, projection, tag1, tag2):
    addStartTag(sheet, PJNZParams, tag1)
    modvar = projection[tag2]

    PJNZParams.currRow += 2    
    addValueTag(sheet, PJNZParams)
    
    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams, 'Gender bounds')
    addValue(sheet, PJNZParams, GB_RW_DataStartCol, str(GB_Male))
    addValue(sheet, PJNZParams, GB_RW_DataStartCol + 1, str(GB_Female))

    for sex in GBRange(GB_Male, GB_Female):
        PJNZParams.currRow += 1
        values = modvar[sex]
        addDescript(sheet, PJNZParams, getSexLabel(sex))
        setRowOfYearVals(sheet, values, params, PJNZParams.currRow)    
        
    addEndTag(sheet, PJNZParams)

def format2(sheet, params, PJNZParams, projection, tag1, tag2, label = ''):
    addStartTag(sheet, PJNZParams, tag1)
    
    modvar = projection[tag2]
    
    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams,  label)

    PJNZParams.currRow += 1
    addValueTag(sheet, PJNZParams)

    values = modvar
    setRowOfYearVals(sheet, values, params, PJNZParams.currRow)
    
    addEndTag(sheet, PJNZParams)


########################################################################
#                                                                      #
#                      Results used as inputs                          #
#                                                                      #
########################################################################

def export_SurvRate1970(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<SurvRate1970 MV>')

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)
    addValue(sheet, PJNZParams, GB_RW_DataStartCol, '')
    addEndTag(sheet, PJNZParams)

def export_FirstYear(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<FirstYear MV2>')
    modvar = projection[PJN_FirstYearTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)
    addValue(sheet, PJNZParams, GB_RW_DataStartCol, modvar)
    addEndTag(sheet, PJNZParams)

def export_FinalYear(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<FinalYear MV2>')
    modvar = projection[PJN_FinalYearTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)
    addValue(sheet, PJNZParams, GB_RW_DataStartCol, modvar)
    addEndTag(sheet, PJNZParams)

def export_ProjectionValid(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<ProjectionValid MV2>')

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)
    addValue(sheet, PJNZParams, GB_RW_DataStartCol, 0) #False
    addEndTag(sheet, PJNZParams)

def export_CustomFileYears(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<CustomFileYears MV>')
    modvar = projection[DP_CustomFileYearsTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)
    addValue(sheet, PJNZParams, GB_RW_DataStartCol, modvar['DP_CPopFirstYr'])
    addValue(sheet, PJNZParams, GB_RW_DataStartCol + 1, modvar['DP_CPopFinalYr'])
    addEndTag(sheet, PJNZParams)

def export_CustomPopStopRescalingYear(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<CustomPopStopRescalingYear MV>')
    modvar = projection[DP_CustomPopStopRescalingYearTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)
    addValue(sheet, PJNZParams, GB_RW_DataStartCol, modvar)
    addEndTag(sheet, PJNZParams)

def export_EdAdSource(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<EdAdSource MV>')
    userSourceModvar = projection[PJN_UserSourceTag]
    # defaultModvar = projection[AM_AMSourcesTag]

    PJNZParams.currRow += 2
     
    addValueTag(sheet, PJNZParams)
    
    sourceCount = len(userSourceModvar); # + len(defaultModvar)
    addValue(sheet, PJNZParams, GB_RW_DataStartCol, sourceCount)
    for s in GBRange(1, len(userSourceModvar)):
        addValue(sheet, PJNZParams, GB_RW_DataStartCol + s, userSourceModvar[s - 1])

    # for s in GBRange(1, len(defaultModvar)):
    #     addValue(sheet, PJNZParams, GB_RW_DataStartCol + len(userSourceModvar) + s, defaultModvar[s - 1])

    addEndTag(sheet, PJNZParams)

def export_EdDmSource(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<EdDmSource MV>')
    modvar = projection[PJN_UserSourceTag]

    PJNZParams.currRow += 2
    
    addValueTag(sheet, PJNZParams)
    
    sourceCount = len(modvar)
    addValue(sheet, PJNZParams, GB_RW_DataStartCol, sourceCount)
    for s in GBRange(1, sourceCount):
        addValue(sheet, PJNZParams, GB_RW_DataStartCol + s, modvar[s - 1])

    addEndTag(sheet, PJNZParams)

def export_DPSources(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<DPSources MV>')
    modvar = projection[DP_DPSourcesTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)
    addNote(sheet, PJNZParams, 'Provider')
    addValue(sheet, PJNZParams, GB_RW_DataStartCol,  modvar['Provider'])
    
    PJNZParams.currRow += 1
    addNote(sheet, PJNZParams, 'Version')
    addValue(sheet, PJNZParams, GB_RW_DataStartCol,  modvar['VersionNum'])
    PJNZParams.currRow += 1
    addValue(sheet, PJNZParams, GB_RW_NotesCol, 'Sources')

    for i in GBRange(DP_UPD_Pop, DP_UPD_Migration):
        addValue(sheet, PJNZParams, GB_RW_DataStartCol,  modvar['Sources'][i]['Name'])
        addValue(sheet, PJNZParams, GB_RW_DataStartCol + 1,  modvar['Sources'][i]['Summary'])
        addValue(sheet, PJNZParams, GB_RW_DataStartCol + 2,  modvar['Sources'][i]['Source'])
        addValue(sheet, PJNZParams, GB_RW_DataStartCol + 3,  modvar['Sources'][i]['Date'])
        PJNZParams.currRow += 1

    PJNZParams.currRow -= 1
    addEndTag(sheet, PJNZParams)

def export_DefaultUPDLE(sheet, params, PJNZParams, projection):
    format1(sheet, params, PJNZParams, projection, '<DefaultUPDLE MV>', DP_DefaultUPDLETag)

def export_DefaultUPDIMR(sheet, params, PJNZParams, projection):
    format1(sheet, params, PJNZParams, projection, '<DefaultUPDIMR MV>', DP_DefaultUPDIMRTag)

def export_DefaultUPDCMR(sheet, params, PJNZParams, projection): 
    format1(sheet, params, PJNZParams, projection, '<DefaultUPDCMR MV>', DP_DefaultUPDCMRTag)

def export_DefaultUPDSurvRate(sheet, params, PJNZParams, projection):    
    addStartTag(sheet, PJNZParams, '<DefaultUPDSurvRate MV>')
    modvar = projection[DP_DefaultUPDSurvRateTag]

    PJNZParams.currRow += 2    
    addValueTag(sheet, PJNZParams)
    
    PJNZParams.currRow += 1
    
    sStart = GB_Male
    sEnd = GB_Female
    
    addDescript(sheet, PJNZParams, 'Gender bounds')
    addValue(sheet, PJNZParams, GB_RW_DataStartCol, str(sStart))
    addValue(sheet, PJNZParams, GB_RW_DataStartCol + 1, str(sEnd))
    
    PJNZParams.currRow += 1
    
    aStart = 0
    aEnd = DP_MAX_SURVRATE
    
    addDescript(sheet, PJNZParams, 'Survival bounds')
    addValue(sheet, PJNZParams, GB_RW_DataStartCol, str(aStart))
    addValue(sheet, PJNZParams, GB_RW_DataStartCol + 1, str(aEnd))
    
    for age in GBRange(aStart, aEnd):
        for sex in GBRange(sStart, sEnd):
            PJNZParams.currRow += 1
            values = modvar[age][sex]
            addDescript(sheet, PJNZParams, getSexLabel(sex))
            setRowOfYearVals(sheet, values, params, PJNZParams.currRow)    
        
    addEndTag(sheet, PJNZParams)

def export_BigPop(sheet, params, PJNZParams, projection):    
    addStartTag(sheet, PJNZParams, '<BigPop MV3>')
    modvar = projection[DP_BigPopTag]

    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams, 'First year population single age')
    
    PJNZParams.currRow += 1
    addValueTag(sheet, PJNZParams)
    
    t = 0
    for year in GBRange(params.firstYear, params.finalYear):
        addValue(sheet, PJNZParams, GB_RW_DataStartCol + t, str(year))
        t += 1
                
    for sex in GBRange(GB_Male, GB_Female):
        for age in GBRange(0, DP_MaxSingleAges):
            PJNZParams.currRow += 1
            values = modvar[sex][age]
            addNote(sheet, PJNZParams, getSexLabel(sex) + '; ' + 'Age ' + str(age))
            setRowOfYearVals(sheet, values, params, PJNZParams.currRow, rowIncludesFirstYear = True)        
        
    addEndTag(sheet, PJNZParams)
            
def export_TFR(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<TFR MV>')
    modvar = projection[DP_TFRTag]

    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams, 'Total fertility rate')
            
    PJNZParams.currRow += 1
    values = modvar
    addValueTag(sheet, PJNZParams)
    setRowOfYearVals(sheet, values, params, PJNZParams.currRow)
    addEndTag(sheet, PJNZParams) 

def export_ASFR(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<ASFR MV>')
    modvar = projection[DP_ASFRTag]

    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams, 'Age Distribution of Fertility (%) - Entered from keyboard')
    
    PJNZParams.currRow += 1
    addValueTag(sheet, PJNZParams)
    addValue(sheet, PJNZParams, GB_RW_DataStartCol, projection[DP_ASFRNumTag])
    
    for age in GBRange(DP_A15_19, DP_A45_49):
        PJNZParams.currRow += 1
        values = modvar[age]
        setRowOfYearVals(sheet, values, params, PJNZParams.currRow)

    addEndTag(sheet, PJNZParams) 

def export_UNPopASFR(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<UNPopASFR MV>')
    modvar = projection[DP_UNPopASFRTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)
    addValue(sheet, PJNZParams, GB_RW_DataStartCol, projection[DP_ASFRNumTag])
    
    for age in GBRange(DP_A15_19, DP_A45_49):
        PJNZParams.currRow += 1
        values = modvar[age]
        setRowOfYearVals(sheet, values, params, PJNZParams.currRow)

    addEndTag(sheet, PJNZParams)

def export_ASFRTables(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<ASFRTables MV>')
    modvar = projection[DP_ASFRTablesTag]
    
    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams, 'ASFR model tables')
    
    PJNZParams.currRow += 1
    addValueTag(sheet, PJNZParams)
    
    for m in GBRange(DP_ASFR_UNAfrica, DP_ASFR_Average):
        addNote(sheet, PJNZParams,  getASFRName(m))
        for r in GBRange(1, DP_ASFR_NumRows):
            for c in GBRange(1, DP_ASFR_NumCols):
                addValue(sheet, PJNZParams, GB_RW_DataStartCol + c - 1,  modvar[m][c][r])
            PJNZParams.currRow += 1
    
    PJNZParams.currRow -= 1
    addEndTag(sheet, PJNZParams)

def export_ASFRNum(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<ASFRNum MV>')
    modvar = projection[DP_ASFRNumTag]
    
    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams,  'Age Distribution of Fertility (%) - Using model table')
    
    PJNZParams.currRow += 1
    addValueTag(sheet, PJNZParams)
    addValue(sheet, PJNZParams, GB_RW_DataStartCol,  modvar)
    addEndTag(sheet, PJNZParams)
            
def export_ASFRCustomFlag(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<ASFRCustomFlag MV>')
    modvar = projection[DP_ASFRCustomFlagTag]
    
    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)
    addValue(sheet, PJNZParams, GB_RW_DataStartCol,  int(modvar))
    addEndTag(sheet, PJNZParams)

def export_SexBirthRatio(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<SexBirthRatio MV>')
    modvar = projection[DP_SexBirthRatioTag]

    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams,  'Birth ratio (male births per 100 female births)')

    PJNZParams.currRow += 1
    addValueTag(sheet, PJNZParams)
    values = modvar
    setRowOfYearVals(sheet, values, params, PJNZParams.currRow)  
    addEndTag(sheet, PJNZParams)  

def export_LE(sheet, params, PJNZParams, projection):   
    addStartTag(sheet, PJNZParams, '<LE MV2>')
    modvar = projection[DP_LETag]

    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams,  'Life expectancy')

    PJNZParams.currRow += 1
    addValueTag(sheet, PJNZParams)

    labels = {
        GB_Male : 'LE - Male - Input Assumption',
        GB_Female : 'LE - Female - Input Assumption',
    }
    
    for sex in GBRange(GB_Male, GB_Female):
        PJNZParams.currRow += 1    
        values = modvar[sex]
        addDescript(sheet, PJNZParams,  labels[sex])
        setRowOfYearVals(sheet, values, params, PJNZParams.currRow)
    
    addEndTag(sheet, PJNZParams)

def export_MigrRate(sheet, params, PJNZParams, projection):    
    addStartTag(sheet, PJNZParams, '<MigrRate MV2>')
    modvar = projection[DP_MigrRateTag]

    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams,  'Total net migrants per year')

    PJNZParams.currRow += 1
    addValueTag(sheet, PJNZParams)

    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams,  'Male Migration')

    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams,  'All ages')
    
    values = modvar[GB_Male][DP_AllAges]
    setRowOfYearVals(sheet, values, params, PJNZParams.currRow)
    
    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams,  'Female Migration')

    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams,  'All ages')
    
    values = modvar[GB_Female][DP_AllAges]
    setRowOfYearVals(sheet, values, params, PJNZParams.currRow)  
    
    addEndTag(sheet, PJNZParams)

def export_MigrAgeDist(sheet, params, PJNZParams, projection):    
    addStartTag(sheet, PJNZParams, '<MigrAgeDist MV2>')
    
    modvar = projection[DP_MigrAgeDistTag]

    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams,  'Percent distribution of migrants by age')

    PJNZParams.currRow += 1
    addValueTag(sheet, PJNZParams)
    
    PJNZParams.currRow += 1
            
    for sex in GBRange(GB_Male, GB_Female):
        addDescript(sheet, PJNZParams, getSexLabelSingular(sex) + ' Migration')
        for age in GBRange(DP_A0_4, DP_MAX_AGE):  
            values = modvar[sex][age]
            addNote(sheet, PJNZParams, GetAgeName2(age))
            setRowOfYearVals(sheet, values, params, PJNZParams.currRow)  
            PJNZParams.currRow += 1
            
    PJNZParams.currRow -= 1
            
    addEndTag(sheet, PJNZParams)

def export_CD4ThreshHold(sheet, params, PJNZParams, projection):    
    addStartTag(sheet, PJNZParams, '<CD4ThreshHold MV>')
    
    modvar = projection[AM_CD4ThreshHoldTag]

    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams,  'Eligibility for treatment - Children')

    PJNZParams.currRow += 1
    addValueTag(sheet, PJNZParams)
    
    for pernum in GBRange(DP_Number, DP_Percent):
        for age in GBRange(DP_AgeLT11Mths, DP_AgeGT5Years):
            values = modvar[pernum][age]
            setRowOfYearVals(sheet, values, params, PJNZParams.currRow)    
            PJNZParams.currRow += 1
        
    PJNZParams.currRow -= 1

    addEndTag(sheet, PJNZParams)

def export_PopsEligTreat(sheet, params, PJNZParams, projection):    
    addStartTag(sheet, PJNZParams, '<PopsEligTreat MV>')
    
    modvar = projection[AM_PopsEligTreatTag]

    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams,  'Populations eligible for treatment regardless of CD4 count - Adults')

    PJNZParams.currRow += 1
    addValueTag(sheet, PJNZParams)

    labels = {
        DP_EligTreatPregnantWomen : 'Pregnant women',
        DP_EligTreatTB_HIV : 'TB/HIV co-infected',
        DP_EligTreatDiscordantCouples : 'Discordant couples',
        DP_EligTreatSexWorkers : 'Sex workers',
        DP_EligTreatMSM : 'Men who have sex with men',
        DP_EligTreatIDU : 'Injecting drug users',
        DP_EligTreatOtherPop : 'Other population'
    }
    
    for pop in GBRange(1, DP_EligTreatPopsMax):
            PJNZParams.currRow += 1
            addDescript(sheet, PJNZParams, labels[pop]) 
            addValue(sheet, PJNZParams, GB_RW_DataStartCol,  int(modvar[pop]['Eligible']))
            addValue(sheet, PJNZParams, GB_RW_DataStartCol + 1,  modvar[pop]['PercentHIV'])
            addValue(sheet, PJNZParams, GB_RW_DataStartCol + 2,  modvar[pop]['Year'])
    
    addEndTag(sheet, PJNZParams)
            
def export_AgeHIVChildOnTreatment(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<AgeHIVChildOnTreatment MV>')
    
    modvar = projection[AM_AgeHIVChildOnTreatmentTag]

    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams,  'Age below which all HIV+ children should be on treatment (months)')

    PJNZParams.currRow += 1
    addValueTag(sheet, PJNZParams)

    values = modvar
    setRowOfYearVals(sheet, values, params, PJNZParams.currRow)   
    
    addEndTag(sheet, PJNZParams)
            
def export_CD4ThreshHoldAdults(sheet, params, PJNZParams, projection):
    format2(sheet, params, PJNZParams, projection, '<CD4ThreshHoldAdults MV>', AM_CD4ThreshHoldAdultsTag, 
            'CD4 count threshold for eligibility - Adults')

def export_InfantFeedingOptions(sheet, params, PJNZParams, projection):    
    addStartTag(sheet, PJNZParams, '<InfantFeedingOptions MV>')
    
    modvar = projection[AM_InfantFeedingOptionsTag]

    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams,  'Breastfeeding status by age')

    PJNZParams.currRow += 1
    addValueTag(sheet, PJNZParams)

    for id in GBRange(DP_NotInPMTCT, DP_InPMTCT):
        for r in GBRange(1, DP_InfantFeedingMths):
            values = modvar[r][id]
            setRowOfYearVals(sheet, values, params, PJNZParams.currRow)    
            PJNZParams.currRow += 1
      
    PJNZParams.currRow -= 1

    addEndTag(sheet, PJNZParams)

def export_ARVRegimen(sheet, params, PJNZParams, projection):    
    addStartTag(sheet, PJNZParams, '<ARVRegimen MV3>')
    
    modvar = projection[AM_ARVRegimenTag]
    
    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams,  'HIV+ pregnant women')

    PJNZParams.currRow += 1
    addValueTag(sheet, PJNZParams)

    #   (* No prophylaxis *)
    values = modvar[DP_PrenatalProphylaxis][DP_NoProphylaxis][DP_Percent]
    addNote(sheet, PJNZParams,  'No prophylaxis')
    addValue(sheet, PJNZParams, GB_RW_DataStartCol,  'Percent')
    setRowOfYearVals(sheet, values, params, PJNZParams.currRow, startCol = GB_RW_DataStartCol + 1)    
    PJNZParams.currRow += 1

    #   (* Single dose nevir *)
    values = modvar[DP_PrenatalProphylaxis][DP_SingleDoseNevir][DP_Number]
    addNote(sheet, PJNZParams,  'Single dose nevirapine')
    addValue(sheet, PJNZParams, GB_RW_DataStartCol,  'Number')
    setRowOfYearVals(sheet, values, params, PJNZParams.currRow, startCol = GB_RW_DataStartCol + 1)    
    PJNZParams.currRow += 1
    values = modvar[DP_PrenatalProphylaxis][DP_SingleDoseNevir][DP_Percent]
    addValue(sheet, PJNZParams, GB_RW_DataStartCol,  'Percent')
    setRowOfYearVals(sheet, values, params, PJNZParams.currRow, startCol = GB_RW_DataStartCol + 1)    
    PJNZParams.currRow += 1
    
    #   (* Dual ARV *)
    values = modvar[DP_PrenatalProphylaxis][DP_DualARV][DP_Number]
    addNote(sheet, PJNZParams,  'Dual ARV')
    addValue(sheet, PJNZParams, GB_RW_DataStartCol,  'Number')
    setRowOfYearVals(sheet, values, params, PJNZParams.currRow, startCol = GB_RW_DataStartCol + 1)    
    PJNZParams.currRow += 1
    values = modvar[DP_PrenatalProphylaxis][DP_DualARV][DP_Percent]
    addValue(sheet, PJNZParams, GB_RW_DataStartCol,  'Percent')
    setRowOfYearVals(sheet, values, params, PJNZParams.currRow, startCol = GB_RW_DataStartCol + 1)    
    PJNZParams.currRow += 1

    #   (* Option A - maternal *)
    values = modvar[DP_PrenatalProphylaxis][DP_OptA][DP_Number]
    addNote(sheet, PJNZParams,  'Option A - maternal')
    addValue(sheet, PJNZParams, GB_RW_DataStartCol,  'Number')
    setRowOfYearVals(sheet, values, params, PJNZParams.currRow, startCol = GB_RW_DataStartCol + 1)    
    PJNZParams.currRow += 1
    values = modvar[DP_PrenatalProphylaxis][DP_OptA][DP_Percent]
    addValue(sheet, PJNZParams, GB_RW_DataStartCol,  'Percent')
    setRowOfYearVals(sheet, values, params, PJNZParams.currRow, startCol = GB_RW_DataStartCol + 1)    
    PJNZParams.currRow += 1

    #   (* Option B - triple prophylaxis from 14 weeks *)
    values = modvar[DP_PrenatalProphylaxis][DP_OptB][DP_Number]
    addNote(sheet, PJNZParams,  'Option B - triple prophylaxis from 14 weeks')
    addValue(sheet, PJNZParams, GB_RW_DataStartCol,  'Number')
    setRowOfYearVals(sheet, values, params, PJNZParams.currRow, startCol = GB_RW_DataStartCol + 1)    
    PJNZParams.currRow += 1
    values = modvar[DP_PrenatalProphylaxis][DP_OptB][DP_Percent]
    addValue(sheet, PJNZParams, GB_RW_DataStartCol,  'Percent')
    setRowOfYearVals(sheet, values, params, PJNZParams.currRow, startCol = GB_RW_DataStartCol + 1)    
    PJNZParams.currRow += 1
    
    #   (* Triple ART started before pregnancy *)
    values = modvar[DP_PrenatalProphylaxis][DP_TripleARTBefPreg][DP_Number]
    addNote(sheet, PJNZParams,  'Option B+: ART started before current pregnancy')
    addValue(sheet, PJNZParams, GB_RW_DataStartCol,  'Number')
    setRowOfYearVals(sheet, values, params, PJNZParams.currRow, startCol = GB_RW_DataStartCol + 1)    
    PJNZParams.currRow += 1
    values = modvar[DP_PrenatalProphylaxis][DP_TripleARTBefPreg][DP_Percent]
    addValue(sheet, PJNZParams, GB_RW_DataStartCol,  'Percent')
    setRowOfYearVals(sheet, values, params, PJNZParams.currRow, startCol = GB_RW_DataStartCol + 1)    
    PJNZParams.currRow += 1
    
    #   (* Triple ART started during pregnancy *)
    values = modvar[DP_PrenatalProphylaxis][DP_TripleARTDurPreg][DP_Number]
    addNote(sheet, PJNZParams,  'Option B+: ART started during current pregnancy > 4 weeks before delivery')
    addValue(sheet, PJNZParams, GB_RW_DataStartCol,  'Number')
    setRowOfYearVals(sheet, values, params, PJNZParams.currRow, startCol = GB_RW_DataStartCol + 1)    
    PJNZParams.currRow += 1
    values = modvar[DP_PrenatalProphylaxis][DP_TripleARTDurPreg][DP_Percent]
    addValue(sheet, PJNZParams, GB_RW_DataStartCol,  'Percent')
    setRowOfYearVals(sheet, values, params, PJNZParams.currRow, startCol = GB_RW_DataStartCol + 1)    
    PJNZParams.currRow += 1
   
    #   (* Triple ART started during pregnancy - Late *)
    values = modvar[DP_PrenatalProphylaxis][DP_TripleARTDurPreg_Late][DP_Number]
    addNote(sheet, PJNZParams,  'Option B+: ART started during current pregnancy < 4 weeks before delivery')
    addValue(sheet, PJNZParams, GB_RW_DataStartCol,  'Number')
    setRowOfYearVals(sheet, values, params, PJNZParams.currRow, startCol = GB_RW_DataStartCol + 1)    
    PJNZParams.currRow += 1
    values = modvar[DP_PrenatalProphylaxis][DP_TripleARTDurPreg_Late][DP_Percent]
    addValue(sheet, PJNZParams, GB_RW_DataStartCol,  'Percent')
    setRowOfYearVals(sheet, values, params, PJNZParams.currRow, startCol = GB_RW_DataStartCol + 1)    
    PJNZParams.currRow += 1
    
    #   (* Total *)
    values = modvar[DP_PrenatalProphylaxis][DP_TotalTreat][DP_Number]
    addNote(sheet, PJNZParams,  'Total')
    addValue(sheet, PJNZParams, GB_RW_DataStartCol,  'Number')
    setRowOfYearVals(sheet, values, params, PJNZParams.currRow, startCol = GB_RW_DataStartCol + 1)    
    PJNZParams.currRow += 1
    
    #   (* Postnatal prophylaxis *)
    
    #   (* No prophylaxis *)
    values = modvar[DP_PostnatalProphylaxis][DP_NoProphylaxis][DP_Percent]
    addDescript(sheet, PJNZParams,  'Post natal prophylaxis for mothers or children among breastfeeding women or children not on ART')
    addNote(sheet, PJNZParams,  'No prophylaxis')
    addValue(sheet, PJNZParams, GB_RW_DataStartCol,  'Percent')
    setRowOfYearVals(sheet, values, params, PJNZParams.currRow, startCol = GB_RW_DataStartCol + 1)    
    PJNZParams.currRow += 1
    
    #   (* Option A *)
    values = modvar[DP_PostnatalProphylaxis][DP_OptA][DP_Number]
    addNote(sheet, PJNZParams,  'Option A')
    addValue(sheet, PJNZParams, GB_RW_DataStartCol,  'Number')
    setRowOfYearVals(sheet, values, params, PJNZParams.currRow, startCol = GB_RW_DataStartCol + 1)    
    PJNZParams.currRow += 1
    values = modvar[DP_PostnatalProphylaxis][DP_OptA][DP_Percent]
    addValue(sheet, PJNZParams, GB_RW_DataStartCol,  'Percent')
    setRowOfYearVals(sheet, values, params, PJNZParams.currRow, startCol = GB_RW_DataStartCol + 1)    
    PJNZParams.currRow += 1
    
    #   (* Option B *)
    values = modvar[DP_PostnatalProphylaxis][DP_OptB][DP_Number]
    addNote(sheet, PJNZParams,  'Option B')
    addValue(sheet, PJNZParams, GB_RW_DataStartCol,  'Number')
    setRowOfYearVals(sheet, values, params, PJNZParams.currRow, startCol = GB_RW_DataStartCol + 1)    
    PJNZParams.currRow += 1
    values = modvar[DP_PostnatalProphylaxis][DP_OptB][DP_Percent]
    addValue(sheet, PJNZParams, GB_RW_DataStartCol,  'Percent')
    setRowOfYearVals(sheet, values, params, PJNZParams.currRow, startCol = GB_RW_DataStartCol + 1)    
    PJNZParams.currRow += 1
    
    #   (* Total *)
    values = modvar[DP_PostnatalProphylaxis][DP_TotalTreat][DP_Number]
    addNote(sheet, PJNZParams,  'Total')
    addValue(sheet, PJNZParams, GB_RW_DataStartCol,  'Number')
    setRowOfYearVals(sheet, values, params, PJNZParams.currRow, startCol = GB_RW_DataStartCol + 1)    
    PJNZParams.currRow += 1

    #   (* Option A *)
    values = modvar[DP_AnnDropPostnatalProph][DP_OptA][DP_Percent]
    addDescript(sheet, PJNZParams,  'Monthly drop-out rate of postnatal prophylaxis')
    addNote(sheet, PJNZParams,  'Option A')
    addValue(sheet, PJNZParams, GB_RW_DataStartCol,  'Percent')
    setRowOfYearVals(sheet, values, params, PJNZParams.currRow, startCol = GB_RW_DataStartCol + 1)    
    PJNZParams.currRow += 1

    #   (* Option B *)
    values = modvar[DP_AnnDropPostnatalProph][DP_OptB][DP_Percent]
    addNote(sheet, PJNZParams,  'Option B')
    addValue(sheet, PJNZParams, GB_RW_DataStartCol,  'Percent')
    setRowOfYearVals(sheet, values, params, PJNZParams.currRow, startCol = GB_RW_DataStartCol + 1)    
    PJNZParams.currRow += 1
    
    #   (* ART 0-12 months BF *)
    values = modvar[DP_AnnDropPostnatalProph][DP_ART0_12MthsBF][DP_Percent]
    addNote(sheet, PJNZParams,  'ART 0-12 months breastfeeding')
    addValue(sheet, PJNZParams, GB_RW_DataStartCol,  'Percent')
    setRowOfYearVals(sheet, values, params, PJNZParams.currRow, startCol = GB_RW_DataStartCol + 1)    
    PJNZParams.currRow += 1

    #   (* ART 12+ months BF *)
    values = modvar[DP_AnnDropPostnatalProph][DP_ARTGT12MthsBF][DP_Percent]
    addNote(sheet, PJNZParams,  'ART 12+ months breastfeeding')
    addValue(sheet, PJNZParams, GB_RW_DataStartCol,  'Percent')
    setRowOfYearVals(sheet, values, params, PJNZParams.currRow, startCol = GB_RW_DataStartCol + 1)    
    
    addEndTag(sheet, PJNZParams)

def export_PatientsReallocated(sheet, params, PJNZParams, projection):
    format2(sheet, params, PJNZParams, projection, '<DP_TGX_PatientsReallocated_MV>', AM_PatientsReallocatedTag, 'HIV+ pregnant women')

def export_PercentARTDelivery(sheet, params, PJNZParams, projection):    
    addStartTag(sheet, PJNZParams, '<PercentARTDelivery MV>')
    
    modvar = projection[AM_PercentARTDeliveryTag]
    
    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams,  'HIV+ pregnant women')

    PJNZParams.currRow += 1
    addValueTag(sheet, PJNZParams)

    values = modvar
    for i in GBRange(DP_OnARTAtDelivery, DP_StartingARTAtDelivery):  
        values = modvar[i]
        setRowOfYearVals(sheet, values, params, PJNZParams.currRow) 
        PJNZParams.currRow += 1
        
    PJNZParams.currRow -= 1

    addEndTag(sheet, PJNZParams)

def export_PregTermAbortionPerNum(sheet, params, PJNZParams, projection):
    format2(sheet, params, PJNZParams, projection, '<PregTermAbortionPerNum MV2>', AM_PregTermAbortionPerNumTag, 
            'Percent of pregnancies to HIV+ women terminated by abortion - Number or Percent')

def export_PregTermAbortion(sheet, params, PJNZParams, projection):
    format2(sheet, params, PJNZParams, projection, '<PregTermAbortion MV3>', AM_PregTermAbortionTag, 'HIV+ pregnant women')

def export_MedCD4CountInit(sheet, params, PJNZParams, projection):
    format2(sheet, params, PJNZParams, projection, '<MedCD4CountInit MV>', AM_MedCD4CountInitTag, 'Median CD4 count at ART initiation')

def export_PercLostFollowup(sheet, params, PJNZParams, projection):
    format2(sheet, params, PJNZParams, projection, '<PercLostFollowup MV>', AM_PercInterruptedTag, 'Number of adults receiving ART')

def export_NumberInitTreatmentReinit(sheet, params, PJNZParams, projection):
    format2(sheet, params, PJNZParams, projection, '<NumberInitTreatmentReinits MV>', AM_NumberInitTreatmentReinitsTag)

def export_NumNewlyInitART(sheet, params, PJNZParams, projection):   
    addStartTag(sheet, PJNZParams, '<NumNewlyInitART MV>')
    
    modvar = projection[AM_NumNewlyInitARTTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)

    for sex in GBRange(GB_Male, GB_Female):
        values = modvar[sex]
        addNote(sheet, PJNZParams,  getSexLabel(sex))
        setRowOfYearVals(sheet, values, params, PJNZParams.currRow)    
        PJNZParams.currRow += 1
        
    PJNZParams.currRow -= 1
    addEndTag(sheet, PJNZParams)

def export_PercLostFollowupChild(sheet, params, PJNZParams, projection):
    format2(sheet, params, PJNZParams, projection, '<PercLostFollowupChild MV>', AM_PercInterruptedChildTag, 'Number of children receiving ART')

def export_NumberInitTreatmentReinitsChild(sheet, params, PJNZParams, projection):
    format2(sheet, params, PJNZParams, projection, '<NumberInitTreatmentReinitsChild MV>', AM_NumberInitTreatmentReinitsChildTag)

def export_NumNewlyInitARTChild(sheet, params, PJNZParams, projection):
    format2(sheet, params, PJNZParams, projection, '<NumNewlyInitARTChild MV>', AM_NumNewlyInitARTChildTag)

def export_HAARTBySex(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<HAARTBySex MV>')
    
    modvar = projection[AM_HAARTBySexTag]

    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams,  'Number of adults receiving ART')

    PJNZParams.currRow += 1
    addValueTag(sheet, PJNZParams)

    for sex in GBRange(GB_BothSexes, GB_Female):
        PJNZParams.currRow += 1
        values = modvar[sex]
        addDescript(sheet, PJNZParams,  getSexLabel(sex))
        setRowOfYearVals(sheet, values, params, PJNZParams.currRow)  
    
    addEndTag(sheet, PJNZParams)

def export_HAARTBySexPerNum(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<HAARTBySexPerNum MV>')
    
    modvar = projection[AM_HAARTBySexPerNumTag]

    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams,  'Number of Adults receiving ART / Percent of adults in need receiving ART - Number or Percent')

    PJNZParams.currRow += 1
    addValueTag(sheet, PJNZParams)

    for sex in GBRange(GB_BothSexes, GB_Female):
        PJNZParams.currRow += 1
        values = modvar[sex]
        addDescript(sheet, PJNZParams,  getSexLabel(sex))
        setRowOfYearVals(sheet, values, params, PJNZParams.currRow)  
    
    addEndTag(sheet, PJNZParams)

def export_AdultARTAdjFactor(sheet, params, PJNZParams, projection):   
    addStartTag(sheet, PJNZParams, '<AdultARTAdjFactor>')
    
    modvar = projection[AM_AdultARTAdjFactorTag]

    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams,  '')

    PJNZParams.currRow += 1
    addValueTag(sheet, PJNZParams)

    for sex in GBRange(GB_Male, GB_Female):
        PJNZParams.currRow += 1
        values = modvar[sex]
        addDescript(sheet, PJNZParams,  getSexLabel(sex))
        setRowOfYearVals(sheet, values, params, PJNZParams.currRow)  
    
    addEndTag(sheet, PJNZParams)

def export_AdultPatsAllocToFromOtherRegion(sheet, params, PJNZParams, projection):   
    addStartTag(sheet, PJNZParams, '<AdultPatsAllocToFromOtherRegion>')
    
    modvar = projection[AM_AdultPatsAllocToFromOtherRegionTag]

    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams,  '')

    PJNZParams.currRow += 1
    addValueTag(sheet, PJNZParams)

    for sex in GBRange(GB_Male, GB_Female):
        PJNZParams.currRow += 1
        values = modvar[sex]
        addDescript(sheet, PJNZParams,  getSexLabel(sex))
        setRowOfYearVals(sheet, values, params, PJNZParams.currRow)  
    
    addEndTag(sheet, PJNZParams)
        
def export_AdultARTAdjFactorFlag(sheet, params, PJNZParams, projection):   
    addStartTag(sheet, PJNZParams, '<AdultARTAdjFactorFlag>')
    
    modvar = projection[AM_AdultARTAdjFactorFlagTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)
    addValue(sheet, PJNZParams, GB_RW_DataStartCol, int(modvar))
    
    addEndTag(sheet, PJNZParams)

def export_CD4Coverage(sheet, params, PJNZParams, projection):   
    addStartTag(sheet, PJNZParams, '<CD4Coverage MV2>')
    
    modvar = projection[AM_CD4CoverageTag]
    
    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams,  'Coverage of ART by CD4 count category')

    PJNZParams.currRow += 1
    addValueTag(sheet, PJNZParams)

    labels = {
        DP_CD4_GT500    : '> 500',
        DP_CD4_350_500  : '350 - 500',
        DP_CD4_250_349  : '250 - 349',
        DP_CD4_200_249  : '200 - 249',
        DP_CD4_100_199  : '100 - 199',
        DP_CD4_50_99    : '50 - 99',
        DP_CD4_LT50     : '< 50'
    }

    for perNum in GBRange(DP_CD4Percent, DP_CD4Number):
        PJNZParams.currRow += 1
        for i in GBRange(DP_CD4_GT500, DP_CD4_LT50):
            values = modvar[perNum][i]
            addDescript(sheet, PJNZParams,  labels[i])
            setRowOfYearVals(sheet, values, params, PJNZParams.currRow)    
            PJNZParams.currRow += 1
           
    PJNZParams.currRow -= 1
    addEndTag(sheet, PJNZParams)

def export_ARTByAgeInputType(sheet, params, PJNZParams, projection):   
    addStartTag(sheet, PJNZParams, '<ARTByAgeInputType MV>')
    
    modvar = projection[AM_ARTByAgeInputTypeTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)
    addValue(sheet, PJNZParams, GB_RW_DataStartCol, modvar)
    
    addEndTag(sheet, PJNZParams)

def export_ARTByAge5YearAG(sheet, params, PJNZParams, projection):   
    addStartTag(sheet, PJNZParams, '<ARTByAge5YearAG MV>')
    
    modvar = projection[AM_ARTByAge5YearAGTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)

    for sex in GBRange(GB_Male, GB_Female):
        for age in GBRange(DP_A0_4, DP_A80_Up):  
            PJNZParams.currRow += 1
            values = modvar[sex][age]
            setRowOfYearVals(sheet, values, params, PJNZParams.currRow)  
    
    addEndTag(sheet, PJNZParams)

def export_ARTByAgeGAMAG(sheet, params, PJNZParams, projection):   
    addStartTag(sheet, PJNZParams, '<ARTByAgeGAMAG MV>')
    
    modvar = projection[AM_ARTByAgeGAMAGTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)

    for sex in GBRange(GB_Male, GB_Female):
        for age in GBRange(DP_A0_4, DP_GAMAG_A50Plus):
            PJNZParams.currRow += 1
            values = modvar[sex][age]
            setRowOfYearVals(sheet, values, params, PJNZParams.currRow)    
    
    addEndTag(sheet, PJNZParams)

def export_CovPopsEligTreat(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<CovPopsEligTreat MV>')
    
    modvar = projection[AM_CovPopsEligTreatTag]

    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams,  'ART coverage for populations eligible for treatment regardless of CD4 count')

    PJNZParams.currRow += 1
    addValueTag(sheet, PJNZParams)

    labels = {
        DP_EligTreatPregnantWomen       : 'Pregnant women',
        DP_EligTreatTB_HIV              : 'TB/HIV co-infected',
        DP_EligTreatDiscordantCouples   : 'Discordant couples',
        DP_EligTreatSexWorkers          : 'Sex workers',
        DP_EligTreatMSM                 : 'Men who have sex with men',
        DP_EligTreatIDU                 : 'Injecting drug users',
        DP_EligTreatOtherPop            : 'Other population'
    }

    for pop in GBRange(DP_EligTreatPregnantWomen, DP_EligTreatPopsMax):    
        PJNZParams.currRow += 1
        values = modvar[pop]
        addDescript(sheet, PJNZParams,  labels[pop])
        setRowOfYearVals(sheet, values, params, PJNZParams.currRow)
    
    addEndTag(sheet, PJNZParams)

def export_ChildTreatInputs(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<ChildTreatInputs MV3>')
    
    modvar = projection[AM_ChildTreatInputsTag]
    
    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams,  'Number of children receiving ART')

    PJNZParams.currRow += 1
    addValueTag(sheet, PJNZParams)

    for id in GBRange(DP_PerChildHIVPosCot, DP_PerChildHIVRecART10_14):
        values = modvar[id]
        setRowOfYearVals(sheet, values, params, PJNZParams.currRow)    
        PJNZParams.currRow += 1
       
    PJNZParams.currRow -= 1
    addEndTag(sheet, PJNZParams)

def export_ChildARTAdjFactor(sheet, params, PJNZParams, projection):
    format2(sheet, params, PJNZParams, projection, '<ChildARTAdjFactor MV>', AM_ChildARTAdjFactorTag)

def export_ChildARTAdjFactorFlag(sheet, params, PJNZParams, projection):   
    addStartTag(sheet, PJNZParams, '<ChildARTAdjFactorFlag>')
    
    modvar = projection[AM_ChildARTAdjFactorFlagTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)
    addValue(sheet, PJNZParams, GB_RW_DataStartCol,  int(modvar))
    
    addEndTag(sheet, PJNZParams)

def export_ChildARTByAgeGroupPerNum(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<ChildARTByAgeGroupPerNum MV2>')
    
    modvar = projection[AM_ChildARTByAgeGroupPerNumTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)

    for id in GBRange(DP_PerChildHIVPosCot, DP_PerChildHIVRecART10_14):
        values = modvar[id]
        setRowOfYearVals(sheet, values, params, PJNZParams.currRow)    
        PJNZParams.currRow += 1 
    
    PJNZParams.currRow -= 1    
    addEndTag(sheet, PJNZParams)

def export_ANCTestingValues(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<ANCTestingValues MV4>')
    
    modvar = projection[AM_ANCTestingValuesTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)

    for id in GBRange(DP_FirstANCVisits, DP_HIVNegFirstANCVisit):
        values = modvar[id]
        setRowOfYearVals(sheet, values, params, PJNZParams.currRow)    
        PJNZParams.currRow += 1
        
    PJNZParams.currRow -= 1
    addEndTag(sheet, PJNZParams)

# def export_NetMigrationPLHIV(sheet, params, PJNZParams, projection):   
#     addStartTag(sheet, PJNZParams, '<NetMigrationPLHIV MV>')
#     modvar = projection[AM_NetMigrationPLHIVTag]

#     PJNZParams.currRow += 3
#     for sex in GBRange(GB_Male, GB_Female):
#         for age in GBRange(DP_A0_4, DP_A80_Up):
#             values = modvar[sex][age]
#             setRowOfYearVals(sheet, values, params, PJNZParams.currRow)    
#             PJNZParams.currRow += 1

# def export_NewInfectionsLessImmigrants(sheet, params, PJNZParams, projection):   
#     addStartTag(sheet, PJNZParams, '<NewInfectionsLessImmigrants MV>')
    
#     modvar = projection[AM_NewInfectionsLessImmigrantsTag]

#     PJNZParams.currRow += 2
#     addValueTag(sheet, PJNZParams)

#     for sex in GBRange(GB_BothSexes, GB_Female):                                     #old all single-ages sum row
#         for age in GBRange(0, 81):  
#             PJNZParams.currRow += 1
#             if age <= 80:
#                 values = modvar[sex][age]
#             else:
#                 values = [0] * len(modvar[sex][0])
#             setRowOfYearVals(sheet, values, params, PJNZParams.currRow)
    
#     addEndTag(sheet, PJNZParams)
            
def export_HIVTesting(sheet, params, PJNZParams, projection):   
    addStartTag(sheet, PJNZParams, '<HIVTesting MV3>')
    
    modvar = projection[AM_HIVTestingTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)
    PJNZParams.currRow += 1
    
    # setRowOfYearVals(sheet, [rec['DiagTests'] for rec in modvar], params, PJNZParams.currRow)  
    # setRowOfYearVals(sheet, [rec['PosTests'] for rec in modvar], params, PJNZParams.currRow + 1)  
    # setRowOfYearVals(sheet, [rec['HTSTests'] for rec in modvar], params, PJNZParams.currRow + 2)  
    # setRowOfYearVals(sheet, [rec['PosHTSTests'] for rec in modvar], params, PJNZParams.currRow + 3)  
    # setRowOfYearVals(sheet, [rec['ANCTests'] for rec in modvar], params, PJNZParams.currRow + 4)  
    # setRowOfYearVals(sheet, [rec['PosANCTests'] for rec in modvar], params, PJNZParams.currRow + 5)  
    # setRowOfYearVals(sheet, [rec['SelfTests'] for rec in modvar], params, PJNZParams.currRow + 6)   
    # setRowOfYearVals(sheet, [rec['IndexPartnerTests'] for rec in modvar], params, PJNZParams.currRow + 7) 

    addNoteAtRow(sheet, PJNZParams.currRow + 0, 'DiagTests')
    addNoteAtRow(sheet, PJNZParams.currRow + 1, 'PosTests')
    addNoteAtRow(sheet, PJNZParams.currRow + 2, 'HTSTests')
    addNoteAtRow(sheet, PJNZParams.currRow + 3, 'PosHTSTests')
    addNoteAtRow(sheet, PJNZParams.currRow + 4, 'ANCTests')
    addNoteAtRow(sheet, PJNZParams.currRow + 5, 'PosANCTests')
    addNoteAtRow(sheet, PJNZParams.currRow + 6, 'CommunityBasedTests')
    addNoteAtRow(sheet, PJNZParams.currRow + 7, 'CommunityBasedTestsHIVPos')
    addNoteAtRow(sheet, PJNZParams.currRow + 8, 'SelfTests')
    addNoteAtRow(sheet, PJNZParams.currRow + 9, 'TestsChild0t14')
    addNoteAtRow(sheet, PJNZParams.currRow + 10, 'TestsMen15Plus')
    addNoteAtRow(sheet, PJNZParams.currRow + 11, 'TestsFemale15Plus')
    addNoteAtRow(sheet, PJNZParams.currRow + 12, 'TestsTrans15Plus')
    addNoteAtRow(sheet, PJNZParams.currRow + 13, 'TestsHIVPosChild0t14')
    addNoteAtRow(sheet, PJNZParams.currRow + 14, 'TestsHIVPosMen15Plus')
    addNoteAtRow(sheet, PJNZParams.currRow + 15, 'TestsHIVPosFemale15Plus')
    addNoteAtRow(sheet, PJNZParams.currRow + 16, 'TestsHIVPosTrans15Plus')

    setRowOfYearVals(sheet, [rec['DiagTests'] for rec in modvar], params, PJNZParams.currRow)  
    setRowOfYearVals(sheet, [rec['PosTests'] for rec in modvar], params, PJNZParams.currRow + 1)  
    setRowOfYearVals(sheet, [rec['HTSTests'] for rec in modvar], params, PJNZParams.currRow + 2)  
    setRowOfYearVals(sheet, [rec['PosHTSTests'] for rec in modvar], params, PJNZParams.currRow + 3)  
    setRowOfYearVals(sheet, [rec['ANCTests'] for rec in modvar], params, PJNZParams.currRow + 4)  
    setRowOfYearVals(sheet, [rec['PosANCTests'] for rec in modvar], params, PJNZParams.currRow + 5)  
    setRowOfYearVals(sheet, [rec['CommunityBasedTests'] for rec in modvar], params, PJNZParams.currRow + 6)   
    setRowOfYearVals(sheet, [rec['CommunityBasedTestsHIVPos'] for rec in modvar], params, PJNZParams.currRow + 7)   
    setRowOfYearVals(sheet, [rec['SelfTests'] for rec in modvar], params, PJNZParams.currRow + 8)
    setRowOfYearVals(sheet, [rec['TestsChild0t14'] for rec in modvar], params, PJNZParams.currRow + 9)
    setRowOfYearVals(sheet, [rec['TestsMen15Plus'] for rec in modvar], params, PJNZParams.currRow + 10)
    setRowOfYearVals(sheet, [rec['TestsFemale15Plus'] for rec in modvar], params, PJNZParams.currRow + 11)
    setRowOfYearVals(sheet, [rec['TestsTrans15Plus'] for rec in modvar], params, PJNZParams.currRow + 12)
    setRowOfYearVals(sheet, [rec['TestsHIVPosChild0t14'] for rec in modvar], params, PJNZParams.currRow + 13)
    setRowOfYearVals(sheet, [rec['TestsHIVPosMen15Plus'] for rec in modvar], params, PJNZParams.currRow + 14)
    setRowOfYearVals(sheet, [rec['TestsHIVPosFemale15Plus'] for rec in modvar], params, PJNZParams.currRow + 15)
    setRowOfYearVals(sheet, [rec['TestsHIVPosTrans15Plus'] for rec in modvar], params, PJNZParams.currRow + 16)

    PJNZParams.currRow += 16
    
    addEndTag(sheet, PJNZParams) 

def export_HIVTestingHTSTestsByAge(sheet, params, PJNZParams, projection):   
    addStartTag(sheet, PJNZParams, '<HIVTestingHTSTestsByAge MV>')
    
    modvar = projection[AM_HIVTestingHTSTestsByAgeTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)

    for s in GBRange(GB_Male, GB_Female):
        for a in GBRange(DP_AllAges, DP_GAMAG_A50Plus):    
            PJNZParams.currRow += 1
            values = modvar[s][a]
            setRowOfYearVals(sheet, values, params, PJNZParams.currRow)
    
    addEndTag(sheet, PJNZParams)

def export_Shiny90SurveyData(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<Shiny90SurveyData MV>')
    
    modvar = projection[AM_Shiny90SurveyDataTag]
    
    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)
    addNote(sheet, PJNZParams,  len(modvar))
  
    for s in GBRange(1, len(modvar)):
        PJNZParams.currRow += 1
        sheetInsertRow(
            sheet, PJNZParams.currRow,
            [
                int(modvar[s-1]['isUsed']),
                modvar[s-1]['surveyID'],
                modvar[s-1]['year'],
                modvar[s-1]['ageGroup'],
                modvar[s-1]['sex'],
                modvar[s-1]['HIVStatus'],
                modvar[s-1]['estimate'],
                modvar[s-1]['standardError'],
                modvar[s-1]['lowerBound'],
                modvar[s-1]['upperBound'],
                modvar[s-1]['count']
            ], 
            1
        )
    
    addEndTag(sheet, PJNZParams)

def export_Shiny90ProgramData(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<Shiny90ProgramData MV>')
    
    modvar = projection[AM_Shiny90ProgramDataTag]
    
    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)
    addNote(sheet, PJNZParams, len(modvar))

    for s in GBRange(1, len(modvar)):
        PJNZParams.currRow += 1
        sheetInsertRow(
            sheet, 
            PJNZParams.currRow,
            [
                str(int(modvar[s-1].get('isUsed', 0))),
                str(modvar[s-1]['year']),
                str(modvar[s-1]['sex']),
                str(modvar[s-1]['totalTests']),
                str(modvar[s-1]['totalPosTests']),
                str(modvar[s-1]['totalHTCTests']),
                str(modvar[s-1]['totalPosHTCTests']),
                str(modvar[s-1]['totalANCTests']),
                str(modvar[s-1]['totalPosANCTests'])
            ], 
            1
        )
        pass
    
    addEndTag(sheet, PJNZParams)

def export_Shiny90AIDSDeathsFYear(sheet, params, PJNZParams, projection):   
    addStartTag(sheet, PJNZParams, '<Shiny90AIDSDeathsFYear MV>')
    
    modvar = projection[AM_Shiny90AIDSDeathsFYearTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)
    addValue(sheet, PJNZParams, GB_RW_DataStartCol,  modvar)
    
    addEndTag(sheet, PJNZParams)

def export_Shiny90Pop(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<Shiny90Pop MV>')
    
    modvar = projection[AM_Shiny90PopTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)

    for HIV in GBRange(DP_D_All, DP_D_HIVPos):
        for sex in GBRange(GB_BothSexes, GB_Female):
            for age in GBRange(DP_S90_15_24, DP_S90_15Plus):
                for dataType in GBRange(DP_Number, DP_UpperBound):  
                    values = modvar[HIV][sex][age][dataType]
                    setRowOfYearVals(sheet, values, params, PJNZParams.currRow) 
                    PJNZParams.currRow += 1 
    
    PJNZParams.currRow -= 1
    addEndTag(sheet, PJNZParams)

def export_Shiny90NumTests(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<Shiny90NumTests MV>')
    
    modvar = projection[AM_Shiny90NumTestsTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)

    for HIV in GBRange(DP_D_All, DP_D_HIVPos):
        for sex in GBRange(GB_BothSexes, GB_Female):
            for age in GBRange(DP_S90_15_24, DP_S90_15Plus):
                for dataType in GBRange(DP_Number, DP_UpperBound):
                    values = modvar[HIV][sex][age][dataType]
                    setRowOfYearVals(sheet, values, params, PJNZParams.currRow)    
                    PJNZParams.currRow += 1
    
    PJNZParams.currRow -= 1
    addEndTag(sheet, PJNZParams)

def export_Shiny90NumTested12M(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<Shiny90NumTested12M MV>')
    
    modvar = projection[AM_Shiny90NumTested12MTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)

    for HIV in GBRange(DP_D_All, DP_D_HIVPos):
        for sex in GBRange(GB_BothSexes, GB_Female):
            for age in GBRange(DP_S90_15_24, DP_S90_15Plus):
                for dataType in GBRange(DP_Number, DP_UpperBound):
                    values = modvar[HIV][sex][age][dataType]
                    setRowOfYearVals(sheet, values, params, PJNZParams.currRow)    
                    PJNZParams.currRow += 1
    
    PJNZParams.currRow -= 1
    addEndTag(sheet, PJNZParams)

def export_Shiny90TotalTests(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<Shiny90TotalTests MV>')
    
    modvar = projection[AM_Shiny90TotalTestsTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)

    for HIV in GBRange(DP_D_All, DP_D_HIVPos):
        for sex in GBRange(GB_BothSexes, GB_Female):
            for age in GBRange(DP_S90_15_24, DP_S90_15Plus):
                for dataType in GBRange(DP_Number, DP_UpperBound):
                    values = modvar[HIV][sex][age][dataType]
                    setRowOfYearVals(sheet, values, params, PJNZParams.currRow)    
                    PJNZParams.currRow += 1
    
    PJNZParams.currRow -= 1
    addEndTag(sheet, PJNZParams)

def export_Shiny90EverTested(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<Shiny90EverTested MV>')
    
    modvar = projection[AM_Shiny90EverTestedTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)

    for HIV in GBRange(DP_D_All, DP_D_HIVPos):
        for sex in GBRange(GB_BothSexes, GB_Female):
            for age in GBRange(DP_S90_15_24, DP_S90_15Plus):
                for dataType in GBRange(DP_Number, DP_UpperBound):
                    values = modvar[HIV][sex][age][dataType]
                    setRowOfYearVals(sheet, values, params, PJNZParams.currRow)    
                    PJNZParams.currRow += 1
    
    PJNZParams.currRow -= 1
    addEndTag(sheet, PJNZParams)

def export_Shiny90Diagnosed(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<Shiny90Diagnosed MV>')
    
    modvar = projection[AM_Shiny90DiagnosedTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)

    for HIV in GBRange(DP_D_All, DP_D_HIVPos):
        for sex in GBRange(GB_BothSexes, GB_Female):
            for age in GBRange(DP_S90_15_24, DP_S90_15Plus):
                for dataType in GBRange(DP_Number, DP_UpperBound):
                    values = modvar[HIV][sex][age][dataType]
                    setRowOfYearVals(sheet, values, params, PJNZParams.currRow)    
                    PJNZParams.currRow += 1
    
    PJNZParams.currRow -= 1
    addEndTag(sheet, PJNZParams)

def export_Shiny90NumAware(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<Shiny90NumberAware MV>')
    
    modvar = projection[AM_Shiny90NumAwareTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)

    for HIV in GBRange(DP_D_All, DP_D_HIVPos):
        for sex in GBRange(GB_BothSexes, GB_Female):
            for age in GBRange(DP_S90_15_24, DP_S90_15Plus):
                for dataType in GBRange(DP_Number, DP_UpperBound):
                    values = modvar[HIV][sex][age][dataType]
                    setRowOfYearVals(sheet, values, params, PJNZParams.currRow)    
                    PJNZParams.currRow += 1
    
    PJNZParams.currRow -= 1
    addEndTag(sheet, PJNZParams)

def export_Shiny90NumDiagnoses(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<Shiny90NumDiagnoses MV>')
    
    modvar = projection[AM_Shiny90NumDiagnosesTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)

    for HIV in GBRange(DP_D_All, DP_D_HIVPos):
        for sex in GBRange(GB_BothSexes, GB_Female):
            for age in GBRange(DP_S90_15_24, DP_S90_15Plus):
                for dataType in GBRange(DP_Number, DP_UpperBound):
                    values = modvar[HIV][sex][age][dataType]
                    setRowOfYearVals(sheet, values, params, PJNZParams.currRow)    
                    PJNZParams.currRow += 1
    
    PJNZParams.currRow -= 1
    addEndTag(sheet, PJNZParams)

def export_Shiny90NumDiagnosesMod(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<Shiny90NumDiagnosesMod MV>')
    
    modvar = projection[AM_Shiny90NumDiagnosesModTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)

    for HIV in GBRange(DP_D_All, DP_D_HIVPos):
        for sex in GBRange(GB_BothSexes, GB_Female):
            for age in GBRange(DP_S90_15_24, DP_S90_15Plus):
                for dataType in GBRange(DP_Number, DP_UpperBound):
                    values = modvar[HIV][sex][age][dataType]
                    setRowOfYearVals(sheet, values, params, PJNZParams.currRow)    
                    PJNZParams.currRow += 1
    
    PJNZParams.currRow -= 1
    addEndTag(sheet, PJNZParams)

def export_Shiny90NumLateDiagnoses(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<Shiny90NumLateDiagnoses MV>')
    
    modvar = projection[AM_Shiny90NumLateDiagnosesTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)

    for HIV in GBRange(DP_D_All, DP_D_HIVPos):
        for sex in GBRange(GB_BothSexes, GB_Female):
            for age in GBRange(DP_S90_15_24, DP_S90_15Plus):
                for dataType in GBRange(DP_Number, DP_UpperBound):
                    values = modvar[HIV][sex][age][dataType]
                    setRowOfYearVals(sheet, values, params, PJNZParams.currRow)    
                    PJNZParams.currRow += 1
    
    PJNZParams.currRow -= 1
    addEndTag(sheet, PJNZParams)

def export_Shiny90NotDiagHIV1Yr(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<Shiny90NotDiagHIV1Yr MV>')
    
    modvar = projection[AM_Shiny90NotDiagHIV1YrTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)

    for HIV in GBRange(DP_D_All, DP_D_HIVPos):
        for sex in GBRange(GB_BothSexes, GB_Female):
            for age in GBRange(DP_S90_15_24, DP_S90_15Plus):
                for dataType in GBRange(DP_Number, DP_UpperBound):
                    values = modvar[HIV][sex][age][dataType]
                    setRowOfYearVals(sheet, values, params, PJNZParams.currRow)    
                    PJNZParams.currRow += 1
    
    PJNZParams.currRow -= 1
    addEndTag(sheet, PJNZParams)

def export_Shiny90NumReTestHIVNeg(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<Shiny90NumReTestHIVNeg MV>')
    
    modvar = projection[AM_Shiny90NumReTestHIVNeg_Tag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)

    for HIV in GBRange(DP_D_All, DP_D_HIVPos):
        for sex in GBRange(GB_BothSexes, GB_Female):
            for age in GBRange(DP_S90_15_24, DP_S90_15Plus):
                for dataType in GBRange(DP_Number, DP_UpperBound):
                    values = modvar[HIV][sex][age][dataType]
                    setRowOfYearVals(sheet, values, params, PJNZParams.currRow)    
                    PJNZParams.currRow += 1
    
    PJNZParams.currRow -= 1
    addEndTag(sheet, PJNZParams)

def export_Shiny90NumFirstTestHIVNeg(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<Shiny90NumFirstTestHIVNeg MV>')
    
    modvar = projection[AM_Shiny90NumFirstTestHIVNeg_Tag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)

    for HIV in GBRange(DP_D_All, DP_D_HIVPos):
        for sex in GBRange(GB_BothSexes, GB_Female):
            for age in GBRange(DP_S90_15_24, DP_S90_15Plus):
                for dataType in GBRange(DP_Number, DP_UpperBound):
                    values = modvar[HIV][sex][age][dataType]
                    setRowOfYearVals(sheet, values, params, PJNZParams.currRow)    
                    PJNZParams.currRow += 1
    
    PJNZParams.currRow -= 1
    addEndTag(sheet, PJNZParams)

def export_Shiny90NumRetestPLHIVOnART(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<Shiny90NumRetestPLHIVOnART MV>')
    
    modvar = projection[AM_Shiny90NumRetestPLHIVOnART_Tag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)

    for HIV in GBRange(DP_D_All, DP_D_HIVPos):
        for sex in GBRange(GB_BothSexes, GB_Female):
            for age in GBRange(DP_S90_15_24, DP_S90_15Plus):
                for dataType in GBRange(DP_Number, DP_UpperBound):
                    values = modvar[HIV][sex][age][dataType]
                    setRowOfYearVals(sheet, values, params, PJNZParams.currRow)    
                    PJNZParams.currRow += 1
    
    PJNZParams.currRow -= 1
    addEndTag(sheet, PJNZParams)

def export_Shiny90NumRetestPLHIVNoART(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<Shiny90NumRetestPLHIVNoART MV>')
    
    modvar = projection[AM_Shiny90NumRetestPLHIVNoART_Tag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)

    for HIV in GBRange(DP_D_All, DP_D_HIVPos):
        for sex in GBRange(GB_BothSexes, GB_Female):
            for age in GBRange(DP_S90_15_24, DP_S90_15Plus):
                for dataType in GBRange(DP_Number, DP_UpperBound):
                    values = modvar[HIV][sex][age][dataType]
                    setRowOfYearVals(sheet, values, params, PJNZParams.currRow)    
                    PJNZParams.currRow += 1
    
    PJNZParams.currRow -= 1
    addEndTag(sheet, PJNZParams)

def export_Shiny90NumNewDiagnoses(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<Shiny90NumNewDiagnoses MV>')
    
    modvar = projection[AM_Shiny90NumNewDiagnoses_Tag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)

    for HIV in GBRange(DP_D_All, DP_D_HIVPos):
        for sex in GBRange(GB_BothSexes, GB_Female):
            for age in GBRange(DP_S90_15_24, DP_S90_15Plus):
                for dataType in GBRange(DP_Number, DP_UpperBound):
                    values = modvar[HIV][sex][age][dataType]
                    setRowOfYearVals(sheet, values, params, PJNZParams.currRow)    
                    PJNZParams.currRow += 1
    
    PJNZParams.currRow -= 1
    addEndTag(sheet, PJNZParams)

def export_Shiny90PosRate(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<Shiny90PosRate MV>')
    
    modvar = projection[AM_Shiny90PosRate_Tag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)

    for HIV in GBRange(DP_D_All, DP_D_HIVPos):
        for sex in GBRange(GB_BothSexes, GB_Female):
            for age in GBRange(DP_S90_15_24, DP_S90_15Plus):
                for dataType in GBRange(DP_Number, DP_UpperBound):
                    values = modvar[HIV][sex][age][dataType]
                    setRowOfYearVals(sheet, values, params, PJNZParams.currRow)    
                    PJNZParams.currRow += 1
    
    PJNZParams.currRow -= 1
    addEndTag(sheet, PJNZParams)

def export_Shiny90YieldNewDiagn(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<Shiny90YieldNewDiagn MV>')
    
    modvar = projection[AM_Shiny90YieldNewDiagn_Tag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)

    for HIV in GBRange(DP_D_All, DP_D_HIVPos):
        for sex in GBRange(GB_BothSexes, GB_Female):
            for age in GBRange(DP_S90_15_24, DP_S90_15Plus):
                for dataType in GBRange(DP_Number, DP_UpperBound):
                    values = modvar[HIV][sex][age][dataType]
                    setRowOfYearVals(sheet, values, params, PJNZParams.currRow)    
                    PJNZParams.currRow += 1
    
    PJNZParams.currRow -= 1
    addEndTag(sheet, PJNZParams)

def export_Shiny90IsFitted(sheet, params, PJNZParams, projection):   
    addStartTag(sheet, PJNZParams, '<Shiny90IsFitted MV>')
    
    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)
    addValue(sheet, PJNZParams, GB_RW_DataStartCol,  int(projection[AM_Shiny90IsFittedTag]))
    
    addEndTag(sheet, PJNZParams)

def export_KnowledgeOfStatusInputType(sheet, params, PJNZParams, projection):   
    addStartTag(sheet, PJNZParams, '<KnowledgeOfStatusInputType MV2>')
    
    modvar = projection[AM_KnowledgeOfStatusInputTypeTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)
    addValue(sheet, PJNZParams, GB_RW_DataStartCol,  modvar)
    
    addEndTag(sheet, PJNZParams)

def export_KnowledgeOfStatusInput(sheet, params, PJNZParams, projection):   
    addStartTag(sheet, PJNZParams, '<KnowledgeOfStatusInput MV4>')
    
    modvar = projection[AM_KnowledgeOfStatusInputTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)

    for ageGroup in GBRange(DP_Cas_AG_Child, DP_Cas_AG_AdultFemale):
        values = modvar[ageGroup]
        setRowOfYearVals(sheet, values, params, PJNZParams.currRow)  
        # for year in GBRange(DP_Cas_2010, DP_Cas_2025):
        #     sheet.values[row, GB_RW_DataStartCol + year] = modvar[ageGroup][year]
        PJNZParams.currRow += 1
    
    PJNZParams.currRow -= 1    
    addEndTag(sheet, PJNZParams)

def export_KnowledgeOfStatusFileTitle(sheet, params, PJNZParams, projection):   
    addStartTag(sheet, PJNZParams, '<KnowledgeOfStatusFileTitle MV>')
    
    modvar = projection[AM_KnowledgeOfStatusFileTitleTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)
    addValue(sheet, PJNZParams, GB_RW_DataStartCol,  modvar)
    
    addEndTag(sheet, PJNZParams)

def export_ViralSuppressionInputType(sheet, params, PJNZParams, projection):   
    addStartTag(sheet, PJNZParams, '<ViralSuppressionInputType MV2>')
    
    modvar = projection[AM_ViralSuppressionInputTypeTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)
    addValue(sheet, PJNZParams, GB_RW_DataStartCol,  modvar)
    
    addEndTag(sheet, PJNZParams)

def export_ViralSuppressionInput(sheet, params, PJNZParams, projection):   
    addStartTag(sheet, PJNZParams, '<ViralSuppressionInput MV4>')
    
    modvar = projection[AM_ViralSuppressionInputTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)

    for ageGroup in GBRange(DP_Cas_AG_Child, DP_Cas_AG_AdultFemale):
        for dataType in GBRange(DP_VS_NumOnART, DP_VS_PLHIVSuppressed):
            values = modvar[ageGroup][dataType]
            setRowOfYearVals(sheet, values, params, PJNZParams.currRow) 
            # for year in GBRange(DP_Cas_2010, DP_Cas_2025):
            #     sheet.values[row, GB_RW_DataStartCol + year] = modvar[ageGroup][dataType][year]
            PJNZParams.currRow += 1
    
    PJNZParams.currRow -= 1
    addEndTag(sheet, PJNZParams)

def export_ViralSuppressionThreshold(sheet, params, PJNZParams, projection):   
    addStartTag(sheet, PJNZParams, '<ViralSuppressionThreshold MV4>')
    
    modvar = projection[AM_ViralSuppressionThresholdTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)

    values = modvar
    setRowOfYearVals(sheet, values, params, PJNZParams.currRow) 
    # for year in GBRange(DP_Cas_2010, DP_Cas_2025):
    #     sheet.values[row, GB_RW_DataStartCol + year] = modvar[year]
    
    addEndTag(sheet, PJNZParams)

def export_ChildAnnRateProgressLowerCD4(sheet, params, PJNZParams, projection):   
    addStartTag(sheet, PJNZParams, '<ChildAnnRateProgressLowerCD4 MV2>')
    
    modvar = projection[AM_ChildAnnRateProgressLowerCD4Tag]

    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams,  'Annual rate of progression to next lower CD4 category for Children')

    PJNZParams.currRow += 1
    addValueTag(sheet, PJNZParams)
    
    for sex in GBRange(GB_Male, GB_Female):
        col = 0
        PJNZParams.currRow += 1
        for a in GBRange(DP_A0t2, DP_A5t14):
            for c in GBRange(DP_CD4_Per_GT30, DP_CD4_Per_5_10):
                addValue(sheet, PJNZParams, GB_RW_DataStartCol + col,  modvar[DP_Data][sex][a][c])
                col += 1
    
    addEndTag(sheet, PJNZParams)

def export_ChildDistNewInfectionsCD4(sheet, params, PJNZParams, projection):   
    addStartTag(sheet, PJNZParams, '<ChildDistNewInfectionsCD4 MV>')
    
    modvar = projection[AM_ChildDistNewInfectionsCD4Tag]

    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams,  'Distribution of new infections by CD4 percent for Children')

    PJNZParams.currRow += 1
    addValueTag(sheet, PJNZParams)    

    col = 0
    for c in GBRange(DP_CD4_Per_GT30, DP_CD4_Per_LT5):
        addValue(sheet, PJNZParams, GB_RW_DataStartCol + col, modvar[DP_Data][c])
        col += 1
    
    addEndTag(sheet, PJNZParams)

def export_ChildMortByCD4NoART(sheet, params, PJNZParams, projection):   
    addStartTag(sheet, PJNZParams, '<ChildMortByCD4NoART MV2>')
    
    modvar = projection[AM_ChildMortByCD4NoARTTag]

    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams,  'Annual probability of HIV-related mortality among those not on ART by CD4 category for Children')

    PJNZParams.currRow += 1
    addValueTag(sheet, PJNZParams)    

    labels = {
        DP_A0t2:'Age 0-2: CD4 Percent',
        DP_A3t4:'Age 3-4: CD4 Percent',
        DP_A5t14:'Age 5-14: CD4 Count'
    }
    
    for a in GBRange(DP_A0t2, DP_A5t14):
        addNote(sheet, PJNZParams,  labels[a])
        for b in GBRange(DP_P_Perinatal, DP_P_BF12):
            col = 0
            for c in GBRange(DP_CD4_Per_GT30, DP_CD4_Per_LT5):
                addValue(sheet, PJNZParams, GB_RW_DataStartCol + col,  modvar[DP_Data][a][b][c])
                col += 1
            PJNZParams.currRow += 1
    
    PJNZParams.currRow -= 1
    addEndTag(sheet, PJNZParams)

def export_ChildMortalityRates(sheet, params, PJNZParams, projection):   
    addStartTag(sheet, PJNZParams, '<ChildMortalityRates MV2>')
    
    modvar = projection[AM_ChildMortalityRatesTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)    

    for age in GBRange(DP_CD4_0t4, DP_CD4_5t14):
        for timePeriod in GBRange(DP_MortRates_LT12Mo, DP_MortRates_GT12Mo):
            values = modvar[DP_Data][age][timePeriod]
            setRowOfYearVals(sheet, values, params, PJNZParams.currRow)    
            PJNZParams.currRow += 1
    
    PJNZParams.currRow -= 1
    addEndTag(sheet, PJNZParams)

def export_ChildMortalityRatesMultiplier(sheet, params, PJNZParams, projection):   
    addStartTag(sheet, PJNZParams, '<ChildMortalityRatesMultiplier MV>')
    
    modvar = projection[AM_ChildMortalityRatesMultiplierTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams) 
    addValue(sheet, PJNZParams, GB_RW_DataStartCol,  modvar)
    
    addEndTag(sheet, PJNZParams)

def export_ChildMortByCD4WithART0to6(sheet, params, PJNZParams, projection):   
    addStartTag(sheet, PJNZParams, '<ChildMortByCD4WithART0to6 MV2>')
    
    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams,  '0-6 months on treatment for Children')
    
    PJNZParams.currRow += 1
    addValueTag(sheet, PJNZParams) 
    
    modvarCount = projection[AM_ChildMortByCD4WithART0to6Tag]
    modvarPerc = projection[AM_ChildMortByCD4WithART0to6PercTag]

    for sex in GBRange(GB_Male, GB_Female):
        col = 0
        for a in GBRange(DP_A0, DP_A3t4):
            for c in GBRange(DP_CD4_Per_GT30, DP_CD4_Per_LT5):
                addValue(sheet, PJNZParams, GB_RW_DataStartCol + col,  modvarPerc[DP_Data][sex][a][c])
                col += 1
        for a in GBRange(DP_A5t9, DP_A10t14):
            for c in GBRange(DP_CD4_Ped_Top, DP_CD4_Ped_LT200):
                addValue(sheet, PJNZParams, GB_RW_DataStartCol + col,  modvarCount[DP_Data][sex][a][c])
                col += 1
        PJNZParams.currRow += 1
    
    PJNZParams.currRow -= 1
    addEndTag(sheet, PJNZParams)

def export_ChildMortByCD4WithART7to12(sheet, params, PJNZParams, projection):   
    addStartTag(sheet, PJNZParams, '<ChildMortByCD4WithART7to12 MV>')
    
    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams,  '7-12 months on treatment for Children')
    
    PJNZParams.currRow += 1
    addValueTag(sheet, PJNZParams) 
    
    modvarCount = projection[AM_ChildMortByCD4WithART7to12Tag]
    modvarPerc = projection[AM_ChildMortByCD4WithART7to12PercTag]

    PJNZParams.currRow += 1
    for sex in GBRange(GB_Male, GB_Female):
        col = 0
        for a in GBRange(DP_A0, DP_A3t4):
            for c in GBRange(DP_CD4_Per_GT30, DP_CD4_Per_LT5):
                addValue(sheet, PJNZParams, GB_RW_DataStartCol + col,  modvarPerc[DP_Data][sex][a][c])
                col += 1
        for a in GBRange(DP_A5t9, DP_A10t14):
            for c in GBRange(DP_CD4_Ped_Top, DP_CD4_Ped_LT200):
                addValue(sheet, PJNZParams, GB_RW_DataStartCol + col,  modvarCount[DP_Data][sex][a][c])
                col += 1
        PJNZParams.currRow += 1
    
    PJNZParams.currRow -= 1
    addEndTag(sheet, PJNZParams)

def export_ChildMortByCD4WithARTGT12(sheet, params, PJNZParams, projection):   
    addStartTag(sheet, PJNZParams, '<ChildMortByCD4WithARTGT12 MV>')
    
    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams,  'Greater than 12 months on treatment for children')
    
    PJNZParams.currRow += 1
    addValueTag(sheet, PJNZParams) 
    
    modvarCount = projection[AM_ChildMortByCD4WithARTGT12Tag]
    modvarPerc = projection[AM_ChildMortByCD4WithARTGT12PercTag]

    PJNZParams.currRow += 1
    for sex in GBRange(GB_Male, GB_Female):
        col = 0
        for a in GBRange(DP_A0, DP_A3t4):
            for c in GBRange(DP_CD4_Per_GT30, DP_CD4_Per_LT5):
                addValue(sheet, PJNZParams, GB_RW_DataStartCol + col,  modvarPerc[DP_Data][sex][a][c])
                col += 1
        for a in GBRange(DP_A5t9, DP_A10t14):
            for c in GBRange(DP_CD4_Ped_Top, DP_CD4_Ped_LT200):
                addValue(sheet, PJNZParams, GB_RW_DataStartCol + col,  modvarCount[DP_Data][sex][a][c])
                col += 1
        PJNZParams.currRow += 1
    
    PJNZParams.currRow -= 1
    addEndTag(sheet, PJNZParams)

def export_ChildARTDist(sheet, params, PJNZParams, projection):   
    addStartTag(sheet, PJNZParams, '<ChildARTDist MV>')
    
    modvar = projection[AM_ChildARTDistTag]

    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams,  'Probability of initiating ART by age for Children')
    
    PJNZParams.currRow += 1
    addValueTag(sheet, PJNZParams)

    for a in GBRange(0, 14):
        values = modvar[DP_Data][a]
        addNote(sheet, PJNZParams,  'Age: ' + str(a))
        setRowOfYearVals(sheet, values, params, PJNZParams.currRow)    
        PJNZParams.currRow += 1
    
    PJNZParams.currRow -= 1
    addEndTag(sheet, PJNZParams)

def export_EffectTreatChild(sheet, params, PJNZParams, projection):   
    addStartTag(sheet, PJNZParams, '<EffectTreatChild MV>')
    
    modvar = projection[AM_EffectTreatChildTag]

    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams,  'Percent of children with moderate-to-severe HIV disease receiving ART')
    
    PJNZParams.currRow += 1
    addValueTag(sheet, PJNZParams)

    for eff in GBRange(DP_Cotrim, DP_ChildEffWithART):
        col = GB_RW_DataStartCol
        for t in GBRange(1, DP_MaxChildTreatmentYears):
            addValue(sheet, PJNZParams, col, modvar[DP_Data][eff][t])
            col += 1 
        PJNZParams.currRow += 1
    
    PJNZParams.currRow -= 1
    addEndTag(sheet, PJNZParams)

def export_ChildWeightBands(sheet, params, PJNZParams, projection):   
    addStartTag(sheet, PJNZParams, '<ChildWeightBands MV>')
    
    modvar = projection[AM_ChildWeightBandsTag]

    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams,  'Weight bands')
    
    PJNZParams.currRow += 1
    addValueTag(sheet, PJNZParams)

    labels = {
        DP_A6Months : 'Age: 0.5',
        1 : 'Age: 1',
        2 : 'Age: 2',
        3 : 'Age: 3',
        4 : 'Age: 4',
        5 : 'Age: 5',
        6 : 'Age: 6',
        7 : 'Age: 7',
        8 : 'Age: 8',
        9 : 'Age: 9',
        10 : 'Age: 10',
        11 : 'Age: 11',
        12 : 'Age: 12',
        13 : 'Age: 13',
        DP_A14 : 'Age: 14',
    }

    for sex in GBRange(GB_Male, GB_Female):
        addNote(sheet, PJNZParams, getSexLabel(sex))                
        PJNZParams.currRow += 1
        for a in GBRange(DP_A6Months, DP_A14):
            addNote(sheet, PJNZParams, labels[a])                
            col = 0
            for b in GBRange(DP_Kgs_3_5pt9, DP_Kgs_35_Plus):
                addValue(sheet, PJNZParams, GB_RW_DataStartCol + col, modvar[DP_Data][sex][a][b])
                col += 1
            PJNZParams.currRow += 1
    
    PJNZParams.currRow -= 1
    addEndTag(sheet, PJNZParams)

def export_AdultAnnRateProgressLowerCD4(sheet, params, PJNZParams, projection):   
    addStartTag(sheet, PJNZParams, '<AdultAnnRateProgressLowerCD4 MV>')
    
    modvar = projection[AM_AdultAnnRateProgressLowerCD4Tag]

    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams,  'Annual rate of progression to next lower CD4 category for Adults')
    
    PJNZParams.currRow += 1
    addValueTag(sheet, PJNZParams)

    for sex in GBRange(GB_Male, GB_Female):
        col = 0
        PJNZParams.currRow += 1
        for a in GBRange(DP_CD4_15_24, DP_CD4_45_54):
            for c in GBRange(DP_CD4_GT500, DP_CD4_LT50):
                addValue(sheet, PJNZParams, GB_RW_DataStartCol + col,  modvar[DP_Data][sex][a][c])
                col += 1
    
    addEndTag(sheet, PJNZParams)

def export_AdultDistNewInfectionsCD4(sheet, params, PJNZParams, projection):   
    addStartTag(sheet, PJNZParams, '<AdultDistNewInfectionsCD4 MV>')
    
    modvar = projection[AM_AdultDistNewInfectionsCD4Tag]

    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams,  'Distribution of new infections by CD4 count (percent) for Adults')
    
    PJNZParams.currRow += 1
    addValueTag(sheet, PJNZParams)

    for sex in GBRange(GB_Male, GB_Female):
        col = 0
        PJNZParams.currRow += 1
        for a in GBRange(DP_CD4_15_24, DP_CD4_45_54):
            for c in GBRange(DP_CD4_GT500, DP_CD4_LT50):
                addValue(sheet, PJNZParams, GB_RW_DataStartCol + col,  modvar[DP_Data][sex][a][c])
                col += 1
    
    addEndTag(sheet, PJNZParams)

def export_AdultMortByCD4NoART(sheet, params, PJNZParams, projection):   
    addStartTag(sheet, PJNZParams, '<AdultMortByCD4NoART MV>')
    
    modvar = projection[AM_AdultMortByCD4NoARTTag]

    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams,  'Annual probability of HIV-related mortality when not on ART for Adults')
    
    PJNZParams.currRow += 1
    addValueTag(sheet, PJNZParams)

    for sex in GBRange(GB_Male, GB_Female):
        col = 0
        PJNZParams.currRow += 1
        for a in GBRange(DP_CD4_15_24, DP_CD4_45_54):
            for c in GBRange(DP_CD4_GT500, DP_CD4_LT50):
                addValue(sheet, PJNZParams, GB_RW_DataStartCol + col,  modvar[DP_Data][sex][a][c])
                col += 1
    
    addEndTag(sheet, PJNZParams)

def export_AdultInfectReduc(sheet, params, PJNZParams, projection):   
    addStartTag(sheet, PJNZParams, '<AdultInfectReduc MV>')
    
    modvar = projection[AM_AdultInfectReducTag]

    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams,  'Reduction in HIV transmission when on ART for Adults')
    
    PJNZParams.currRow += 1
    addValueTag(sheet, PJNZParams)
    addValue(sheet, PJNZParams, GB_RW_DataStartCol,  modvar[DP_Data])
    
    addEndTag(sheet, PJNZParams)

def export_MortalityRates(sheet, params, PJNZParams, projection):   
    addStartTag(sheet, PJNZParams, '<MortalityRates MV2>')
    
    modvar = projection[AM_MortalityRatesTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)

    for timePeriod in GBRange(DP_MortRates_LT12Mo, DP_MortRates_GT12Mo):
        values = modvar[DP_Data][timePeriod]
        setRowOfYearVals(sheet, values, params, PJNZParams.currRow)    
        PJNZParams.currRow += 1

    PJNZParams.currRow -= 1
    addEndTag(sheet, PJNZParams)

def export_MortalityRatesMultiplier(sheet, params, PJNZParams, projection):   
    addStartTag(sheet, PJNZParams, '<MortalityRatesMultiplier MV>')
    
    modvar = projection[AM_MortalityRatesMultiplierTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)
    addValue(sheet, PJNZParams, GB_RW_DataStartCol,  modvar)
    
    addEndTag(sheet, PJNZParams)

def export_AdultMortByCD4WithART0to6(sheet, params, PJNZParams, projection):   
    addStartTag(sheet, PJNZParams, '<AdultMortByCD4WithART0to6 MV2>')
    
    modvar = projection[AM_AdultMortByCD4WithART0to6Tag]

    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams,  '0-6 months on treatment for Adults')
    
    PJNZParams.currRow += 1
    addValueTag(sheet, PJNZParams)

    for sex in GBRange(GB_Male, GB_Female):
        col = 0
        for a in GBRange(DP_CD4_15_24, DP_CD4_45_54):
            for c in GBRange(DP_CD4_GT500, DP_CD4_LT50):
                addValue(sheet, PJNZParams, GB_RW_DataStartCol + col,  modvar[DP_Data][sex][a][c])
                col += 1
        PJNZParams.currRow += 1
    
    PJNZParams.currRow -= 1
    addEndTag(sheet, PJNZParams)

def export_AdultMortByCD4WithART7to12(sheet, params, PJNZParams, projection):   
    addStartTag(sheet, PJNZParams, '<AdultMortByCD4WithART7to12 MV2>')
    
    modvar = projection[AM_AdultMortByCD4WithART7to12Tag]

    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams,  '7-12 months on treatment for Adults')
    
    PJNZParams.currRow += 1
    addValueTag(sheet, PJNZParams)

    for sex in GBRange(GB_Male, GB_Female):
        col = 0
        for a in GBRange(DP_CD4_15_24, DP_CD4_45_54):
            for c in GBRange(DP_CD4_GT500, DP_CD4_LT50):
                addValue(sheet, PJNZParams, GB_RW_DataStartCol + col,  modvar[DP_Data][sex][a][c])
                col += 1
        PJNZParams.currRow += 1
    
    PJNZParams.currRow -= 1
    addEndTag(sheet, PJNZParams)

def export_AdultMortByCD4WithARTGT12(sheet, params, PJNZParams, projection):   
    addStartTag(sheet, PJNZParams, '<AdultMortByCD4WithARTGt12 MV2>')
    
    modvar = projection[AM_AdultMortByCD4WithARTGT12Tag]

    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams,  'Greater than 12 months on treatment for Adults')
    
    PJNZParams.currRow += 1
    addValueTag(sheet, PJNZParams)

    for sex in GBRange(GB_Male, GB_Female):
        col = 0
        for a in GBRange(DP_CD4_15_24, DP_CD4_45_54):
            for c in GBRange(DP_CD4_GT500, DP_CD4_LT50):
                addValue(sheet, PJNZParams, GB_RW_DataStartCol + col,  modvar[DP_Data][sex][a][c])
                col += 1
        PJNZParams.currRow += 1
    
    PJNZParams.currRow -= 1
    addEndTag(sheet, PJNZParams)

def export_TFRRegion(sheet, params, PJNZParams, projection):   
    addStartTag(sheet, PJNZParams, '<TFRRegion MV>')
    
    modvar = projection[AM_TFRRegionTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)
    addNote(sheet, PJNZParams, getRegionEN(modvar))
    addValue(sheet, PJNZParams, GB_RW_DataStartCol,  modvar)
    
    PJNZParams.currRow += 1

    addEndTag(sheet, PJNZParams)
            
def export_HIVTFRCustomFlag(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<HIVTFRCustomFlag MV>')
    
    modvar = projection[AM_HIVTFRCustomFlagTag]
    
    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)
    addValue(sheet, PJNZParams, GB_RW_DataStartCol,  int(modvar))
    
    addEndTag(sheet, PJNZParams)

def export_HIVTFR(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<HIVTFR MV4>')
    
    modvar = projection[AM_HIVTFRTag]

    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams,  'Fertility multiplier by age for HIV+ women off ART')
    
    PJNZParams.currRow += 1
    addValueTag(sheet, PJNZParams)
    addNote(sheet, PJNZParams,  'ages From 4 to 10')
    
    for a in GBRange(DP_A15_19, DP_A45_49):
        values = modvar[DP_Data][a]
        setRowOfYearVals(sheet, values, params, PJNZParams.currRow)    
        PJNZParams.currRow += 1
    
    PJNZParams.currRow -= 1
    addEndTag(sheet, PJNZParams)

def export_TFRInputType(sheet, params, PJNZParams, projection):   
    addStartTag(sheet, PJNZParams, '<TFRInputType MV>')
    
    modvar = projection[AM_TFRInputTypeTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)
    addValue(sheet, PJNZParams, GB_RW_DataStartCol,  modvar)
    
    addEndTag(sheet, PJNZParams)
    
def export_FertCD4Discount(sheet, params, PJNZParams, projection):   
    addStartTag(sheet, PJNZParams, '<FertCD4Discount MV>')
    
    modvar = projection[AM_FertCD4DiscountTag]

    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams,  'Ratio of fertility among HIV infected women to the fertiity of uninfected women by CD4 count category')
    
    PJNZParams.currRow += 1
    addValueTag(sheet, PJNZParams)
    
    for cd4 in GBRange(DP_CD4_GT500, DP_CD4_LT50):
        addValue(sheet, PJNZParams, GB_RW_DataStartCol + cd4 - 1,  modvar[DP_Data][cd4])
    
    addEndTag(sheet, PJNZParams)

def export_RatioWomenOnART(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<RatioWomenOnART MV2>')
    
    modvar = projection[AM_RatioWomenOnARTTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)

    col = GB_RW_DataStartCol
    for a in GBRange(DP_A15_19, DP_A45_49):
        addValue(sheet, PJNZParams, col,  modvar[DP_Data][a])
        col += 1
    
    addEndTag(sheet, PJNZParams)

def export_FRRFitInput(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<FRRFitInput MV>')
    
    modvar = projection[AM_FRRFitInputTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)

    for i in GBRange(DP_Number, DP_Percent):
        values = modvar[i]
        setRowOfYearVals(sheet, values, params, PJNZParams.currRow)    
        PJNZParams.currRow += 1
    
    PJNZParams.currRow -= 1    
    addEndTag(sheet, PJNZParams)

def export_FRRbyLocation(sheet, params, PJNZParams, projection):   
    addStartTag(sheet, PJNZParams, '<FRRbyLocation MV>')
    
    modvar = projection[AM_FRRbyLocationTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)
    addValue(sheet, PJNZParams, GB_RW_DataStartCol, modvar[DP_Data])
    
    addEndTag(sheet, PJNZParams)

def export_TransEffAssump(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<TransEffAssump MV>')
    
    modvar = projection[AM_TransEffAssumpTag]

    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams,  'Peripartum and breastfeeding transmission rates (%)')
    
    PJNZParams.currRow += 1
    addValueTag(sheet, PJNZParams)
    
    for regimen in GBRange(DP_NoProphExistInfCD4LT200, DP_ARTStartDurPreg_Late):
        for stage in GBRange(DP_Perinatal, DP_BreastfeedingGE350):
            addValue(sheet, PJNZParams, GB_RW_DataStartCol + stage - 1, modvar[DP_Data][regimen][stage])
        PJNZParams.currRow += 1
    
    PJNZParams.currRow -= 1    
    addEndTag(sheet, PJNZParams)

def export_DALYDisabilityWeights(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<DALYDisabilityWeights MV>')
    
    modvar = projection[AM_DALYDisabilityWeightsTag]

    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams,  'Disability weights')
    
    PJNZParams.currRow += 1
    addValueTag(sheet, PJNZParams)
    
    for r in GBRange(DP_DALY_CD4CountGE200, DP_DALY_OnART):
        for c in GBRange(DP_Adult, DP_Child):
            addValue(sheet, PJNZParams, GB_RW_DataStartCol + c - 1, modvar[r][c])
        PJNZParams.currRow += 1
    
    PJNZParams.currRow -= 1
    addEndTag(sheet, PJNZParams)

def export_NewARTPatAlloc(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<NewARTPatAlloc MV>')
    
    modvar = projection[AM_NewARTPatAllocTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)

    for i in GBRange(DP_AdvOpt_ART_ExpMort, DP_AdvOpt_ART_PropElig):
        addValue(sheet, PJNZParams, GB_RW_DataStartCol + i - DP_AdvOpt_ART_ExpMort, modvar[i])
    
    addEndTag(sheet, PJNZParams)

def export_NewARTPatAllocationMethod(sheet, params, PJNZParams, projection):   
    addStartTag(sheet, PJNZParams, '<NewARTPatAllocationMethod MV2>')
    
    modvar = int(projection[AM_NewARTPatAllocMethodTag])

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)
    addValue(sheet, PJNZParams, GB_RW_DataStartCol, modvar)
    
    addEndTag(sheet, PJNZParams)

def export_RiskPopOrphans(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<RiskPopOrphans MV2>')
    
    modvar = projection[AM_RiskPopOrphansTag]

    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams,  'Orphans')
    
    PJNZParams.currRow += 1
    addValueTag(sheet, PJNZParams)
    
    for c in GBRange(DP_PercAIDSDeaths, DP_PercMarried):
        col = GB_RW_DataStartCol
        for g in GBRange(DP_InjectingDrugUsers, DP_LowerRiskGenPop):
            addValue(sheet, PJNZParams, col,  modvar[g][c])
            col += 1
        PJNZParams.currRow += 1
    
    PJNZParams.currRow -= 1
    addEndTag(sheet, PJNZParams)

def export_ECDCValues(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<ECDCValues MV>')
    
    modvar = projection[AM_ECDCValuesTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)

    for i in GBRange(DP_Number, DP_UpperBound):
        values = modvar[i]
        setRowOfYearVals(sheet, values, params, PJNZParams.currRow)    
        PJNZParams.currRow += 1
    
    PJNZParams.currRow -= 1
    addEndTag(sheet, PJNZParams)

def export_ECDCFQName(sheet, params, PJNZParams, projection):   
    addStartTag(sheet, PJNZParams, '<ECDCFQName MV>')
    
    modvar = projection[AM_ECDCFQNameTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)
    addValue(sheet, PJNZParams, GB_RW_DataStartCol, modvar)
    
    addEndTag(sheet, PJNZParams)

def export_NosocomialInfectionsByAge(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<NosocomialInfectionsByAge MV>')
    
    modvar = projection[AM_NosocomialInfectionsByAgeTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)
    for a in GBRange(DP_A0_4, DP_A10_14):
        values = modvar[a]
        setRowOfYearVals(sheet, values, params, PJNZParams.currRow)    
        PJNZParams.currRow += 1
    
    PJNZParams.currRow -= 1
    addEndTag(sheet, PJNZParams)

def export_HIVMigrantsByAgeSex(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<HIVMigrantsByAgeSex MV>')
    
    modvar = projection[AM_HIVMigrantsBySexAgeTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)

    for sex in GBRange(GB_Male, GB_Female):
        for a in GBRange(DP_A0_4, DP_MAX_AGE):    
            PJNZParams.currRow += 1
            values = modvar[sex][a]
            setRowOfYearVals(sheet, values, params, PJNZParams.currRow)
    
    addEndTag(sheet, PJNZParams)

def export_IncidenceInput1970(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<IncidenceInput1970 MV>')
    
    modvar = projection[AM_IncidenceInput1970Tag]

    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams,  'Enter incidence values starting at 1970 (Used to fine-tune incidence values prior to the first year of the projection.)')
    
    PJNZParams.currRow += 1
    addValueTag(sheet, PJNZParams)
    
    values = modvar
    setRowOfYearVals(sheet, values, params, PJNZParams.currRow)  
    
    addEndTag(sheet, PJNZParams)

def export_CSAVRInputAIDSDeathsSource(sheet, params, PJNZParams, projection):   
    addStartTag(sheet, PJNZParams, '<CSAVRInputAIDSDeathsSource MV>')
    
    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)

    addValue(sheet, PJNZParams, GB_RW_DataStartCol,  projection[AM_CSAVRInputAIDSDeathsSourceTag])

    addEndTag(sheet, PJNZParams)

def export_CSAVRInputAIDSDeathsSourceName(sheet, params, PJNZParams, projection):   
    addStartTag(sheet, PJNZParams, '<CSAVRInputAIDSDeathsSourceName MV>')
    
    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)

    for i in GBRange(CSAVRSource1, CSAVRSource3):
        addValue(sheet, PJNZParams, GB_RW_DataStartCol+i, projection[AM_CSAVRInputAIDSDeathsSourceNameTag][i])
    
    addEndTag(sheet, PJNZParams)

def export_CSAVRInputAIDSDeaths(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<CSAVRInputAIDSDeaths MV2>')
    
    modvar = projection[AM_CSAVRInputAIDSDeathsTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)

    SourceLabels = {
        CSAVRSource1 : "Source: 0",
        CSAVRSource2 : "Source: 1",
        CSAVRSource3 : "Source: 2"
    }

    ReportedLabels = {
        CSAVRNumReported : 'Number reported',
        CSAVRNumNotReported : 'Number not reported'
    }

    for i in GBRange(CSAVRSource1, CSAVRSource3):
        for j in GBRange(CSAVRNumReported, CSAVRNumNotReported):
            values = modvar[i][j]
            addNote(sheet, PJNZParams, SourceLabels[i] + '; ' + ReportedLabels[j])
            setRowOfYearVals(sheet, values, params, PJNZParams.currRow)    
            PJNZParams.currRow += 1
    
    PJNZParams.currRow -= 1
    addEndTag(sheet, PJNZParams)

def export_CSAVRInputAIDSDeathsBySex(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<CSAVRInputAIDSDeathsBySex MV2>')
    
    modvar = projection[AM_CSAVRInputAIDSDeathsBySexTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)

    SourceLabels = {
        CSAVRSource1 : "Source: 0",
        CSAVRSource2 : "Source: 1",
        CSAVRSource3 : "Source: 2"
    }

    ReportedLabels = {
        CSAVRNumReported : 'Number reported',
        CSAVRNumNotReported : 'Number not reported'
    }

    for i in GBRange(CSAVRSource1, CSAVRSource3):
        for sex in GBRange(GB_Male, GB_Female):
            for j in GBRange(CSAVRNumReported, CSAVRNumNotReported):
                values = modvar[i][sex][j]
                addNote(sheet, PJNZParams, SourceLabels[i] + '; ' + getSexLabelSingular(sex) + '; ' + ReportedLabels[j])
                setRowOfYearVals(sheet, values, params, PJNZParams.currRow)    
                PJNZParams.currRow += 1    
    
    PJNZParams.currRow -= 1    
    addEndTag(sheet, PJNZParams)

def export_CSAVRInputAIDSDeathsBySexAge(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<CSAVRInputAIDSDeathsBySexAge MV2>')
    
    modvar = projection[AM_CSAVRInputAIDSDeathsBySexAgeTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)

    SourceLabels = {
        CSAVRSource1 : "Source: 0",
        CSAVRSource2 : "Source: 1",
        CSAVRSource3 : "Source: 2"
    }

    for i in GBRange(CSAVRSource1, CSAVRSource3):
        for sex in GBRange(GB_Male, GB_Female):
            for a in GBRange(DP_A15_19, DP_A50Plus):
                values = modvar[i][sex][a]
                addNote(sheet, PJNZParams, SourceLabels[i] + '; ' + getSexLabelSingular(sex) + '; ' + GetAgeName2(a))
                setRowOfYearVals(sheet, values, params, PJNZParams.currRow)    
                PJNZParams.currRow += 1
    
    PJNZParams.currRow -= 1    
    addEndTag(sheet, PJNZParams)

def export_CSAVRInputNewDiagnoses(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<CSAVRInputNewDiagnoses MV>')
    
    modvar = projection[AM_CSAVRInputNewDiagnosesTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)

    ReportedLabels = {
        CSAVRNumReported : 'Number reported',
        CSAVRNumNotReported : 'Number not reported'
    }

    for i in GBRange(CSAVRNumReported, CSAVRNumNotReported):
        values = modvar[i]
        addNote(sheet, PJNZParams, ReportedLabels[i])
        setRowOfYearVals(sheet, values, params, PJNZParams.currRow)    
        PJNZParams.currRow += 1
    
    PJNZParams.currRow -= 1
    addEndTag(sheet, PJNZParams)

def export_CSAVRInputNewDiagnosesBySex(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<CSAVRInputNewDiagnosesBySex MV>')
    
    modvar = projection[AM_CSAVRInputNewDiagnosesBySexTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)

    ReportedLabels = {
        CSAVRNumReported : 'Number reported',
        CSAVRNumNotReported : 'Number not reported'
    }

    for sex in GBRange(GB_Male, GB_Female):
        for i in GBRange(CSAVRNumReported, CSAVRNumNotReported):
            values = modvar[sex][i]
            addNote(sheet, PJNZParams, getSexLabelSingular(sex) + '; ' + ReportedLabels[i])
            setRowOfYearVals(sheet, values, params, PJNZParams.currRow)    
            PJNZParams.currRow += 1    
    
    PJNZParams.currRow -= 1
    addEndTag(sheet, PJNZParams)

def export_CSAVRInputNewDiagnosesBySexAge(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<CSAVRInputNewDiagnosesBySexAge MV>')
    
    modvar = projection[AM_CSAVRInputNewDiagnosesBySexAgeTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)

    for sex in GBRange(GB_Male, GB_Female):
        for a in GBRange(DP_A15_19, DP_A50Plus):
            values = modvar[sex][a]
            addNote(sheet, PJNZParams, getSexLabelSingular(sex) + '; ' + GetAgeName2(a))
            setRowOfYearVals(sheet, values, params, PJNZParams.currRow)    
            PJNZParams.currRow += 1
    
    PJNZParams.currRow -= 1
    addEndTag(sheet, PJNZParams)

def export_CSAVRInputNewDiagnosesBySexAgeCD4(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<CSAVRInputNewDiagnosesBySexAgeCD4 MV>')
    
    modvar = projection[AM_CSAVRInputNewDiagnosesBySexAgeCD4Tag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)
    
    CD4Labels = {
        CSAVR_CD4_LT200 : '<200',
        CSAVR_CD4_200_350 : '200-350',
        CSAVR_CD4_350_500  : '350-500',
        CSAVR_CD4_500Plus : '500+'
    }

    for sex in GBRange(GB_Male, GB_Female):
        for a in GBRange(DP_A15_19, DP_A50Plus):
            for cd4 in GBRange(CSAVR_CD4_LT200, CSAVR_CD4_500Plus):
                values = modvar[sex][a][cd4]
                addNote(sheet, PJNZParams, getSexLabelSingular(sex) + '; ' + GetAgeName2(a) + '; ' + CD4Labels[cd4])
                setRowOfYearVals(sheet, values, params, PJNZParams.currRow)    
                PJNZParams.currRow += 1
    
    PJNZParams.currRow -= 1
    addEndTag(sheet, PJNZParams)

def export_CSAVRInputCD4DistAtDiag(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<CSAVRInputCD4DistAtDiag MV>')
    
    modvar = projection[AM_CSAVRInputCD4DistAtDiagTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)

    CD4Labels = {
        CSAVR_CD4_LT200 : '<200',
        CSAVR_CD4_200_350 : '200-350',
        CSAVR_CD4_350_500  : '350-500',
        CSAVR_CD4_500Plus : '500+'
    }

    for cd4 in GBRange(CSAVR_CD4_LT200, CSAVR_CD4_500Plus):
        values = modvar[cd4]
        addNote(sheet, PJNZParams, CD4Labels[cd4])
        setRowOfYearVals(sheet, values, params, PJNZParams.currRow)    
        PJNZParams.currRow += 1
    
    PJNZParams.currRow -= 1
    addEndTag(sheet, PJNZParams)

def export_FitIncidencePopulationValue(sheet, params, PJNZParams, projection):   
    addStartTag(sheet, PJNZParams, '<FitIncidencePopulationValue_MV>')
    
    modvar = projection[AM_CSAVRPopulationValueTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)
    addValue(sheet, PJNZParams, GB_RW_DataStartCol,  modvar)
    
    addEndTag(sheet, PJNZParams)

def export_AIDSMortalityAllAges(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<AIDSMortalityAllAges MV2>')
    
    modvar = projection[AM_AIDSMortalityAllAgesTag]

    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams,  'AIDS Mortality All Ages')

    PJNZParams.currRow += 1
    addValueTag(sheet, PJNZParams)
    
    for n in GBRange(DP_Median, DP_UnderCount): 
        PJNZParams.currRow += 1
        values = modvar[n]
        setRowOfYearVals(sheet, values, params, PJNZParams.currRow)   
    
    addEndTag(sheet, PJNZParams)

# def export_AnnualInterruptionRate(sheet, params, PJNZParams, projection):   
#     addStartTag(sheet, PJNZParams, '<AnnualInterruptionRate MV>')
    
#     modvar = projection[AM_AnnualInterruptionRateTag]

#     PJNZParams.currRow += 2
#     sheet.values[row, GB_RW_DataStartCol] = modvar
    
#     addEndTag(sheet, PJNZParams)

def export_IncreasedLikelihoodOfReinit(sheet, params, PJNZParams, projection):   
    addStartTag(sheet, PJNZParams, '<IncreasedLikelihoodOfReinit MV>')
    
    modvar = projection[AM_IncreasedLikelihoodOfReinitTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)
    addValue(sheet, PJNZParams, GB_RW_DataStartCol,  modvar)
    
    addEndTag(sheet, PJNZParams)

def export_OffARTMortRateMultiplier(sheet, params, PJNZParams, projection):   
    addStartTag(sheet, PJNZParams, '<OffARTMortRateMultiplier MV>')
    
    modvar = projection[AM_OffARTMortRateMultiplierTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)
    addValue(sheet, PJNZParams, GB_RW_DataStartCol,  modvar)
    
    addEndTag(sheet, PJNZParams)

# def export_ChildAnnualInterruptionRate(sheet, params, PJNZParams, projection):   
#     addStartTag(sheet, PJNZParams, '<ChildAnnualInterruptionRate MV>')
    
#     modvar = projection[AM_ChildAnnualInterruptionRateTag]

#     PJNZParams.currRow += 2
#     sheet.values[row, GB_RW_DataStartCol] = modvar
    
#     addEndTag(sheet, PJNZParams)

def export_ChildIncreasedLikelihoodOfReinit(sheet, params, PJNZParams, projection):   
    addStartTag(sheet, PJNZParams, '<ChildIncreasedLikelihoodOfReinit MV>')
    
    modvar = projection[AM_ChildIncreasedLikelihoodOfReinitTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)
    addValue(sheet, PJNZParams, GB_RW_DataStartCol,  modvar)
    
    addEndTag(sheet, PJNZParams)

def export_ChildOffARTMortRateMultiplier(sheet, params, PJNZParams, projection):   
    addStartTag(sheet, PJNZParams, '<ChildOffARTMortRateMultiplier MV>')
    
    modvar = projection[AM_ChildOffARTMortRateMultiplierTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)
    addValue(sheet, PJNZParams, GB_RW_DataStartCol,  modvar)
    
    addEndTag(sheet, PJNZParams)

def export_CSAVRFitOptions(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<CSAVRFitOptions MV3>')
    
    modvar = projection[AM_CSAVRFitOptionsTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)

    for i in GBRange(DP_PLHIV, DP_CD4DistAtDiag):
        addValue(sheet, PJNZParams, GB_RW_DataStartCol + i,  int(modvar[i]))
    
    addEndTag(sheet, PJNZParams)

def export_FitIncidenceParameters(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<FitIncidenceParameters MV7>')
    
    modvar = projection[AM_CSAVRParametersTag]

    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams,  'Fit incidence parameters')

    PJNZParams.currRow += 1
    addValueTag(sheet, PJNZParams)
    
    PJNZParams.currRow += 1

    for fit in GBRange(DP_DoubleLogistic, DP_CSAVRMaxFit):
        col = GB_RW_DataStartCol
        count = len(modvar[str(fit)])                                            
        addValue(sheet, PJNZParams, col, count)
        PJNZParams.currRow += 1

        col = GB_RW_DataStartCol
        for i in modvar[str(fit)]:
            addValue(sheet, PJNZParams, col, modvar[str(fit)][i]['mstID'])
            col += 1

        PJNZParams.currRow += 1

        col = GB_RW_DataStartCol
        for i in modvar[str(fit)]:
            addValue(sheet, PJNZParams, col, modvar[str(fit)][i]['value'])
            col += 1

        PJNZParams.currRow += 1
  
    PJNZParams.currRow -= 1
    addEndTag(sheet, PJNZParams)

def export_FitIncidenceIncScaleParameters(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<FitIncidenceIncScaleParameters MV2>')
    
    modvar = projection[AM_CSAVRIncScaleParametersTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)

    PJNZParams.currRow += 1

    for fit in GBRange(DP_DoubleLogistic, DP_CSAVRMaxFit):
        col = GB_RW_DataStartCol
        count = len(modvar[str(fit)])                                            
        addValue(sheet, PJNZParams, col, count)
        PJNZParams.currRow += 1

        col = GB_RW_DataStartCol
        for i in modvar[str(fit)]:
            addValue(sheet, PJNZParams, col, modvar[str(fit)][i]['mstID'])
            col += 1

        PJNZParams.currRow += 1

        col = GB_RW_DataStartCol
        for i in modvar[str(fit)]:
            addValue(sheet, PJNZParams, col, modvar[str(fit)][i]['value'])
            col += 1

        PJNZParams.currRow += 1
    
    PJNZParams.currRow -= 1
    addEndTag(sheet, PJNZParams)

def export_FitIncidenceUncertaintyParams(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<FitIncidenceUncertaintyParams MV3>')
    
    modvar = projection[AM_CSAVRUncertaintyParamsTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)

    PJNZParams.currRow += 1

    for fit in GBRange(DP_DoubleLogistic, DP_CSAVRMaxFit):
        for i in GBRange(CSAVR_Unc_BurnIn, CSAVR_Unc_NumSamples):
            addValue(sheet, PJNZParams, GB_RW_DataStartCol + i, int(modvar[fit][i]))
        PJNZParams.currRow += 1

    PJNZParams.currRow -= 1
    addEndTag(sheet, PJNZParams)
    
def export_CSAVRConstrainPLHIVGTNumART(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<CSAVRConstrainPLHIVGTNumART MV3>')
    
    modvar = projection[AM_CSAVRConstrainPLHIVGTNumARTTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)

    for fit in GBRange(DP_DoubleLogistic, DP_CSAVRMaxFit):
        addValue(sheet, PJNZParams, GB_RW_DataStartCol + fit, int(modvar[fit]))

    addEndTag(sheet, PJNZParams)

def export_FitIncidenceTypeOfFit(sheet, params, PJNZParams, projection):   
    addStartTag(sheet, PJNZParams, '<FitIncidenceTypeOfFit MV2>')
    
    modvar = projection[AM_CSAVRTypeOfFitTag]

    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams,  'Fit incidence type of fit (single or double logistic curve)')

    PJNZParams.currRow += 1
    addValueTag(sheet, PJNZParams)
    
    addValue(sheet, PJNZParams, GB_RW_DataStartCol,  modvar)
    
    addEndTag(sheet, PJNZParams)

def export_CSAVRAdjustIRRs(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<CSAVRAdjustIRRs MV4>')
    
    modvar = projection[AM_CSAVRAdjustIRRsTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)

    for fitType in GBRange(DP_DoubleLogistic, DP_CSAVRMaxFit):
        values = modvar[fitType]
        addValue(sheet, PJNZParams, GB_RW_DataStartCol,  int(values[DP_CSAVR_SexRatio]))
        addValue(sheet, PJNZParams, GB_RW_DataStartCol + 1,  int(values[DP_CSAVR_DistOfHIV]))
        PJNZParams.currRow += 1
    
    PJNZParams.currRow -= 1    
    addEndTag(sheet, PJNZParams)

# def export_FitIncidenceFitMethod(sheet, params, PJNZParams, projection):
#     addStartTag(sheet, PJNZParams, '<FitIncidenceFitMethod MV2>')
    
#     modvar = projection[AM_CSAVRFitMethodTag]

#     PJNZParams.currRow += 2
#     addValueTag(sheet, PJNZParams)

#     for fitType in GBRange(DP_DoubleLogistic, DP_CSAVRMaxFit):
#         addValue(sheet, PJNZParams, GB_RW_DataStartCol + fitType, modvar[fitType])
    
#     addEndTag(sheet, PJNZParams)

def export_CSAVRMetaData(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<CSAVRMetaData MV2>')
    
    modvar = projection[AM_CSAVRMetaDataTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)

    for fitType in GBRange(DP_DoubleLogistic, DP_CSAVRMaxFit):
        addValue(sheet, PJNZParams, GB_RW_DataStartCol,  modvar[fitType]['AIC'])
        addValue(sheet, PJNZParams, GB_RW_DataStartCol + 1,  int(modvar[fitType]['isFitted']))   
        try:
            addValue(sheet, PJNZParams, GB_RW_DataStartCol + 2, dateTime_toDelphi(datetime.strptime(modvar[fitType]['date'], GB_DateTime_Format)))
        except (ValueError, TypeError):
            addValue(sheet, PJNZParams, GB_RW_DataStartCol + 2, modvar[fitType]['date'])
        PJNZParams.currRow += 1
    
    PJNZParams.currRow -= 1    
    addEndTag(sheet, PJNZParams)

def export_MeanCD4atDiagnosis(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<MeanCD4atDiagnosis MV5>')
    
    modvar = projection[AM_CSAVRMeanCD4atDiagnosisTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)

    for fitType in GBRange(DP_DoubleLogistic, DP_CSAVRMaxFit):
        for sex in GBRange(GB_BothSexes, GB_Female):
            for dataType in GBRange(DP_Number, DP_UpperBound):
                values = modvar[fitType][sex][dataType]
                setRowOfYearVals(sheet, values, params, PJNZParams.currRow)      
                PJNZParams.currRow += 1  
    
    PJNZParams.currRow -= 1    
    addEndTag(sheet, PJNZParams)

def export_MeanCD4atDiagnosisByAgeSex(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<MeanCD4atDiagnosisByAgeSex MV2>')
    
    modvar = projection[AM_CSAVRMeanCD4atDiagnosisByAgeSexTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)

    for fitType in GBRange(DP_DoubleLogistic, DP_CSAVRMaxFit):
        for sex in GBRange(GB_BothSexes, GB_Female):
            for age in GBRange(DP_AllAges, DP_A50Plus):
                for dataType in GBRange(DP_Number, DP_UpperBound):
                    values = modvar[fitType][sex][age][dataType]
                    setRowOfYearVals(sheet, values, params, PJNZParams.currRow)      
                    PJNZParams.currRow += 1 
    
    PJNZParams.currRow -= 1    
    addEndTag(sheet, PJNZParams) 

def export_TimeInfToDiag(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<TimeInfToDiag MV5>')
    
    modvar = projection[AM_CSAVRTimeInfToDiagTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)

    for fitType in GBRange(DP_DoubleLogistic, DP_CSAVRMaxFit):
        for sex in GBRange(GB_BothSexes, GB_Female):
            for dataType in GBRange(DP_Number, DP_UpperBound):
                values = modvar[fitType][sex][dataType]
                setRowOfYearVals(sheet, values, params, PJNZParams.currRow)      
                PJNZParams.currRow += 1  
    
    PJNZParams.currRow -= 1    
    addEndTag(sheet, PJNZParams)

def export_PropOfDiagnosed(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<PropOfDiagnosed MV5>')
    
    modvar = projection[AM_CSAVRPropOfDiagnosedTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)

    for fitType in GBRange(DP_DoubleLogistic, DP_CSAVRMaxFit):
        for sex in GBRange(GB_BothSexes, GB_Female):
            for dataType in GBRange(DP_Number, DP_UpperBound):
                values = modvar[fitType][sex][dataType]
                setRowOfYearVals(sheet, values, params, PJNZParams.currRow)      
                PJNZParams.currRow += 1  
    
    PJNZParams.currRow -= 1  
    addEndTag(sheet, PJNZParams)

def export_PropOfDiagnosedNoART(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<PropOfDiagnosedNoART MV2>')
    
    modvar = projection[AM_CSAVRPropOfDiagnosedNoARTTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)

    for fitType in GBRange(DP_DoubleLogistic, DP_CSAVRMaxFit):
        for sex in GBRange(GB_BothSexes, GB_Female):
            for dataType in GBRange(DP_Number, DP_UpperBound):
                values = modvar[fitType][sex][dataType]
                setRowOfYearVals(sheet, values, params, PJNZParams.currRow)      
                PJNZParams.currRow += 1  
    
    PJNZParams.currRow -= 1  
    addEndTag(sheet, PJNZParams)

def export_PropofDiagnosedByAgeSexCD4(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<PropOfDiagnosedByAgeSexCD4 MV2>')
    
    modvar = projection[AM_CSAVRPropOfDiagnosedByAgeSexCD4Tag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)
    rows = []
    last_row = PJNZParams.currRow
    for fitType in GBRange(DP_DoubleLogistic, DP_CSAVRMaxFit):
        for sex in GBRange(GB_BothSexes, GB_Female):
            for age in GBRange(DP_AllAges, DP_A50Plus):
                for cd4 in GBRange(CSAVR_CD4_LT200, CSAVR_CD4_All):
                    for dataType in GBRange(DP_Number, DP_UpperBound):
                        values = modvar[fitType][sex][age][cd4][dataType]
                        setRowOfYearVals(sheet, values, params, PJNZParams.currRow)   
                        PJNZParams.currRow +=  1
                        # rows.append(modvar[fitType][sex][age][cd4][dataType])
                        # values = modvar[fitType][sex][age][cd4][dataType]
                        # setRowOfYearVals(sheet, values, params, PJNZParams.currRow)      
                        # PJNZParams.currRow += 1  
    # sheet.sheet.iloc[PJNZParams.currRow:PJNZParams.currRow+len(rows), GB_RW_DataStartCol:GB_RW_DataStartCol+len(rows[0])] = rows
    # PJNZParams.currRow += len(rows)-1  
    
    PJNZParams.currRow -=  1
    addEndTag(sheet, PJNZParams)
    pass

def export_CSAVRNumPLHIV(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<CSAVRNumPLHIV MV3>')
    
    modvar = projection[AM_CSAVRNumPLHIVTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)

    for fitType in GBRange(DP_DoubleLogistic, DP_CSAVRMaxFit):
        for sex in GBRange(GB_BothSexes, GB_Female):
            for dataType in GBRange(DP_Number, DP_UpperBound):
                values = modvar[fitType][sex][dataType]
                setRowOfYearVals(sheet, values, params, PJNZParams.currRow)      
                PJNZParams.currRow += 1  
    
    PJNZParams.currRow -= 1  
    addEndTag(sheet, PJNZParams)

def export_CSAVRNumPLHIVByAgeSexCD4(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<CSAVRNumPLHIVByAgeSexCD4 MV2>')
    
    modvar = projection[AM_CSAVRNumPLHIVByAgeSexCD4Tag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)

    rows = []
    for fitType in GBRange(DP_DoubleLogistic, DP_CSAVRMaxFit):
        for sex in GBRange(GB_BothSexes, GB_Female):
            for age in GBRange(DP_AllAges, DP_A50Plus):
                for cd4 in GBRange(CSAVR_CD4_LT200, CSAVR_CD4_All):
                    for dataType in GBRange(DP_Number, DP_UpperBound):
                        # rows.append(modvar[fitType][sex][age][cd4][dataType])
                        values = modvar[fitType][sex][age][cd4][dataType]
                        setRowOfYearVals(sheet, values, params, PJNZParams.currRow)   
                        PJNZParams.currRow += 1 
                        # values = modvar[fitType][sex][age][cd4][dataType]
                        # setRowOfYearVals(sheet, values, params, PJNZParams.currRow)      
                        # PJNZParams.currRow += 1 
    
    # sheet.sheet.loc[PJNZParams.currRow:PJNZParams.currRow+len(rows)-1, GB_RW_DataStartCol:GB_RW_DataStartCol+len(rows[0])] = rows
    # sheet.sheet.iloc[PJNZParams.currRow:PJNZParams.currRow+len(rows), GB_RW_DataStartCol:GB_RW_DataStartCol+len(rows[0])] = rows
    # PJNZParams.currRow += len(rows)-1 

    PJNZParams.currRow -= 1
    addEndTag(sheet, PJNZParams) 

def export_CSAVRNumDiagnosed(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<CSAVRNumDiagnosed MV3>')
    
    modvar = projection[AM_CSAVRNumDiagnosedTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)

    for fitType in GBRange(DP_DoubleLogistic, DP_CSAVRMaxFit):
        for sex in GBRange(GB_BothSexes, GB_Female):
            for dataType in GBRange(DP_Number, DP_UpperBound):
                values = modvar[fitType][sex][dataType]
                setRowOfYearVals(sheet, values, params, PJNZParams.currRow)      
                PJNZParams.currRow += 1  
    
    PJNZParams.currRow -= 1  
    addEndTag(sheet, PJNZParams)

def export_CSAVRNumDiagnosedByAgeSexCD4(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<CSAVRNumDiagnosedByAgeSexCD4 MV2>')
    
    modvar = projection[AM_CSAVRNumDiagnosedByAgeSexCD4Tag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)

    rows = []
    for fitType in GBRange(DP_DoubleLogistic, DP_CSAVRMaxFit):
        for sex in GBRange(GB_BothSexes, GB_Female):
            for age in GBRange(DP_AllAges, DP_A50Plus):
                for cd4 in GBRange(CSAVR_CD4_LT200, CSAVR_CD4_All):
                    for dataType in GBRange(DP_Number, DP_UpperBound):
                        # rows.append(modvar[fitType][sex][age][cd4][dataType])
                        values = modvar[fitType][sex][age][cd4][dataType]
                        setRowOfYearVals(sheet, values, params, PJNZParams.currRow)   
                        PJNZParams.currRow += 1 
                        # values = modvar[fitType][sex][age][cd4][dataType]
                        # setRowOfYearVals(sheet, values, params, PJNZParams.currRow)      
                        # PJNZParams.currRow += 1 
    
    # sheet.sheet.loc[PJNZParams.currRow:PJNZParams.currRow+len(rows)-1, GB_RW_DataStartCol:GB_RW_DataStartCol+len(rows[0])] = rows
    # sheet.sheet.iloc[PJNZParams.currRow:PJNZParams.currRow+len(rows), GB_RW_DataStartCol:GB_RW_DataStartCol+len(rows[0])] = rows
    # PJNZParams.currRow += len(rows)-1

    PJNZParams.currRow -= 1 
    addEndTag(sheet, PJNZParams)   

def export_CSAVRAIDSDeaths(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<CSAVRAIDSDeaths MV3>')
    
    modvar = projection[AM_CSAVRAIDSDeathsTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)

    for fitType in GBRange(DP_DoubleLogistic, DP_CSAVRMaxFit):
        for sex in GBRange(GB_BothSexes, GB_Female):
            for dataType in GBRange(DP_Number, DP_UpperBound):
                values = modvar[fitType][sex][dataType]
                setRowOfYearVals(sheet, values, params, PJNZParams.currRow)      
                PJNZParams.currRow += 1  
    
    PJNZParams.currRow -= 1  
    addEndTag(sheet, PJNZParams)

def export_CSAVRAIDSDeathsByAgeSex(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<CSAVRAIDSDeathsByAgeSex MV2>')
    
    modvar = projection[AM_CSAVRAIDSDeathsByAgeSexTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)

    for fitType in GBRange(DP_DoubleLogistic, DP_CSAVRMaxFit):
        for sex in GBRange(GB_BothSexes, GB_Female):
            for age in GBRange(DP_AllAges, DP_A50Plus):
                for dataType in GBRange(DP_Number, DP_UpperBound):
                    values = modvar[fitType][sex][age][dataType]
                    setRowOfYearVals(sheet, values, params, PJNZParams.currRow)      
                    PJNZParams.currRow += 1 
    
    PJNZParams.currRow -= 1  
    addEndTag(sheet, PJNZParams)

def export_CSAVRNumNewInfections(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<CSAVRNumNewInfections MV3>')
    
    modvar = projection[AM_CSAVRNumNewInfectionsTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)

    for fitType in GBRange(DP_DoubleLogistic, DP_CSAVRMaxFit):
        for sex in GBRange(GB_BothSexes, GB_Female):
            for dataType in GBRange(DP_Number, DP_UpperBound):
                values = modvar[fitType][sex][dataType]
                setRowOfYearVals(sheet, values, params, PJNZParams.currRow)      
                PJNZParams.currRow += 1   
    
    PJNZParams.currRow -= 1  
    addEndTag(sheet, PJNZParams)

def export_CSAVRIncidenceByFit(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<CSAVRIncidenceByFit MV2>')
    
    modvar = projection[AM_CSAVRIncidenceByFitTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)

    for fitType in GBRange(DP_DoubleLogistic, DP_CSAVRMaxFit): 
        PJNZParams.currRow += 1   
        values = modvar[fitType]
        setRowOfYearVals(sheet, values, params, PJNZParams.currRow)     
    
    # PJNZParams.currRow -= 1  
    addEndTag(sheet, PJNZParams)

                
def export_HIVSexRatio(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<HIVSexRatio MV>')
    
    # modvar = projection[AM_HIVSexRatioTag]
    
    value = projection[AM_CustomSAPDataIndexTag]
    if value == DP_PatternFromCSAVR_Index:
        fit_type = projection[AM_CSAVRTypeOfFitTag]
        sex_ratios = projection[AM_CSAVRHIVSexRatioTag][fit_type]
    else:
        sex_ratios = projection[AM_HIVSexRatioTag]
    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)

    PJNZParams.currRow += 1

    setRowOfYearVals(sheet, sex_ratios, params, PJNZParams.currRow)
    
    addEndTag(sheet, PJNZParams)
                
def export_CSAVRHIVSexRatio(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<CSAVRHIVSexRatio MV3')
    
    modvar = projection[AM_CSAVRHIVSexRatioTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)

    PJNZParams.currRow += 1

    for fitType in GBRange(DP_DoubleLogistic, DP_CSAVRMaxFit):
        values = modvar[fitType]
        setRowOfYearVals(sheet, values, params, PJNZParams.currRow)     
        PJNZParams.currRow += 1
    
    PJNZParams.currRow -= 1
    addEndTag(sheet, PJNZParams)

def getSAPFitIndex(fitType, HIVPrevModel, projection):
    idx = -1
    for i, dataDict in enumerate(projection[AM_CustomSAPDataTag]):    
        if dataDict['fitType'] == fitType:
            if (fitType == DP_SAP_HIVPrevByAge):
                if (dataDict['HIVPrevModel'] == HIVPrevModel):
                    idx = i
            else:
                idx = i
    return idx

def export_HIVSexRatioFittingValues(sheet, params, PJNZParams, projection):
    FixedIROverTimeIdx = getSAPFitIndex(DP_SAP_HIVPrevByAge, DP_SAP_FixedIROverTime, projection)
    TimeDependentIRIdx = getSAPFitIndex(DP_SAP_HIVPrevByAge, DP_SAP_TimeDependentIR, projection)

    if (FixedIROverTimeIdx >= 0) and (TimeDependentIRIdx >= 0):
        addStartTag(sheet, PJNZParams, '<HIVSexRatioFittingValues MV>')
        
        # modvar = projection[AM_HIVSexRatioFittingValuesTag]
        modvar = projection[AM_CustomSAPDataTag]
        zeroArr = np.zeros(getYearIdx(params.finalYear, params.firstYear) + 1)

        PJNZParams.currRow += 1
        addDescript(sheet, PJNZParams,  'Sex ratio by epidemic pattern')

        PJNZParams.currRow += 1
        addValueTag(sheet, PJNZParams)
        
        # for i in GBRange(DP_SAP_FixedIROverTime, DP_SAP_TimeDependentIR):     
        #     PJNZParams.currRow += 1  
        #     values = modvar[i]
        #     setRowOfYearVals(sheet, values, params, PJNZParams.currRow)   
        
        PJNZParams.currRow += 1  
        if (FixedIROverTimeIdx >= 0):
            values = modvar[FixedIROverTimeIdx]['HIVSexRatio']
        else:
            values = zeroArr
        setRowOfYearVals(sheet, values, params, PJNZParams.currRow)   
        
        PJNZParams.currRow += 1  
        if (TimeDependentIRIdx >= 0):
            values = modvar[TimeDependentIRIdx]['HIVSexRatio']
        else:
            values = zeroArr
        setRowOfYearVals(sheet, values, params, PJNZParams.currRow)   
        
        addEndTag(sheet, PJNZParams)
                
def export_ARTTreatFitHIVSexRatio(sheet, params, PJNZParams, projection):
    dataIdx = getSAPFitIndex(DP_SAP_ARTByAge, 0, projection)

    if (dataIdx >= 0):
        addStartTag(sheet, PJNZParams, '<ARTTreatFitHIVSexRatio MV>')
        
        modvar = projection[AM_CustomSAPDataTag]

        PJNZParams.currRow += 2
        addValueTag(sheet, PJNZParams)   
        
        PJNZParams.currRow += 1  

        values = modvar[dataIdx]['HIVSexRatio']
        setRowOfYearVals(sheet, values, params, PJNZParams.currRow)
        
        addEndTag(sheet, PJNZParams)

def export_FittingAICData(sheet, params, PJNZParams, projection):
    FixedIROverTimeIdx = getSAPFitIndex(DP_SAP_HIVPrevByAge, DP_SAP_FixedIROverTime, projection)
    TimeDependentIRIdx = getSAPFitIndex(DP_SAP_HIVPrevByAge, DP_SAP_TimeDependentIR, projection)

    if (FixedIROverTimeIdx >= 0) and (TimeDependentIRIdx >= 0):
        addStartTag(sheet, PJNZParams, '<FittingAICData MV>')
        
        modvar = projection[AM_CustomSAPDataTag]

        PJNZParams.currRow += 1
        addDescript(sheet, PJNZParams,  'Akaike information criterion')

        PJNZParams.currRow += 1
        addValueTag(sheet, PJNZParams)

        # for i in GBRange(DP_SAP_FixedIROverTime, DP_SAP_TimeDependentIR):
            # addValue(sheet, PJNZParams, GB_RW_DataStartCol,  modvar[i]['AIC'])
            # addValue(sheet, PJNZParams, GB_RW_DataStartCol + 1,  int(modvar[i]['isFitted']))
            # PJNZParams.currRow += 1
        if (FixedIROverTimeIdx >= 0):
            addValue(sheet, PJNZParams, GB_RW_DataStartCol,  modvar[FixedIROverTimeIdx]['AIC'])
            addValue(sheet, PJNZParams, GB_RW_DataStartCol + 1,  int(True))
        else:
            addValue(sheet, PJNZParams, GB_RW_DataStartCol,  0)
            addValue(sheet, PJNZParams, GB_RW_DataStartCol + 1,  0)
        PJNZParams.currRow += 1
    
        if (TimeDependentIRIdx >= 0):
            addValue(sheet, PJNZParams, GB_RW_DataStartCol,  modvar[TimeDependentIRIdx]['AIC'])
            addValue(sheet, PJNZParams, GB_RW_DataStartCol + 1,  int(True))
        else:
            addValue(sheet, PJNZParams, GB_RW_DataStartCol,  0)
            addValue(sheet, PJNZParams, GB_RW_DataStartCol + 1,  0)
        PJNZParams.currRow += 1
        
        PJNZParams.currRow -= 1
        addEndTag(sheet, PJNZParams)

def export_ARTTreatFittingData(sheet, params, PJNZParams, projection):
    dataIdx = getSAPFitIndex(DP_SAP_ARTByAge, 0, projection)

    if (dataIdx >= 0):
        addStartTag(sheet, PJNZParams, '<ARTTreatFittingData MV>')
        
        modvar = projection[AM_CustomSAPDataTag]

        PJNZParams.currRow += 2
        addValueTag(sheet, PJNZParams)
        
        addValue(sheet, PJNZParams, GB_RW_DataStartCol,   modvar[dataIdx]['AIC'])
        addValue(sheet, PJNZParams, GB_RW_DataStartCol + 1, int(True))
        
        addEndTag(sheet, PJNZParams)

def export_DistOfHIV(sheet, params, PJNZParams, projection):    
    addStartTag(sheet, PJNZParams, '<DistOfHIV MV2>')
    
    
    value = projection[AM_CustomSAPDataIndexTag]
    if value == DP_PatternFromCSAVR_Index:
        fit_type = projection[AM_CSAVRTypeOfFitTag]
        dist_of_hiv = projection[AM_CSAVRDistOfHIVTag][fit_type]
    else:
        dist_of_hiv = projection[AM_DistOfHIVTag]

    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams,  'Incidence rate ratios')

    PJNZParams.currRow += 1
    addValueTag(sheet, PJNZParams)    

    PJNZParams.currRow += 1

    for sex in GBRange(GB_Male, GB_Female):
        addDescript(sheet, PJNZParams,  getSexLabel(sex))
        for age in GBRange(DP_A0_4, DP_MAX_AGE):
            values = dist_of_hiv[sex][age]
            setRowOfYearVals(sheet, values, params, PJNZParams.currRow)    
            PJNZParams.currRow += 1
        
    PJNZParams.currRow -= 1
    addEndTag(sheet, PJNZParams)

def export_CSAVRDistOfHIV(sheet, params, PJNZParams, projection):    
    addStartTag(sheet, PJNZParams, '<CSAVRDistOfHIV MV2>')
    
    modvar = projection[AM_CSAVRDistOfHIVTag]

    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams,  'Incidence rate ratios')

    PJNZParams.currRow += 1
    addValueTag(sheet, PJNZParams)    

    PJNZParams.currRow += 1

    for fitType in GBRange(DP_DoubleLogistic, DP_CSAVRMaxFit): 
        for sex in GBRange(GB_Male, GB_Female):
            addDescript(sheet, PJNZParams,  getSexLabel(sex))
            for age in GBRange(DP_A0_4, DP_MAX_AGE):
                values = modvar[fitType][sex][age]
                setRowOfYearVals(sheet, values, params, PJNZParams.currRow)    
                PJNZParams.currRow += 1             
        PJNZParams.currRow += 1
    
    PJNZParams.currRow -= 2
    addEndTag(sheet, PJNZParams)

def export_IRRFittingValues(sheet, params, PJNZParams, projection):    
    FixedIROverTimeIdx = getSAPFitIndex(DP_SAP_HIVPrevByAge, DP_SAP_FixedIROverTime, projection)
    TimeDependentIRIdx = getSAPFitIndex(DP_SAP_HIVPrevByAge, DP_SAP_TimeDependentIR, projection)

    if (FixedIROverTimeIdx >= 0) and (TimeDependentIRIdx >= 0):
        addStartTag(sheet, PJNZParams, '<IRRFittingValues MV>')
        
        # modvar = projection[AM_IRRFittingValuesTag]
        modvar = projection[AM_CustomSAPDataTag]
        zeroArr = np.zeros(getYearIdx(params.finalYear, params.firstYear) + 1).tolist()

        PJNZParams.currRow += 1
        addDescript(sheet, PJNZParams,  'Incident rate ratios fitted values')

        PJNZParams.currRow += 1
        addValueTag(sheet, PJNZParams)    

        # for i in GBRange(DP_SAP_FixedIROverTime, DP_SAP_TimeDependentIR):
            # PJNZParams.currRow += 1
            # for sex in GBRange(GB_Male, GB_Female):
            #     addDescript(sheet, PJNZParams,  getSexLabel(sex))
            #     for age in GBRange(DP_A0_4, DP_MAX_AGE):
            #         values = modvar[i][sex][age]
            #         setRowOfYearVals(sheet, values, params, PJNZParams.currRow)    
            #         PJNZParams.currRow += 1
        PJNZParams.currRow += 1
        
        for sex in GBRange(GB_Male, GB_Female):
            addDescript(sheet, PJNZParams,  getSexLabel(sex))
            for age in GBRange(DP_A0_4, DP_MAX_AGE):
                # values = modvar[i][sex][age]
                if (FixedIROverTimeIdx >= 0):
                    values = modvar[FixedIROverTimeIdx]['DistOfHIV'][sex][age]
                else:
                    values = zeroArr
                setRowOfYearVals(sheet, values, params, PJNZParams.currRow)    
                PJNZParams.currRow += 1
                
        PJNZParams.currRow += 1
        for sex in GBRange(GB_Male, GB_Female):
            addDescript(sheet, PJNZParams,  getSexLabel(sex))
            for age in GBRange(DP_A0_4, DP_MAX_AGE):
                # values = modvar[i][sex][age]
                if (TimeDependentIRIdx >= 0):
                    values = modvar[TimeDependentIRIdx]['DistOfHIV'][sex][age]
                else:
                    values = zeroArr
                setRowOfYearVals(sheet, values, params, PJNZParams.currRow)    
                PJNZParams.currRow += 1
        
        PJNZParams.currRow -= 1
        addEndTag(sheet, PJNZParams)

def export_ARTTreatFitDistOfHIV(sheet, params, PJNZParams, projection):    
    dataIdx = getSAPFitIndex(DP_SAP_ARTByAge, 0, projection)

    if (dataIdx >= 0):
        addStartTag(sheet, PJNZParams, '<ARTTreatFit MV>')
        
        modvar = projection[AM_CustomSAPDataTag]

        PJNZParams.currRow += 2
        addValueTag(sheet, PJNZParams)
        
        PJNZParams.currRow += 1
            
        for sex in GBRange(GB_Male, GB_Female):
            addDescript(sheet, PJNZParams,  getSexLabel(sex))
            for age in GBRange(DP_A0_4, DP_MAX_AGE):
                values = modvar[dataIdx]['DistOfHIV'][sex][age]
                setRowOfYearVals(sheet, values, params, PJNZParams.currRow)    
                PJNZParams.currRow += 1
        
        PJNZParams.currRow -= 1
        addEndTag(sheet, PJNZParams)

def export_AIDS45q15(sheet, params, PJNZParams, projection):
    format2(sheet, params, PJNZParams, projection, '<AIDS45q15 MV>', AM_AIDS45q15Tag, 'AIDS 45q15')

def export_NonAIDS45q15(sheet, params, PJNZParams, projection):
    format2(sheet, params, PJNZParams, projection, '<NonAIDS45q15 MV>', AM_NonAIDS45q15Tag, 'Non-AIDS 45q15')

def export_Total45q15(sheet, params, PJNZParams, projection):
   format2(sheet, params, PJNZParams, projection, '<Total45q15 MV>', AM_Total45q15Tag, 'Total 45q15')
   
def export_Under5MortRate(sheet, params, PJNZParams, projection):
    format2(sheet, params, PJNZParams, projection, '<Under5MortRate MV>', AM_Under5MortRateTag, 'Under 5 mortality rate (per 1000 live births)')

def export_PMTCTProgEstNeed(sheet, params, PJNZParams, projection):
    format2(sheet, params, PJNZParams, projection, '<PMTCTProgEstNeed MV>', AM_PMTCTProgEstNeedTag, 'Program estimate of need')

def export_NumberOnART(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<NumberOnART MV>')
    
    values = np.sum(np.array(projection[AM_OnARTBySingleAgeTag][0]), axis=0).tolist()
    
    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams,  'Number on ART')
    PJNZParams.currRow += 1
    addValueTag(sheet, PJNZParams)

    setRowOfYearVals(sheet, values, params, PJNZParams.currRow)
    
    addEndTag(sheet, PJNZParams)


def export_ARTCovByAge(sheet, params, PJNZParams, projection):    
    addStartTag(sheet, PJNZParams, '<ARTCovByAge MV>')
    
    modvar = projection[AM_ARTCovByAgeTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)
    
    PJNZParams.currRow += 1
    
    labels = {
        DP_A0_4    :  '0-4',
        DP_A5_9    :  '5-9',
        DP_A10_14  :  '10-14',
        DP_A15_19  :  '15-19',
        DP_A20_24  :  '20-24',
        DP_A25_29  :  '25-29',
        DP_A30_34  :  '30-34',
        DP_A35_39  :  '35-39',
        DP_A40_44  :  '40-44',
        DP_A45_49  :  '45-49',
        DP_A50_54  :  '50-54',
        DP_A55_59  :  '55-59',
        DP_A60_64  :  '60-64',
        DP_A65_69  :  '65-69',
        DP_A70_74  :  '70-74',
        DP_A75_79  :  '75-79',
        DP_A80_Up  :  '80+'
    }
    
    for sex in GBRange(GB_BothSexes, GB_Female):
        addDescript(sheet, PJNZParams,  getSexLabel(sex))
        for age in GBRange(DP_A0_4, DP_MAX_AGE):
            values = modvar[sex][age]
            addNote(sheet, PJNZParams, 'Age: ' + labels[age])
            setRowOfYearVals(sheet, values, params, PJNZParams.currRow)    
            PJNZParams.currRow += 1
    
    PJNZParams.currRow -= 1
    addEndTag(sheet, PJNZParams)

def export_KeyPops(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<KeyPops MV>')
    
    modvar = projection[AM_KeyPopsTag]
    
    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)

    for ind in GBRange(DP_KP_PSE, DP_KP_NewInfs):
        for pop in GBRange(DP_KP_FSW, DP_KP_TG):
            addValue(sheet, PJNZParams, GB_RW_DataStartCol + pop,  modvar['data'][ind][pop])
        PJNZParams.currRow += 1

    PJNZParams.currRow -= 1    
    addEndTag(sheet, PJNZParams)

def export_KeyPopsYear(sheet, params, PJNZParams, projection):   
    addStartTag(sheet, PJNZParams, '<KeyPopsYear MV>')
    
    modvar = projection[AM_KeyPopsTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)
    addValue(sheet, PJNZParams, GB_RW_DataStartCol,  modvar['year'])
    
    addEndTag(sheet, PJNZParams)

def export_KeyPopsFName(sheet, params, PJNZParams, projection):   
    addStartTag(sheet, PJNZParams, '<KeyPopsFName MV>')
    
    modvar = projection[AM_KeyPopsTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)
    addValue(sheet, PJNZParams, GB_RW_DataStartCol,  modvar['fName'])
    
    addEndTag(sheet, PJNZParams)

def export_PregWomenPrevRoutineTest(sheet, params, PJNZParams, projection):   
    addStartTag(sheet, PJNZParams, '<PregWomenPrevRoutineTest MV>')
    
    modvar = projection[AM_PregWomenPrevRoutineTestTag]

    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams,  'HIV prevalance among pregnant women from routine testing')

    PJNZParams.currRow += 1
    addValueTag(sheet, PJNZParams)    

    addValue(sheet, PJNZParams, GB_RW_DataStartCol,  modvar)
    
    addEndTag(sheet, PJNZParams)

def export_PregWomenPrev(sheet, params, PJNZParams, projection):
    format2(sheet, params, PJNZParams, projection, '<PregWomenPrev MV>', AM_PregWomenPrevTag, 'Pregnant women prevalence')

def export_PrevSurveyData(sheet, params, PJNZParams, projection):    
    addStartTag(sheet, PJNZParams, '<PrevSurveyData MV5>')
    
    modvar = projection[AM_PrevSurveyTag]

    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams,  'Prevalence Validation')

    PJNZParams.currRow += 1
    addValueTag(sheet, PJNZParams)    

    PJNZParams.currRow += 1
    
    labels = {
        DP_A2_4    :  '2-4',
        DP_A5_9    :  '5-9',
        DP_A10_14  :  '10-14',
        DP_A15_19  :  '15-19',
        DP_A20_24  :  '20-24',
        DP_A25_29  :  '25-29',
        DP_A30_34  :  '30-34',
        DP_A35_39  :  '35-39',
        DP_A40_44  :  '40-44',
        DP_A45_49  :  '45-49',
        DP_A50_54  :  '50-54',
        DP_A55_59  :  '55-59',
        DP_A60_64  :  '60-64',
        DP_A65_69  :  '65-69',
        DP_A70_74  :  '70-74',
        DP_A75_79  :  '75-79',
        DP_A80_Up  :  '80+'
    }
    
    for survey in GBRange(DP_PrevSurvey1, DP_PrevSurvey8):
        addDescript(sheet, PJNZParams,  'Prevalence survey ' + str(survey))
        PJNZParams.currRow += 1
        for sex in GBRange(GB_BothSexes, GB_Female):
            addDescript(sheet, PJNZParams,  getSexLabel(sex))
            for age in GBRange(DP_A2_4, DP_MAX_AGE):
                addNote(sheet, PJNZParams, 'Age: ' + labels[age])
                for dt in GBRange(DP_Number, DP_WeightedSampleSize):
                    addValue(sheet, PJNZParams, GB_RW_DataStartCol + dt,  modvar[survey]['data'][sex][dt][age])
                PJNZParams.currRow += 1
    
    PJNZParams.currRow -= 1
    addEndTag(sheet, PJNZParams)

def export_PrevSurveyUsed(sheet, params, PJNZParams, projection):    
    addStartTag(sheet, PJNZParams, '<PrevSurveyUsed MV3>')
    
    modvar = projection[AM_PrevSurveyTag]

    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams,  'Using prevalence survey')

    PJNZParams.currRow += 1
    addValueTag(sheet, PJNZParams)    

    for survey in GBRange(DP_PrevSurvey1, DP_PrevSurvey8):
        addValue(sheet, PJNZParams, GB_RW_DataStartCol + survey - 1,  int(modvar[survey]['used']))
    
    addEndTag(sheet, PJNZParams)

def export_PrevSurveyName(sheet, params, PJNZParams, projection):    
    addStartTag(sheet, PJNZParams, '<PrevSurveyName MV3>')
    
    modvar = projection[AM_PrevSurveyTag]

    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams,  'Prevalence Survey Name')

    PJNZParams.currRow += 1
    addValueTag(sheet, PJNZParams)    

    for survey in GBRange(DP_PrevSurvey1, DP_PrevSurvey8):
        addValue(sheet, PJNZParams, GB_RW_DataStartCol + survey - 1,  modvar[survey]['name'])
    
    addEndTag(sheet, PJNZParams)

def export_PrevSurveyYear(sheet, params, PJNZParams, projection):    
    addStartTag(sheet, PJNZParams, '<PrevSurveyYear MV3>')
    
    modvar = projection[AM_PrevSurveyTag]

    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams,  'Prevalence Survey Year')

    PJNZParams.currRow += 1
    addValueTag(sheet, PJNZParams)    

    for survey in GBRange(DP_PrevSurvey1, DP_PrevSurvey8):
        addValue(sheet, PJNZParams, GB_RW_DataStartCol + survey - 1,  modvar[survey]['year'])
    
    addEndTag(sheet, PJNZParams)

def export_ARTCovSurveyData(sheet, params, PJNZParams, projection):    
    addStartTag(sheet, PJNZParams, '<ARTCovSurveyData MV2>')
    
    modvar = projection[AM_ARTCovSurveyTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)

    PJNZParams.currRow += 1    

    labels = {
        DP_A0_4         : '0-4',
        DP_A5_9         : '5-9',
        DP_A10_14       : '10-14',
        DP_A15_19       : '15-19',
        DP_A20_24       : '20-24',
        DP_A25_29       : '25-29',
        DP_A30_34       : '30-34',
        DP_A35_39       : '35-39',
        DP_A40_44       : '40-44',
        DP_A45_49       : '45-49',
        DP_A50_54       : '50-54',
        DP_A55_59       : '55-59',
        DP_A60_64       : '60-64',
        DP_A65_69       : '65-69',
        DP_A70_74       : '70-74',
        DP_A75_79       : '75-79',
        DP_A80_Up       : '80+',
        DP_Val_A0_14    : '80+',
        DP_Val_A15_49   : '80+',
        DP_Val_A50Plus  : '80+',
    }
    
    for survey in GBRange(DP_PrevSurvey1, DP_PrevSurvey8):
        addDescript(sheet, PJNZParams,  'Prevalence survey ' + str(survey))
        PJNZParams.currRow += 1
        for sex in GBRange(GB_BothSexes, GB_Female):
            addDescript(sheet, PJNZParams,  getSexLabel(sex))
            for age in GBRange(DP_A0_4, DP_Val_A50Plus):
                addNote(sheet, PJNZParams, 'Age : ' + labels[age])
                for dt in GBRange(DP_Number, DP_WeightedSampleSize):
                    addValue(sheet, PJNZParams, GB_RW_DataStartCol + dt,  modvar[survey]['data'][sex][dt][age])
                PJNZParams.currRow += 1
    
    PJNZParams.currRow -= 1    
    addEndTag(sheet, PJNZParams)

def export_ARTCovSurveyUsed(sheet, params, PJNZParams, projection):    
    addStartTag(sheet, PJNZParams, '<ARTCovSurveyUsed MV2>')
    
    modvar = projection[AM_ARTCovSurveyTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)

    for survey in GBRange(DP_PrevSurvey1, DP_PrevSurvey8):
        addValue(sheet, PJNZParams, GB_RW_DataStartCol + survey - 1, int(modvar[survey]['used']))
    
    addEndTag(sheet, PJNZParams)

def export_ARTCovSurveyName(sheet, params, PJNZParams, projection):    
    addStartTag(sheet, PJNZParams, '<ARTCovSurveyName MV2>')
    
    modvar = projection[AM_ARTCovSurveyTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)
    
    for survey in GBRange(DP_PrevSurvey1, DP_PrevSurvey8):
        addValue(sheet, PJNZParams, GB_RW_DataStartCol + survey - 1, modvar[survey]['name'])
    
    addEndTag(sheet, PJNZParams)

def export_ARTCovSurveyYear(sheet, params, PJNZParams, projection):    
    addStartTag(sheet, PJNZParams, '<ARTCovSurveyYear MV2>')
    
    modvar = projection[AM_ARTCovSurveyTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)
    
    for survey in GBRange(DP_PrevSurvey1, DP_PrevSurvey8):
        addValue(sheet, PJNZParams, GB_RW_DataStartCol + survey - 1, modvar[survey]['year'])
    
    addEndTag(sheet, PJNZParams)

def export_MortRateByAge(sheet, params, PJNZParams, projection):    
    addStartTag(sheet, PJNZParams, '<MortRateByAge MV2>')
    
    modvar = projection[AM_MortRateByAgeTag]

    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams,  'Mortality rate by age')

    PJNZParams.currRow += 1
    addValueTag(sheet, PJNZParams)    

    PJNZParams.currRow += 1

    for sex in GBRange(GB_Male, GB_Female):
        addDescript(sheet, PJNZParams, getSexLabel(sex))
        for age in GBRange(DP_A0_4, DP_MAX_AGE):
            values = modvar[sex][age]
            addNote(sheet, PJNZParams, GetAgeName2(age))
            setRowOfYearVals(sheet, values, params, PJNZParams.currRow)    
            PJNZParams.currRow += 1
    
    PJNZParams.currRow -= 1
    addEndTag(sheet, PJNZParams)

def export_AllCauseMortality(sheet, params, PJNZParams, projection):    
    addStartTag(sheet, PJNZParams, '<AllCauseMortality MV2>')
    
    modvar = projection[AM_AllCauseMortalityTag]

    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams,  'All-cause mortality')

    PJNZParams.currRow += 1
    addValueTag(sheet, PJNZParams)    

    PJNZParams.currRow += 1
    
    for sex in GBRange(GB_Male, GB_Female):
        addDescript(sheet, PJNZParams, getSexLabel(sex))
        for age in GBRange(DP_A0_4, DP_MAX_AGE):
            values = modvar[sex][age]
            addNote(sheet, PJNZParams, GetAgeName2(age))
            setRowOfYearVals(sheet, values, params, PJNZParams.currRow)    
            PJNZParams.currRow += 1
    
    PJNZParams.currRow -= 1
    addEndTag(sheet, PJNZParams)

def export_AIDSMortality(sheet, params, PJNZParams, projection):    
    addStartTag(sheet, PJNZParams, '<AIDSMortality MV2>')
    
    modvar = projection[AM_AIDSMortalityTag]

    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams,  'AIDS mortality')

    PJNZParams.currRow += 1
    addValueTag(sheet, PJNZParams)    

    PJNZParams.currRow += 1
    
    for sex in GBRange(GB_Male, GB_Female):
        addDescript(sheet, PJNZParams, getSexLabel(sex))
        for age in GBRange(DP_A0_4, DP_MAX_AGE):
            values = modvar[sex][age]
            addNote(sheet, PJNZParams, GetAgeName2(age))
            setRowOfYearVals(sheet, values, params, PJNZParams.currRow)    
            PJNZParams.currRow += 1
    
    PJNZParams.currRow -= 1
    addEndTag(sheet, PJNZParams)

def export_NumberOnARTByAge(sheet, params, PJNZParams, projection):    
    addStartTag(sheet, PJNZParams, '<NumberOnARTByAge MV2>')
    
    modvar = projection[AM_NumberOnARTByAgeTag]

    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams,  'Number on ART by age')

    PJNZParams.currRow += 1
    addValueTag(sheet, PJNZParams)    

    PJNZParams.currRow += 1
    
    for sex in GBRange(GB_BothSexes, GB_Female):
        addDescript(sheet, PJNZParams, getSexLabel(sex))
        for age in GBRange(DP_A0_4, DP_MAX_AGE):
            values = modvar[sex][age]
            addNote(sheet, PJNZParams, GetAgeName2(age))
            setRowOfYearVals(sheet, values, params, PJNZParams.currRow)    
            PJNZParams.currRow += 1
    
    PJNZParams.currRow -= 1
    addEndTag(sheet, PJNZParams)

def export_NewlyStartingART(sheet, params, PJNZParams, projection):    
    addStartTag(sheet, PJNZParams, '<NewlyStartingART MV>')
    
    modvar = projection[AM_NewlyStartingARTTag]

    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams, 'Adults and children newly starting ART, by age')

    PJNZParams.currRow += 1
    addValueTag(sheet, PJNZParams)    

    PJNZParams.currRow += 1
    
    for sex in GBRange(GB_BothSexes, GB_Female):
        addDescript(sheet, PJNZParams, getSexLabel(sex))
        for age in GBRange(DP_A0_4, DP_MAX_AGE):
            values = modvar[sex][age]
            addNote(sheet, PJNZParams, GetAgeName2(age))
            setRowOfYearVals(sheet, values, params, PJNZParams.currRow)    
            PJNZParams.currRow += 1
    
    PJNZParams.currRow -= 1
    addEndTag(sheet, PJNZParams)

def export_AdultsChildrenStartingART(sheet, params, PJNZParams, projection):    
    addStartTag(sheet, PJNZParams, '<AdultsChildrenStartingART MV>')
    
    modvar = projection[AM_AdultsChildrenStartingARTTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)    

    PJNZParams.currRow += 1
    
    for sex in GBRange(GB_Male, GB_Female):
        addDescript(sheet, PJNZParams, getSexLabel(sex))
        for age in GBRange(DP_AllAges, DP_MAX_AGE):
            values = modvar[sex][age]
            addNote(sheet, PJNZParams, GetAgeName2(age))
            setRowOfYearVals(sheet, values, params, PJNZParams.currRow)    
            PJNZParams.currRow += 1
    
    PJNZParams.currRow -= 1
    addEndTag(sheet, PJNZParams)

def export_PercentOfPop(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<PercentOfPop MV>')
    
    modvar = projection[AM_PercentOfPopTag]

    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams,  'Percent of Population')

    PJNZParams.currRow += 1
    addValueTag(sheet, PJNZParams)    

    values = modvar
    setRowOfYearVals(sheet, values, params, PJNZParams.currRow)
    
    addEndTag(sheet, PJNZParams)

def export_ModelLifeFileName(sheet, params, PJNZParams, projection):   
    addStartTag(sheet, PJNZParams, '<ModelLifeFileName MV2>')
    
    modvar = projection[DP_ModelLifeFileNameTag]

    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams, 'Model Life File Name')
    
    PJNZParams.currRow += 1
    addValueTag(sheet, PJNZParams)
    
    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams, 'Custom Life Table Name')
    addValue(sheet, PJNZParams, GB_RW_DataStartCol, modvar)
    
    addEndTag(sheet, PJNZParams)

def export_UseFYrSingleAges(sheet, params, PJNZParams, projection):   
    addStartTag(sheet, PJNZParams, '<UseFYrSingleAges MV2>')
    
    modvar = projection[DP_UseFYrSingleAgesTag]

    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams, 'Use First Year Single Ages')
    
    PJNZParams.currRow += 1
    addValueTag(sheet, PJNZParams)
    
    PJNZParams.currRow += 1

    if int(modvar) == 1:
      addDescript(sheet, PJNZParams, 'Use First Year Single Age Inputs')
    else:
      addDescript(sheet, PJNZParams, 'Do not use First Year Single Age Inputs')

    addValue(sheet, PJNZParams, GB_RW_DataStartCol, int(modvar))
    
    addEndTag(sheet, PJNZParams)

def export_RegionalAdjustPopData(sheet, params, PJNZParams, projection):    
    addStartTag(sheet, PJNZParams, '<RegionalAdjustPopData MV2>')
    
    modvar = projection[DP_RegionalAdjustPopDataTag]

    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams, 'Regional Adjusted Population Data')
    
    PJNZParams.currRow += 1
    addValueTag(sheet, PJNZParams)
    
    PJNZParams.currRow += 1
    
    for sex in GBRange(GB_Male, GB_Female): 
        addDescript(sheet, PJNZParams, getSexLabel(sex))
        for age in GBRange(0, 80):
            values = modvar[sex][age]
            addNote(sheet, PJNZParams, 'Age: ' + str(age))
            setRowOfYearVals(sheet, values, params, PJNZParams.currRow)    
            PJNZParams.currRow += 1
        
        values = np.zeros(params.finalYear - params.firstYear + 1).tolist()  #old all single-ages sum row
        addNote(sheet, PJNZParams, 'All Ages')
        setRowOfYearVals(sheet, values, params, PJNZParams.currRow)   
        PJNZParams.currRow += 1
       
    PJNZParams.currRow -= 1

    addEndTag(sheet, PJNZParams)

def export_RegionalAdjustPopCBState(sheet, params, PJNZParams, projection):   
    addStartTag(sheet, PJNZParams, '<RegionalAdjustPopCBState MV>')
    
    modvar = projection[DP_RegionalAdjustPopCBStateTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)

    addValue(sheet, PJNZParams, GB_RW_DataStartCol, int(modvar))
    
    addEndTag(sheet, PJNZParams)

def export_RegionalAdjustPopFName(sheet, params, PJNZParams, projection):   
    addStartTag(sheet, PJNZParams, '<RegionalAdjustPopFName MV>')
    
    modvar = projection[DP_RegionalAdjustPopFNameTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)

    addValue(sheet, PJNZParams, GB_RW_DataStartCol, modvar)
    
    addEndTag(sheet, PJNZParams)

def export_RegionalAdjustPopFDate(sheet, params, PJNZParams, projection):   
    addStartTag(sheet, PJNZParams, '<RegionalAdjustPopFDate MV>')
    
    modvar = projection[DP_RegionalAdjustPopFDateTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)

    addValue(sheet, PJNZParams, GB_RW_DataStartCol, modvar)
    
    addEndTag(sheet, PJNZParams)

def export_LifeTableNum(sheet, params, PJNZParams, projection):   
    addStartTag(sheet, PJNZParams, '<LifeTableNum MV2>')
    
    modvar = projection[DP_LifeTableNumTag]

    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams, 'Regional model life tables')
    
    PJNZParams.currRow += 1
    addValueTag(sheet, PJNZParams)
    
    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams, 'Life Table Number')
    addValue(sheet, PJNZParams, GB_RW_DataStartCol, modvar)
    
    addEndTag(sheet, PJNZParams)

def export_FirstYearOfEpidemic(sheet, params, PJNZParams, projection):   
    addStartTag(sheet, PJNZParams, '<FirstYearOfEpidemic MV>')
    
    modvar = projection[AM_FirstYearOfEpidemicTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)
    addValue(sheet, PJNZParams, GB_RW_DataStartCol, modvar)
    
    addEndTag(sheet, PJNZParams)

def export_ARTCoverageSelection(sheet, params, PJNZParams, projection):   
    addStartTag(sheet, PJNZParams, '<ARTCoverageSelection MV>')
    
    modvar = projection[AM_ARTCoverageSelectionTag]

    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams, 'Select method of ART coverage entry')
    
    PJNZParams.currRow += 1
    addValueTag(sheet, PJNZParams)
    addValue(sheet, PJNZParams, GB_RW_DataStartCol, modvar)
    
    addEndTag(sheet, PJNZParams)

def export_BFYearsRGIdx(sheet, params, PJNZParams, projection):   
    addStartTag(sheet, PJNZParams, '<BFYearsRGIdx MV>')
    
    modvar = projection[AM_BFYearsRGIdxTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)
    addValue(sheet, PJNZParams, GB_RW_DataStartCol, modvar)
    
    addEndTag(sheet, PJNZParams)

def export_BFArvRGIdx(sheet, params, PJNZParams, projection):   
    addStartTag(sheet, PJNZParams, '<BFArvRGIdx MV>')
    
    modvar = projection[AM_BFArvRGIdxTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)
    addValue(sheet, PJNZParams, GB_RW_DataStartCol, modvar)
    
    addEndTag(sheet, PJNZParams)

def export_ChildHIVMortARTRegion(sheet, params, PJNZParams, projection):   
    addStartTag(sheet, PJNZParams, '<ChildHIVMortARTRegion MV>')
    
    modvar = projection[AM_ChildHIVMortARTRegionTag]

    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams, 'Annual probability of HIV-related mortality among those on ART by CD4 level at treatment initiation, duration of treatment and age Region for Children')
    
    PJNZParams.currRow += 1
    addValueTag(sheet, PJNZParams)
    addValue(sheet, PJNZParams, GB_RW_DataStartCol, modvar)
    
    addEndTag(sheet, PJNZParams)
            
def export_ChildHIVMortARTCustomFlag(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<ChildHIVMortARTCustomFlag MV>')
    
    modvar = projection[AM_ChildHIVMortARTCustomFlagTag]
    
    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)
    addValue(sheet, PJNZParams, GB_RW_DataStartCol, int(modvar))
    
    addEndTag(sheet, PJNZParams)

def export_ChildARTDistRegion(sheet, params, PJNZParams, projection):   
    addStartTag(sheet, PJNZParams, '<ChildARTDistRegion MV2>')
    
    modvar = projection[AM_ChildARTDistRegionTag]

    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams, 'Probability of initiating ART by age Region for Children')
    
    PJNZParams.currRow += 1
    addValueTag(sheet, PJNZParams)
    addNote(sheet, PJNZParams, getRegionEN(modvar))
    addValue(sheet, PJNZParams, GB_RW_DataStartCol, modvar)
    
    addEndTag(sheet, PJNZParams)
            
def export_ChildARTDistCustomFlag(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<ChildARTDistCustomFlag MV>')
    
    modvar = projection[AM_ChildARTDistCustomFlagTag]
    
    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)
    addValue(sheet, PJNZParams, GB_RW_DataStartCol, int(modvar))
    
    addEndTag(sheet, PJNZParams)

def export_AdultProgressRatesRegion(sheet, params, PJNZParams, projection):   
    addStartTag(sheet, PJNZParams, '<AdultProgressRatesRegion MV2>')
    
    modvar = projection[AM_AdultProgressRatesRegionTag]

    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams, 'Annual rate of progression to next lower CD4 category Region for Adults')
    
    PJNZParams.currRow += 1
    addValueTag(sheet, PJNZParams)
    addNote(sheet, PJNZParams, getRegionEN(modvar))
    addValue(sheet, PJNZParams, GB_RW_DataStartCol, modvar)
    
    addEndTag(sheet, PJNZParams)
            
def export_AdultProgressRatesCustomFlag(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<AdultProgressRatesCustomFlag MV>')
    
    modvar = projection[AM_AdultProgressRatesCustomFlagTag]
    
    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)
    addValue(sheet, PJNZParams, GB_RW_DataStartCol, int(modvar))
    
    addEndTag(sheet, PJNZParams)

def export_AdultHIVMortNoARTRegion(sheet, params, PJNZParams, projection):   
    addStartTag(sheet, PJNZParams, '<AdultHIVMortNoARTRegion MV2>')
    
    modvar = projection[AM_AdultHIVMortNoARTRegionTag]

    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams, 'Annual probability of HIV-related mortality when not on ART Region for Adults')
    
    PJNZParams.currRow += 1
    addValueTag(sheet, PJNZParams)
    addNote(sheet, PJNZParams, getRegionEN(modvar))
    addValue(sheet, PJNZParams, GB_RW_DataStartCol, modvar)
    
    addEndTag(sheet, PJNZParams)
            
def export_AdultHIVMortNoARTCustomFlag(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<AdultHIVMortNoARTCustomFlag MV>')
    
    modvar = projection[AM_AdultHIVMortNoARTCustomFlagTag]
    
    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)
    addValue(sheet, PJNZParams, GB_RW_DataStartCol, int(modvar))
    
    addEndTag(sheet, PJNZParams)

def export_AdultHIVMortARTRegion(sheet, params, PJNZParams, projection):   
    addStartTag(sheet, PJNZParams, '<HIV Mortality with ART Country or Region MV>')
    
    modvar = projection[AM_AdultHIVMortARTRegionTag]

    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams, 'Annual probability of HIV-related mortality on ART by CD4 count at treatment initiation Region')
    
    PJNZParams.currRow += 1
    addValueTag(sheet, PJNZParams)
    addNote(sheet, PJNZParams, getRegionEN(modvar))
    addValue(sheet, PJNZParams, GB_RW_DataStartCol, modvar)
    
    PJNZParams.currRow += 1

    addEndTag(sheet, PJNZParams)
            
def export_AdultHIVMortARTCustomFlag(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<AdultHIVMortARTCustomFlag MV>')
    
    modvar = projection[AM_AdultHIVMortARTCustomFlagTag]
    
    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)
    addValue(sheet, PJNZParams, GB_RW_DataStartCol, int(modvar))
    
    addEndTag(sheet, PJNZParams)

def export_DALYBaseYear(sheet, params, PJNZParams, projection):   
    addStartTag(sheet, PJNZParams, '<DALYBaseYear MV>')
    
    modvar = projection[AM_DALYBaseYearTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)
    addValue(sheet, PJNZParams, GB_RW_DataStartCol, modvar)
    
    addEndTag(sheet, PJNZParams)

def export_DALYDiscountRate(sheet, params, PJNZParams, projection):   
    addStartTag(sheet, PJNZParams, '<DALYDiscountRate MV>')
    
    modvar = projection[AM_DALYDiscountRateTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)
    addValue(sheet, PJNZParams, GB_RW_DataStartCol, modvar)
    
    addEndTag(sheet, PJNZParams)
            
def export_DALYUseStandardLifeTable(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<DALYUseStandardLifeTable MV>')
    
    modvar = projection[AM_DALYUseStandardLifeTableTag]
    
    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)
    addValue(sheet, PJNZParams, GB_RW_DataStartCol, int(modvar))
    
    addEndTag(sheet, PJNZParams)

def export_OrphansRegionalPattern(sheet, params, PJNZParams, projection):   
    addStartTag(sheet, PJNZParams, '<OrphansRegionalPattern MV>')
    
    modvar = projection[AM_OrphansRegionalPatternTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)
    addValue(sheet, PJNZParams, GB_RW_DataStartCol, modvar)
    
    addEndTag(sheet, PJNZParams)
            
def export_IncidenceInput1970Bool(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<IncidenceInput1970Bool MV>')
    
    modvar = projection[AM_IncidenceInput1970BoolTag]
    
    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)
    addValue(sheet, PJNZParams, GB_RW_DataStartCol, int(modvar))
    
    addEndTag(sheet, PJNZParams)

def export_IncidenceOptions(sheet, params, PJNZParams, projection):   
    addStartTag(sheet, PJNZParams, '<IncidenceOptions MV>')
    
    modvar = projection[AM_IncidenceOptionsTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)
    addValue(sheet, PJNZParams, GB_RW_DataStartCol, modvar)
    
    addEndTag(sheet, PJNZParams)

def export_IncidenceByFit(sheet, params, PJNZParams, projection):   
    addStartTag(sheet, PJNZParams, '<IncidenceByFit MV4>')
    
    modvar = projection[AM_IncidenceByFitTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)
    
    labels = {
        DP_DirectIncidenceInputOpt  : 'Direct incidence input (15 - 49)',
        DP_EPPIncOpt                : 'EPP Incidence (15 - 49)',
        DP_AEMIncOpt                : 'AEM Incidence (15-49)',
        DP_FitToProgramDataOpt      : 'Fit incidence in CSAVR',
        DP_FitToMortalityDataOpt    : 'Fit incidence to mortality data',
        DP_ECDCOpt                  : 'ECDC'
    }

    for i in GBRange(DP_DirectIncidenceInputOpt, DP_ECDCOpt):
        values = modvar[i]
        addNote(sheet, PJNZParams, labels[i])
        setRowOfYearVals(sheet, values, params, PJNZParams.currRow)    
        PJNZParams.currRow += 1
    
    PJNZParams.currRow -= 1
    addEndTag(sheet, PJNZParams)

def export_FourDecPlaceID(sheet, params, PJNZParams, projection):   
    addStartTag(sheet, PJNZParams, '<FourDecPlaceID MV2>')
    
    modvar = projection[AM_FourDecPlaceIDTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)

    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams, 'Four Decimal ID')
    addValue(sheet, PJNZParams, GB_RW_DataStartCol, int(modvar))
    
    addEndTag(sheet, PJNZParams)
            
def export_EPPPrevAdj(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<EPPPrevAdj MV>')
    
    modvar = projection[AM_EPPPrevAdjTag]
    
    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)
    addValue(sheet, PJNZParams, GB_RW_DataStartCol, int(modvar))
    
    addEndTag(sheet, PJNZParams)
            
def export_EPPMaxAdjFactor(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<EPPMaxAdjFactor MV>')
    
    modvar = projection[AM_EPPMaxAdjFactorTag]
    
    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)
    addValue(sheet, PJNZParams, GB_RW_DataStartCol, modvar)
    
    addEndTag(sheet, PJNZParams)
            
def export_EPPPopulationAges(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<EPPPopulationAges MV>')
    
    modvar = projection[AM_EPPPopulationAgesTag]
    
    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)
    addNote(sheet, PJNZParams, 'Adults 15-49 = 0; Adults 15+ = 1')
    addValue(sheet, PJNZParams, GB_RW_DataStartCol, modvar)
    
    addEndTag(sheet, PJNZParams)
            
def export_IncEpidemicRGIdx(sheet, params, PJNZParams, projection):
    DP_FittedPattern            = 6
    DP_CSAVRPattern             = 7

    addStartTag(sheet, PJNZParams, '<IncEpidemicRGIdx MV>')
    
    value = projection[AM_CustomSAPDataIndexTag]
    if value in [DP_HIVPrevFixed_Index, DP_HIVPrevTime_Index, DP_FittedToART_Index]:
        value = DP_FittedPattern
    elif value == DP_PatternFromCSAVR_Index:
        value = DP_CSAVRPattern

    value = max(value, projection[AM_DefaultEpidemicTag])
    
    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)
    addValue(sheet, PJNZParams, GB_RW_DataStartCol, value)
    
    addEndTag(sheet, PJNZParams)
            
def export_SAPFitType(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<SAPFitType MV>')

    value = DP_SAP_HIVPrevByAge
    if projection[AM_CustomSAPDataIndexTag] in [DP_HIVPrevFixed_Index, DP_HIVPrevTime_Index]:   
        value = DP_SAP_HIVPrevByAge
    elif projection[AM_CustomSAPDataIndexTag] == DP_FittedToART_Index:
        value = DP_SAP_ARTByAge
  
    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)
    addValue(sheet, PJNZParams, GB_RW_DataStartCol, value)
    
    addEndTag(sheet, PJNZParams)
            
def export_HIVPrevModel(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<HIVPrevModel MV>')

    value = DP_SAP_FixedIROverTime
    if projection[AM_CustomSAPDataIndexTag] == DP_HIVPrevFixed_Index:   
        value = DP_SAP_FixedIROverTime
    elif projection[AM_CustomSAPDataIndexTag] == DP_HIVPrevTime_Index:
        value = DP_SAP_TimeDependentIR

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)
    addValue(sheet, PJNZParams, GB_RW_DataStartCol, value)
    
    addEndTag(sheet, PJNZParams)
            
def export_IncEpidemicCustomFlagIdx(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<IncEpidemicCustomFlagIdx MV>')
    
    modvar = projection[AM_IncEpidemicCustomFlagTag]
    
    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)
    addValue(sheet, PJNZParams, GB_RW_DataStartCol, int(modvar))
    
    addEndTag(sheet, PJNZParams)
            
def export_SexRatioFromEPP(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<SexRatioFromEPP MV>')
    
    modvar = projection[AM_SexRatioFromEPPTag]
    
    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams, 'Sex Ratio from EPP')
    
    PJNZParams.currRow += 1
    addValueTag(sheet, PJNZParams)
    addValue(sheet, PJNZParams, GB_RW_DataStartCol, int(modvar))
    
    addEndTag(sheet, PJNZParams)

def export_HIVSexRatioFromEPP(sheet, params, PJNZParams, projection):
    format2(sheet, params, PJNZParams, projection, '<HIVSexRatioFromEPP MV>', AM_HIVSexRatioFromEPPTag, 'HIV sex ratio from EPP')
            
def export_EpidemicTypeFromEPP(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<EpidemicTypeFromEPP MV>')
    
    modvar = projection[AM_EpidemicTypeFromEPPTag]
    
    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams, 'Epidemic Type from EPP')
    
    PJNZParams.currRow += 1
    addValueTag(sheet, PJNZParams)
    addValue(sheet, PJNZParams, GB_RW_DataStartCol, modvar)
    
    addEndTag(sheet, PJNZParams)

def export_ChangesLog(sheet, params, PJNZParams, projection):  
    addStartTag(sheet, PJNZParams, '<ChangesLog MV>')
    modvar = projection[AM_ChangesLogTag]
    
    PJNZParams.currRow += 2
    
    addValueTag(sheet, PJNZParams)
    
    count = len(modvar)
    addValue(sheet, PJNZParams, GB_RW_DataStartCol, count)
    
    for s in GBRange(1, count):
        addValue(sheet, PJNZParams, GB_RW_DataStartCol + s, modvar[s - 1])

    addEndTag(sheet, PJNZParams)

def export_AdultPrevalence(sheet, params, PJNZParams, projection):
    format2(sheet, params, PJNZParams, projection, '<AdultPrevalence MV>', AM_AdultPrevalenceTag, 'Adult prevalence')
            
def export_NumOfEPPEpidemics(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<NumOfEPPEpidemics MV>')
    
    modvar = projection[AM_NumOfEPPEpidemicsTag]    
    
    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams, 'Number of EPP Epidemics')
    
    PJNZParams.currRow += 1
    addValueTag(sheet, PJNZParams)
    addValue(sheet, PJNZParams, GB_RW_DataStartCol, modvar)
    
    addEndTag(sheet, PJNZParams)
            
def export_EPPCountryName(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<EPPCountryName MV>')
    
    modvar = projection[AM_EPPCountryNameTag]    
    
    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams, 'EPP Country Name')
    
    PJNZParams.currRow += 1
    addValueTag(sheet, PJNZParams)
    addValue(sheet, PJNZParams, GB_RW_DataStartCol, modvar)
    
    addEndTag(sheet, PJNZParams)
            
def export_EPPEpiName(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<EPPEpiName MV>')
    
    modvar = projection[AM_EPPEpiNameTag]

    numEpidemics = projection[AM_NumOfEPPEpidemicsTag]
    
    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams, 'EPP Epidemic Name')
    
    PJNZParams.currRow += 1
    addValueTag(sheet, PJNZParams)
    
    for epi in GBRange(DP_MinEpidemic, numEpidemics):
        if epi < len(modvar):
            sheetInsertRow(sheet, PJNZParams.currRow, [modvar[epi]])
            PJNZParams.currRow += 1
    
    addEndTag(sheet, PJNZParams)
            
def export_EPPEpidemic(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<EPPEpidemic MV>')
    
    modvar = projection[AM_EPPEpidemicTag]

    numEpidemics = projection[AM_NumOfEPPEpidemicsTag]
    
    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams, 'EPP Epidemic')
    
    PJNZParams.currRow += 1
    addValueTag(sheet, PJNZParams)
    
    for epi in GBRange(DP_MinEpidemic, numEpidemics):
        sheetInsertRow(sheet, PJNZParams.currRow, [modvar[epi]])
        PJNZParams.currRow += 1
    
    addEndTag(sheet, PJNZParams)
            
def export_EPPPrevData(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<EPPPrevData MV>')
    
    modvar = projection[AM_EPPPrevDataTag]

    numEpidemics = projection[AM_NumOfEPPEpidemicsTag]
    
    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams, 'EPP Prevalence Data')
    
    PJNZParams.currRow += 1
    addValueTag(sheet, PJNZParams)
    
    hasData = False
    
    for epi in GBRange(DP_MinEpidemic, numEpidemics):
        hasData = True
        values = modvar[epi]
        sheetInsertRow(sheet, PJNZParams.currRow, values)
        PJNZParams.currRow += 1
    
    if hasData:
        PJNZParams.currRow -= 1

    addEndTag(sheet, PJNZParams)
            
def export_EPPIncData(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<EPPIncData MV>')
    
    modvar = projection[AM_EPPIncDataTag]

    numEpidemics = projection[AM_NumOfEPPEpidemicsTag]
    
    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams, 'EPP Incidence Data')
    
    PJNZParams.currRow += 1
    addValueTag(sheet, PJNZParams)

    hasData = False

    for epi in GBRange(DP_MinEpidemic, numEpidemics):
        hasData = True
        values = modvar[epi]
        sheetInsertRow(sheet, PJNZParams.currRow, values)
        PJNZParams.currRow += 1
    
    if hasData:
        PJNZParams.currRow -= 1
         
    addEndTag(sheet, PJNZParams)
            
def export_EPPPopData(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<EPPPopData MV>')
    
    modvar = projection[AM_EPPPopDataTag]

    numEpidemics = projection[AM_NumOfEPPEpidemicsTag]
    
    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams, 'EPP Pop Data')
    
    PJNZParams.currRow += 1
    addValueTag(sheet, PJNZParams)

    hasData = False

    for epi in GBRange(DP_MinEpidemic, numEpidemics):
        hasData = True
        values = modvar[epi]
        sheetInsertRow(sheet, PJNZParams.currRow, values)
        PJNZParams.currRow += 1
    
    if hasData:
        PJNZParams.currRow -= 1

    addEndTag(sheet, PJNZParams)
            
def export_EPPSexRatio(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<EPPSexRatio MV>')
    
    modvar = projection[AM_EPPSexRatioTag]

    
    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams, 'Sex Ratio from EPP')
    
    PJNZParams.currRow += 1
    addValueTag(sheet, PJNZParams)

    PJNZParams.currRow += 1

    # NOTE: Though it makes sense to not output something if it has no values,
    # the desktop currently outputs all 500. So mimicing that here will mean
    # that if we want to change it, it would be best to change it here AND the desktop
    # Also, we don't know if EPP is reading in all 500 rows instead of checking
    # for how many numOfEPPEpidemics there are like in other places.
    # Skipping doing this for now.

    numEpidemics = projection[AM_NumOfEPPEpidemicsTag]
    for epi in GBRange(DP_MinEpidemic, numEpidemics):
        # for epi in GBRange(DP_MinEpidemic, DP_MaxEpidemic):
        values = modvar[epi]
        addNote(sheet, PJNZParams, 'Epidemic: ' + str(epi))
        sheetInsertRow(sheet, PJNZParams.currRow, values)
        PJNZParams.currRow += 1

    # sheet.sheet.loc[PJNZParams.currRow:PJNZParams.currRow+len(modvar[epi])] =    
    
    PJNZParams.currRow -= 1
    addEndTag(sheet, PJNZParams)
            
def export_EPPBaseYrPop(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<EPPBaseYrPop MV>')
    
    modvar = projection[AM_EPPBaseYrPopTag]

    numEpidemics = projection[AM_NumOfEPPEpidemicsTag]
    
    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams, 'EPP Base Year Population')
    
    PJNZParams.currRow += 1
    addValueTag(sheet, PJNZParams)
    
    # Desktop includes the 0th
    if numEpidemics > 0:
        for epi in GBRange(DP_CountryID, numEpidemics):
            addValue(sheet, PJNZParams, GB_RW_DataStartCol + epi - DP_CountryID, modvar[epi])
    else:
        addValue(sheet, PJNZParams, GB_RW_DataStartCol, 0.0)
    
    addEndTag(sheet, PJNZParams)
            
def export_EPPIDUMortality(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<EPPIDUMortality MV>')
    
    modvar = projection[AM_EPPIDUMortalityTag]

    numEpidemics = projection[AM_NumOfEPPEpidemicsTag]
    
    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)

    # Desktop includes the 0th
    if numEpidemics > 0:
        for epi in GBRange(DP_CountryID, numEpidemics):
            addValue(sheet, PJNZParams, GB_RW_DataStartCol + epi - DP_CountryID, modvar[epi])
    else:
        addValue(sheet, PJNZParams, GB_RW_DataStartCol, 0.0)
    
        
    addEndTag(sheet, PJNZParams)
            
def export_EPPPathInfo(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<EPPPathInfo MV>')
    
    modvar = projection[AM_EPPPathInfoTag]

    numEpidemics = projection[AM_NumOfEPPEpidemicsTag]
    
    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams, 'EPP Path Info')
    
    PJNZParams.currRow += 1
    addValueTag(sheet, PJNZParams)

    if numEpidemics > 0:
        for epi in GBRange(DP_MinEpidemic, numEpidemics):
            sheetInsertRow(sheet, PJNZParams.currRow, [int(modvar[epi]['IsTotal']), modvar[epi]['FullName']])
            PJNZParams.currRow += 1
        PJNZParams.currRow -= 1
    
    addEndTag(sheet, PJNZParams)

def export_EppAgeRange(sheet, params, PJNZParams, projection):   
    addStartTag(sheet, PJNZParams, '<EppAgeRange MV>')
    
    modvar = projection[AM_EPPAgeRangeTag]

    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams, 'EPP Age Range')
    
    PJNZParams.currRow += 1
    addValueTag(sheet, PJNZParams)
    addValue(sheet, PJNZParams, GB_RW_DataStartCol, modvar)
    
    addEndTag(sheet, PJNZParams)

def export_YrPtPrevalence_WB(sheet, params, PJNZParams, projection):   
    addStartTag(sheet, PJNZParams, '<YrPtPrevalence_WB MV2>')
    
    modvar = projection[AM_YrPtPrevalence_WBTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)

    if modvar == '':
        addValue(sheet, PJNZParams, GB_RW_DataStartCol, "None")
    else:
        addValue(sheet, PJNZParams, GB_RW_DataStartCol, modvar)
    
    addEndTag(sheet, PJNZParams)

def export_AIDSDeathsAmongIDU(sheet, params, PJNZParams, projection):
    format2(sheet, params, PJNZParams, projection, '<AIDSDeathsAmongIDU MV>', AM_AIDSDeathsAmongIDUTag)
            
def export_PropIDU_WB(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<PropIDU_WB MV>')
    
    modvar = projection[AM_PropIDU_WBTag]
    
    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)

    PJNZParams.currRow += 1

    # NOTE: Though it makes sense to not output something if it has no values,
    # the desktop currently outputs all 500. So mimicing that here will mean
    # that if we want to change it, it would be best to change it here AND the desktop
    # Also, we don't know if EPP is reading in all 500 rows instead of checking
    # for how many numOfEPPEpidemics there are like in other places.
    # Also, note this starts from 0 and not 1. Why? Dunno, desktop does it.
    # Skipping doing this for now.

    numEpidemics = projection[AM_NumOfEPPEpidemicsTag]
    if numEpidemics > 0:
        for epi in GBRange(DP_CountryID, projection[AM_NumOfEPPEpidemicsTag]):
            # for epi in GBRange(DP_CountryID, DP_MaxEpidemic):
            values = modvar[epi]
            addDescript(sheet, PJNZParams, 'Epidemic: ' + str(epi))
            sheetInsertRow(sheet, PJNZParams.currRow, values)
            PJNZParams.currRow += 1
        
    PJNZParams.currRow -= 1
    addEndTag(sheet, PJNZParams)
            
def export_NonAIDSDeathsAmongIDU(sheet, params, PJNZParams, projection):
    format2(sheet, params, PJNZParams, projection, '<NonAIDSDeathsAmongIDU MV>', AM_NonAIDSDeathsAmongIDUTag)

def export_SurvRate(sheet, params, PJNZParams, projection):   
    addStartTag(sheet, PJNZParams, '<SurvRate MV2>')
    
    modvar = projection[DP_SurvRateTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)

    PJNZParams.currRow += 1

    for sex in GBRange(GB_Male, GB_Female):
        addDescript(sheet, PJNZParams, getSexLabel(sex))
        for sr in GBRange(1, 82):
            values = modvar[sr][sex]
            if sr < 82:
                addNote(sheet, PJNZParams, 'Age: ' + str(sr-1))
            else:
                addNote(sheet, PJNZParams, 'Age: 80+')
            setRowOfYearVals(sheet, values, params, PJNZParams.currRow)    
            PJNZParams.currRow += 1
       
    PJNZParams.currRow -= 1
    
    addEndTag(sheet, PJNZParams)

def export_SexuallyActive15to19(sheet, params, PJNZParams, projection):    
    addStartTag(sheet, PJNZParams, '<SexuallyActive15to19 MV2>')
    
    modvar = projection[AM_SexuallyActive15to19Tag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)

    PJNZParams.currRow += 1    
    addValue(sheet, PJNZParams, GB_RW_DataStartCol,  modvar['value'])
    addValue(sheet, PJNZParams, GB_RW_DataStartCol + 1,  modvar['str'])
    
    addEndTag(sheet, PJNZParams)
            
def export_AIDSMortAllAgesFYrAdjIdx(sheet, params, PJNZParams, projection):   
    addStartTag(sheet, PJNZParams, '<AIDSMortAllAgesFYrAdjIdx MV>')
    
    modvar = projection[AM_AIDSMortAllAgesFYrAdjIdxTag]

    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)
    addValue(sheet, PJNZParams, GB_RW_DataStartCol,  modvar)
    
    addEndTag(sheet, PJNZParams)

def export_ValidationAllCauseDeathsART(sheet, params, PJNZParams, projection):
    format2(sheet, params, PJNZParams, projection, '<AllCauseDeathsARTValidation MV>', AM_ValidationAllCauseDeathsARTTag)

def export_PrevNeedFirstTime(sheet, params, PJNZParams, projection):   
    addStartTag(sheet, PJNZParams, '<PreventionNeeds_FirstTime MV>')
    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)
    
    # Prevention needs will always have data. 
    if 'data' not in projection[AM_PreventionNeedsKeyPopsTag]:
        addValue(sheet, PJNZParams, GB_RW_DataStartCol, '0')
    else:
        addValue(sheet, PJNZParams, GB_RW_DataStartCol, '1')
    
    addEndTag(sheet, PJNZParams)
    pass

def export_PrevNeedShowVMMC(sheet, params, PJNZParams, projection):   
    addStartTag(sheet, PJNZParams, '<PreventionNeeds_ShowVMMCTab MV>') 
    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)
    if projection[AM_PreventionNeedsShowVMMCTabTag]:
        addValue(sheet, PJNZParams, GB_RW_DataStartCol, '1')
    else:
        addValue(sheet, PJNZParams, GB_RW_DataStartCol, '0')
    
    addEndTag(sheet, PJNZParams)

    pass

def export_PrevNeedKeyPop(sheet, params, PJNZParams, projection):   
    addStartTag(sheet, PJNZParams, '<PreventionNeeds_KeyPops MV>') 
    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)
    PJNZParams.currRow += 1
    modvar = projection[AM_PreventionNeedsKeyPopsTag]
    
    KeyPopsLabels = {
        DP_kpFSW : 'FSW',
        DP_kpMSM : 'MSM',
        DP_kpPWID : 'PWID',
        DP_kpTG : 'TG'
    }

    for kp in range(len(DP_TKeyPopType)):
        addDescript(sheet, PJNZParams, KeyPopsLabels[kp] + 'pop')
        addValue(sheet, PJNZParams, GB_RW_DataStartCol,  modvar['data'][kp]['population'])
        PJNZParams.currRow += 1

    for kp in range(len(DP_TKeyPopType)):
        addDescript(sheet, PJNZParams, KeyPopsLabels[kp] + 'cov')
        addValue(sheet, PJNZParams, GB_RW_DataStartCol,  modvar['data'][kp]['coverage'])
        PJNZParams.currRow += 1

    addDescript(sheet, PJNZParams, 'Ratio')
    addValue(sheet, PJNZParams, GB_RW_DataStartCol,  modvar['ratio'])
    PJNZParams.currRow += 1

    for kp in range(len(DP_TKeyPopType)):
        addDescript(sheet, PJNZParams, KeyPopsLabels[kp] + 'source')
        addValue(sheet, PJNZParams, GB_RW_DataStartCol,  modvar['data'][kp]['source'])
        PJNZParams.currRow += 1

    for kp in range(len(DP_TKeyPopType)):
        addDescript(sheet, PJNZParams, KeyPopsLabels[kp] + 'usercov')
        addValue(sheet, PJNZParams, GB_RW_DataStartCol,  modvar['data'][kp]['userCoverage'])
        PJNZParams.currRow += 1

    PJNZParams.currRow -= 1
    addEndTag(sheet, PJNZParams)
    pass


def export_PrevNeedVMMC(sheet, params, PJNZParams, projection): 
    pass  
    addStartTag(sheet, PJNZParams, '<PreventionNeeds_VMMC MV>') 
    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)
    PJNZParams.currRow += 1
    
    for area in projection[AM_PreventionNeedsVMMCTag]:
        addValue(sheet, PJNZParams, GB_RW_DescriptCol  ,  area['region'])
        addValue(sheet, PJNZParams, GB_RW_NotesCol  ,     area['name'])
        addValue(sheet, PJNZParams, GB_RW_DataStartCol  ,  area['popFirstYear'])
        addValue(sheet, PJNZParams, GB_RW_DataStartCol+1,  area['popFinalYear'])
        addValue(sheet, PJNZParams, GB_RW_DataStartCol+2,  area['covFirstYear'])
        addValue(sheet, PJNZParams, GB_RW_DataStartCol+3,  area['targetCov'])
        addValue(sheet, PJNZParams, GB_RW_DataStartCol+4,  area['tradCircum'])
        addValue(sheet, PJNZParams, GB_RW_DataStartCol+5,  area['percAged15'])
        addValue(sheet, PJNZParams, GB_RW_DataStartCol+6,  area['percAged29'])
        PJNZParams.currRow += 2
    addEndTag(sheet, PJNZParams)
    pass


def export_PrevNeedCondoms(sheet, params, PJNZParams, projection):   
    addStartTag(sheet, PJNZParams, '<PreventionNeeds_Condoms MV>') 
    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)
    PJNZParams.currRow += 1

    CondomLabels = {
        DP_Condom_Sero : 'Condom_Sero',
        DP_Condom_Sex_workers : 'Condom_Sex_workers',
        DP_Condom_MSM : 'Condom_MSM',
        DP_Condom_YP_15_24_nr_partners : 'Condom_YP_15_24_nr_partners',
        DP_Condom_MW_25_34_nr_partners : 'Condom_MW_25_34_nr_partners',
        DP_Condom_MW_35_49_nr_partners : 'Condom_MW_35_49_nr_partners',
        DP_Condom_MW_50_plus_nr_partners : 'Condom_MW_50_plus_nr_partners',
        DP_Condom_Couples_using_condoms_FP : 'Condom_Couples_using_condoms_FP',
        DP_Condom_Unmet_need_FP : 'Condom_Unmet_need_FP',
        DP_Condom_PWID : 'Condom_PWID',
        DP_Condom_TG : 'Condom_TG'
    }

    modvar = projection[AM_PreventionNeedsCondomsTag]
    for condom in range(len(DP_TCondomType)):
        addDescript(sheet, PJNZParams, CondomLabels[condom] + ' PopFirstYear')
        addValue(sheet, PJNZParams, GB_RW_DataStartCol,  modvar['data'][condom]['popFirstYear'])
        PJNZParams.currRow += 1

    for condom in range(len(DP_TCondomType)):
        addDescript(sheet, PJNZParams, CondomLabels[condom] + ' PopFinalYear')
        addValue(sheet, PJNZParams, GB_RW_DataStartCol,  modvar['data'][condom]['popFinalYear'])
        PJNZParams.currRow += 1

    for condom in range(len(DP_TCondomType)):
        addDescript(sheet, PJNZParams, CondomLabels[condom] + ' BaselineCov')
        addValue(sheet, PJNZParams, GB_RW_DataStartCol,  modvar['data'][condom]['baselineCov'])
        PJNZParams.currRow += 1

    for condom in range(len(DP_TCondomType)):
        addDescript(sheet, PJNZParams, CondomLabels[condom] + ' TargetCov')
        addValue(sheet, PJNZParams, GB_RW_DataStartCol,  modvar['data'][condom]['targetCov'])
        PJNZParams.currRow += 1

    for condom in range(len(DP_TCondomType)):
        addDescript(sheet, PJNZParams, CondomLabels[condom] + ' SexActs')
        addValue(sheet, PJNZParams, GB_RW_DataStartCol,  modvar['data'][condom]['sexActs'])
        PJNZParams.currRow += 1

    for condom in range(len(DP_TCondomType)):
        addDescript(sheet, PJNZParams, CondomLabels[condom] + ' Wastage')
        addValue(sheet, PJNZParams, GB_RW_DataStartCol,  modvar['data'][condom]['wastage'])
        PJNZParams.currRow += 1

    PJNZParams.currRow -= 1
    addEndTag(sheet, PJNZParams)

   
def export_PrevNeedPrEP(sheet, params, PJNZParams, projection):   
    addStartTag(sheet, PJNZParams, '<PreventionNeeds_PrEP MV3>')
    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)
    PJNZParams.currRow += 1
    modvar = projection[AM_PreventionNeedsPrEPTag]
    for PP in range(len(DP_TPrEPType)):
        addValue(sheet, PJNZParams, GB_RW_DescriptCol,'PrEP_' + DP_PrevNeedPrEPTypeName[PP])
        addValue(sheet, PJNZParams, GB_RW_DataStartCol,  PP)
        addValue(sheet, PJNZParams, GB_RW_DataStartCol+1,  'PopFirstYear')
        addValue(sheet, PJNZParams, GB_RW_DataStartCol+2,  modvar['data'][PP]['PopFirstYear'])
        PJNZParams.currRow += 1

    for PP in range(len(DP_TPrEPType)):
        addValue(sheet, PJNZParams, GB_RW_DescriptCol, 'PrEP_' + DP_PrevNeedPrEPTypeName[PP])
        addValue(sheet, PJNZParams, GB_RW_DataStartCol,  PP)
        addValue(sheet, PJNZParams, GB_RW_DataStartCol+1,  'PopFinalYear')
        addValue(sheet, PJNZParams, GB_RW_DataStartCol+2,  modvar['data'][PP]['PopFinalYear'])
        PJNZParams.currRow += 1

    for PP in range(len(DP_TPrEPType)):
        addValue(sheet, PJNZParams, GB_RW_DescriptCol, 'PrEP_' + DP_PrevNeedPrEPTypeName[PP])
        addValue(sheet, PJNZParams, GB_RW_DataStartCol,  PP)
        addValue(sheet, PJNZParams, GB_RW_DataStartCol+1,  'Prev')
        addValue(sheet, PJNZParams, GB_RW_DataStartCol+2,  modvar['data'][PP]['Prev'])
        PJNZParams.currRow += 1

    for PP in range(len(DP_TPrEPType)):
        addValue(sheet, PJNZParams, GB_RW_DescriptCol, 'PrEP_' + DP_PrevNeedPrEPTypeName[PP])
        addValue(sheet, PJNZParams, GB_RW_DataStartCol,  PP)
        addValue(sheet, PJNZParams, GB_RW_DataStartCol+1,  'PrEPCov')
        addValue(sheet, PJNZParams, GB_RW_DataStartCol+2,  modvar['data'][PP]['PrEPCov'])
        PJNZParams.currRow += 1

    for PP in range(len(DP_TPrEPType)):
        addValue(sheet, PJNZParams, GB_RW_DescriptCol, 'PrEP_' + DP_PrevNeedPrEPTypeName[PP])
        addValue(sheet, PJNZParams, GB_RW_DataStartCol,  PP)
        addValue(sheet, PJNZParams, GB_RW_DataStartCol+1,  'TargetCov')
        addValue(sheet, PJNZParams, GB_RW_DataStartCol+2,  modvar['data'][PP]['TargetCov'])
        PJNZParams.currRow += 1

    for pr in range(DP_PreventionNeeds_PrEPYearLen):
        for PP in range(len(DP_TPrEPType)):
            addValue(sheet, PJNZParams, GB_RW_DescriptCol, 'PrEP_' + DP_PrevNeedPrEPTypeName[PP])
            addValue(sheet, PJNZParams, GB_RW_DataStartCol,  PP)
            addValue(sheet, PJNZParams, GB_RW_DataStartCol+1, 'Oral')
            addValue(sheet, PJNZParams, GB_RW_DataStartCol+2, pr+1)
            addValue(sheet, PJNZParams, GB_RW_DataStartCol+3, modvar['data'][PP]['Oral'][pr])
            PJNZParams.currRow += 1

    for pr in range(DP_PreventionNeeds_PrEPYearLen):
        for PP in range(len(DP_TPrEPType)):
            addValue(sheet, PJNZParams, GB_RW_DescriptCol, 'PrEP_' + DP_PrevNeedPrEPTypeName[PP])
            addValue(sheet, PJNZParams, GB_RW_DataStartCol,  PP)
            addValue(sheet, PJNZParams, GB_RW_DataStartCol+1, 'Ring')
            addValue(sheet, PJNZParams, GB_RW_DataStartCol+2, pr+1)
            addValue(sheet, PJNZParams, GB_RW_DataStartCol+3, modvar['data'][PP]['Ring'][pr])
            PJNZParams.currRow += 1

    for pr in range(DP_PreventionNeeds_PrEPYearLen):
        for PP in range(len(DP_TPrEPType)):
            addValue(sheet, PJNZParams, GB_RW_DescriptCol, 'PrEP_' + DP_PrevNeedPrEPTypeName[PP])
            addValue(sheet, PJNZParams, GB_RW_DataStartCol,  PP)
            addValue(sheet, PJNZParams, GB_RW_DataStartCol+1, 'TwoMonth')
            addValue(sheet, PJNZParams, GB_RW_DataStartCol+2, pr+1)
            addValue(sheet, PJNZParams, GB_RW_DataStartCol+3, modvar['data'][PP]['TwoMonth'][pr])
            PJNZParams.currRow += 1

    for pr in range(DP_PreventionNeeds_PrEPYearLen):
        for PP in range(len(DP_TPrEPType)):
            addValue(sheet, PJNZParams, GB_RW_DescriptCol, 'PrEP_' + DP_PrevNeedPrEPTypeName[PP])
            addValue(sheet, PJNZParams, GB_RW_DataStartCol,  PP)
            addValue(sheet, PJNZParams, GB_RW_DataStartCol+1, 'SixMonth')
            addValue(sheet, PJNZParams, GB_RW_DataStartCol+2, pr+1)
            addValue(sheet, PJNZParams, GB_RW_DataStartCol+3, modvar['data'][PP]['SixMonth'][pr])
            PJNZParams.currRow += 1
    
    PJNZParams.currRow -= 1
    addEndTag(sheet, PJNZParams)

    
def export_PrEPParameters(sheet, params, PJNZParams, projection):   
    addStartTag(sheet, PJNZParams, '<PrEPParameters MV>')

    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams, 'PrEP parameters')
    PJNZParams.currRow += 1
    addValueTag(sheet, PJNZParams)
    PJNZParams.currRow += 1

    modvar = projection[AM_PMTCTPrEPParametersTag]

    addNote(sheet, PJNZParams, 'PrEPParameters_OralPrEPAdnerence')
    addValue(sheet, PJNZParams, GB_RW_DataStartCol, modvar['adherence']['oral'] )
    PJNZParams.currRow += 1

    addNote(sheet, PJNZParams, 'PrEPParameters_LongActingPrEPAdherence')
    addValue(sheet, PJNZParams, GB_RW_DataStartCol, modvar['adherence']['injectable'] )
    PJNZParams.currRow += 1
    
    addNote(sheet, PJNZParams, 'PrEPParameters_RatioIncidence')
    addValue(sheet, PJNZParams, GB_RW_DataStartCol, modvar['selection']['incidenceRatio'] )
    PJNZParams.currRow += 1
    
    addNote(sheet, PJNZParams, 'PrEPParameters_OralPersonYears')
    addValue(sheet, PJNZParams, GB_RW_DataStartCol, modvar['personYearsPrEP']['oral'] )
    PJNZParams.currRow += 1
    
    addNote(sheet, PJNZParams, 'PrEPParameters_InjectablePersonYears')
    addValue(sheet, PJNZParams, GB_RW_DataStartCol, modvar['personYearsPrEP']['injectable'] )
    
    addEndTag(sheet, PJNZParams)
    pass
        
def export_PrEPForPregnantWomen(sheet, params, PJNZParams, projection):   
    addStartTag(sheet, PJNZParams, '<PrEPForPregnantWomen MV>')
    PJNZParams.currRow += 1

    addDescript(sheet, PJNZParams, 'PrEP for pregnant and breastfeeding women')
    PJNZParams.currRow += 1

    addValueTag(sheet, PJNZParams)

    setRowOfYearVals(sheet, projection[AM_PMTCTReceivingOralPrEPTag], params, PJNZParams.currRow)    
    PJNZParams.currRow += 1
    setRowOfYearVals(sheet,  projection[AM_PMTCTReceivingInjectablePrEPTag], params, PJNZParams.currRow)    
    addEndTag(sheet, PJNZParams)
    pass

def export_KOSNewDiagnosesAdults15Plus(sheet, params, PJNZParams, projection):   
    addStartTag(sheet, PJNZParams, '<KOSNewDiagnosesAdults15Plus MV>')
    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)

    setRowOfYearVals(sheet, projection[AM_KOSNewDiagnosesAdults15PlusTag], params, PJNZParams.currRow)    
    addEndTag(sheet, PJNZParams)
    pass

def export_KOSNewDiagnosesChildren0to14(sheet, params, PJNZParams, projection):   
    addStartTag(sheet, PJNZParams, '<KOSNewDiagnosesChildren0_14 MV>')
    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)
    
    setRowOfYearVals(sheet, projection[AM_KOSNewDiagnosesChildren0t14Tag], params, PJNZParams.currRow)   
    addEndTag(sheet, PJNZParams)
    pass

def export_KOSNewDiagnosesRecCD4Test(sheet, params, PJNZParams, projection):   
    addStartTag(sheet, PJNZParams, '<KOSNewDiagnosesRecCD4Test MV>')
    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)
    
    setRowOfYearVals(sheet, projection[AM_KOSNewDiagnosesRecCD4TestTag], params, PJNZParams.currRow)    
    addEndTag(sheet, PJNZParams)
    pass
#############################################################################################################################
#############################################################################################################################
#############################################################################################################################
#############################################################################################################################
#############################################################################################################################
#############################################################################################################################
#############################################################################################################################
#############################################################################################################################
#############################################################################################################################
#############################################################################################################################
#############################################################################################################################
#############################################################################################################################
#############################################################################################################################
#############################################################################################################################
#############################################################################################################################
#############################################################################################################################
#############################################################################################################################
#############################################################################################################################
#############################################################################################################################
#############################################################################################################################

def export_AIDSDeaths(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<AIDSDeaths MV2>')
    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)
    PJNZParams.currRow += 1
    num_years = params.finalYear-params.firstYear+1
    aids_deaths = np.zeros((GB_Female+1, GB_MAX_AGE+1, num_years))
    
    for sex in GBRange(GB_Male, GB_Female):
        aids_deaths[sex][GB_AllAges] = np.sum(projection[AM_AIDSDeathsByAgeTag][sex][0:], axis=0)
        aids_deaths[sex][GB_A0_4]    = np.sum(projection[AM_AIDSDeathsByAgeTag][sex][0:5], axis=0)
        aids_deaths[sex][GB_A5_9]    = np.sum(projection[AM_AIDSDeathsByAgeTag][sex][5:10], axis=0)
        aids_deaths[sex][GB_A10_14]  = np.sum(projection[AM_AIDSDeathsByAgeTag][sex][10:15], axis=0)
        aids_deaths[sex][GB_A15_19]  = np.sum(projection[AM_AIDSDeathsByAgeTag][sex][15:20], axis=0)
        aids_deaths[sex][GB_A20_24]  = np.sum(projection[AM_AIDSDeathsByAgeTag][sex][20:25], axis=0)
        aids_deaths[sex][GB_A25_29]  = np.sum(projection[AM_AIDSDeathsByAgeTag][sex][25:30], axis=0)
        aids_deaths[sex][GB_A30_34]  = np.sum(projection[AM_AIDSDeathsByAgeTag][sex][30:35], axis=0)
        aids_deaths[sex][GB_A35_39]  = np.sum(projection[AM_AIDSDeathsByAgeTag][sex][35:40], axis=0)
        aids_deaths[sex][GB_A40_44]  = np.sum(projection[AM_AIDSDeathsByAgeTag][sex][40:45], axis=0)
        aids_deaths[sex][GB_A45_49]  = np.sum(projection[AM_AIDSDeathsByAgeTag][sex][45:50], axis=0)
        aids_deaths[sex][GB_A50_54]  = np.sum(projection[AM_AIDSDeathsByAgeTag][sex][50:55], axis=0)
        aids_deaths[sex][GB_A55_59]  = np.sum(projection[AM_AIDSDeathsByAgeTag][sex][55:60], axis=0)
        aids_deaths[sex][GB_A60_64]  = np.sum(projection[AM_AIDSDeathsByAgeTag][sex][60:65], axis=0)
        aids_deaths[sex][GB_A65_69]  = np.sum(projection[AM_AIDSDeathsByAgeTag][sex][65:70], axis=0)
        aids_deaths[sex][GB_A70_74]  = np.sum(projection[AM_AIDSDeathsByAgeTag][sex][70:75], axis=0)
        aids_deaths[sex][GB_A75_79]  = np.sum(projection[AM_AIDSDeathsByAgeTag][sex][75:80], axis=0)
        aids_deaths[sex][GB_A80_Up]  = np.sum(projection[AM_AIDSDeathsByAgeTag][sex][80:], axis=0)

    for age in GBRange(GB_AllAges, GB_MAX_AGE):
        aids_deaths[GB_BothSexes][age] = np.sum(aids_deaths[GB_Male:GB_Female+1, age], axis=0)

    aids_deaths = aids_deaths.tolist()
    for age in GBRange(GB_AllAges, GB_MAX_AGE):
        setRowOfYearVals(sheet, aids_deaths[GB_Male][age], params, PJNZParams.currRow)
        PJNZParams.currRow += 1
 
    for age in GBRange(GB_AllAges, GB_MAX_AGE):
        setRowOfYearVals(sheet, aids_deaths[GB_Female][age], params, PJNZParams.currRow)
        PJNZParams.currRow += 1

    addEndTag(sheet, PJNZParams)
    pass


def export_AIDSDeathsART(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<AIDSDeathsART MV2>')
    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)

    PJNZParams.currRow += 1
    num_years = params.finalYear-params.firstYear+1
    art_deaths = np.zeros((GB_Female+1, GB_MAX_AGE+1, num_years))
    
    for sex in GBRange(GB_Male, GB_Female):
        art_deaths[sex][GB_AllAges] = np.sum(projection[AM_AIDSDeathsARTSingleAgeTag][sex][0:], axis=0)
        art_deaths[sex][GB_A0_4]    = np.sum(projection[AM_AIDSDeathsARTSingleAgeTag][sex][0:5], axis=0)
        art_deaths[sex][GB_A5_9]    = np.sum(projection[AM_AIDSDeathsARTSingleAgeTag][sex][5:10], axis=0)
        art_deaths[sex][GB_A10_14]  = np.sum(projection[AM_AIDSDeathsARTSingleAgeTag][sex][10:15], axis=0)
        art_deaths[sex][GB_A15_19]  = np.sum(projection[AM_AIDSDeathsARTSingleAgeTag][sex][15:20], axis=0)
        art_deaths[sex][GB_A20_24]  = np.sum(projection[AM_AIDSDeathsARTSingleAgeTag][sex][20:25], axis=0)
        art_deaths[sex][GB_A25_29]  = np.sum(projection[AM_AIDSDeathsARTSingleAgeTag][sex][25:30], axis=0)
        art_deaths[sex][GB_A30_34]  = np.sum(projection[AM_AIDSDeathsARTSingleAgeTag][sex][30:35], axis=0)
        art_deaths[sex][GB_A35_39]  = np.sum(projection[AM_AIDSDeathsARTSingleAgeTag][sex][35:40], axis=0)
        art_deaths[sex][GB_A40_44]  = np.sum(projection[AM_AIDSDeathsARTSingleAgeTag][sex][40:45], axis=0)
        art_deaths[sex][GB_A45_49]  = np.sum(projection[AM_AIDSDeathsARTSingleAgeTag][sex][45:50], axis=0)
        art_deaths[sex][GB_A50_54]  = np.sum(projection[AM_AIDSDeathsARTSingleAgeTag][sex][50:55], axis=0)
        art_deaths[sex][GB_A55_59]  = np.sum(projection[AM_AIDSDeathsARTSingleAgeTag][sex][55:60], axis=0)
        art_deaths[sex][GB_A60_64]  = np.sum(projection[AM_AIDSDeathsARTSingleAgeTag][sex][60:65], axis=0)
        art_deaths[sex][GB_A65_69]  = np.sum(projection[AM_AIDSDeathsARTSingleAgeTag][sex][65:70], axis=0)
        art_deaths[sex][GB_A70_74]  = np.sum(projection[AM_AIDSDeathsARTSingleAgeTag][sex][70:75], axis=0)
        art_deaths[sex][GB_A75_79]  = np.sum(projection[AM_AIDSDeathsARTSingleAgeTag][sex][75:80], axis=0)
        art_deaths[sex][GB_A80_Up]  = np.sum(projection[AM_AIDSDeathsARTSingleAgeTag][sex][80:], axis=0)

    for age in GBRange(GB_AllAges, GB_MAX_AGE):
        art_deaths[GB_BothSexes][age] = np.sum(art_deaths[GB_Male:GB_Female+1, age], axis=0)

    art_deaths = art_deaths.tolist()
    for age in GBRange(GB_AllAges, GB_MAX_AGE):
        setRowOfYearVals(sheet, art_deaths[GB_Male][age], params, PJNZParams.currRow)
        PJNZParams.currRow += 1
 
    for age in GBRange(GB_AllAges, GB_MAX_AGE):
        setRowOfYearVals(sheet, art_deaths[GB_Female][age], params, PJNZParams.currRow)
        PJNZParams.currRow += 1

    addEndTag(sheet, PJNZParams)
    pass


def export_AIDSDeathsARTSingleAge(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<AIDSDeathsARTSingleAge MV>')
    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)
    PJNZParams.currRow += 1

    for sex in GBRange(GB_BothSexes, GB_Female):
        for age in GBRange(0, GB_MaxSingleAges):
            setRowOfYearVals(sheet, projection[AM_AIDSDeathsARTSingleAgeTag][sex][age], params, PJNZParams.currRow)
            PJNZParams.currRow += 1
    addEndTag(sheet, PJNZParams)
    pass


def export_AIDSDeathsNoART(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<AIDSDeathsNoART MV2>')
    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)

    PJNZParams.currRow += 1
    num_years = params.finalYear-params.firstYear+1
    no_art_deaths = np.zeros((GB_Female+1, GB_MAX_AGE+1, num_years))
    
    for sex in GBRange(GB_Male, GB_Female):
        no_art_deaths[sex][GB_AllAges] = np.sum(projection[AM_AIDSDeathsNoARTSingleAgeTag][sex][0:], axis=0)
        no_art_deaths[sex][GB_A0_4]    = np.sum(projection[AM_AIDSDeathsNoARTSingleAgeTag][sex][0:5], axis=0)
        no_art_deaths[sex][GB_A5_9]    = np.sum(projection[AM_AIDSDeathsNoARTSingleAgeTag][sex][5:10], axis=0)
        no_art_deaths[sex][GB_A10_14]  = np.sum(projection[AM_AIDSDeathsNoARTSingleAgeTag][sex][10:15], axis=0)
        no_art_deaths[sex][GB_A15_19]  = np.sum(projection[AM_AIDSDeathsNoARTSingleAgeTag][sex][15:20], axis=0)
        no_art_deaths[sex][GB_A20_24]  = np.sum(projection[AM_AIDSDeathsNoARTSingleAgeTag][sex][20:25], axis=0)
        no_art_deaths[sex][GB_A25_29]  = np.sum(projection[AM_AIDSDeathsNoARTSingleAgeTag][sex][25:30], axis=0)
        no_art_deaths[sex][GB_A30_34]  = np.sum(projection[AM_AIDSDeathsNoARTSingleAgeTag][sex][30:35], axis=0)
        no_art_deaths[sex][GB_A35_39]  = np.sum(projection[AM_AIDSDeathsNoARTSingleAgeTag][sex][35:40], axis=0)
        no_art_deaths[sex][GB_A40_44]  = np.sum(projection[AM_AIDSDeathsNoARTSingleAgeTag][sex][40:45], axis=0)
        no_art_deaths[sex][GB_A45_49]  = np.sum(projection[AM_AIDSDeathsNoARTSingleAgeTag][sex][45:50], axis=0)
        no_art_deaths[sex][GB_A50_54]  = np.sum(projection[AM_AIDSDeathsNoARTSingleAgeTag][sex][50:55], axis=0)
        no_art_deaths[sex][GB_A55_59]  = np.sum(projection[AM_AIDSDeathsNoARTSingleAgeTag][sex][55:60], axis=0)
        no_art_deaths[sex][GB_A60_64]  = np.sum(projection[AM_AIDSDeathsNoARTSingleAgeTag][sex][60:65], axis=0)
        no_art_deaths[sex][GB_A65_69]  = np.sum(projection[AM_AIDSDeathsNoARTSingleAgeTag][sex][65:70], axis=0)
        no_art_deaths[sex][GB_A70_74]  = np.sum(projection[AM_AIDSDeathsNoARTSingleAgeTag][sex][70:75], axis=0)
        no_art_deaths[sex][GB_A75_79]  = np.sum(projection[AM_AIDSDeathsNoARTSingleAgeTag][sex][75:80], axis=0)
        no_art_deaths[sex][GB_A80_Up]  = np.sum(projection[AM_AIDSDeathsNoARTSingleAgeTag][sex][80:], axis=0)

    for age in GBRange(GB_AllAges, GB_MAX_AGE):
        no_art_deaths[GB_BothSexes][age] = np.sum(no_art_deaths[GB_Male:GB_Female+1, age], axis=0)

    no_art_deaths = no_art_deaths.tolist()
    for age in GBRange(GB_AllAges, GB_MAX_AGE):
        setRowOfYearVals(sheet, no_art_deaths[GB_Male][age], params, PJNZParams.currRow)
        PJNZParams.currRow += 1
 
    for age in GBRange(GB_AllAges, GB_MAX_AGE):
        setRowOfYearVals(sheet, no_art_deaths[GB_Female][age], params, PJNZParams.currRow)
        PJNZParams.currRow += 1
    addEndTag(sheet, PJNZParams)
    pass


def export_AIDSDeathsNoARTSingleAge(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<AIDSDeathsNoARTSingleAge MV>')
    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)
    PJNZParams.currRow += 1

    for sex in GBRange(GB_BothSexes, GB_Female):
        for age in GBRange(0, GB_MaxSingleAges):
            setRowOfYearVals(sheet, projection[AM_AIDSDeathsNoARTSingleAgeTag][sex][age], params, PJNZParams.currRow)
            PJNZParams.currRow += 1
    addEndTag(sheet, PJNZParams)
    pass


def export_AdultNonAIDSExcessMort(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<AdultNonAIDSExcessMort MV>')
    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)

    # result = np.zeros((DP_Data + 1, GB_Female + 1, DP_CD4_45_54 + 1, DP_CD4_LT50 + 1, DP_OnART + 1)).tolist()
    mortality = np.array(projection[AM_AdultNonAIDSExcessMortTag][DP_Data]).swapaxes(2, 3).tolist()
    for sex in GBRange(GB_Male, GB_Female):
        for d in GBRange(DP_NoTreat, DP_OnART):
            col = GB_RW_DataStartCol
            for a in GBRange(DP_CD4_15_24, DP_CD4_45_54):
                for c in GBRange(DP_CD4_GT500, DP_CD4_LT50): # will be included
                    addValueAtRowCol(sheet, PJNZParams.currRow, col, mortality[sex][a][d][c])
                    col += 1
            PJNZParams.currRow += 1
            pass
    addEndTag(sheet, PJNZParams)
    pass


def export_AidsDeathsByAge(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<AidsDeathsByAge MV2>')
    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)
    PJNZParams.currRow += 1

    for age in GBRange(0, GB_MaxSingleAges):
        setRowOfYearVals(sheet, projection[AM_AIDSDeathsNoARTSingleAgeTag][GB_Male][age], params, PJNZParams.currRow)
        PJNZParams.currRow += 1


    for age in GBRange(0, GB_MaxSingleAges):
        setRowOfYearVals(sheet, projection[AM_AIDSDeathsNoARTSingleAgeTag][GB_Female][age], params, PJNZParams.currRow)
        PJNZParams.currRow += 1


    addEndTag(sheet, PJNZParams)
    pass


def export_Births(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<Births MV>')
    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)

    setRowOfYearVals(sheet, projection[DP_BirthsTag][GB_BothSexes][GB_AllAges], params, PJNZParams.currRow)
    addEndTag(sheet, PJNZParams)
    pass


def export_ChAged14ByCD4Cat(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<ChAged14ByCD4Cat MV>')
    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)

    for sex in GBRange(GB_Male, GB_Female):
        for cd4 in GBRange(DP_CD4_Ped_GT1000, DP_CD4_Ped_LT200):
            for art in GBRange(DP_P_Perinatal, DP_GT12monthsTreat):
                setRowOfYearVals(sheet, projection[AM_ChAged14ByCD4CatTag][sex][cd4][art], params, PJNZParams.currRow)
                PJNZParams.currRow += 1
    addEndTag(sheet, PJNZParams)
    pass


def export_ChildARTCalc(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<ChildARTCalc MV2>')
    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)
    PJNZParams.currRow += 1

    addDescript(sheet, PJNZParams, 'Children needing cotrimoxazole (0-14)')
    for sex in GBRange(GB_BothSexes, GB_Female):
        setRowOfYearVals(sheet, projection[AM_ChildNeedCotrimTag][sex], params, PJNZParams.currRow)
        PJNZParams.currRow += 1
        
    addDescript(sheet, PJNZParams, 'Children receiving cotrimoxazole (0-14)')
    for sex in GBRange(GB_BothSexes, GB_Female):
        setRowOfYearVals(sheet, projection[AM_ChildOnCotrimTag][sex], params, PJNZParams.currRow)
        PJNZParams.currRow += 1

    addDescript(sheet, PJNZParams, 'Children needing ART (0-14)')
    for sex in GBRange(GB_BothSexes, GB_Female):
        child_need_art = np.sum(projection[AM_NeedARTTag][sex][0:15], axis=0).tolist()
        setRowOfYearVals(sheet, child_need_art, params, PJNZParams.currRow)
        PJNZParams.currRow += 1

    addDescript(sheet, PJNZParams, 'Children receiving ART (0-14)')
    for sex in GBRange(GB_BothSexes, GB_Female):
        child_on_art = np.sum(projection[AM_OnARTBySingleAgeTag][sex][0:15], axis=0).tolist()
        setRowOfYearVals(sheet, child_on_art, params, PJNZParams.currRow)
        PJNZParams.currRow += 1

    addEndTag(sheet, PJNZParams)
    pass


def export_ChildNeedPMTCT(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<ChildNeedPMTCT MV>')
    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)
    
    setRowOfYearVals(sheet, projection[AM_ChildNeedPMTCTTag], params, PJNZParams.currRow)
    addEndTag(sheet, PJNZParams)
    pass


def export_ChildPatsAllocToFromOtherRegion(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<ChildPatsAllocToFromOtherRegion MV>')
    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)

    setRowOfYearVals(sheet, projection[AM_ChildPatsAllocToFromOtherRegionTag], params, PJNZParams.currRow)
    addEndTag(sheet, PJNZParams)
    pass


def export_Deaths(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<Deaths MV2>')
    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)

    PJNZParams.currRow += 1
    num_years = params.finalYear-params.firstYear+1
    deaths = np.zeros((GB_Female+1, GB_MAX_AGE+1, num_years))
    
    for sex in GBRange(GB_Male, GB_Female):
        deaths[sex][GB_AllAges] = np.sum(projection[DP_DeathsByAgeTag][sex][0:], axis=0)
        deaths[sex][GB_A0_4]    = np.sum(projection[DP_DeathsByAgeTag][sex][0:5], axis=0)
        deaths[sex][GB_A5_9]    = np.sum(projection[DP_DeathsByAgeTag][sex][5:10], axis=0)
        deaths[sex][GB_A10_14]  = np.sum(projection[DP_DeathsByAgeTag][sex][10:15], axis=0)
        deaths[sex][GB_A15_19]  = np.sum(projection[DP_DeathsByAgeTag][sex][15:20], axis=0)
        deaths[sex][GB_A20_24]  = np.sum(projection[DP_DeathsByAgeTag][sex][20:25], axis=0)
        deaths[sex][GB_A25_29]  = np.sum(projection[DP_DeathsByAgeTag][sex][25:30], axis=0)
        deaths[sex][GB_A30_34]  = np.sum(projection[DP_DeathsByAgeTag][sex][30:35], axis=0)
        deaths[sex][GB_A35_39]  = np.sum(projection[DP_DeathsByAgeTag][sex][35:40], axis=0)
        deaths[sex][GB_A40_44]  = np.sum(projection[DP_DeathsByAgeTag][sex][40:45], axis=0)
        deaths[sex][GB_A45_49]  = np.sum(projection[DP_DeathsByAgeTag][sex][45:50], axis=0)
        deaths[sex][GB_A50_54]  = np.sum(projection[DP_DeathsByAgeTag][sex][50:55], axis=0)
        deaths[sex][GB_A55_59]  = np.sum(projection[DP_DeathsByAgeTag][sex][55:60], axis=0)
        deaths[sex][GB_A60_64]  = np.sum(projection[DP_DeathsByAgeTag][sex][60:65], axis=0)
        deaths[sex][GB_A65_69]  = np.sum(projection[DP_DeathsByAgeTag][sex][65:70], axis=0)
        deaths[sex][GB_A70_74]  = np.sum(projection[DP_DeathsByAgeTag][sex][70:75], axis=0)
        deaths[sex][GB_A75_79]  = np.sum(projection[DP_DeathsByAgeTag][sex][75:80], axis=0)
        deaths[sex][GB_A80_Up]  = np.sum(projection[DP_DeathsByAgeTag][sex][80:], axis=0)

    for age in GBRange(GB_AllAges, GB_MAX_AGE):
        deaths[GB_BothSexes][age] = np.sum(deaths[GB_Male:GB_Female+1, age], axis=0)

    deaths = deaths.tolist()
    for age in GBRange(GB_AllAges, GB_MAX_AGE):
        setRowOfYearVals(sheet, deaths[GB_Male][age], params, PJNZParams.currRow)
        PJNZParams.currRow += 1
 
    for age in GBRange(GB_AllAges, GB_MAX_AGE):
        setRowOfYearVals(sheet, deaths[GB_Female][age], params, PJNZParams.currRow)
        PJNZParams.currRow += 1
    addEndTag(sheet, PJNZParams)
    pass


def export_DeathsByAge(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<DeathsByAge MV2>')
    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)
    PJNZParams.currRow += 1

    for age in GBRange(0, GB_MaxSingleAges):
        setRowOfYearVals(sheet, projection[DP_DeathsByAgeTag][GB_Male][age], params, PJNZParams.currRow)
        PJNZParams.currRow += 1


    for age in GBRange(0, GB_MaxSingleAges):
        setRowOfYearVals(sheet, projection[DP_DeathsByAgeTag][GB_Female][age], params, PJNZParams.currRow)
        PJNZParams.currRow += 1

    addEndTag(sheet, PJNZParams)
    pass


def export_HIV(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<HIV MV>')
    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)
    
    num_years = params.finalYear-params.firstYear+1
    hiv = np.zeros((GB_Female+1, GB_MAX_AGE+1, num_years))
    
    for sex in GBRange(GB_Male, GB_Female):
        hiv[sex][GB_AllAges] = np.sum(projection[AM_HIVBySingleAgeTag][sex][0:], axis=0)
        hiv[sex][GB_A0_4]    = np.sum(projection[AM_HIVBySingleAgeTag][sex][0:5], axis=0)
        hiv[sex][GB_A5_9]    = np.sum(projection[AM_HIVBySingleAgeTag][sex][5:10], axis=0)
        hiv[sex][GB_A10_14]  = np.sum(projection[AM_HIVBySingleAgeTag][sex][10:15], axis=0)
        hiv[sex][GB_A15_19]  = np.sum(projection[AM_HIVBySingleAgeTag][sex][15:20], axis=0)
        hiv[sex][GB_A20_24]  = np.sum(projection[AM_HIVBySingleAgeTag][sex][20:25], axis=0)
        hiv[sex][GB_A25_29]  = np.sum(projection[AM_HIVBySingleAgeTag][sex][25:30], axis=0)
        hiv[sex][GB_A30_34]  = np.sum(projection[AM_HIVBySingleAgeTag][sex][30:35], axis=0)
        hiv[sex][GB_A35_39]  = np.sum(projection[AM_HIVBySingleAgeTag][sex][35:40], axis=0)
        hiv[sex][GB_A40_44]  = np.sum(projection[AM_HIVBySingleAgeTag][sex][40:45], axis=0)
        hiv[sex][GB_A45_49]  = np.sum(projection[AM_HIVBySingleAgeTag][sex][45:50], axis=0)
        hiv[sex][GB_A50_54]  = np.sum(projection[AM_HIVBySingleAgeTag][sex][50:55], axis=0)
        hiv[sex][GB_A55_59]  = np.sum(projection[AM_HIVBySingleAgeTag][sex][55:60], axis=0)
        hiv[sex][GB_A60_64]  = np.sum(projection[AM_HIVBySingleAgeTag][sex][60:65], axis=0)
        hiv[sex][GB_A65_69]  = np.sum(projection[AM_HIVBySingleAgeTag][sex][65:70], axis=0)
        hiv[sex][GB_A70_74]  = np.sum(projection[AM_HIVBySingleAgeTag][sex][70:75], axis=0)
        hiv[sex][GB_A75_79]  = np.sum(projection[AM_HIVBySingleAgeTag][sex][75:80], axis=0)
        hiv[sex][GB_A80_Up]  = np.sum(projection[AM_HIVBySingleAgeTag][sex][80:], axis=0)

    for age in GBRange(GB_AllAges, GB_MAX_AGE):
        hiv[GB_BothSexes][age] = np.sum(hiv[GB_Male:GB_Female+1, age], axis=0)

    hiv = hiv.tolist()
    for a in GBRange(GB_AllAges, GB_MAX_AGE):
        for s in GBRange(GB_BothSexes, GB_Female):
            # Need to write this out starting at t = 1 because there are calculations in DPCalc for the results that use
            # t-1 and it will produce a zero vValue if we haven't saved it *)
            # Note: double check that we dont need to do calcstate
            # sheet.Cells[GB_RW_NotesCol, currRow]:='age='+intToStr(a)+ '; ' +'Sex='+intToStr(s);
            addNote(sheet, PJNZParams, f'age={a}; Sex={s}')
            setRowOfYearVals(sheet, hiv[s][a], params, PJNZParams.currRow)
            PJNZParams.currRow += 1
    addEndTag(sheet, PJNZParams)
    pass


def export_HIVBySingleAge(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<HIVBySingleAge MV2>')
    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)
    PJNZParams.currRow += 1

    for sex in GBRange(GB_Male, GB_Female):
        for age in GBRange(0, GB_MaxSingleAges):
            # Need to write this out starting at t = 1 because there are calculations in DPCalc for the results that use
            # t-1 and it will produce a zero vValue if we haven't saved it *)
            # Note: double check that we dont need to do calcstate, we may ignore if projection is native projection
            # sheet.Cells[GB_RW_NotesCol, currRow]:='age='+intToStr(a)+ '; ' +'Sex='+intToStr(s);
            addNote(sheet, PJNZParams, f'Age: {age}')
            setRowOfYearVals(sheet, projection[AM_HIVBySingleAgeTag][sex][age], params, PJNZParams.currRow)
            PJNZParams.currRow += 1
    addEndTag(sheet, PJNZParams)
    pass



def export_NeedART(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<NeedART MV>')
    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)

    num_years = params.finalYear-params.firstYear+1
    need_art = np.zeros((GB_Female+1, GB_MAX_AGE+1, num_years))
    
    for sex in GBRange(GB_Male, GB_Female):
        need_art[sex][GB_AllAges] = np.sum(projection[AM_NeedARTTag][sex][0:], axis=0)
        need_art[sex][GB_A0_4]    = np.sum(projection[AM_NeedARTTag][sex][0:5], axis=0)
        need_art[sex][GB_A5_9]    = np.sum(projection[AM_NeedARTTag][sex][5:10], axis=0)
        need_art[sex][GB_A10_14]  = np.sum(projection[AM_NeedARTTag][sex][10:15], axis=0)
        need_art[sex][GB_A15_19]  = np.sum(projection[AM_NeedARTTag][sex][15:20], axis=0)
        need_art[sex][GB_A20_24]  = np.sum(projection[AM_NeedARTTag][sex][20:25], axis=0)
        need_art[sex][GB_A25_29]  = np.sum(projection[AM_NeedARTTag][sex][25:30], axis=0)
        need_art[sex][GB_A30_34]  = np.sum(projection[AM_NeedARTTag][sex][30:35], axis=0)
        need_art[sex][GB_A35_39]  = np.sum(projection[AM_NeedARTTag][sex][35:40], axis=0)
        need_art[sex][GB_A40_44]  = np.sum(projection[AM_NeedARTTag][sex][40:45], axis=0)
        need_art[sex][GB_A45_49]  = np.sum(projection[AM_NeedARTTag][sex][45:50], axis=0)
        need_art[sex][GB_A50_54]  = np.sum(projection[AM_NeedARTTag][sex][50:55], axis=0)
        need_art[sex][GB_A55_59]  = np.sum(projection[AM_NeedARTTag][sex][55:60], axis=0)
        need_art[sex][GB_A60_64]  = np.sum(projection[AM_NeedARTTag][sex][60:65], axis=0)
        need_art[sex][GB_A65_69]  = np.sum(projection[AM_NeedARTTag][sex][65:70], axis=0)
        need_art[sex][GB_A70_74]  = np.sum(projection[AM_NeedARTTag][sex][70:75], axis=0)
        need_art[sex][GB_A75_79]  = np.sum(projection[AM_NeedARTTag][sex][75:80], axis=0)
        need_art[sex][GB_A80_Up]  = np.sum(projection[AM_NeedARTTag][sex][80:], axis=0)

    for age in GBRange(GB_AllAges, GB_MAX_AGE):
        need_art[GB_BothSexes][age] = np.sum(need_art[GB_Male:GB_Female+1, age], axis=0)

    need_art = need_art.tolist()
    for a in GBRange(GB_AllAges, GB_MAX_AGE):
        for s in GBRange(GB_BothSexes, GB_Female):
            setRowOfYearVals(sheet, need_art[s][a], params, PJNZParams.currRow)
            PJNZParams.currRow += 1
    addEndTag(sheet, PJNZParams)
    pass


def export_NeedARTDec31(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<NeedARTDec31 MV>')
    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)

    num_years = params.finalYear-params.firstYear+1
    need_art = np.zeros((GB_Female+1, GB_MAX_AGE+1, num_years))
    
    for sex in GBRange(GB_Male, GB_Female):
        need_art[sex][GB_AllAges] = np.sum(projection[AM_NeedARTTag][sex][0:], axis=0)
        need_art[sex][GB_A0_4]    = np.sum(projection[AM_NeedARTTag][sex][0:5], axis=0)
        need_art[sex][GB_A5_9]    = np.sum(projection[AM_NeedARTTag][sex][5:10], axis=0)
        need_art[sex][GB_A10_14]  = np.sum(projection[AM_NeedARTTag][sex][10:15], axis=0)
        need_art[sex][GB_A15_19]  = np.sum(projection[AM_NeedARTTag][sex][15:20], axis=0)
        need_art[sex][GB_A20_24]  = np.sum(projection[AM_NeedARTTag][sex][20:25], axis=0)
        need_art[sex][GB_A25_29]  = np.sum(projection[AM_NeedARTTag][sex][25:30], axis=0)
        need_art[sex][GB_A30_34]  = np.sum(projection[AM_NeedARTTag][sex][30:35], axis=0)
        need_art[sex][GB_A35_39]  = np.sum(projection[AM_NeedARTTag][sex][35:40], axis=0)
        need_art[sex][GB_A40_44]  = np.sum(projection[AM_NeedARTTag][sex][40:45], axis=0)
        need_art[sex][GB_A45_49]  = np.sum(projection[AM_NeedARTTag][sex][45:50], axis=0)
        need_art[sex][GB_A50_54]  = np.sum(projection[AM_NeedARTTag][sex][50:55], axis=0)
        need_art[sex][GB_A55_59]  = np.sum(projection[AM_NeedARTTag][sex][55:60], axis=0)
        need_art[sex][GB_A60_64]  = np.sum(projection[AM_NeedARTTag][sex][60:65], axis=0)
        need_art[sex][GB_A65_69]  = np.sum(projection[AM_NeedARTTag][sex][65:70], axis=0)
        need_art[sex][GB_A70_74]  = np.sum(projection[AM_NeedARTTag][sex][70:75], axis=0)
        need_art[sex][GB_A75_79]  = np.sum(projection[AM_NeedARTTag][sex][75:80], axis=0)
        need_art[sex][GB_A80_Up]  = np.sum(projection[AM_NeedARTTag][sex][80:], axis=0)

    for age in GBRange(GB_AllAges, GB_MAX_AGE):
        need_art[GB_BothSexes][age] = np.sum(need_art[GB_Male:GB_Female+1, age], axis=0)

    need_art = need_art.tolist()
    for a in GBRange(GB_AllAges, GB_MAX_AGE):
        for s in GBRange(GB_BothSexes, GB_Female):
            setRowOfYearVals(sheet, need_art[s][a], params, PJNZParams.currRow)
            PJNZParams.currRow += 1
    addEndTag(sheet, PJNZParams)
    pass


def export_NewInfections(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<NewInfections MV>')
    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)

    num_years = params.finalYear-params.firstYear+1
    infections = np.zeros((GB_Female+1, GB_MAX_AGE+1, num_years))
    
    for sex in GBRange(GB_Male, GB_Female):
        infections[sex][GB_AllAges] = np.sum(projection[AM_NewInfectionsBySingleAgeTag][sex][0:], axis=0)
        infections[sex][GB_A0_4]    = np.sum(projection[AM_NewInfectionsBySingleAgeTag][sex][0:5], axis=0)
        infections[sex][GB_A5_9]    = np.sum(projection[AM_NewInfectionsBySingleAgeTag][sex][5:10], axis=0)
        infections[sex][GB_A10_14]  = np.sum(projection[AM_NewInfectionsBySingleAgeTag][sex][10:15], axis=0)
        infections[sex][GB_A15_19]  = np.sum(projection[AM_NewInfectionsBySingleAgeTag][sex][15:20], axis=0)
        infections[sex][GB_A20_24]  = np.sum(projection[AM_NewInfectionsBySingleAgeTag][sex][20:25], axis=0)
        infections[sex][GB_A25_29]  = np.sum(projection[AM_NewInfectionsBySingleAgeTag][sex][25:30], axis=0)
        infections[sex][GB_A30_34]  = np.sum(projection[AM_NewInfectionsBySingleAgeTag][sex][30:35], axis=0)
        infections[sex][GB_A35_39]  = np.sum(projection[AM_NewInfectionsBySingleAgeTag][sex][35:40], axis=0)
        infections[sex][GB_A40_44]  = np.sum(projection[AM_NewInfectionsBySingleAgeTag][sex][40:45], axis=0)
        infections[sex][GB_A45_49]  = np.sum(projection[AM_NewInfectionsBySingleAgeTag][sex][45:50], axis=0)
        infections[sex][GB_A50_54]  = np.sum(projection[AM_NewInfectionsBySingleAgeTag][sex][50:55], axis=0)
        infections[sex][GB_A55_59]  = np.sum(projection[AM_NewInfectionsBySingleAgeTag][sex][55:60], axis=0)
        infections[sex][GB_A60_64]  = np.sum(projection[AM_NewInfectionsBySingleAgeTag][sex][60:65], axis=0)
        infections[sex][GB_A65_69]  = np.sum(projection[AM_NewInfectionsBySingleAgeTag][sex][65:70], axis=0)
        infections[sex][GB_A70_74]  = np.sum(projection[AM_NewInfectionsBySingleAgeTag][sex][70:75], axis=0)
        infections[sex][GB_A75_79]  = np.sum(projection[AM_NewInfectionsBySingleAgeTag][sex][75:80], axis=0)
        infections[sex][GB_A80_Up]  = np.sum(projection[AM_NewInfectionsBySingleAgeTag][sex][80:], axis=0)

    for age in GBRange(GB_AllAges, GB_MAX_AGE):
        infections[GB_BothSexes][age] = np.sum(infections[GB_Male:GB_Female+1, age], axis=0)

    infections = infections.tolist()
    for a in GBRange(GB_AllAges, GB_MAX_AGE):
        for s in GBRange(GB_BothSexes, GB_Female):
            # Need to write this out starting at t = 1 because there are calculations in DPCalc for the results that use
            # t-1 and it will produce a zero vValue if we haven't saved it *)
            # Note: double check that we dont need to do calcstate
            # sheet.Cells[GB_RW_NotesCol, currRow]:='age='+intToStr(a)+ '; ' +'Sex='+intToStr(s);
            addNote(sheet, PJNZParams, f'age={a}; Sex={s}')
            setRowOfYearVals(sheet, infections[s][a], params, PJNZParams.currRow)
            PJNZParams.currRow += 1
    addEndTag(sheet, PJNZParams)
    pass


def export_NewInfectionsBySingleAge(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<NewInfectionsBySingleAge MV>')
    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)

    for age in GBRange(0, GB_MaxSingleAges):
        for sex in GBRange(GB_BothSexes, GB_Female):
            setRowOfYearVals(sheet, projection[AM_NewInfectionsBySingleAgeTag][sex][age], params, PJNZParams.currRow)
            PJNZParams.currRow += 1

    addEndTag(sheet, PJNZParams)
    pass


def export_NonAIDSExcessDeathsSingleAge(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<NonAIDSExcessDeathsSingleAge MV>')
    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)
    PJNZParams.currRow += 1


    for sex in GBRange(GB_BothSexes, GB_Female):
        for age in GBRange(0, GB_MaxSingleAges):
            for d in GBRange(DP_NoTreat, DP_OnART):
                setRowOfYearVals(sheet, projection[AM_NonAIDSExcessDeathsSingleAgeTag][d][sex][age], params, PJNZParams.currRow)
                PJNZParams.currRow += 1
    addEndTag(sheet, PJNZParams)
    pass


def export_OnART(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<OnART MV>')
    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)
    
    num_years = params.finalYear-params.firstYear+1
    on_art = np.zeros((GB_Female+1, GB_MAX_AGE+1, num_years))
    
    for sex in GBRange(GB_Male, GB_Female):
        on_art[sex][GB_AllAges] = np.sum(projection[AM_OnARTBySingleAgeTag][sex][0:], axis=0)
        on_art[sex][GB_A0_4]    = np.sum(projection[AM_OnARTBySingleAgeTag][sex][0:5], axis=0)
        on_art[sex][GB_A5_9]    = np.sum(projection[AM_OnARTBySingleAgeTag][sex][5:10], axis=0)
        on_art[sex][GB_A10_14]  = np.sum(projection[AM_OnARTBySingleAgeTag][sex][10:15], axis=0)
        on_art[sex][GB_A15_19]  = np.sum(projection[AM_OnARTBySingleAgeTag][sex][15:20], axis=0)
        on_art[sex][GB_A20_24]  = np.sum(projection[AM_OnARTBySingleAgeTag][sex][20:25], axis=0)
        on_art[sex][GB_A25_29]  = np.sum(projection[AM_OnARTBySingleAgeTag][sex][25:30], axis=0)
        on_art[sex][GB_A30_34]  = np.sum(projection[AM_OnARTBySingleAgeTag][sex][30:35], axis=0)
        on_art[sex][GB_A35_39]  = np.sum(projection[AM_OnARTBySingleAgeTag][sex][35:40], axis=0)
        on_art[sex][GB_A40_44]  = np.sum(projection[AM_OnARTBySingleAgeTag][sex][40:45], axis=0)
        on_art[sex][GB_A45_49]  = np.sum(projection[AM_OnARTBySingleAgeTag][sex][45:50], axis=0)
        on_art[sex][GB_A50_54]  = np.sum(projection[AM_OnARTBySingleAgeTag][sex][50:55], axis=0)
        on_art[sex][GB_A55_59]  = np.sum(projection[AM_OnARTBySingleAgeTag][sex][55:60], axis=0)
        on_art[sex][GB_A60_64]  = np.sum(projection[AM_OnARTBySingleAgeTag][sex][60:65], axis=0)
        on_art[sex][GB_A65_69]  = np.sum(projection[AM_OnARTBySingleAgeTag][sex][65:70], axis=0)
        on_art[sex][GB_A70_74]  = np.sum(projection[AM_OnARTBySingleAgeTag][sex][70:75], axis=0)
        on_art[sex][GB_A75_79]  = np.sum(projection[AM_OnARTBySingleAgeTag][sex][75:80], axis=0)
        on_art[sex][GB_A80_Up]  = np.sum(projection[AM_OnARTBySingleAgeTag][sex][80:], axis=0)

    for age in GBRange(GB_AllAges, GB_MAX_AGE):
        on_art[GB_BothSexes][age] = np.sum(on_art[GB_Male:GB_Female+1, age], axis=0)

    on_art = on_art.tolist()
    for a in GBRange(GB_AllAges, GB_MAX_AGE):
        for s in GBRange(GB_BothSexes, GB_Female):
            # Need to write this out starting at t = 1 because there are calculations in DPCalc for the results that use
            # t-1 and it will produce a zero vValue if we haven't saved it *)
            # Note: double check that we dont need to do calcstate
            # sheet.Cells[GB_RW_NotesCol, currRow]:='age='+intToStr(a)+ '; ' +'Sex='+intToStr(s);
            setRowOfYearVals(sheet, on_art[s][a], params, PJNZParams.currRow)
            PJNZParams.currRow += 1

    addEndTag(sheet, PJNZParams)
    pass


def export_OnARTBySingleAge(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<OnARTBySingleAge MV>')
    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)
    
    for age in GBRange(0, GB_MaxSingleAges):
        for sex in GBRange(GB_BothSexes, GB_Female):
            setRowOfYearVals(sheet, projection[AM_OnARTBySingleAgeTag][sex][age], params, PJNZParams.currRow)
            PJNZParams.currRow += 1
    addEndTag(sheet, PJNZParams)
    pass


def export_PerinatalTransmission(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<PerinatalTransmission MV>')
    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)

    setRowOfYearVals(sheet, projection[AM_PerinatalTransmissionTag], params, PJNZParams.currRow)
    PJNZParams.currRow += 1
    addEndTag(sheet, PJNZParams)
    pass
          
def export_ValidDate(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<ValidDate MV>')
    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)
    time_now = datetime.now()
    time_str =  f"{time_now:%m/%d/%y  %I:%M:%S %p}"
    excel_serial = (time_now - datetime(1899, 12, 30)).total_seconds() / 86400
    addValue(sheet, PJNZParams, 2, time_str)
    addValue(sheet, PJNZParams, 3, excel_serial)
    
    PJNZParams.currRow += 1
    addEndTag(sheet, PJNZParams)
    pass  

def export_ValidVersion(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<ValidVers MV>')
    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)

    addValue(sheet, PJNZParams, GB_RW_DataStartCol, '6.42')
  
    
    PJNZParams.currRow += 1
    addEndTag(sheet, PJNZParams)
    pass
def export_ValidVersion2(sheet, params, PJNZParams, projection):
    addStartTag(sheet, PJNZParams, '<VersionNum MV2>')
    PJNZParams.currRow += 2
    addValueTag(sheet, PJNZParams)

    addValue(sheet, PJNZParams, GB_RW_DataStartCol, '5.1')
  
    
    PJNZParams.currRow += 1
    addEndTag(sheet, PJNZParams)
    pass



