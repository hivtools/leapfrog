from leapfrog_mapping.GBConst import *

AMUNAIDSSummaryTemplate        = 'UNAIDSSummaryTemplate'
DPInitialConditionsDBSubDir = 'initialConditions/'

#EasyAIMData sheet names
DP_EAD_Incidence                        = 'Incidence'
DP_EAD_AdultARTMale                     = 'AdultARTMale'
DP_EAD_AdultARTFemale                   = 'AdultARTFemale'
DP_EAD_MedianCD4AtInit                  = 'MedianCD4AtInit'
DP_EAD_PercLostToFollowup               = 'PercLostToFollowup'
DP_EAD_ChildART                         = 'ChildART'
DP_EAD_ChildCotrim                      = 'ChildCotrim'
DP_EAD_PMTCTSingleDoseNevirapine        = 'PMTCTSingleDoseNevirapine'
DP_EAD_PMTCTDualARV                     = 'PMTCTDualARV'
DP_EAD_PMTCTOptA                        = 'PMTCTOptA'
DP_EAD_PMTCTOptB                        = 'PMTCTOptB'
DP_EAD_PMTCTOptBPlusStartBefPreg        = 'PMTCTOptBPlusStartBefPreg'
DP_EAD_PMTCTOptBPlusStartDurPregGT4Wks  = 'PMTCTOptBPlusStartDurPregGT4Wks'
DP_EAD_PMTCTOptBPlusStartDurPregLT4Wks  = 'PMTCTOptBPlusStartDurPregLT4Wks'
DP_EAD_PMTCTPostnatalOptA               = 'PMTCTPostnatalOptA'
DP_EAD_PMTCTPostnatalOptB               = 'PMTCTPostnatalOptB'
DP_EAD_PercentHIVPopEligible            = 'PercentHIVPopEligible'
DP_EAD_AdultHIVPrev                     = 'AdultHIVPrev'
DP_EAD_SexRatio                         = 'SexRatio'
DP_EAD_PercNotBFNotRecARVs              = 'PercNotBFNotRecARVs'
DP_EAD_PercNotBFRecARVs                 = 'PercNotBFRecARVs'
DP_EAD_LocalAdjustmentFactor            = 'LocalAdjustmentFactor'

#  District estimates tool standard indicator filename
DP_DET_StandardIndicatorsFName  = 'DistrictEstimatesStandardResults.csv'

DP_UPDFinalYear=2100

DP_ASFR_AFR      = 'ASFR_AFR'
DP_ASFR_ARB      = 'ASFR_ARB'
DP_ASFR_ASA      = 'ASFR_ASA'
DP_ASFR_AVG      = 'ASFR_AVG'
DP_LifeTable10   = 'LifeTable10'

DP_UPDCurrentVersion = 2015
DP_DHSYearsOffset    = 5

# Default constants
DP_Default  = 1
DP_Data     = 2

# # Global Constants }
DP_NOERROR           = 0
DP_ERROR             = 1
DP_ERROR_YRMATCH     = 2

# File Name consts
DP_ReadFile  = 1
DP_WriteFile = 2

# EPP constants
DP_EPP_CONCENTRATED             = 'CONCENTRATED'
DP_EPP_GENERALIZED              = 'GENERALIZED'
DP_EPP_PROJNAME	                = 'PROJNAME'
DP_EPP_COUNTRY	                = 'COUNTRY'
DP_EPP_MU	                    = 'MU'
DP_EPP_ARTSTART	                = 'ARTSTART'
DP_EPP_ARTEND	                = 'ARTEND'
DP_EPP_INFECTREDUC	            = 'INFECTREDUC'
DP_EPP_NEWINFECTSCD4_350	    = 'NEWINFECTSCD4_350'
DP_EPP_LAMBDA	                = 'LAMBDA'
DP_EPP_ALPHA1	                = 'ALPHA1'
DP_EPP_ALPHA2	                = 'ALPHA2'
DP_EPP_ALPHA3	                = 'ALPHA3'
DP_EPP_BETA1	                = 'BETA1'
DP_EPP_BETA2	                = 'BETA2'
DP_EPP_NEWINFECTSCD4            = 'NEWINFECTSCD4'
DP_EPP_NONAIDSEXCESSOFF         = 'NONAIDSEXCESSOFF'
DP_EPP_NONAIDSEXCESSART         = 'NONAIDSEXCESSART'
DP_EPP_CD4LOWLIMITS	            = 'CD4LOWLIMITS'
DP_EPP_ELIGIBILITYTHRESHOLD	    = 'ELIGIBILITYTHRESHOLD'
DP_EPP_FIRSTPROJYR	            = 'FIRSTPROJYR'
DP_EPP_LASTPROJYR	            = 'LASTPROJYR'
DP_EPP_IDUMORT	                = 'IDUMORT'
DP_EPP_AGERANGE                 = 'AGERANGE'
DP_EPP_POPSTART	                = 'POPSTART'
DP_EPP_POPEND                   = 'POPEND'
DP_EPP_MALEINCIDENCESTART	    = 'MALEINCIDENCESTART'
DP_EPP_MALEINCIDENCEEND	        = 'MALEINCIDENCEEND'
DP_EPP_FEMALEINCIDENCESTART	    = 'FEMALEINCIDENCESTART'
DP_EPP_FEMALEINCIDENCEEND	    = 'FEMALEINCIDENCEEND'
DP_EPP_SPECPOP                  = 'SPECPOP'
DP_EPP_PW                       = 'PW'
DP_EPP_TBHIV                    = 'TBHIV'
DP_EPP_DC                       = 'DC'
DP_EPP_FSW                      = 'FSW'
DP_EPP_MSM                      = 'MSM'
DP_EPP_IDU                      = 'IDU'
DP_EPP_OTHER                    = 'OTHER'
DP_EPP_ARTCOVERAGE              = 'ARTCOVERAGE'
DP_EPP_MALE_FEMALE              = 'MALE_FEMALE'
DP_EPP_CD4_PERCENT              = 'CD4_PERCENT'
DP_EPP_CD4_NUMBER               = 'CD4_NUMBER'
DP_EPP_NEW_PATIENTS             = 'NEW_PATIENTS'
DP_EPP_CD4MEDIAN_START          = 'CD4MEDIAN_START'
DP_EPP_CD4MEDIAN_END            = 'CD4MEDIAN_END'
DP_EPP_HIVPOS_15YEAROLDS        = 'HIVPOS_15YEAROLDS'
DP_EPP_HIVPOS_15YEAROLDS_END    = 'HIVPOS_15YEAROLDS_END'
DP_EPP_HIVPOS15_CD4             = 'HIVPOS15_CD4'
DP_EPP_HIVPOS15_CD4_END         = 'HIVPOS15_CD4_END'
DP_EPP_HIVPOS_15YEAROLDSART     = 'HIVPOS_15YEAROLDSART'
DP_EPP_HIVPOS_15YEAROLDSART_END = 'HIVPOS_15YEAROLDSART_END'
DP_EPP_HIVPOS15ART_CD4          = 'HIVPOS15ART_CD4'
DP_EPP_HIVPOS15ART_CD4_END      = 'HIVPOS15ART_CD4_END'
DP_EPP_HIVPOS_50YEAROLDS        = 'HIVPOS_50YEAROLDS'
DP_EPP_HIVPOS_50YEAROLDS_END    = 'HIVPOS_50YEAROLDS_END'
DP_EPP_HIVPOS_50YEAROLDSART     = 'HIVPOS_50YEAROLDSART'
DP_EPP_HIVPOS_50YEAROLDSART_END = 'HIVPOS_50YEAROLDSART_END'
DP_EPP_ARTDROPOUTRATE           = 'ARTDROPOUTRATE'
DP_EPP_ARTDROPOUTRATE_END       = 'ARTDROPOUTRATE_END'

# Population type sent to EPP
DP_EPP_15t49  = 0
DP_EPP_15Plus = 1

# QALYs: The default values of the weights used in the equations
# Adults
DP_W1 = 0.547
DP_W2 = 0.221
DP_W3 = 0.053

# Children
DP_W4 = 0.547
DP_W5 = 0.221
DP_W6 = 0.053

# Advanced Options - DALYs: constants for weights used in the equations
DP_DALY_CD4CountGE200 = 1
DP_DALY_CD4CountLT200 = 2
DP_DALY_OnART         = 3

# Advanced Options - New ART patients allocation method
DP_AdvOpt_ART_ExpMort         = 1
DP_AdvOpt_ART_PropElig        = 2
DP_AdvOpt_ART_MixedRelWeight  = 3
DP_AdvOpt_ART_LowCD4First     = 4

# DP TFR
DP_FRR_SingleYearInput = 0
DP_FRRAllYearsInput    = 1

# EP constants now in DP
DP_EP_low             = 1
DP_EP_medium          = 2
DP_EP_high            = 3
DP_EP_StartAge        = 1
DP_EP_FinalAge        = 17
DP_EP_A15_19          = 1
DP_EP_A20_24          = 2
DP_EP_A25_29          = 3
DP_EP_A30_34          = 4
DP_EP_A35_39          = 5
DP_EP_A40_44          = 6
DP_EP_A45_49          = 7
DP_LastYear           = 32


# Age constants

DP_AUnder1 = 0       #for COVID inputs,
DP_A1_4    = 1       #required >1 and 1-4's

