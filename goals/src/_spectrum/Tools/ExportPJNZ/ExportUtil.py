import numpy as np
from pydantic import BaseModel
#import time

from SpectrumCommon.Modvars.GB.GBDefs import createProjectionParams
# from AvenirCommon.Wrappers.GBSheetWrapper import GBSheet

from SpectrumCommon.Const.GB import GB_RW_DataStartCol, GB_NativeYear
from AvenirCommon.Util import GBRange
from SpectrumCommon.Modvars.GB.GBUtil import getYearIdx
from SpectrumCommon.Const.DP import *

class createPJNZParams(BaseModel):
    currRow: int = 0

def trimNumber(value):
    # NOTE: Prevent outputting values with a decimal of 0 (example: 123.0) to be able to compare against desktop projections better.
    if type(value) in [float]:
        if value == int(value):
            value = int(value); 
    return value

def trimNumbers(values : list=[]):
    # NOTE: Prevent outputting values with a decimal of 0 (example: 123.0) to be able to compare against desktop projections better.
    newValues = values.copy()
    for i in range(len(newValues)):
        if type(newValues[i]) in [float]:
            if newValues[i] == int(newValues[i]):
                newValues[i] = int(newValues[i]);    
    return newValues

def writeHeaders(sheet, PJNZParams):
    addValue(sheet, PJNZParams, GB_RW_TagCol, 'Tag')
    addValue(sheet, PJNZParams, GB_RW_DescriptCol, 'Description')
    addValue(sheet, PJNZParams, GB_RW_NotesCol, 'Notes')
    addValue(sheet, PJNZParams, GB_RW_DataStartCol, 'Data')
    sheet.append([])   # blank row
    PJNZParams.currRow += 2

def addStartTag(sheet, PJNZParams, tag):
    # print(tag)
#    global time_start
#    global time_tag
#    time_tag = tag
#    time_start = time.time()
    sheet.append([tag])
    sheet.append([])
    PJNZParams.currRow = len(sheet) - 2
    pass
    # PJNZParams.currRow += 1

def addValueTag(sheet, PJNZParams):
    if len(sheet) <= PJNZParams.currRow:
        for r in GBRange(len(sheet), PJNZParams.currRow):
            sheet.append([])

    sheet[PJNZParams.currRow] = ['', '<Value>']
    pass
    # PJNZParams.currRow += 1

def addEndTag(sheet, PJNZParams):
    PJNZParams.currRow += 1
    if len(sheet) <= PJNZParams.currRow:
        for r in GBRange(len(sheet), PJNZParams.currRow):
            sheet.append(['', ''])
    sheet[PJNZParams.currRow][0] = '<End>'
    PJNZParams.currRow += 1
#    global time_start
#    global time_tag
#    end_time = time.time()-time_start
#    if end_time > 1.0:
#        print(f'{time_tag} {end_time}')
    # PJNZParams.currRow += 1

def addDescript(sheet, PJNZParams, description : str):
    col = GB_RW_DescriptCol
    if len(sheet) <= PJNZParams.currRow:
        for r in GBRange(len(sheet), PJNZParams.currRow):
            sheet.append([''] * (col + 1))
    if len(sheet[PJNZParams.currRow]) <= col:
        sheet[PJNZParams.currRow] += [''] * (col - len(sheet[PJNZParams.currRow]) + 1)
    sheet[PJNZParams.currRow][col] = description

def addNote(sheet, PJNZParams, note : str):
    col = GB_RW_NotesCol
    if len(sheet) <= PJNZParams.currRow:
        for r in GBRange(len(sheet), PJNZParams.currRow):
            sheet.append([''] * (col + 1))
    if len(sheet[PJNZParams.currRow]) <= col:
        sheet[PJNZParams.currRow] += [''] * (col - len(sheet[PJNZParams.currRow]) + 1)
    sheet[PJNZParams.currRow][col] = note

def addNoteAtRow(sheet, row, note : str):
    col = GB_RW_NotesCol
    if len(sheet) <= row:
        for r in GBRange(len(sheet), row):
            sheet.append([''] * (col + 1))
    if len(sheet[row]) <= col:
        sheet[row] += [''] * (col - len(sheet[row]) + 1)
    sheet[row][col] = note

