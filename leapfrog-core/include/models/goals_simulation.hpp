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

      INF_PRIM          = 1,
      INF_ASYMPT        = 2,
      INF_SYMPT_NO_ART  = 3,
      INF_SYMPT_ART     = 4,

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

      POC_CD4 = 0,
      POC_VL  = 1,
     
  };

  //stsatic constexpr int MALE = SS::MALE;
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
    
    //auto dbg_model = capture_model(state_next, intermediate, pars);

    n_hv.total_population += t; //c_dp.p_totpop(20,S_MALE);


  };

  void run_goals_pre_hiv_loop() {

    //check goals inputs 
    //print_goals_inputs();
    
    //initialize annual variables
    init_vars_pre_hiv_loop();
  
    //initilize adult population
    if(t==1){
      set_riskgroup_proportions();
      set_initial_pop();
    }

    //at hiv first year, apply initial pulse, t starts at 0
    int proj_start_year = opts.proj_start_year;
    //if(t==(p_hv.epi_start_year-proj_start_year)){
    if(t==1){
      set_initial_pulse();
    }

    //calc new vaccinations
    calc_new_vaccinations();

  
    //auto dbg_model = capture_model(state_next, intermediate, pars);
    //nda_print_info(dbg_model.hv.adults);

  }

   void run_goals_hiv_loop(int hiv_step) {

    //initialize inner loop varaibles
    init_vars_hiv_loop();
     
    //collect info from dp/aim to set demographical and HIV rates
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
    //progress_hivn_hivp_art(t);

    //calc new infections
    //calc_r_multiplier(t);

    //ART allocation
     //if (t >= opts.ts_art_start)
     //allocate_art(t);
    
  }

  void run_goals_post_hiv_loop() {

    //sum over dimensions of adult pop structure
    sum_adult_pop_dims(t);

  }

 void init_vars_pre_hiv_loop() {

  auto& n_hv = state_next.hv; 
  auto& i_hv = intermediate.hv;
  const auto& p_hv = pars.hv;
  
  nda::fill(n_hv.deaths, 0.0);//track deaths for each t

  //CDP: temp, using i_hv change back to p_hv
   nda::fill(i_hv.art_coverage_rg, 0.0);


  //infectiousness not on art
  nda::fill(n_hv.mult_no_art, 0.0);
  n_hv.mult_no_art(CD4_PRIM) = p_hv.epi_infectiousness(2); //INF_PRIM
  n_hv.mult_no_art(CD4_GT500) =  p_hv.epi_infectiousness(3); //INF_ASYMPT
  n_hv.mult_no_art(CD4_350_500) =  p_hv.epi_infectiousness(3); //INF_ASYMPT
  n_hv.mult_no_art(CD4_250_349) = p_hv.epi_infectiousness(3); //INF_ASYMPT
  n_hv.mult_no_art(CD4_200_249) = p_hv.epi_infectiousness(3); //INF_ASYMPT
  n_hv.mult_no_art(CD4_100_199) = p_hv.epi_infectiousness(4); //INF_SYMPT_NO_ART
  n_hv.mult_no_art(CD4_50_99) = p_hv.epi_infectiousness(4); //INF_SYMPT_NO_ART
  n_hv.mult_no_art(CD4_LT50) = p_hv.epi_infectiousness(4); //INF_SYMPT_NO_ART

  //infectiousness on art
  //CDP check CD4 dependency
  nda::fill(n_hv.mult_art, 0.0);
  for (int hd = CD4_GT500; hd <= CD4_LT50; ++hd){
      n_hv.mult_art(hd) = p_hv.epi_inf_mult_art(t) * p_hv.epi_infectiousness(4);
  }
    
  auto dbg_model = capture_model(state_next, intermediate, pars);

  nda_print_info(dbg_model.hv.epi_infectiousness);
  
  //##nda_print_info(dbg_model.hv.epi_inf_mult_art);
  
  //nda_print_info(dbg_model.hv.mult_no_art);
  //nda_print_info(dbg_model.hv.mult_art);

 }

  void init_vars_hiv_loop() {

   auto& n_hv = state_next.hv; 
  
    //init time dependent vars
    for (int s = S_MALE; s <= S_FEMALE; ++s)
        for (int rg = RG_NONE; rg <= RG_ALL; ++rg)
            for (int v = VAC_UNV; v <= VAC_ALL; ++v)
                for (int hd = CD4_NEG; hd <= CD4_LT50_ART; ++hd){
                  n_hv.adults_ts(v,rg,hd,s)=n_hv.adults(v,rg,hd,s);
                }

    nda::fill(n_hv.new_infections, 0.0);//new infections for time step 
    nda::fill(n_hv.newly_on_art, 0.0);//art allocation for time step         

 }

 void print_goals_inputs() {

  auto dbg_model = capture_model(state_next, intermediate, pars);

  nda_print_info(dbg_model.dp.p_totpop);

  // nda_print_info(dbg_model.hv.epi_start_year);
  //nda_print_info(dbg_model.hv.b_balance_sex_acts);

  //nda_print_info(dbg_model.hv.epi_months_in_primary);
  //nda_print_info(dbg_model.hv.epi_initial_pulse);
  nda_print_info(dbg_model.hv.b_condom_prop);
  nda_print_info(dbg_model.hv.b_behav_dur);
  nda_print_info(dbg_model.hv.b_sex_acts);
  nda_print_info(dbg_model.hv.b_num_partners);
  nda_print_info(dbg_model.hv.b_incr_recruit);
  nda_print_info(dbg_model.hv.b_married_prop);
  nda_print_info(dbg_model.hv.b_age_first_sex);
  nda_print_info(dbg_model.hv.b_idu_share_prop);
  nda_print_info(dbg_model.hv.rn_poc_cov);
  nda_print_info(dbg_model.hv.rn_vac_params);
  nda_print_info(dbg_model.hv.rn_vac_coverage);
  nda_print_info(dbg_model.hv.epi_infectiousness);
  nda_print_info(dbg_model.hv.epi_inf_mult_art);

  //nda_print_info(dbg_model.hv.rn_vac_cov_type);
  //nda_print_info(dbg_model.hv.rn_vac_targetting);


  // p_hv.epi_start_year;
  //  p_hv.epi_months_in_primary;
  //  p_hv.b_balance_sex_acts;
  //  p_hv.epi_initial_pulse;
 //  p_hv.b_condom_prop;
  //  p_hv.b_behav_dur;
  //  p_hv.b_sex_acts;
  //  p_hv.b_num_partners;
  //  p_hv.b_incr_recruit;
  //  p_hv.b_married_prop;
  //  p_hv.b_age_first_sex;
  //  p_hv.b_idu_share_prop;
  //  p_hv.rn_vac_params;
  //  p_hv.rn_vac_coverage;
  //  p_hv.rn_vac_cov_type;
  //  p_hv.rn_vac_targetting;   

 
 } 