DP_AllAges = GB_AllAges
DP_A0_4    = GB_A0_4
DP_A5_9    = GB_A5_9
DP_A10_14  = GB_A10_14
DP_A15_19  = GB_A15_19
DP_A20_24  = GB_A20_24
DP_A25_29  = GB_A25_29
DP_A30_34  = GB_A30_34
DP_A35_39  = GB_A35_39
DP_A40_44  = GB_A40_44
DP_A45_49  = GB_A45_49
DP_A50_54  = GB_A50_54
DP_A50Plus = GB_A50_54  #for CSAVR
DP_A55_59  = GB_A55_59
DP_A60_64  = GB_A60_64
DP_A65_69  = GB_A65_69
DP_A70_74  = GB_A70_74
DP_A75_Up  = GB_A75_79  #used for AgeRatioPatternIncidence
DP_A75_79  = GB_A75_79
DP_A80_Up  = GB_A80_Up
DP_MAX_AGE = GB_MAX_AGE

# ART Coverage validation constants
DP_Val_A0_14    = 18
DP_Val_A15_49   = 19
DP_Val_A50Plus  = 20

# GAM Age Groups
DP_GAMAG_A25_49  = 6
DP_GAMAG_A50Plus = 7

# Years for ART by month
DP_ART_MonthlyFYear   = 2020
DP_ART_2020           = 0
DP_ART_2021           = 1
DP_ARTMonthlyMaxYear  = DP_ART_2021

# Number on ART input type
ARTByAge5YearAG = 0
ARTByAgeGAMAG   = 1

#15-19 coefficient constants
DP_Intercept  = 0
DP_Slope      = 1

#For Goals interaction*}
DP_Pop_All      = 1
DP_Pop_H_NoART  = 2
DP_Pop_H_OnART  = 3

# Adult & Child TP - Mortality rates constants
DP_MortRates_LT12Mo = 0
DP_MortRates_GT12Mo = 1

# CD4 Age Groups *}
DP_CD4_15_24  = 1
DP_CD4_25_34  = 2
DP_CD4_35_44  = 3
DP_CD4_45_54  = 4

# CD4 Children Age Groups Progression *}
DP_CD4_0_2    = 1
DP_CD4_3_4    = 2
DP_CD4_5_14   = 3

# Child age groups for ART mortality
DP_ART_0_1    = 1
DP_ART_1_2    = 2
DP_ART_2_5    = 3
DP_ART_5_10   = 4
DP_ART_10_15  = 5
DP_ART_15_20  = 6
DP_ART_20_up  = 7

# "HIV Mortality with ART" ART treatment intervals
DP_0to6monthsTreat             = 6 # RLG: was 1, replace with DP_D_ARTlt6m
DP_7to12monthsTreat            = 7 # RLG: was 2, replace with DP_D_ART6to12m
DP_GT12monthsTreat             = 8 # RLG: was 3, replace with DP_D_ARTgt12m

# CD4 Count Categores *}
DP_CD4_GT500    = 2
DP_CD4_350_500  = 3
DP_CD4_250_349  = 4
DP_CD4_200_249  = 5
DP_CD4_100_199  = 6
DP_CD4_50_99    = 7
DP_CD4_LT50     = 8
DP_CD4_MaxCategories = 8

# CD4 Count categories for children 5-14
DP_CD4_Ped_Top     = 2
DP_CD4_Ped_GT1000  = 3
DP_CD4_Ped_750_999 = 4
DP_CD4_Ped_500_749 = 5
DP_CD4_Ped_350_499 = 6
DP_CD4_Ped_200_349 = 7
DP_CD4_Ped_LT200   = 8

# CD4 percent categories for children 0-2 and 3-4
DP_CD4_Per_GT30   = 2
DP_CD4_Per_26_30  = 3
DP_CD4_Per_21_25  = 4
DP_CD4_Per_16_20  = 5
DP_CD4_Per_11_15  = 6
DP_CD4_Per_5_10   = 7
DP_CD4_Per_LT5    = 8

# Map each single year of age to its corresponding maximum CD4 category
# DP_CD4_Start : array[0..80] of byte = (
# DP_CD4_Per_GT30, DP_CD4_Per_GT30, DP_CD4_Per_GT30, DP_CD4_Per_GT30, DP_CD4_Per_GT30, # ages 0-4
# DP_CD4_Ped_Top,  DP_CD4_Ped_Top,  DP_CD4_Ped_Top,  DP_CD4_Ped_Top,  DP_CD4_Ped_Top,  # 5-9
# DP_CD4_Ped_Top,  DP_CD4_Ped_Top,  DP_CD4_Ped_Top,  DP_CD4_Ped_Top,  DP_CD4_Ped_Top,  # 10-14
# DP_CD4_GT500,    DP_CD4_GT500,    DP_CD4_GT500,    DP_CD4_GT500,    DP_CD4_GT500,    # 15-19
# DP_CD4_GT500,    DP_CD4_GT500,    DP_CD4_GT500,    DP_CD4_GT500,    DP_CD4_GT500,    # 20-24
# DP_CD4_GT500,    DP_CD4_GT500,    DP_CD4_GT500,    DP_CD4_GT500,    DP_CD4_GT500,
# DP_CD4_GT500,    DP_CD4_GT500,    DP_CD4_GT500,    DP_CD4_GT500,    DP_CD4_GT500,    # 30-34
# DP_CD4_GT500,    DP_CD4_GT500,    DP_CD4_GT500,    DP_CD4_GT500,    DP_CD4_GT500,
# DP_CD4_GT500,    DP_CD4_GT500,    DP_CD4_GT500,    DP_CD4_GT500,    DP_CD4_GT500,    # 40-44
# DP_CD4_GT500,    DP_CD4_GT500,    DP_CD4_GT500,    DP_CD4_GT500,    DP_CD4_GT500,
# DP_CD4_GT500,    DP_CD4_GT500,    DP_CD4_GT500,    DP_CD4_GT500,    DP_CD4_GT500,    # 50-54
# DP_CD4_GT500,    DP_CD4_GT500,    DP_CD4_GT500,    DP_CD4_GT500,    DP_CD4_GT500,
# DP_CD4_GT500,    DP_CD4_GT500,    DP_CD4_GT500,    DP_CD4_GT500,    DP_CD4_GT500,    # 60-64
# DP_CD4_GT500,    DP_CD4_GT500,    DP_CD4_GT500,    DP_CD4_GT500,    DP_CD4_GT500,
# DP_CD4_GT500,    DP_CD4_GT500,    DP_CD4_GT500,    DP_CD4_GT500,    DP_CD4_GT500,    # 70-74
# DP_CD4_GT500,    DP_CD4_GT500,    DP_CD4_GT500,    DP_CD4_GT500,    DP_CD4_GT500,
# DP_CD4_GT500) # 80+

# Map each single year of age to its corresponding minimum CD4 category
# DP_CD4_Final : array[0..80] of byte = (
# DP_CD4_Per_LT5,   DP_CD4_Per_LT5,   DP_CD4_Per_LT5,   DP_CD4_Per_LT5,   DP_CD4_Per_LT5,   # ages 0-4
# DP_CD4_Ped_LT200, DP_CD4_Ped_LT200, DP_CD4_Ped_LT200, DP_CD4_Ped_LT200, DP_CD4_Ped_LT200, # 5-9
# DP_CD4_Ped_LT200, DP_CD4_Ped_LT200, DP_CD4_Ped_LT200, DP_CD4_Ped_LT200, DP_CD4_Ped_LT200, # 10-14
# DP_CD4_LT50,      DP_CD4_LT50,      DP_CD4_LT50,      DP_CD4_LT50,      DP_CD4_LT50,      # 15-19
# DP_CD4_LT50,      DP_CD4_LT50,      DP_CD4_LT50,      DP_CD4_LT50,      DP_CD4_LT50,      # 20-24
# DP_CD4_LT50,      DP_CD4_LT50,      DP_CD4_LT50,      DP_CD4_LT50,      DP_CD4_LT50,
# DP_CD4_LT50,      DP_CD4_LT50,      DP_CD4_LT50,      DP_CD4_LT50,      DP_CD4_LT50,      # 30-34
# DP_CD4_LT50,      DP_CD4_LT50,      DP_CD4_LT50,      DP_CD4_LT50,      DP_CD4_LT50,
# DP_CD4_LT50,      DP_CD4_LT50,      DP_CD4_LT50,      DP_CD4_LT50,      DP_CD4_LT50,      # 40-44
# DP_CD4_LT50,      DP_CD4_LT50,      DP_CD4_LT50,      DP_CD4_LT50,      DP_CD4_LT50,
# DP_CD4_LT50,      DP_CD4_LT50,      DP_CD4_LT50,      DP_CD4_LT50,      DP_CD4_LT50,      # 50-54
# DP_CD4_LT50,      DP_CD4_LT50,      DP_CD4_LT50,      DP_CD4_LT50,      DP_CD4_LT50,
# DP_CD4_LT50,      DP_CD4_LT50,      DP_CD4_LT50,      DP_CD4_LT50,      DP_CD4_LT50,      # 60-64
# DP_CD4_LT50,      DP_CD4_LT50,      DP_CD4_LT50,      DP_CD4_LT50,      DP_CD4_LT50,
# DP_CD4_LT50,      DP_CD4_LT50,      DP_CD4_LT50,      DP_CD4_LT50,      DP_CD4_LT50,      # 70-74
# DP_CD4_LT50,      DP_CD4_LT50,      DP_CD4_LT50,      DP_CD4_LT50,      DP_CD4_LT50,
# DP_CD4_LT50) # 80+

# Pediatric constants for CD4 model
DP_P_Perinatal = 2
DP_P_BF0       = 3
DP_P_BF7       = 4
DP_P_BF12      = 5

# HIV and ART status. These and the pediatric constants DP_P_* above are
    # used for dimension d of pop1[...,d]
