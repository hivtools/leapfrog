from leapfrog_py import (
    LeapfrogData,
    LeapfrogDataSingleYear,
    LeapfrogParameters,
    LeapfrogRange,
<<<<<<< HEAD
=======
    LeapfrogStateSpace
>>>>>>> 11ae9f4be0fefc897892a8eb6689b4043c7c0bd7
)

def run_base_model(
    parameters: LeapfrogParameters, configuration: str, output_years: LeapfrogRange
) -> LeapfrogData: ...
def run_base_model_from_state(
    parameters: LeapfrogParameters,
    configuration: str,
    initial_state: LeapfrogDataSingleYear,
    simulation_start_year: int,
    output_years: LeapfrogRange,
) -> LeapfrogData: ...
def run_base_model_single_year(
    parameters: LeapfrogParameters,
    configuration: str,
    initial_state: LeapfrogDataSingleYear,
    simulation_start_year: int,
) -> LeapfrogDataSingleYear: ...
<<<<<<< HEAD
=======
def get_leapfrog_ss_py(
    configuration: str
) -> LeapfrogStateSpace: ...
>>>>>>> 11ae9f4be0fefc897892a8eb6689b4043c7c0bd7
