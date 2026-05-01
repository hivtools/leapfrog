#pragma once

#include "../options.hpp"
#include "../generated/config_mixer.hpp"
#include "../model_debugger.hpp"

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
  static constexpr int nNS = SS::nNS; 
  static constexpr int nRG = SS::nRG; 
  static constexpr int nVAC = SS::nVAC;
  static constexpr int nHIV = SS::nHIV;
  static constexpr int nART = SS::nART;
  static constexpr int nCD4 = SS::nCD4; 
  static constexpr int nCD4p = SS::nCD4p; 
  static constexpr int nCD4a = SS::nCD4a;


  static constexpr int pIDX_24to35 = SS::pIDX_24to35; 
  static constexpr int pIDX_15to49 = SS::pIDX_15to49; 
  static constexpr int pAges5Yrs = SS::pAges5Yrs; 
  static constexpr int rRG_TOTAL = SS::rRG_TOTAL; 
  static constexpr int rRG_MSM_F3 = SS::rRG_MSM_F3; 
  static constexpr int rRG_DUR = SS::rRG_DUR; 
  static constexpr int vVAC_NO_PROT = SS::vVAC_NO_PROT; 
  static constexpr int vVAC_NUM_PARS = SS::vVAC_NUM_PARS; 
  static constexpr int vVAC_NUM_EFFECTS = SS::vVAC_NUM_EFFECTS; 
  static constexpr int hDS = SS::hDS; 
  static constexpr int hTS = SS::hTS;
  static constexpr int hCD4_ALL_HIV = SS::hCD4_ALL_HIV;
  static constexpr int hCD4_LT50 = SS::hCD4_LT50;
  static constexpr int hHIV_Cats = SS::hHIV_Cats; 

/* 
     "pNumSexes": 2,
      "pIDX_24to35": 2,
      "pIDX_15to49": 15,
      "pAges5Yrs": 17,
      "rRG_TOTAL": 11,
      "rRG_MSM_F3": 18,
      "rRG_DUR": 2,
      "vVAC_NO_PROT": 4,
      "hDS": 7,
      "hTS": 3,
      "hCD4_ALL_HIV": 17,
      "hCD4_LT50": 7,
      "hHIV_Cats": 5
      
      */
  

  enum Index {

      //Sexes
      S_MALE = 0,
      S_FEMALE = 1,
      S_ALL = 2,

      //Risk Groups
      RG_NONE = 0,
      RG_LRH = 1,
      RG_MRH = 2,
      RG_HRH = 3,
      RG_IDU = 4,
      RG_MSM = 5,
      RG_TOTAL1 = 5,
      RG_MSMLR = 6,
      RG_MSMMR = 7,
      RG_MSMHR = 8,
      RG_MSMIDU = 9,
      RG_TOTAL = 10,
      RG_NONE_F3 = 11,
      RG_LRH_F3 = 12,
      RG_MRH_F3 = 13,
      RG_HRH_F3 = 14,
      RG_IDU_F3 = 15,
      RG_MSM_F3 = 16,
      RG_ALL = 17,

      //Duration
      PERC_POP = 0,
      DUR_AVG = 1,

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
      CD4_GT500_ART = 9,
      CD4_350_500_ART = 10,
      CD4_250_349_ART = 11,
      CD4_200_249_ART = 12,
      CD4_100_199_ART = 13,
      CD4_50_99_ART = 14,
      CD4_LT50_ART = 15,
      CD4_ALL = 16,
    
      POP_H_HIVNeg     = 0,
      POP_H_NoART      = 1,
      POP_H_ARTlt6m    = 2,
      POP_H_ART6to12m  = 3,
      POP_H_ARTgt12m   = 4,
      POP_H_OnART      = 5,
      POP_H_ALL        = 6,

      VAC_UNV           = 0,
      VAC_TAKE          = 1,
      VAC_PARTIAL       = 2,
      VAC_NO_PROT       = 3,
      VAC_ALL           = 4,

      VAC_EFF               = 0,
      VAC_INF               = 1,
      VAC_PROG              = 2,
      VAC_DUR               = 3,
      VAC_TYPE              = 4, 

      VAC_TAKEACTION        = 0,
      VAC_DEGREEACTION      = 1,

      VAC_COV_SINGLE        = 0,
      VAC_COV_ALLRISK       = 1,

      ART_NUM_PERCENT       =0,
      ART_CD4_PERCENT       =1,
      ART_CD4_NUMBER        =2,
      ART_NEW_PATS          =3,
      ART_RG_PERCENT        =4,
     
  };

  //st atic constexpr int MALE = SS::MALE;
  //static constexpr int FEMALE = SS::FEMALE;


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
    const auto& c_dp = state_curr.dp;
    
    auto& n_hv = state_next.hv;
    auto dbg_model = capture_model(state_next, intermediate, pars);

    n_hv.total_population += t; //c_dp.p_totpop(20,S_MALE);

    nda_print_info(dbg_model.dp.p_totpop);
    
    //example_step();
  };

  void run_goals_pre_hiv_loop() {

    //from goals
    auto& p_hv = pars.hv;

    int proj_start_year = opts.proj_start_year;

    //initilize adult population
    if(t==1){
      int a=1;
      set_riskgroup_proportions();
      set_initial_pop();
    }

    //at hiv first year, apply initial pulse, t starts at 0
    //if(t==(p_hv.epi_start_year-proj_start_year)){
    if(t==1){
      int a=1;
      set_initial_pulse();
    }

    //calc new vaccinations
    calc_new_vaccinations();

    
    int a=1;
    //auto dbg_model = capture_model(state_next, intermediate, pars);
    //nda_print_info(dbg_model.hv.adults);

  }

   void run_goals_hiv_loop(int hiv_step) {
    
    //collect info from dp/aim to set demographical and HIV rates
    int a=1;
    set_goals_vars_from_dp(t);
    
    //set these rates to vars in goals
    calc_goals_rates(t);

    //adjust distribution of new entrants into different risk groups
    calc_newrecruits_distribution(t);
    
    //progress, hiv-neg, not at risk (RG_NONE)
    progress_norisk_hiv_neg(t);

    //progress, hiv-neg, at risk (RG_LRH..RG_MSM)
    //progress_atrisk_hiv_neg(t);

    //progress, hiv-neg, hiv-pos and hiv-art (RG_LRH..RG_MSM)
    progress_hivn_hivp_art(t);

    //ART allocation
    allocate_art(t);
    
  }

  void run_goals_post_hiv_loop() {

    sum_adult_pop_dims(t);

  }