//pre inner loop functions
 void set_riskgroup_proportions() {

    const auto& p_hv = pars.hv;
    auto& i_hv = intermediate.hv; 

    nda::fill(i_hv.riskgroup_proportions, 0.0);//risk group proportions
    nda::fill(i_hv.behave_change_rate, 0.0);//risk group proportions

    //risk group proportions, and behaviur change rates
    for (int rg = RG_NONE; rg <= RG_TOTAL1; ++rg) {

      //CDP note +1 on inputs
      i_hv.riskgroup_proportions(rg,S_MALE) = p_hv.b_behav_dur(rg+1, PERC_POP) / 100.0;
      if (rg > RG_LRH) i_hv.behave_change_rate(rg,S_MALE) = (p_hv.b_behav_dur(rg+1, DUR_AVG)!=0) ? 1 / p_hv.b_behav_dur(rg, DUR_AVG) : 0;
      
      if (rg != RG_MSM) {
        //CDP note offset for women
        i_hv.riskgroup_proportions(rg,S_FEMALE) = p_hv.b_behav_dur(rg+1+RG_NONE_F3 , PERC_POP) / 100.0;
        if (rg > RG_LRH) i_hv.behave_change_rate(rg,S_FEMALE) = (p_hv.b_behav_dur(rg+1+RG_NONE_F3, DUR_AVG)!=0) ? 1 / p_hv.b_behav_dur(rg, DUR_AVG) : 0;
      }

    }

    //auto dbg_model = capture_model(state_next, intermediate, pars);
    //nda_print_info(dbg_model.hv.riskgroup_proportions);
    //nda_print_info(dbg_model.hv.behave_change_rate);


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

      n_hv.adults(VAC_UNV,CD4_NEG,rg,s)=i_hv.riskgroup_proportions(rg,s)*i_hv.totpop_1549(s);

    }
  }  


  //auto dbg_model = capture_model(state_next, intermediate, pars);
  //nda_print_info(dbg_model.hv.totpop_1549);
  //nda_print_info(dbg_model.hv.adults);

}


  void set_initial_pulse() {
   
    //from dp/aim
    const auto& p_ha = pars.ha;

    //from goals
    const auto& c_hv = state_curr.hv;
    auto& n_hv = state_next.hv;
    auto& i_hv = intermediate.hv;
    const auto& p_hv = pars.hv;
    
    real_type pulse =0;
    real_type distr =0;

    for (int s = S_MALE; s <= S_FEMALE; ++s) { 

      for (int rg = RG_NONE; rg <= RG_TOTAL1; ++rg) {

        pulse = p_hv.epi_initial_pulse * c_hv.adults_ts(VAC_UNV,CD4_NEG,rg,s);

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
  const auto& p_hv = pars.hv;

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
    const auto& i_dp = intermediate.dp;
  

    //aim
    const auto& c_ha = state_curr.ha;
    const auto& p_ha = pars.ha;
    
    //goals
    auto& i_hv = intermediate.hv;
     
    //vars mapped from DP/AIM
    nda::fill(i_hv.totpop_deaths_background, 0.0);//dp background deaths numerator
    //CDP review name
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


  auto dbg_model = capture_model(state_next, intermediate, pars);
  
  //nda_print_info(dbg_model.hv.totpop_deaths_background);
  //nda_print_info(dbg_model.hv.totpop_1549);
 // nda_print_info(dbg_model.hv.pop_1549);
  //nda_print_info(dbg_model.hv.entrants_age_15);
  //nda_print_info(dbg_model.hv.aging_50);
  //nda_print_info(dbg_model.hv.aging_denom_1549);

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
          if(hd==CD4_LT50) i_hv.hiv_lambda(hd,s) = 0;//no progession out of this stage
          
          i_hv.rate_aging_50(POP_H_NoART, CD4_NEG, s) = (i_hv.aging_denom_1549(POP_H_NoART, CD4_NEG, s) !=0) ? i_hv.aging_50(POP_H_NoART, CD4_NEG, s)/i_hv.aging_denom_1549(POP_H_NoART, CD4_NEG, s) : 0; 
      
          denominator = 0.0;
          numerator = 0.0;
          for (int ht = CD4_GT500; ht <= CD4_LT50; ++ht) {
            numerator +=   i_hv.aging_50(POP_H_ARTlt6m+ht, hd, s);              
            denominator += i_hv.aging_denom_1549(POP_H_ARTlt6m+ht, hd, s);
          }
          i_hv.rate_aging_50(POP_H_OnART, hd, s) = (denominator !=0) ? numerator/denominator : 0;

      }


      //aggregate exit rates  CDP review if still needed
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

}

void calc_newrecruits_distribution(int t)
{
  auto& n_hv = state_next.hv;
  auto& i_hv = intermediate.hv;
  const auto& p_hv = pars.hv;

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

    const auto& c_hv = state_curr.hv;
    auto& n_hv = state_next.hv;
    auto& i_hv = intermediate.hv;
    const auto& p_hv = pars.hv;

    real_type dt = 1/opts.hts_per_year;
    real_type value = 0;
    real_type temp1 = 0;
    real_type temp2 = 0;
    nda::fill(i_hv.new_vaccinations, 0.0);
    nda::fill(i_hv.vac_params, 0.0);

    //unvaccinated
    for (int s = S_MALE; s <= S_FEMALE; ++s)
    {
     
        temp1=c_hv.adults(VAC_UNV,CD4_NEG,RG_NONE,s);
        temp2=c_hv.adults(VAC_UNV,CD4_ALL,RG_NONE,s);

        value = 
        c_hv.adults(VAC_UNV,CD4_NEG,RG_NONE,s) + dt*(
        //new entrants 15 yrs , note that they are not vaccinated by assumption
        i_hv.entrants_age_15(POP_H_HIVNeg,CD4_NEG,s) -
        //exits and migration
        c_hv.adults(VAC_UNV,CD4_NEG,RG_NONE,s) * (
        (std::max(p_hv.b_age_first_sex(s,t) - 15.0, 1.0)!=0)? 1/std::max(p_hv.b_age_first_sex(s,t) - 15.0, 1.0) : 0 +
        i_hv.background_death_rate(s) + 
        i_hv.rate_aging_50(POP_H_HIVNeg,CD4_NEG,s) - 
        i_hv.migration_rate(s) ) -

        //new vaccinations
        i_hv.new_vaccinations(RG_NONE,CD4_NEG,s) + // *
        //c_hv.adults(VAC_UNV,CD4_NEG,RG_NONE,s) *
        //(c_hv.adults(VAC_UNV,CD4_ALL,RG_NONE,s)!=0)? 1/ c_hv.adults(VAC_UNV,CD4_ALL,RG_NONE,s) : 0 +
      
        //vaccine waning, entrants
        (c_hv.adults(VAC_TAKE,CD4_NEG,RG_NONE,s) +
          c_hv.adults(VAC_PARTIAL,CD4_NEG,RG_NONE,s) +
          c_hv.adults(VAC_NO_PROT,CD4_NEG,RG_NONE,s)) *
        (i_hv.vac_params(VAC_DUR)!=0)? 1 / i_hv.vac_params(VAC_DUR) : 0  );

        if(value<0) value=0;
        n_hv.adults(VAC_UNV,CD4_NEG,RG_NONE,s) = value;

        //keep track of deaths
        n_hv.deaths(VAC_UNV,CD4_NEG,RG_NONE,s) += dt*n_hv.adults_ts(VAC_UNV,CD4_NEG,RG_NONE,s)*
                                                    i_hv.background_death_rate(s);


        //vaccinated
        for (int v = VAC_TAKE; v <= VAC_NO_PROT; ++v)
        {
              value = 
              c_hv.adults(v,CD4_NEG,RG_NONE,s) + dt*( -
              //exits and migration
              c_hv.adults(v,CD4_NEG,RG_NONE,s) * (
              (std::max(p_hv.b_age_first_sex(s,t) - 15.0, 1.0)!=0)? 1/std::max(p_hv.b_age_first_sex(s,t) - 15.0, 1.0) : 0 +
              i_hv.background_death_rate(s) + 
              i_hv.rate_aging_50(POP_H_HIVNeg,CD4_NEG,s) - 
              i_hv.migration_rate(s) ) + 

              //new vaccinations
              i_hv.new_vaccinations(RG_NONE,CD4_NEG, s) * i_hv.vac_effect(p_hv.rn_vac_targetting,v) -
               - // *
              //temp1 * (temp2!=0)? 1 / temp2 : 0 -
            
              //vaccine, exits
              c_hv.adults(v,CD4_NEG,RG_NONE,s)*
              (i_hv.vac_params(VAC_DUR)!=0)? 1 / i_hv.vac_params(VAC_DUR) : 0  );

              if(value<0) value=0;
              n_hv.adults(v,CD4_NEG,RG_NONE,s)=value;

              //keep track of deaths
              n_hv.deaths(v,CD4_NEG,RG_NONE,s) += dt*n_hv.adults_ts(v,CD4_NEG,RG_NONE,s)*
                                                     i_hv.background_death_rate(s);
           
        }//v

    }//s
}

void progress_atrisk_hiv_neg(int t)
{

    const auto& c_hv = state_curr.hv;
    auto& n_hv = state_next.hv;
    auto& i_hv = intermediate.hv;
    const auto& p_hv = pars.hv;

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
          
          temp1=c_hv.adults(VAC_UNV,CD4_NEG,rg,s);
          temp2=c_hv.adults(VAC_UNV,CD4_ALL,rg,s);

          value = 
          c_hv.adults(VAC_UNV,CD4_NEG,rg,s) + dt*(
          
           //no risk at sexual debut
           c_hv.adults(VAC_UNV,CD4_NEG,RG_NONE,s) *
           (std::max(p_hv.b_age_first_sex(s,t) - 15.0, 1.0)!=0)? 1/std::max(p_hv.b_age_first_sex(s,t) - 15.0, 1.0) : 0 *
           i_hv.riskgroup_proportions(rg,s) -
           
          //exits and migration
          c_hv.adults(VAC_UNV,CD4_NEG,rg,s) * (
          i_hv.background_death_rate(s) + 
          i_hv.rate_aging_50(POP_H_HIVNeg,CD4_NEG,s) +
          i_hv.behave_change_rate(rg,s) - 
          i_hv.migration_rate(s) ) -

          //new vaccinations
          i_hv.new_vaccinations(rg,CD4_NEG,s) + // *
          //c_hv.adults(VAC_UNV,CD4_NEG,rg,s) *
          //(c_hv.adults(VAC_UNV,CD4_ALL,rg,s)!=0)? 1/ c_hv.adults(VAC_UNV,CD4_ALL,rg,s) : 0 +
        
          //vaccine waning, entrants
          (c_hv.adults(VAC_TAKE,CD4_NEG,rg,s) +
            c_hv.adults(VAC_PARTIAL,CD4_NEG,rg,s) +
            c_hv.adults(VAC_NO_PROT,CD4_NEG,rg,s)) *
          (i_hv.vac_params(VAC_DUR)!=0)? 1 / i_hv.vac_params(VAC_DUR) : 0 +  
        
          //entrants following behavior change
          c_hv.adults(VAC_UNV,CD4_NEG,rg-1,s) * i_hv.behave_change_rate(rg-1,s) );

          if(value<0) value=0;
          n_hv.adults(VAC_UNV,CD4_NEG,rg,s) = value;

          //keep track of deaths
          n_hv.deaths(VAC_UNV,CD4_NEG,rg,s) += dt*n_hv.adults_ts(VAC_UNV,CD4_NEG,rg,s)*
                                               i_hv.background_death_rate(s);
                                                    

          //vaccinated
          for (int v = VAC_TAKE; v <= VAC_NO_PROT; ++v)
          {
                value = 
                c_hv.adults(v,CD4_NEG,rg,s) + dt*( -
                //exits and migration
                c_hv.adults(v,CD4_NEG,rg,s) * (
                i_hv.background_death_rate(s) + 
                i_hv.rate_aging_50(POP_H_HIVNeg,CD4_NEG,s) -
                i_hv.behave_change_rate(rg,s) - 
                i_hv.migration_rate(s) ) -

                //new vaccinations
                i_hv.new_vaccinations(rg,CD4_NEG,s) * i_hv.vac_effect(p_hv.rn_vac_targetting,v) - // *
                //temp1 * (temp2!=0)? 1 / temp2 : 0 -
              
                //vaccine, exits
                c_hv.adults(v,CD4_NEG,rg,s)*
                (i_hv.vac_params(VAC_DUR)!=0)? 1 / i_hv.vac_params(VAC_DUR) : 0  +

                //entrants following behavior change
                c_hv.adults(VAC_UNV,CD4_NEG,rg-1,s) * i_hv.behave_change_rate(rg-1,s) ); 

                if(value<0) value=0;
                n_hv.adults(v,CD4_NEG,rg,s)=value;

                //keep track of deaths
                n_hv.deaths(v,CD4_NEG,rg,s) += dt*n_hv.adults_ts(v,CD4_NEG,rg,s)*
                                               i_hv.background_death_rate(s);
                                                    
            
          }//v

      }//rg

    }//s
}

