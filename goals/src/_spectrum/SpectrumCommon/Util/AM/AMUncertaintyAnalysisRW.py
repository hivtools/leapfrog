from io import BytesIO

from src._spectrum.AvenirCommon.Util import GBRange, getTagRow, gb_read_csv_sheet

from SpectrumCommon.Const.PJ import *
from SpectrumCommon.Util.DP.DPUtil import getUALowHighRatiosRec
from SpectrumCommon.Const.DP.DPConst import *
from SpectrumCommon.Const.DP.DPTags import DP_UALowHighRatiosTag, DP_AIDSDeathsFYearUATag, DP_UAHasRanTag, DP_UAInfoTag
from SpectrumCommon.Modvars.DP.DPModvarDef import UALowHighRatios_Init, AIDSDeathsFYearUA_Init, UAHasRan_Init, UAInfo_Init

from SpectrumCommon.Const.UA.UATags import UA_AGUAIterationsTag

from src._spectrum.Tools.ExportPJNZ.ExportUtil import getSexLabel, setRowOfYearVals, addValueAtRowCol



def writeDPUAFile(projection):
    sheet = []

    addValueAtRowCol(sheet, 0, 0, 'Uncertainty Analysis configuration file')
    addValueAtRowCol(sheet, 1, 0, 'Version')
    addValueAtRowCol(sheet, 1, 1, 10)

    addValueAtRowCol(sheet, 2, 0, 'Process Date')
    addValueAtRowCol(sheet, 2, 1, projection[DP_UAInfoTag]['ProcessDate'])
    addValueAtRowCol(sheet, 2, 2, projection[DP_UAInfoTag].get('ProcessDateDelphi', 0))

    addValueAtRowCol(sheet, 3, 0, 'First year')
    addValueAtRowCol(sheet, 3, 1, projection[PJN_FirstYearTag])

    addValueAtRowCol(sheet, 4, 0, 'Last year')
    addValueAtRowCol(sheet, 4, 1, projection[PJN_FinalYearTag])

    addValueAtRowCol(sheet, 5, 0, 'Projection Valid')
    addValueAtRowCol(sheet, 5, 1, int(True))

    addValueAtRowCol(sheet, 6, 0, 'Process Time of Last Calc')
    addValueAtRowCol(sheet, 6, 1, projection[DP_UAInfoTag]['ProcessTime'])

    addValueAtRowCol(sheet, 7, 0, 'Ratio of fertility of HIV+ to HIV- women')
    addValueAtRowCol(sheet, 7, 1, DP_UASettings['HIVTFR'])
    addValueAtRowCol(sheet, 8, 0, 'Ratio of female to male incidence')
    addValueAtRowCol(sheet, 8, 1, DP_UASettings['HIVSexRatio'])
    addValueAtRowCol(sheet, 9, 0, 'MTCT Rate')
    addValueAtRowCol(sheet, 9, 1, DP_UASettings['MTCTRate'])
    addValueAtRowCol(sheet, 10, 0, 'Cotrimoxazole per Number Infected')
    addValueAtRowCol(sheet, 10, 1, DP_UASettings['Cotrim'][DPUA_Mean])
    addValueAtRowCol(sheet, 10, 2, DP_UASettings['Cotrim'][DPUA_StdDev])
    addValueAtRowCol(sheet, 11, 0, 'Child survival on ART, under 1 year old')
    addValueAtRowCol(sheet, 11, 1, DP_UASettings['UAChildLT1'][DPUA_Mean])
    addValueAtRowCol(sheet, 11, 2, DP_UASettings['UAChildLT1'][DPUA_StdDev])
    addValueAtRowCol(sheet, 12, 0, 'Child survival on ART, over 1 year old, first year on ART:')
    addValueAtRowCol(sheet, 12, 1, DP_UASettings['UAChildGT1FY'][DPUA_Mean])
    addValueAtRowCol(sheet, 12, 2, DP_UASettings['UAChildGT1FY'][DPUA_StdDev])
    addValueAtRowCol(sheet, 13, 0, 'Child survival on ART, over 1 year old, subsequent years on ART')
    addValueAtRowCol(sheet, 13, 1, DP_UASettings['UAChildGT1SY'][DPUA_Mean])
    addValueAtRowCol(sheet, 13, 2, DP_UASettings['UAChildGT1SY'][DPUA_StdDev])

    addValueAtRowCol(sheet, 14, 0, 'Confidence Interval')
    addValueAtRowCol(sheet, 14, 1, DPUA_ConfInterval)

    addValueAtRowCol(sheet, 15, 0, 'Number of Iterations')
    addValueAtRowCol(sheet, 15, 1, projection[DP_UAInfoTag]['NumIterations'])

    addValueAtRowCol(sheet, 16, 0, 'Aggregate Data Capture Year')
    addValueAtRowCol(sheet, 16, 1, projection[DP_UAInfoTag]['AgDataYear'])

    return sheet