//pre inner loop functions
 void set_riskgroup_proportions() {

    const auto& p_hv = pars.hv;
    auto& i_hv = intermediate.hv; 

    nda::fill(i_hv.riskgroup_proportions, 0.0);//risk group proportions
    nda::fill(i_hv.behave_change_rate, 0.0);//risk group proportions

    //risk group proportions, and behaviur change rates
    for (int rg = RG_NONE; rg <= RG_TOTAL1; ++rg) {

      i_hv.riskgroup_proportions(rg,S_MALE) = p_hv.b_behav_dur(rg, PERC_POP) / 100.0;
      if (rg > RG_LRH) i_hv.behave_change_rate(rg,S_MALE) = (p_hv.b_behav_dur(rg, DUR_AVG)!=0) ? 1 / p_hv.b_behav_dur(rg, DUR_AVG) : 0;
      
      if (rg != RG_MSM) {
        i_hv.riskgroup_proportions(rg,S_FEMALE) = p_hv.b_behav_dur(rg, PERC_POP) / 100.0;
        if (rg > RG_LRH) i_hv.behave_change_rate(rg,S_FEMALE) = (p_hv.b_behav_dur(rg, DUR_AVG)!=0) ? 1 / p_hv.b_behav_dur(rg, DUR_AVG) : 0;
      }

    }

    //auto dbg_model = capture_model(state_next, intermediate, pars);
    //nda_print_info(dbg_model.hv.riskgroup_proportions);


}  

void set_initial_pop() {

  //dp
  const auto& c_dp = state_curr.dp;

  //goals
  auto& n_hv = state_next.hv;
  auto& i_hv = intermediate.hv;
      
  nda::fill(i_hv.pop_1549, 0.0);

  for (int s = S_MALE; s <= S_FEMALE; ++s) {
    for(int a = SS::pIDX_15to49; a < SS::pIDX_15to49 + SS::pAG_15to49; ++a) {

      i_hv.totpop_1549(s) += c_dp.p_totpop(a, s);

    }

    for (int rg = RG_NONE; rg <= RG_TOTAL1; ++rg) {

      n_hv.adults(VAC_UNV,CD4_NEG,rg,s)=1000+s+rg;//i_hv.riskgroup_proportions(rg,s)*i_hv.totpop_1549(s);

    }
  }  

}


  void set_initial_pulse() {
   
    //from dp/aim
    const auto& p_ha = pars.ha;

    //from goals
    auto& n_hv = state_next.hv;
    auto& i_hv = intermediate.hv;
    auto& p_hv = pars.hv;
    
    real_type pulse =0;
    real_type distr =0;

    for (int s = S_MALE; s <= S_FEMALE; ++s) { 

      for (int rg = RG_NONE; rg <= RG_TOTAL1; ++rg) {

        pulse = p_hv.epi_initial_pulse * n_hv.adults(VAC_UNV,CD4_NEG,rg,s);

        if (rg==RG_MRH){
          pulse = 3/5*pulse;
        }
        
        if (rg==RG_LRH){
          pulse = 1/5*pulse;
        }  

        if (rg==RG_NONE || rg==RG_IDU) {  
          pulse = 0;
        }  
        if (rg==S_FEMALE && rg==RG_MSM) {   
          pulse = 0;
        }


        for (int hd = CD4_PRIM; hd <= CD4_LT50; ++hd) {

          if(hd==0){
            distr  = p_ha.cd4_initial_distribution(CD4_GT500, pIDX_15to49, s);
          }
          else{
            distr  = p_ha.cd4_initial_distribution(hd, pIDX_15to49, s);
          }

          n_hv.adults(VAC_UNV,hd,rg,s)  = n_hv.adults(VAC_UNV,hd,rg,s) + pulse*distr;
          n_hv.adults(VAC_UNV,CD4_NEG,rg,s) = n_hv.adults(VAC_UNV,CD4_NEG,rg,s) - pulse*distr;

        }

    }

  }

 }

void calc_new_vaccinations()
{
  auto& n_hv = state_next.hv;
  auto& i_hv = intermediate.hv;
  auto& p_hv = pars.hv;

  nda::fill(i_hv.new_vaccinations, 0.0);
  nda::fill(i_hv.vac_effect, 0.0);

  //real_type dt = 1/opts.hts_per_year;

  //vac effect
  i_hv.vac_effect(VAC_TAKEACTION,VAC_TAKE)       = p_hv.rn_vac_params(VAC_EFF)/100;
  i_hv.vac_effect(VAC_TAKEACTION,VAC_NO_PROT)    = p_hv.rn_vac_params(VAC_EFF)/100;
  i_hv.vac_effect(VAC_DEGREEACTION,VAC_PARTIAL)  = 1;

   real_type value = 0;
   for (int s = S_MALE; s <= S_FEMALE; ++s)
    {
        for (int rg = RG_NONE; rg <= RG_TOTAL1; ++rg) 
        {

          if (s == S_FEMALE && rg > RG_IDU) continue; //no female MSM
        
          int h1 = CD4_LT50_ART;                     
          if (p_hv.rn_vac_targetting == 1) h1 = CD4_NEG;
          
          for (int hd = CD4_NEG; hd <= h1; ++hd) {
          
              int nr = RG_TOTAL1;
              // Determine the risk index (nr) used for coverage lookup
              if (p_hv.rn_vac_cov_type != VAC_COV_SINGLE){
                nr = RG_TOTAL1;
              }
                else {
                nr = rg;
              }

              value =  p_hv.rn_vac_coverage(nr,t)/100 * //dt *
                          (n_hv.adults(VAC_ALL,hd,rg,s)  +
                          i_hv.entrants_age_15(POP_H_HIVNeg,CD4_NEG,s) *
                          n_hv.adults(VAC_ALL,hd,rg,s)  / n_hv.adults(VAC_ALL,CD4_ALL,rg,s))-
                          (n_hv.adults(VAC_TAKE,hd,rg,s) +
                          n_hv.adults(VAC_PARTIAL,hd,rg,s) +
                          n_hv.adults(VAC_NO_PROT,hd,rg,s) ) * (1 - (1 / p_hv.rn_vac_params(VAC_DUR)));

              if(value<0) value=0;                 
              i_hv.new_vaccinations(rg,hd,s)+=value;

            }
    

      }//rg

    } //s 
      

}


