from Tools.ExportPJNZ.ExportUtil import createPJNZParams
from Tools.ExportPJNZ.ExportUtil import writeHeaders, addStartTag, addDescript, addNote, addValue
from SpectrumCommon.Modvars.GB.GBUtil import get_country_ISO3Numeric
from SpectrumCommon.Modvars.GB.GBDefs import createProjectionParams

from SpectrumCommon.Const.GB import *

def writePJN(params = createProjectionParams()):
    # sheet = GBSheet()
    sheet = []
    PJNZParams = createPJNZParams()

    writeHeaders(sheet, PJNZParams)    
    
    addStartTag(sheet, PJNZParams, '<Projection General>')
    
    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams, 'Projection file version')
    PJNZParams.currRow += 1
    addValue(sheet, PJNZParams, GB_RW_DataStartCol, 'Projection File Version 4.0')   
    PJNZParams.currRow += 1
    addValue(sheet, PJNZParams, 1, 'Spectrum version number')  
    PJNZParams.currRow += 1
    addValue(sheet, PJNZParams, GB_RW_DataStartCol, 6.42)  
    
    PJNZParams.currRow += 2
    
    addStartTag(sheet, PJNZParams, '<Projection Name>')
    
    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams, 'Name of the projection')
    PJNZParams.currRow += 1
    addValue(sheet, PJNZParams, GB_RW_DataStartCol, params.fileName)   
    
    PJNZParams.currRow += 2
    
    addStartTag(sheet, PJNZParams, '<Projection Year Details>')
    
    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams, 'First year')
    PJNZParams.currRow += 1
    addValue(sheet, PJNZParams, GB_RW_DataStartCol, params.firstYear) 
    
    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams, 'Final year')
    PJNZParams.currRow += 1
    addValue(sheet, PJNZParams, GB_RW_DataStartCol, params.finalYear) 
    
    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams, 'Calc year')
    PJNZParams.currRow += 1
    addValue(sheet, PJNZParams, GB_RW_DataStartCol, params.firstYear) 
    
    PJNZParams.currRow += 2
    
    addStartTag(sheet, PJNZParams, '<Projection Parameters>')
    
    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams, 'Country Code')
    PJNZParams.currRow += 1
    addValue(sheet, PJNZParams, GB_RW_DataStartCol, get_country_ISO3Numeric(params.country))
    
    PJNZParams.currRow += 2
    
    addStartTag(sheet, PJNZParams, '<Projection Parameters - Subnational Region Name2>')
    
    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams, 'Subnational Region Name and Code')
    PJNZParams.currRow += 2
    addValue(sheet, PJNZParams, GB_RW_DataStartCol, 0)
    if 'subNatCode' in params.extra:
        addValue(sheet, PJNZParams, GB_RW_DataStartCol, params.extra['subNatCode'])
    
    PJNZParams.currRow += 2
    
    extensions = {
        GB_DP : '.DP',
        GB_AM : '.AIM'
    }
    
    addStartTag(sheet, PJNZParams, '<Projection Modules>')
    PJNZParams.currRow += 1
    addDescript(sheet, PJNZParams, 'Names of the files associated to each module')
    PJNZParams.currRow += 1
    for modID in params.modules:
        addValue(sheet, PJNZParams, GB_RW_DataStartCol, modID)
        addValue(sheet, PJNZParams, GB_RW_DataStartCol + 1, params.fileName + extensions[modID])
        PJNZParams.currRow += 1
    
    PJNZParams.currRow += 1
    
    addStartTag(sheet, PJNZParams, '<LiST Costing On?>')
    
    PJNZParams.currRow += 1
    addNote(sheet, PJNZParams, 'FALSE')
    addValue(sheet, PJNZParams, GB_RW_DataStartCol, 0)
    if GB_LIST_COSTING_ON in params.extra:
        addNote(sheet, PJNZParams, params.extra[GB_LIST_COSTING_ON])
        addValue(sheet, PJNZParams, GB_RW_DataStartCol, int(params.extra[GB_LIST_COSTING_ON]))
    
    PJNZParams.currRow += 2
    
    addStartTag(sheet, PJNZParams, '<TIME Econ On?>')
    
    PJNZParams.currRow += 1
    addNote(sheet, PJNZParams, 'FALSE')
    addValue(sheet, PJNZParams, GB_RW_DataStartCol, 0)
    if GB_TB_COSTING_ON in params.extra:
        addNote(sheet, PJNZParams, params.extra[GB_TB_COSTING_ON])
        addValue(sheet, PJNZParams, GB_RW_DataStartCol, int(params.extra[GB_TB_COSTING_ON]))
    
    PJNZParams.currRow += 2

    return sheet