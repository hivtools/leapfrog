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
  using InternalState = Config::InternalState;
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
      S_OFFSET =1, //offset of 1 with respect to goals inputs

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
      RG_OFFSET = 1, //offset of 1 with respect to goals inputs

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

      HV_SUCC = 0,
      HV_INF  = 1,

      INTVN_MC15_49 = 19,
      INTVN_ALL = 43,

      PREP_OralDaily = 0,
      PREP_OralMonthly = 1,
      PREP_OralPlusCon = 2,
      PREP_Inject1Mo = 3,
      PREP_Inject2Mo = 4,
      PREP_Inject6Mo = 5,
      PREP_Ring = 6,
      PREP_bNABs = 7,
      PREP_Implant = 8,
      PREP_PEP = 9,
      PREP_NUM = 9,

      PREP_EFFECT = 0,
      PREP_ADH = 1,
      PREP_SUB = 2,
      PREP_DUR  = 3

  };

  //stsatic constexpr int MALE = SS::MALE;
  //static constexpr int FEMALE = SS::FEMALE;

  // function args
  int t;
  const Pars& pars;
  const State& state_curr;
  State& state_next;
  Intermediate& intermediate;
  InternalState& internal_state;
  const Options<real_type>& opts;

  // only exposing the constructor and some methods
  public:
  GoalsSimulation(Args& args):
    t(args.t),
    pars(args.pars),
    state_curr(args.state_curr),
    state_next(args.state_next),
    intermediate(args.intermediate),
    internal_state(args.internal_state),
    opts(args.opts)
  {};

static void init_internal_state(const Pars& pars, InternalState& internal_state) {
    const auto& p_hv = pars.hv;
    auto& s_hv = internal_state.hv;

    for (int rg = RG_NONE; rg <= RG_TOTAL; ++rg) {
      s_hv.riskgroup_proportions(rg, S_MALE) = p_hv.b_behav_dur(rg, PERC_POP);
      if (rg > RG_LRH) s_hv.behave_change_rate(rg, S_MALE) = (p_hv.b_behav_dur(rg, DUR_AVG) != 0) ? 1 / p_hv.b_behav_dur(rg, DUR_AVG) : 0;

      if (rg != RG_MSM) {
        s_hv.riskgroup_proportions(rg, S_FEMALE) = p_hv.b_behav_dur(rg + RG_NONE_F3, PERC_POP);
        if (rg > RG_LRH) s_hv.behave_change_rate(rg, S_FEMALE) = (p_hv.b_behav_dur(rg + RG_NONE_F3, DUR_AVG) != 0) ? 1 / p_hv.b_behav_dur(rg, DUR_AVG) : 0;
      }
    }
  };

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
  
    //set risk group sizes from inputs
    //CDP move to t==1 when new variable type than intermediate is available
    set_riskgroup_proportions();

    //initilize adult population
    if(t==1){
      set_initial_pop();
    }


    //at hiv first year, apply initial pulse, t starts at 0
    int proj_start_year = opts.proj_start_year;
    //if(t==(p_hv.epi_start_year-proj_start_year)){ //CDP reinstate coorect time for pulse
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

    //sum over the dimensions of adult pop 
    sum_adult_pop_dims(t);

    //make inner-time loop copy of adult structure
    set_adults_hiv_loop();
     
    //collect info from dp/aim to set demographical and HIV rates
    set_goals_vars_from_dp(t);
    
    //set these rates to vars in goals
    calc_goals_rates(t);

    //adjust distribution of new entrants into different risk groups
    //if( t>=2 && hiv_step=1)
      //calc_newrecruits_distribution(t);
    
    //progress, hiv-neg, not at risk (RG_NONE)
    progress_norisk_hiv_neg(t);

    //progress, hiv-neg, at risk (RG_LRH..RG_MSM)
    progress_atrisk_hiv_neg(t);

    //progress, hiv-neg, hiv-pos and hiv-art (RG_LRH..RG_MSM)
    progress_hivn_hivp_art(t);

    //calc prevalence used for new infections calc
    calc_prevalence();

    //calc new infections
    calc_r_multiplier(t);
    //calc_new_infections(t);
    
    //add new infections 
    add_new_infections();

    //ART allocation
     //if (t >= opts.ts_art_start)
     //allocate_art(t);
    
  }

  void run_goals_post_hiv_loop() {

    //sum over dimensions of adult pop structure
    //sum_adult_pop_dims(t);

  }

 void init_vars_pre_hiv_loop() {

  auto& n_hv = state_next.hv; 
  auto& i_hv = intermediate.hv;
  const auto& p_hv = pars.hv;
  
  nda::fill(n_hv.deaths, 0.0);//deaths for each t
  nda::fill(n_hv.new_infections, 0.0);//new infections for each v, rg,  t

  nda::fill(n_hv.new_inf_vrs, 0.0);//new infections for each t, by v,r,s, for goals
  nda::fill(n_hv.new_inf_s, 0.0);//new infections for each t, by sex, for aim

  //CDP: temp, using i_hv change back to p_hv
   nda::fill(i_hv.art_coverage_rg, 0.0);


  //infectiousness not on art
  nda::fill(n_hv.mult_no_art, 0.0);
  n_hv.mult_no_art(CD4_PRIM) = p_hv.epi_infectiousness(INF_PRIM); //INF_PRIM
  n_hv.mult_no_art(CD4_GT500) =  p_hv.epi_infectiousness(INF_ASYMPT); //INF_ASYMPT
  n_hv.mult_no_art(CD4_350_500) =  p_hv.epi_infectiousness(INF_ASYMPT); //INF_ASYMPT
  n_hv.mult_no_art(CD4_250_349) = p_hv.epi_infectiousness(INF_ASYMPT); //INF_ASYMPT
  n_hv.mult_no_art(CD4_200_249) = p_hv.epi_infectiousness(INF_ASYMPT); //INF_ASYMPT
  n_hv.mult_no_art(CD4_100_199) = p_hv.epi_infectiousness(INF_SYMPT_NO_ART); //INF_SYMPT_NO_ART
  n_hv.mult_no_art(CD4_50_99) = p_hv.epi_infectiousness(INF_SYMPT_NO_ART); //INF_SYMPT_NO_ART
  n_hv.mult_no_art(CD4_LT50) = p_hv.epi_infectiousness(INF_SYMPT_NO_ART); //INF_SYMPT_NO_ART

  //infectiousness on art
  //CDP check CD4 dependency
  nda::fill(n_hv.mult_art, 0.0);
  for (int hd = CD4_GT500; hd <= CD4_LT50; ++hd){
      n_hv.mult_art(hd) = p_hv.epi_inf_mult_art(t) * p_hv.epi_infectiousness(INF_SYMPT_NO_ART);
  }
   
         
 
  for (int s = S_MALE; s <= S_FEMALE; ++s)              
      for (int rg = RG_LRH; rg <= RG_TOTAL1; ++rg)         
          for (int m = PREP_OralDaily; m <= PREP_PEP ; ++m)
         {
    
             i_hv.prep_effect(rg,s) +=  p_hv.prep_effectiveness(PREP_EFFECT, m)  
                                      * p_hv.prep_effectiveness(PREP_ADH, m)
                                      * p_hv.prep_method_mix(S_OFFSET+s,RG_OFFSET+rg,m,t);
          }//s,r,m

      
          

  
  //auto dbg_model = capture_model(state_next, intermediate, pars);
  
  //nda_print_info(dbg_model.hv.epi_infectiousness);
  
  //nda_print_info(dbg_model.hv.epi_inf_mult_art);
  
  //nda_print_info(dbg_model.hv.mult_no_art);
  
  //nda_print_info(dbg_model.hv.mult_art);

  //nda_print_info(dbg_model.hv.prep_effect);



 }

  void init_vars_hiv_loop() {

   auto& n_hv = state_next.hv; 
  
    nda::fill(n_hv.newly_on_art, 0.0);//art allocation for time step    
    nda::fill(n_hv.prevalence, 0.0);//prevalence for each rg,  t

 }

   void set_adults_hiv_loop() {

   auto& n_hv = state_next.hv; 
  
    //init time dependent vars
          for (int v = VAC_UNV; v <= VAC_ALL; ++v)
            for (int rg = RG_NONE; rg <= RG_ALL; ++rg)
                for (int hd = CD4_NEG; hd <= CD4_ALL; ++hd)
                  for (int s = S_MALE; s <= S_FEMALE; ++s){
                    n_hv.adults_ts(v,rg,hd,s)=n_hv.adults(v,rg,hd,s);
                  }

  }

 void print_goals_inputs() {

  auto dbg_model = capture_model(state_next, intermediate, pars);



  nda_print_info(dbg_model.hv.b_age_first_sex);



  // nda_print_info(dbg_model.hv.epi_start_year);
  //nda_print_info(dbg_model.hv.b_balance_sex_acts
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

    nda::fill(i_hv.b_riskgroup_proportions, 0.0);//risk group proportions
    nda::fill(i_hv.b_behave_change_rate, 0.0);//risk group proportions

    //risk group proportions, and behaviour change rates
    for (int rg = RG_NONE; rg <= RG_MSM; ++rg) { //CDP reset range

      //CDP note +1 on inputs
      i_hv.b_riskgroup_proportions(rg,S_MALE) = p_hv.b_behav_dur(RG_OFFSET+rg, PERC_POP); 
      if (rg > RG_LRH) i_hv.b_behave_change_rate(rg,S_MALE) = (p_hv.b_behav_dur(RG_OFFSET+rg, DUR_AVG)!=0) ? 1 / p_hv.b_behav_dur(rg, DUR_AVG) : 0;
      
      if (rg != RG_MSM) {
        //CDP note offset for women
        i_hv.b_riskgroup_proportions(rg,S_FEMALE) = p_hv.b_behav_dur(RG_OFFSET+rg+RG_NONE_F3, PERC_POP);
        if (rg > RG_LRH) i_hv.b_behave_change_rate(rg,S_FEMALE) = (p_hv.b_behav_dur(RG_OFFSET+rg+RG_NONE_F3, DUR_AVG)!=0) ? 1 / p_hv.b_behav_dur(rg, DUR_AVG) : 0;
      }

    }

    //auto dbg_model = capture_model(state_next, intermediate, pars);
    
    //nda_print_info(dbg_model.hv.b_riskgroup_proportions);
    //nda_print_info(dbg_model.hv.b_behave_change_rate);
    //nda_print_info(dbg_model.hv.b_behav_dur);


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

      i_hv.pop_1549(s) += c_dp.p_totpop(a, s);

    }//a

    for (int rg = RG_NONE; rg <= RG_TOTAL; ++rg) {

      n_hv.adults(VAC_UNV,CD4_NEG,rg,s)=i_hv.b_riskgroup_proportions(rg,s)*i_hv.pop_1549(s);

    }//rg

  } //s 


  //auto dbg_model = capture_model(state_next, intermediate, pars);
  //nda_print_info(dbg_model.hv.b_riskgroup_proportions);
  //nda_print_info(dbg_model.hv.pop_1549);
  //nda_print_info(dbg_model.hv.adults,0,0,0,0); //list VAC_UNV, CD4_NEG

}


  void set_initial_pulse() {
   
    //from dp/aim
    const auto& p_ha = pars.ha;

    //from goals
    //const auto& c_hv = state_curr.hv;
    auto& n_hv = state_next.hv;
    //auto& i_hv = intermediate.hv;
    const auto& p_hv = pars.hv;
    
    real_type pulse =0;
    real_type distr =0;

    for (int s = S_MALE; s <= S_FEMALE; ++s) { 

      for (int rg = RG_NONE; rg <= RG_TOTAL; ++rg) {

        pulse = p_hv.epi_initial_pulse * n_hv.adults(VAC_UNV,rg,CD4_NEG,s);

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

          const int hd_hds = (hd == CD4_PRIM) ? 0 : (hd - CD4_GT500);

          distr = p_ha.cd4_initial_distribution(hd_hds, pIDX_15to49+10, s);//CDP note the use of one age category for distr from AIM

          n_hv.adults(VAC_UNV,rg,hd,s)  = n_hv.adults(VAC_UNV,rg,hd,s) + pulse*distr;
          n_hv.adults(VAC_UNV,rg,CD4_NEG,s) = n_hv.adults(VAC_UNV,rg,CD4_NEG,s) - pulse*distr;

        }

    }//rg

  }//s


  //auto dbg_model = capture_model(state_next, intermediate, pars);
  //nda_print_info(dbg_model.hv.adults,0,0,2,8,0,RG_MSM); //list VAC_UNV, CD4_NEG

 }

