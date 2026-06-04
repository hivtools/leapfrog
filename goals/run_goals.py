#!/usr/bin/python3

import os

from leapfrog_goals import get_goals_ss, run_goals
from SpectrumCommon.Util.LeapfrogDataMapping import modvars_to_leapfrog
from SpectrumCommon.Util.ConvertNumpy import modvars_to_numpy
from Tools.ImportPJNZ.Importer import GB_ImportProjectionFromFile
from SpectrumCommon.Const.PJ.PJNTags import PJN_FirstYearTag, PJN_FinalYearTag


"""
Script for running goals whilst in development. This should be turned
into a proper pytest test at some point.
"""


modvars, param, epp, shiny90 = GB_ImportProjectionFromFile(
    os.path.join("tests", "resources", "SouthAfrica.PJNZ")
)

print("Finished reading import")


modvars = modvars_to_numpy(modvars)

ss = get_goals_ss()

print("converting to leapfrog")
lf_data = modvars_to_leapfrog(modvars, ss, "Goals")

print("finished converting to leapfrog")

print(f"Running from {modvars[PJN_FirstYearTag]} to {modvars[PJN_FinalYearTag] + 1}")

output = run_goals(
    lf_data,
    output_years=range(modvars[PJN_FirstYearTag], modvars[PJN_FinalYearTag] + 1),
)
