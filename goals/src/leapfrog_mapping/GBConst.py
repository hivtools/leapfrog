# fmt: off

# Projection file types for dialogs. *)
GB_AllPrjFiles = 1
GB_PJNZFiles = 2
GB_PJNFiles = 3
GB_ZIPFiles = 4
GB_XLSFiles = 5
GB_XLSXFiles = 6
GB_CSVFiles = 7
GB_MOFiles = 8
GB_EQFiles = 9
GB_EQQAFiles = 10
GB_GAMFiles = 1

# Modvar constants *)
MV_RW_ReadData = 1  # used when reading in a saved file normally
MV_RW_WriteData = 2  # used when saving data to file normally
MV_RW_ImportData = 3  # used when importing proj2 data into proj1
MV_RW_ExtendFinalYr = 4  # used when extending proj's final year
MV_RW_ReadLockedPrj = 5  # used for IHT modules
MV_RW_LoadDefData = 6  # used to load default values from a file
MV_RW_Comparison = 7  # used to load a comparison file that may have a
MV_InputVariable = 8
MV_ResultVariable = 9
MV_Extractable = 10
MV_General = 11
MV_DP = 12
MV_AM = 13
MV_HV = 14
MV_FP = 15
MV_DataListExtract = 16
MV_ConfigVariable = 17


GB_NativeYear = 1985
GB_BaseYear = 1970
GB_FirstPossibleYear = 1970

GB_Nan = "NAN"
GB_FloatDiff = 0.00001
GB_NOT_FOUND = -1

GB_BothSexes = 0
GB_Male = 1
GB_Female = 2
GB_NumSexes = GB_Female

GB_SexName = {
    GB_BothSexes : 'Both Sexes',
    GB_Male : 'Males',
    GB_Female : 'Females'
}

GB_January = 0
GB_February = 1
GB_March = 2
GB_April = 3
GB_May = 4
GB_June = 5
GB_July = 6
GB_August = 7
GB_September = 8
GB_October = 9
GB_November = 10
GB_December = 11

#   Inflation rate constants. Only need to hold values for local and US. Constants changed from desktop.
GB_NoInflation = 0
GB_InflationLocal = 1  # inflation for local currency
GB_InflationUS = 2  # inflation for USD
GB_NumInflationTypes = GB_InflationUS

#   Inflation method constants
GB_UseInflation = 1
GB_UseGDPDeflator = 2


#   Disability weight age groups
GB_DW_AllAges = 0
GB_DW_Age0_4 = 1
GB_DW_Age5_9 = 2
GB_DW_Age10_14 = 3
GB_DW_Age15_19 = 4
GB_DW_Age20_24 = 5
GB_DW_Age25_29 = 6
GB_DW_Age30_39 = 7
GB_DW_Age40_49 = 8
GB_DW_Age50_59 = 9
GB_DW_Age60_69 = 10
GB_DW_Age70_79 = 11
GB_DW_Age80_100 = 12
GB_DW_MaxAgeGrp = 12

# File types
GB_JSON = "JSON"

# PJNZ Read/Write col constants
GB_RW_TagCol = 0
GB_RW_DescriptCol = 1
GB_RW_NotesCol = 2
GB_RW_DataStartCol = 3

# Module codes (two-letter abbreviations) *)
GB_GBCode = "GB"
GB_DPCode = "DP"
GB_IVCode = "IV"
GB_FPCode = "FP"
GB_AMCode = "AM"
GB_RPCode = "RP"
GB_HVCode = "HV"
GB_CSCode = "CS"
GB_IHCode = "OH"
GB_HWCode = "HR"
GB_BACode = "BA"
GB_ICCode = "IC"
GB_ISCode = "IS"
GB_FSCode = "FS"
GB_PCCode = "PC"
GB_LGCode = "LG"
GB_TBCode = "TB"
GB_BGCode = "BG"
GB_HSCode = "HS"
GB_RNCode = "RN"
GB_GVCode = "GV"
GB_HFCode = "HF"
GB_NCCode = "NC"
GB_TICode = "TI"
GB_MACode = "MA"
GB_GCCode = "GC"
GB_HACode = "HA"
GB_MTCode = "MT"
GB_SICode = "SI"
GB_GTCode = "GT"
GB_PJCode = "PJ"
GB_VWCode = "VW"
GB_UACode = "UA"
GB_LCCode = "LC"
GB_TECode = "TE"