//inner loop functions
  void set_goals_vars_from_dp(int t) {
    //dp
    const auto& c_dp = state_curr.dp;
    auto& i_dp = intermediate.dp;
  

    //aim
    const auto& c_ha = state_curr.ha;
    const auto& p_ha = pars.ha;
    
    //goals
    auto& i_hv = intermediate.hv;
     
    //vars mapped from DP/AIM
    nda::fill(i_hv.totpop_deaths_background, 0.0);//dp background deaths numerator
    nda::fill(i_hv.totpop_1549, 0.0);//dp background deaths denominator
    
    nda::fill(i_hv.pop_1549, 0.0);//denominator for background mortality, check age index (a-1)

    nda::fill(i_hv.pop_1549_hiv, 0.0);//denominator for goals mu
    nda::fill(i_hv.pop_1549_art, 0.0);//denominator for goals alpha
    
    nda::fill(i_hv.hiv_cd4_mort_no_art, 0.0);//numerator for  mu
    nda::fill(i_hv.hiv_cd4_mort_art, 0.0);//numerator for alphda
    nda::fill(i_hv.hiv_cd4_progression, 0.0);//numerator for lambda

    
    nda::fill(i_hv.pop_sex_age_hiv, 0.0);//used for ART allocation in goals
    nda::fill(i_hv.entrants_age_15, 0.0);//numerator for 15 yr old entrants into goals
    nda::fill(i_hv.aging_50, 0.0);//numerator for aging rate in goals, 50 yrs
    nda::fill(i_hv.aging_denom_1549, 0.0);//denominator for aging rate in goals

    nda::fill(i_hv.migration_num, 0.0);//numerator for avg migration rate
    nda::fill(i_hv.migration_denom, 0.0);//denominaor for avg migration rate

  
    for (int s = S_MALE; s <= S_FEMALE; ++s) {
      
     for(int a = SS::pIDX_15to49; a < SS::pIDX_15to49 + SS::pAG_15to49; ++a) {
     
      i_hv.totpop_deaths_background(s) += c_dp.p_deaths_background_totpop(a, s);
      i_hv.totpop_1549(s) += c_dp.p_totpop(a - 1, s);

      i_hv.migration_num(s) += c_dp.p_totpop(a, s) * i_dp.migration_rate(a, s);
      i_hv.migration_denom(s) += c_dp.p_totpop(a, s);
      
      i_hv.pop_1549(s) += c_dp.p_totpop(a, s);
      i_hv.aging_denom_1549(POP_H_HIVNeg, CD4_NEG, s) += c_dp.p_totpop(a, s);
      if(a==SS::pIDX_15to49){
          i_hv.entrants_age_15(POP_H_HIVNeg, CD4_NEG, s) += c_dp.p_totpop(a, s);
        }
        
        if(a==SS::pIDX_15to49 + SS::pAG_15to49){
          i_hv.aging_50(POP_H_HIVNeg, CD4_NEG, s) += c_dp.p_totpop(a, s);
        }

      for (int hd = CD4_GT500; hd <= CD4_LT50; ++hd) {
  
          i_hv.pop_1549_hiv(hd,s) += c_ha.h_hivpop(hd, a, s);

          i_hv.pop_sex_age_hiv(POP_H_NoART, s) += c_ha.h_hivpop(hd, a, s);
          i_hv.aging_denom_1549(POP_H_NoART, hd, s) += c_ha.h_hivpop(hd, a, s);
          i_hv.aging_denom_1549(POP_H_HIVNeg, CD4_NEG, s) -= c_ha.h_hivpop(hd, a, s);//remove hiv states
          
          //i_hv.hiv_mu(hd,s) +=  (p_ha.cd4_mortality(hd, a, s)+p_ha.cd4_nonaids_excess_mort(hd, a, s)) * c_ha.h_hivpop(hd, a, s);
        
          if(a==SS::pIDX_15to49){
            i_hv.entrants_age_15(POP_H_NoART, hd, s) += c_ha.h_hivpop(hd, a, s);
            i_hv.entrants_age_15(POP_H_HIVNeg, CD4_NEG, s) -= c_ha.h_hivpop(hd, a, s);
          }
          
          if(a==SS::pIDX_15to49 + SS::pAG_15to49){
            i_hv.aging_50(POP_H_NoART, hd, s) += c_ha.h_hivpop(hd, a, s);
            i_hv.aging_50(POP_H_HIVNeg, CD4_NEG, s) -= c_ha.h_hivpop(hd, a, s);
          }

          i_hv.hiv_cd4_mort_no_art(hd,s) += c_ha.h_hiv_deaths_no_art(hd, a, s);
          if(hd>1){
            i_hv.hiv_cd4_progression(hd-1, s) += p_ha.cd4_progression(hd - 1, a, s) * c_ha.h_hivpop(hd - 1, a, s);
          }

          for (int ht = 0; ht <= nART; ++ht) {
            
            i_hv.pop_1549_art (hd,s) += c_ha.h_artpop(ht, hd, a, s);
            
            i_hv.pop_sex_age_hiv(POP_H_ARTlt6m+ht, s) += c_ha.h_artpop(ht, hd, a, s);
            i_hv.pop_sex_age_hiv(POP_H_OnART ,s) += c_ha.h_artpop(ht, hd, a, s);
            i_hv.aging_denom_1549(POP_H_ARTlt6m+ht, hd, s) += c_ha.h_artpop(ht, hd, a, s);
            i_hv.aging_denom_1549(POP_H_HIVNeg, CD4_NEG, s) -= c_ha.h_artpop(ht, hd, a, s);//remove art states

            //CDP: using an average rate. review
            //i_hv.art_alpha(hd,s) +=  (p_ha.art_mortality(ht, hd, a, s)+p_ha.art_nonaids_excess_mort(ht, hd, a, s)) * c_ha.h_artpop(ht, hd, a, s);

            if(a==SS::pIDX_15to49){
              i_hv.entrants_age_15(POP_H_ARTlt6m+ht, hd, s) += c_ha.h_artpop(ht, hd, a, s);
              i_hv.entrants_age_15(POP_H_HIVNeg, CD4_NEG, s) -= c_ha.h_artpop(ht, hd, a, s);
            }

            if(a==SS::pIDX_15to49 + SS::pAG_15to49){
              i_hv.aging_50(POP_H_ARTlt6m+ht, hd, s) += c_ha.h_artpop(ht, hd, a, s);
              i_hv.aging_50(POP_H_HIVNeg, CD4_NEG, s) -= c_ha.h_artpop(ht, hd, a, s);
            }

             i_hv.hiv_cd4_mort_art(hd, s) = c_ha.h_hiv_deaths_art(ht, hd, a, s);

          }//t            
          
        }//h

    }//a

  }//s


}