DP_D_All       = 0
DP_D_HIVNeg    = 1
DP_D_HIVPos    = 2 # Used for all HIV+ persons aged 15+ who is not on ART
DP_D_ARTlt6m   = 6
DP_D_ART6to12m = 7
DP_D_ARTgt12m  = 8
DP_D_Max       = 8

# Pediatric model - mort No ART
DP_A0     = 0
DP_A1t2   = 1
DP_A3t4   = 2
DP_A5t9   = 3
DP_A10t14 = 4

# Pediatric model - mort with ART and profresion rates
DP_A0t2  = 1
# DP_A3t4  = 3 is already defined
DP_A5t14 = 3

# CD4 distribution not on ART
DP_CD4_0t4  = 1
DP_CD4_5t14 = 2

DP_OnARTAtDelivery        = 0
DP_StartingARTAtDelivery  = 1

#   (* Region string constants. Used to search the csv files for the correct region
#      data. *)
DP_AsiaStr         = 'Asia'
DP_CAfricaStr      = 'Central Africa'
DP_DevCountriesStr = 'High Income Countries'
DP_EAfricaStr      = 'East Africa'
DP_EEuropeStr      = 'Eastern Europe'
DP_LatAmerCarrStr  = 'Latin America and Caribbean'
DP_NAfrMiddEastStr = 'North Africa Middle East'
DP_SAfricaStr      = 'Southern Africa'
DP_WAfricaStr      = 'West Africa'


# Region Current IDs
DP_Asia           = 1
DP_CAfrica        = 2
DP_DevCountries   = 3
DP_EAfrica        = 4
DP_EEurope        = 5
DP_LatAmerCarr    = 6
DP_NAfrMiddEast   = 7
DP_SAfrica        = 8
DP_WAfrica        = 9
DP_Custom         = 10
DP_MaxNumRegions  = 10

DP_GlobalRegions = {
    DP_AsiaStr.lower()          : DP_Asia,
    DP_CAfricaStr.lower()       : DP_CAfrica,
    DP_DevCountriesStr.lower()  : DP_DevCountries,
    DP_EAfricaStr.lower()       : DP_EAfrica,
    DP_EEuropeStr.lower()       : DP_EEurope,
    DP_LatAmerCarrStr.lower()   : DP_LatAmerCarr,
    DP_NAfrMiddEastStr.lower()  : DP_NAfrMiddEast,
    DP_SAfricaStr.lower()       : DP_SAfrica,
    DP_WAfricaStr.lower()       : DP_WAfrica,
}

# Years for child ART distribution
DP_ChildARTDistFirstYear = 2004
DP_ChildARTDistFinalYear = 2020


DP_NonAgeRatioIncPatt = [1,2,3,17]

# CD4 Time on Treatment
#  DP_CD4_0to3 = 0
#  DP_CD4_GT3  = 1

# Data Option Constants
DP_GrowthRtDiff = 'URGD'
DP_GrowthRtDir  = 'Percent'

# HIB Prev type
DP_HetPattern      = 1
DP_IDUMSM          = 2
DP_ReadHIVPrevFile = 3
DP_EnterKeyboard   = 4

DP_NoProj     = 0

# Time constants }
DP_All                   = 0
DP_FIRST_INDEX           = 0
DP_MIN_YEAR              = 0
DP_MaxSingleAges         = 80
DP_MaxSingleAgesAdults   = 65
DP_MaxSingleAgesChildren = 14
DP_MaxAIDSYears          = 30
DP_MaxDBYear             = 2030



DP_NaomiAge00_004 = 0
DP_NaomiAge05_009 = 1
DP_NaomiAge10_014 = 2
DP_NaomiAge15_019 = 3
DP_NaomiAge20_024 = 4
DP_NaomiAge25_029 = 5
DP_NaomiAge30_034 = 6
DP_NaomiAge35_039 = 7
DP_NaomiAge40_044 = 8
DP_NaomiAge45_049 = 9
DP_NaomiAge50_054 = 10
DP_NaomiAge55_059 = 11
DP_NaomiAge60_064 = 12
DP_NaomiAge65_069 = 13
DP_NaomiAge70_074 = 14
DP_NaomiAge75_079 = 15
DP_NaomiAge80_999 = 16
DP_NaomiAge15_049 = 17
DP_NaomiFinalAgeCount = DP_NaomiAge80_999+1

DP_NaomiEstimateChoice = 'mean' #median


DP_MAX_SURVRATE  = 84

DP_ofPoint  = 0
DP_ofPeriod = 1

DPOnly     = True

DPNotAvail = -9999

# ASFR table constants }
DP_INPUTTED_TABLE  = 0
DP_cdNone          = 0
DP_MAX_ASFR_TABLES = 4

# ASFR Model Tables
DP_ASFR_UNAfrica    = 1
DP_ASFR_UNArab      = 2
DP_ASFR_UNAsia      = 3
DP_ASFR_Average     = 4
DP_ASFR_NumCols     = 7
DP_ASFR_NumRows     = 6

DP_ASFR_UNPop       = 5

ASFRTables = {
  DP_ASFR_UNAfrica : DP_ASFR_AFR,
  DP_ASFR_UNArab : DP_ASFR_ARB,
  DP_ASFR_UNAsia : DP_ASFR_ASA,
  DP_ASFR_Average : DP_ASFR_AVG,
}

DP_cdWest           = 1
DP_cdNorth          = 2
DP_cdEast           = 3
DP_cdSouth          = 4
DP_unGeneral        = 5
DP_unLatinAmerica   = 6
DP_unChile          = 7
DP_unSouthAsia      = 8
DP_unEastAsia       = 9
DP_UNPopLT          = 10
DP_CustomLT         = 11
DP_MAX_LIFE_TABLES  = 11

# for reading UPD file
DP_ReadAll                = 1
DP_ReadSrLeImrU5mr        = 2
DP_ReadASFR               = 3
DP_CallFromCommandLine    = 4
DP_ReadDefaultValuesOnly  = 5

# for setting DemProj default data
DP_SetAllDemProjDefaultData         = 1
DP_SetAllDemProjDefaultDataExceptLE = 2

# Single Age Constants
DP_A6Months    = 0 # used for weight bands
DP_A14         = 14

###     DEAD     ###
# DP_AllSingAges = 0
# DP_A1          = 2
# DP_A2          = 3
# DP_A3          = 4
# DP_A4          = 5
# DP_A5          = 6
# DP_A6          = 7
# DP_A7          = 8
# DP_A8          = 9
# DP_A9          = 10
# DP_A10         = 11
# DP_A11         = 12
# DP_A12         = 13
# DP_A13         = 14

# DP_A15         = 16
# DP_A16         = 17
# DP_A17         = 18
# DP_A18         = 19
# DP_A19         = 20
# DP_A20         = 21
# DP_A21         = 22
# DP_A22         = 23
# DP_A23         = 24
# DP_A24         = 25
# DP_A25         = 26
# DP_A26         = 27
# DP_A27         = 28
# DP_A28         = 29
# DP_A29         = 30
# DP_A30         = 31
# DP_A31         = 32
# DP_A32         = 33
# DP_A33         = 34
# DP_A34         = 35
# DP_A35         = 36
# DP_A36         = 37
# DP_A37         = 38
# DP_A38         = 39
# DP_A39         = 40
# DP_A40         = 41
# DP_A41         = 42
# DP_A42         = 43
# DP_A43         = 44
# DP_A44         = 45
# DP_A45         = 46
# DP_A46         = 47
# DP_A47         = 48
# DP_A48         = 49
# DP_A49         = 50
# DP_A50         = 51
# DP_A51         = 52
# DP_A52         = 53
# DP_A53         = 54
# DP_A54         = 55
# DP_A55         = 56
# DP_A56         = 57
# DP_A57         = 58
# DP_A58         = 59
# DP_A59         = 60
# DP_A60         = 61
# DP_A61         = 62
# DP_A62         = 63
# DP_A63         = 64
# DP_A64         = 65
# DP_A65         = 66
# DP_A66         = 67
# DP_A67         = 68
# DP_A68         = 69
# DP_A69         = 70
# DP_A70         = 71
# DP_A71         = 72
# DP_A72         = 73
# DP_A73         = 74
# DP_A74         = 75
# DP_A75         = 76
# DP_A76         = 77
# DP_A77         = 78
# DP_A78         = 79
# DP_A79         = 80
# DP_A80         = 81

# Child weight bands
DP_Kgs_3_5pt9   = 1
DP_Kgs_6_9pt9   = 2
DP_Kgs_10_13pt9 = 3
DP_Kgs_14_19pt9 = 4
DP_Kgs_20_24pt9 = 5
DP_Kgs_25_34pt9 = 6
DP_Kgs_35_Plus  = 7

# Ranges Summary Table Constants
# Quality
DP_Poor         = 0
DP_Average      = 1
DP_Good         = 2

# Trend
DP_RisingPrev   = 0
DP_StablePrev   = 1
DP_DeclinePrev  = 2

# Indicators for Range Summary
# Adult 15-49
DP_HIVPop_Adult        = 1
DP_AdultPrev_Adult     = 2
DP_NewHIVInfec_Adult   = 3
DP_AnnAIDSDeaths_Adult = 4
DP_AdultPop15_49_Adult = 5

# Child 0-14
DP_ChildHIVPop_Child   = 6
DP_ChildHIVPrev_Child  = 7
DP_NewHIVInfec_Child   = 8
DP_AnnAIDSDeath_Child  = 9

# Column for Range summary table
DP_Country = 1
DP_Low     = 2
DP_High    = 3

# Quality
DP_Quality0 = 0
DP_Quality1 = 1
DP_Quality2 = 2