# Module ID's, do not change except for GB_MaxStdModules *)
# Module ID's are written to disk in the Projection files *)
GB_GB = 0  # {Main Shell}
GB_DP = 1
GB_IV = 2  # former GB_FC = 2     Focus (NewGen)
GB_FP = 3
GB_AM = 4
GB_RP = 5
GB_TROld = 6  # Former Training Module
GB_BCOld = 7  # Benefit Cost
GB_MTOld = 8  # MTCT
GB_LGOld = 9  # Logistics
GB_GLOld = 10  # Old Goals
GB_CROld = 11  # Condom Requirements
GB_SMOld = 12  # Safe Motherhood
GB_HV = 13
GB_ALOld = 14  # Allocate
GB_CS = 15
GB_IH = 16
GB_HW = 17
GB_BA = 18
GB_IC = 19
GB_IS = 20
GB_FS = 21
GB_PC = 22
GB_LG = 23
GB_TB = 24
GB_BG = 25
GB_HS = 26
GB_RN = 27
GB_GV = 28
GB_LOOld = 29  # Logistics optimization
GB_HF = 30
GB_NC = 31
GB_TI = 32
GB_MA = 33
GB_GC = 34
GB_HA = 35
GB_MT = 36
GB_SI = 37
GB_GT = 38
GB_PJ = 39
GB_VW = 40
GB_LF = 41
GB_MaxStdModules = 41

# Extras, pseudo modules (be sure these start at GB_MaxStdModules + 1)
GB_PseudoModuleStart = 100
GB_UA = 100
#  Even though LiST Costing is not truly a module and there is no separate
#  folder for it, treating it as a pseudo module makes certain processes
#  easier, like loading default data and creating projections with it in
#  MultiProj. TIME Econ is similar.
GB_LC = 101
GB_TE = 102
GB_NumPseudoModules = GB_TE - GB_PseudoModuleStart + 1

GB_PseudoModules = [GB_UA] #check for usage - prevents module inits from being run on projection creation

GB_MODULE_NUM_TO_MODULE_CODE = {
    0: GB_GBCode,
    1: GB_DPCode,
    2: GB_IVCode,
    3: GB_FPCode,
    4: GB_AMCode,
    5: GB_RPCode,
    13: GB_HVCode,
    15: GB_CSCode,
    16: GB_IHCode,
    17: GB_HWCode,
    18: GB_BACode,
    19: GB_ICCode,
    20: GB_ISCode,
    21: GB_FSCode,
    22: GB_PCCode,
    23: GB_LGCode,
    24: GB_TBCode,
    25: GB_BGCode,
    26: GB_HSCode,
    27: GB_RNCode,
    28: GB_GVCode,
    30: GB_HFCode,
    31: GB_NCCode,
    32: GB_TICode,
    33: GB_MACode,
    34: GB_GCCode,
    35: GB_HACode,
    36: GB_MTCode,
    37: GB_SICode,
    38: GB_GTCode,
    39: GB_PJCode,
    40: GB_VWCode,
    100: GB_UACode,
    101: GB_LCCode,
    102: GB_TECode,
}


# Modvar constants *)
MV_RW_ReadData = 1  # used when reading in a saved file normally
MV_RW_WriteData = 2  # used when saving data to file normally
MV_RW_ImportData = 3  # used when importing proj2 data into proj1
MV_RW_ExtendFinalYr = 4  # used when extending proj's final year
MV_RW_ReadLockedPrj = 5  # used for IHT modules
MV_RW_LoadDefData = 6  # used to load default values from a file
MV_RW_Comparison = 7  # used to load a comparison file that may have a
MV_InputVariable = 8
MV_ResultVariable = 9
MV_Extractable = 10
MV_General = 11
MV_DP = 12
MV_AM = 13
MV_HV = 14
MV_FP = 15
MV_DataListExtract = 16
MV_ConfigVariable = 17


