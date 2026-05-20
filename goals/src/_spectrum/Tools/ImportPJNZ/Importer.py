from io import BytesIO
import numpy as np
from zipfile import ZipFile

from SpectrumCommon.Modvars.GB.GBCreateProjection import *
from SpectrumCommon.Modvars.GB.GBDefs import createProjectionParams
from Tools.ImportPJNZ.ImportPJN import *
from src._spectrum.Tools.ImportPJNZ.DP.ImportDP import *
from src._spectrum.Tools.ImportPJNZ.CS.ImportCS import *
from src._spectrum.Tools.ImportPJNZ.FP.ImportFP import *
from src._spectrum.Tools.ImportPJNZ.HV.ImportHV import openHV
from src._spectrum.Tools.ImportPJNZ.RN.ImportRN import openRN

from AvenirCommon.Database import *
from SpectrumCommon.Const.GB import *
from SpectrumCommon.Const.DP import *

from src._spectrum.SpectrumCommon.Util.AM.AMUncertaintyAnalysisRW import readDPUADFile, readDPUAFile, readDPUAD_AUAFile

def GB_ImportProjectionFromFile(FQName : str):
    with open(FQName, "rb") as f:
        PJNZ = BytesIO(f.read())
    return GB_ImportProjection(PJNZ)


def GB_ImportProjection(PJNZ: BytesIO):
    success = False
    params  = createProjectionParams()
    epp_files = {}
    shiny90 = None
    projection = None


    with ZipFile(PJNZ, "r") as zipObj:
        names = zipObj.namelist()

        for FName in names:
            if str.lower(FName).endswith(".pjn"):  # find .PJN file, call openPJN
                with zipObj.open(FName) as file:
                    params = openPJN(file)
                    params.extra['blankProjection'] = True
                    success = True
                    break

        if success:
            success = False
            projection = GB_CreateProjection(params)

            if isinstance(projection, dict):
                for FName in names:
                    if str.lower(FName).endswith(".dp"):  # find .DP file, call openDP
                        with zipObj.open(FName) as file:
                            openDP(file, params, projection)
                            success = True

                    if str.lower(FName).endswith(".cs"):  # find .CS file, call openCS
                        with zipObj.open(FName) as file:
                            openCS(file, params, projection)
                            success = True

                    if str.lower(FName).endswith(".fp4"):  # find .DP file, call openDP
                        with zipObj.open(FName) as file:
                            openFP(file, params, projection)
                            success = True
                            
                    if str.lower(FName).endswith(".shiny90"):  # find .DP file, call openDP
                        with zipObj.open(FName) as file:
                            shiny90 ={
                                "name": FName,
                                "file": file.read()
                            }
                            
                    if str.lower(FName).endswith(".hv"):  # find .HV file, call openHV
                        with zipObj.open(FName) as file:
                            openHV(file, params, projection)
                            success = True

                    if str.lower(FName).endswith(".rn"):  # find .RN file, call openRN
                        with zipObj.open(FName) as file:
                            openRN(file, params, projection)
                            success = True

                    DPUAOutput = []
                    if str.lower(FName).startswith(str.lower("DPUA") + "/") and str.lower(FName).endswith(str.lower(".DPUA")):
                        with zipObj.open(FName) as file:
                            DPUAOutput = readDPUAFile(file, projection)
                            projection.update(DPUAOutput)

                    DPUADOutput = []
                    if str.lower(FName).startswith(str.lower("DPUA") + "/") and str.lower(FName).endswith(str.lower(".DPUAD")):
                        with zipObj.open(FName) as file:
                            DPUADOutput = readDPUADFile(file)
                            projection.update(DPUADOutput)

                    DPUAD_AUAOutput = []
                    if str.lower(FName).startswith(str.lower("DPUA") + "/") and str.lower(FName).endswith(str.lower(".DPUAD_AUA")):
                        with zipObj.open(FName) as file:
                            DPUAD_AUAOutput = readDPUAD_AUAFile(file)
                            projection.update(DPUAD_AUAOutput)

                            if GB_UA not in projection[PJN_ModulesTag]:
                                projection[PJN_ModulesTag] = np.append(projection[PJN_ModulesTag], GB_UA)
                            if GB_UA not in params.modules:
                                params.modules.append(GB_UA)


            epp_file_names = [name for name in zipObj.namelist() if str.lower(name).startswith(str.lower("EPP/"))]
            epp_files = {name: zipObj.read(name) for name in epp_file_names}
            

        if success:
            return projection, params, epp_files, shiny90
        else:
            return None, None, None, None