void calc_goals_rates(int t) {

  const auto& p_hv = pars.hv;
  auto& i_hv = intermediate.hv; 
  
  real_type denominator = 0.0;
  real_type numerator = 0.0;

  //demographical rates
  nda::fill(i_hv.background_death_rate, 0.0);//dp total pop 1549
  nda::fill(i_hv.rate_aging_50, 0.0);//mort rate, hiv on ART
  nda::fill(i_hv.migration_rate, 0.0);//migration rate
  

  //rates for HIV dynamics
  nda::fill(i_hv.hiv_mu, 0.0);//mort rate, hiv not on ART
  nda::fill(i_hv.hiv_lambda, 0.0);//progression rate, hiv not on ART
  nda::fill(i_hv.art_alpha, 0.0);//mort rate, hiv on ART

  //aggregate rates
  nda::fill(i_hv.hiv_exit_rates, 0.0);//total exit rate, hiv not on ART
  nda::fill(i_hv.art_exit_rates, 0.0);//total exit rate, hiv on ART  
  nda::fill(i_hv.hiv_stage_progressors, 0.0);//progression rate, hiv not on ART

  real_type years_in_primary=p_hv.epi_months_in_primary/12;

  for (int s = S_MALE; s <= S_FEMALE; ++s) { 
    
        //demographical rate
        i_hv.background_death_rate(s) = (i_hv.totpop_1549(s)!=0) ? i_hv.totpop_deaths_background(s)/i_hv.totpop_1549(s) : 0;

        //migration rate
        i_hv.migration_rate(s) = (i_hv.migration_denom(s) !=0) ? i_hv.migration_num(s)/i_hv.migration_denom(s) : 0;
     
        //set aging rates, out of 15-49 year old population 
        i_hv.rate_aging_50(POP_H_HIVNeg, CD4_NEG, s) = (i_hv.aging_denom_1549(POP_H_HIVNeg, CD4_NEG, s) !=0) ? i_hv.aging_50(POP_H_HIVNeg, CD4_NEG, s)/i_hv.aging_denom_1549(POP_H_HIVNeg, CD4_NEG, s) : 0; 

        //cd4 transition rate for primary stage 
        i_hv.hiv_lambda(CD4_PRIM,s) = (years_in_primary!=0) ? 1/years_in_primary : 0;
       
        for (int hd = CD4_GT500; hd <= CD4_LT50; ++hd) {

          //hiv dynamics: mortality and progression rates
          i_hv.hiv_mu(hd,s) = (i_hv.pop_1549_hiv(hd,s)!=0) ? i_hv.hiv_cd4_mort_no_art(hd,s)/i_hv.pop_1549_hiv(hd,s) : 0;
          i_hv.hiv_lambda(hd,s) = (i_hv.pop_1549_hiv(hd,s)!=0) ? i_hv.hiv_cd4_progression(hd,s)/i_hv.pop_1549_hiv(hd,s) : 0;
          i_hv.art_alpha(hd,s) = (i_hv.pop_1549_art(hd,s)!=0) ? i_hv.hiv_cd4_mort_art(hd,s)/i_hv.pop_1549_art(hd,s) : 0;
          
          if(hd==CD4_GT500){
            real_type stage_duration = 1.0 / i_hv.hiv_lambda(CD4_GT500,s)  - years_in_primary;
            i_hv.hiv_lambda(CD4_GT500,s) = 1-exp(-1/stage_duration);//remove time in primary stage
            i_hv.hiv_mu(CD4_PRIM,s) = i_hv.hiv_mu(CD4_GT500,s);
          } 
          if(hd==CD4_LT50) i_hv.hiv_lambda(hd,s) = 0;
          
          i_hv.rate_aging_50(POP_H_NoART, CD4_NEG, s) = (i_hv.aging_denom_1549(POP_H_NoART, CD4_NEG, s) !=0) ? i_hv.aging_50(POP_H_NoART, CD4_NEG, s)/i_hv.aging_denom_1549(POP_H_NoART, CD4_NEG, s) : 0; 
      
          denominator = 0.0;
          numerator = 0.0;
          for (int ht = CD4_GT500; ht <= CD4_LT50; ++ht) {
            numerator +=   i_hv.aging_50(POP_H_ARTlt6m+ht, hd, s);              
            denominator += i_hv.aging_denom_1549(POP_H_ARTlt6m+ht, hd, s);
          }
          i_hv.rate_aging_50(POP_H_OnART, hd, s) = (denominator !=0) ? numerator/denominator : 0;

      }


      //aggregate exit rates  
      for (int hd = CD4_GT500; hd < CD4_LT50; ++hd) {

        for (int rg = RG_NONE; rg <= RG_TOTAL; ++rg) {
            i_hv.hiv_exit_rates(rg,hd,s) = i_hv.background_death_rate(s)+
                                        i_hv.hiv_mu(hd,s)+
                                        (p_hv.b_behav_dur(rg,DUR_AVG)>0) ? (1 /p_hv.b_behav_dur(rg,DUR_AVG)) : 0 +
                                        i_hv.rate_aging_50(POP_H_NoART, hd, s);

            i_hv.art_exit_rates(rg,hd,s) = i_hv.background_death_rate(s)+
                                        i_hv.art_alpha(hd,s)+
                                        (p_hv.b_behav_dur(rg,DUR_AVG)>0) ? (1 /p_hv.b_behav_dur(rg,DUR_AVG)) : 0 +
                                        i_hv.rate_aging_50(POP_H_OnART, hd, s);  
        }                          
                                        
        }


      }

      //risk group proportions, and behaviur change rates
      for (int rg = RG_NONE; rg <= RG_TOTAL1; ++rg) {

        i_hv.riskgroup_proportions(rg,S_MALE) = p_hv.b_behav_dur(rg, PERC_POP) / 100.0;
        if (rg > RG_LRH) i_hv.behave_change_rate(rg,S_MALE) = (p_hv.b_behav_dur(rg, DUR_AVG)!=0) ? 1 / p_hv.b_behav_dur(rg, DUR_AVG) : 0;
        
        if (rg != RG_MSM) {
          i_hv.riskgroup_proportions(rg,S_FEMALE) = p_hv.b_behav_dur(rg+RG_NONE_F3, PERC_POP) / 100.0;
          if (rg > RG_LRH) i_hv.behave_change_rate(rg,S_FEMALE) = (p_hv.b_behav_dur(rg+RG_NONE_F3, DUR_AVG)!=0) ? 1 / p_hv.b_behav_dur(rg, DUR_AVG) : 0;
        }

      }


}

void calc_newrecruits_distribution(int t)
{
  auto& n_hv = state_next.hv;
  auto& i_hv = intermediate.hv;
  auto& p_hv = pars.hv;

  real_type value=0;
  real_type rg_sum=0;

   for (int s = S_MALE; s <= S_FEMALE; ++s)
   {

    rg_sum = 0;
    for (int rg = RG_LRH; rg <= RG_TOTAL1; ++rg)
    {
        if (s == S_FEMALE && rg > RG_IDU) continue; 

        if(i_hv.riskgroup_proportions(rg,s)-
            n_hv.adults(VAC_ALL,CD4_ALL,rg,s)/n_hv.adults(VAC_ALL,CD4_ALL,rg,s) != 0)
        {
            if ( n_hv.adults(VAC_ALL,CD4_ALL,rg,s) == 0.0 ||
                i_hv.behave_change_rate(rg,s)== 0.0 ||
                n_hv.adults(VAC_ALL,CD4_ALL,rg,s) == 0.0)
            {
                value = 0.0;
            }
            else
            {
                value = i_hv.riskgroup_proportions(rg,s) +
                        i_hv.riskgroup_proportions(rg,s) -
                    (1-i_hv.behave_change_rate(rg,s))*
                    n_hv.adults(VAC_ALL,CD4_ALL,rg,s)/
                    n_hv.adults(VAC_ALL,CD4_ALL,RG_ALL,s)  *
                    p_hv.b_incr_recruit(s,rg)/100;
            }

            if(value<0) value=0;
            rg_sum += value;

            i_hv.riskgroup_proportions(rg,s)=value;
        }  

    }//rg 

    //normalize
    for (int rg = RG_LRH; rg <= RG_TOTAL1; ++rg)
    {
        if (s == S_FEMALE && rg > RG_IDU) continue; 
        i_hv.riskgroup_proportions(rg,s)/=rg_sum;
    }

   }//s
   
}