# Trend
DP_Trend0 = 0
DP_Trend1 = 1
DP_Trend2 = 2

# Indicators for Sub-Population Summary
# Adult constants
DP_HIVPopTot_Ad               = 1
DP_HIVPopMale_Ad              = 2
DP_HIVPopFemale_Ad            = 3
DP_AdultPrev_Ad               = 4
DP_NewHIVInfectTot_Ad         = 5
DP_NewHIVInfectMale_Ad        = 6
DP_NewHIVInfectFemale_Ad      = 7
DP_AdultHIVInc_Ad             = 8
DP_AnnAIDSDeathTot_Ad         = 9
DP_AnnAIDSDeathMale_Ad        = 10
DP_AnnAIDSDeathFemale_Ad      = 11
DP_NumOnARTTot_Ad             = 12
DP_NumOnARTMale_Ad            = 13
DP_NumOnARTFemale_Ad          = 14
DP_NumNeedARTTot_Ad           = 15
DP_NumNeedARTMale_Ad          = 16
DP_NumNeedARTFemale_Ad        = 17
DP_AdPop15PlusTot_Ad          = 18
DP_AdPop15PlusMale_Ad         = 19
DP_AdPop15PlusFemale_Ad       = 20
# Child constants
DP_HIVPopTot_Child            = 21
DP_HIVPopMale_Child           = 22
DP_HIVPopFemale_Child         = 23
DP_NewHIVInfectTot_Child      = 24
DP_NewHIVInfectMale_Child     = 25
DP_NewHIVInfectFemale_Child   = 26
DP_AnnAIDSDeathTot_Child      = 27
DP_AnnAIDSDeathMale_Child     = 28
DP_AnnAIDSDeathFemale_Child   = 29
DP_NeedPMTCT_Child            = 30
DP_OnPMTCT_Child              = 31
DP_AdPop0_14Tot_Child         = 32
DP_AdPop0_14Male_Child        = 33
DP_AdPop0_14Female_Child      = 34
DP_MaxSubPopInd               = 34

#These constants are for the table combox box and extract to define the
# range of years to be used.  Currently current year - 5 to current year + 5

DP_Region_Table_Year_Range   = 5
DP_Region_Table_Yr_End     = 2020
DP_Region_Table_Yr_2012    = 2012

# Column IDs for Region
DP_CountryID     = 0
DP_MinEpidemic   = 1
DP_MaxEpidemic   = 500

# DHS
DP_A15_19DHS = 1
DP_A20_24DHS = 2
DP_A25_29DHS = 3
DP_A30_34DHS = 4
DP_A35_39DHS = 5
DP_A40_44DHS = 6
DP_A45_49DHS = 7
DP_A50_54DHS = 8
DP_TotalDHS  = 9

# Transmission Default IDs
DP_None_TID          = 0
DP_Nevirapine_TID    = 1
DP_NevirapineAZT_TID = 2
DP_Other_TID         = 3

DP_NoProgram_BFID        = 0
DP_SubFeeding_BFID       = 1
DP_ExclusBreastFeed_BFID = 2

# Base Transmission Default IDs
DP_LessEqual6Month  = 0
DP_7to17Month       = 1
DP_18PlusMonth      = 2

# Epidemics
DP_Generalized     = 0
DP_LowLevel        = 1
DP_Concentrated    = 2

DP_Number    = 0
DP_Percent   = 1
DP_NumAndPer = 2

# Incidence input options
DP_DirectIncidenceInputOpt  = 0
DP_EPPIncOpt                = 1
DP_AEMIncOpt                = 2
DP_FitToProgramDataOpt      = 3
DP_FitToMortalityDataOpt    = 4
DP_ECDCOpt                  = 5
DP_NosocomialInfOpt         = 6  #DO NOT REMOVE, DO NOT USE

# CSAVR Key Pops
CSAVR_Total       = 0
CSAVR_MSM         = 1
CSAVR_MIDU        = 2
CSAVR_FSW         = 3
CSAVR_FIDU        = 4
CSAVR_GenPop      = 5
CSAVR_FitToTotal  = 6

CSAVR_InputNewDiag     = 0
CSAVR_InputAIDSDeaths  = 1

# CSAVR Num Reported/Not Reported
CSAVRNumReported      = 0
CSAVRNumNotReported   = 1

CSAVRSource1 = 0
CSAVRSource2 = 1
CSAVRSource3 = 2

# CSAVR Num Reported/Not Reported
CSAVR_CD4_LT200   = 0
CSAVR_CD4_200_350 = 1
CSAVR_CD4_350_500 = 2
CSAVR_CD4_500Plus = 3
CSAVR_CD4_All     = 4

# CSAVR Population input type
DP_FitToKeyPops = 0
DP_FitToTotal   = 1

# CSAVR Diagnosis rate trends
DP_GammaCDF       = 0
DP_UserSpecified  = 1

# constants for Fitting incidence option
DP_PLHIV          = 1
DP_NewHIVCases    = 2
DP_AIDSDeaths     = 3
DP_DeathsHIVPos   = 4
DP_CD4DistAtDiag  = 4 #used only for fitting checkboxes!!!
#  DP_MeanCD4     = 4  #used only for fitting checkboxes

DP_FitNotCalculated = 0
DP_DoubleLogistic   = 1
DP_SingleLogistic   = 2
DP_Spline5Knots     = 3
DP_rLogistic        = 4
DP_Spline4Knots     = 5
DP_Spline3Knots     = 6
DP_CSAVRMaxFit      = DP_Spline3Knots

DP_CSAVR_FitSet = [
  DP_DoubleLogistic,
  DP_SingleLogistic,
  DP_Spline5Knots,
  DP_Spline4Knots,
  DP_Spline3Knots,
  DP_rLogistic
]

#  Adjust IRRs
DP_CSAVR_SexRatio   = 0
DP_CSAVR_DistOfHIV  = 1

CSAVR_TrainingRun = 0  #old CSAVR_PointEstimate
CSAVR_NationalRun = 1  #old CSAVR_Uncertainty

CSAVR_Unc_BurnIn      = 0
CSAVR_Unc_NumSamples  = 1

# WARNING BELOW ARE MASTER IDS DO NOT CHANGE
DL_Mst_Alpha            = 0
DL_Mst_Beta             = 1
DL_Mst_t0               = 2
DL_Mst_a                = 3
DL_Mst_b                = 4
DL_Mst_kappa1           = 5
DL_Mst_kappa2           = 6
DL_Mst_d0               = 7
DL_Mst_d1               = 8
DL_Mst_d2               = 9
DL_Mst_d3               = 10
DL_Mst_d4               = 11
DL_Mst_d5               = 12#Guy, new
DL_Mst_d6               = 13#Guy, new
DL_Mst_FirstYearHIVDiag = 14#Guy, Increased

# WARNING BELOW ARE MASTER IDS DO NOT CHANGE
SL_Mst_Alpha            = 0
SL_Mst_Beta             = 1
SL_Mst_d0               = 2
SL_Mst_d1               = 3
SL_Mst_d2               = 4
SL_Mst_d3               = 5
SL_Mst_d4               = 6
SL_Mst_d5               = 7
SL_Mst_d6               = 8
SL_Mst_FirstYearHIVDiag = 9

# WARNING BELOW ARE MASTER IDS DO NOT CHANGE
SOSP_Mst_p0               = 0
SOSP_Mst_p1               = 1
SOSP_Mst_p2               = 2
SOSP_Mst_p3               = 3
SOSP_Mst_p4               = 4
SOSP_Mst_p5               = 5
SOSP_Mst_p6               = 6
SOSP_Mst_p7               = 7
SOSP_Mst_p8               = 8
SOSP_Mst_p9               = 9
SOSP_Mst_p10              = 10
SOSP_Mst_d0               = 11
SOSP_Mst_d1               = 12
SOSP_Mst_d2               = 13
SOSP_Mst_d3               = 14
SOSP_Mst_d4               = 15
SOSP_Mst_d5               = 16
SOSP_Mst_d6               = 17
SOSP_Mst_FirstYearHIVDiag = 18

# WARNING BELOW ARE MASTER IDS DO NOT CHANGE
rL_Mst_a                = 0
rL_Mst_b                = 1
rL_Mst_c                = 2
rL_Mst_t0               = 3
rL_Mst_iota             = 4
rL_Mst_d0               = 5
rL_Mst_d1               = 6
rL_Mst_d2               = 7
rL_Mst_d3               = 8
rL_Mst_d4               = 9
rL_Mst_d5               = 10
rL_Mst_d6               = 11
rL_Mst_FirstYearHIVDiag = 12

# constants for Fit incidence editor
DP_PLHIV_Num              = 1
DP_PLHIV_PercUnder        = 2
DP_NewHIV_Num             = 3
DP_NewHIV_Lag             = 4
DP_AIDSDeaths_Num         = 5
DP_AIDSDeaths_PercUnder   = 6

#CSAVR DLL Path
CSAVRDLLFName             = 'eppcsavri686.dll'

# Disaggregate by age constants
DP_SingleYear = 0
DP_FiveYear   = 1

# Age ratio patterns
# DP_Generalized_Patt         = 0
# DP_Concentrated_Patt        = 1
# DP_Concentrated2_Patt       = 2
# DP_Custom_Patt              = 3

# nonFittedAgeDists           = 4

# DP_FixedIROverTime          = 4
# DP_TimeDependentIR          = 5

# DP_FittedPattern            = 6
# DP_CSAVRPattern             = 7
# DP_WebCustomPattern         = 8