def readDPUAFile(file, projection):
    UAInfo = UAInfo_Init()

    sheet = gb_read_csv_sheet(file)

    UAInfo['ProcessDate'] = sheet[2, 1]
    UAInfo['ProcessDateDelphi'] = float(sheet[2, 2])
    UAInfo['ProcessTime'] = sheet[6, 1]
    UAInfo['NumIterations'] = int(sheet[15, 1])
    UAInfo['AgDataYear'] = int(sheet[16, 1])

    return {DP_UAInfoTag : UAInfo}

def writeDPUADFile(params, projection):
    UALowHighRatios = projection[DP_UALowHighRatiosTag]
    sheet = []
    
    addValueAtRowCol(sheet, 0, 0, 'Uncertainty Analysis data file')

    addValueAtRowCol(sheet, 1, 0, 'Version')
    addValueAtRowCol(sheet, 1, 1, 10)

    addValueAtRowCol(sheet, 2, 0, 'Process Date')
    addValueAtRowCol(sheet, 2, 1, projection[DP_UAInfoTag]['ProcessDate'])
    addValueAtRowCol(sheet, 2, 2, projection[DP_UAInfoTag].get('ProcessDateDelphi', 0))

    addValueAtRowCol(sheet, 3, 0, 'AIDS Deaths in final year of projection:')
    addValueAtRowCol(sheet, 3, 1, projection[DP_AIDSDeathsFYearUATag])

    addValueAtRowCol(sheet, 4, 0, 'Master ID')
    addValueAtRowCol(sheet, 4, 1, 'Indicator name')
    addValueAtRowCol(sheet, 4, 2, 'Sex name')
    addValueAtRowCol(sheet, 4, 3, 'Sex value')
    addValueAtRowCol(sheet, 4, 4, 'High/Low')

    col = 5
    for t in GBRange(projection[PJN_FirstYearTag], projection[PJN_FinalYearTag]):
        addValueAtRowCol(sheet, 4, col, t)
        col += 1
    
    def getLowHighLabel(lowHigh):
        if lowHigh == DPUA_HighRatio:
            return 'High'
        else:
            return "Low"

    row = 6
    for rec in UALowHighRatios:
        addValueAtRowCol(sheet, row, 0, rec['mstID'])
        # sheet(row, 1, UALowHighRatios[i]['mstID']) indicator name - no access currently
        for sex, sexRec in enumerate(rec['values']):
            for lowHigh in GBRange(DPUA_LowRatio, DPUA_HighRatio):
                addValueAtRowCol(sheet, row, 2, getSexLabel(sex))
                addValueAtRowCol(sheet, row, 3, int(sex))
                addValueAtRowCol(sheet, row, 4, getLowHighLabel(lowHigh))
                values = sexRec[lowHigh] 
                setRowOfYearVals(sheet, values, None,  row, startCol=5)
                row += 1
    addValueAtRowCol(sheet, row, 0, '<end>')

    return sheet

def readDPUADFile(file):

    sheet = gb_read_csv_sheet(file)

    tagCol = 0
    sexCol = 3
    yearStartCol = 5 
    headerRow = 4
    dataStartRow = 6    

    def readMstIDBlock(sheet, row : int, numYears : int):
        UALowHighRatiosRec = getUALowHighRatiosRec(numYears)
        values = np.zeros_like(UALowHighRatiosRec['values'])
        UALowHighRatiosRec['mstID'] = int(sheet[row][tagCol])
        while True:
            for r in GBRange(DPUA_LowRatio, DPUA_HighRatio):
                sex = int(sheet[row][sexCol])
                values[sex][r] = sheet[row][yearStartCol:].copy()
            
                row += 1
            if not (str(sheet[row][tagCol]) == ''):
                break
        UALowHighRatiosRec['values'] = values.tolist()
        UALowHighRatiosRec['isValidUAData'] = True
        
        return UALowHighRatiosRec, row
    
    # Get MV shapes from init
    UALowHighRatios = UALowHighRatios_Init()
    AIDSDeathsFYearUA = AIDSDeathsFYearUA_Init()
    UAHasRan = UAHasRan_Init()

    numYears = len(sheet[headerRow][yearStartCol:])

    endTagRow = getTagRow(sheet, '<end>')
    row = dataStartRow
    
    while (row < endTagRow):
        UALowHighRatiosRec, row = readMstIDBlock(sheet, row, numYears) 
        UALowHighRatios.append(UALowHighRatiosRec)

    AIDSDeathsFYearUA = int(sheet[3, 1])
    UAHasRan = True
    
    return {
        DP_UALowHighRatiosTag : UALowHighRatios,
        DP_AIDSDeathsFYearUATag : AIDSDeathsFYearUA,
        DP_UAHasRanTag : UAHasRan,
    } 