void progress_norisk_hiv_neg(int t)
{

    auto& n_hv = state_next.hv;
    auto& i_hv = intermediate.hv;
    auto& p_hv = pars.hv;

    real_type dt = 1/opts.hts_per_year;
    real_type value = 0;
    real_type temp1 = 0;
    real_type temp2 = 0;
    nda::fill(i_hv.new_vaccinations, 0.0);
    nda::fill(i_hv.vac_params, 0.0);

    //unvaccinated
    for (int s = S_MALE; s <= S_FEMALE; ++s)
    {
     
        temp1=n_hv.adults(VAC_UNV,CD4_NEG,RG_NONE,s);
        temp2=n_hv.adults(VAC_UNV,CD4_ALL,RG_NONE,s);

        value = 
        n_hv.adults(VAC_UNV,CD4_NEG,RG_NONE,s) + dt*(
        //new entrants 15 yrs , note that they are not vaccinated by assumption
        i_hv.entrants_age_15(POP_H_HIVNeg,CD4_NEG,s) -
        //exits and migration
        n_hv.adults(VAC_UNV,CD4_NEG,RG_NONE,s) * (
        (std::max(p_hv.b_age_first_sex(s,t) - 15.0, 1.0)!=0)? 1/std::max(p_hv.b_age_first_sex(s,t) - 15.0, 1.0) : 0 +
        i_hv.background_death_rate(s) + 
        i_hv.rate_aging_50(POP_H_HIVNeg,CD4_NEG,s) - 
        i_hv.migration_rate(s) ) -

        //new vaccinations
        i_hv.new_vaccinations(RG_NONE,CD4_NEG,s) + // *
        //n_hv.adults(VAC_UNV,CD4_NEG,RG_NONE,s) *
        //(n_hv.adults(VAC_UNV,CD4_ALL,RG_NONE,s)!=0)? 1/ n_hv.adults(VAC_UNV,CD4_ALL,RG_NONE,s) : 0 +
      
        //vaccine waning, entrants
        (n_hv.adults(VAC_TAKE,CD4_NEG,RG_NONE,s) +
          n_hv.adults(VAC_PARTIAL,CD4_NEG,RG_NONE,s) +
          n_hv.adults(VAC_NO_PROT,CD4_NEG,RG_NONE,s)) *
        (i_hv.vac_params(VAC_DUR)!=0)? 1 / i_hv.vac_params(VAC_DUR) : 0  );

        if(value<0) value=0;
        n_hv.adults(VAC_UNV,CD4_NEG,RG_NONE,s) = value;

        //vaccinated
        for (int v = VAC_TAKE; v <= VAC_NO_PROT; ++v)
        {
              value = 
              n_hv.adults(v,CD4_NEG,RG_NONE,s) + dt*( -
              //exits and migration
              n_hv.adults(v,CD4_NEG,RG_NONE,s) * (
              (std::max(p_hv.b_age_first_sex(s,t) - 15.0, 1.0)!=0)? 1/std::max(p_hv.b_age_first_sex(s,t) - 15.0, 1.0) : 0 +
              i_hv.background_death_rate(s) + 
              i_hv.rate_aging_50(POP_H_HIVNeg,CD4_NEG,s) - 
              i_hv.migration_rate(s) ) + 

              //new vaccinations
              i_hv.new_vaccinations(RG_NONE,CD4_NEG, s) * i_hv.vac_effect(p_hv.rn_vac_targetting,v) -
               - // *
              //temp1 * (temp2!=0)? 1 / temp2 : 0 -
            
              //vaccine, exits
              n_hv.adults(v,CD4_NEG,RG_NONE,s)*
              (i_hv.vac_params(VAC_DUR)!=0)? 1 / i_hv.vac_params(VAC_DUR) : 0  );

              if(value<0) value=0;
              n_hv.adults(v,CD4_NEG,RG_NONE,s)=value;
           
        }//v

    }//s
}

void progress_atrisk_hiv_neg(int t)
{

    auto& n_hv = state_next.hv;
    auto& i_hv = intermediate.hv;
    auto& p_hv = pars.hv;

    real_type dt = 1/opts.hts_per_year;
    real_type value = 0;
    real_type temp1 = 0;
    real_type temp2 = 0;
    nda::fill(i_hv.new_vaccinations, 0.0);
    nda::fill(i_hv.vac_params, 0.0);

    //unvaccinated
    for (int s = S_MALE; s <= S_FEMALE; ++s)
    {
     
        for (int rg = RG_LRH; rg <= RG_TOTAL1; ++rg)
        { 
          
          if (s == S_FEMALE && rg > RG_IDU) continue; 
          
          temp1=n_hv.adults(VAC_UNV,CD4_NEG,rg,s);
          temp2=n_hv.adults(VAC_UNV,CD4_ALL,rg,s);

          value = 
          n_hv.adults(VAC_UNV,CD4_NEG,rg,s) + dt*(
          
           //no risk at sexual debut
           n_hv.adults(VAC_UNV,CD4_NEG,RG_NONE,s) *
           (std::max(p_hv.b_age_first_sex(s,t) - 15.0, 1.0)!=0)? 1/std::max(p_hv.b_age_first_sex(s,t) - 15.0, 1.0) : 0 *
           i_hv.riskgroup_proportions(rg,s) -
           
          //exits and migration
          n_hv.adults(VAC_UNV,CD4_NEG,rg,s) * (
          i_hv.background_death_rate(s) + 
          i_hv.rate_aging_50(POP_H_HIVNeg,CD4_NEG,s) +
          i_hv.behave_change_rate(rg,s) - 
          i_hv.migration_rate(s) ) -

          //new vaccinations
          i_hv.new_vaccinations(rg,CD4_NEG,s) + // *
          //n_hv.adults(VAC_UNV,CD4_NEG,rg,s) *
          //(n_hv.adults(VAC_UNV,CD4_ALL,rg,s)!=0)? 1/ n_hv.adults(VAC_UNV,CD4_ALL,rg,s) : 0 +
        
          //vaccine waning, entrants
          (n_hv.adults(VAC_TAKE,CD4_NEG,rg,s) +
            n_hv.adults(VAC_PARTIAL,CD4_NEG,rg,s) +
            n_hv.adults(VAC_NO_PROT,CD4_NEG,rg,s)) *
          (i_hv.vac_params(VAC_DUR)!=0)? 1 / i_hv.vac_params(VAC_DUR) : 0 +  
        
          //entrants following behavior change
          n_hv.adults(VAC_UNV,CD4_NEG,rg-1,s) * i_hv.behave_change_rate(rg-1,s) );

          if(value<0) value=0;
          n_hv.adults(VAC_UNV,CD4_NEG,RG_NONE,s) = value;

          //vaccinated
          for (int v = VAC_TAKE; v <= VAC_NO_PROT; ++v)
          {
                value = 
                n_hv.adults(v,CD4_NEG,rg,s) + dt*( -
                //exits and migration
                n_hv.adults(v,CD4_NEG,rg,s) * (
                i_hv.background_death_rate(s) + 
                i_hv.rate_aging_50(POP_H_HIVNeg,CD4_NEG,s) -
                i_hv.behave_change_rate(rg,s) - 
                i_hv.migration_rate(s) ) -

                //new vaccinations
                i_hv.new_vaccinations(rg,CD4_NEG,s) * i_hv.vac_effect(p_hv.rn_vac_targetting,v) - // *
                //temp1 * (temp2!=0)? 1 / temp2 : 0 -
              
                //vaccine, exits
                n_hv.adults(v,CD4_NEG,rg,s)*
                (i_hv.vac_params(VAC_DUR)!=0)? 1 / i_hv.vac_params(VAC_DUR) : 0  +

                //entrants following behavior change
                n_hv.adults(VAC_UNV,CD4_NEG,rg-1,s) * i_hv.behave_change_rate(rg-1,s) ); 

                if(value<0) value=0;
                n_hv.adults(v,CD4_NEG,rg,s)=value;
            
          }//v

      }//rg

    }//s
}

