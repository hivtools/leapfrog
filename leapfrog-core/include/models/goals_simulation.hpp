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
  static constexpr int pRG_MSM_F3 = SS::pRG_MSM_F3;//Number of behavior groups
  static constexpr int pDUR_AVG = SS::pDUR_AVG;    //Number of average duration groups
  static constexpr int pRG_DUR = SS::pDUR_AVG;    


  enum Index {

      //Sexes
      S_BOTH_SEXES = 0,
      S_MALE = 1,
      S_FEMALE = 2,

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

      //CD4 10 year age bins
      CA_15_24 = 1,
      CA_25_34 = 2,
      CA_35_44 = 3,
      CA_45_54 = 4,

      CD4_NEG = 0,
      CD4_PRIM = 1,
      CD4_GT500 = 2,
      CD4_350_500 = 3,
      CD4_250_349 = 4,
      CD4_200_249 = 5,
      CD4_100_199 = 6,
      CD4_50_99 = 7,
      CD4_LT50 = 8,
      CD4_GT500_ART = 12,
      CD4_350_500_ART = 13,
      CD4_250_349_ART = 14,
      CD4_200_249_ART = 15,
      CD4_100_199_ART = 16,
      CD4_50_99_ART = 17,
      CD4_LT50_ART = 18,
      CD4_ALL_HIV = 19,

     
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

  void run_goals_pre_inner_loop() {
    auto& n_hv = state_next.hv;
    
    nda::fill(n_hv.a_adults, 0.0); //please remove with real model calculations 
    nda::fill(n_hv.c_mu, 1.0); //please remove with real model calculations 
  }

  void run_goals_inner_loop(int hiv_step) {
    auto& n_hv = state_next.hv;
    auto& i_hv = intermediate.hv;
    auto& p_hv = pars.hv;

    for (int sex = 0; sex < SS::NS; ++sex) {
      for (int rg = 0; rg < SS::pRG_TOTAL; ++rg) {
        for (int hiv = 0; hiv < SS::pHIV; ++hiv) {
          for (int vacc = 0; vacc < SS::pVacc; ++vacc) {
            n_hv.a_adults(sex, rg, hiv, vacc) = p_hv.epi_initial_pulse;
          }
        }
      }
    }
  }

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

  void THVProj_Calc_CD4Trans() {
    const auto& p_ha = pars.ha;
    auto& i_hv = intermediate.hv;
    // Mortality by CD4 averaged over age groups
    for (int s = S_MALE; s <= S_FEMALE; ++s) {
        for (int h = CD4_GT500; h <= CD4_LT50; ++h) {
            i_hv.c_mu[h][s] = p_ha.cd4_mortality(h, CA_25_34, s); //HV_GetDPMortByCD4NoART(p, s, HV_DP_CD4_25_34, h);
            i_hv.c_mu[h][s] += p_ha.cd4_nonaids_excess_mort(h, CA_25_34, s); //HV_GetAdultNonAIDSExcessMort(p, s, HV_DP_CD4_25_34, h, DP_NoTreat);

            //if (t > 1) {
            //    _mu[h][s] = std::max(_mu[h][s], _NonAIDSDeathRate[s][t - 1]);
           // }
        }
        //c_mu[CD4_PRIM][s] = c_mu[CD4_GT500][s];
    }

    
}


  


};

}
}