void progress_hivn_hivp_art(int t)
{
    //from goals
    auto& n_hv = state_next.hv;
    auto& i_hv = intermediate.hv;
    const auto& p_hv = pars.hv;

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
          n_hv.adults(VAC_UNV,hd,rg,s) = value;

          //keep track of deaths
          n_hv.deaths(VAC_UNV,hd,rg,s) += dt*n_hv.adults_ts(VAC_UNV,hd,rg,s)*
                                            (i_hv.background_death_rate(s)+mort_hiv);

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

                //keep track of deaths
                n_hv.deaths(v,hd,rg,s) += dt*n_hv.adults_ts(v,hd,rg,s)*
                                            (i_hv.background_death_rate(s)+mort_hiv);
            
          }//v

        } //hd

      }//rg

    }//s
}


void calc_r_multiplier(int t)
{
    
  //from goals
  auto& n_hv = state_next.hv;
  const auto& p_hv = pars.hv; 

  const double rMultEqlb = 1.7;// 2.44 in previous version of Goals
  double rMultNumeratorAll = 0.0;
  double rMultDenominatorAll = 0.0;

  nda::fill(n_hv.r_mult, 1.0); //default multiplier

  for (int s = S_MALE; s <= S_FEMALE; ++s)
  {
      for (int rg = RG_LRH; rg <= RG_MSM; ++rg)
      {
        
        if (rg == RG_IDU) continue; //IDU force of infection is external input 
        if (s == S_FEMALE && rg > RG_IDU) continue; //no female MSM
        
          double rMultNumerator   = 0.0;
          double rMultDenominator = 0.0;
          // not on ART
          for (int hd = CD4_PRIM ; hd <=CD4_LT50 ; ++hd)
          {
              rMultNumerator   += n_hv.mult_no_art(hd) * n_hv.adults(VAC_ALL ,rg,hd,s);
              rMultDenominator += n_hv.adults(VAC_ALL,rg,hd,s);

              rMultNumeratorAll   +=  n_hv.mult_no_art(hd) * n_hv.adults(VAC_ALL,rg,hd,s);
              rMultDenominatorAll += n_hv.adults(VAC_ALL,rg,hd,s);
          }
    
          //on ART
          for (int hd = CD4_GT500_ART ; hd <= CD4_LT50_ART ; ++hd)
          {
              rMultNumerator   += n_hv.mult_art(hd) * n_hv.adults(VAC_ALL,rg,hd,s);
              rMultDenominator += n_hv.adults(VAC_ALL,rg,hd,s);

              rMultNumeratorAll   += n_hv.mult_art(hd) * n_hv.adults(VAC_ALL,rg,hd,s);
              rMultDenominatorAll += n_hv.adults(VAC_ALL,rg,hd,s);
          }

          if (rMultDenominator > 0.0)
          {
              double vaccineFactor = 1.0;// - ( _VaccineEffectiveness[HV_RN_Infectiousness] / 100.0 )
                                          //* _TotalVaccinated[HV_Bothsexes][t - 1]
                                          /// _Populations[HV_Bothsexes][t - 1];

              n_hv.r_mult(rg,s) = (rMultNumerator / rMultDenominator) / rMultEqlb
                                    * vaccineFactor;
          }

      }//r

   }//s

    if (rMultDenominatorAll > 0.0)
    {
        double vaccineFactor = 1.0; //- ( _VaccineEffectiveness[HV_RN_Infectiousness] / 100.0 )
                                     //* _TotalVaccinated[HV_Bothsexes][t - 1]
                                     // / _Populations[HV_Bothsexes][t - 1];

        n_hv.r_mult(RG_ALL, S_ALL) = (rMultNumeratorAll / rMultDenominatorAll) / rMultEqlb
                                                * vaccineFactor;
    }

}