void progress_hivn_hivp_art(int t)
{
    //from goals
    auto& n_hv = state_next.hv;
    auto& i_hv = intermediate.hv;
    auto& p_hv = pars.hv;

    real_type dt = 1/opts.hts_per_year;
    real_type value = 0;
    real_type temp1 = 0;
    real_type temp2 = 0;
    nda::fill(i_hv.new_vaccinations, 0.0);
    nda::fill(i_hv.vac_params, 0.0);

    //unvaccinated
    for (int s = S_MALE; s <= S_FEMALE; ++s)
    {
     
        for (int rg = RG_LRH; rg <= RG_TOTAL1; ++rg)
        { 


        for (int hd = CD4_PRIM; hd <= CD4_LT50_ART; ++hd) 
        {  
          
          if (s == S_FEMALE && rg > RG_IDU) continue;

          //Mortality 
          //hiv-pos or hiv-art mortality rate
          real_type mort_hiv = 0;
          if (CD4_PRIM <= hd && hd <= CD4_LT50) {
            mort_hiv = i_hv.hiv_mu(hd,s);
          }
          else {
            mort_hiv =  i_hv.art_alpha(hd,s); 
          }; 

          //Aging out rate
          real_type rate_aging_out = 0;
          if(hd==CD4_NEG){
            rate_aging_out = i_hv.rate_aging_50(POP_H_HIVNeg,CD4_NEG,s);
          }
          else if (CD4_PRIM <= hd && hd <= CD4_LT50) {
            rate_aging_out = i_hv.rate_aging_50(POP_H_NoART,hd,s);
          }
          else {
            rate_aging_out = i_hv.rate_aging_50(POP_H_OnART,hd,s);
          }; 

          //Progression rate
          //hiv-pos cd 4 progression rate, not progression on art
          real_type progress_out = 0;
          if (CD4_PRIM <= hd && hd <= CD4_LT50) {
            progress_out = i_hv.hiv_lambda(hd,s);
          };

          real_type progress_in = 0;
          if (CD4_GT500 <= hd && hd <= CD4_LT50) {
            progress_in = i_hv.hiv_lambda(hd-1,s);
          };

          //temp1=n_hv.adults(VAC_UNV,CD4_NEG,rg,s);
          //temp2=n_hv.adults(VAC_UNV,CD4_ALL,rg,s);

          value = 
          n_hv.adults(VAC_UNV,hd,rg,s) + dt*(
          
          //no risk at sexual debut
           n_hv.adults(VAC_UNV,hd,RG_NONE,s) *
           (std::max(p_hv.b_age_first_sex(s,t) - 15.0, 1.0)!=0)? 1/std::max(p_hv.b_age_first_sex(s,t) - 15.0, 1.0) : 0 *
           i_hv.riskgroup_proportions(rg,s) -
           
          //exits and migration
          n_hv.adults(VAC_UNV,hd,rg,s) * (
          i_hv.background_death_rate(s) + 
          mort_hiv + //hiv mortality rate
          progress_out + //hiv progrssion rate 
          rate_aging_out + // aging out at age 50
          i_hv.behave_change_rate(rg,s) - 
          i_hv.migration_rate(s) ) -

          //new vaccinations
          i_hv.new_vaccinations(rg,hd,s) + //*
          //n_hv.adults(VAC_UNV,CD4_NEG,rg,s) *
         // (n_hv.adults(VAC_UNV,CD4_ALL,rg,s)!=0)? 1/ n_hv.adults(VAC_UNV,CD4_ALL,rg,s) : 0 +
        
          //vaccine waning, entrants
          (n_hv.adults(VAC_TAKE,hd,rg,s) +
            n_hv.adults(VAC_PARTIAL,hd,rg,s) +
            n_hv.adults(VAC_NO_PROT,hd,rg,s)) *
          (i_hv.vac_params(VAC_DUR)!=0)? 1 / i_hv.vac_params(VAC_DUR) : 0 +  
        
          //entrants following behavior change
          n_hv.adults(VAC_UNV,hd,rg-1,s) * i_hv.behave_change_rate(rg-1,s) +

          //entrants following hiv stage progression
          n_hv.adults(VAC_UNV,hd-1,rg,s) * progress_in);

          if(value<0) value=0;
          n_hv.adults(VAC_UNV,hd,RG_NONE,s) = value;

          //vaccinated
          for (int v = VAC_TAKE; v <= VAC_NO_PROT; ++v)
          {
                value = 
                n_hv.adults(v,hd,rg,s) + dt*( -
                //exits and migration
                n_hv.adults(v,hd,rg,s) * (
                i_hv.background_death_rate(s) + 
                mort_hiv + //hiv mortality rate
                progress_out + //hiv progrssion rate 
                rate_aging_out + // aging out at age 50
                i_hv.migration_rate(s) ) -

                //new vaccinations
                i_hv.new_vaccinations(rg,hd,s)  * i_hv.vac_effect(p_hv.rn_vac_targetting,v) - // *
                //temp1 * (temp2!=0)? 1 / temp2 : 0 -
              
                //vaccine, exits
                n_hv.adults(v,hd,rg,s)*
                (i_hv.vac_params(VAC_DUR)!=0)? 1 / i_hv.vac_params(VAC_DUR) : 0  +

                //entrants following behavior change
                n_hv.adults(v,hd,rg-1,s) * i_hv.behave_change_rate(rg-1,s) +
              
                //entrants following hiv stage progression
                n_hv.adults(VAC_UNV,hd,rg,s) * progress_in); 

                if(value<0) value=0;
                n_hv.adults(v,hd,rg,s)=value;
            
          }//v

        } //hd

      }//rg

    }//s
}