GB_MOD_STR = {
    GB_GB: "GB",
    GB_DP: "DP",
    GB_IV: "IV",
    GB_FP: "FP",
    GB_AM: "AM",
    GB_RP: "RP",
    GB_HV: "HV",
    GB_CS: "CS",
    GB_IH: "OH",
    GB_HW: "HR",
    GB_BA: "BA",
    GB_IC: "IC",
    GB_IS: "IS",
    GB_FS: "FS",
    GB_PC: "PC",
    GB_LG: "LG",
    GB_TB: "TB",
    GB_BG: "BG",
    GB_HS: "HS",
    GB_RN: "RN",
    GB_GV: "GV",
    GB_HF: "HF",
    GB_NC: "NC",
    GB_TI: "TI",
    GB_MA: "MA",
    GB_GC: "GC",
    GB_HA: "HA",
    GB_MT: "MT",
    GB_SI: "SI",
    GB_GT: "GT",
    GB_PJ: "PJ",
    GB_VW: "VW",
    GB_UA: "UA",
    GB_LF: "LF",
}


GB_MOD_ID = {
    "GB": GB_GB,
    "DP": GB_DP,
    "IV": GB_IV,
    "FP": GB_FP,
    "AM": GB_AM,
    "RP": GB_RP,
    "HV": GB_HV,
    "CS": GB_CS,
    "OH": GB_IH,
    "HR": GB_HW,
    "BA": GB_BA,
    "IC": GB_IC,
    "IS": GB_IS,
    "FS": GB_FS,
    "PC": GB_PC,
    "LG": GB_LG,
    "TB": GB_TB,
    "BG": GB_BG,
    "HS": GB_HS,
    "RN": GB_RN,
    "GV": GB_GV,
    "HF": GB_HF,
    "NC": GB_NC,
    "TI": GB_TI,
    "MA": GB_MA,
    "GC": GB_GC,
    "HA": GB_HA,
    "MT": GB_MT,
    "SI": GB_SI,
    "GT": GB_GT,
    "PJ": GB_PJ,
    "UA": GB_UA,
}

GB_EXISTING_MOD_ID = {
    "GB": GB_GB,
    "PJ": GB_PJ,
    "DP": GB_DP,
    "AM": GB_AM,
    "FP": GB_FP,
    "TB": GB_TB,
    "CS": GB_CS,
    "OH": GB_IH,
    "IC": GB_IC,
    "PC": GB_PC,
    "HR": GB_HW,
    "IS": GB_IS,
    "HS": GB_HS,
    "FS": GB_FS,
    "BG": GB_BG,
    "UA": GB_UA,
    "RP": GB_RP,
    "GV": GB_GV,
    "HF": GB_HF,
    "LG": GB_LG,
    "HV": GB_HV,
    "RN": GB_RN,
}

GB_PSEUDO_MOD_ID = {
    "UA": GB_UA,
}

GB_NativeYear = 1970
GB_FirstPossibleYear = 1970

# Environment variables
GB_SPECT_MOD_DATA_CONN_ENV = "AVENIR_SW_DEFAULT_DATA_CONNECTION"

# Partial paths for DefaultData repo
GB_DEFAULT_DATA_SOURCE_DATA_PATH = r'DefaultData\SourceData'
GB_DEFAULT_DATA_JSON_DATA_PATH   = r'DefaultData\JSONData'
GB_DEFAULT_DATA_SCRIPTS_PATH     = r'DefaultData\Scripts'

# Container names
GB_GB_CONTAINER      = 'globals'
GB_IH_CORE_CONTAINER = 'ohtcore'
GB_IC_CONTAINER      = 'interventioncosting'
GB_IV_CONTAINER      = 'interventions'
GB_IS_CONTAINER      = 'infrastructure'
GB_LG_CONTAINER      = 'supplychain'
GB_HW_CONTAINER      = 'humanresources'
GB_CS_CONTAINER      = 'list'
GB_PC_CONTAINER      = 'programmecosting'
GB_BG_CONTAINER      = 'budgetmapping'
GB_TI_CONTAINER      = 'tuberculosis'
GB_RP_CONTAINER      = 'rapid'

GB_CONTAINERS = {
    GB_GB : GB_GB_CONTAINER,
    GB_IH : GB_IH_CORE_CONTAINER,
    GB_IC : GB_IC_CONTAINER,
    GB_IV : GB_IV_CONTAINER,
    GB_IS : GB_IS_CONTAINER,
    GB_HW : GB_HW_CONTAINER,
    GB_CS : GB_CS_CONTAINER,
    GB_PC : GB_PC_CONTAINER,
    GB_BG : GB_BG_CONTAINER,
    GB_TI : GB_TI_CONTAINER,
    GB_RP : GB_RP_CONTAINER,
    GB_LG : GB_LG_CONTAINER
}

