#!/usr/bin/python3

import os
import pickle

import numpy as np

from leapfrog_goals import get_goals_ss, run_goals
from src.leapfrog_mapping.leapfrog_data_mapping import modvars_to_leapfrog
from Tools.ImportPJNZ.Importer import GB_ImportProjectionFromFile
"""
Note this script is only expected to be used temporarily until the
proper data reading code is ready to go.

Pickle created via:

def modvars_to_numpy(tag, value):
    # Taken from FilterUtils.py
    if type(value) is list:
        try:
            if len(value) > 0 and ((type(value[0]) is dict) or (type(value[0]) is str) or (type(value[0]) is bool)):
                value = np.array(value, order='C')
            else:
                value = np.array(value, order='C', dtype=np.dtype(np.float64))

        except:
            print(f'Failed to convert list to numpy array {tag}')

    return value

pjnz = "C:\\Users\\Test\\Downloads\\Zimbabwe.PJNZ"
with open(pjnz, "rb") as fh:
    buf = BytesIO(fh.read())
projection, params, epp_files, shiny90 = GB_ImportProjection(buf)

numpy_modvars = {tag: modvars_to_numpy(tag, value) for tag, value in projection.items()}

with open("zimbabwe_modvars.pickle", "wb") as handle:
    pickle.dump(numpy_modvars, handle, protocol=pickle.HIGHEST_PROTOCOL)
"""

# zim_pickle_path = os.path.expanduser("~/Downloads/zimbabwe_modvars.pickle")

# with open(zim_pickle_path, "rb") as handle:
#     modvars = pickle.load(handle)



modvars, param, epp, shiny90 = GB_ImportProjectionFromFile(r"C:\work\LeapFrog\V2\Files_PJNZ\Eswatini-2025-sqb.pjnz")

for tag, value in modvars.items():
    if isinstance(value, list):
        try:
            if len(value) > 0 and ((isinstance(value[0], dict)) or (isinstance(value[0], str)) or (isinstance(value[0], bool))):
                value = np.array(value, order='C')
            else:
                value = np.array(value, order='C', dtype=np.dtype(np.float64))
        except:
            print(f'Failed to convert list to numpy array {tag}')

    modvars[tag] = np.array(value)

ss = get_goals_ss()
lf_data = modvars_to_leapfrog(modvars, ss)

lf_data["ex_input"] = np.full((81, 2), 1)

output = run_goals(lf_data)
print(output)