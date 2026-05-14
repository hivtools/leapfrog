from AvenirCommon.Util import gb_read_csv_sheet,  getAllTags
from SpectrumCommon.Modvars.GB.GBUtil import get_country_ISO3Alpha
from SpectrumCommon.Modvars.GB.GBDefs import createProjectionParams

from SpectrumCommon.Const.GB import *

def openPJN(file):
    # importVersionNum = '6.2'
    # importBetaNum = '4'
    params = createProjectionParams()
    # import pandas as pd
    # sheet = pd.read_csv(file, header=None, na_filter=False)
    sheet = gb_read_csv_sheet(file)
    tags = getAllTags(sheet)
    projectionVersionRow = tags.get('<Projection Version Details>', None)
    if projectionVersionRow:
        versionNum = sheet[projectionVersionRow + 2, GB_RW_DataStartCol]
        betaNum = sheet[projectionVersionRow + 4, GB_RW_DataStartCol]
    
    # if (importVersionNum != versionNum) or (importBetaNum != betaNum):
    #     raise Exception('PJNZ file has not been created with the correct version of Spectrum Desktop, Version' + importVersionNum + ', Beta ' + importBetaNum)

    projNameRow = tags.get('<Projection Name>', None)
    if projNameRow:
        params.fileName = sheet[projNameRow + 2, GB_RW_DataStartCol]

    projYrDtlsRow = tags.get('<Projection Year Details>', None)
    if projYrDtlsRow:
        params.finalYear = int(sheet[projYrDtlsRow + 4, GB_RW_DataStartCol])
        params.firstYear = int(sheet[projYrDtlsRow + 6, GB_RW_DataStartCol])

    projParamsRow = tags.get('<Projection Parameters>', None)
    if projParamsRow:
        params.country =  get_country_ISO3Alpha(int(sheet[projParamsRow + 2, GB_RW_DataStartCol]))
    # params.country =  int(sheet.values[projParamsRow + 2, GB_RW_DataStartCol])
    
    projParamsSubnatRow = tags.get('<Projection Parameters - Subnational Region Name2>', None)
    if projParamsSubnatRow:
        params.extra[GB_Extra_subnatName] = sheet[projParamsSubnatRow + 2, GB_RW_DataStartCol]
        params.extra[GB_Extra_SubnatCode] = int(sheet[projParamsSubnatRow + 3, GB_RW_DataStartCol])


    projModulesRow = tags.get('<Projection Modules>', None)
    modules = []
    if projModulesRow:
        modulesRow = projModulesRow + 2
        while sheet[modulesRow, GB_RW_DataStartCol] != '':
            modules.append(int(sheet[modulesRow, GB_RW_DataStartCol]))
            modulesRow += 1
    params.modules = modules

    # params.extra['region'] = 4

    return params