def writeDPUAD_AUAFile(params, projection):
    AGUAIterations = projection[UA_AGUAIterationsTag]
    sheet = []

    addValueAtRowCol(sheet, 0, 0, 'Uncertainty Analysis data file')

    addValueAtRowCol(sheet, 1, 0, 'Version')
    addValueAtRowCol(sheet, 1, 1, 10)

    addValueAtRowCol(sheet, 2, 0, 'Process Date')
    addValueAtRowCol(sheet, 2, 1, projection[DP_UAInfoTag]['ProcessDate'])
    addValueAtRowCol(sheet, 2, 2, projection[DP_UAInfoTag].get('ProcessDateDelphi', 0))

    addValueAtRowCol(sheet, 3, 0, 'Year')
    addValueAtRowCol(sheet, 3, 1, projection[DP_UAInfoTag]['AgDataYear'])

    addValueAtRowCol(sheet, 4, 0, 'Master ID')
    addValueAtRowCol(sheet, 4, 1, 'Indicator name')
    addValueAtRowCol(sheet, 4, 2, 'Sex name')
    addValueAtRowCol(sheet, 4, 3, 'Sex value')

    col = 4
    for i in GBRange(1, projection[DP_UAInfoTag]['NumIterations']):
        addValueAtRowCol(sheet, 4, col, i)
        col += 1

    row = 6
    for mstID in AGUAIterations:
        addValueAtRowCol(sheet, row, 0, mstID)
        # sheet(row, 1, mstID) indicator name - no access currently
        for sex, sexRec in enumerate(AGUAIterations[mstID]):
            addValueAtRowCol(sheet, row, 2, getSexLabel(sex))
            addValueAtRowCol(sheet, row, 3, int(sex))
            col = 4
            for val in sexRec:
                addValueAtRowCol(sheet, row, col, val)
                col += 1
            row += 1

    return sheet

def readDPUAD_AUAFile(file):
    
    tagCol = 0
    sexCol = 3
    runsStartCol = 4 
    headerRow = 5
    dataStartRow = 6

    def readMstIDBlock(sheet, row : int, numRuns : int, UARuns : dict):

        mstID = sheet[row][tagCol]
        values = np.zeros((GB_Female + 1, numRuns))
        while True:
            sex = int(sheet[row][sexCol])
            values[sex, :] = sheet[row][runsStartCol:].copy()
        
            row += 1
            if (row >= len(sheet)):
                break

            if not (str(sheet[row][tagCol]) == ''):
                break
        UARuns[mstID] = values.tolist()
        
        return row

    sheet = gb_read_csv_sheet(file) 
    row = dataStartRow
    
    numRuns = len(sheet[headerRow][runsStartCol:])
    UARuns = {}
    while (row < len(sheet)):
        row = readMstIDBlock(sheet, row, numRuns, UARuns) 
    
    return {UA_AGUAIterationsTag : UARuns}

def readSPUFile(spu_file):
    
    def findTagRows(sheet, tag : str, column = 0):
        whereArr = [i for i, si in enumerate(sheet[:, column]) if si.startswith(tag)]
        return whereArr

    def getCurve(sheet, startRow, col):
        curve = []
        row = startRow
        while not (sheet[row, 0].split(',')[0] == '=='):
            curve.append(float(sheet[row, 0].split(',')[col]))
            row += 1
        return curve
    
    incidenceCol = 2
    prevalenceCol = 1

    #buffer
    buffer = BytesIO(spu_file)
    sheet = gb_read_csv_sheet(buffer)

    rows = findTagRows(sheet, 'COUNT')

    incidenceCurves = []
    prevalenceCurves = []

    for row in rows:
        incidenceCurves.append(getCurve(sheet, row + 1, incidenceCol))
        prevalenceCurves.append(getCurve(sheet, row + 1, prevalenceCol))


    return incidenceCurves, prevalenceCurves  
    