void allocate_art(int t)
{
  //from aim
  auto& i_ha = intermediate.ha;
  const auto& p_ha = pars.ha;

  //from goals
  auto& n_hv = state_next.hv;
  auto& c_hv = state_curr.hv;
  auto& i_hv = intermediate.hv;
  auto& p_hv = pars.hv;

  real_type not_receiving_art_vrhs[nVAC][nRG][nCD4p][nNS]; 
  real_type eligible_art_vrhs[nVAC][nRG][nCD4p][nNS]; 

  real_type receiving_art_vrs[nVAC][nRG][nNS] ;   
  real_type not_receiving_art_vrs[nVAC][nRG][nNS] ;
  real_type start_art[nVAC][nRG][nNS]  ; 
  real_type sum_elig_art[nVAC][nRG][nNS]   ;       
 
  real_type  sex_age_hiv[POP_H_OnART][nNS];         
  real_type  art_cov[RG_TOTAL1][nNS];             
  bool  kp_cd4_elig[RG_TOTAL1][nNS];  
  
  real_type new_patients[nCD4p];            
  real_type mort_rate[nCD4p];           
  real_type prop1[nCD4p];           
  real_type prop2[nCD4p];            
  real_type prop_avg[nCD4p]; 
  
  real_type prop_gt12m;            
  real_type prop_lt12m;            
  real_type num_ltfu;               
  real_type prop_by_mort;         
  real_type prop_by_elig;            
  real_type remaining_new_art;
  real_type Entrants_hrv;

  real_type ltfu;
  real_type new_art_cap;
  real_type sum1;  


for (int s = S_MALE; s <= S_FEMALE; ++s) {
    for (int rg = RG_NONE; rg <= RG_TOTAL1; ++rg) {
        kp_cd4_elig[rg][s] = true;
    }
}

prop_by_mort = p_ha.initiation_mortality_weight;
prop_by_elig = 0;

// Do LTFU dynamics, before achieving a CD4 coverage
// convert the LTFU % to a per-capita annual rate
ltfu = -std::log(1.0 - p_ha.dropout_rate(t));

if (ltfu > 0) {
    for (int s = S_MALE; s <= S_FEMALE; ++s) {
        for (int hd = CD4_LT50; hd >= CD4_GT500; --hd) {

            prop_gt12m = i_hv.aging_denom_1549(POP_H_ARTgt12m, hd, s);
            prop_lt12m = i_hv.aging_denom_1549(POP_H_ARTlt6m, hd, s)
                                 + i_hv.aging_denom_1549(POP_H_ART6to12m, hd, s);

            if ((prop_lt12m + prop_gt12m) > 0.0)
                prop_gt12m = prop_gt12m / (prop_gt12m + prop_lt12m);
            else
                prop_gt12m = 0.0;

            prop_lt12m = 1.0 - prop_gt12m;

            for (int rg = RG_NONE; rg <= RG_TOTAL1; ++rg) {
                for (int v = VAC_UNV; v <= VAC_NO_PROT; ++v) {
                    
                  num_ltfu = ltfu / opts.hts_per_year *  c_hv.adults(v,hd+7,rg,s);

                    if (hd == CD4_GT500) {
                        n_hv.adults(v,hd,rg,s) += num_ltfu;
                    } else {
                        n_hv.adults(v,hd-1,rg,s) += prop_gt12m * num_ltfu;
                        n_hv.adults(v,hd,rg,s)   += prop_lt12m * num_ltfu;
                    }
                    // note offset on h
                    n_hv.adults(v,hd+7,rg,s)   -= num_ltfu;
                }
            }
        }
    }
}

new_art_cap = 0.99;


/* for (int s = S_MALE; s <= S_FEMALE; ++s) {
    sex_age_hiv[s][DP_Pop_H_NoART] = 0;
    sex_age_hiv[s][POP_H_OnART] = 0;
    for (int hd = CD4_GT500; hd >= CD4_LT50; ++hd) {
        sex_age_hiv[s][DP_Pop_H_NoART] += i_hv.aging_denom_1549(POP_H_NoART, hd, s);
        sex_age_hiv[s][POP_H_OnART]    += i_hv.aging_denom_1549(POP_H_OnART, hd, s);
    }
}


for (int s = S_MALE; s <= S_FEMALE; ++s) {
    for (int rg = RG_NONE; rg <= RG_TOTAL1; ++rg) {
        if (s == S_FEMALE) {
            if ((rg == TG_HRH) && DP.GetPopsEligTreat(DP_EligTreatSexWorkers).Eligible &&
                DP.GetPopsEligTreat(DP_EligTreatSexWorkers).Year <= (DP.GetFirstYear + t - 1)) {
                kp_cd4_elig[S_FEMALE][RG_HRH] = false;
            }
            if ((rg == RG_IDU) && DP.GetPopsEligTreat(DP_EligTreatIDU).Eligible &&
                DP.GetPopsEligTreat(DP_EligTreatIDU).Year <= (DP.GetFirstYear + t - 1)) {
                kp_cd4_elig[S_FEMALE][RG_IDU] = false;
            }
        }

        if (s == S_MALE) {
            if ((rg == RG_MSM) && DP.GetPopsEligTreat(DP_EligTreatMSM).Eligible &&
                DP.GetPopsEligTreat(DP_EligTreatMSM).Year <= (DP.GetFirstYear + t - 1)) {
                kp_cd4_elig[S_MALE][RG_MSM] = false;
                //not doing these groups, currently 
                //kp_cd4_elig[HV_Male][RG_MSMLR] = false;
                //kp_cd4_elig[HV_Male][RG_MSMMR] = false;
                //kp_cd4_elig[HV_Male][RG_MSMHR] = false;
                //kp_cd4_elig[HV_Male][RG_MSMIDU] = false;
            }
            if ((rg == RG_IDU) && DP.GetPopsEligTreat(DP_EligTreatIDU).Eligible &&
                DP.GetPopsEligTreat(DP_EligTreatIDU).Year <= (DP.GetFirstYear + t - 1)) {
                AM_KP_CD4Elig[S_MALE][RG_IDU] = false;
            }
        }
    }
} */


for (int s = S_MALE; s <= S_FEMALE; ++s) {
// Set ART coverage for all risk groups to AIM 15‑49 coverage
if (sex_age_hiv[S_MALE][POP_H_OnART] > 0.0)
    for (int rg = RG_NONE; rg <= RG_TOTAL1; ++rg)
    {
     
        art_cov[S_MALE][rg] = sex_age_hiv[S_MALE][POP_H_OnART] /
                               (sex_age_hiv[S_MALE][POP_H_NoART] +
                                sex_age_hiv[S_MALE][POP_H_OnART]);

        art_cov[S_FEMALE][rg] = sex_age_hiv[S_FEMALE][POP_H_OnART] /
                                 (sex_age_hiv[S_FEMALE][POP_H_NoART] +
                                  sex_age_hiv[S_FEMALE][POP_H_OnART]);
    }


      // ART_NUM_PERCENT       =0;
      // ART_CD4_PERCENT       =1;
      // ART_CD4_NUMBER        =2;
      // ART_NEW_PATS          =3;
      // ART_RG_PERCENT        =4;
     
  
//KP coverage from AIM input editor
//if (p_ha.art_cov_num_percent == ART_RG_PERCENT)
if (p_ha.art_cov_num_percent == 0)
{
    // Coverage for males, risk groups HV_IDU … HV_MSM
    for (int rg = RG_IDU; rg <= RG_MSM; ++rg)
    {
        art_cov[rg][S_MALE] = p_hv.art_coverage_rg(S_FEMALE, rg, t) / 100.0;
    }

    // Coverage for females, risk groups HV_HRH … HV_IDU
    for (int rg = RG_HRH; rg <= RG_IDU; ++rg)
    {
        art_cov[rg][S_FEMALE]= p_hv.art_coverage_rg(S_FEMALE, rg, t) / 100.0;
    }
}

}


// Calc new ART by sex and allocate it
for (int s = S_MALE; s <= S_FEMALE; ++s)              
{

    for (int hd = CD4_GT500; hd <= CD4_LT50 ; ++hd)   
    {
        for (int rg = RG_NONE; rg <= RG_TOTAL1; ++rg)     
        {
            for (int v = VAC_UNV; v <= VAC_NO_PROT; ++v) 
            {
                // not receiving ART (by sex & risk‑HIV‑risk‑viral)
                not_receiving_art_vrs[v][rg][s] += n_hv.adults(v,rg,hd,s);
                not_receiving_art_vrhs[v][rg][hd][s] += n_hv.adults(v,rg,hd,s);

                // receiving ART (by sex & risk‑viral)
                receiving_art_vrs[v][rg][s] += n_hv.adults(v,rg,hd+7,s);

                if (kp_cd4_elig[rg][s] == true)
                {
                    if (hd>=i_ha.everARTelig_idx)
                    {
                        // eligible ART (by sex, CD4, risk‑viral)
                        eligible_art_vrhs[v][rg][hd][s] = n_hv.adults(v,rg,hd,s);
                        sum_elig_art[v][rg][s] += n_hv.adults(v,rg,hd,s);
                    }
                }
                else
                {
                    // eligible ART (by sex, CD4, risk‑viral) – default path
                    eligible_art_vrhs[v][rg][hd][s] = n_hv.adults(v,rg,hd,s);
                    sum_elig_art[v][rg][s] += n_hv.adults(v,rg,hd,s);
                }
            } // v
        } // r
    } // h



} // s


};

