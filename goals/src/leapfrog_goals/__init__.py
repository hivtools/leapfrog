from typing import TypeAlias, Union, cast

import h5py
import numpy as np
from h5py._hl.dataset import Dataset

from leapfrog_goals._core import (
    get_goals_ss_py,
    run_base_model,
    run_base_model_from_state,
    run_base_model_single_year,
)

LeapfrogParameters: TypeAlias = dict[str, Union[np.ndarray, int, float]]
LeapfrogDataSingleYear: TypeAlias = LeapfrogParameters
LeapfrogData: TypeAlias = dict[str, np.ndarray]
LeapfrogRange: TypeAlias = Union[range, list]
LeapfrogStateSpace: TypeAlias = dict[str, int | float]


def read_h5_file(file_path: str) -> LeapfrogParameters:
    ret = {}
    f = h5py.File(file_path, "r")
    for key in list(f.keys()):
        dset = cast(Dataset, f[key])
        if dset.size == 1:
            val = dset[0]
            if isinstance(val, bytes):
                ret[key] = val.decode("utf-8")
            else:
                ret[key] = val
        else:
            ret[key] = np.transpose(np.array(f[key]))
    f.close()
    return ret


def save_h5_file(dat: Union[LeapfrogParameters, LeapfrogData], file_path: str) -> None:
    f = h5py.File(file_path, "w")
    for key in list(dat.keys()):
        arr = dat[key]
        if isinstance(arr, np.ndarray):
            f.create_dataset(key, data=np.transpose(arr))
        else:
            f[key] = dat[key]
    f.close()


def get_time_slice(state: LeapfrogData, index: int) -> LeapfrogDataSingleYear:
    return {
        k: v[..., index] if v.ndim > 1 else v[index].item() for (k, v) in state.items()
    }


def concat_on_time_dim(state1, state2):
    return {k: np.concatenate((state1[k], state2[k]), axis=-1) for k in state1.keys()}


def run_goals(
    parameters: LeapfrogParameters,
    output_years: LeapfrogRange = range(1970, 2031),
):
    return run_base_model(parameters, output_years)


def run_goals_from_state(
    parameters: LeapfrogParameters,
    initial_state: LeapfrogDataSingleYear,
    simulation_start_year: int,
    output_years: LeapfrogRange = range(1970, 2031),
):
    return run_base_model_from_state(
        parameters, initial_state, simulation_start_year, output_years
    )


def run_goals_single_year(
    parameters: LeapfrogParameters,
    initial_state: LeapfrogDataSingleYear,
    simulation_start_year: int,
):
    return run_base_model_single_year(parameters, initial_state, simulation_start_year)


def get_goals_ss(configuration: str) -> LeapfrogStateSpace:
    return get_goals_ss_py(configuration)
