from leapfrog_goals import (
    LeapfrogData,
    LeapfrogDataSingleYear,
    LeapfrogParameters,
    LeapfrogRange,
    LeapfrogStateSpace,
)

def run_base_model(
    parameters: LeapfrogParameters, output_years: LeapfrogRange
) -> LeapfrogData: ...
def run_base_model_from_state(
    parameters: LeapfrogParameters,
    initial_state: LeapfrogDataSingleYear,
    simulation_start_year: int,
    output_years: LeapfrogRange,
) -> LeapfrogData: ...
def run_base_model_single_year(
    parameters: LeapfrogParameters,
    initial_state: LeapfrogDataSingleYear,
    simulation_start_year: int,
) -> LeapfrogDataSingleYear: ...
def get_leapfrog_ss_py(configuration: str) -> LeapfrogStateSpace: ...