# Epidemic Pattern Indices
DP_Generalized_Index = 0
DP_NonIDUConcentrated_Index = 1
DP_IDUConcentrated_Index = 2
DP_PatternFromCSAVR_Index = 3
DP_HIVPrevFixed_Index = 4
DP_HIVPrevTime_Index = 5
DP_FittedToART_Index = 6


# Sex Age Pattern Fit Type
DP_SAP_HIVPrevByAge         = 0
DP_SAP_ARTByAge             = 1

# Sex Age Pattern Prevalence Fit Model
DP_SAP_FixedIROverTime      = 0
DP_SAP_TimeDependentIR      = 1



DP_AgeRatioMinYear = 0
DP_AgeRatioMaxYear = 30

# ART
DP_AdNewNeedART = 1
DP_TotNeedART   = 2
DP_NumRecART    = 3
DP_UnmetNeedART = 4

DP_NumNeedCot = 1
DP_NumOnCot   = 2
DP_NumNeedART = 3
DP_NumOnART   = 4

DP_ChildTreatAllChildren = 0
DP_ChildTreatAgeGroups   = 1
# Child Treatment Input IDs
DP_PerChildHIVPosCot      = 1
DP_PerChildHIVRecART      = 2
DP_PerChildHIVRecART0_4   = 3
DP_PerChildHIVRecART5_9   = 4
DP_PerChildHIVRecART10_14 = 5
# DP_PerChldCotSurYr    = 3
DP_PerChldARTSurYr    = 4
DP_PerChldARTCotSurYr = 5

# Child HIV Calc IDs
DP_HIVNeg = 1
DP_HIVPos = 2

# ANC Testing Editor constants
DP_FirstANCVisits       = 0
DP_RecAtLeast1HIVTest   = 1
DP_PosOnFirstHIVTest    = 2
DP_HIVPosFirstANCVisit  = 3
DP_PercHIVPosCensus     = 4
DP_NumRetested          = 5
DP_NumPosAtRetest       = 6
DP_ProgReportedBirths   = 7
DP_HIVNegFirstANCVisit  = 8

#$REGION ' Cascade results '}
# Program Statistics - Knowledge of Status
DP_KoS_CaseReps     = 0
DP_KoS_Shiny90      = 1
DP_KoS_CSAVR        = 2
DP_KoS_ECDC         = 3
DP_KoS_DirectInput  = 4

# Shiny90 fitter constants
DP_S90_15_24  = 0
DP_S90_25_34  = 1
DP_S90_35_49  = 2
DP_S90_15_49  = 3
DP_S90_15Plus = 4

# Program Statistics - Viral Suppression
DP_VS_Clinical  = 0
DP_VS_Surveys   = 1

# Age Groups
DP_Cas_AG_Child           = 0
DP_Cas_AG_AdultMale       = 1
DP_Cas_AG_AdultFemale     = 2
DP_Cas_AG_AllAges         = 3
DP_Cas_AG_AdultBothSexes  = 4

# Indicators
DP_Cas_IND_Numbers    = 0
DP_Cas_IND_PerElig    = 1
DP_Cas_IND_PerPLHIV   = 2

# Data Type
DP_Cas_PLHIV          = 0
DP_Cas_KnowStatus     = 1
DP_Cas_OnART          = 2
DP_Cas_ViralSuppr     = 3

#Value/Low/High
DP_Cas_Value          = 0
DP_Cas_Low            = 1
DP_Cas_High           = 2

# Input Years
DP_Cas_2010           = 1
DP_Cas_StartYear      = 2010
DP_Cas_2018           = 9
DP_Cas_2019           = 10
DP_Cas_2025           = 16
DP_Cas_EndYear        = 2025

# Case reports specific constants
DP_Knowledge_CaseReps    = 0
DP_Knowledge_DeathsPLHIV = 1

# PHIA & VS Survey constants
DP_0_14  = 0
DP_15_24 = 1
DP_25_34 = 2
DP_35_44 = 3
DP_45_54 = 4
DP_55_64 = 5
DP_15_64 = 6       #PHIA
DP_VS_AllAges = 6  #VS Surveys

# DHS specific constants
DP_DHS_15_19 = 0
DP_DHS_20_24 = 1
DP_DHS_25_29 = 2
DP_DHS_30_39 = 3
DP_DHS_40_49 = 4
DP_DHS_15_49 = 5

# Clinical specific constants
DP_VS_NumOnART        = 0
DP_VS_NumTested       = 1
DP_VS_PLHIVSuppressed = 2
#$ENDREGION}


#$REGION ' PMTCT by source '}
MTCT_FirstYear            = 2017

PMTCT_NumberOfWomen       = 0
PMTCT_NewChildInfections  = 1
PMTCT_TransmissionRate    = 2
#$ENDREGION}

#link to TI structure
DP_HIVARTlt6m  = 3
DP_HIVARTgt6m  = 4
DP_HIVARTgt12m = 5

DP_TxNone = 1
DP_TxCTX  = 2
DP_TxART  = 3
DP_TxBoth = 4

# Demo Div
DP_Pop0_14   = 1
DP_Pop15_64  = 2
DP_Pop65Plus = 3

DP_H_All           = 0
DP_H_No            = 1
DP_H_Asym          = 2
DP_H_NeedTx        = 3
DP_H_OnFLArt       = 4
DP_H_NeedSL        = 5
DP_H_OnSLArt       = 6
DP_H_BF_LT6_Asym   = 7
DP_H_BF_6to12_Asym = 8
DP_H_BF_GT12_Asym  = 9
DP_H_Elig          = 10
DP_H_Max           = 8

# Effectiveness of Treatment, Child
DP_Cotrim                 = 1
DP_ChildEffNoART          = 2
DP_ChildEffWithART        = 3
DP_MaxChildTreatmentYears = 10

# DHS Set
DP_DHS1 = 1
DP_DHS2 = 2
DP_DHS3 = 3

# ART Coverage method
DP_NumOrPercent      = 0
DP_CD4Percent        = 1
DP_CD4Number         = 2
DP_NumNewARTPats     = 3
DP_PcntByRiskGrp     = 4

DP_LinIncTotNeed     = 2
DP_ConReducUnNeed    = 3
DP_HistRedUnNeed     = 4

# ARV Regimen Period
DP_PrenatalProphylaxis   = 1
DP_PostnatalProphylaxis  = 2
DP_AnnDropPostnatalProph = 3

# ARV Regimen Treatments
DP_NoProphylaxis          = 1
DP_SingleDoseNevir        = 2
DP_DualARV                = 3
DP_OptA                   = 4
DP_OptB                   = 5
DP_TripleARTBefPreg       = 6
DP_TripleARTDurPreg       = 7
DP_TripleARTDurPreg_Late  = 8
DP_TotalTreat             = 9

# Used for Drop out in PMTCT editor
DP_ART0_12MthsBF          = 6
DP_ARTGT12MthsBF          = 7

DP_NumPrenatalOptions  = 8
DP_NumPostnatalOptions = 3

# ARV Regimen treatments for PMTCT costing in RN
DP_OptA_BF            = 9
DP_OptB_BF            = 10
DP_ART_BF             = 11

# Prob MTCT Trans HIVData
DP_None            = 1
DP_SDNevir         = 2
DP_DuPrevARV       = 3
DP_OptionA1        = 4
DP_OptionB1        = 5
DP_TripTreatARV    = 6

DP_TripARVTreatment     = 1
DP_DailyNeviChild       = 2
DP_Mixed                = 3
DP_Exclusive            = 4
DP_AllOtherRegimens     = 5

# Regimen values for Transmission and efficacy assumptions for MTCT
# These constants will replace the constants under Prob MTCT Trans HIVData
DP_NoProphExistInfCD4LT200    = 1
DP_NoProphExistInfCD4200_350  = 2
DP_NoProphExistInfCD4GT350    = 3
DP_NoProphIncidentInf         = 4
DP_SingleDoseNev              = 5
DP_WHO2006DualARV             = 6
DP_OptionA                    = 7
DP_OptionB                    = 8
DP_ARTStartPrePreg            = 9
DP_ARTStartDurPreg            = 10
DP_ARTStartDurPreg_Late       = 11

# Stage values for Transmission and efficacy assumptions for MTCT
DP_Perinatal            = 1
DP_BreastfeedingLT350   = 2
DP_BreastfeedingGE350   = 3

# Distrib of HIV+ mothers by infant feeding method
DP_MixFeed_HIVMoth = 1
DP_ExBF_HIVMoth    = 2
DP_RepFeed_HIVMoth = 3
DP_Total_HIVMoth   = 4

DP_NoTreat         = 1
DP_OnART           = 2

#  DP_EID             = 3

# Populations eligible for treatment regardless of CD4 count
DP_EligTreatPregnantWomen       = 1
DP_EligTreatTB_HIV              = 2
DP_EligTreatDiscordantCouples   = 3
DP_EligTreatSexWorkers          = 4
DP_EligTreatMSM                 = 5
DP_EligTreatIDU                 = 6
DP_EligTreatOtherPop            = 7
DP_EligTreatPopsMax             = 7

DP_NotEligible  = 0
DP_Eligible     = 1

# Current Year and First Year of HIV Data, used in Future ART ed
DP_FirstYearOfData = 1996
DP_FirstYearOfART  = 1995

# Easy Proj
DPEP_CountryCode  = 1
DPEP_TFRProj      = 2
DPEP_LEproj       = 3
DPEP_CountryIndex = 4

DP_NormPattern = 1
DP_FastPattern = 2
DP_HIVtoTreat = 1
DP_TreatToDeath = 2

# HIV progression editor
DP_CD4Lt200 = 1
DP_CD4Lt250 = 2
DP_CD4Lt350 = 3

