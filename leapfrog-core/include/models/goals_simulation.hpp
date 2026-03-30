#pragma once

#include "../generated/config_mixer.hpp"
#include "../options.hpp"

namespace leapfrog {
namespace internal {

template<typename Config>
concept GoalsSimulationEnabled = RunDemographicProjection<Config>
    && RunHivSimulation<Config> && RunChildModel<Config> && RunGoals<Config>;

template<typename Config>
struct GoalsSimulation {
  GoalsSimulation(...) {};
};

template<GoalsSimulationEnabled Config>
struct GoalsSimulation<Config> {
  using real_type = typename Config::real_type;
  using ModelVariant = typename Config::ModelVariant;
  using SS = Config::SS;
  using Pars = Config::Pars;
  using State = Config::State;
  using Intermediate = Config::Intermediate;
  using Args = Config::Args;

  // private members of this struct
private:
  // state space
  static constexpr int NS = SS::NS;
  static constexpr int hDS = SS::hDS;
  static constexpr int hTS = SS::hTS;
  static constexpr int hAG = SS::hAG;
  static constexpr auto hAG_span = SS::hAG_span;
  static constexpr int pAG = SS::pAG;
  static constexpr int p_idx_hiv_first_adult = SS::p_idx_hiv_first_adult;
  static constexpr int ex = SS::ex;

  // function args
  int t;
  const Pars& pars;
  const State& state_curr;
  State& state_next;
  Intermediate& intermediate;
  const Options<real_type>& opts;

  // only exposing the constructor and some methods
public:
  GoalsSimulation(Args& args) :
      t(args.t),
      pars(args.pars),
      state_curr(args.state_curr),
      state_next(args.state_next),
      intermediate(args.intermediate),
      opts(args.opts) {};

  void run_goals_simulation() { example_step(); };

  // private methods that we don't want people to call
private:
  void example_step() {
    const auto& p_hv = pars.hv;
    const auto& c_dp = state_curr.dp;
    auto& n_hv = state_next.hv;
    auto& i_hv = intermediate.hv;

    for (int s = 0; s < NS; ++s) {
      for (int a = 0; a < pAG; ++a) {
        i_hv.ex_intermediate(a, s) = 1.0;

        n_hv.ex_output(a, s) = c_dp.p_totpop(a, s) + p_hv.ex_input(a, s);
      }
    }

    for (int e = 0; e < ex; ++e) {
      n_hv.new_output(e) = p_hv.transition_rate(e) + 1;
    }
  };
};

}  // namespace internal
}  // namespace leapfrog
