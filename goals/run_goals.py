#!/usr/bin/python3

import os
import numpy as np

from leapfrog_goals import get_goals_ss, run_goals
from SpectrumCommon.Util.LeapfrogDataMapping import modvars_to_leapfrog
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


for tag, value in modvars.items():
    if isinstance(value, list):
        try:
            if len(value) > 0 and (
                (isinstance(value[0], dict))
                or (isinstance(value[0], str))
                or (isinstance(value[0], bool))
            ):
                value = np.array(value, order="C")
            else:
                value = np.array(value, order="C", dtype=np.dtype(np.float64))
        except Exception() as e:
            raise Exception(f"Failed to convert list to numpy array {tag}") from e

    modvars[tag] = np.array(value)

ss = get_goals_ss()

print("converting to leapfrog")
lf_data = modvars_to_leapfrog(modvars, ss, "Goals")

print("finished converting to leapfrog")

# lf_data["b_condom_prop_sum"] = np.full((81), 0)

print(f"Running from {modvars[PJN_FirstYearTag]} to {modvars[PJN_FinalYearTag] + 1}")

output = run_goals(
    lf_data,
    output_years=range(modvars[PJN_FirstYearTag], modvars[PJN_FinalYearTag] + 1),
)

# print(output['total_population'])