//post inner loop functions
void sum_adult_pop_dims(int t)
{

  auto& n_hv = state_next.hv;

    for (int s = S_MALE; s <= S_FEMALE; ++s)
        for (int hd = CD4_NEG; hd <= CD4_LT50_ART; ++hd)
            for (int rg = RG_NONE; rg <= RG_MSMIDU; ++rg)
            {
                real_type sum = 0.0;
                for (int v = VAC_UNV; v <= VAC_NO_PROT; ++v)
                {
                    // Exclude female MSM and higher risk groups
                    if (!((s == S_FEMALE) && (rg >= RG_MSM)))
                        sum += n_hv.adults(VAC_ALL,hd,rg,s);
                }
                n_hv.adults(VAC_ALL,rg,hd,s) = sum;
            }

     for (int s = S_MALE; s <= S_FEMALE; ++s)
        for (int hd = CD4_NEG; hd <= CD4_LT50_ART; ++hd)
            for (int v = VAC_UNV; v <= VAC_ALL; ++v)
            {
                real_type sum = 0.0;
                for (int rg = RG_NONE; rg <= RG_MSMIDU; ++rg)
                {
                    // Exclude female MSM and higher risk groups
                    if (!((s == S_FEMALE) && (rg >= RG_MSM)))
                        sum += n_hv.adults(VAC_ALL,hd,rg,s);
                }
                n_hv.adults(v,RG_ALL,hd,s) = sum;
            } 
            
            
       for (int s = S_MALE; s <= S_FEMALE; ++s)
        for (int rg = RG_NONE; rg <= RG_ALL; ++rg)
            for (int v = VAC_UNV; v <= VAC_ALL; ++v)
            {
                real_type sum = 0.0;
                for (int hd = CD4_NEG; hd <= CD4_LT50_ART; ++hd)
                {
                    // Exclude female MSM and higher risk groups
                    if (!((s == S_FEMALE) && (rg >= RG_MSM)))
                        sum += n_hv.adults(VAC_ALL,hd,rg,s);
                }
                n_hv.adults(v,rg,CD4_ALL,s) = sum;
            }    
            
        
        for (int hd = CD4_NEG; hd <= CD4_ALL; ++hd)
        for (int rg = RG_NONE; rg <= RG_ALL; ++rg)
            for (int v = VAC_UNV; v <= VAC_ALL; ++v)
            {
                real_type sum = 0.0;
                for (int s = S_MALE; s <= S_FEMALE; ++s)
                {
                    // Exclude female MSM and higher risk groups
                    if (!((s == S_FEMALE) && (rg >= RG_MSM)))
                        sum += n_hv.adults(VAC_ALL,hd,rg,s);
                }
                n_hv.adults(v,rg,hd,S_ALL) = sum;
            }          
     

}

//post inner loop functions
void sum_adult_pop_dims_goals(int t)
{

  auto& n_hv = state_next.hv;


    for (int s = S_MALE; s <= S_FEMALE; ++s)
        for (int rg = RG_NONE; rg <= RG_MSMIDU; ++rg)
            for (int hd = CD4_NEG; hd <= CD4_LT50_ART; ++hd)
            {
                real_type sum = 0.0;
                for (int v = VAC_UNV; v <= VAC_NO_PROT; ++v)
                {
                    // Exclude female MSM and higher risk groups
                    if (!((s == S_FEMALE) && (rg >= RG_MSM)))
                        sum += n_hv.adults(VAC_ALL,hd,rg,s);
                }
                n_hv.adults(VAC_ALL,hd,rg,s) = sum;
            }

    for (int s = S_MALE; s <= S_FEMALE; ++s)
    {
        double totalAcrossRisks = 0.0;
        for (int rg = RG_NONE; rg <= RG_MSMIDU; ++rg)
        {
            double sum = 0.0;              
            for (int hd = CD4_NEG; hd <= CD4_LT50_ART; ++hd)
            {
                for (int v = VAC_UNV; v <= VAC_NO_PROT; ++v)
                {
                    if (!((s == S_FEMALE) && (rg >= RG_MSM)))
                         sum += n_hv.adults(v,hd,rg,s);
                }
            }
            n_hv.adults(VAC_ALL,CD4_ALL,rg,s) = sum;
            totalAcrossRisks += sum;
        }
        n_hv.adults(VAC_ALL,CD4_ALL,RG_ALL,s) = totalAcrossRisks;
    }


    for (int s = S_MALE; s <= S_FEMALE; ++s)
        for (int rg = RG_NONE; rg <= RG_MSMIDU; ++rg)
            for (int v = VAC_UNV; v <= VAC_NO_PROT; ++v)
            {
                double sum = 0.0;
                for (int hd = CD4_NEG; hd <= CD4_LT50_ART; ++hd)
                {
                    if (!((s == S_FEMALE) && (rg >= RG_MSM)))
                        sum += n_hv.adults(v,hd,rg,s);
                }
                n_hv.adults(v,CD4_ALL,rg,s) = sum;
            }

      for (int s = S_MALE; s <= S_FEMALE; ++s)
       for (int hd = CD4_NEG; hd <= CD4_LT50_ART; ++hd){
        double sum = 0.0;
        for (int rg = RG_NONE; rg <= RG_MSMIDU; ++rg)
            for (int v = VAC_UNV; v <= VAC_NO_PROT; ++v){
                if (!((s == S_FEMALE) && (rg >= RG_MSM)))
                sum += n_hv.adults(v,hd,rg,s);
           }
         n_hv.adults(VAC_ALL,hd,RG_ALL,s) = sum;
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
    for (int r = 0; r < rRG_TOTAL; ++r) {
        n_hv.b_condom_prop_sum += p_hv.b_condom_prop(r, t);// * c_dp.p_totpop(r, s);
    }
    p_hv.b_condom_prop(RG_NONE, t) = n_hv.b_condom_prop_sum;

    //   for (int a = 0; a < pAG; ++a) {
    //     i_hv.ex_intermediate(a, s) = 1.0;

    //     n_hv.ex_output(a, s) = c_dp.p_totpop(a, s) + p_hv.b_condom_prop(a, s);
    //   }
    // }

  };


 



};

} // namespace internal
} // namespace leapfrog