def addValue(sheet, PJNZParams, col, value):
    if len(sheet) <= PJNZParams.currRow:
        for r in GBRange(len(sheet), PJNZParams.currRow):
            sheet.append([''] * (col + 1))
    if len(sheet[PJNZParams.currRow]) <= col:
        sheet[PJNZParams.currRow] += [''] * (col - len(sheet[PJNZParams.currRow]) + 1)
    newValue = trimNumber(value) 
    sheet[PJNZParams.currRow][col] = newValue

def addValueAtRowCol(sheet, row, col, value):
    if len(sheet) <= row:
        for r in GBRange(len(sheet), row):
            sheet.append([''] * (col + 1))
    if len(sheet[row]) <= col:
        sheet[row] += [''] * (col - len(sheet[row]) + 1)
    newValue = trimNumber(value) 
    sheet[row][col] = newValue

def getRowOfYearValsInt(sheet,
                        values : list=[],
                        params : createProjectionParams=createProjectionParams(),
                        row : int=-1,
                        startCol : int=GB_RW_DataStartCol,
                        rowIncludesFirstYear : bool=False,
                        defaultStrReplace : int=DPNotAvail):

    getRowOfYearVals(sheet, values, params, row, startCol, rowIncludesFirstYear, defaultStrReplace)
    for t in GBRange(0, len(values) - 1):
        values[t] = int(values[t])

def getRowOfYearVals(sheet,
                     values : list=[],
                     params : createProjectionParams=createProjectionParams(),
                     row : int=-1,
                     startCol : int=GB_RW_DataStartCol,
                     rowIncludesFirstYear : bool=False,
                     defaultStrReplace : int=DPNotAvail):
    rowValues = sheet.values[row]
    yearCount = params.finalYear - params.firstYear + 1
    toFloat = float

    if rowIncludesFirstYear and (params.firstYear > GB_NativeYear):     #calcState projection and needs 'first-year' values imported
        values[0] = toFloat(rowValues[startCol])
        colStart = startCol + 1
    else:                                                               #non-calcstate projection or no 'first-year' values imported
        colStart = startCol

    for t, rawVal in enumerate(rowValues[colStart:colStart + yearCount]):
        if rawVal != '':
            values[t] = toFloat(rawVal)

getFloatValue = lambda sheet, row, col, defaultStrReplace: float(sheet.values[row, col])
    # val =
    # return defaultStrReplace if np.isnan(val) else val

def setRowOfYearVals(sheet : list = [],
                     values : list = [],
                     params : createProjectionParams =createProjectionParams(),
                     row : int = -1,
                     startCol : int = GB_RW_DataStartCol,
                     rowIncludesFirstYear : bool = False):

    if len(sheet) <= row:
        for r in GBRange(len(sheet), row):
            sheet.append([''] * (len(values) + 1))
    if len(sheet[row]) <= startCol:
        sheet[row] += [''] * (startCol - len(sheet[row]))

    # sheet[row] = sheet[row][:startCol] + values

    newValues = trimNumbers(values)
    sheet[row] = sheet[row][:startCol] + newValues

def sheetInsertRow(sheet, row = int, values = [], startCol = GB_RW_DataStartCol):
    col = startCol
    for val in values:
        addValueAtRowCol(sheet, row, col, val)
        col += 1

def deleteDFRows(sheet, rowStart : int, rowEnd : int):
    sheet = sheet.drop(sheet.index[GBRange(rowStart, rowEnd)])
    sheet = sheet.sort_index().reset_index(drop=True)
    return sheet

def addDFRow(sheet, row : int):
    sheet.loc[row - .5] = np.zeros_like(sheet[row])
    sheet = sheet.sort_index().reset_index(drop=True)
    return sheet

def getSexLabel(sex):
    SexLabels = {
        GB_BothSexes : 'Male+Female',
        GB_Male : 'Males',
        GB_Female : 'Females',
    }
    return SexLabels[sex]

def getSexLabelSingular(sex):
    SexLabels = {
        GB_BothSexes : 'Male+Female',
        GB_Male : 'Male',
        GB_Female : 'Female',
    }
    return SexLabels[sex]

def getRegionEN(currId):
    Labels = {
        DP_Asia : "Asia",
        DP_DevCountries : "High Income Countries",
        DP_EAfrica : "East Africa",
        DP_EEurope : "Eastern Europe",
        DP_LatAmerCarr : "Latin America and Caribbean",
        DP_NAfrMiddEast : "North Africa Middle East",
        DP_SAfrica : "Southern Africa",
        DP_WAfrica : "West Africa",
        DP_CAfrica : "Central Africa",
        DP_Custom : "Inputted"
    }
    return Labels[currId]