# "extra" fields (passed into "extra" object when creating projections)
GB_IHT_ON                 = 'IHTCostingOn'
GB_TB_COSTING_ON          = 'TBCostingOn'
GB_LIST_COSTING_ON        = 'LiSTCostingOn'
GB_GSKMode                = 'GSKMode'
GB_MODULES                = 'modules'
# GB_RAPID_SECTORS_ON       = 'RAPIDSectorsOn'
GB_TB_ImpactStatistical   = 'TBImpactStatistical'
GB_TB_ImpactDynamical     = 'TBImpactDynamical'
GB_Extra_SubnatCode       = 'subNatCode'
GB_Extra_subnatName       = 'subNatName'
GB_Extra_projection_title = 'fileName'
GB_Extra_modules          = 'modules'
GB_Extra_Author           = 'author'
GB_Extra_organization     = 'organization'
GB_Extra_notes            = 'notes'
GB_Extra_appID            = 'appID'
GB_Extra_plantype         = 'planType'
GB_Extra_readonly         = 'readOnly'
GB_Extra_TBSubnatRegion   = 'TBSubnatRegion'
GB_Extra_epidemicStartYr  = 'epidemicStartYr'
GB_Extra_UseLeapfrog      = 'useLeapfrog'

# Treat as master IDs.
GB_NO_COSTING_MODE   = 0
GB_IHT_COSTING_MODE  = 1
GB_TB_COSTING_MODE   = 2
GB_LIST_COSTING_MODE = 3
GB_NUM_COSTING_MODES = GB_LIST_COSTING_MODE

# the first established subnational region code for any country will always be
# 10. Any subnational region code less than 10 will mean it is a custom region.
# if the subnational region code is 0, then it is the entire country
GB_FirstSubNatRegionCode       = 10
GB_EntireCountry               = 0
GB_CustomSubnatRegion          = 1

GB_PERCENT = 1
GB_NUMBER  = 2

GB_DYNAMIC = 1
GB_STATIC  = 2

# Single age constants
GB_MaxSingleAges         = 80

# 5-year age groups
GB_AllAges = 0
GB_A0_4    = 1
GB_A5_9    = 2
GB_A10_14  = 3
GB_A15_19  = 4
GB_A20_24  = 5
GB_A25_29  = 6
GB_A30_34  = 7
GB_A35_39  = 8
GB_A40_44  = 9
GB_A45_49  = 10
GB_A50_54  = 11
GB_A55_59  = 12
GB_A60_64  = 13
GB_A65_69  = 14
GB_A70_74  = 15
GB_A75_79  = 16
GB_A80_Up  = 17
GB_MAX_AGE = 17

# Interpolation types
GB_LINEAR          = 1
GB_S_SHAPED        = 2
GB_EXPONENTIAL     = 3
GB_FRONT_LOADED    = 4
GB_AgeCatStr = {

    GB_AllAges : 'AllAges',
    GB_A0_4    : 'Age 0-4',
    GB_A5_9    : 'Age 5-9',
    GB_A10_14  : 'Age 10-14',
    GB_A15_19  : 'Age 15-19',
    GB_A20_24  : 'Age 20-24',
    GB_A25_29  : 'Age 25-29',
    GB_A30_34  : 'Age 30-34',
    GB_A35_39  : 'Age 35-39',
    GB_A40_44  : 'Age 40-44',
    GB_A45_49  : 'Age 45-49',
    GB_A50_54  : 'Age 50-54',
    GB_A55_59  : 'Age 55-59',
    GB_A60_64  : 'Age 60-64',
    GB_A65_69  : 'Age 65-69',
    GB_A70_74  : 'Age 70-74',
    GB_A75_79  : 'Age 75-79',
    GB_A80_Up  : 'Age 80-Up',
}

# appIDs
GB_DP_Client      = 'DemProj'
GB_AIM_Client     = 'AIM'
GB_LiST_Client    = 'LiST'
GB_FamPlan_Client = 'FamPlan'
GB_Rapid_Client   = 'RAPID'
GB_IHT_Client     = 'IHT'
GB_TB_Client      = 'TB'
GB_Status_Client  = 'SWStatus'

GB_DP_Client_lc      = GB_DP_Client.lower()
GB_AIM_Client_lc     = GB_AIM_Client.lower()
GB_LiST_Client_lc    = GB_LiST_Client .lower()
GB_FamPlan_Client_lc = GB_FamPlan_Client.lower()
GB_Rapid_Client_lc   = GB_Rapid_Client.lower()
GB_IHT_Client_lc     = GB_IHT_Client .lower()
GB_TB_Client_lc      = GB_TB_Client.lower()
GB_Status_Client_lc  = GB_Status_Client.lower()

