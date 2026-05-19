import numpy as np
import io
import csv
#import time

from AvenirCommon.Util import GBRange

from SpectrumCommon.Modvars.GB.GBDefs import createProjectionParams
from SpectrumCommon.Const.GB import GB_RW_DataStartCol, GB_NativeYear
from SpectrumCommon.Modvars.GB.GBUtil import getYearIdx
from SpectrumCommon.Const.DP import *



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

    if rowIncludesFirstYear and (params.firstYear > GB_NativeYear):     #calcState projection and needs 'first-year' values imported
        values[0] = float(sheet[row, startCol])
        col = startCol + 1
        for year in GBRange(params.firstYear, params.finalYear):
            t = getYearIdx(year, params.firstYear)
            if not sheet[row, col] == '':
                values[t] = getFloatValue(sheet, row, col, defaultStrReplace)
            col += 1
    else:                                                               #non-calcstate projection or no 'first-year' values imported
        col = startCol
        for year in GBRange(params.firstYear, params.finalYear):
            t = getYearIdx(year, params.firstYear)
            if not sheet[row, col] == '':
                values[t] = getFloatValue(sheet, row, col, defaultStrReplace)
            col += 1

getFloatValue = lambda sheet, row, col, defaultStrReplace: float(sheet[row, col])