void calc_new_vaccinations()
{
  auto& n_hv = state_next.hv;
  auto& i_hv = intermediate.hv;
  const auto& p_hv = pars.hv;

  nda::fill(i_hv.new_vaccinations, 0.0);
  nda::fill(i_hv.vac_effect, 0.0);

  //real_type dt = 1/opts.hts_per_year;

  real_type vac_waning_rate=0;
  vac_waning_rate = (p_hv.rn_vac_params(VAC_DUR)>0) ? 1/p_hv.rn_vac_params(VAC_DUR) : 0;

  //vac effect
  i_hv.vac_effect(VAC_TAKEACTION,VAC_TAKE)       = p_hv.rn_vac_params(VAC_EFF)/100;//CDP: this /100 can be done in modvar mapping
  i_hv.vac_effect(VAC_TAKEACTION,VAC_NO_PROT)    = 1-p_hv.rn_vac_params(VAC_EFF)/100;
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

              value =  p_hv.rn_vac_coverage(RG_OFFSET+nr,t) * //dt *
                          (n_hv.adults(VAC_ALL,rg,hd,s)  +
                          //note it assume no one is vaccined below age 15
                          i_hv.dp_entrants_age_15(POP_H_HIVNeg,CD4_NEG,s) *
                          n_hv.adults(VAC_ALL,rg,hd,s)  / n_hv.adults(VAC_ALL,rg,CD4_ALL,s))-
                          (n_hv.adults(VAC_TAKE,rg,hd,s) +
                          n_hv.adults(VAC_PARTIAL,rg,hd,s) +
                          n_hv.adults(VAC_NO_PROT,rg,hd,s)) * (1 - vac_waning_rate);

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
    nda::fill(i_hv.dp_totpop_deaths_background, 0.0);//dp background deaths numerator
    //CDP review name
    nda::fill(i_hv.dp_totpop_1549, 0.0);//dp background deaths denominator
    
    nda::fill(i_hv.dp_pop_1549, 0.0);//denominator for background mortality, check age index (a-1)

    nda::fill(i_hv.dp_pop_1549_hiv, 0.0);//denominator for goals mu
    nda::fill(i_hv.dp_pop_1549_art, 0.0);//denominator for goals alpha
    
    nda::fill(i_hv.dp_hiv_cd4_mort_no_art, 0.0);//numerator for  mu
    nda::fill(i_hv.dp_hiv_cd4_mort_art, 0.0);//numerator for alpha
    nda::fill(i_hv.dp_hiv_cd4_progression, 0.0);//numerator for lambda

    
    nda::fill(i_hv.dp_pop_sex_age_hiv, 0.0);//used for ART allocation in goals
    nda::fill(i_hv.dp_entrants_age_15, 0.0);//numerator for 15 yr old entrants into goals
    nda::fill(i_hv.dp_aging_50, 0.0);//numerator for aging rate in goals, 50 yrs
    nda::fill(i_hv.dp_aging_denom_1549, 0.0);//denominator for aging rate in goals

    nda::fill(i_hv.dp_migration_num, 0.0);//numerator for avg migration rate
    nda::fill(i_hv.dp_migration_denom, 0.0);//denominaor for avg migration rate

  
    for (int s = S_MALE; s <= S_FEMALE; ++s) {
      
     for(int a = SS::pIDX_15to49; a < SS::pIDX_15to49 + SS::pAG_15to49; ++a) {
     
      i_hv.dp_totpop_deaths_background(s) += c_dp.p_deaths_background_totpop(a, s);
      i_hv.dp_totpop_1549(s) += c_dp.p_totpop(a - 1, s);

      i_hv.dp_migration_num(s) += 2000; //c_dp.p_totpop(a, s) * i_dp.migration_rate(a, s);
      i_hv.dp_migration_denom(s) += c_dp.p_totpop(a, s);
      
      i_hv.dp_pop_1549(s) += c_dp.p_totpop(a, s);
      i_hv.dp_aging_denom_1549(POP_H_HIVNeg, CD4_NEG, s) += c_dp.p_totpop(a, s);
      if(a==SS::pIDX_15to49){
         i_hv.dp_entrants_age_15(POP_H_HIVNeg, CD4_NEG, s) += c_dp.p_totpop(a, s);
      }
      
      if(a==SS::pIDX_15to49 + SS::pAG_15to49 - 1){
          i_hv.dp_aging_50(POP_H_HIVNeg, CD4_NEG, s) += c_dp.p_totpop(a, s);
      }

      for (int hd = CD4_GT500; hd <= CD4_LT50; ++hd) {
          const int hd_hds = hd - CD4_GT500;
  
          i_hv.dp_pop_1549_hiv(hd,s) += c_ha.h_hivpop(hd_hds, a, s);

          i_hv.dp_pop_sex_age_hiv(POP_H_NoART, s) += c_ha.h_hivpop(hd_hds, a, s);
          i_hv.dp_aging_denom_1549(POP_H_NoART, hd, s) += c_ha.h_hivpop(hd_hds, a, s);
          i_hv.dp_aging_denom_1549(POP_H_HIVNeg, CD4_NEG, s) -= c_ha.h_hivpop(hd_hds, a, s);//remove hiv states
          
          //i_hv.hiv_mu(hd,s) +=  (p_ha.cd4_mortality(hd, a, s)+p_ha.cd4_nonaids_excess_mort(hd, a, s)) * c_ha.h_hivpop(hd, a, s);
        
          if(a==SS::pIDX_15to49){
            i_hv.dp_entrants_age_15(POP_H_NoART, hd, s) += c_ha.h_hivpop(hd_hds, a, s);
            i_hv.dp_entrants_age_15(POP_H_HIVNeg, CD4_NEG, s) -= c_ha.h_hivpop(hd_hds, a, s);
          }
          
          if(a==SS::pIDX_15to49 + SS::pAG_15to49){
            i_hv.dp_aging_50(POP_H_NoART, hd, s) += c_ha.h_hivpop(hd_hds, a, s);
            i_hv.dp_aging_50(POP_H_HIVNeg, CD4_NEG, s) -= c_ha.h_hivpop(hd_hds, a, s);
          }

          i_hv.dp_hiv_cd4_mort_no_art(hd,s) += c_ha.h_hiv_deaths_no_art(hd_hds, a, s);
          if(hd > CD4_GT500){
            i_hv.dp_hiv_cd4_progression(hd-1, s) += p_ha.cd4_progression(hd_hds - 1, a, s) * c_ha.h_hivpop(hd_hds - 1, a, s);
          }

          for (int ht = 0; ht < nART; ++ht) {
            
            i_hv.dp_pop_1549_art (hd,s) += c_ha.h_artpop(ht, hd_hds, a, s);
            
            i_hv.dp_pop_sex_age_hiv(POP_H_ARTlt6m+ht, s) += c_ha.h_artpop(ht, hd_hds, a, s);
            i_hv.dp_aging_denom_1549(POP_H_ARTlt6m+ht, hd, s) += c_ha.h_artpop(ht, hd_hds, a, s);
            i_hv.dp_aging_denom_1549(POP_H_HIVNeg, CD4_NEG, s) -= c_ha.h_artpop(ht, hd_hds, a, s);//remove art states

            //CDP: using an average rate. review
            //i_hv.art_alpha(hd,s) +=  (p_ha.art_mortality(ht, hd, a, s)+p_ha.art_nonaids_excess_mort(ht, hd, a, s)) * c_ha.h_artpop(ht, hd, a, s);

            if(a==SS::pIDX_15to49){
              i_hv.dp_entrants_age_15(POP_H_ARTlt6m+ht, hd, s) += c_ha.h_artpop(ht, hd_hds, a, s);
              i_hv.dp_entrants_age_15(POP_H_HIVNeg, CD4_NEG, s) -= c_ha.h_artpop(ht, hd_hds, a, s);
            }

            if(a==SS::pIDX_15to49 + SS::pAG_15to49){
              i_hv.dp_aging_50(POP_H_ARTlt6m+ht, hd, s) += c_ha.h_artpop(ht, hd_hds, a, s);
              i_hv.dp_aging_50(POP_H_HIVNeg, CD4_NEG, s) -= c_ha.h_artpop(ht, hd_hds, a, s);
            }

             i_hv.dp_hiv_cd4_mort_art(hd_hds, s) += c_ha.h_hiv_deaths_art(ht, hd_hds, a, s);

          }//t            
          
        }//h

    }//a

  }//s


  auto dbg_model = capture_model(state_next, intermediate, pars);
  
   //nda_print_info(dbg_model.hv.dp_totpop_deaths_background);
   //nda_print_info(dbg_model.hv.dp_totpop_1549);
   //nda_print_info(dbg_model.hv.dp_pop_1549);
   //nda_print_info(dbg_model.hv.dp_entrants_age_15);
   //nda_print_info(dbg_model.hv.dp_aging_50);
   //nda_print_info(dbg_model.hv.dp_aging_denom_1549);

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
        i_hv.background_death_rate(s) = (i_hv.dp_totpop_1549(s)!=0) ? i_hv.dp_totpop_deaths_background(s)/i_hv.dp_totpop_1549(s) : 0;

        //migration rate
        i_hv.migration_rate(s) = (i_hv.dp_migration_denom(s) !=0) ? i_hv.dp_migration_num(s)/i_hv.dp_migration_denom(s) : 0;
     
        //set aging rates, out of 15-49 year old population 
        i_hv.rate_aging_50(POP_H_HIVNeg, CD4_NEG, s) = (i_hv.dp_aging_denom_1549(POP_H_HIVNeg, CD4_NEG, s) !=0) ? i_hv.dp_aging_50(POP_H_HIVNeg, CD4_NEG, s)/i_hv.dp_aging_denom_1549(POP_H_HIVNeg, CD4_NEG, s) : 0; 

        //cd4 transition rate for primary stage 
        i_hv.hiv_lambda(CD4_PRIM,s) = (years_in_primary!=0) ? 1/years_in_primary : 0;
       
        for (int hd = CD4_GT500; hd <= CD4_LT50; ++hd) {

          //hiv dynamics: mortality and progression rates
          i_hv.hiv_mu(hd,s) = (i_hv.dp_pop_1549_hiv(hd,s)!=0) ? i_hv.dp_hiv_cd4_mort_no_art(hd,s)/i_hv.dp_pop_1549_hiv(hd,s) : 0;
          i_hv.hiv_lambda(hd,s) = (i_hv.dp_pop_1549_hiv(hd,s)!=0) ? i_hv.dp_hiv_cd4_progression(hd,s)/i_hv.dp_pop_1549_hiv(hd,s) : 0;
          i_hv.art_alpha(hd,s) = (i_hv.dp_pop_1549_art(hd,s)!=0) ? i_hv.dp_hiv_cd4_mort_art(hd - CD4_GT500,s)/i_hv.dp_pop_1549_art(hd,s) : 0;
          
          if(hd==CD4_GT500){
            real_type stage_duration = 1.0 / i_hv.hiv_lambda(CD4_GT500,s)  - years_in_primary;
            i_hv.hiv_lambda(CD4_GT500,s) = 1-exp(-1/stage_duration);//remove time in primary stage
            i_hv.hiv_mu(CD4_PRIM,s) = i_hv.hiv_mu(CD4_GT500,s);
          } 
          if(hd==CD4_LT50) i_hv.hiv_lambda(hd,s) = 0;//no progession out of this stage
          
          i_hv.rate_aging_50(POP_H_NoART, CD4_NEG, s) = (i_hv.dp_aging_denom_1549(POP_H_NoART, CD4_NEG, s) !=0) ? i_hv.dp_aging_50(POP_H_NoART, CD4_NEG, s)/i_hv.dp_aging_denom_1549(POP_H_NoART, CD4_NEG, s) : 0; 
      
          denominator = 0.0;
          numerator = 0.0;
          for (int ht = CD4_GT500; ht <= CD4_LT50; ++ht) {
            numerator +=   i_hv.dp_aging_50(POP_H_ARTlt6m+ht, hd, s);              
            denominator += i_hv.dp_aging_denom_1549(POP_H_ARTlt6m+ht, hd, s);
          }
          i_hv.rate_aging_50(POP_H_OnART, hd, s) = (denominator !=0) ? numerator/denominator : 0;

      }


      //aggregate exit rates  CDP review if still needed
      for (int hd = CD4_GT500; hd < CD4_LT50; ++hd) {

        for (int rg = RG_NONE; rg <= RG_TOTAL; ++rg) {
            i_hv.hiv_exit_rates(rg,hd,s) = i_hv.background_death_rate(s)+
                                        i_hv.hiv_mu(hd,s)+
                                        (p_hv.b_behav_dur(RG_OFFSET+rg,DUR_AVG)>0) ? (1 /p_hv.b_behav_dur(RG_OFFSET+rg,DUR_AVG)) : 0 +
                                        i_hv.rate_aging_50(POP_H_NoART, hd, s);

            i_hv.art_exit_rates(rg,hd,s) = i_hv.background_death_rate(s)+
                                        i_hv.art_alpha(hd,s)+
                                        (p_hv.b_behav_dur(RG_OFFSET+rg,DUR_AVG)>0) ? (1 /p_hv.b_behav_dur(RG_OFFSET+rg,DUR_AVG)) : 0 +
                                        i_hv.rate_aging_50(POP_H_OnART, hd, s);  
        }                          
                                        
        }


      }

   auto dbg_model = capture_model(state_next, intermediate, pars);
  
   nda_print_info(dbg_model.hv.background_death_rate);     
   nda_print_info(dbg_model.hv.migration_rate);     
   nda_print_info(dbg_model.hv.rate_aging_50);   

   nda_print_info(dbg_model.hv.dp_migration_denom); 
   nda_print_info(dbg_model.hv.dp_migration_num); 
   
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
        if (s == S_FEMALE && rg >= RG_MSM) continue; 

        if(i_hv.riskgroup_proportions(rg,s)-
            n_hv.adults(VAC_ALL,rg,CD4_ALL,s)/n_hv.adults(VAC_ALL,rg,CD4_ALL,s) != 0)
        {
            if ( n_hv.adults(VAC_ALL,rg,CD4_ALL,s) == 0.0 ||
                 i_hv.behave_change_rate(rg,s)== 0.0 ||
                 n_hv.adults(VAC_ALL,RG_ALL,CD4_ALL,s) == 0.0)
            {
                value = 0.0;
            }
            else
            {
                value = i_hv.riskgroup_proportions(rg,s) +
                       ( (i_hv.riskgroup_proportions(rg,s) -
                         (1-i_hv.behave_change_rate(rg,s))*
                          n_hv.adults(VAC_ALL,rg,CD4_ALL,s)/
                          n_hv.adults(VAC_ALL,RG_ALL,CD4_ALL,s))*
                          p_hv.b_incr_recruit(s+S_OFFSET,rg+RG_OFFSET) );
            }

            if(value<0) value=0;
              rg_sum += value;

            //i_hv.riskgroup_proportions(rg,s)=value;
        }  

    }//rg 

    //normalize
    for (int rg = RG_LRH; rg <= RG_TOTAL1; ++rg)
    {
       // if (s == S_FEMALE && rg >= RG_MSM) continue; 
       // i_hv.riskgroup_proportions(rg,s)/=rg_sum;
    }

   }//s

 auto dbg_model = capture_model(state_next, intermediate, pars);

 nda_print_info(dbg_model.hv.b_incr_recruit); 
  
 nda_print_info(dbg_model.hv.riskgroup_proportions);  

   
}



