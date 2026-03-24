#include "../../leapfrog-core/include/leapfrog_py.hpp"

template<typename ...Args>
auto sim_model(Args&&... args) {
  return simulate_model<leapfrog::Goals>(std::forward<Args>(args)...);
};


nb::dict run_base_model(
  const nb::dict parameters,
  const std::vector<int> output_years
) {
  return sim_model(parameters, output_years);
}

nb::dict run_base_model_from_state(
  const nb::dict parameters,
  const nb::dict initial_state,
  int simulation_start_year,
  const std::vector<int> output_years
) {
  return sim_model(parameters, output_years, initial_state, simulation_start_year);
}

nb::dict run_base_model_single_year(
  const nb::dict parameters,
  const nb::dict initial_state,
  int simulation_start_year
) {
  return sim_model(parameters, initial_state, simulation_start_year);
}


nb::dict get_leapfrog_ss() {
  return leapfrog::get_ss_py<leapfrog::Goals>();
}

NB_MODULE(_core, m) {
  m.doc() = "Leapfrog-Goals python interface";

  m.def("run_base_model", &run_base_model, R"pbdoc(
      Run the goals model.
  )pbdoc");
  m.def("run_base_model_from_state", &run_base_model_from_state, R"pbdoc(
      Run the goals model from an initial state.
  )pbdoc");
  m.def("run_base_model_single_year", &run_base_model_single_year, R"pbdoc(
      Run the goals model from an initial state for a single year.
  )pbdoc");
  m.def("get_goals_ss_py", &get_leapfrog_ss, R"pbdoc(
    Get the state space dimensions for the Goals model,
  )pbdoc");
}
