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
  static constexpr int pRG_TOTAL = SS::pRG_TOTAL;  //Number of risk groups
  static constexpr int pRG_MSM_F3 = SS::pRG_MSM_F3;  //Number of behavior groups
  static constexpr int pDUR_AVG = SS::pDUR_AVG;  //Number of average duration groups

  enum Index {

      //Risk Groups
      RG_ALL = 0,
      RG_None = 1,
      RG_LRH = 2,
      RG_MRH = 3,
      RG_HRH = 4,
      RG_IDU = 5,
      RG_MSM = 6,
      RG_MSMLR = 7,
      RG_MSMMR = 8,
      RG_MSMHR = 9,
      RG_MSMIDU = 10,
      RG_TOTAL = 11,
      RG_NONE_F3 = 12,
      RG_LRH_F3 = 13,
      RG_MRH_F3 = 14,
      RG_HRH_F3 = 15,
      RG_IDU_F3 = 16,
      RG_MSM_F3 = 17,

      //Duration
      DUR_PERC_POP = 1,
      DUR_AVG = 2,
     
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
    for (int r = 0; r < pRG_TOTAL; ++r) {
        n_hv.b_condom_prop_sum += p_hv.b_condom_prop(r, t);// * c_dp.p_totpop(r, s);
    }
    p_hv.b_condom_prop(RG_ALL, t) = n_hv.b_condom_prop_sum;

    //   for (int a = 0; a < pAG; ++a) {
    //     i_hv.ex_intermediate(a, s) = 1.0;

    //     n_hv.ex_output(a, s) = c_dp.p_totpop(a, s) + p_hv.b_condom_prop(a, s);
    //   }
    // }
  };

};

}
}