void progress_norisk_hiv_neg(int t)
{

    const auto& c_hv = state_curr.hv;
    auto& n_hv = state_next.hv;
    auto& i_hv = intermediate.hv;
    const auto& p_hv = pars.hv;

    real_type dt = 1/opts.hts_per_year;
    real_type value = 0;
   
    nda::fill(i_hv.new_vaccinations, 0.0);
    nda::fill(i_hv.vac_params, 0.0);

    real_type temp1 = 0;
    real_type temp2 = 0;

    real_type temp3 = 0;
    real_type temp4 = 0;
    real_type temp5 = 0;
    real_type temp6 = 0;
    real_type temp7 = 0;
    real_type temp8 = 0;

    //unvaccinated
    for (int s = S_MALE; s <= S_FEMALE; ++s)
    {
     
        temp1=n_hv.adults_ts(VAC_UNV,RG_NONE,CD4_NEG,s);
        temp2=n_hv.adults_ts(VAC_UNV,RG_NONE,CD4_ALL,s);

        temp3=i_hv.dp_entrants_age_15(POP_H_HIVNeg,CD4_NEG,s);
        temp4=(
        ( (std::max(p_hv.b_age_first_sex(S_OFFSET+s,t) - 15.0, 1.0)!=0)? 1/std::max(p_hv.b_age_first_sex(S_OFFSET+s,t) - 15.0, 1.0) : 0) +
        i_hv.background_death_rate(s) + 
        i_hv.rate_aging_50(POP_H_HIVNeg,CD4_NEG,s) + 
        i_hv.migration_rate(s) );
        
        temp5=i_hv.background_death_rate(s);
        temp6=i_hv.rate_aging_50(POP_H_HIVNeg,CD4_NEG,s);
        temp7=((i_hv.vac_params(VAC_DUR)!=0)? 1 / i_hv.vac_params(VAC_DUR) : 0);
        temp8=p_hv.b_age_first_sex(S_OFFSET+s,t);

         auto dbg_model = capture_model(state_next, intermediate, pars);

         nda_print_info(dbg_model.hv.b_age_first_sex);
     
        value = 
        n_hv.adults_ts(VAC_UNV,RG_NONE,CD4_NEG,s) + dt*(
        //new entrants 15 yrs , note that they are not vaccinated by assumption
        i_hv.dp_entrants_age_15(POP_H_HIVNeg,CD4_NEG,s) -
        //exits and migration
        n_hv.adults_ts(VAC_UNV,RG_NONE,CD4_NEG,s) * (
        ((std::max(p_hv.b_age_first_sex(S_OFFSET+s,t) - 15.0, 1.0)!=0)? 1/std::max(p_hv.b_age_first_sex(S_OFFSET+s,t) - 15.0, 1.0) : 0) +
        i_hv.background_death_rate(s) + 
        i_hv.rate_aging_50(POP_H_HIVNeg,CD4_NEG,s) + 
        i_hv.migration_rate(s) ) -

        //new vaccinations
        i_hv.new_vaccinations(RG_NONE,CD4_NEG,s) + // *
        //c_hv.adults(VAC_UNV,RG_NONE,CD4_NEG,s) *
        //(c_hv.adults(VAC_UNV,RG_NONE,CD4_ALL,s)!=0)? 1/ c_hv.adults(VAC_UNV,RG_NONE,CD4_ALL,s) : 0 +
      
        //vaccine waning, entrants
        (n_hv.adults_ts(VAC_TAKE,RG_NONE,CD4_NEG,s) +
          n_hv.adults_ts(VAC_PARTIAL,RG_NONE,CD4_NEG,s) +
          n_hv.adults_ts(VAC_NO_PROT,RG_NONE,CD4_NEG,s)) *
        ( (i_hv.vac_params(VAC_DUR)!=0)? 1 / i_hv.vac_params(VAC_DUR) : 0)  );

        if(value<0) value=0;
        n_hv.adults(VAC_UNV,RG_NONE,CD4_NEG,s) = value;

        //keep track of deaths
        n_hv.deaths(VAC_UNV,RG_NONE,CD4_NEG,s) += dt*n_hv.adults_ts(VAC_UNV,RG_NONE,CD4_NEG,s)*
                                                     i_hv.background_death_rate(s);


        //vaccinated
        for (int v = VAC_TAKE; v <= VAC_NO_PROT; ++v)
        {
              value = 
              n_hv.adults_ts(v,RG_NONE,CD4_NEG,s) + dt*( -
              //exits and migration
              n_hv.adults_ts(v,RG_NONE,CD4_NEG,s) * (
              ((std::max(p_hv.b_age_first_sex(S_OFFSET+s,t) - 15.0, 1.0)!=0)? 1/std::max(p_hv.b_age_first_sex(S_OFFSET+s,t) - 15.0, 1.0) : 0) +
              i_hv.background_death_rate(s) + 
              i_hv.rate_aging_50(POP_H_HIVNeg,CD4_NEG,s) - 
              i_hv.migration_rate(s) ) + 

              //new vaccinations
              i_hv.new_vaccinations(RG_NONE,CD4_NEG, s) * i_hv.vac_effect(p_hv.rn_vac_targetting,v) -
               - // *
              //temp1 * (temp2!=0)? 1 / temp2 : 0 -
            
              //vaccine, exits
              n_hv.adults_ts(v,RG_NONE,CD4_NEG,s)*
              ((i_hv.vac_params(VAC_DUR)!=0)? 1 / i_hv.vac_params(VAC_DUR) : 0)  );

              if(value<0) value=0;
              n_hv.adults(v,RG_NONE,CD4_NEG,s)=value;

              //keep track of deaths
              n_hv.deaths(v,RG_NONE,CD4_NEG,s) += dt*n_hv.adults_ts(v,RG_NONE,CD4_NEG,s)*
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
          
          if (s == S_FEMALE && rg >= RG_MSM) continue; 
          
          temp1=c_hv.adults(VAC_UNV,rg,CD4_NEG,s);
          temp2=c_hv.adults(VAC_UNV,rg,CD4_ALL,s);

          value = 
          c_hv.adults(VAC_UNV,rg,CD4_NEG,s) + dt*(
          
           //no risk at sexual debut
           c_hv.adults(VAC_UNV,RG_NONE,CD4_NEG,s) *
           (std::max(p_hv.b_age_first_sex(S_OFFSET+s,t) - 15.0, 1.0)!=0)? 1/std::max(p_hv.b_age_first_sex(S_OFFSET+s,t) - 15.0, 1.0) : 0 *
           i_hv.b_riskgroup_proportions(rg,s) -
           
          //exits and migration
          c_hv.adults(VAC_UNV,rg,CD4_NEG,s) * (
          i_hv.background_death_rate(s) + 
          i_hv.rate_aging_50(POP_H_HIVNeg,CD4_NEG,s) +
          i_hv.b_behave_change_rate(rg,s) - 
          i_hv.migration_rate(s) ) -

          //new vaccinations
          i_hv.new_vaccinations(rg,CD4_NEG,s) + // *
          //c_hv.adults(VAC_UNV,rg,CD4_NEG,s) *
          //(c_hv.adults(VAC_UNV,rg,CD4_ALL,s)!=0)? 1/ c_hv.adults(VAC_UNV,rg,CD4_ALL,s) : 0 +
        
          //vaccine waning, entrants
          (c_hv.adults(VAC_TAKE,rg,CD4_NEG,s) +
            c_hv.adults(VAC_PARTIAL,rg,CD4_NEG,s) +
            c_hv.adults(VAC_NO_PROT,rg,CD4_NEG,s)) *
          (i_hv.vac_params(VAC_DUR)!=0)? 1 / i_hv.vac_params(VAC_DUR) : 0 +  
        
          //entrants following behavior change
          c_hv.adults(VAC_UNV,rg-1,CD4_NEG,s) * i_hv.b_behave_change_rate(rg-1,s) );

          if(value<0) value=0;
          n_hv.adults(VAC_UNV,rg,CD4_NEG,s) = value;

          //keep track of deaths
          n_hv.deaths(VAC_UNV,rg,CD4_NEG,s) += dt*n_hv.adults_ts(VAC_UNV,rg,CD4_NEG,s)*
                                               i_hv.background_death_rate(s);
                                                    

          //vaccinated
          for (int v = VAC_TAKE; v <= VAC_NO_PROT; ++v)
          {
                value = 
                c_hv.adults(v,rg,CD4_NEG,s) + dt*( -
                //exits and migration
                c_hv.adults(v,rg,CD4_NEG,s) * (
                i_hv.background_death_rate(s) + 
                i_hv.rate_aging_50(POP_H_HIVNeg,CD4_NEG,s) -
                i_hv.b_behave_change_rate(rg,s) - 
                i_hv.migration_rate(s) ) -

                //new vaccinations
                i_hv.new_vaccinations(rg,CD4_NEG,s) * i_hv.vac_effect(p_hv.rn_vac_targetting,v) - // *
                //temp1 * (temp2!=0)? 1 / temp2 : 0 -
              
                //vaccine, exits
                c_hv.adults(v,rg,CD4_NEG,s)*
                (i_hv.vac_params(VAC_DUR)!=0)? 1 / i_hv.vac_params(VAC_DUR) : 0  +

                //entrants following behavior change
                c_hv.adults(VAC_UNV,rg-1,CD4_NEG,s) * i_hv.b_behave_change_rate(rg-1,s) ); 

                if(value<0) value=0;
                n_hv.adults(v,rg,CD4_NEG,s)=value;

                //keep track of deaths
                n_hv.deaths(v,rg,CD4_NEG,s) += dt*n_hv.adults_ts(v,rg,CD4_NEG,s)*
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
          
          if (s == S_FEMALE && rg >= RG_MSM) continue;

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

          //temp1=n_hv.adults(VAC_UNV,rg,CD4_NEG,s);
          //temp2=n_hv.adults(VAC_UNV,rg,CD4_ALL,s);

          value = 
          n_hv.adults(VAC_UNV,rg,hd,s) + dt*(
          
          //no risk at sexual debut
           n_hv.adults(VAC_UNV,RG_NONE,hd,s) *
           (std::max(p_hv.b_age_first_sex(S_OFFSET+s,t) - 15.0, 1.0)!=0)? 1/std::max(p_hv.b_age_first_sex(S_OFFSET+s,t) - 15.0, 1.0) : 0 *
           i_hv.b_riskgroup_proportions(rg,s) -
           
          //exits and migration
          n_hv.adults(VAC_UNV,rg,hd,s) * (
          i_hv.background_death_rate(s) + 
          mort_hiv + //hiv mortality rate
          progress_out + //hiv progrssion rate 
          rate_aging_out + // aging out at age 50
          i_hv.b_behave_change_rate(rg,s) - 
          i_hv.migration_rate(s) ) -

          //new vaccinations
          i_hv.new_vaccinations(rg,hd,s) + //*
          //n_hv.adults(VAC_UNV,rg,CD4_NEG,,s) *
         // (n_hv.adults(VAC_UNV,rg,CD4_ALL,s)!=0)? 1/ n_hv.adults(VAC_UNV,rg,CD4_ALL,s) : 0 +
        
          //vaccine waning, entrants
          (n_hv.adults(VAC_TAKE,rg,hd,s) +
            n_hv.adults(VAC_PARTIAL,rg,hd,s) +
            n_hv.adults(VAC_NO_PROT,rg,hd,s)) *
          (i_hv.vac_params(VAC_DUR)!=0)? 1 / i_hv.vac_params(VAC_DUR) : 0 +  
        
          //entrants following behavior change
          n_hv.adults(VAC_UNV,rg-1,hd,s) * i_hv.b_behave_change_rate(rg-1,s) +

          //entrants following hiv stage progression
          n_hv.adults(VAC_UNV,rg,hd-1,s) * progress_in);

          if(value<0) value=0;
          n_hv.adults(VAC_UNV,rg,hd,s) = value;

          //keep track of deaths
          n_hv.deaths(VAC_UNV,rg,hd,s) += dt*n_hv.adults_ts(VAC_UNV,rg,hd,s)*
                                            (i_hv.background_death_rate(s)+mort_hiv);

          //vaccinated
          for (int v = VAC_TAKE; v <= VAC_NO_PROT; ++v)
          {
                value = 
                n_hv.adults(v,rg,hd,s) + dt*( -
                //exits and migration
                n_hv.adults(v,rg,hd,s) * (
                i_hv.background_death_rate(s) + 
                mort_hiv + //hiv mortality rate
                progress_out + //hiv progrssion rate 
                rate_aging_out + // aging out at age 50
                i_hv.migration_rate(s) ) -

                //new vaccinations
                i_hv.new_vaccinations(rg,hd,s)  * i_hv.vac_effect(p_hv.rn_vac_targetting,v) - // *
                //temp1 * (temp2!=0)? 1 / temp2 : 0 -
              
                //vaccine, exits
                n_hv.adults(v,rg,hd,s)*
                (i_hv.vac_params(VAC_DUR)!=0)? 1 / i_hv.vac_params(VAC_DUR) : 0  +

                //entrants following behavior change
                n_hv.adults(v,rg-1,hd,s) * i_hv.b_behave_change_rate(rg-1,s) +
              
                //entrants following hiv stage progression
                n_hv.adults(VAC_UNV,rg,hd,s) * progress_in); 

                if(value<0) value=0;
                n_hv.adults(v,rg,hd,s)=value;

                //keep track of deaths
                n_hv.deaths(v,rg,hd,s) += dt*n_hv.adults_ts(v,rg,hd,s)*
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
  double rMultNumerator   = 0.0;
  double rMultDenominator = 0.0;
  double rMultNumeratorAll = 0.0;
  double rMultDenominatorAll = 0.0;
  
  //CDP check goals calc
  double vaccine_factor = 1.0 -  p_hv.rn_vac_params(VAC_EFF) * 
                                 (n_hv.adults(VAC_ALL,RG_ALL,CD4_ALL,S_ALL)-n_hv.adults(VAC_UNV,RG_ALL,CD4_ALL,S_ALL))
                                 /n_hv.adults(VAC_ALL,RG_ALL,CD4_ALL,S_ALL);                  


  nda::fill(n_hv.r_mult, 1.0); //default multiplier

  for (int s = S_MALE; s <= S_FEMALE; ++s)
  {
      for (int rg = RG_LRH; rg <= RG_MSM; ++rg)
      {
        
        if (rg == RG_IDU) continue; //IDU force of infection is external input 
        if (s == S_FEMALE && rg >= RG_MSM) continue; //no female MSM
        
          rMultNumerator   = 0.0;
          rMultDenominator = 0.0;

          // not on ART
          for (int hd = CD4_PRIM ; hd <=CD4_LT50 ; ++hd)
          {
              rMultNumerator   += n_hv.mult_no_art(hd) * n_hv.adults(VAC_ALL,rg,hd,s);
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
            n_hv.r_mult(rg, s) = vaccine_factor * (rMultNumerator / rMultDenominator) / rMultEqlb;
                                
          }

      }//r

   }//s

    if (rMultDenominatorAll > 0.0)
    {
      n_hv.r_mult(RG_ALL, S_ALL) = vaccine_factor * (rMultNumeratorAll / rMultDenominatorAll) / rMultEqlb;                                       
    }

}

void calc_prevalence()
{
   
   real_type denom=0;
   real_type plhiv=0;
   
   auto& n_hv = state_next.hv;
   for (int s = S_MALE; s <= S_FEMALE; ++s)
        for (int rg = RG_NONE; rg <= RG_ALL; ++rg)
        {
           denom=0;
           plhiv=0; 
           for (int v = VAC_UNV; v <= VAC_ALL; ++v)
           {
              for (int hd = CD4_NEG; hd <= CD4_LT50_ART; ++hd)
              {
  
                  // Exclude female MSM and higher risk groups
                  if (!((s == S_FEMALE) && (rg >= RG_MSM)))
                  {
                      denom += n_hv.adults(VAC_ALL,rg,hd,s);
                      if(hd>=CD4_PRIM)
                        plhiv += n_hv.adults(VAC_ALL,rg,hd,s); 
                  }
              }

            }
              
              if(denom>0)
                n_hv.prevalence(rg,s) = plhiv/denom;
                  
        }//s,rg    

}

void calc_new_infections(int t)
{

//from goals
auto& n_hv = state_next.hv;
auto& i_hv = intermediate.hv; 
const auto& p_hv = pars.hv;   

double totalSexActs  = 0.0;
double totalSexActsF = 0.0;
double totalSexActsM = 0.0;

double PrevM  = 0.0;
double PrevF  = 0.0;
double PrevML = 0.0;
double PrevFL = 0.0;
double denom  = 0.0;

double rMultM =1;
double rMultF =1;

double foi = 0;

// Sex‑acts ratio, toggled by balanceSexActs
double SexActsRatioM   = 1.0;
double SexActsRatioF   = 1.0;

//for idu
double PrevM_IDU =0;
double PrevF_IDU =0;

double rMultM_IDU =1;
double rMultF_IDU =1;

double SexActsRatioM_IDU =1;
double SexActsRatioF_IDU =1;

double circum=p_hv.rn_coverage(INTVN_MC15_49,t);

for (int rg = RG_LRH; rg <= RG_HRH; ++rg)
{

    if (rg == RG_LRH)
    {
     
      totalSexActsF = n_hv.adults(VAC_ALL,RG_LRH,CD4_ALL,S_FEMALE) * p_hv.b_num_partners(RG_OFFSET+RG_LRH,t) * p_hv.b_sex_acts(RG_OFFSET+RG_LRH,t);
      PrevFL = n_hv.adults(VAC_ALL,RG_LRH,CD4_ALL,S_FEMALE) * n_hv.prevalence(RG_LRH,S_FEMALE);
      denom = n_hv.adults(VAC_ALL,RG_LRH,CD4_ALL,S_FEMALE) * p_hv.b_married_prop(RG_OFFSET+RG_LRH+RG_NONE_F3,t);
      for (int rg2 = RG_MRH; rg2 <= RG_IDU; ++rg2)
      {
        totalSexActsF +=  n_hv.adults(VAC_ALL,rg2,CD4_ALL,S_FEMALE) * p_hv.b_num_partners(RG_OFFSET+rg2+RG_NONE_F3,t) * p_hv.b_sex_acts(RG_OFFSET+rg2+RG_NONE_F3,t) * p_hv.b_married_prop(RG_OFFSET+rg2+RG_NONE_F3,t);
        PrevFL += n_hv.adults(VAC_ALL,rg2,CD4_ALL,S_FEMALE) * n_hv.prevalence(rg2,S_FEMALE) * p_hv.b_married_prop(RG_OFFSET+rg2+RG_NONE_F3,t);
        denom += n_hv.adults(VAC_ALL,rg2,CD4_ALL,S_FEMALE) * p_hv.b_married_prop(RG_OFFSET+rg2+RG_NONE_F3,t);
      }

      PrevFL = PrevFL/denom;
      PrevF  = PrevFL;

      totalSexActsM = n_hv.adults(VAC_ALL,RG_LRH,CD4_ALL,S_MALE) * p_hv.b_num_partners(RG_OFFSET+rg,t) * p_hv.b_sex_acts(RG_OFFSET+rg,t);
      PrevFL = n_hv.adults(VAC_ALL,RG_LRH,CD4_ALL,S_MALE) * n_hv.prevalence(RG_LRH,S_MALE);
      denom = n_hv.adults(VAC_ALL,RG_LRH,CD4_ALL,S_MALE) * p_hv.b_married_prop(RG_OFFSET+RG_LRH,t);
      for (int rg2 = RG_MRH; rg2 <= RG_MSMIDU; ++rg2)
      {
        totalSexActsF +=  n_hv.adults(VAC_ALL,rg2,CD4_ALL,S_FEMALE) * p_hv.b_num_partners(rg2+RG_NONE_F3,t) * p_hv.b_sex_acts(rg2+RG_NONE_F3,t) * p_hv.b_married_prop(rg2+RG_NONE_F3,t);
        PrevFL += n_hv.adults(VAC_ALL,rg2,CD4_ALL,S_MALE) * n_hv.prevalence(rg2,S_MALE) * p_hv.b_married_prop(RG_OFFSET+rg2,t);
        denom += n_hv.adults(VAC_ALL,rg2,CD4_ALL,S_MALE) * p_hv.b_married_prop(RG_OFFSET+rg2,t);
      } 

       PrevML = PrevML/denom;
       PrevM  = PrevML;
    }
    else
    {
      totalSexActsF = n_hv.adults(VAC_ALL,rg,CD4_ALL,S_MALE) * p_hv.b_num_partners(RG_OFFSET+rg+RG_NONE_F3,t) * p_hv.b_sex_acts(rg+RG_NONE_F3,t);
      totalSexActsM = n_hv.adults(VAC_ALL,rg,CD4_ALL,S_MALE) * p_hv.b_num_partners(RG_OFFSET+rg,t) * p_hv.b_sex_acts(RG_OFFSET+rg,t);

      PrevM = std::max(n_hv.prevalence(rg,S_MALE),PrevML);
      PrevF = std::max(n_hv.prevalence(rg,S_FEMALE),PrevFL);
    }  

    

    // Global multiplier
    rMultM  = n_hv.r_mult(RG_ALL, S_ALL);
    rMultF =  n_hv.r_mult(RG_ALL, S_ALL);

    // Assume equal adjustment for men and women
    double totalSexActs = (totalSexActsM + totalSexActsF) / 2.0;
    SexActsRatioM = (totalSexActsM > 0) ? totalSexActs / totalSexActsM : 1;
    SexActsRatioF = (totalSexActsF > 0) ? totalSexActs / totalSexActsF : 1;

    // Toggle balancing
    if (p_hv.b_balance_sex_acts = 0)
    {
      SexActsRatioM = 1.0;   
      SexActsRatioF = 1.0;  
    }

    // Assuming IDU have medium‑risk sexual behaviour and are exposed to the same risk as HV_MRH
    if (rg == RG_MRH)
    {
      PrevM_IDU   = PrevM;
      PrevF_IDU   = PrevF;

      rMultM_IDU   = rMultM;
      rMultF_IDU   = rMultF;

      SexActsRatioM_IDU = SexActsRatioM;
      SexActsRatioF_IDU = SexActsRatioF;
    }

    
    //men
    int s = S_MALE;

    for (int v = VAC_UNV; v <= VAC_ALL; ++v)
    {
    
       double vacc_effect = 0;

      //no new infections in take category 
      if(v==VAC_TAKE) continue;

      //no_protection category same as un vaccinated
      if(v==VAC_PARTIAL) vacc_effect = 1;

      foi  =    1     - std::pow(
                    PrevF * std::pow(
                          (1 - p_hv.transm_hiv_F * (1-vacc_effect) * rMultF *
                              ((1 - circum) + (1 - p_hv.epi_redwhen_circum(HV_SUCC)) * circum) *
                              (1 + (p_hv.epi_transm_sti_mult - 1) * p_hv.sti_prev(RG_OFFSET+rg,t)) *
                              (1 - p_hv.b_condom_prop(RG_OFFSET+rg,t) * p_hv.condom_effect) *
                              (1 - p_hv.prep_cov(S_OFFSET+S_MALE,RG_OFFSET+rg,t) * i_hv.prep_effect(rg,t)) *
                              (1 - i_hv.cured_prop(rg,S_MALE))
                          ),
                          p_hv.b_sex_acts(RG_OFFSET+rg,t) * SexActsRatioM) + (1 - PrevF),
                          p_hv.b_num_partners(RG_OFFSET+rg,t));
        
      n_hv.new_inf_vrs(v,rg,S_MALE)=foi*n_hv.adults(v,rg,CD4_NEG,S_MALE); 
      

    } //v, S_MALE   

    //women
    int s = S_FEMALE;
    for (int v = VAC_UNV; v <= VAC_ALL; ++v)
    {
    
       double vacc_effect = 0;

      //no new infections in take category 
      if(v==VAC_TAKE) continue;

      //no_protection category same as un vaccinated
      if(v==VAC_PARTIAL) vacc_effect = 1;

      foi  =    1     - std::pow(
                    PrevM * std::pow(
                          (1 - p_hv.epi_transm_hiv_F * p_hv.epi_transm_mult_M * rMultM * //CDP check per act prob
                              ((1 - circum) + (1 - p_hv.epi_redwhen_circum(HV_INF)) * circum) *
                              (1 + (p_hv.epi_transm_sti_mult - 1) * p_hv.sti_prev(RG_OFFSET+rg,t)) * //check index
                              (1 - p_hv.b_condom_prop(RG_OFFSET+rg,t) * p_hv.condom_effect)   *   //
                              (1 - p_hv.prep_cov(S_OFFSET+S_FEMALE,RG_OFFSET,t) * i_hv.prep_effect(rg,t))  *
                              (1 - i_hv.cured_prop(rg,S_FEMALE))
                          ),
                          p_hv.b_sex_acts(RG_OFFSET+rg,t) * SexActsRatioF) + (1 - PrevM),
                          p_hv.b_num_partners(RG_OFFSET+rg,t));
        
      n_hv.new_inf_vrs(v,rg,S_FEMALE)=foi*n_hv.adults(v,rg,CD4_NEG,S_FEMALE); 
      
      
    }//v, S_FEMALE  
    
  
}//rg


for (int rg = RG_MSM; rg <= RG_MSMIDU; ++rg)
{

    //MSM multiplier calculated among MSM groups only
    rMultM =n_hv.r_mult(rg, S_MALE);

    //men
    int s = S_MALE;
    double circum=p_hv.rn_coverage(INTVN_MC15_49,t);

    for (int v = VAC_UNV; v <= VAC_ALL; ++v)
    {
    
       double vacc_effect = 0;

      //no new infections in take category 
      if(v==VAC_TAKE) continue;

      //no_protection category same as un vaccinated
      if(v==VAC_PARTIAL) vacc_effect = 1;

      foi  =    1     - std::pow(
                    PrevM * std::pow(
                          (1 - p_hv.epi_transm_hiv_F * (1-vacc_effect) * rMultM *
                              ((1 - circum) + (1 - p_hv.epi_redwhen_circum(HV_SUCC)) * circum) *
                               p_hv.epi_transm_mult_MSM *
                              (1 + (p_hv.epi_transm_sti_mult - 1) * p_hv.sti_prev(RG_OFFSET+rg,t)) *
                              (1 - p_hv.b_condom_prop(RG_OFFSET+rg,t) * p_hv.condom_effect) *
                              (1 - p_hv.prep_cov(S_OFFSET+S_MALE,RG_OFFSET+rg,t) * i_hv.prep_effect(rg,t)) *
                              (1 - i_hv.cured_prop(rg,S_MALE))
                          ),
                          p_hv.b_sex_acts(RG_OFFSET+rg,t) * SexActsRatioM) + (1 - PrevM),
                          p_hv.b_num_partners(RG_OFFSET+rg,t));
        
      n_hv.new_inf_vrs(v,rg,S_MALE)=foi*n_hv.adults(v,rg,CD4_NEG,S_MALE); 
      

    } //v, S_MALE



} //rg MSM


 int rg = RG_IDU;

  //Assuming IDU have medium risk sexual behavior, see r=HV_MRH above
  PrevM=PrevM_IDU;
  PrevF=PrevF_IDU;
  SexActsRatioM=SexActsRatioM_IDU;
  SexActsRatioF=SexActsRatioF_IDU;

  rMultM = n_hv.r_mult(RG_ALL, S_MALE);
  rMultF = n_hv.r_mult(RG_ALL, S_MALE);

  //IDU risk, partner prevalence calc
  double PrevB = 0;
  if(adults(VAC_ALL,RG_IDU,CD4_ALL,S_MALE) +
            adults(VAC_ALL,RG_IDU,CD4_ALL,S_FEMALE)+
            adults(VAC_ALL,RG_MSMIDU,CD4_ALL,S_MALE)>0)

    PrevB = (n_hv.prevalence(RG_IDU,S_MALE)    * adults(VAC_ALL,RG_IDU,CD4_ALL,S_MALE) +
              n_hv.prevalence(RG_IDU,S_FEMALE)  * adults(VAC_ALL,RG_IDU,CD4_ALL,S_FEMALE)+
              n_hv.prevalence(RG_MSMIDU,S_MALE) * adults(VAC_ALL,RG_MSMIDU,CD4_ALL,S_MALE)) /
            (adults(VAC_ALL,RG_IDU,CD4_ALL,S_MALE) +
            adults(VAC_ALL,RG_IDU,CD4_ALL,S_FEMALE)+
            adults(VAC_ALL,RG_MSMIDU,CD4_ALL,S_MALE));

   PrevB = (p_hv.b_idu_share_prop(t)>0) ? PrevB / p_hv.b_idu_share_prop(t) : PrevB;  
   
   PrevB = std::max(PrevB,  std::min(prevalence(RG_LRH,S_MALE),prevalence(RG_LRH),S_FEMALE)) ;

   double SusceptibleIDU =0;
   double foi_idu_sex=0;
   for (int s = S_MALE; s <= S_FEMALE; ++s)
   {
      for (int v = VAC_UNV; v <= VAC_ALL; ++v)
      {
      
        SusceptibleIDU = adults(v,RG_IDU,CD4_NEG,s); 
        if( SusceptibleIDU > adults(v,RG_IDU,CD4_ALL,s) * p_hv.b_idu_share_prop(t) -
                            (adults(v,RG_IDU,CD4_ALL,s) - adults(v,RG_IDU,CD4_NEG,s)))
        {                    
            SusceptibleIDU = adults(v,RG_IDU,CD4_ALL,s) * p_hv.b_idu_share_prop(t) -
                          (adults(v,RG_IDU,CD4_ALL,s) - adults(v,RG_IDU,CD4_NEG,s));
        }

        double vacc_effect = 0;

        //no new infections in take category 
        if(v==VAC_TAKE) continue;

        //no_protection category same as un vaccinated
        if(v==VAC_PARTIAL) vacc_effect = 1;

        if(s=S_MALE)
        {
    
          foi_idu_sex  =    1     - std::pow(
                        PrevF * std::pow(
                              (1 - p_hv.transm_hiv_F * (1-vacc_effect) * rMultF *
                                  ((1 - circum) + (1 - p_hv.epi_redwhen_circum(HV_SUCC)) * circum) *
                                  (1 + (p_hv.epi_transm_sti_mult - 1) * p_hv.sti_prev(RG_OFFSET+rg,t)) *
                                  (1 - p_hv.b_condom_prop(RG_OFFSET+rg,t) * p_hv.condom_effect) *
                                  (1 - p_hv.prep_cov(S_OFFSET+S_MALE,rg,t) * i_hv.prep_effect(rg,t)) *
                                  (1 - i_hv.cured_prop(rg,S_MALE))
                              ),
                              p_hv.b_sex_acts(RG_OFFSET+rg,t) * SexActsRatioM) + (1 - PrevF),
                              p_hv.b_num_partners(rg,t));
        

        }
        else
        {
          foi_idu_sex  =    1     - std::pow(
                    PrevM * std::pow(
                          (1 - p_hv.epi_transm_hiv_F * p_hv.epi_transm_mult_M * rMultM * //CDP check per act prob
                              ((1 - circum) + (1 - p_hv.epi_redwhen_circum(HV_INF)) * circum) *
                              (1 + (p_hv.epi_transm_sti_mult - 1) * p_hv.sti_prev(RG_OFFSET+rg,t)) * //check index
                              (1 - p_hv.b_condom_prop(RG_OFFSET+rg,t) * p_hv.condom_effect)   *   //
                              (1 - p_hv.prep_cov(S_OFFSET+S_FEMALE,rg,t) * i_hv.prep_effect(rg,t))  *
                              (1 - i_hv.cured_prop(rg,S_FEMALE))
                          ),
                          p_hv.b_sex_acts(RG_OFFSET+rg,t) * SexActsRatioF) + (1 - PrevM),
                          p_hv.b_num_partners(rg,t));
        
          

        }

        //needle sharing
        n_hv.new_inf_vrs(v,rg,s)+= p_hv.b_foi_idu(s,t) * n_hv.r_mult(RG_ALL, S_MALE) * PrevB * SusceptibleIDU *
                                                      (1-p_hv.prep_cov(S_OFFSET+s,RG_OFFSET+rg,t) * i_hv.prep_effect(rg,t));
                                                      //+_ForceNeedleTransmIDU*SusceptibleIDU;//no explicit needle sharing mechanism 
      
        //sexual transmission 
        n_hv.new_inf_vrs(v,RG_IDU,s) += foi_idu_sex * n_hv.adults(v,RG_IDU,CD4_NEG,s);                                             


   }//v                    

  }//s


}



void add_new_infections()
{
    
  //from goals
  auto& n_hv = state_next.hv;

  real_type dt = 1/opts.hts_per_year;
  for (int v = VAC_UNV; v <= VAC_NO_PROT; ++v)            
  {
      for (int rg = RG_LRH; rg <= RG_MSMIDU; ++rg)          
      {
          for (int s = S_MALE; s <= S_FEMALE; ++s) 
          {
  
              if (!((s == S_FEMALE) && (rg >= RG_MSM)))
              {
                  // Remove new infections from HIV‑negative category
                  n_hv.adults(v,rg,CD4_NEG,s) -= dt * n_hv.new_inf_vrs(v,rg,s);
                  n_hv.new_inf_s(s) += dt * n_hv.new_inf_vrs(v,rg,s);


                  // Add new infections to each HIV‑positive stage
                  for (int hd = CD4_PRIM; hd <= CD4_LT50; ++hd)
                  {
                      n_hv.adults(v,rg,CD4_NEG,s) += dt * n_hv.new_inf_vrs(v,rg,s);

                  }
              }
          } //s 
      } //r
  } //v

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

            prop_gt12m = i_hv.dp_aging_denom_1549(POP_H_ARTgt12m, hd, s);
            prop_lt12m = i_hv.dp_aging_denom_1549(POP_H_ARTlt6m, hd, s)+
                         i_hv.dp_aging_denom_1549(POP_H_ART6to12m, hd, s);

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
  sex_age_hiv[POP_H_NoART][s] = 0;
  sex_age_hiv[POP_H_OnART][s] = 0;
  for (int hd = CD4_GT500; hd <= CD4_LT50; ++hd) {
        sex_age_hiv[POP_H_NoART][s] += i_hv.dp_(POP_H_NoART, hd, s);
        sex_age_hiv[POP_H_OnART][s] += i_hv.dp_aging_denom_1549(POP_H_OnART, hd, s);
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

    for (int v = VAC_UNV; v <= VAC_NO_PROT; ++v)
    {
        for (int rg = RG_NONE; rg <= RG_MSMIDU; ++rg)
        {
            for (int hd = CD4_NEG; hd <= CD4_LT50_ART; ++hd)
            {
               real_type sum = 0.0;
               for (int s = S_MALE; s <= S_FEMALE; ++s)
               {
                    // Exclude female MSM and higher risk groups
                    //if (!((s == S_FEMALE) && (rg >= RG_MSM) && (rg <= RG_MSMIDU)))
                        sum += n_hv.adults(VAC_ALL,rg,hd,s);
                } //s
                
                //if(sum>0){
                  n_hv.adults(v,rg,hd,S_ALL) = sum;
                // }

            } //hd
         } //rg
      }//v

    for (int v = VAC_UNV; v <= VAC_NO_PROT; ++v)
     {
          for (int rg = RG_NONE; rg <= RG_MSMIDU; ++rg)
          {
              for (int s = S_MALE; s <= S_ALL; ++s)
              {
                  real_type sum = 0.0;
                  for (int hd = CD4_NEG; hd <= CD4_LT50_ART; ++hd)
                  {
                      // Exclude female MSM and higher risk groups
                      //if (!((s == S_FEMALE) && (rg >= RG_MSM) && (rg <= RG_MSMIDU)))
                          sum += n_hv.adults(v,rg,hd,s);
                  }//hd
                  if(sum>0){
                    n_hv.adults(v,rg,CD4_ALL,s) = sum;
                  }

              } //s
            } //rg
        }//v
    
             
       for (int v = VAC_UNV; v <= VAC_NO_PROT; ++v)
       {
          for (int hd = CD4_NEG; hd <= CD4_ALL; ++hd)
          {
              for (int s = S_MALE; s <= S_ALL; ++s)
              {
                  real_type sum = 0.0;
                  for (int rg = RG_NONE; rg <= RG_MSMIDU; ++rg)
                  {
                      // Exclude female MSM and higher risk groups
                      //if (!((s == S_FEMALE) && (rg >= RG_MSM) && (rg < RG_ALL)))
                          sum += n_hv.adults(v,rg,hd,s);
                  }//hd

                  //if(sum>0){
                    n_hv.adults(v,RG_ALL,hd,s) = sum;
                  // } 
                    
              }//v
            }//rg
        }//s
            
        
        for (int rg = RG_NONE; rg <= RG_ALL; ++rg)
        {
          for (int hd = CD4_NEG; hd <= CD4_ALL; ++hd)
          {
              for (int s = S_MALE; s <= S_ALL; ++s)
              {
                  real_type sum = 0.0;
                  for (int v = VAC_UNV; v <= VAC_NO_PROT; ++v)
                  {
                      // Exclude female MSM and higher risk groups
                      //if (!((s == S_FEMALE) && (rg >= RG_MSM) && (rg < RG_ALL)))
                          sum += n_hv.adults(v,rg,hd,s);
                  }//v
                  
                  n_hv.adults(VAC_ALL,rg,hd,s) = sum;

              }//s
            }//hd
        }//rg              
/*  
    real_type temp1 = 0;
    real_type temp2 = 0;
    real_type temp3 = 0;

    temp1=n_hv.adults(VAC_UNV,RG_NONE,CD4_NEG,S_MALE);
    temp1=n_hv.adults(VAC_UNV,RG_NONE,CD4_NEG,S_FEMALE);
    temp2=n_hv.adults(VAC_UNV,RG_NONE,CD4_ALL,S_MALE);
    temp3=n_hv.adults(VAC_UNV,RG_ALL,CD4_ALL,S_MALE); */


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