GB_AppList = [GB_DP_Client,
              GB_AIM_Client,
              GB_LiST_Client,
              GB_FamPlan_Client,
              GB_Rapid_Client,
              GB_IHT_Client,
              GB_TB_Client,
              GB_Status_Client]

gb_shape_module = {
    GB_DPCode : 'demproj',
    GB_AMCode : 'aim',
    GB_FPCode : 'famplan',
    GB_TBCode : 'tuberculosis',
}

GB_RestrictSaveProjList=[GB_LiST_Client, GB_TB_Client, GB_AIM_Client, GB_FamPlan_Client] # currently used to restrict saving

GB_AppLowerCaseList = [app.lower() for app in GB_AppList]

GB_SW_BETANOTALLOWED  = 'SW_BETANOTALLOWED'
GB_SW_NOTLOGGEDIN     = 'SW_NOTLOGGEDIN'
GB_SW_UNKNOWN         = 'SW_UNKNOWN'
GB_SW_GENERAL         = 'SW_GENERAL'
GB_SW_DOESNOTEXIST    = 'SW_DOESNOTEXIST'
GB_SW_INVALIDREQUEST  = 'SW_INVALIDREQUEST'
GB_SW_OLDERROR        = 'SW_OLDERROR'
GB_SW_REQUSUPERDET    = 'SW_REQUSUPERDET'
GB_SW_BADMODVARJSON   = 'SW_BADMODVARJSON'
GB_SW_FILTERFAILED    = 'SW_FILTERFAILED'
GB_SW_BADPROJPARAM    = 'SW_BADPROJPARAM'
GB_SW_BADGETMODVARS   = 'SW_BADGETMODVARS'
GB_SW_BADSETMODVARS   = 'SW_BADSETMODVARS'
GB_SW_BADCALCULATE    = 'SW_FAILEDCALCULATE'
GB_SW_BADEPPCALL      = 'SW_BADEPPCALL'
GB_SW_JWTEXPIRED      = 'SW_JWTEXPIRED'
GB_SW_JWTDECODEFAILED = 'SW_JWTDECODEFAILED'
GB_SW_THIRDPARTYFAILED = 'SW_THIRDPARTYFAILED'
GB_SW_NOPERMISSION     = 'SW_NOPERMISSION'
GB_SW_BUSY             = 'SW_BUSY'
GB_SW_MISSINGPROJECTION = 'SW_MISSINGPROJECTION'
GB_SW_PROJECTIONFILEMISSING = 'SW_PROJECTIONFILEMISSING'
GB_SW_PJNZIMPORTFAILED = "SW_PJNZIMPORTFAILED"
GB_SW_JSONIMPORTFAILED = "SW_JSONIMPORTFAILED"
GB_SW_PROJECTIONOUTOFDATE = 'SW_PROJECTIONOUTOFDATE'
GB_SW_PROJECTIONDELETED = 'SW_PROJECTIONOUTOFDATE'
GB_SW_PROJECTIONTOOMANY = 'SW_PROJECTIONTOOMANY'

