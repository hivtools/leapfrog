#pragma once

#include "../options.hpp"
#include "../generated/config_mixer.hpp"

namespace leapfrog {
namespace internal {

template<typename Config>
concept GoalsSimulationEnabled = RunDemographicProjection<Config> && RunHivSimulation<Config> && RunChildModel<Config> && RunGoals<Config>;

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
  static constexpr int pRG = SS::pRG;  //Number of risk groups
  static constexpr int pF3 = SS::pF3;  //Number of behavior groups
  static constexpr int pAvgDur = SS::pAvgDur;  //Number of average duration groups

  enum Index {
    //Risk group indices
      AllRisk         = 0,
      None            = 1,
      LRH             = 2,
      MRH             = 3,
      HRH             = 4,
      IDU             = 5,
      MSM             = 6,
      MSMLR           = 7,
      MSMMR           = 8,
      MSMHR           = 9,
      MSMIDU          = 10,
      RG_Total        = 11,   //NOTE:  _Total IS USED IN CALCULATIONS FOR MALE/FEMALE OFFSET
      None_F3         = 12,
      LRH_F3          = 13,
      MRH_F3          = 14,
      HRH_F3          = 15,
      IDU_F3          = 16,
      MSM_F3          = 17,
    //Duration group indices
      PercPop           = 1,
      AvgDur            = 2

  };


  // function args
  int t;
  const Pars& pars;
  const State& state_curr;
  State& state_next;
  Intermediate& intermediate;
  const Options<real_type>& opts;

  // only exposing the constructor and some methods
  public:
  GoalsSimulation(Args& args):
    t(args.t),
    pars(args.pars),
    state_curr(args.state_curr),
    state_next(args.state_next),
    intermediate(args.intermediate),
    opts(args.opts)
  {};

  void run_goals_simulation() {
    example_step();
  };

  // private methods that we don't want people to call
  private:
  void example_step() {
    const auto& p_hv = pars.hv;
    const auto& c_dp = state_curr.dp;
    auto& n_hv = state_next.hv;
    auto& i_hv = intermediate.hv;
    
    //sum the condom percents by year
    n_hv.ex_output = p_hv.epi_initial_pulse;
    n_hv.b_condom_prop_sum = 0;
    for (int r = 0; r < pRG; ++r) {
        n_hv.b_condom_prop_sum += p_hv.b_condom_prop(r, t);// * c_dp.p_totpop(r, s);
    }
    p_hv.b_condom_prop(AllRisk, t) = n_hv.b_condom_prop_sum;

    //   for (int a = 0; a < pAG; ++a) {
    //     i_hv.ex_intermediate(a, s) = 1.0;

    //     n_hv.ex_output(a, s) = c_dp.p_totpop(a, s) + p_hv.b_condom_prop(a, s);
    //   }
    // }
  };

};

}
}