DP_ChildrenInfIntrapartum = 1
DP_ChildrenInfBreastfeeding = 2

DP_PerinatalProg        = 1
DP_PostNatal0_180Days   = 2
DP_PostNatal181_365Days = 3
DP_PostNatal365PlusDays = 4

# InfantFeedingDHSSheet
DP_InfantFeedingMths = 18
DP_NoBF = 1
DP_ExBF = 2

# Infant Feeding Optons Sheet
#  DP_InfantFeedingMths = 18
DP_NotInPMTCT = 1
DP_InPMTCT    = 2

DP_DataCurrentYear = 0
DP_DataAllYears    = 1

DP_InfantFeedMonths = 0
DP_InfantFeedMethod = 1

# Eligibility for  treatment among children
DP_AgeLT11Mths      = 0
DP_Age12to35Mths    = 1
DP_Age35to59Mths    = 2
DP_AgeGT5Years      = 3

# Plot values for ARV regimen, Adult ART and Child ART


DP_PS_ARVPageIdx                = 0
DP_PS_ANCTestingPageIdx         = 1
DP_PS_ChildTreatPageIdx         = 2
DP_PS_AdultARTPageIdx           = 3
DP_PS_KnowledgeOfStatusPageIdx  = 4
DP_PS_ViralSuppressionPageIdx   = 5

#  DP_ARVPlotValues        = 0
#  DP_AdultARTPlotValues   = 1
#  DP_ChildTreatPlotValues = 2

DP_PlotDataStartYear    = 2000  #this can be changed if in the future we want to start the plot at a different year

# Orphans Constants
DP_Total_orphans     = 0
DP_Maternal_AIDS     = 1
DP_Maternal_Non_AIDS = 2
DP_Paternal_AIDS     = 3
DP_Paternal_Non_AIDS = 4
DP_Dual_AIDS         = 5
DP_Dual_Non_AIDS     = 6
DP_Total_AIDS        = 7
DP_Total_Non_AIDS    = 8
DP_Dual_Total        = 9
DP_Maternal_Orphans  = 10
DP_Paternal_Orphans  = 11

# Dual Orphans Constants
DP_Wom15_49NeverMarried    = 1
DP_MarWomMonogamUnion      = 2

# Risk Group Constants
DP_InjectingDrugUsers      = 1
DP_MenSexWithMen           = 2
DP_SexWorkers              = 3
DP_LowerRiskGenPop         = 4

DP_PercAIDSDeaths          = 1
DP_PercMarried             = 2

# Orphans Regional Pattern
DP_SSA                     = 0
DP_OutsideSSA              = 1

DP_Total_AIDS_NonAIDS   = 1
DP_AIDS                 = 2
DP_Non_AIDS             = 3

DP_MaternalTotal     = 1
DP_PaternalTotal     = 2
DP_DualTotal         = 3
DP_TotalOrphans      = 4
DP_AllNonAIDSOrphans = 5
DP_AllAIDSOrphans    = 6

DP_MaternalAIDS_ALB        = 1
DP_MaternalNonAIDS_ALB     = 2
DP_PaternalAIDS_ALB        = 3
DP_PaternalNonAIDS_ALB     = 4
DP_DualAIDS_ALB            = 5
DP_DualNonAIDS_ALB         = 6
DP_Dual_ALB                = 7

# Orphans Constants
DP_Orphans_Maternal  = 1
DP_Orphans_Paternal  = 2
DP_Orphans_Dual      = 3

DP_Orphans_Total     = 1
DP_Orphans_AIDS      = 2   #Orphans of parents with infection  (could be born before or after infection)
DP_Orphans_NON_AIDS  = 3   #Orphans of parents with not history of infection
DP_MaxChildAge       = 17

# AIDS Impacts
DP_AIDSImpactsLatestYear = 2000

# Fit incidence parameters
#  DP_FI_Alpha = 1
#  DP_FI_Beta  = 2
#  DP_FI_t0    = 3
#  DP_FI_a     = 4
#  DP_FI_b     = 5
#  DP_FI_P0    = 6
#  DP_FI_P1    = 7
#
#  DP_FI_SOSP_P0        = 1
#  DP_FI_SOSP_P1        = 2
#  DP_FI_SOSP_P2        = 3
#  DP_FI_SOSP_P3        = 4
#  DP_FI_SOSP_P4        = 5
#  DP_FI_SOSP_P5        = 6
#  DP_FI_SOSP_P6        = 7
#  DP_FI_SOSP_P7        = 8
#  DP_FI_SOSP_P8        = 9
#  DP_FI_SOSP_P9        = 10
#  DP_FI_SOSP_P10       = 11
#  DP_FI_SOSP_P11       = 12
#  DP_FI_SOSP_P12       = 13
#  DP_FI_SOSP_P13       = 14
#  DP_FI_SOSP_P14       = 15
#  DP_FI_SOSP_P15       = 16
#  DP_FI_SOSP_P16       = 17
#  DP_FI_SOSP_P17       = 18
#  DP_FI_SOSP_P18       = 19
#  DP_FI_SOSP_P19       = 20
#  DP_FI_SOSP_P20       = 21
#  DP_FI_SOSP_P21       = 22
#  DP_FI_SOSP_P22       = 23
#  DP_FI_SOSP_P23       = 24
#  DP_FI_SOSP_P24       = 25 #Guy added this and increased DP_FI_SOSP_MinKnots and DP_FI_SOSP_MaxKnots by one }
#  DP_FI_SOSP_MinKnots  = 26
#  DP_FI_SOSP_MaxKnots  = 27


# Max number of conditions per fit incidence parameter
DP_Condition1       = 1
DP_Condition2       = 2
DP_Condition3       = 3
DP_MaxNumConditions = 3
DP_NoYear = 0

# EasyAIM Data
DP_ReadEntireEasyAIMData         = 0
DP_ReadAdultTPSectionEasyAIMData = 1
DP_ReadChildTPSectionEasyAIMData = 2
DP_ReadIncidenceEasyAIMData      = 3
DP_ReadHIVFertReducEasyAIMData   = 4

# Help Topic constants
# DemProj
DP_Help_ProjectionParameters      = 'Projection_parameters'
DP_Help_FirstYearPopulation       = 'First_year_population'
DP_Help_TotalFertilityRate        = 'Total_fertility_rate'
DP_Help_ASFR                      = 'ASFR'
DP_Help_SexRatioAtBirth           = 'Sex_ratio_at_birth'
DP_Help_LifeExpectancy            = 'Life_expectancy'
DP_Help_ModelLifeTable            = 'Model_life_table'
DP_Help_InternationalMigration    = 'International_migration'
DP_Help_RegionalAssumptions       = 'Regional_assumptions'
# AIM editors
DP_Help_WomenReceivingPMTCT       = 'Women_receiving_PMTCT_services'
DP_Help_BreastfeedingPatterns     = 'Breastfeeding_patterns'
DP_Help_Abortion                  = 'Abortion_AIM'
DP_Help_TransmissionProbability   = 'Transmission_probability'
DP_Help_AdultART                  = 'Adult_ART'
DP_Help_ChildTreatment            = 'Child_treatment'
DP_Help_KnowledgeOfStatus         = 'knowledge_of_status'
DP_Help_ViralSuppression          = 'viral_suppression'
DP_Help_EligibilityAdults         = 'Eligibility_adults'
DP_Help_EligibilityChildren       = 'Eligibility_children'
DP_Help_HIVProgAndMortNoART       = 'HIV_progression_and_mortality_without_ART'
DP_Help_HIVMortWithART            = 'HIV_mortality_with_ART'
DP_Help_TreatEffectsChildren      = 'Treatment_effects_for_children'
DP_Help_ProgramStatistics         = 'pediatric_transition_parameters'
DP_Help_ProgHIVToAIDSDeathChild   = 'Progression_from_HIV_infection_to_AIDS_death_in_children'
DP_Help_TFRReduction              = 'TFR_reduction'
DP_Help_AdultHIVIncidence         = 'Adult_HIV_incidence'
DP_Help_AgeSexDistribution        = 'Age_and_sex_distribution_of_infections'
DP_Help_Orphans                   = 'Orphans_AIM_editor'
# AIM Validation
DP_Help_PrevalenceValidation      = 'Prevalence_validation'
DP_Help_AdultMortalityValidation  = 'Adult_mortality_15_plus_validation'
DP_Help_MortalityByAgeValidation  = 'Mortality_by_age_all_ages_validation'
DP_Help_AIDSMortalityValidation   = 'AIDS_mortality_all_ages_validation'
DP_Help_AdultARTValidation        = 'Adult_ART_15_plus_validation'
DP_Help_PMTCTValidation           = 'PMTCT_validation'
DP_Help_Under5MortValidation      = 'Under_5_mortality_rate_validation'
DP_Help_ChildARTValidation        = 'Child_ART_0_14_validation'
DP_Help_PregWomenPrevValidation   = 'Pregnant-women-prevalence'

DP_Help_DistrictEstimatesTool     = 'District_estimates'
DP_Help_HIVEInputs                = 'HIVE_inputs'
DP_Help_GAM                       = 'GAM'
DP_Help_AggregateUncertainty      = 'Aggregate_uncertainty'
DP_Help_HIVRelatedFertilityReduct = 'HIV_related_fertility_reductions'