GB_SW_ExceptMessages = {
    GB_SW_BETANOTALLOWED  : 'Operation not allowed in beta.',
    GB_SW_NOTLOGGEDIN     : 'Not logged in.',
    GB_SW_UNKNOWN         : 'Unknown error.',
    GB_SW_GENERAL         : 'General error.',
    GB_SW_INVALIDREQUEST  : 'Invalid request.',
    GB_SW_OLDERROR        : 'Old error exception.',
    GB_SW_BADMODVARJSON   : 'Failed to convert modvar to json.',
    GB_SW_DOESNOTEXIST    : 'The API call or link does not exist',
    GB_SW_REQUSUPERDET    : 'Requires admin priveleges',
    GB_SW_FILTERFAILED    : 'Filter failed.',
    GB_SW_BADPROJPARAM    : 'Bad projection parameters',
    GB_SW_BADCALCULATE    : 'Failed to calculate',
    GB_SW_BADGETMODVARS   : 'Failed to get modvars',
    GB_SW_BADSETMODVARS   : 'Failed to set modvars',
    GB_SW_BADEPPCALL      : 'Failed to make EPP call',
    GB_SW_JWTEXPIRED      : 'Login has expired, please login again.',
    GB_SW_JWTDECODEFAILED : 'Login failed, please try login again.',
    GB_SW_THIRDPARTYFAILED: 'Authorization failed. Please contact support.',
    GB_SW_NOPERMISSION    : 'You do not have permission to perform this action.',
    GB_SW_BUSY            : 'The server is currently busy. Please try again later.',
    GB_SW_MISSINGPROJECTION: 'Failed to locate projection.',
    GB_SW_PROJECTIONFILEMISSING: 'File missing from projection.',
    GB_SW_PJNZIMPORTFAILED: "Failed to import PJNZ.",
    GB_SW_JSONIMPORTFAILED: "Failed to import JSON.",
    GB_SW_PROJECTIONOUTOFDATE: "Failed to update projection. Someone else has updated this projection since you last opened it.",
    GB_SW_PROJECTIONDELETED: "Failed to update projection. Someone else has deleted since you last opened it.",
    GB_SW_PROJECTIONTOOMANY: "Failed to save projection, you have too many projections."
}
GB_SW_StatusCode = {
    GB_SW_BETANOTALLOWED  : 401,
    GB_SW_NOTLOGGEDIN     : 401,
    GB_SW_INVALIDREQUEST  : 422,
    GB_SW_UNKNOWN         : 500,
    GB_SW_GENERAL         : 500,
    GB_SW_OLDERROR        : 500,
    GB_SW_BADMODVARJSON   : 500,
    GB_SW_DOESNOTEXIST    : 404,
    GB_SW_REQUSUPERDET    : 401,
    GB_SW_FILTERFAILED    : 500,
    GB_SW_BADPROJPARAM    : 422,
    GB_SW_BADCALCULATE    : 500,
    GB_SW_BADGETMODVARS   : 500,
    GB_SW_BADSETMODVARS   : 500,
    GB_SW_BADEPPCALL      : 500,
    GB_SW_JWTEXPIRED      : 401,
    GB_SW_JWTDECODEFAILED : 401,
    GB_SW_THIRDPARTYFAILED: 401,
    GB_SW_NOPERMISSION    : 403,
    GB_SW_BUSY            : 429,
    GB_SW_MISSINGPROJECTION: 400,
    GB_SW_PROJECTIONFILEMISSING: 500,
    GB_SW_PJNZIMPORTFAILED: 400,
    GB_SW_JSONIMPORTFAILED: 400,
    GB_SW_PROJECTIONOUTOFDATE: 412,
    GB_SW_PROJECTIONDELETED: 412,
    GB_SW_PROJECTIONTOOMANY: 400,
}

# Languages
GB_ENGLISH_MST_ID    = 1
GB_FRENCH_MST_ID     = 2
GB_ARABIC_MST_ID     = 3
GB_SPANISH_MST_ID    = 4
GB_RUSSIAN_MST_ID    = 5
GB_PORTUGUESE_MST_ID = 6
GB_CHINESE_MST_ID    = 7
GB_INDONESIAN_MST_ID = 8
GB_UKRANIAN_MST_ID   = 9

GB_LANGUAGES = [
    GB_ENGLISH_MST_ID, GB_FRENCH_MST_ID, GB_ARABIC_MST_ID,
    GB_SPANISH_MST_ID, GB_RUSSIAN_MST_ID, GB_PORTUGUESE_MST_ID,
    GB_CHINESE_MST_ID, GB_INDONESIAN_MST_ID, GB_UKRANIAN_MST_ID
]

GB_STRING_DB_CURR_VERSION = 'V1'

GB_ENGLISH_STRINGS_DB_NAME = 'en'
GB_FRENCH_STRINGS_DB_NAME = 'fr'
GB_ARABIC_STRINGS_DB_NAME = ''
GB_SPANISH_STRINGS_DB_NAME = 'es'
GB_RUSSIAN_STRINGS_DB_NAME = 'ru'
GB_PORTUGUESE_STRINGS_DB_NAME = ''
GB_CHINESE_STRINGS_DB_NAME = ''
GB_INDONESIAN_STRINGS_DB_NAME = ''
GB_UKRANIAN_STRINGS_DB_NAME = 'uk'

#Permission constants
GB_AllowBetaSave = "allowBetaSave"
GB_AllowGSK = "allowGSK"
GB_AllowSWQA = "allowSWQA"
# GB_AllowEQUIST = "allowEQUIST"