void allocate_art(int t)
{

//from aim
auto& i_ha = intermediate.ha;
const auto& p_ha = pars.ha;

//from goals
auto& n_hv = state_next.hv;
auto& i_hv = intermediate.hv;
const auto& p_hv = pars.hv;

real_type not_receiving_art_vrhs[nVAC][nRG][nCD4p][nNS]; 
real_type eligible_art_vrhs[nVAC][nRG][nCD4p][nNS]; 

real_type receiving_art_vrs[nVAC][nRG][nNS] ;   
real_type not_receiving_art_vrs[nVAC][nRG][nNS] ;
real_type start_art[nVAC][nRG][nNS]  ; 
real_type sum_elig_art[nVAC][nRG][nNS]   ;       

real_type  sex_age_hiv[POP_H_ALL][nNS];         
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
real_type entrants;

real_type ltfu;
real_type new_art_cap;
real_type sum1;  


for (int s = S_MALE; s <= S_FEMALE; ++s) {
    
   for (int hd = CD4_GT500; hd <= CD4_LT50 ; ++hd){
      sex_age_hiv[hd][s] =0;
   }

    for (int rg = RG_NONE; rg <= RG_TOTAL1; ++rg) {
      kp_cd4_elig[rg][s] = true;
      art_cov[rg][s] = 0;
    }    

    for (int v = VAC_UNV; v <= VAC_NO_PROT; ++v) {

      for (int rg = RG_NONE; rg <= RG_TOTAL1; ++rg) {
        receiving_art_vrs[v][rg][s]=0;
        not_receiving_art_vrs[v][rg][s]=0;
        start_art[v][rg][s]=0;
        sum_elig_art[v][rg][s]=0;
      
      for (int hd = CD4_GT500; hd <= CD4_LT50 ; ++hd){
        not_receiving_art_vrhs[v][rg][hd][s] =0;
        eligible_art_vrhs[v][rg][hd][s] =0;
      }
      
    }//rg
    
  }//v     
          
}//s

prop_by_mort = 1/2;//p_ha.initiation_mortality_weight;
prop_by_elig = 1.2;//0;

// do LTFU dynamics, before achieving a CD4 coverage
// convert the LTFU % to a per-capita annual rate
ltfu = -std::log(1.0 - p_ha.dropout_rate(t));

new_art_cap = 0.99;

const int hOnArt = 7;
if (ltfu > 0) {
    for (int s = S_MALE; s <= S_FEMALE; ++s) {
        for (int hd = CD4_LT50; hd >= CD4_GT500; --hd) {

            prop_gt12m = i_hv.aging_denom_1549(POP_H_ARTgt12m, hd, s);
            prop_lt12m = i_hv.aging_denom_1549(POP_H_ARTlt6m, hd, s)+
                        i_hv.aging_denom_1549(POP_H_ART6to12m, hd, s);

            if ((prop_lt12m + prop_gt12m) > 0.0)
                prop_gt12m = prop_gt12m / (prop_gt12m + prop_lt12m);
            else
                prop_gt12m = 0.0;

            prop_lt12m = 1.0 - prop_gt12m;

            for (int rg = RG_NONE; rg <= RG_TOTAL1; ++rg) {
                for (int v = VAC_UNV; v <= VAC_NO_PROT; ++v) {
                    
                    num_ltfu = ltfu / opts.hts_per_year *  n_hv.adults(v,rg,hd+hOnArt,s);

                    if (hd == CD4_GT500) {
                        n_hv.adults(v,rg,hd,s) += num_ltfu;
                    } else {
                        n_hv.adults(v,rg,hd-1,s) += prop_gt12m * num_ltfu;
                        n_hv.adults(v,rg,hd,s)   += prop_lt12m * num_ltfu;
                    }
                    // note offset on h
                    n_hv.adults(v,rg,hd+hOnArt,s)   -= num_ltfu;
                }
            }
        }//hd
    }//s
}//if (ltfu > 0) {


for (int s = S_MALE; s <= S_FEMALE; ++s) {
    sex_age_hiv[s][POP_H_NoART] = 0;
    sex_age_hiv[s][POP_H_OnART] = 0;
    for (int hd = CD4_GT500; hd >= CD4_LT50; ++hd) {
        sex_age_hiv[POP_H_NoART][s] += i_hv.aging_denom_1549(POP_H_NoART, hd, s);
        sex_age_hiv[POP_H_OnART][s] += i_hv.aging_denom_1549(POP_H_OnART, hd, s);
    }
}


for (int s = S_MALE; s <= S_FEMALE; ++s) {
    for (int rg = RG_NONE; rg <= RG_TOTAL1; ++rg) {
      if (s == S_FEMALE) {
           //if ((rg == TG_HRH) && DP.GetPopsEligTreat(DP_EligTreatSexWorkers).Eligible &&
           //     DP.GetPopsEligTreat(DP_EligTreatSexWorkers).Year <= (DP.GetFirstYear + t - 1)) {
           //     kp_cd4_elig[RG_HRH][S_FEMALE] = false;
           // }
           // if ((rg == RG_IDU) && DP.GetPopsEligTreat(DP_EligTreatIDU).Eligible &&
            //    DP.GetPopsEligTreat(DP_EligTreatIDU).Year <= (DP.GetFirstYear + t - 1)) {
                kp_cd4_elig[RG_IDU][S_FEMALE] = false;
            //}
        }

        if (s == S_MALE) {
            //if ((rg == RG_MSM) && DP.GetPopsEligTreat(DP_EligTreatMSM).Eligible &&
            //    DP.GetPopsEligTreat(DP_EligTreatMSM).Year <= (DP.GetFirstYear + t - 1)) {
            //    kp_cd4_elig[RG_MSM][S_MALE] = false;
                //not doing these groups, currently 
                //kp_cd4_elig[HV_Male][RG_MSMLR] = false;
                //kp_cd4_elig[HV_Male][RG_MSMMR] = false;
                //kp_cd4_elig[HV_Male][RG_MSMHR] = false;
                //kp_cd4_elig[HV_Male][RG_MSMIDU] = false;
           // }
           // if ((rg == RG_IDU) && DP.GetPopsEligTreat(DP_EligTreatIDU).Eligible &&
           //     DP.GetPopsEligTreat(DP_EligTreatIDU).Year <= (DP.GetFirstYear + t - 1)) {
                kp_cd4_elig[RG_IDU][S_MALE] = false;
            //}
        }
    }//rg
}//s 



// Set ART coverage for all risk groups to AIM 15 to 49 coverage
if (sex_age_hiv[POP_H_OnART][S_MALE] > 0.0){
    for (int rg = RG_NONE; rg <= RG_TOTAL1; ++rg)
    {
     
        art_cov[rg][S_MALE] = sex_age_hiv[POP_H_OnART][S_MALE] /
                               (sex_age_hiv[POP_H_NoART][S_MALE] +
                                sex_age_hiv[POP_H_OnART][S_MALE]);

        art_cov[rg][S_FEMALE] = sex_age_hiv[POP_H_OnART][S_FEMALE] /
                                 (sex_age_hiv[POP_H_NoART][S_FEMALE] +
                                  sex_age_hiv[POP_H_OnART][S_FEMALE]);
    }
}//if sex_age_hiv[S_MALE][POP_H_OnART] > 0.0

      
//KP coverage from AIM input editor
//if (p_ha.art_cov_num_percent == ART_RG_PERCENT)
if (p_ha.art_cov_num_percent == 0)
{
    // Coverage for males, risk groups HV_IDU … HV_MSM
    for (int rg = RG_IDU; rg <= RG_MSM; ++rg)
    {
        art_cov[rg][S_MALE] = i_hv.art_coverage_rg(S_FEMALE, rg, t) / 100.0; //CDP check /100
    }

    // Coverage for females, risk groups HV_HRH … HV_IDU
    for (int rg = RG_HRH; rg <= RG_IDU; ++rg)
    {
        art_cov[rg][S_FEMALE]= i_hv.art_coverage_rg(S_FEMALE, rg, t) / 100.0;
    }
}


// Calc new ART by sex and allocate it
for (int s = S_MALE; s <= S_FEMALE; s++)              
{

    //calc numbers eligible
    for (int hd = CD4_GT500; hd <= CD4_LT50 ; ++hd)   
    {
        for (int rg = RG_NONE; rg <= RG_TOTAL1; ++rg)     
        {
            for (int v = VAC_UNV; v <= VAC_NO_PROT; ++v) 
            {
                // not receiving ART (by sex & rg)
                not_receiving_art_vrs[v][rg][s] += n_hv.adults(v,rg,hd,s);//CDP check adults or adultsTS
                not_receiving_art_vrhs[v][rg][hd][s] += n_hv.adults(v,rg,hd,s);

                // receiving ART (by sex & rg)
                receiving_art_vrs[v][rg][s] += n_hv.adults(v,rg,hd+hOnArt,s);

                if (kp_cd4_elig[rg][s] == true)
                {
                    if (hd>=i_ha.everARTelig_idx)//CDp check role of this condition
                    {
                        // eligible ART (by rg, CD4, sex)
                        eligible_art_vrhs[v][rg][hd][s] = n_hv.adults(v,rg,hd,s);
                        sum_elig_art[v][rg][s] += n_hv.adults(v,rg,hd,s);
                    }
                }
                else
                {
                    // eligible ART (by rg, CD4, sex) – default path
                    eligible_art_vrhs[v][rg][hd][s] = n_hv.adults(v,rg,hd,s);
                    sum_elig_art[v][rg][s] += n_hv.adults(v,rg,hd,s);
                }

            } // v
        } // rg
    } // hd



    for (int rg = RG_NONE; rg <= RG_TOTAL1; ++rg) {
        for (int v = VAC_UNV; v <= VAC_NO_PROT; ++v) {

            start_art[v][rg][s] =
                                (not_receiving_art_vrs[v][rg][s] + receiving_art_vrs[v][rg][s]) *
                                art_cov[rg][s] -
                                receiving_art_vrs[v][rg][s];

            // aggregate both sexes – required for comparison with AIM
            //start_art[v][rg][S_ALL] += start_art[v][rg][s];
            
            //allocate new ART according to eligibility (Prop1) and mortality (Prop2)
            for (int hd = CD4_GT500; hd <= CD4_LT50; ++hd) {
                prop1[hd]        = 0.0;
                mort_rate[hd]    = 0.0;
                prop2[hd]        = 0.0;
                mort_rate[hd]    = 0.0;
                new_patients[hd] = 0.0;
            }

        
            if(sum_elig_art[v][rg][s] > 0.0) {
                  for (int hd = CD4_GT500; hd <= CD4_LT50; ++hd) {
                      if (hd == CD4_GT500) {
                          prop1[hd] = (eligible_art_vrhs[v][rg][hd][s] +
                                      eligible_art_vrhs[s][CD4_PRIM ][rg][v]) / //CDP check no prim stage allocation
                                      sum_elig_art[v][rg][s];
                      } else {
                          prop2[hd] = eligible_art_vrhs[v][rg][hd][s] /
                                      sum_elig_art[v][rg][s];
                      }
                  }    
            }

        
              double sum1 = 0.0;
              for (int hd = CD4_GT500; hd <= CD4_LT50; ++hd) {
                  sum1 += (1.0 / opts.hts_per_year) *
                          i_hv.hiv_mu(hd,s) *
                          eligible_art_vrhs[v][rg][hd][s];
              }

              if (sum1 > 0.0) {
                  for (int hd = CD4_GT500 ; hd <= CD4_LT50 ; ++hd) {
                      mort_rate[hd] = (1.0 / opts.hts_per_year) *
                                    i_hv.hiv_mu(hd,s) *
                                    eligible_art_vrhs[v][rg][hd][s] / sum1;
                  }
              }


            //weighted average of number eligible and mortality
            remaining_new_art = start_art[v][rg][s];
            for (int hd = CD4_LT50; hd >= CD4_GT500; --hd) {
                sum1 = 0.0;
                for (int h2 = hd; h2 >= CD4_GT500 ; --h2) {
                    sum1 += eligible_art_vrhs[v][rg][h2][s] * mort_rate[h2];//CDp check h2
                }

                if (sum1 <= 0.0) {
                    new_patients[hd] = 0.0;
                } else{
                    new_patients[hd] = (sum1>0) ? remaining_new_art *
                                                (eligible_art_vrhs[v][rg][hd][s] * mort_rate[hd]) /
                                                sum1 : 0;
                }

                //do not allocate more than are eligible in this CD4 band
                if (new_patients[hd] > eligible_art_vrhs[v][rg][hd][s]) {
                    new_patients[hd] = eligible_art_vrhs[v][rg][hd][s];
                }

                // Reduce the pool of ART that still needs to be allocated
                remaining_new_art -= new_patients[hd];
                if (remaining_new_art < 0.0) {
                    break;//hd loop: no more ART to distribute
                }

              }//hd
                

              // ---- Calculate proportion starting (Prop2) --------------------
              for (int hd = CD4_GT500; hd <= CD4_LT50; ++hd) {
                  prop2[hd] = 0.0;
                  if (start_art[v][rg][s] > 0.0) {
                      prop2[hd] = new_patients[hd] / start_art[v][rg][s];
                  }
              }//hd

              //final average of the two methods (propAvg)
              for (int hd = CD4_GT500; hd <= CD4_LT50 ; ++hd) {
                  prop_avg[hd] = prop_by_elig * prop1[hd] + prop_by_mort * prop2[hd];
              }

              //allocate the new ART by CD4 category 
              if (start_art[v][rg][s] > 0.0) {
                  for (int hd = CD4_GT500; hd <= CD4_LT50; ++hd) {
                      
                     entrants = prop_avg[hd] * start_art[v][rg][s];

                      // cannot remove ART patients!
                      entrants = std::max(entrants, 0.0);

                      // respect the cap for new ART
                      entrants = std::min(entrants, new_art_cap * n_hv.adults(v,rg,hd,s));

                      // HIV+ not on ART -> subtract entrants
                      n_hv.adults(v,rg,hd,s) -= entrants;

                      // HIV+ on ART -> add entrants (note the +10 offset)
                      n_hv.adults(v,rg,hd+hOnArt,s)+= entrants;


                      // keep track of newly started ART
                      n_hv.newly_on_art(hd,s) += entrants; //CDP check init of this array
                  }//hd
              }//if (StartART[s][rg][v] > 0.0)

        } // end of v loop
    } // end of r loop


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