# DP Summary Tables
#  DP_DisplayDemographicData        = 0
#  DP_DisplayAIDS                   = 1
#  DP_DisplayAdultAIDS_15to49       = 2
#  DP_DisplayAdultAIDS_15to24       = 3
#  DP_DisplayAdultAIDS_15Plus       = 4
#  DP_DisplayAdoleAIDS_10to19       = 5
#  DP_DisplayChildAIDS_0to14        = 6
#  DP_DisplayChildAIDS_Under1       = 7
#  DP_DisplayChildAIDS_1to4         = 8
#  DP_DisplayPMTCT                  = 9
#  DP_DisplayAIDSRegionalOutput     = 10
#  DP_DisplayDemoDivTable           = 11
#  DP_DisplayARTDec31               = 12
#  DP_DisplayARTMidYear             = 13
#  DP_DisplayAdultAIDS_50Plus       = 14


# Scaling array constants
#  DP_IndicatorRow = 1
#  DP_FirstValuesRow = 2
#  DP_LastValuesRow = 3

# Validation constants
# Comparisons
DP_PrevValidation                   = 1
DP_AIDS45q15Validation              = 2
DP_NonAIDS45q15Validation           = 3
DP_Total45q15Validation             = 4
DP_MortalityRateByAgeValidation     = 5
DP_AllCauseMortalityValidation      = 6
DP_AIDSMortalityValidation          = 7
DP_AdultARTValidation               = 8
DP_PMTCTValidation                  = 9
DP_PMTCTProgEstNeedValidation       = 10
DP_U5MRValidation                   = 11
DP_ChildARTValidation               = 12
DP_NumOnARTValidation               = 13
DP_NumOnARTByAgeValidation          = 14
DP_PregWomenPrevValidation          = 15
DP_AdultsAndChildrenStartingART     = 16

# Surveys
DP_PrevSurvey1         = 1
DP_PrevSurvey2         = 2
DP_PrevSurvey3         = 3
DP_PrevSurvey4         = 4
DP_PrevSurvey5         = 5
DP_PrevSurvey6         = 6
DP_PrevSurvey7         = 7
DP_PrevSurvey8         = 8
DP_PrevSurveyMax       = 8
# DP_Number and DP_Percent are 0 and 1
DP_LowerBound          = 2
DP_UpperBound          = 3
DP_WeightedSampleSize  = 4        #KH for Rob's function
# AIDSDeaths all ages number
DP_Median              = 1
DP_UnderCount          = 4
# Lower age group for prevalence comparison
DP_A2_4                = 1
# Defaults
DP_DefaultSurveyYear   = 1990
DP_ThinLine            = 5

DP_GT12M                  = 3

DP_ARTStartYear = 1996
DP_AIDSStartYear = 1970

## RG 2023-10-24: for projections that start after DeathsApproxStartYear year,
## we extrapolate base year deaths from deaths in the first two years of the
## projection. We only do this for projections that start after 1980 because
## otherwise some AIM projections could have AIDS deaths a year before there
## are any HIV infections.
DP_DeathsApproxStartYear = 1980

# Exception Log constants
DP_LTZ = 'Less than 0'
DP_LTEZ = 'Less than or equal to 0'
DP_EZ = 'Equal 0'
DP_GT1 = 'Greater than 1'
DP_GTE100 = 'Greater than or equal to 100'
DP_DPAIM = 'DP/AIM'
DP_False = 'False'

# DPEdFM Glow button constants
DP_PrmBtn     = 1
DP_DemBtn     = 2
DP_ResultsBtn = 3

# UPD Source Constants
DP_UPD_Pop            = 0
DP_UPD_TFR            = 1
DP_UPD_LE             = 2
DP_UPD_AgeMortality   = 3
DP_UPD_ChildMortality = 4
DP_UPD_Migration      = 5

DP_Adult              = 1
DP_Child              = 2
DP_AdultAndChild      = 3

# for aggregate
DP_Ages15_49   = 1
DP_Ages15Plus  = 2

# Effects for AIM calcs for LiST
DP_CotrimNoARTEffect     = 0.33   #reduction in AIDS deaths among those on Cotrim but not on ART
DP_CotrimARTEffect       = 0.16   #reduction in AIDS deaths among those on both Cotrim and ART
DP_ARTEffect             = 0.63   #reduction in AIDS deaths among those on ART
DP_PMTCTEffect           = 0.88   #reduction in new infections (and  AIDS deaths) with ART before or during current pregnancy

# DPAMEdFM Glow button constants
DP_AM_EligibilityForTreatmentBtn = 1
DP_AM_ProgramStatisticsBtn       = 2
DP_AM_AdvancedOptionsBtn         = 3
DP_AM_IncidenceBtn               = 4
DP_AM_SexAgePatternBtn           = 5
DP_AM_ResultsBtn                 = 6
DP_AM_ValidationBtn              = 7
DP_AM_ChangesBtn                 = 8

#Note : Calcs Inside DP module}

DP_MLE = 0
DP_MKS = 1

# Constants for creating and reading EasyAIMData
DP_DataStartRow         = 3

DP_FileYearCol          = 0
DP_CountryCodeCol       = 0
DP_CountryNameCol       = 1
DP_SubNatRegionCodeCol  = 2
DP_SubNatRegionNameCol  = 3
DP_DataStartCol         = 4
DP_1970_2020_EndCol     = 54
DP_2000_2020_EndCol     = 24

DP_RegionCol                   = 4
DP_HasEasyAIMDataCol           = 5

#  DP_IncStartCol                 = 6
#  DP_IncEndCol                   = 56

#  DP_AdultARTMaleStartCol        = 57
#  DP_AdultARTMaleEndCol          = 77

#  DP_AdultARTFemaleStartCol      = 78
#  DP_AdultARTFemaleEndCol        = 98

#  DP_MedianCD4StartCol           = 99
#  DP_MedianCD4EndCol             = 119

#  DP_PercentLostStartCol         = 120
#  DP_PercentLostEndCol           = 140

#  DP_ChildARTStartCol            = 141
#  DP_ChildARTEndCol              = 161

#  DP_ChildCotrimStartCol         = 162
#  DP_ChildCotrimEndCol           = 182

#  DP_EarlyInfantStartCol         = 183
#  DP_EarlyInfantEndCol           = 203
DP_LocalAdjustmentFactorCol    = 543

#  DP_PMTCTSingleDoseStartCol     = 204
#  DP_PMTCTSingleDoseEndCol       = 224

#  DP_PMTCTDualARVStartCol        = 225
#  DP_PMTCTDualARVEndCol          = 245

#  DP_PMTCTOptionAStartCol        = 246
#  DP_PMTCTOptionAEndCol          = 266

#  DP_PMTCTOptionBStartCol        = 267
#  DP_PMTCTOptionBEndCol          = 287

#  DP_PMTCTARTBefPregStartCol     = 288
#  DP_PMTCTARTBefPregEndCol       = 308

#  DP_PMTCTARTDurGT4WkStartCol    = 309
#  DP_PMTCTARTDurGT4WkEndCol      = 329

#  DP_PMTCTARTDurLT4WkStartCol    = 330
#  DP_PMTCTARTDurLT4WkEndCol      = 350

#  DP_PMTCTPNOptionAStartCol      = 351
#  DP_PMTCTPNOptionAEndCol        = 371

#  DP_PMTCTPNOptionBStartCol      = 372
#  DP_PMTCTPNOptionBEndCol        = 392

#  DP_PercHIVPopEligTBCol         = 393
#  DP_PercHIVPopEligDCCol         = 395
#  DP_PercHIVPopEligFSWCol        = 397
#  DP_PercHIVPopEligMSMCol        = 399
#  DP_PercHIVPopEligIDUCol        = 401
#  DP_PercHIVPopEligOtherCol      = 403

#  DP_PrevStartCol                = 405
#  DP_PrevEndCol                  = 455

#  DP_SexRatioIncStartCol         = 456
#  DP_SexRatioIncEndCol           = 506

#  DP_PercNotBFNoARVCol           = 507

#  DP_PercNotBFARVCol             = 525

# Constants for writing GAM
DP_ISOCodeWriteCol                  = 0
DP_IndicatorWriteCol                = 1
DP_ConfigurationWriteCol            = 2
DP_Indicator_codeWriteCol           = 3
DP_Question_codeWriteCol            = 4
DP_Disaggregation_codeWriteCol      = 5
DP_PeriodWriteCol                   = 6
DP_ValueWriteCol                    = 7
DP_CommentWriteCol                  = 8
# Constants for reading GAM
DP_IndicatorReadCol                = 0
DP_ConfigurationReadCol            = 1
DP_Indicator_codeReadCol           = 2
DP_Question_codeReadCol            = 3
DP_Disaggregation_codeReadCol      = 4
DP_PeriodReadCol                   = 5
DP_SexReadCol                      = 6
DP_GAM_MstIDReadCol                = 8

# GAM tags
DP_ISOCodeTag                  = 'iso_code'
DP_IndicatorTag                = 'Indicator'
DP_ConfigurationTag            = 'Configuration'
DP_Indicator_codeTag           = 'indicator_code'
DP_Question_codeTag            = 'question_code'
DP_Disaggregation_codeTag      = 'disaggregation_code'
DP_PeriodTag                   = 'period'
DP_ValueTag                    = 'value'
DP_CommentTag                  = 'comment'

DP_CPopFirstYr                 = 0
DP_CPopFinalYr                 = 1

# Used for Knowledge of status and Viral suppression editors.
DP_2015 = 2015

DP_PerDemoDivid = 1
DP_NumDemoDivid = 2

#*****************************   DP UA   *********************************

# UA Constants

DP_Min = 1
DP_Max = 2

# General parameters for indicators in DP UA. P1 is always the year and
#    P2 is always the age group, when applicable.
DP_P1     = 1
DP_P2     = 2
DP_P3     = 3
DP_P4     = 4
DP_MaxP   = 4

# COVID-19 editors span at most these years.
DP_COVID19FirstYr = 2020
DP_COVID19FinalYr = 2024

# Key Populations

DP_KP_FSW     = 0
DP_KP_MSM     = 1
DP_KP_PWID    = 2
DP_KP_TG      = 3

DP_KP_PSE     = 0
DP_KP_HIVPrev = 1
DP_KP_ARTCov  = 2
DP_KP_NewInfs = 3


# Program Statistics - Knowledge of Status *)
DP_KoS_CaseReps     = 0
DP_KoS_Shiny90      = 1
DP_KoS_CSAVR        = 2
DP_KoS_ECDC         = 3
DP_KoS_DirectInput  = 4

# Program Statistics - Viral Suppression *)
DP_VS_Clinical  = 0
DP_VS_Surveys   = 1
# Age Groups *)
DP_Cas_AG_Child           = 0
DP_Cas_AG_AdultMale       = 1
DP_Cas_AG_AdultFemale     = 2
DP_Cas_AG_AllAges         = 3
DP_Cas_AG_AdultBothSexes  = 4
# Indicators *)
DP_Cas_IND_Numbers    = 0
DP_Cas_IND_PerElig    = 1
DP_Cas_IND_PerPLHIV   = 2
# Data Type *)
DP_Cas_PLHIV          = 0
DP_Cas_KnowStatus     = 1
DP_Cas_OnART          = 2
DP_Cas_ViralSuppr     = 3

#Value/Low/High *)
DP_Cas_Value          = 0
DP_Cas_Low            = 1
DP_Cas_High           = 2
# Input Years *)
DP_Cas_2010           = 1
DP_Cas_StartYear      = 2010
DP_Cas_2018           = 9
DP_Cas_2019           = 10
DP_Cas_2025           = 16
DP_Cas_EndYear        = 2025
DP_DetCas_KoSDiagOnTreat                        = 0
DP_DetCas_KoSDiagNeverTreat                     = 1
DP_DetCas_KoSDiagPrevOnTreat                    = 2
DP_DetCas_KoSLongStandingInfNotDiag             = 3
DP_DetCas_KoSIncidentInfNotDiag                 = 4
KoSNumSubsets                         = 5

DP_DetCas_TreatStatusNewlyInitTreat             = 0
DP_DetCas_TreatStatusOnTreat1PlusYrs            = 1
DP_DetCas_TreatStatusPrevTreated                = 2
DP_DetCas_TreatStatusDiagNoTreat                = 3
TreatStatusNumSubsets                 = 4

DP_DetCas_ViralSupprVirallySupprRoutineTest     = 0
DP_DetCas_ViralSupprAssumedSupprNoTest          = 1
DP_DetCas_ViralSupprAdjThreshToLT1000Copies     = 2
DP_DetCas_ViralSupprNotSuppressedOnTreat        = 3
ViralSupprNumSubsets                  = 4

# Case reports specific constants *)
DP_Knowledge_CaseReps    = 0
DP_Knowledge_DeathsPLHIV = 1

# PHIA & VS Survey constants *)
DP_0_14  = 0
DP_15_24 = 1
DP_25_34 = 2
DP_35_44 = 3
DP_45_54 = 4
DP_55_64 = 5
DP_15_64 = 6       #PHIA
DP_VS_AllAges = 6  #VS Surveys

# DHS specific constants *)
DP_DHS_15_19 = 0
DP_DHS_20_24 = 1
DP_DHS_25_29 = 2
DP_DHS_30_39 = 3
DP_DHS_40_49 = 4
DP_DHS_15_49 = 5

# Clinical specific constants *)
DP_VS_NumOnART        = 0
DP_VS_NumTested       = 1
DP_VS_PLHIVSuppressed = 2



MTCT_FirstYear            = 2017

PMTCT_NumberOfWomen       = 0
PMTCT_NewChildInfections  = 1
PMTCT_TransmissionRate    = 2

MTCT_Ind_NumWomen_ARVBeforePreg      = 0
MTCT_Ind_NumWomen_ARVBeforeDropout   = 1
MTCT_Ind_NumWomen_ARVDuringPreg      = 2
MTCT_Ind_NumWomen_ARVDuringDropout   = 3
MTCT_Ind_NumWomen_ARVLate            = 4
MTCT_Ind_NumWomen_NoARV              = 5
MTCT_Ind_NumWomen_IncidentPerinatal  = 6
MTCT_Ind_NumWomen_MaxInd             = MTCT_Ind_NumWomen_IncidentPerinatal

MTCT_Ind_ARVBeforePerinatal        = 0
MTCT_Ind_ARVDuringPerinatal        = 1
MTCT_Ind_ARVDuringDropoutChildInf  = 2
MTCT_Ind_ARVLatePerinatal          = 3
MTCT_Ind_NoARVPerinatal            = 4
MTCT_Ind_IncidentPerinatal         = 5
MTCT_Ind_ARVBeforeBF               = 6
MTCT_Ind_ARVDuringBF               = 7
MTCT_Ind_DroppedARTDurBF           = 8
MTCT_Ind_ARVLateBF                 = 9
MTCT_Ind_NoARVBF                   = 10
MTCT_Ind_IncidentBF                = 11
MTCT_Ind_MaxInd                    = MTCT_Ind_IncidentBF


## Uncertainty Analysis ##


DPUA_Default_Num_Iterations = 300
DPUA_ConfInterval = 95

DPUA_NumFileRuns = 1000

# Random number for seed, actually a favorite number of Karen Foreit
DPUA_RandomSeed = 173

DPUA_LowRatio            = 1
DPUA_HighRatio           = 2

DPUA_Mean   = 0
DPUA_StdDev = 1

# Number of age-specific incidence rate ratio patterns; must match UA database #
DPUA_NumDistHIVCurvesHiPrev = 200
DPUA_NumDistHIVCurvesLoPrev = 17
DPUA_NumDistHIVCurvesIDU = 3

DPUA_HIVMortARTSheets = {

    DP_Asia : 'HIVMortART_Asia',
    DP_CAfrica : 'HIVMortART_CentralAfrica',
    DP_DevCountries : 'HIVMortART_DevelopedCountries',
    DP_EAfrica : 'HIVMortART_EastAfrica',
    DP_EEurope : 'HIVMortART_DevelopedCountries',
    DP_LatAmerCarr : 'HIVMortART_LatinAmAndCaribbean',
    DP_NAfrMiddEast : 'HIVMortART_LatinAmAndCaribbean',
    DP_SAfrica : 'HIVMortART_SouthernAfrica',
    DP_WAfrica : 'HIVMortART_WestAfrica',
    # DP_Custom : 'HIVMortART_EastAfrica',
}


#  Prevention needs tool Key populations
DP_kpFSW  = 0
DP_kpMSM  = 1
DP_kpPWID  = 2
DP_kpTG = 3
DP_TKeyPopType = (DP_kpFSW, DP_kpMSM, DP_kpPWID, DP_kpTG)



DP_Condom_Sero = 0
DP_Condom_Sex_workers = 1
DP_Condom_MSM = 2
DP_Condom_YP_15_24_nr_partners = 3
DP_Condom_MW_25_34_nr_partners = 4
DP_Condom_MW_35_49_nr_partners = 5
DP_Condom_MW_50_plus_nr_partners = 6
DP_Condom_Couples_using_condoms_FP = 7
DP_Condom_Unmet_need_FP = 8
DP_Condom_PWID = 9
DP_Condom_TG = 10
#  Prevention needs tool Condoms
DP_TCondomType = (
    DP_Condom_Sero,
    DP_Condom_Sex_workers,
    DP_Condom_MSM,
    DP_Condom_YP_15_24_nr_partners,
    DP_Condom_MW_25_34_nr_partners,
    DP_Condom_MW_35_49_nr_partners,
    DP_Condom_MW_50_plus_nr_partners,
    DP_Condom_Couples_using_condoms_FP,
    DP_Condom_Unmet_need_FP,
    DP_Condom_PWID,
    DP_Condom_TG)


DP_PrEP_AGYW = 0
DP_PrEP_ABYM = 1
DP_PrEP_Female25plus = 2
DP_PrEP_Male25plus = 3
DP_PrEP_MSM = 4
DP_PrEP_FSW = 5
DP_PrEP_PWID = 6
DP_PrEP_BF = 7
DP_PrEP_TG = 8

#  Prevention needs tool PrEP
DP_TPrEPType = (
    # DP_PrEP_Sero,
    DP_PrEP_AGYW,
    DP_PrEP_ABYM,
    DP_PrEP_Female25plus,
    DP_PrEP_Male25plus,
    DP_PrEP_MSM,
    DP_PrEP_FSW,
    DP_PrEP_PWID,
    DP_PrEP_BF,
    DP_PrEP_TG)

DP_PrevNeedPrEPTypeName = {
    DP_PrEP_AGYW : 'AGYW',
    DP_PrEP_ABYM : 'ABYM',
    DP_PrEP_Female25plus : 'Females25Plus', # Female 25+
    DP_PrEP_Male25plus : 'Males25Plus', # Male 25+
    DP_PrEP_MSM : 'MSM',
    DP_PrEP_FSW : 'FSW',
    DP_PrEP_PWID : 'PWID',
    DP_PrEP_BF : 'BF',
    DP_PrEP_TG : 'TG',

}


DP_PreventionNeeds_PrEPYearLen = 6

# (* Fertility *)
DP_MinFertileAge = 15
DP_MaxFertileAge = 49
DP_NumFertileAges = 35 # DP_MaxFertileAge - DP_MinFertileAge + 1
