#pragma once

#include "../options.hpp"
#include "../generated/config_mixer.hpp"
#include "../model_debugger.hpp"

#include <list>
#include <iostream>

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
      //S_OFFSET =1, //offset of 1 with respect to goals inputs

      //Risk Groups
      RG_NONE = 0,
      RG_LRH = 1,
      RG_MRH = 2,
      RG_HRH = 3,
      RG_IDU = 4,
      RG_MSM = 5,
      RG_TOTAL1 = 5,
      RG_TOTAL_ART = 6,
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
      //RG_OFFSET = 1, //offset of 1 with respect to goals inputs

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

      ART_GT12m = 2,

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

      VAC_COV_ALLRISK       = 0,
      VAC_COV_SINGLE        = 1,

      CURE_COV_ALLRISK       = 0,
      CURE_COV_SINGLE        = 1,

      ART_NUM_PERCENT       =0,
      ART_CD4_PERCENT       =1,
      ART_CD4_NUMBER        =2,
      ART_NEW_PATS          =3,
      ART_RG_PERCENT        =4,

      POC_CD4 = 0,
      POC_VL  = 1,

      HV_SUCC = 0,
      HV_INF  = 1,

      INTVN_MC15_49 = 26,
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
      PREP_DUR  = 3,

  
      //Intervention mapping
      RN_COM_MOB          = 1,
      RN_MASS_MEDIA       = 2,
      RN_HTS              = 3,
      RN_CONDOMS          = 4,
      RN_PRIM_TEACH       = 5,
      RN_COMP_SEX_EDUC    = 6,
      RN_OUT_OF_SCHOOL    = 7,
      RN_ECON_STRENGTH    = 8,
      RN_WORK_PLACE_STI   = 9,

      //Most At-Risk populations
      RN_FSW_OUTREACH     = 10,
      RN_MSW              = 11,
      RN_MSM_OUTREACH     = 12,
      RN_MSM_LUB          = 13,
      RN_IDU_HARM_RED     = 14,
      RN_IDU_CandT        = 15,
      RN_IDU_OUTREACH     = 16,
      RN_IDU_NSEP         = 17,
      RN_IDU_DRUG_SUB     = 18,
      //Male circumcision
      RN_MC15_49          = 19,
      RN_NUM_VMMC         = 20,
      RN_MC_INFANT        = 21,
      //PrEP
      RN_PrEP_OralDaily    = 22,
      RN_PrEP_OralMonthly  = 23,
      RN_PrEP_OralPlusCon  = 24,
      RN_PrEP_Inject1Mo    = 25,
      RN_PrEP_Inject2Mo    = 26,
      RN_PrEP_Inject6Mo    = 27,
      RN_PrEP_Ring         = 28,
      RN_PrEP_bNABs        = 29,
      RN_PrEP_Implant      = 30,
      RN_PrEP_PEP          = 31,

      // Medical services for Coverage
      RN_MALE_STITx       = 32,
      RN_FEMALE_STITx     = 33,
      RN_BLOOD_SAFE       = 34,
      RN_PEP              = 35,
      RN_ADSYRYNGE        = 36,
      RN_RED_INJECT       = 37,
      RN_UNIV_PREC        = 38,
      //Vaccines
      RN_VACCINES         = 39,
      RN_CURE             = 40,
      RN_AHD_TX           = 41,
      RN_POC_CD4_INT      = 42,
      RN_POC_VL_INT       = 43,
      //PMTCT
      RN_HIV_TEST_ANC      = 44,
      RN_HIV_WOMAN_COUNS   = 45,
      RN_EXPOSED_INFANT_Dx = 46,
      RN_ADULT_ON_ART      = 47,
      RN_CHILD_ON_ART      = 48,

      //new interventions in general pop section
      RN_CONDOM_SUPPLY     = 49,
      RN_ANC_TESTING       = 50,
      RN_MAX_INTERVN       = 50,

      RN_DIRECT_COSTS      = 51,
      RN_PROGRAM_COSTS     = 52,
      RN_TOTAL_COSTS       = 53,
      RN_MAX_COSTS         = 53,

      RN_MAX_BEHAV_INTVN   = RN_IDU_DRUG_SUB,

      //behaviour intervention impacts
      HV_IM_CONDOMS_HIGH        = 1,
      HV_IM_CONDOMS_MED         = 2,
      HV_IM_CONDOMS_LOW         = 3,
      HV_IM_CONDOMS_MSM         = 4,
      HV_IM_CONDOMS_IDU         = 5,
      HV_IM_CONDOMS_MSM_HIGH    = 6,
      HV_IM_CONDOMS_MSM_MED     = 7,
      HV_IM_CONDOMS_MSM_LOW     = 8,
      HV_IM_CONDOMS_MSM_IDU     = 9,
      HV_IM_PARTNERS_HIGH       = 10,
      HV_IM_PARTNERS_MED        = 11,
      HV_IM_PARTNERS_LOW        = 12,
      HV_IM_PARTNERS_MSM        = 13,
      HV_IM_PARTNERS_IDU        = 14,
      HV_IM_PARTNERS_MSM_HIGH   = 15,
      HV_IM_PARTNERS_MSM_MED    = 16,
      HV_IM_PARTNERS_MSM_LOW    = 17,
      HV_IM_PARTNERS_MSM_IDU    = 18,
      HV_IM_AGE_FIRST_SEX       = 19,
      HV_IM_UNSAFE_INJECT_IDU   = 20,
      HV_IM_NEEDLE_SHARING_IDU  = 21,
      HV_IM_NEEDLE_SHARING_MSIDU= 22,
      HV_IM_NUM_SHARING_PARTNERS= 23,

      HV_MAX_BEHAV_IMPACTS       = 23,

      RN_POP_CONDOM_WASTAGE        = 8,
      RN_POP_SEC_SCHOOL_MALE       = 12,
      RN_POP_SEC_SCHOOL_FEMALE     = 13,
      RN_POP_Rapes                 = 17,
      RN_POP_IDU_OPIOD_DEP         = 22,
      RN_POP_NUM_INJECT_YEAR       = 23,
      RN_POP_PEPKitsRequired       = 30,

      DP_EligTreatPregnantWomen       = 1,
      DP_EligTreatTB_HIV              = 2,
      DP_EligTreatDiscordantCouples   = 3,
      DP_EligTreatSexWorkers          = 4,
      DP_EligTreatMSM                 = 5,
      DP_EligTreatIDU                 = 6,
      DP_EligTreatOtherPop            = 7,
      DP_EligTreatPopsMax             = 7,

    
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

    const auto& p_hv = pars.hv;
    auto& n_hv = state_next.hv;
    const auto& c_hv = state_curr.hv;
    auto& i_hv = intermediate.hv;

    //initialize annual variables
    init_vars_pre_hiv_loop(t);


    //check goals inputs
    //print_goals_inputs();

    //set coverage chnage for impact adj
    //if(t>p_hv.goals_base_year_idx){
    if(t>=1){
      //calc_adj_matrix(t);
      //calc_behav_matrix_impacts();
    }

    //set risk group sizes from inputs
    //CDP move to t==1 when new variable type than intermediate is available
    set_riskgroup_proportions();

    //initilize adult population
    if(t==1){
      set_initial_pop();
    }
    
    if(t>1){

      //next state variables are cleared, make copy from current
      for (int v = VAC_UNV; v <= VAC_ALL; ++v)
            for (int rg = RG_NONE; rg <= RG_ALL; ++rg)
                for (int hd = CD4_NEG; hd <= CD4_ALL; ++hd)
                  for (int s = S_MALE; s <= S_ALL; ++s){
                      n_hv.adults(v,rg,hd,s)=c_hv.adults(v,rg,hd,s);
  
                  }

      //next state variables are cleared, make copy from current            
      for (int rg = RG_NONE; rg <= RG_MSMIDU; ++rg)
        for (int s = S_MALE; s <= S_FEMALE; ++s){
            n_hv.cured_pop(rg, s)=c_hv.cured_pop(rg, s);
        }

    }


    //at hiv first year, apply initial pulse, t starts at 0
    //int proj_start_year = opts.proj_start_year;
    if(t==(p_hv.epi_start_year-opts.proj_start_year)){ //CDP reinstate correct time for pulse
       std::cout << "initial pulse at: t " << t  << " " << std::endl;
       nda::fill(n_hv.new_infections_goals, 0.0);//incidence for DP, init at initial pulse
       set_initial_pulse();
    }


    //set these rates to vars in goals
    if(t>p_hv.goals_base_year_idx){
      calc_HIV_cure(t);
      calc_HIV_mort_adjustments(t);
    }

  }

   void run_goals_hiv_loop(int hiv_step) {

    const auto& p_hv = pars.hv;
    auto& n_hv = state_next.hv;
    auto& i_hv = intermediate.hv;
    
  
    //initialize inner loop varaibles
    init_vars_hiv_loop();

    //sum over the dimensions of adult pop
    sum_adult_pop_dims(t);

    //set these rates to vars in goals
    if((hiv_step ==0) && (t>p_hv.goals_base_year_idx)){
     //calc_new_vaccinations(t);
    }

    //make inner-time loop copy of adult structure
    set_adults_hiv_loop();

    //collect info from dp/aim to set demographical and HIV rates
    set_goals_vars_from_dp(t);

    //set the rates to vars in goals, including progression, aging and mortality
    calc_goals_rates(t,hiv_step);

    //adjust distribution of new entrants into different risk groups
    if( t>=2 ) //&& hiv_step=0
      calc_newrecruits_distribution(t);


    //calc prevalence used for new infections calc
    calc_prevalence(t,hiv_step);

    //calc multiplier and new infections
    if(t>=(p_hv.epi_start_year-opts.proj_start_year)){
      //std::cout << "calc multiplier at: t " << t  << " " << std::endl;
      calc_r_multiplier(t);
      //std::cout << "calc new inf at: t " << t  << " " << std::endl;
      calc_new_infections(t,hiv_step);
    }


    //progress, hiv-neg, not at risk (RG_NONE)
    progress_norisk_hiv_neg(t,hiv_step);

    //progress, hiv-neg, at risk (RG_LRH..RG_MSM)
    progress_atrisk_hiv_neg(t);

    //progress, hiv-pos and hiv-art (RG_LRH..RG_MSM)
    progress_hivp_and_art(t);//CDP can split ART progression out, so it can be run when t >= opts.ts_art_start
    
     //sum over the dimensions of adult pop
    sum_adult_pop_dims(t);

    //add new infections
    if(t>=(p_hv.epi_start_year-opts.proj_start_year)){
      add_new_infections(t,hiv_step);
      //add_new_infections_goals(t, hiv_step);
    }  

    //sum over the dimensions of adult pop
    sum_adult_pop_dims(t);

    //calc prevalence used for new infections calc
    //calc_prevalence(t,hiv_step);

    //ART allocation
    if (t >= opts.ts_art_start)
     allocate_art(t);

  }

  void run_goals_post_hiv_loop() {
    const auto& p_hv = pars.hv;

    //sum over the dimensions of adult pop
    sum_adult_pop_dims(t); 

    //set yearly goals outputs
    set_goals_outputs(t);

    if(t>p_hv.goals_base_year_idx){
      //calc_resource_needs();
    }

  }

  void set_goals_outputs(int t) {

     /* 
     Outputs to compare between leapfrog goals and spectrum delphi goals:  
     
     n_hv.total_population: total population 15-49 both sexes

     n_hv.total_deaths: total deaths both sexes, all hiv states
     n_hv.total_deaths_hiv: total deaths both sexes, PLHIV

     n_hv.incidence_goals(S_ALL): incidence for both sexes [0,1]
     n_hv.new_infections_goals(S_ALL): new infections both sexes [0,1]

     n_hv.prevalence(RG_ALL,S_ALL): prevalence for both sexes [0,1] 
     */
     
    auto& n_hv = state_next.hv;
    auto& i_hv = intermediate.hv;
    const auto& c_hv = state_curr.hv;

    n_hv.total_population = n_hv.adults(VAC_ALL,RG_ALL,CD4_ALL,S_MALE)+n_hv.adults(VAC_ALL,RG_ALL,CD4_ALL,S_FEMALE);

    //toggle continue here:
    //return;
  

    double total_pop=n_hv.total_population;
    std::cout << "pop goals: t " << t << " " << total_pop << " " << std::endl;

    total_pop= i_hv.dp_pop_1549(S_MALE)+i_hv.dp_pop_1549(S_FEMALE);

    std::cout << "pop dp: t " << t << " " << total_pop << " " << std::endl;

    double deaths=n_hv.total_deaths;

    std::cout << "total deaths goals: t " << t << " " << deaths << " " << std::endl;

    double hiv_deaths=n_hv.total_deaths_hiv;

    std::cout << "total deaths hiv goals: t " << t << " " << hiv_deaths << " " << std::endl;

    double inci=n_hv.incidence_goals(S_MALE);

    std::cout << "hiv incidence goals M (%): t " << t << " " << 100.00*inci << " " << std::endl;

    inci=n_hv.incidence_goals(S_FEMALE);

    std::cout << "hiv incidence goals F (%): t " << t << " " << 100.00*inci << " " << std::endl;

    inci=n_hv.incidence_goals(S_ALL);

    std::cout << "hiv incidence goals (%): t " << t << " " << 100.00*inci << " " << std::endl;

    double new_inf=n_hv.new_infections_goals(S_ALL);

    std::cout << "hiv new inf goals to dp: t " << t << " " << new_inf << " " << std::endl;

    new_inf=n_hv.total_new_infections;

    std::cout << "new inf goals: t " << t << " " << new_inf << " " << std::endl;

    new_inf=n_hv.new_infections_dp;

    std::cout << "new inf dp aim: t " << t << " " << new_inf << " " << std::endl;


    double art_cov = 0.0;
    double on_art  = 0.0;
    for (int hd = CD4_GT500_ART; hd <= CD4_LT50_ART; ++hd){
       on_art += n_hv.adults(VAC_ALL,RG_ALL,hd,S_ALL);
    } 
    //double plhiv  = n_hv.adults(VAC_ALL,RG_ALL,CD4_ALL,S_ALL)-n_hv.adults(VAC_ALL,RG_ALL,CD4_NEG,S_ALL);
    double plhiv  =   n_hv.adults(VAC_ALL,RG_ALL,CD4_ALL,S_MALE)+n_hv.adults(VAC_ALL,RG_ALL,CD4_ALL,S_FEMALE) -
                      n_hv.adults(VAC_ALL,RG_ALL,CD4_NEG,S_MALE)-n_hv.adults(VAC_ALL,RG_ALL,CD4_NEG,S_FEMALE); 

    if(plhiv>0.0){
      art_cov=on_art/plhiv;
    }  

    std::cout << "art cov goals (%) t " << t << " " << 100.00*art_cov << " " << std::endl;

    std::cout << "art number: t " << t << " " << on_art << " " << std::endl;

    std::cout << "plhiv number: t " << t << " " << plhiv << " " << std::endl;

    double prev = plhiv/n_hv.total_population;

    std::cout << "prev goals1 (%) t " << t << " " << 100.00*prev << " " << std::endl;

    prev = n_hv.prevalence(RG_ALL,S_ALL);//n_hv.total_prevalence;

    std::cout << "prev goals2 (%) t " << t << " " << 100.00*prev << " " << std::endl;

    prev = n_hv.prevalence(RG_ALL,S_MALE);

    std::cout << "prev goals M (%) t " << t << " " << 100.00*prev << " " << std::endl;

    prev = n_hv.prevalence(RG_ALL,S_FEMALE);

    std::cout << "prev goals F (%) t " << t << " " << 100.00*prev << " " << std::endl;

     plhiv = i_hv.total_art_adults+i_hv.total_pop_hivpos;
     total_pop   = i_hv.dp_totpop_1549(S_MALE)+i_hv.dp_totpop_1549(S_FEMALE);
     prev=plhiv/total_pop;

     std::cout << "prev dp/aim (%) t " << t << " " << 100.00*prev << " " << std::endl;



  };

 void init_vars_pre_hiv_loop(int t) {

  auto& n_hv = state_next.hv;
  auto& i_hv = intermediate.hv;
  const auto& p_hv = pars.hv;

 nda::fill(i_hv.i_condom_prop, 0.0);//input data, condom use, time t
 nda::fill(i_hv.i_num_partners, 0.0);//input data, number of partners, time t
 nda::fill(i_hv.i_age_first_sex, 0.0);//input data, age first sex, time t
 i_hv.i_idu_share_prop=0.0;//input data, idu sharing,, time t
 

  nda::fill(n_hv.deaths, 0.0);//deaths for each t
  n_hv.total_deaths = 0.0;//deaths for each t
  n_hv.total_deaths_hiv = 0.0;//deaths for each t

  nda::fill(n_hv.new_infections, 0.0);//new infections for each v, rg,  t
  n_hv.total_new_infections=  0.0;//new infections for each  t


  nda::fill(n_hv.new_inf_s, 0.0);//new infections for each t, by sex, for aim
  nda::fill(n_hv.new_infections_goals, 0.0);//incidence for DP
  nda::fill(n_hv.incidence_goals, 0.0); 


  //CDP: temp, using i_hv change back to p_hv
   nda::fill(p_hv.art_coverage_rg, 0.0);


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
      if(t>p_hv.goals_base_year_idx){
        n_hv.mult_art(hd) = p_hv.epi_inf_mult_art(t) * p_hv.epi_infectiousness(INF_SYMPT_NO_ART) *
                            (1 - p_hv.rn_poc_cov(POC_VL,t) * p_hv.rn_poc_effect(POC_VL));
      }  

  }    
  //auto dbg_model = capture_model(state_next, intermediate, pars);
  //nda_print_info(dbg_model.hv.prep_effectiveness);
  
  // nda_print_info(dbg_model.hv.prep_effect);
  // nda_print_info(dbg_model.hv.prep_method_mix);
  
    nda::fill(i_hv.prep_effect, 0.0);
    //if(t>p_hv.goals_base_year_idx){
    if(t>=2000){  
      for (int s = S_MALE; s <= S_FEMALE; ++s){
          for (int rg = RG_LRH; rg <= RG_TOTAL1; ++rg){
            
            if (s == S_FEMALE && rg >= RG_MSM){
              continue;
            } 

            for (int m = PREP_OralDaily; m <= PREP_PEP ; ++m)
            {

                
                double prep_effect = std::clamp(p_hv.prep_effectiveness(PREP_EFFECT, m), 0.0, 1.0);
                double prep_adh = std::clamp(p_hv.prep_effectiveness(PREP_ADH, m), 0.0, 1.0);
                
                i_hv.prep_effect(rg,s) +=  0.0*prep_effect * prep_adh * p_hv.prep_method_mix(s,rg,m,t);
                
                // double temp1=p_hv.prep_effectiveness(PREP_EFFECT, m);
                // double temp2=p_hv.prep_effectiveness(PREP_ADH, m);
                // double temp3=p_hv.prep_method_mix(s,rg,m,t);

                // std::cout << "temp1 " << temp1 << std::endl;
                // std::cout << "temp2 " << temp2 << std::endl;
                // std::cout << "temp3 " << temp3 << std::endl;
                // std::cout << "temp4 " << i_hv.prep_effect(rg,s) << std::endl;

                // double x=0;                             
            }//m
          }//rg
        }//s

      //auto dbg_model = capture_model(state_next, intermediate, pars);
      //nda_print_info(dbg_model.hv.prep_effect);
    }

  
  //mort impact variables 
  i_hv.ADH_Tx_Impact = 1.0;
  i_hv.alpha_mult = 1.0;


  //these behavioral parameters are adjusted by interventions via the impact matrix.
  //copies of the input parameters, which cant be changes, are made for this prupose
  for (int rg = RG_NONE; rg <= RG_MSM_F3; ++rg){
     i_hv.i_condom_prop(rg)=p_hv.b_condom_prop(rg,t);
     i_hv.i_num_partners(rg)=p_hv.b_num_partners(rg,t);
  }  

  i_hv.i_condom_prop(RG_IDU)=p_hv.b_condom_prop(RG_MRH,t);//IDU has MR behavior

  i_hv.i_age_first_sex(S_MALE)=p_hv.b_age_first_sex(S_MALE,t);
  i_hv.i_age_first_sex(S_FEMALE)=p_hv.b_age_first_sex(S_FEMALE,t);

  i_hv.i_idu_share_prop=p_hv.b_idu_share_prop(t);

  //auto dbg_model = capture_model(state_next, intermediate, pars);

  //nda_print_info(dbg_model.hv.i_condom_prop);
  //nda_print_info(dbg_model.hv.i_num_partners);
  //nda_print_info(dbg_model.hv.i_age_first_sex);

  //std::cout << "idu " << i_hv.i_idu_share_prop << std::endl;



 }

  void init_vars_hiv_loop() {

   auto& n_hv = state_next.hv;
  

    nda::fill(n_hv.newly_on_art, 0.0);//art allocation for time step
    nda::fill(n_hv.prevalence, 0.0);//prevalence for each rg,  t

    nda::fill(n_hv.new_inf_vrs, 0.0);//new infections for each t, by v,r,s, for goals

    n_hv.total_prevalence=0;//total prevalence for each t

    auto& i_hv = intermediate.hv;
    
    nda::fill(i_hv.new_vaccinations, 0.0);
    nda::fill(i_hv.vac_effect, 0.0);


 }

   void set_adults_hiv_loop() {

   auto& n_hv = state_next.hv;

    //init time dependent vars
          for (int v = VAC_UNV; v <= VAC_ALL; ++v)
            for (int rg = RG_NONE; rg <= RG_ALL; ++rg)
                for (int hd = CD4_NEG; hd <= CD4_ALL; ++hd)
                  for (int s = S_MALE; s <= S_ALL; ++s){
                    n_hv.adults_ts(v,rg,hd,s)=n_hv.adults(v,rg,hd,s);
                  }

  }

 void print_goals_inputs() {

  auto dbg_model = capture_model(state_next, intermediate, pars);

   //nda_print_info(dbg_model.hv.b_condom_prop);
   //nda_print_info(dbg_model.hv.b_num_partners);
   //nda_print_info(dbg_model.hv.b_age_first_sex);

   //nda_print_info(dbg_model.hv.i_condom_prop);
   //nda_print_info(dbg_model.hv.i_num_partners);
   //nda_print_info(dbg_model.hv.i_age_first_sex);

   //return;


  nda_print_info(dbg_model.hv.b_condom_prop);
  nda_print_info(dbg_model.hv.b_sex_acts);
  nda_print_info(dbg_model.hv.b_num_partners);
  nda_print_info(dbg_model.hv.b_incr_recruit);
  nda_print_info(dbg_model.hv.b_age_first_sex);
  nda_print_info(dbg_model.hv.b_incr_recruit);
  nda_print_info(dbg_model.hv.b_age_first_sex);
  //nda_print_info(dbg_model.hv.epi_sti_prev);
  //nda_print_info(dbg_model.hv.prep_cov);
  //nda_print_info(dbg_model.hv.b_foi_idu);

  // nda_print_info(dbg_model.hv.epi_start_year);
  //nda_print_info(dbg_model.hv.b_balance_sex_acts
  //nda_print_info(dbg_model.hv.epi_months_in_primary);
  //nda_print_info(dbg_model.hv.epi_initial_pulse);
  nda_print_info(dbg_model.hv.b_condom_prop);
 // nda_print_info(dbg_model.hv.b_behav_properties);
  nda_print_info(dbg_model.hv.b_sex_acts);
  nda_print_info(dbg_model.hv.b_num_partners);
  nda_print_info(dbg_model.hv.b_incr_recruit);
  nda_print_info(dbg_model.hv.b_married_prop);
  nda_print_info(dbg_model.hv.b_age_first_sex);
  nda_print_info(dbg_model.hv.b_idu_share_prop);
  nda_print_info(dbg_model.hv.rn_poc_cov);
  nda_print_info(dbg_model.hv.rn_vac_params);
  nda_print_info(dbg_model.hv.rn_vac_coverage_all);
  nda_print_info(dbg_model.hv.epi_infectiousness);
  nda_print_info(dbg_model.hv.epi_inf_mult_art);

  //nda_print_info(dbg_model.hv.rn_vac_cov_type);
  //nda_print_info(dbg_model.hv.rn_vac_targetting);


  // p_hv.epi_start_year;
  //  p_hv.epi_months_in_primary;
  //  p_hv.b_balance_sex_acts;
  //  p_hv.epi_initial_pulse;
 //  p_hv.b_condom_prop;
  //  p_hv.b_behav_properties;
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
      i_hv.b_riskgroup_proportions(rg,S_MALE) = p_hv.b_behav_properties(rg, PERC_POP);
      if (rg > RG_LRH){
        i_hv.b_behave_change_rate(rg,S_MALE) = (p_hv.b_behav_properties(rg, DUR_AVG)!=0) ? 1 / p_hv.b_behav_properties(rg, DUR_AVG) : 0.0;
      }

      if (rg != RG_MSM){
        //CDP note offset for women
        i_hv.b_riskgroup_proportions(rg,S_FEMALE) = p_hv.b_behav_properties(rg+RG_NONE_F3, PERC_POP);
        if (rg > RG_LRH){
          i_hv.b_behave_change_rate(rg,S_FEMALE) = (p_hv.b_behav_properties(rg+RG_NONE_F3, DUR_AVG)!=0) ? 1 / p_hv.b_behav_properties(rg, DUR_AVG) : 0.0;
        }
      }

    }

    //auto dbg_model = capture_model(state_next, intermediate, pars);

    //nda_print_info(dbg_model.hv.b_riskgroup_proportions);
    //nda_print_info(dbg_model.hv.b_behave_change_rate);
    //nda_print_info(dbg_model.hv.b_behav_properties);


}

void set_initial_pop() {

  //dp
  const auto& c_dp = state_curr.dp;

  //goals
  auto& n_hv = state_next.hv;
  auto& i_hv = intermediate.hv;

  nda::fill(n_hv.adults, 0.0);
  nda::fill(n_hv.adults_ts, 0.0);
  nda::fill(i_hv.pop_1549, 0.0);

  for (int s = S_MALE; s <= S_FEMALE; ++s) {
    
    for(int a = SS::pIDX_15to49; a < SS::pIDX_15to49 + SS::pAG_15to49; ++a) {

      i_hv.pop_1549(s) += c_dp.p_totpop(a, s);

    }//a

    //for (int rg = RG_NONE; rg <= RG_NONE; ++rg) { //RG_TOTAL

    // n_hv.adults(VAC_UNV,rg,CD4_NEG,s)=i_hv.pop_1549(s);//i_hv.b_riskgroup_proportions(rg,s)*i_hv.pop_1549(s);

    //}//rg

    for (int rg = RG_NONE; rg <= RG_TOTAL; ++rg) { 

      n_hv.adults(VAC_UNV,rg,CD4_NEG,s)=i_hv.b_riskgroup_proportions(rg,s)*i_hv.pop_1549(s);

    }//rg

  } //s

}


  void set_initial_pulse() {

    //from dp/aim
    const auto& p_ha = pars.ha;

    //from goals
    //const auto& c_hv = state_curr.hv;
    auto& n_hv = state_next.hv;
    //auto& i_hv = intermediate.hv;
    const auto& p_hv = pars.hv;

    double pulse =0.0;
    double distr =0.0;

    for (int s = S_MALE; s <= S_FEMALE; ++s) {

      for (int rg = RG_LRH; rg <= RG_TOTAL; ++rg) {


        if (s == S_FEMALE && rg >= RG_MSM){
          continue;
        } 


       const int a25_34=10;//of set from index 0=age 15

        pulse = p_hv.epi_initial_pulse * n_hv.adults(VAC_UNV,rg,CD4_NEG,s);
        n_hv.new_infections_goals(s)+=pulse;

        if (rg==RG_MRH){
          pulse = (3.0/5.0)*pulse;
        }

        if (rg==RG_LRH){
          pulse = (1.0/5.0)*pulse;
        }

        if (rg==RG_NONE || rg==RG_IDU) {
          pulse = 0.0;
        }
        if (rg==S_FEMALE && rg==RG_MSM) {
          pulse = 0.0;
        }


        for (int hd = CD4_PRIM; hd <= CD4_LT50; ++hd) {

          int hd_hds = 0; //set prim

          if(hd==CD4_GT500){
            continue; //see goals
          }  

          if(hd>=CD4_350_500){
            hd_hds = hd - CD4_GT500; //CD4_350_500 and higher indices
          }  

          distr = p_ha.cd4_initial_distribution(hd_hds, a25_34, s);//CDP note the use of one age category for distr from AIM

          //pulse = 10000.00;//CDP remove this
          //pulse = n_hv.adults(VAC_UNV,rg,CD4_NEG,s);
          n_hv.adults(VAC_UNV,rg,hd,s)  = n_hv.adults(VAC_UNV,rg,hd,s) + pulse*distr;
          n_hv.adults(VAC_UNV,rg,CD4_NEG,s) = n_hv.adults(VAC_UNV,rg,CD4_NEG,s) - pulse*distr;
          
          if(n_hv.adults(VAC_UNV,rg,CD4_NEG,s)<0.0){
            n_hv.adults(VAC_UNV,rg,CD4_NEG,s)=0.0;
          }

        }

    }//rg

  }//s

}



void calc_new_vaccinations(int t)
{
  auto& n_hv = state_next.hv;
  auto& i_hv = intermediate.hv;
  const auto& p_hv = pars.hv;

  nda::fill(i_hv.new_vaccinations, 0.0);
  nda::fill(i_hv.vac_effect, 0.0);

  //real_type dt = 1/opts.hts_per_year;

  real_type vac_waning_rate=0;
  vac_waning_rate = (p_hv.rn_vac_params(VAC_DUR)>0.0) ? 1/p_hv.rn_vac_params(VAC_DUR) : 0.0;

  //vac effect
  i_hv.vac_effect(VAC_TAKEACTION,VAC_TAKE)       = 0.5;//p_hv.rn_vac_params(VAC_EFF)/100.0;//CDP: this /100 can be done in modvar mapping
  i_hv.vac_effect(VAC_TAKEACTION,VAC_NO_PROT)    = 1-0.5;//p_hv.rn_vac_params(VAC_EFF)/100.0;
  i_hv.vac_effect(VAC_DEGREEACTION,VAC_PARTIAL)  = 1;

   double value = 0.0;
   double vac_coverage =0.0;

   int nr=0;

   for (int s = S_MALE; s <= S_FEMALE; ++s)
    {
        for (int rg = RG_NONE; rg <= RG_TOTAL1; ++rg)
        {

          if (s == S_FEMALE && rg >= RG_MSM){ 
           continue; //no female MSM
          }

          
          int h1 = CD4_LT50_ART;                     
          if (p_hv.rn_vac_targetting == 1){
            h1 = CD4_NEG;
          }  

          for (int hd = CD4_NEG; hd <= h1; ++hd) {
          
              // Determine the risk index (nr) used for coverage lookup
              nr = rg;
              if(s==S_FEMALE){
                nr = rg + RG_NONE_F3;
              }  
  
              vac_coverage = p_hv.rn_vac_coverage_all(t);
              if (p_hv.rn_vac_cov_type != VAC_COV_ALLRISK)
              {
                vac_coverage = p_hv.rn_vac_coverage_rg(nr, t); 
              }

              vac_coverage = std::clamp(vac_coverage, 0.0, 1.0);

              value =  vac_coverage * (n_hv.adults(VAC_ALL,rg,hd,s)  +
                          //note it assume no one is vaccined below age 15
                          i_hv.dp_entrants_age_15(POP_H_HIVNeg,CD4_NEG,s) *
                          n_hv.adults(VAC_ALL,rg,hd,s)  / n_hv.adults(VAC_ALL,rg,CD4_ALL,s))-
                          (n_hv.adults(VAC_TAKE,rg,hd,s) +
                          n_hv.adults(VAC_PARTIAL,rg,hd,s) +
                          n_hv.adults(VAC_NO_PROT,rg,hd,s)) * (1 - vac_waning_rate);


              value=std::max(value,0.0);

              i_hv.new_vaccinations(rg,hd,s)+=value;
              i_hv.new_vaccinations_total+=value;

            }


      }//rg

    } //s


    std::cout << "total new vaccinations: " << i_hv.new_vaccinations_total << std::endl;


}


//inner loop functions
  void set_goals_vars_from_dp(int t) {
    //dp
    const auto& c_dp = state_curr.dp;
    const auto& n_dp = state_next.dp;
    const auto& i_dp = intermediate.dp;


    //aim
    const auto& c_ha = state_curr.ha;
    const auto& n_ha = state_next.ha;
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

    i_hv.total_art_adults=0.0;//denominator for resource needs
    i_hv.total_art_children=0.0;//denominator for resource needs
    i_hv.total_pop_hivpos=0.0;//denominator for resource need


    for (int s = S_MALE; s <= S_FEMALE; ++s)
    for(int a = SS::pIDX_15to49; a < SS::pIDX_15to49 + SS::pAG_15to49; ++a)
    {

         const int a_hv   = a - 15;//for adult structure age 15 starts at 0
         for (int hd = CD4_GT500; hd <= CD4_LT50; ++hd) {
            const int hd_hds = hd - CD4_GT500;
            i_hv.total_pop_hivpos += n_ha.h_hivpop(hd_hds, a_hv, s);
            for (int ht = 0; ht < nART; ++ht) {
              if(a>=15){
                i_hv.total_art_adults +=n_ha.h_artpop(ht, hd_hds, a_hv, s);
              }
              else{
                i_hv.total_art_children +=n_ha.h_artpop(ht, hd_hds, a_hv, s);
              }
            }
        }

     }

    for (int s = S_MALE; s <= S_FEMALE; ++s) {

      int a50 = SS::pIDX_15to49 + SS::pAG_15to49;
      i_hv.dp_aging_50(POP_H_HIVNeg, CD4_NEG, s) += n_dp.p_totpop(a50, s); 
    
      const int a50_hv   = 35;//for adult structure age 15 starts at 0
      for (int hd = CD4_GT500; hd <= CD4_LT50; ++hd) {
      
        const int hd_hds = hd - CD4_GT500;

        i_hv.dp_aging_50(POP_H_NoART, hd, s) += n_ha.h_hivpop(hd_hds, a50_hv, s);
        i_hv.dp_aging_50(POP_H_HIVNeg, CD4_NEG, s) -= n_ha.h_hivpop(hd_hds, a50_hv, s);
        
        for (int ht = 0; ht < nART; ++ht) {
          i_hv.dp_aging_50(POP_H_ARTlt6m+ht, hd, s) += n_ha.h_artpop(ht, hd_hds, a50_hv, s);
          i_hv.dp_aging_50(POP_H_HIVNeg, CD4_NEG, s) -= n_ha.h_artpop(ht, hd_hds, a50_hv, s);
        }
      }

      
      
   // std::cout << "ages 1: " << SS::pIDX_15to49 << std::endl;
   // std::cout << "ages 2: " << SS::pIDX_15to49 + SS::pAG_15to49 << std::endl;

     for(int a = SS::pIDX_15to49; a < SS::pIDX_15to49 + SS::pAG_15to49; ++a) {

      i_hv.dp_totpop_deaths_background(s) += n_dp.p_deaths_background_totpop(a, s);
      i_hv.dp_totpop_1549(s) += n_dp.p_totpop(a - 1, s);

      i_hv.dp_migration_num(s) += n_dp.p_totpop(a, s) * i_dp.migration_rate(a, s);
      i_hv.dp_migration_denom(s) += n_dp.p_totpop(a, s);

      i_hv.dp_pop_1549(s) += n_dp.p_totpop(a, s);
      i_hv.dp_aging_denom_1549(POP_H_HIVNeg, CD4_NEG, s) += n_dp.p_totpop(a, s);
      if(a==SS::pIDX_15to49){
         i_hv.dp_entrants_age_15(POP_H_HIVNeg, CD4_NEG, s) += n_dp.p_totpop(a, s);
      }

      //if(a==SS::pIDX_15to49 + SS::pAG_15to49 - 1){
      //    i_hv.dp_aging_50(POP_H_HIVNeg, CD4_NEG, s) += n_dp.p_totpop(a, s);
      //}

      for (int hd = CD4_GT500; hd <= CD4_LT50; ++hd) {
          
          const int hd_hds = hd - CD4_GT500;
          const int a_hv   = a - 15;//for adult structure age 15 starts at 0

          i_hv.dp_pop_1549_hiv(hd,s) += n_ha.h_hivpop(hd_hds, a_hv, s);
      
          double hivpop_h  = n_ha.h_hivpop(hd_hds, a_hv, s);
          double hivpop_h1 = n_ha.h_hivpop(hd_hds-1, a_hv, s);

          i_hv.dp_pop_sex_age_hiv(POP_H_NoART, s) += hivpop_h;
          i_hv.dp_aging_denom_1549(POP_H_NoART, hd, s) += hivpop_h;
          i_hv.dp_aging_denom_1549(POP_H_HIVNeg, CD4_NEG, s) -= hivpop_h;//remove hiv states

          if(a==SS::pIDX_15to49){
            i_hv.dp_entrants_age_15(POP_H_NoART, hd, s) += hivpop_h;
            i_hv.dp_entrants_age_15(POP_H_HIVNeg, CD4_NEG, s) -= hivpop_h;
          }

          
          //if(a==SS::pIDX_15to49 + SS::pAG_15to49){ //CDP note using age 50
          //  sum1+= n_ha.h_hivpop(hd_hds, a, s);
          //  i_hv.dp_aging_50(POP_H_NoART, hd, s) += n_ha.h_hivpop(hd_hds, a, s);
          //  i_hv.dp_aging_50(POP_H_HIVNeg, CD4_NEG, s) -= n_ha.h_hivpop(hd_hds, a, s);
         // }

          i_hv.dp_hiv_cd4_mort_no_art(hd,s) += n_ha.h_hiv_deaths_no_art(hd_hds, a_hv, s);
          if(hd > CD4_GT500){
            i_hv.dp_hiv_cd4_progression(hd-1, s) += p_ha.cd4_progression(hd_hds - 1, a_hv, s) * hivpop_h1;
          }

          for (int ht = 0; ht < nART; ++ht) {

            double artpop_h = n_ha.h_artpop(ht, hd_hds, a_hv, s);

            i_hv.dp_pop_1549_art(hd,s) += artpop_h;

            i_hv.dp_pop_sex_age_hiv(POP_H_ARTlt6m+ht, s) += artpop_h;
            i_hv.dp_aging_denom_1549(POP_H_ARTlt6m+ht, hd, s) += artpop_h;
            i_hv.dp_aging_denom_1549(POP_H_HIVNeg, CD4_NEG, s) -= artpop_h;//remove art states

            //CDP: using an average rate. review
            //i_hv.art_alpha(hd,s) +=  (p_ha.art_mortality(ht, hd, a, s)+p_ha.art_nonaids_excess_mort(ht, hd, a, s)) * c_ha.h_artpop(ht, hd, a, s);

            if(a==SS::pIDX_15to49){
              i_hv.dp_entrants_age_15(POP_H_ARTlt6m+ht, hd, s) += artpop_h;
              i_hv.dp_entrants_age_15(POP_H_HIVNeg, CD4_NEG, s) -= artpop_h;
            }

            //if(a==SS::pIDX_15to49 + SS::pAG_15to49-1){
            //  i_hv.dp_aging_50(POP_H_ARTlt6m+ht, hd, s) += n_ha.h_artpop(ht, hd_hds, a, s);
            //  i_hv.dp_aging_50(POP_H_HIVNeg, CD4_NEG, s) -= n_ha.h_artpop(ht, hd_hds, a, s);
           // }

             i_hv.dp_hiv_cd4_mort_art(hd_hds, s) += n_ha.h_hiv_deaths_art(ht, hd_hds, a_hv, s);

          }//t

        }//h

    }//a

  }//s


  if(t>1500)
  {
   auto dbg_model = capture_model(state_next, intermediate, pars);

  // nda_print_info(dbg_model.hv.dp_totpop_deaths_background);
   //nda_print_info(dbg_model.hv.dp_totpop_1549);
   //nda_print_info(dbg_model.hv.dp_pop_1549);
   //nda_print_info(dbg_model.hv.dp_entrants_age_15);
   
   //std::cout << "inputs from dp: " << std::endl;
   //std::cout << "dp_aging_50: " << sum1 << std::endl;

   //nda_print_info(dbg_model.ha.h_hivpop,1,1,-1,-1,0,0);
   //nda_print_info(dbg_model.hc.h_hivpop1,1,1,-1,-1,0,0);

   nda_print_info(dbg_model.ha.h_hivpop);
   nda_print_info(dbg_model.ha.cd4_progression);

  
   nda_print_info(dbg_model.ha.h_hivpop,-1,-1,25,25,0,0);
   nda_print_info(dbg_model.ha.h_hivpop,-1,-1,48,48,0,0);
   nda_print_info(dbg_model.ha.h_hivpop,-1,-1,49,49,0,0);
   nda_print_info(dbg_model.ha.h_hivpop,-1,-1,50,50,0,0);


   

   nda_print_info(dbg_model.hv.dp_aging_50,POP_H_HIVNeg,POP_H_HIVNeg,-1,-1,0,0);
   nda_print_info(dbg_model.hv.dp_aging_50,POP_H_NoART,POP_H_NoART,-1,-1,0,0);


  // nda_print_info(dbg_model.hv.dp_aging_denom_1549);
  }
}


void calc_goals_rates(int t, int hiv_step) {

  const auto& p_ha = pars.ha;

  const auto& p_hv = pars.hv;
  auto& i_hv = intermediate.hv;

  real_type denominator = 0.0;
  real_type numerator = 0.0;

  //demographical rates
  if(hiv_step==0){
    nda::fill(i_hv.background_death_rate, 0.0);//dp total pop 1549
    nda::fill(i_hv.rate_aging_50, 0.0);//mort rate, hiv on ART
  }

  nda::fill(i_hv.migration_rate, 0.0);//migration rate

  //rates for HIV dynamics
  nda::fill(i_hv.hiv_mu, 0.0);//mort rate, hiv not on ART
  nda::fill(i_hv.hiv_mu_excess, 0.0);//non aids excess mortality

  nda::fill(i_hv.hiv_lambda, 0.0);//progression rate, hiv not on ART
  nda::fill(i_hv.art_alpha, 0.0);//mort rate, hiv on ART

  //aggregate rates
  nda::fill(i_hv.hiv_exit_rates, 0.0);//total exit rate, hiv not on ART
  nda::fill(i_hv.art_exit_rates, 0.0);//total exit rate, hiv on ART
  nda::fill(i_hv.hiv_stage_progressors, 0.0);//progression rate, hiv not on ART

  real_type years_in_primary=p_hv.epi_months_in_primary/12;

  //ADH treatment impact on mort
  //double ADH_Tx_Impact = 1.0;
  //double AHD_cov = 0;
  //int GoalsBaseYearIdx=1;

  //AHD_cov = p_hv.rn_adh_treat_cov(t) * (1 + p_hv.rn_poc_cov(POC_CD4,t) * p_hv.rn_poc_effect(POC_CD4));
  //if(AHD_cov > 1.0) AHD_cov = 1.0;
  //ADH_Tx_Impact = 1 - (AHD_cov- p_hv.rn_adh_treat_cov(GoalsBaseYearIdx))* p_hv.rn_adh_treat_reduc_mort;
  //***************************


  const int hOnArt = 7;
  const int a25_34=10;//of set from index 0=age 15
  for (int s = S_MALE; s <= S_FEMALE; ++s) {

        //demographical rate  dp_pop_1549 dp_totpop_1549
        if(hiv_step==0){
          i_hv.background_death_rate(s) = (i_hv.dp_pop_1549(s)!=0) ? i_hv.dp_totpop_deaths_background(s)/i_hv.dp_pop_1549(s) : 0.0;
        }

        //migration rate
        if(hiv_step==0){
          i_hv.migration_rate(s) = (i_hv.dp_migration_denom(s) !=0) ? i_hv.dp_migration_num(s)/i_hv.dp_migration_denom(s) : 0.0;
        }

        //set aging rates, out of 15-49 year old population
        i_hv.rate_aging_50(POP_H_HIVNeg, CD4_NEG, s) = (i_hv.dp_aging_denom_1549(POP_H_HIVNeg, CD4_NEG, s) !=0) ? i_hv.dp_aging_50(POP_H_HIVNeg, CD4_NEG, s)/i_hv.dp_aging_denom_1549(POP_H_HIVNeg, CD4_NEG, s) : 0.0;

        //cd4 transition rate for primary stage
        i_hv.hiv_lambda(CD4_PRIM,s) = (years_in_primary!=0) ? 1/years_in_primary : 0.0;

        for (int hd = CD4_GT500; hd <= CD4_LT50; ++hd) {

          const int hd_hds = hd - CD4_GT500;

          //hiv dynamics: mortality and progression rates
          //i_hv.hiv_mu(hd,s) = (i_hv.dp_pop_1549_hiv(hd,s)!=0) ? i_hv.dp_hiv_cd4_mort_no_art(hd,s)/i_hv.dp_pop_1549_hiv(hd,s) : p_ha.cd4_mortality(hd_hds, 25, s);//using age 25 for defaults
          //i_hv.hiv_lambda(hd,s) = (i_hv.dp_pop_1549_hiv(hd,s)!=0) ? i_hv.dp_hiv_cd4_progression(hd,s)/i_hv.dp_pop_1549_hiv(hd,s) : p_ha.cd4_progression(hd_hds, 25, s);//
          //i_hv.art_alpha(hd,s) = (i_hv.dp_pop_1549_art(hd,s)!=0) ? i_hv.dp_hiv_cd4_mort_art(hd,s)/i_hv.dp_pop_1549_art(hd,s) : p_ha.art_mortality(2, hd_hds, 25, s);//2 is gt12 m on ART

          //direct from age categories, no averaging
          i_hv.hiv_mu(hd,s)        = i_hv.ADH_Tx_Impact * p_ha.cd4_mortality(hd_hds, a25_34, s); //using age 25 for defaults
          i_hv.hiv_mu_excess(hd,s) = p_ha.cd4_nonaids_excess_mort(hd_hds, a25_34, s);
          i_hv.hiv_mu(hd,s)        = i_hv.hiv_mu(hd,s) + i_hv.hiv_mu_excess(hd,s); 
          i_hv.hiv_mu(hd,s)        = std::max(i_hv.hiv_mu(hd,s), i_hv.background_death_rate(s));

          
          //auto dbg_model = capture_model(state_next, intermediate, pars);
          //nda_print_info(dbg_model.ha.cd4_mortality,2,2,-1,-1,-1,35,0,0);
          //nda_print_info(dbg_model.ha.cd4_mortality,2,2,6,6,-1,-1,0,0);

          i_hv.hiv_lambda(hd,s) = p_ha.cd4_progression(hd_hds, a25_34, s);//


          i_hv.art_alpha(hd+hOnArt,s)  = i_hv.alpha_mult * p_ha.art_mortality_time_rate_ratio(ART_GT12m, t) * 
                                                           p_ha.art_mortality(ART_GT12m, hd_hds, a25_34, s);
          i_hv.art_alpha_excess(+hOnArt,s)  = p_ha.art_nonaids_excess_mort(ART_GT12m, hd_hds, a25_34, s);
          i_hv.art_alpha(hd+hOnArt,s)  =  i_hv.art_alpha(hd+hOnArt,s) + i_hv.art_alpha_excess(hd+hOnArt,s); 
   

          if(hd==CD4_GT500){
            real_type stage_duration = 1.0 / i_hv.hiv_lambda(CD4_GT500,s)  - years_in_primary;
            i_hv.hiv_lambda(CD4_GT500,s) = (1-exp(-opts.dt/stage_duration))/opts.dt;//remove time in primary stage
            i_hv.hiv_mu(CD4_PRIM,s) = i_hv.hiv_mu(CD4_GT500,s);
            //double val1=i_hv.hiv_lambda(CD4_GT500,s);
          }

          if(hd==CD4_LT50){
            i_hv.hiv_lambda(hd,s) = 0.0;//no progession out of this stage
          }

          i_hv.rate_aging_50(POP_H_NoART, hd, s) = (i_hv.dp_aging_denom_1549(POP_H_NoART, hd, s) !=0) ? i_hv.dp_aging_50(POP_H_NoART, hd, s)/i_hv.dp_aging_denom_1549(POP_H_NoART, hd, s) : 0.0;
          if(hd==CD4_GT500){
            i_hv.rate_aging_50(POP_H_NoART, CD4_PRIM, s) =i_hv.rate_aging_50(POP_H_NoART, hd, s); 
          }  

          denominator = 0.0;
          numerator = 0.0;
          for (int ht = 0; ht < nART; ++ht) {
            numerator +=   i_hv.dp_aging_50(POP_H_ARTlt6m+ht, hd, s);
            denominator += i_hv.dp_aging_denom_1549(POP_H_ARTlt6m+ht, hd, s);
          }
          i_hv.rate_aging_50(POP_H_OnART, hd, s) = (denominator !=0) ? numerator/denominator : 0.0;

      }


      //aggregate exit rates  CDP review if still needed
      for (int hd = CD4_GT500; hd < CD4_LT50; ++hd) {

        for (int rg = RG_NONE; rg <= RG_TOTAL; ++rg) {
            i_hv.hiv_exit_rates(rg,hd,s) = i_hv.background_death_rate(s)+
                                        i_hv.hiv_mu(hd,s)+
                                        (p_hv.b_behav_properties(rg,DUR_AVG) > 0.0) ? (1 /p_hv.b_behav_properties(rg,DUR_AVG)) : 0.0 +
                                        i_hv.rate_aging_50(POP_H_NoART, hd, s);

            i_hv.art_exit_rates(rg,hd,s) = i_hv.background_death_rate(s)+
                                        i_hv.art_alpha(hd,s)+
                                        (p_hv.b_behav_properties(rg,DUR_AVG)>0.0) ? (1 /p_hv.b_behav_properties(rg,DUR_AVG)) : 0.0 +
                                        i_hv.rate_aging_50(POP_H_OnART, hd, s);
        }

        }


      }

      //CDP check the elements of hiv_mu

// auto dbg_model = capture_model(state_next, intermediate, pars);

//nda_print_info(dbg_model.ha.cd4_mortality,-1,-1,25,25,-1,-1);
//nda_print_info(dbg_model.hv.hiv_mu);

//nda_print_info(dbg_model.ha.cd4_progression,-1,-1,25,25,-1,-1);
//nda_print_info(dbg_model.hv.hiv_lambda);

}

 void calc_HIV_mort_adjustments(int t)
{ //Reduce mortality following treatment for advanced HIV disease

  const auto& p_ha = pars.ha;

  auto& i_hv = intermediate.hv;
  const auto& p_hv = pars.hv;
  
  
  double AHD_cov = 0.0;
  int GoalsBaseYearIdx=p_hv.goals_base_year_idx;

  i_hv.ADH_Tx_Impact = 1.0;
  if(t>GoalsBaseYearIdx){
    AHD_cov = p_hv.rn_adh_treat_cov(t) * (1 + p_hv.rn_poc_cov(POC_CD4,t) * p_hv.rn_poc_effect(POC_CD4));
    AHD_cov = std::clamp(AHD_cov, 0.0, 1.0);

    i_hv.ADH_Tx_Impact = 1 - (AHD_cov- p_hv.rn_adh_treat_cov(GoalsBaseYearIdx))* p_hv.rn_adh_treat_reduc_mort;
    i_hv.ADH_Tx_Impact = std::clamp(i_hv.ADH_Tx_Impact, 0.0, 1.0);
  }

  //Reduce mortality by ART by 50% as viral suppression increases to 95%
  //Input is percent not virally suppressed, initial default is 0.25
  //Fast-Track target is 0.05
  i_hv.alpha_mult    = 1 - std::min(0.5,0.5
                      * (p_hv.epi_inf_mult_art(1) -
                         p_hv.epi_inf_mult_art(t) * (1 - p_hv.rn_poc_cov(POC_VL,t) * p_hv.rn_poc_effect(POC_VL)))
                      / (p_hv.epi_inf_mult_art(1) - 0.05));

  i_hv.alpha_mult = std::clamp(i_hv.alpha_mult, 0.0, 1.0);               
}

void calc_HIV_cure(int t)
{

  auto& n_hv = state_next.hv;
  auto& i_hv = intermediate.hv;
  const auto& p_hv = pars.hv;
  double curePercent=0.0;
  double cured=0.0;

  nda::fill(n_hv.pop_hiv_neg, 0.0);
  nda::fill(n_hv.cured_pop, 0.0);
  nda::fill(n_hv.cured_prop, 0.0);

  double cureDuration = p_hv.rn_cure_effect(VAC_DUR);
  double immuneWane   = (cureDuration > 0.0) ? (1.0 / cureDuration) : (1.0 / 9.0);

  int nr=0;

  for (int rg = RG_NONE; rg <= RG_MSMIDU; ++rg)
  for (int s = S_MALE; s <= S_FEMALE; ++s)
  {

    
    for (int v = VAC_UNV; v <= VAC_NO_PROT; ++v)
    {
      if (!((s == S_FEMALE) && (rg >= RG_MSM) && (rg <= RG_MSMIDU))){// Exclude female MSM and higher risk groups
        n_hv.pop_hiv_neg(rg,s) += n_hv.adults(v,rg,CD4_NEG,s);
      } 
    } //v


    // Determine the risk index (nr) used for coverage lookup
    nr = rg;
    if(s==S_FEMALE){
      nr = rg + RG_NONE_F3;
    }  

    curePercent = p_hv.rn_cure_coverage_all(t) * p_hv.rn_cure_effect(VAC_EFF);
    if (p_hv.rn_cure_coverage_type != CURE_COV_ALLRISK)
    {
      curePercent = p_hv.rn_cure_coverage_rg(nr, t) * p_hv.rn_cure_effect(VAC_EFF);
    }

    curePercent = std::clamp(curePercent, 0.0, 1.0);

    if(curePercent>0.0)
    {

        for (int hd = CD4_GT500 ; hd <= CD4_LT50_ART; ++hd)
        for (int v = VAC_UNV; v <= VAC_NO_PROT; ++v)
        {
          cured =  n_hv.adults(v,rg,hd,s) * curePercent; //opts.dt *

          // do not remove more than 99 % of the current compartment >> CDP check
          cured = std::min(cured, 0.99 * n_hv.adults(v, rg, hd, s));

          n_hv.cured_pop(rg, s) += cured;

        //move cured individuals to the HIV‑negative compartment
        if(n_hv.adults(v,rg,hd,s)-cured>0){
            n_hv.adults(v,rg,hd,s)-=cured;
            n_hv.adults(v,rg,CD4_NEG,s)+=cured;
        }

        }//hd,v
 
    }//if

    //Update cured‑population accounting for natural death and waning immunity
    n_hv.cured_pop(rg, s) -= (i_hv.background_death_rate(s)+immuneWane)*n_hv.cured_pop(rg, s); //opts.dt * 
    if(n_hv.cured_pop(rg, s)<0){
      n_hv.cured_pop(rg, s)=0;
    } 


    ///  Record the proportion of cured individuals among the HIV‑negative
    //  population (used later in force‑of‑infection calculations)
    if (n_hv.pop_hiv_neg(rg,s) > 0.0){
      n_hv.cured_pop(rg, s) = n_hv.cured_pop(rg, s) / n_hv.pop_hiv_neg(rg,s);
    }

  }//rg,s

}


void calc_newrecruits_distribution(int t)
{
  auto& n_hv = state_next.hv;
  auto& i_hv = intermediate.hv;
  const auto& p_hv = pars.hv;

  real_type value=0.0;
  real_type rg_sum=0.0;

  //auto dbg_model = capture_model(state_next, intermediate, pars);
  //nda_print_info(dbg_model.hv.b_riskgroup_proportions,-1,-1,0,0);

   for (int s = S_MALE; s <= S_FEMALE; ++s)
   {

    rg_sum = 0.0;
    for (int rg = RG_LRH; rg <= RG_TOTAL1; ++rg)
    {
        if (s == S_FEMALE && rg >= RG_MSM){
          continue;
        } 

        if(i_hv.b_riskgroup_proportions(rg,s)-
            n_hv.adults(VAC_ALL,rg,CD4_ALL,s)/n_hv.adults(VAC_ALL,RG_ALL,CD4_ALL,s) != 0)
        {
            if(n_hv.adults(VAC_ALL,RG_ALL,CD4_ALL,s) == 0.0 ||
                i_hv.b_behave_change_rate(rg,s)== 0.0) // ||
                //n_hv.adults(VAC_ALL,rg,CD4_ALL,s) == 0.0)
            {
                value = 0.0;
            }
            else
            {
                value = i_hv.b_riskgroup_proportions(rg,s) +
                       ( (i_hv.b_riskgroup_proportions(rg,s) -
                         (1-i_hv.b_behave_change_rate(rg,s))*
                          n_hv.adults(VAC_ALL,rg,CD4_ALL,s)/
                          n_hv.adults(VAC_ALL,RG_ALL,CD4_ALL,s))*
                          p_hv.b_incr_recruit(s,rg) );
                 
                value=std::max(value,0.0);
                i_hv.b_riskgroup_proportions(rg,s)=value;         

            }

            rg_sum += i_hv.b_riskgroup_proportions(rg,s);

        }

    }//rg

    //normalize
    for (int rg = RG_LRH; rg <= RG_TOTAL1; ++rg)
    {
        if (s == S_FEMALE && rg >= RG_MSM) continue;
       
         if(rg_sum>0.0){
          i_hv.b_riskgroup_proportions(rg,s)/=rg_sum;
         }
    }

   }//s

   //nda_print_info(dbg_model.hv.b_riskgroup_proportions,-1,-1,0,0);


}



void progress_norisk_hiv_neg(int t, int hiv_step)
{

    //const auto& c_hv = state_curr.hv;
    auto& n_hv = state_next.hv;
    auto& i_hv = intermediate.hv;
    const auto& p_hv = pars.hv;

    //real_type dt = opts.dt; //1/opts.hts_per_year;
    real_type value = 0.0;

    //nda::fill(i_hv.new_vaccinations, 0.0);
    //nda::fill(i_hv.vac_params, 0.0);

    
    //unvaccinated
    for (int s = S_MALE; s <= S_FEMALE; ++s)
    {
        value =
        n_hv.adults(VAC_UNV,RG_NONE,CD4_NEG,s)+opts.dt*(
        
          //new entrants 15 yrs , note that they are not vaccinated by assumption
        i_hv.dp_entrants_age_15(POP_H_HIVNeg,CD4_NEG,s) -
        
        //exits and migration
        n_hv.adults_ts(VAC_UNV,RG_NONE,CD4_NEG,s) * (
        ((std::max(i_hv.i_age_first_sex(s) - 15.0, 1.0)!=0) ? 1/std::max(i_hv.i_age_first_sex(s) - 15.0, 1.0) : 0.0) +
        i_hv.background_death_rate(s) +
        i_hv.rate_aging_50(POP_H_HIVNeg,CD4_NEG,s) -
        i_hv.migration_rate(s) ) - // net migration rate

        //new vaccinations, out
        i_hv.new_vaccinations(RG_NONE,CD4_NEG,s) +

        //vaccine waning, entrants
         (n_hv.adults_ts(VAC_TAKE,RG_NONE,CD4_NEG,s) +
         n_hv.adults_ts(VAC_PARTIAL,RG_NONE,CD4_NEG,s) +
         n_hv.adults_ts(VAC_NO_PROT,RG_NONE,CD4_NEG,s)) *
        ( (i_hv.vac_params(VAC_DUR)!=0)? 1 / i_hv.vac_params(VAC_DUR) : 0.0) ); 
      

        value=std::max(value,0.0);

        n_hv.adults(VAC_UNV,RG_NONE,CD4_NEG,s) = value;

        //keep track of deaths
        n_hv.deaths(VAC_UNV,RG_NONE,CD4_NEG,s) += opts.dt*n_hv.adults_ts(VAC_UNV,RG_NONE,CD4_NEG,s)*
                                                          i_hv.background_death_rate(s);


        n_hv.total_deaths += opts.dt*n_hv.adults_ts(VAC_UNV,RG_NONE,CD4_NEG,s)*
                                     i_hv.background_death_rate(s);   
                                                                                                           

        //continue;
        //vaccinated
        for (int v = VAC_TAKE; v <= VAC_NO_PROT; ++v) 
        {
              value =
              n_hv.adults(v,RG_NONE,CD4_NEG,s) + opts.dt*( -
              //exits and migration
              n_hv.adults_ts(v,RG_NONE,CD4_NEG,s) * (
              i_hv.background_death_rate(s) +
              i_hv.rate_aging_50(POP_H_HIVNeg,CD4_NEG,s) - // aging out at age 50
              i_hv.migration_rate(s) ) + //net migration

              //new vaccinations, in
              i_hv.new_vaccinations(RG_NONE,CD4_NEG, s)  * i_hv.vac_effect(p_hv.rn_vac_targetting,v) - //*
              //temp1 * ((temp2!=0)? 1 / temp2 : 0) -

              //vaccine, exits
              n_hv.adults_ts(v,RG_NONE,CD4_NEG,s)*
              ((i_hv.vac_params(VAC_DUR)!=0)? 1 / i_hv.vac_params(VAC_DUR) : 0.0)  );

              value=std::max(value,0.0);

              n_hv.adults(v,RG_NONE,CD4_NEG,s)=value;

              //keep track of deaths
              n_hv.deaths(v,RG_NONE,CD4_NEG,s) += opts.dt*n_hv.adults_ts(v,RG_NONE,CD4_NEG,s)*
                                                          i_hv.background_death_rate(s);
             
              n_hv.total_deaths += opts.dt*n_hv.adults_ts(v,RG_NONE,CD4_NEG,s)*
                                           i_hv.background_death_rate(s);                                             

        }//v

    }//s

}

void progress_atrisk_hiv_neg(int t)
{

    //const auto& c_hv = state_curr.hv;
    auto& n_hv = state_next.hv;
    auto& i_hv = intermediate.hv;
    const auto& p_hv = pars.hv;

    //real_type dt = 1/opts.hts_per_year;
    real_type value = 0.0;
    //nda::fill(i_hv.new_vaccinations, 0.0);
    //nda::fill(i_hv.vac_params, 0.0);

    double temp1=0;
    double temp2=0;

    //unvaccinated
    for (int s = S_MALE; s <= S_FEMALE; ++s)
    {

        for (int rg = RG_LRH; rg <= RG_TOTAL1; ++rg)
        {

          if (s == S_FEMALE && rg >= RG_MSM){
            continue;
          }

          temp1=n_hv.adults_ts(VAC_UNV,rg,CD4_NEG,s);
          temp2=n_hv.adults_ts(VAC_UNV,rg,CD4_ALL,s);

          value =
          n_hv.adults(VAC_UNV,rg,CD4_NEG,s) + opts.dt*(

          //no risk at sexual debut
          n_hv.adults_ts(VAC_UNV,RG_NONE,CD4_NEG,s) *
          ((std::max(i_hv.i_age_first_sex(s) - 15.0, 1.0)!=0)? 1/std::max(i_hv.i_age_first_sex(s) - 15.0, 1.0) : 0) *
            i_hv.b_riskgroup_proportions(rg,s) -

          //exits and migration
          n_hv.adults_ts(VAC_UNV,rg,CD4_NEG,s) * (
          i_hv.background_death_rate(s) +
          i_hv.rate_aging_50(POP_H_HIVNeg,CD4_NEG,s) +// aging out at age 50
          ((RG_MRH<=rg && rg<<RG_IDU) ? i_hv.b_behave_change_rate(rg,s) : 0.0) - //behavior chnage
          i_hv.migration_rate(s) ) - //net migration

          //new vaccinations
          i_hv.new_vaccinations(rg,CD4_NEG,s) +

          //vaccine waning, entrants
          (n_hv.adults_ts(VAC_TAKE,rg,CD4_NEG,s) +
            n_hv.adults_ts(VAC_PARTIAL,rg,CD4_NEG,s) +
            n_hv.adults_ts(VAC_NO_PROT,rg,CD4_NEG,s)) *
          ((i_hv.vac_params(VAC_DUR)!=0)? 1 / i_hv.vac_params(VAC_DUR) : 0.0) +

          //entrants following behavior change
          ((RG_LRH<=rg && rg<<RG_MRH) ? n_hv.adults_ts(VAC_UNV,rg+1,CD4_NEG,s) * i_hv.b_behave_change_rate(rg+1,s) : 0.0));

          value=std::max(value,0.0);

          n_hv.adults(VAC_UNV,rg,CD4_NEG,s) = value;

          //keep track of deaths
          n_hv.deaths(VAC_UNV,rg,CD4_NEG,s) += opts.dt*n_hv.adults_ts(VAC_UNV,rg,CD4_NEG,s)*
                                                       i_hv.background_death_rate(s);

          n_hv.total_deaths += opts.dt*n_hv.adults_ts(VAC_UNV,rg,CD4_NEG,s)*
                                       i_hv.background_death_rate(s);                                                        

          
          //continue;
          //vaccinated
          for (int v = VAC_TAKE; v <= VAC_NO_PROT; ++v)
          {
                value =
                n_hv.adults(v,rg,CD4_NEG,s) + opts.dt*( -
                //exits and migration
                n_hv.adults_ts(v,rg,CD4_NEG,s) * (
                i_hv.background_death_rate(s) +
                i_hv.rate_aging_50(POP_H_HIVNeg,CD4_NEG,s) -// aging out at age 50
                i_hv.b_behave_change_rate(rg,s) -
                i_hv.migration_rate(s) ) + //net migration

                //new vaccinations
                i_hv.new_vaccinations(rg,CD4_NEG,s)  * i_hv.vac_effect(p_hv.rn_vac_targetting,v) - 
                //temp1 * ((temp2!=0)? 1 / temp2 .0) -

                //vaccine, exits
                n_hv.adults_ts(v,rg,CD4_NEG,s)*
                ((i_hv.vac_params(VAC_DUR)!=0)? 1 / i_hv.vac_params(VAC_DUR) : 0.0)  +

                //entrants following behavior change
                ((rg <= RG_HRH) ? n_hv.adults_ts(v,rg+1,CD4_NEG,s) * i_hv.b_behave_change_rate(rg+1,s) : 0.0) );

                value=std::max(value,0.0);

                n_hv.adults(v,rg,CD4_NEG,s)=value;

                //keep track of deaths
                n_hv.deaths(v,rg,CD4_NEG,s) += opts.dt*n_hv.adults_ts(v,rg,CD4_NEG,s)*
                                                       i_hv.background_death_rate(s);

                n_hv.total_deaths           += opts.dt*n_hv.adults_ts(v,rg,CD4_NEG,s)*
                                                       i_hv.background_death_rate(s);                                       


          }//v

      }//rg

    }//s
}

void progress_hivp_and_art(int t)
{
    //from goals
    auto& n_hv = state_next.hv;
    auto& i_hv = intermediate.hv;
    const auto& p_hv = pars.hv;

    real_type dt = opts.dt;
    real_type value = 0.0;

    //nda::fill(i_hv.new_vaccinations, 0.0);
    //nda::fill(i_hv.vac_params, 0.0);

    double temp1=0;
    double temp2=0;

    //unvaccinated
    for (int s = S_MALE; s <= S_FEMALE; ++s)
    {

        for (int rg = RG_NONE; rg <= RG_TOTAL1; ++rg)
        {


        if (s == S_FEMALE && rg >= RG_MSM){ 
            continue;
        }

        int hd_lb = CD4_LT50;
        if(t >= opts.ts_art_start){
          hd_lb = CD4_LT50_ART;
        }

        const int hOnArt = 7;
        for (int hd = CD4_PRIM; hd <= hd_lb; ++hd) 
        {

          //if (hd >= CD4_GT500_ART &&  t < opts.ts_art_start ) continue;

          temp1=n_hv.adults(VAC_UNV,rg,hd,s);
          temp2=n_hv.adults(VAC_UNV,rg,CD4_ALL,s);

          //Mortality
          //hiv-pos or hiv-art mortality rate
          real_type mort_hiv = 0.0;
          if (CD4_PRIM <= hd && hd <= CD4_LT50) {
            mort_hiv = i_hv.hiv_mu(hd,s);
          }
          else {
            mort_hiv =  i_hv.art_alpha(hd,s);
          };

          //Entrants 15 years from and DP and Aging out rate
          real_type dp_entrants_age_15 = 0.0;
          real_type rate_aging_out = 0.0;

          //auto dbg_model = capture_model(state_next, intermediate, pars);
          //nda_print_info(dbg_model.hv.rate_aging_50,1,1,-1,-1,0,0);
          //nda_print_info(dbg_model.hv.rate_aging_50,POP_H_OnART,POP_H_OnART,-1,-1,0,0);


          if(CD4_PRIM <= hd && hd <= CD4_LT50) {
            rate_aging_out = i_hv.rate_aging_50(POP_H_NoART,hd,s);
            if(rg==RG_NONE){
              dp_entrants_age_15 = i_hv.dp_entrants_age_15(POP_H_NoART,hd,s);
            }
          }
          else {
            rate_aging_out = i_hv.rate_aging_50(POP_H_OnART,hd-hOnArt,s);
            if(rg==RG_NONE){
              dp_entrants_age_15 = i_hv.dp_entrants_age_15(POP_H_OnART,hd-hOnArt,s);
            } 
          };

          //Progression rate
          //hiv-pos cd 4 progression rate, not progression on art
          real_type progress_out = 0.0;
          if(CD4_PRIM <= hd && hd <= CD4_LT50) {
            progress_out = i_hv.hiv_lambda(hd,s);
          };

          real_type progress_in = 0.0;
          if(CD4_GT500 <= hd && hd <= CD4_LT50) {
            progress_in = i_hv.hiv_lambda(hd-1,s);
          };

  
          value =
          n_hv.adults(VAC_UNV,rg,hd,s) + opts.dt*(

          //new entrants 15 yrs , note that they are not vaccinated by assumption
          dp_entrants_age_15 +

          //no risk at sexual debut
          n_hv.adults_ts(VAC_UNV,RG_NONE,hd,s) *
          ((std::max(i_hv.i_age_first_sex(s) - 15.0, 1.0)!=0)? 1/std::max(i_hv.i_age_first_sex(s) - 15.0, 1.0) : 0.0 ) *
          i_hv.b_riskgroup_proportions(rg,s) -

          //exits and migration
          n_hv.adults_ts(VAC_UNV,rg,hd,s)*
          (i_hv.background_death_rate(s) +
            mort_hiv + //hiv mortality rate
            progress_out + //hiv progrssion rate
            rate_aging_out + // aging out at age 50
            ((RG_MRH<=rg && rg<<RG_IDU) ? i_hv.b_behave_change_rate(rg,s) : 0.0) - //behavior chnage
            i_hv.migration_rate(s)) -//net migration

          //new vaccinations
          i_hv.new_vaccinations(rg,hd,s) +

          //vaccine waning, entrants
           (n_hv.adults(VAC_TAKE,rg,hd,s) +
            n_hv.adults(VAC_PARTIAL,rg,hd,s) +
            n_hv.adults(VAC_NO_PROT,rg,hd,s)) *
           ((i_hv.vac_params(VAC_DUR)!=0)? 1 / i_hv.vac_params(VAC_DUR) : 0.0) +

          //entrants following behavior change
          ((RG_LRH<=rg && rg<<RG_MRH) ? n_hv.adults_ts(VAC_UNV,rg+1,hd,s) * i_hv.b_behave_change_rate(rg+1,s) : 0.0) +

          //entrants following hiv stage progression
          n_hv.adults_ts(VAC_UNV,rg,hd-1,s) * progress_in ); 

          value=std::max(value,0.0);

          n_hv.adults(VAC_UNV,rg,hd,s) = value;

          //keep track of deaths
          n_hv.deaths(VAC_UNV,rg,hd,s) += opts.dt*n_hv.adults_ts(VAC_UNV,rg,hd,s)*
                                                  (i_hv.background_death_rate(s)+mort_hiv);

          n_hv.total_deaths +=  opts.dt*n_hv.adults_ts(VAC_UNV,rg,hd,s)*
                                        (i_hv.background_death_rate(s)+mort_hiv);

          n_hv.total_deaths_hiv +=  opts.dt*n_hv.adults_ts(VAC_UNV,rg,hd,s)*(mort_hiv);                                   

          //continue;
          //vaccinated 
          for (int v = VAC_TAKE; v <= VAC_NO_PROT; ++v)
          {
                value =
                n_hv.adults_ts(v,rg,hd,s) + opts.dt*( -
                //exits and migration
                n_hv.adults_ts(v,rg,hd,s) * (
                i_hv.background_death_rate(s) +
                mort_hiv + //hiv mortality rate
                progress_out + //hiv progrssion rate
                rate_aging_out - // aging out at age 50
                i_hv.migration_rate(s) ) +//net migration

                //new vaccinations
                i_hv.new_vaccinations(rg,hd,s) * i_hv.vac_effect(p_hv.rn_vac_targetting,v) -
                //temp1 * ((temp2!=0)? 1 / temp2 .0) - //(temp1/temp2 = ratio of vac in the cd4 category)

                //vaccine, exits
                n_hv.adults_ts(v,rg,hd,s)*
                ((i_hv.vac_params(VAC_DUR)!=0)? 1 / i_hv.vac_params(VAC_DUR) : 0.0)  +

                //entrants following behavior change
                ((rg <= RG_HRH) ? n_hv.adults_ts(v,rg+1,hd,s) * i_hv.b_behave_change_rate(rg+1,s) : 0.0) +

                //entrants following hiv stage progression
                n_hv.adults_ts(v,rg,hd,s) * progress_in);

                value=std::max(value,0.0);

                n_hv.adults(v,rg,hd,s)=value;

                //keep track of deaths
                n_hv.deaths(v,rg,hd,s) += opts.dt*n_hv.adults_ts(v,rg,hd,s)*
                                                 (i_hv.background_death_rate(s)+mort_hiv);

                n_hv.total_deaths +=  opts.dt*n_hv.adults_ts(v,rg,hd,s)*
                                             (i_hv.background_death_rate(s)+mort_hiv);

                n_hv.total_deaths_hiv +=  opts.dt*n_hv.adults_ts(v,rg,hd,s)*(mort_hiv);                             
                                            
                                            

          }//v

        } //hd

      }//rg

    }//s
}


void calc_r_multiplier(int t)
{

  //from goals
  auto& n_hv = state_next.hv;
  auto& i_hv = intermediate.hv;
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



  nda::fill(i_hv.r_mult, 1.0); //default multiplier
 

  //auto dbg_model = capture_model(state_next, intermediate, pars);
  //nda_print_info(dbg_model.hv.r_mult,-1,-1,0,0);
  //nda_print_info(dbg_model.hv.r_mult,-1,-1,1,1);
  //nda_print_info(dbg_model.hv.mult_no_art);

  //nda_print_info(dbg_model.hv.mult_art);



  for (int s = S_MALE; s <= S_FEMALE; ++s)
  {
      for (int rg = RG_LRH; rg <= RG_HRH; ++rg)
      {
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
          for (int hd = CD4_GT500_ART; hd <= CD4_LT50_ART; ++hd)
          {
              rMultNumerator   += n_hv.mult_art(hd) * n_hv.adults(VAC_ALL,rg,hd,s);
              rMultDenominator += n_hv.adults(VAC_ALL,rg,hd,s);

              rMultNumeratorAll   += n_hv.mult_art(hd) * n_hv.adults(VAC_ALL,rg,hd,s);
              rMultDenominatorAll += n_hv.adults(VAC_ALL,rg,hd,s);
          }

          if (rMultDenominator > 0.0)
          {
            i_hv.r_mult(rg, s) = vaccine_factor * (rMultNumerator / rMultDenominator) / rMultEqlb;
          }

      }//r

   }//s

   //both sexes
   if (rMultDenominatorAll > 0.0)
    {
      i_hv.r_mult(RG_ALL, S_ALL) = vaccine_factor * (rMultNumeratorAll / rMultDenominatorAll) / rMultEqlb;
    }

    
    //nda_print_info(dbg_model.hv.r_mult,-1,-1,0,0);
    //nda_print_info(dbg_model.hv.r_mult,-1,-1,1,1);

    //MSM
    double vaccine_factor_m = 1.0 -  p_hv.rn_vac_params(VAC_EFF) *
                                    (n_hv.adults(VAC_ALL,RG_ALL,CD4_ALL,S_MALE)-n_hv.adults(VAC_UNV,RG_ALL,CD4_ALL,S_MALE))
                                    /n_hv.adults(VAC_ALL,RG_ALL,CD4_ALL,S_MALE);

    
    
   rMultNumeratorAll   = 0.0;
   rMultDenominatorAll = 0.0;
   for (int rg = RG_MSM; rg <= RG_MSMIDU; ++rg)
    {

        

        // not on ART
        for (int hd = CD4_PRIM ; hd <=CD4_LT50 ; ++hd)
        {
            rMultNumeratorAll   += n_hv.mult_no_art(hd) * n_hv.adults(VAC_ALL,rg,hd,S_MALE);
            rMultDenominatorAll += n_hv.adults(VAC_ALL,rg,hd,S_MALE);

        }

        //on ART
        for (int hd = CD4_GT500_ART; hd <= CD4_LT50_ART; ++hd)
        {
            rMultNumeratorAll   += n_hv.mult_art(hd) * n_hv.adults(VAC_ALL,rg,hd,S_MALE);
            rMultDenominatorAll += n_hv.adults(VAC_ALL,rg,hd,S_MALE);

        }

    }//r

    for (int rg = RG_MSM; rg <= RG_MSMIDU; ++rg)
    {
      if (rMultDenominatorAll > 0.0){
        i_hv.r_mult(rg, S_MALE) = vaccine_factor_m * (rMultNumeratorAll / rMultDenominatorAll) / rMultEqlb;
      }
    }


    //nda_print_info(dbg_model.hv.r_mult,-1,-1,0,0);
    //nda_print_info(dbg_model.hv.r_mult,-1,-1,1,1);

}

void calc_prevalence(int t, int hiv_step)
{

   double denom_s_both = 0.0;
   double plhiv_s_both = 0.0;

   double denom=0.0;
   double plhiv=0.0;

   auto& n_hv = state_next.hv;
   for (int rg = RG_NONE; rg <= RG_ALL; ++rg) 
   {
        
        denom_s_both = 0.0;
        plhiv_s_both = 0.0;

        for (int s = S_MALE; s <= S_FEMALE; ++s)
        {

           denom=0.0;
           plhiv=0.0;
           for (int v = VAC_UNV; v <= VAC_NO_PROT; ++v)
           {  
            for (int hd = CD4_NEG; hd <= CD4_LT50_ART; ++hd)
            {

                  if(!((s == S_FEMALE) && (rg >= RG_MSM) && (rg <= RG_MSMIDU))){
                    denom += n_hv.adults(v,rg,hd,s);
                    if(hd>=CD4_PRIM){
                      plhiv += n_hv.adults(v,rg,hd,s);
                    }  
                }

            }//hd

            }//v

            if(denom>0.0){
              n_hv.prevalence(rg,s) = plhiv/denom;
            }  

            denom_s_both+=denom;
            plhiv_s_both+=plhiv;

        } //s

        if(denom_s_both > 0.0){
              n_hv.prevalence(rg,S_ALL) = plhiv_s_both/denom_s_both;
        }  
    }//rg

}

void calc_new_infections(int t, int hiv_step)
{

//auto dbg_model = capture_model(state_next, intermediate, pars);
//nda_print_info(dbg_model.hv.rn_coverage);
//nda_print_info(dbg_model.hv.b_married_prop);
//nda_print_info(dbg_model.hv.b_num_partners);
//nda_print_info(dbg_model.hv.b_sex_acts);
//nda_print_info(dbg_model.hv.prevalence);

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

double rMultM =1.0;
double rMultF =1.0;

double foi = 0.0;

// Sex‑acts ratio, toggled by balanceSexActs
double SexActsRatioM   = 1.0;
double SexActsRatioF   = 1.0;

//for idu
double PrevM_IDU =0.0;
double PrevF_IDU =0.0;

double rMultM_IDU =1.0;
double rMultF_IDU =1.0;

double SexActsRatioM_IDU =1.0;
double SexActsRatioF_IDU =1.0;

double circum=p_hv.rn_coverage(INTVN_MC15_49,t);

auto dbg_model = capture_model(state_next, intermediate, pars);


double total_inf_m=0.0;
double total_inf_f=0.0;

double new_inf=0.0;

for (int rg = RG_LRH; rg <= RG_HRH; ++rg)
{

    if (rg == RG_LRH)
    {

      //double temp1 = n_hv.adults(VAC_ALL,RG_LRH,CD4_ALL,S_FEMALE);
      //double temp2 =n_hv.prevalence(RG_LRH,S_FEMALE);

      totalSexActsF = n_hv.adults(VAC_ALL,RG_LRH,CD4_ALL,S_FEMALE) * i_hv.i_num_partners(RG_LRH) * p_hv.b_sex_acts(RG_LRH,t);
      PrevFL = n_hv.adults(VAC_ALL,RG_LRH,CD4_ALL,S_FEMALE) * n_hv.prevalence(RG_LRH,S_FEMALE);
      denom = n_hv.adults(VAC_ALL,RG_LRH,CD4_ALL,S_FEMALE);

      for (int rg2 = RG_MRH; rg2 <= RG_IDU; ++rg2)
      {
        totalSexActsF +=  n_hv.adults(VAC_ALL,rg2,CD4_ALL,S_FEMALE) * i_hv.i_num_partners(rg2+RG_NONE_F3) * p_hv.b_sex_acts(rg2+RG_NONE_F3,t) * p_hv.b_married_prop(rg2+RG_NONE_F3);
        PrevFL += n_hv.adults(VAC_ALL,rg2,CD4_ALL,S_FEMALE) * n_hv.prevalence(rg2,S_FEMALE) * p_hv.b_married_prop(rg2+RG_NONE_F3);
        denom += n_hv.adults(VAC_ALL,rg2,CD4_ALL,S_FEMALE) * p_hv.b_married_prop(rg2+RG_NONE_F3);
      }

       PrevFL = (denom>0.0) ? PrevFL/denom : 0.0;
       PrevF  = PrevFL;

       totalSexActsM = n_hv.adults(VAC_ALL,RG_LRH,CD4_ALL,S_MALE) * i_hv.i_num_partners(rg) * p_hv.b_sex_acts(rg,t);
       PrevML = n_hv.adults(VAC_ALL,RG_LRH,CD4_ALL,S_MALE) * n_hv.prevalence(RG_LRH,S_MALE);
       denom = n_hv.adults(VAC_ALL,RG_LRH,CD4_ALL,S_MALE);
       for (int rg2 = RG_MRH; rg2 <= RG_MSMIDU; ++rg2)
       {
         totalSexActsF +=  n_hv.adults(VAC_ALL,rg2,CD4_ALL,S_MALE) * i_hv.i_num_partners(rg2+RG_NONE_F3) * p_hv.b_sex_acts(rg2+RG_NONE_F3,t) * p_hv.b_married_prop(rg2+RG_NONE_F3);
         PrevML += n_hv.adults(VAC_ALL,rg2,CD4_ALL,S_MALE) * n_hv.prevalence(rg2,S_MALE) * p_hv.b_married_prop(rg2);
         denom += n_hv.adults_ts(VAC_ALL,rg2,CD4_ALL,S_MALE) * p_hv.b_married_prop(rg2);
       }

       PrevML = (denom>0.0) ? PrevML/denom : 0.0;
       PrevM  = PrevML;
    }
    else
    {
      totalSexActsF = n_hv.adults(VAC_ALL,rg,CD4_ALL,S_FEMALE) * i_hv.i_num_partners(rg+RG_NONE_F3) * p_hv.b_sex_acts(rg+RG_NONE_F3,t);
      totalSexActsM = n_hv.adults(VAC_ALL,rg,CD4_ALL,S_MALE) * i_hv.i_num_partners(rg) * p_hv.b_sex_acts(rg,t);

      PrevM = std::max(n_hv.prevalence(rg,S_MALE),PrevML);
      PrevF = std::max(n_hv.prevalence(rg,S_FEMALE),PrevFL);
    }



    // Global multiplier
    rMultM  = i_hv.r_mult(RG_ALL, S_ALL);
    rMultF =  i_hv.r_mult(RG_ALL, S_ALL);

    // Assume equal adjustment for men and women
    double totalSexActs = (totalSexActsM + totalSexActsF) / 2.0;
    SexActsRatioM = (totalSexActsM > 0) ? totalSexActs / totalSexActsM : 1;
    SexActsRatioF = (totalSexActsF > 0) ? totalSexActs / totalSexActsF : 1;

    // Toggle balancing
    if (p_hv.b_balance_sex_acts == 0)
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

     for (int v = VAC_UNV; v <= VAC_NO_PROT; ++v)
     {

        double vacc_effect = 0.0;

       //no new infections in take category
       if(v==VAC_TAKE){
        continue;
       }

       //no_protection category same as unvaccinated
       if(v==VAC_PARTIAL){
        vacc_effect = 1.0;
       }


      //  nda_print_info(dbg_model.hv.epi_redwhen_circum);
       //nda_print_info(dbg_model.hv.i_condom_prop);
      //  nda_print_info(dbg_model.hv.prep_cov);
      //  nda_print_info(dbg_model.hv.prep_effect);
       
      //  nda_print_info(dbg_model.hv.b_sex_acts);
      //  nda_print_info(dbg_model.hv.i_num_partners);
      //  nda_print_info(dbg_model.hv.cured_prop);

       foi  =    1     - std::pow(
                     PrevF * std::pow(
                           (1 - p_hv.epi_transm_hiv_F * (1-vacc_effect) * rMultF *
                               ((1 - circum) + (1 - p_hv.epi_redwhen_circum(HV_SUCC)) * circum) *
                               (1 + (p_hv.epi_transm_sti_mult - 1) * p_hv.epi_sti_prev(rg,t)) *
                               (1 - i_hv.i_condom_prop(rg) * p_hv.epi_condom_effect) *
                               (1 - p_hv.prep_cov(S_MALE,rg,t) * i_hv.prep_effect(rg,t)) *
                               (1 - n_hv.cured_prop(rg,S_MALE))
                           ),
                           p_hv.b_sex_acts(rg,t) * SexActsRatioM) + (1 - PrevF),
                           i_hv.i_num_partners(rg));

       n_hv.new_inf_vrs(v,rg,S_MALE)=std::max(0.0,foi*n_hv.adults(v,rg,CD4_NEG,S_MALE));

       new_inf=n_hv.new_inf_vrs(v,rg,S_MALE);
       total_inf_m+= new_inf;


     } //v, S_MALE

    //women
    s = S_FEMALE;
    for (int v = VAC_UNV; v <= VAC_NO_PROT; ++v)
    {

       double vacc_effect = 0.0;

      //no new infections in take category
      if(v==VAC_TAKE){
        continue;
      }

      //no_protection category same as un vaccinated
      if(v==VAC_PARTIAL){
        vacc_effect = 1.0;
      }

      foi  =    1     - std::pow(
                    PrevM * std::pow(
                          (1 - p_hv.epi_transm_hiv_F * p_hv.epi_transm_mult_M * rMultM * //CDP check per act prob
                              ((1 - circum) + (1 - p_hv.epi_redwhen_circum(HV_INF)) * circum) *
                              (1 + (p_hv.epi_transm_sti_mult - 1) * p_hv.epi_sti_prev(rg,t)) * //check index
                              (1 - i_hv.i_condom_prop(rg) * p_hv.epi_condom_effect)   *   //
                              (1 - p_hv.prep_cov(S_FEMALE,rg,t) * i_hv.prep_effect(rg,t))  *
                              (1 - n_hv.cured_prop(rg,S_FEMALE))
                          ),
                          p_hv.b_sex_acts(rg,t) * SexActsRatioF) + (1 - PrevM),
                          i_hv.i_num_partners(rg));

      n_hv.new_inf_vrs(v,rg,S_FEMALE)=std::max(0.0,foi*n_hv.adults(v,rg,CD4_NEG,S_FEMALE));

      new_inf=n_hv.new_inf_vrs(v,rg,S_FEMALE);
      total_inf_f+= new_inf;


    }//v, S_FEMALE


}//rg

//nda_print_info(dbg_model.hv.new_inf_vrs,VAC_UNV,VAC_UNV,-1,-1,0,0);
//nda_print_info(dbg_model.hv.new_inf_vrs,VAC_UNV,VAC_UNV,-1,-1,1,1);

  if(true){
    for (int rg = RG_MSM; rg <= RG_MSM; ++rg)
    {

        //MSM multiplier calculated among MSM groups only
        rMultM =i_hv.r_mult(rg, S_MALE);

        //men
        int s = S_MALE;
        double circum=p_hv.rn_coverage(INTVN_MC15_49,t);

        for (int v = VAC_UNV; v <= VAC_NO_PROT; ++v)
        {

          double vacc_effect = 0.0;

          //no new infections in take category
          if(v==VAC_TAKE){
            continue;
          }

          //no_protection category same as un vaccinated
          if(v==VAC_PARTIAL){
            vacc_effect = 1.0;
          }

          foi  =    1     - std::pow(
                        PrevM * std::pow(
                              (1 - p_hv.epi_transm_hiv_F * (1-vacc_effect) * rMultM *
                                  ((1 - circum) + (1 - p_hv.epi_redwhen_circum(HV_INF)) * circum) *
                                  p_hv.epi_transm_mult_MSM *
                                  (1 + (p_hv.epi_transm_sti_mult - 1) * p_hv.epi_sti_prev(rg,t)) *
                                  (1 - i_hv.i_condom_prop(rg) * p_hv.epi_condom_effect) *
                                  (1 - p_hv.prep_cov(S_MALE,rg,t) * i_hv.prep_effect(rg,t)) *
                                  (1 - n_hv.cured_prop(rg,S_MALE))
                              ),
                              p_hv.b_sex_acts(rg,t) * SexActsRatioM) + (1 - PrevM),
                              i_hv.i_num_partners(rg));

          n_hv.new_inf_vrs(v,rg,S_MALE)=std::max(0.0,foi*n_hv.adults(v,rg,CD4_NEG,S_MALE));

          new_inf= n_hv.new_inf_vrs(v,rg,S_MALE);
          total_inf_m+= new_inf;


        } //v, S_MALE



    } //rg MSM
  }

  if(false){

    int rg = RG_IDU;

    //Assuming IDU have medium risk sexual behavior, see r=HV_MRH above
    PrevM=PrevM_IDU;
    PrevF=PrevF_IDU;
    SexActsRatioM=SexActsRatioM_IDU;
    SexActsRatioF=SexActsRatioF_IDU;

    rMultM = i_hv.r_mult(RG_ALL, S_MALE);
    rMultF = i_hv.r_mult(RG_ALL, S_FEMALE);

    //IDU risk, partner prevalence calc
    double PrevB = 0.0;
    if(       n_hv.adults(VAC_ALL,RG_IDU,CD4_ALL,S_MALE) +
              n_hv.adults(VAC_ALL,RG_IDU,CD4_ALL,S_FEMALE)+
              n_hv.adults(VAC_ALL,RG_MSMIDU,CD4_ALL,S_MALE)>0.0){

      PrevB = (n_hv.prevalence(RG_IDU,S_MALE)    * n_hv.adults(VAC_ALL,RG_IDU,CD4_ALL,S_MALE) +
                n_hv.prevalence(RG_IDU,S_FEMALE)  * n_hv.adults(VAC_ALL,RG_IDU,CD4_ALL,S_FEMALE)+
                n_hv.prevalence(RG_MSMIDU,S_MALE) * n_hv.adults(VAC_ALL,RG_MSMIDU,CD4_ALL,S_MALE)) /
              (n_hv.adults(VAC_ALL,RG_IDU,CD4_ALL,S_MALE) +
              n_hv.adults(VAC_ALL,RG_IDU,CD4_ALL,S_FEMALE)+
              n_hv.adults(VAC_ALL,RG_MSMIDU,CD4_ALL,S_MALE));
      }

      PrevB = (i_hv.i_idu_share_prop>0.0) ? PrevB / i_hv.i_idu_share_prop : PrevB;

      PrevB = std::max(PrevB,  std::min(n_hv.prevalence(RG_LRH,S_MALE),n_hv.prevalence(RG_LRH,S_FEMALE))) ;

      double SusceptibleIDU =0;
      double foi_idu_sex=0;
      for (int s = S_MALE; s <= S_FEMALE; ++s)
      {
        for (int v = VAC_UNV; v <= VAC_NO_PROT; ++v)
        {

          SusceptibleIDU = n_hv.adults(v,RG_IDU,CD4_NEG,s);
          if(SusceptibleIDU > n_hv.adults(v,RG_IDU,CD4_ALL,s) * i_hv.i_idu_share_prop -
                              (n_hv.adults(v,RG_IDU,CD4_ALL,s) - n_hv.adults(v,RG_IDU,CD4_NEG,s))){

              SusceptibleIDU = n_hv.adults(v,RG_IDU,CD4_ALL,s) * i_hv.i_idu_share_prop -
                            (n_hv.adults(v,RG_IDU,CD4_ALL,s) - n_hv.adults(v,RG_IDU,CD4_NEG,s));
          }

          double vacc_effect = 0.0;

          //no new infections in take category
          if(v==VAC_TAKE){
            continue;
          }

          //no_protection category same as un vaccinated
          if(v==VAC_PARTIAL){
            vacc_effect = 1.0;
          }

          if(s==S_MALE)
          {

            foi_idu_sex  =    1   - std::pow(
                          PrevF * std::pow(
                                (1 - p_hv.epi_transm_hiv_F * (1-vacc_effect) * rMultF *
                                    ((1 - circum) + (1 - p_hv.epi_redwhen_circum(HV_SUCC)) * circum) *
                                    (1 + (p_hv.epi_transm_sti_mult - 1) * p_hv.epi_sti_prev(rg,t)) *
                                    (1 - i_hv.i_condom_prop(rg) * p_hv.epi_condom_effect) *
                                    (1 - p_hv.prep_cov(S_MALE,rg,t) * i_hv.prep_effect(rg,t)) *
                                    (1 - n_hv.cured_prop(rg,S_MALE))
                                ),
                                p_hv.b_sex_acts(rg,t) * SexActsRatioM) + (1 - PrevF),
                                i_hv.i_num_partners(rg));


          }
          else
          {
            foi_idu_sex  =    1     - std::pow(
                      PrevM * std::pow(
                            (1 - p_hv.epi_transm_hiv_F * p_hv.epi_transm_mult_M * rMultM * //CDP check per act prob
                                ((1 - circum) + (1 - p_hv.epi_redwhen_circum(HV_INF)) * circum) *
                                (1 + (p_hv.epi_transm_sti_mult - 1) * p_hv.epi_sti_prev(rg,t)) * //check index
                                (1 - i_hv.i_condom_prop(rg) * p_hv.epi_condom_effect)   *   //
                                (1 - p_hv.prep_cov(S_FEMALE,rg,t) * i_hv.prep_effect(rg,t))  *
                                (1 - n_hv.cured_prop(rg,S_FEMALE))
                            ),
                            p_hv.b_sex_acts(rg,t) * SexActsRatioF) + (1 - PrevM),
                            i_hv.i_num_partners(rg));



          }

          
          //sexual transmission
          n_hv.new_inf_vrs(v,rg,s) = std::max(0.0,foi_idu_sex * SusceptibleIDU);

          //needle sharing
          n_hv.new_inf_vrs(v,rg,s) += p_hv.b_foi_idu(s,t) * i_hv.r_mult(RG_ALL, S_ALL) * PrevB * SusceptibleIDU *
                                                        (1-p_hv.prep_cov(s,rg,t) * i_hv.prep_effect(rg,t));
                                                        //+_ForceNeedleTransmIDU*SusceptibleIDU;//no explicit needle sharing mechanism

      }//v

    }//s

  }


  //std::cout << "new if men " << std::endl;
  //auto dbg_model = capture_model(state_next, intermediate, pars);
  //nda_print_info(dbg_model.hv.new_inf_vrs,VAC_UNV,VAC_UNV,1,5,0,0);

  //std::cout << "initial inf m: t " << t  << " t1 " << hiv_step << " " << total_inf_m << std::endl;
  //std::cout << "initial inf f: t " << t  << " t1 " << hiv_step << " " << total_inf_f << std::endl;

   //double x=0;


}

void add_new_infections_goals(int t, int hiv_step)
{

  
  const auto& p_ha = pars.ha;
  auto& n_ha = state_next.ha;
  
  //new infections from goals
  const auto& p_hv = pars.hv;
  auto& n_hv = state_next.hv;
  auto& i_hv = intermediate.hv;

  nda::fill(n_hv.new_inf_s, 0.0);//new infections for each t, by sex, for aim

  int a25 = 10;
  double new_inf_input=0.0;

  for (int v = VAC_UNV; v <= VAC_NO_PROT; ++v)
  {
      for (int rg = RG_LRH; rg <= RG_MSMIDU; ++rg)
      {
          for (int s = S_MALE; s <= S_FEMALE; ++s)
          {

              if (!((s == S_FEMALE) && (rg >= RG_MSM)))
              {
                  //New inf from goals used as inputs
                  new_inf_input=p_hv.out_new_inf(s,rg,v,t);
                  //if(new_inf_input>0.0)
                  //{
                  //  int new_inf_t=t;
                  //}
                 
                  //Remove new infections from HIV‑negative category
                  n_hv.adults(v,rg,CD4_NEG,s) -= opts.dt * new_inf_input;
                  if(n_hv.adults(v,rg,CD4_NEG,s)<0) {
                    n_hv.adults(v,rg,CD4_NEG,s)=0;
                  }
                  n_hv.new_inf_s(s) += opts.dt * new_inf_input;
                  n_hv.total_new_infections += opts.dt * new_inf_input;


                  //Add new infections to each HIV‑positive stage
                  for (int hd = CD4_PRIM; hd <= CD4_LT50; ++hd)
                  {
                    
                    int hd_hds = 0; //set prim

                    if(hd==CD4_GT500){
                      continue; //see goals
                    }

                    if(hd>=CD4_350_500){
                      hd_hds = hd - CD4_GT500; //CD4_350_500 and higher indices
                    }    

                    n_hv.adults(v,rg,hd,s) += opts.dt * new_inf_input * p_ha.cd4_initial_distribution(hd_hds, a25, s);

                  }
              }
          } //s
      } //r
  } //v

  //const auto adult_incid_first_age_group = p_ha.pIDX_INCIDPOP;
 // const auto adult_incid_last_age_group = adult_incid_first_age_group + p_ha.pAG_INCIDPOP;

  //n_hv.new_infections_dp=0;
  double num_s_both = 0.0;
  double denom_s_both = 0.0;
  if(hiv_step==0)
  {
      for (int s = S_MALE; s <= S_FEMALE; ++s)
      {
        double num   = 1/ opts.dt * n_hv.new_inf_s(s); //dp needs annual new infections, distributes for each hiv_step
        double denom = i_hv.dp_aging_denom_1549(POP_H_HIVNeg, CD4_NEG, s);

        num_s_both += num;
        denom_s_both += denom;
        
        n_hv.incidence_goals(s) = num / denom;
        n_hv.new_infections_goals(s) = num;

        //for(int a = SS::pIDX_15to49; a < SS::pIDX_15to49 + SS::pAG_15to49; ++a) 
       // for (int a = adult_incid_first_age_group; a < adult_incid_last_age_group; ++a) {
        //  n_hv.new_infections_dp += n_ha.p_infections(a, s);
      //}
    }  

    n_hv.incidence_goals(S_ALL) = num_s_both / denom_s_both;
    n_hv.new_infections_goals(S_ALL) = num_s_both;

    //auto dbg_model = capture_model(state_next, intermediate, pars);
    //nda_print_info(dbg_model.hv.adults,VAC_UNV,VAC_UNV,RG_LRH,RG_LRH,-1,-1,-1,-1);

 } 
}


void add_new_infections(int t, int hiv_step)
{

  
  const auto& p_ha = pars.ha;
  auto& n_ha = state_next.ha;
  
  //new infections from goals
  const auto& p_hv = pars.hv;
  auto& n_hv = state_next.hv;
  auto& i_hv = intermediate.hv;

  nda::fill(n_hv.new_inf_s, 0.0);//new infections for each t, by sex, for aim

  int a25 = 10;
  double new_inf_input=0.0;

  for (int v = VAC_UNV; v <= VAC_NO_PROT; ++v)
  {
      for (int rg = RG_LRH; rg <= RG_MSMIDU; ++rg)
      {
          for (int s = S_MALE; s <= S_FEMALE; ++s)
          {

              if (!((s == S_FEMALE) && (rg >= RG_MSM)))
              {
                  //New inf from goals used as inputs
                  new_inf_input=n_hv.new_inf_vrs(v,rg,s);
                  //if(new_inf_input>0.0)
                  //{
                  //  int new_inf_t=t;
                  //}
             
                  //Remove new infections from HIV‑negative category
                  n_hv.adults(v,rg,CD4_NEG,s) -= opts.dt * new_inf_input;
                  if(n_hv.adults(v,rg,CD4_NEG,s)<0) {
                    n_hv.adults(v,rg,CD4_NEG,s)=0;
                  }
                  n_hv.new_inf_s(s) += opts.dt * new_inf_input;
                  n_hv.total_new_infections += opts.dt * new_inf_input;


                  //Add new infections to each HIV‑positive stage
                  for (int hd = CD4_PRIM; hd <= CD4_LT50; ++hd)
                  {
                    
                    int hd_hds = 0; //set prim

                    if(hd==CD4_GT500){
                      continue; //see goals
                    }

                    if(hd>=CD4_350_500){
                      hd_hds = hd - CD4_GT500; //CD4_350_500 and higher indices
                    }    

                    n_hv.adults(v,rg,hd,s) += opts.dt * new_inf_input * p_ha.cd4_initial_distribution(hd_hds, a25, s);

                  }
              }
          } //s
      } //r
  } //v

  //const auto adult_incid_first_age_group = p_ha.pIDX_INCIDPOP;
 // const auto adult_incid_last_age_group = adult_incid_first_age_group + p_ha.pAG_INCIDPOP;

  //n_hv.new_infections_dp=0;
  double num_s_both = 0.0;
  double denom_s_both = 0.0;
  
  //nda::fill(n_hv.new_infections_goals, 0.0);//incidence for DP, init at initial pulse

  //if(hiv_step==0)
  //{
      for (int s = S_MALE; s <= S_FEMALE; ++s)
      {
        double num   = 1/ opts.dt * n_hv.new_inf_s(s); //dp needs annual new infections, distributes for each hiv_step
        double denom = i_hv.dp_aging_denom_1549(POP_H_HIVNeg, CD4_NEG, s);

        num_s_both += num;
        denom_s_both += denom;
        
        n_hv.incidence_goals(s) = num / denom;
        n_hv.new_infections_goals(s) = num;

        //for(int a = SS::pIDX_15to49; a < SS::pIDX_15to49 + SS::pAG_15to49; ++a) 
         // for (int a = adult_incid_first_age_group; a < adult_incid_last_age_group; ++a) {
        //  n_hv.new_infections_dp += n_ha.p_infections(a, s);
        //}
      }  

    n_hv.incidence_goals(S_ALL) = num_s_both / denom_s_both;
    n_hv.new_infections_goals(S_ALL) = num_s_both;

    //auto dbg_model = capture_model(state_next, intermediate, pars);
    //nda_print_info(dbg_model.hv.adults,VAC_UNV,VAC_UNV,RG_LRH,RG_LRH,-1,-1,-1,-1);

 //} 
}



void add_new_infections2()
{

  const auto& p_ha = pars.ha;

  //calculated new infections
  auto& n_hv = state_next.hv;

  for (int v = VAC_UNV; v <= VAC_NO_PROT; ++v)
  {
      for (int rg = RG_LRH; rg <= RG_MSMIDU; ++rg)
      {
          for (int s = S_MALE; s <= S_FEMALE; ++s)
          {

              if (!((s == S_FEMALE) && (rg >= RG_MSM)))
              {
                  // Remove new infections from HIV‑negative category
                  n_hv.adults(v,rg,CD4_NEG,s) -= opts.dt * n_hv.new_inf_vrs(v,rg,s);
                  n_hv.new_inf_s(s) += opts.dt * n_hv.new_inf_vrs(v,rg,s);
                  n_hv.total_new_infections += opts.dt * n_hv.new_inf_vrs(v,rg,s);;


                  // Add new infections to each HIV‑positive stage
                  for (int hd = CD4_PRIM; hd <= CD4_LT50; ++hd)
                  {
                     int hd_hds = 0; //set prim

                     if(hd==CD4_GT500){
                      continue; //see goals
                     }

                     if(hd>=CD4_350_500){
                       hd_hds = hd - CD4_GT500; //CD4_350_500 and higher indices
                     }   

                     n_hv.adults(v,rg,hd,s) += opts.dt * n_hv.new_inf_vrs(v,rg,s) * p_ha.cd4_initial_distribution(hd_hds, pIDX_15to49+10, s);

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

real_type not_receiving_art_vrhs[nVAC][nRG][nCD4p][nNS]={};
real_type eligible_art_vrhs[nVAC][nRG][nCD4p][nNS]={};

real_type receiving_art_vrs[nVAC][nRG][nNS]={};
real_type not_receiving_art_vrs[nVAC][nRG][nNS]={};
real_type start_art[nVAC][nRG][nNS]= {};
real_type sum_elig_art[nVAC][nRG][nNS]={};

real_type  sex_age_hiv[POP_H_ALL][nNS]={};
real_type  art_cov[RG_TOTAL_ART][nNS]={};
bool  kp_cd4_elig[RG_TOTAL_ART][nNS]={};

real_type new_patients[nCD4p]={};
real_type mort_rate[nCD4p]={};
real_type prop1[nCD4p]={};
real_type prop2[nCD4p]={};
real_type prop_avg[nCD4p]={};

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

int rg_eligible_treat_year[DP_EligTreatPopsMax]={};
bool rg_eligible_treat[DP_EligTreatPopsMax]={};

for (int rg = RG_NONE; rg <= RG_TOTAL1; ++rg) {

  rg_eligible_treat_year[rg]= 2010;
  
  for (int s = S_MALE; s <= S_FEMALE; ++s) {
      kp_cd4_elig[rg][s] = true;
  }
  
  //rg_eligible_treat[rg]= false;
}


/*
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
*/

prop_by_mort = p_ha.initiation_mortality_weight;
prop_by_elig = 1-prop_by_mort;

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
                }//v
            }//rg
        }//hd
    }//s
}//if (ltfu > 0)


for (int s = S_MALE; s <= S_FEMALE; ++s) {
  sex_age_hiv[POP_H_NoART][s] = 0.0;
  sex_age_hiv[POP_H_OnART][s] = 0.0;
  for (int hd = CD4_GT500; hd <= CD4_LT50; ++hd) {
        sex_age_hiv[POP_H_NoART][s] += i_hv.dp_aging_denom_1549(POP_H_NoART, hd, s);
        sex_age_hiv[POP_H_OnART][s] += i_hv.dp_aging_denom_1549(POP_H_ARTlt6m, hd, s)+
                                       i_hv.dp_aging_denom_1549(POP_H_ART6to12m, hd, s)+
                                       i_hv.dp_aging_denom_1549(POP_H_ARTgt12m, hd, s);
    }
}

 //set rg eligibility and year
 if(rg_eligible_treat[DP_EligTreatSexWorkers]==true)
 {
    if(rg_eligible_treat_year[DP_EligTreatSexWorkers]<=t){
      kp_cd4_elig[RG_HRH][S_FEMALE] = false;
    }  
 }


if(rg_eligible_treat[DP_EligTreatMSM]==true)
{
  if(rg_eligible_treat_year[DP_EligTreatMSM]<=t){
    kp_cd4_elig[RG_MSM][S_MALE] = false;
  }
}

 if(rg_eligible_treat[DP_EligTreatIDU]==true)
 {
    if(rg_eligible_treat_year[DP_EligTreatIDU]<=t)
    {
      kp_cd4_elig[RG_IDU][S_MALE] = false;
      kp_cd4_elig[RG_IDU][S_FEMALE] = false;
    }
 }


// Set ART coverage for all risk groups to AIM 15 to 49 coverage
// CDP confirm order of inner loop calcs between leapfrog dp and goals 
if (sex_age_hiv[POP_H_OnART][S_FEMALE] > 0.0){
    for (int rg = RG_NONE; rg <= RG_TOTAL1; ++rg)
    {
       art_cov[rg][S_MALE] = 0.0/100.0;
       if(sex_age_hiv[POP_H_NoART][S_MALE]+sex_age_hiv[POP_H_OnART][S_MALE] > 0.0){
          art_cov[rg][S_MALE] = sex_age_hiv[POP_H_OnART][S_MALE] /
                                (sex_age_hiv[POP_H_NoART][S_MALE]+sex_age_hiv[POP_H_OnART][S_MALE]);
       }
 
        art_cov[rg][S_FEMALE] = 0.0/100.0;
        if(sex_age_hiv[POP_H_NoART][S_FEMALE]+sex_age_hiv[POP_H_OnART][S_FEMALE]>0.0){
         art_cov[rg][S_FEMALE] = sex_age_hiv[POP_H_OnART][S_FEMALE] /
                                (sex_age_hiv[POP_H_NoART][S_FEMALE]+sex_age_hiv[POP_H_OnART][S_FEMALE]);
        }
      }
}//if sex_age_hiv[S_FEMALE][POP_H_OnART] > 0.0


// Set ART coverage for all risk groups to AIM 15 to 49 coverage
// for (int s = S_MALE; s <= S_FEMALE; ++s)
// for (int rg = RG_NONE; rg <= RG_TOTAL1; ++rg)
// {
//     rt_cov[rg][S_MALE] =p_ha.adults_on_art(s, t);
// }


//KP coverage from AIM input editor
//if (p_hv.art_cov_num_percent == ART_RG_PERCENT)
//if (p_hv.art_cov_num_percent == 0)
if (false)
{
    // Coverage for males, risk groups HV_IDU … HV_MSM
    for (int rg = RG_IDU; rg <= RG_MSM; ++rg)
    {
        art_cov[rg][S_MALE] = p_hv.art_coverage_rg(S_MALE, rg, t);//CDP check /100
    }

    // Coverage for females, risk groups HV_HRH … HV_IDU
    for (int rg = RG_HRH; rg <= RG_IDU; ++rg)
    {
        art_cov[rg][S_FEMALE]= p_hv.art_coverage_rg(S_FEMALE, rg, t);
    }
}

//auto dbg_model = capture_model(state_next, intermediate, pars);
//nda_print_info(dbg_model.hv.dp_aging_denom_1549,POP_H_NoART,POP_H_NoART,-1,-1,0,0);
//nda_print_info(dbg_model.hv.dp_aging_denom_1549,POP_H_ARTlt6m,POP_H_ARTlt6m,-1,-1,0,0);

//nda_print_info(dbg_model.hv.adults,VAC_UNV,VAC_UNV,RG_LRH,RG_LRH,-1,-1,0,0);

// Calc new ART by sex and rg and allocate it
for (int s = S_MALE; s <= S_FEMALE; s++)
{
    //calc numbers eligible
    for (int hd = CD4_GT500; hd <= CD4_LT50; ++hd)
    {
        
        int hd_hds = hd - CD4_GT500;
        for (int rg = RG_NONE; rg <= RG_TOTAL1; ++rg)
        {
            
            if (s == S_FEMALE && rg >= RG_MSM){
              continue;
            }

            for (int v = VAC_UNV; v <= VAC_NO_PROT; ++v)
            {
                // not receiving ART (by sex & rg)
                not_receiving_art_vrs[v][rg][s] += n_hv.adults(v,rg,hd,s);//CDP check adults or adultsTS
                not_receiving_art_vrhs[v][rg][hd][s] += n_hv.adults(v,rg,hd,s);

                // receiving ART (by sex & rg)
                receiving_art_vrs[v][rg][s] += n_hv.adults(v,rg,hd+hOnArt,s);

                if (kp_cd4_elig[rg][s] == true)
                {
                    if (hd_hds>=i_ha.everARTelig_idx)//CDP check role of this condition
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
        
        if (s == S_FEMALE && rg >= RG_MSM){
            continue;
        }
        
        for (int v = VAC_UNV; v <= VAC_NO_PROT; ++v) {

            start_art[v][rg][s]=(not_receiving_art_vrs[v][rg][s] + receiving_art_vrs[v][rg][s]) *
                                 art_cov[rg][s] - receiving_art_vrs[v][rg][s];

            // aggregate both sexes – required for comparison with AIM
            //start_art[v][rg][S_ALL] += start_art[v][rg][s];

            //allocate new ART according to eligibility (Prop1) and mortality (Prop2)
            for (int hd = CD4_GT500; hd <= CD4_LT50; ++hd) {
                prop1[hd]        = 0.0;
                mort_rate[hd]    = 0.0;
                prop2[hd]        = 0.0;
                new_patients[hd] = 0.0;
            }


            if(sum_elig_art[v][rg][s] > 0.0) {
                  for (int hd = CD4_GT500; hd <= CD4_LT50; ++hd) {
                      if (hd == CD4_GT500) {
                          prop1[hd] = (eligible_art_vrhs[v][rg][hd][s] +
                                      eligible_art_vrhs[v][CD4_PRIM ][rg][s]) / sum_elig_art[v][rg][s];
                      } else {
                          prop1[hd] = eligible_art_vrhs[v][rg][hd][s] / sum_elig_art[v][rg][s];
                      }
                  } //hd
            }//if


            //proportion according to mortality
            double sum1 = 0.0;
            for (int hd = CD4_GT500; hd <= CD4_LT50; ++hd) {
                sum1 += opts.dt * i_hv.hiv_mu(hd,s) *
                                  eligible_art_vrhs[v][rg][hd][s];
            }//hd

            if (sum1 > 0.0) {
                for (int hd = CD4_GT500 ; hd <= CD4_LT50 ; ++hd) {
                    mort_rate[hd] = opts.dt * i_hv.hiv_mu(hd,s) *
                                              eligible_art_vrhs[v][rg][hd][s] / sum1;
                }//hd
            }//if


            //weighted average of number eligible and mortality
            remaining_new_art = start_art[v][rg][s];
            for (int hd = CD4_LT50; hd >= CD4_GT500; --hd) {
                sum1 = 0.0;
                for (int h2 = hd; h2 >= CD4_GT500 ; --h2) {
                    sum1 += eligible_art_vrhs[v][rg][h2][s] * mort_rate[h2];
                }

    
                 new_patients[hd] = (sum1>0.0) ? remaining_new_art *
                                    (eligible_art_vrhs[v][rg][hd][s] * mort_rate[hd]) / sum1 : 0.0;
              

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


              //calculate proportion starting (Prop2)
              for (int hd = CD4_GT500; hd <= CD4_LT50; ++hd) {
                  prop2[hd] = 0.0;
                  if (start_art[v][rg][s] > 0.0) {
                      prop2[hd] = new_patients[hd] / start_art[v][rg][s];
                  }
              }//hd

              //final average of the two methods (propAvg)
              for (int hd = CD4_GT500; hd <= CD4_LT50 ; ++hd) {
                  prop_avg[hd] = prop_by_elig * prop1[hd] + prop_by_mort * prop2[hd];
              }//hd

              //allocate the new ART by CD4 category
              if (start_art[v][rg][s] > 0.0) {
                  for (int hd = CD4_GT500; hd <= CD4_LT50; ++hd) {

                     entrants = prop_avg[hd] * start_art[v][rg][s];

                      // cannot remove ART patients!
                      entrants = std::max(entrants, 0.0);

                      // respect the cap for new ART
                      entrants = std::min(entrants, new_art_cap * n_hv.adults(v,rg,hd,s));

                      if(n_hv.adults(v,rg,hd,s) - entrants > 0){
                        // HIV+ not on ART -> subtract entrants
                        n_hv.adults(v,rg,hd,s) -= entrants;

                        // HIV+ on ART -> add entrants (note the +10 offset)
                        n_hv.adults(v,rg,hd+hOnArt,s)+= entrants;
                      }


                      // keep track of newly started ART
                      n_hv.newly_on_art(hd,s) += entrants; //CDP check init of this array
                  }//hd
              }//if (StartART[s][rg][v] > 0.0)

        } // v

    } // end r


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
               n_hv.adults(v,rg,hd,S_ALL)=0.0;
               real_type sum = 0.0;
               for (int s = S_MALE; s <= S_FEMALE; ++s)
               {
                    // Exclude female MSM and higher risk groups
                    if(!((s == S_FEMALE) && (rg >= RG_MSM) && (rg <= RG_MSMIDU))){
                        sum += n_hv.adults(v,rg,hd,s);
                    }    
                } //s

                //if(sum>0.0){
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
                  n_hv.adults(v,rg,CD4_ALL,s) = 0.0;
                  real_type sum = 0.0;
                  for (int hd = CD4_NEG; hd <= CD4_LT50_ART; ++hd)
                  {
                      // Exclude female MSM and higher risk groups
                      if (!((s == S_FEMALE) && (rg >= RG_MSM))){
                          sum += n_hv.adults(v,rg,hd,s);
                      }   
                  }//hd
                  //if(sum>0.0){
                    n_hv.adults(v,rg,CD4_ALL,s) = sum;
                  //}

              } //s
            } //rg
        }//v


       for (int v = VAC_UNV; v <= VAC_NO_PROT; ++v)
       {
          for (int hd = CD4_NEG; hd <= CD4_ALL; ++hd)
          {
              for (int s = S_MALE; s <= S_ALL; ++s)
              {
                  n_hv.adults(v,RG_ALL,hd,s) = 0.0;
                  real_type sum = 0.0;
                  for (int rg = RG_NONE; rg <= RG_MSMIDU; ++rg)
                  {
                      // Exclude female MSM and higher risk groups
                      if (!((s == S_FEMALE) && (rg >= RG_MSM))){
                          sum += n_hv.adults(v,rg,hd,s);
                      }    
                  }//hd

                  //if(sum>0.0){
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
                  
                  n_hv.adults(VAC_ALL,rg,hd,s) = 0.0;
                  real_type sum = 0.0;
                  for (int v = VAC_UNV; v <= VAC_NO_PROT; ++v)
                  {
                      // Exclude female MSM and higher risk groups
                      if(!((s == S_FEMALE) && (rg >= RG_MSM) && (rg < RG_ALL))){
                          sum += n_hv.adults(v,rg,hd,s);
                      }    
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

  // private methods that we don't want people to call
  private:

void calc_adj_matrix(int t) {

    const auto& c_dp = state_curr.dp;

    const auto& p_hv = pars.hv;
    auto& i_hv = intermediate.hv;

    int GoalsBaseYearIdx=p_hv.goals_base_year_idx;
    nda::fill(i_hv.adj_coverage_base_yr, 0.0);
    nda::fill(i_hv.adj_coverage, 0.0);

    // Calc adjusted coverage
    for (int i = 1; i <= RN_MAX_BEHAV_INTVN; ++i) {
        i_hv.adj_coverage_base_yr(i) = p_hv.rn_coverage(i,GoalsBaseYearIdx);
    }


    for (int i = 1; i <= RN_MAX_BEHAV_INTVN; ++i) {
        switch (i) {

             case RN_COMP_SEX_EDUC: {
                // Adjust coverage of school-based intervention for proportion of adults that are in school
                double coverageDiff = p_hv.rn_coverage(i,t) - i_hv.adj_coverage_base_yr(i);
                double avgSchoolPop = (p_hv.rn_pop_sizes(RN_POP_SEC_SCHOOL_MALE,t) + p_hv.rn_pop_sizes(RN_POP_SEC_SCHOOL_FEMALE,t)) / 2.0;

                double popRatio =0;
                for(int a = 10; a < 19; ++a)
                 popRatio +=(c_dp.p_totpop(a, S_MALE)+c_dp.p_totpop(a, S_FEMALE));


                double total_pop = i_hv.dp_totpop_1549(S_MALE)+i_hv.dp_totpop_1549(S_FEMALE);//CDP check t
                popRatio = (total_pop>0.0) ? (popRatio/total_pop) : 0.0;

                i_hv.adj_coverage(i) = coverageDiff * avgSchoolPop * popRatio;
                break;
            }
            case RN_ECON_STRENGTH: {
                // Adjust coverage of workplace interventions for proportion of adults in formal sector labor force
                double coverageDiff = p_hv.rn_coverage(i,t) - i_hv.adj_coverage_base_yr(i);

                double popRatio =0;
                for(int a = 15; a < 19; ++a)
                 popRatio +=c_dp.p_totpop(a, S_FEMALE);

                double total_pop = i_hv.dp_totpop_1549(S_MALE)+i_hv.dp_totpop_1549(S_FEMALE);//CDP check denom and t
                popRatio = (total_pop > 0.0) ? (popRatio/total_pop) : 0.0;

                i_hv.adj_coverage(i) = coverageDiff * popRatio;
                break;
            }

            default: {
                i_hv.adj_coverage(i) = p_hv.rn_coverage(i,t) - i_hv.adj_coverage_base_yr(i);
                break;
            }
        }//switch i
    }//i


}


void calc_behav_matrix_impacts()
{

  const auto& p_hv = pars.hv;
  auto& i_hv = intermediate.hv;

  nda::fill(i_hv.adj_coverage_prod, 1.0);

  std::list<int> RN_UsedInterventions = {RN_COMP_SEX_EDUC,RN_FSW_OUTREACH,RN_ECON_STRENGTH,
                                        RN_IDU_HARM_RED,RN_IDU_NSEP,RN_IDU_DRUG_SUB,
                                        RN_MSM_OUTREACH,RN_CONDOMS,RN_CONDOM_SUPPLY,RN_ANC_TESTING};

  double impact=0;


   for (int j = 1; j <= HV_MAX_BEHAV_IMPACTS; ++j) {

      for (int  i = 1; i <= RN_MAX_BEHAV_INTVN; ++i) {

            // a few interventions are now excluded from the editors and RN calcs
            if (std::ranges::find(RN_UsedInterventions, i) == RN_UsedInterventions.end()) {
              continue;
            }

            i_hv.adj_coverage_prod(j) *= (1+i_hv.adj_coverage(i) * p_hv.hv_impact_matrix(i,j));
       }//i

       i_hv.adj_coverage_prod(j) = std::clamp(i_hv.adj_coverage_prod(j), 0.0, 1.0);

    }//j




  for (int j = 1; j <= HV_MAX_BEHAV_IMPACTS; ++j) {

      switch (j) {

         //condom use
         case HV_IM_CONDOMS_LOW: {

              impact = 1-(1-i_hv.i_condom_prop(RG_LRH)) * i_hv.adj_coverage_prod(HV_IM_CONDOMS_LOW);
              impact = std::clamp(impact, 0.0, 1.0);
              i_hv.i_condom_prop(RG_LRH) = impact;

              break;
          }
          case HV_IM_CONDOMS_MED: {

              impact = 1-(1-i_hv.i_condom_prop(RG_MRH)) * i_hv.adj_coverage_prod(HV_IM_CONDOMS_MED);
              impact = std::clamp(impact, 0.0, 1.0);
              i_hv.i_condom_prop(RG_MRH) = impact;

              break;
          }

          case HV_IM_CONDOMS_HIGH: {

              impact = 1-(1-i_hv.i_condom_prop(RG_HRH)) * i_hv.adj_coverage_prod(HV_IM_CONDOMS_HIGH);
              impact = std::clamp(impact, 0.0, 1.0);
              i_hv.o_condom_prop(RG_HRH) = impact;

              break;
          }

          case HV_IM_CONDOMS_IDU: {

              impact = 1-(1-i_hv.i_condom_prop(RG_IDU)) * i_hv.adj_coverage_prod(HV_IM_CONDOMS_IDU);
              impact = std::clamp(impact, 0.0, 1.0);
              i_hv.i_condom_prop(RG_IDU) = impact;

              break;
          }

          case HV_IM_CONDOMS_MSM: {

              impact = 1-(1-i_hv.i_condom_prop(RG_MSM)) * i_hv.adj_coverage_prod(HV_IM_CONDOMS_MSM);
              impact = std::clamp(impact, 0.0, 1.0);
              i_hv.i_condom_prop(RG_MSM) = impact;

              break;
          }

          //number of partners
          case HV_IM_PARTNERS_LOW: {

              impact = i_hv.i_num_partners(RG_LRH) * i_hv.adj_coverage_prod(HV_IM_PARTNERS_LOW);
              impact = std::clamp(impact, 0.0, 1000.0);
              i_hv.i_num_partners(RG_LRH) = impact;

              break;
          }

          case HV_IM_PARTNERS_MED: {

              impact = i_hv.i_num_partners(RG_MRH) * i_hv.adj_coverage_prod(HV_IM_PARTNERS_MED);
              impact = std::clamp(impact, 0.0, 1000.0);
              i_hv.i_num_partners(RG_MRH) = impact;

              break;
          }

          case HV_IM_PARTNERS_HIGH: {

              impact = i_hv.i_num_partners(RG_HRH) * i_hv.adj_coverage_prod(HV_IM_PARTNERS_HIGH);
              impact = std::clamp(impact, 0.0, 1000.0);
              i_hv.i_num_partners(RG_HRH) = impact;

              break;
          }


          case HV_IM_PARTNERS_IDU: {

              impact = i_hv.i_num_partners(RG_IDU) * i_hv.adj_coverage_prod(HV_IM_PARTNERS_IDU);
              impact = std::clamp(impact, 0.0, 1000.0);
              i_hv.i_num_partners(RG_IDU) = impact;

              break;
          }

          case HV_IM_PARTNERS_MSM: {

              impact = i_hv.i_num_partners(RG_MSM) * i_hv.adj_coverage_prod(HV_IM_PARTNERS_MSM);
              impact = std::clamp(impact, 0.0, 1000.0);
              i_hv.i_num_partners(RG_MSM) = impact;

              break;
          }

          //age at first sex
          case HV_IM_AGE_FIRST_SEX: {

              impact = i_hv.adj_coverage_prod(HV_IM_AGE_FIRST_SEX);
              impact = std::clamp(impact, 0.0, 1.0);
              i_hv.i_age_first_sex(S_MALE) *= impact;
              i_hv.i_age_first_sex(S_FEMALE) *= impact;

              break;
          }

          //IDU
          case HV_IM_UNSAFE_INJECT_IDU: {

              impact = i_hv.adj_coverage_prod(HV_IM_UNSAFE_INJECT_IDU);
              impact *= (i_hv.adj_coverage_prod(HV_IM_NEEDLE_SHARING_IDU));
              impact = std::clamp(impact, 0.0, 1.0);
              i_hv.i_idu_share_prop *= impact;

              //continue;
              break;
          }

          default:
              break;

      }//switch j

  } //j


}


void calc_resource_needs()
{

  const auto& c_dp = state_curr.dp;

  const auto& p_hc = pars.hc;
  auto& i_hc = intermediate.hc;

  const auto& p_hv = pars.hv;
  auto& i_hv = intermediate.hv;
  auto& n_hv = state_next.hv;

  std::list<int> RN_UsedInterventions = {RN_COMP_SEX_EDUC,RN_FSW_OUTREACH,RN_ECON_STRENGTH,
                                        RN_IDU_HARM_RED,RN_IDU_NSEP,RN_IDU_DRUG_SUB,
                                        RN_MSM_OUTREACH,RN_CONDOMS,RN_CONDOM_SUPPLY,RN_ANC_TESTING,RN_MC15_49,
                                        RN_PrEP_OralDaily,RN_PrEP_OralMonthly,RN_PrEP_OralPlusCon,RN_PrEP_Inject1Mo,
                                        RN_PrEP_Inject2Mo,RN_PrEP_Inject6Mo,RN_PrEP_Ring,
                                        RN_PrEP_bNABs,RN_PrEP_Implant,RN_PrEP_PEP,
                                        RN_HIV_TEST_ANC,RN_HIV_WOMAN_COUNS,RN_EXPOSED_INFANT_Dx,
                                        RN_ADULT_ON_ART,RN_CHILD_ON_ART,
                                        RN_CURE,RN_AHD_TX,RN_POC_CD4_INT,
                                        RN_POC_VL_INT,RN_VACCINES};


   double value=0;
   double pop_reached=0;
   double total_direct_costs=0;

   for (int i = 1; i <= RN_MAX_INTERVN; ++i)
    {
        // a few interventions are now excluded from the editors and RN calcs
        if (std::ranges::find(RN_UsedInterventions, i) == RN_UsedInterventions.end()) {
          continue;
        }

        //value = 0.0;
        pop_reached =0;

        // ------------------------------------------------------------
        switch (i)
        {
            case RN_COM_MOB:// Community mobilization
            {
              pop_reached = (i_hv.dp_totpop_1549(S_MALE)+i_hv.dp_totpop_1549(S_FEMALE))*p_hv.rn_coverage(i,t);
            }

            case RN_MASS_MEDIA:// Mass media
            {
              pop_reached = (i_hv.dp_totpop_1549(S_MALE)+i_hv.dp_totpop_1549(S_FEMALE))*p_hv.rn_coverage(i,t);
            }

            case RN_HTS:// C&T (HTS)
            {
              pop_reached = (i_hv.dp_totpop_1549(S_MALE)+i_hv.dp_totpop_1549(S_FEMALE))*p_hv.rn_coverage(i,t);
            }

            case RN_CONDOMS://condoms
            case RN_CONDOM_SUPPLY://condom supply
            {
              pop_reached *= //i_hv.dp_totpop_1549(S_MALE)*
                             (//p_hv.b_behav_properties(RG_LRH, PERC_POP) *
                              n_hv.adults(VAC_ALL,RG_LRH ,CD4_ALL,S_MALE) *
                              i_hv.b_num_partners(RG_LRH) *
                              p_hv.b_sex_acts(RG_LRH,t)+ 
                              
                              //p_hv.b_behav_properties(RG_MRH, PERC_POP) *
                              n_hv.adults(VAC_ALL,RG_MRH ,CD4_ALL,S_MALE) *
                              i_hv.b_num_partners(RG_MRH) *
                              p_hv.b_sex_acts(RG_MRH,t)+
                              
                              //p_hv.b_behav_properties(RG_HRH, PERC_POP) *
                              n_hv.adults(VAC_ALL,RG_HRH,CD4_ALL,S_MALE) *
                              i_hv.b_num_partners(RG_HRH) * 
                              p_hv.b_sex_acts(RG_HRH,t))*
                              (1+p_hv.rn_pop_sizes(RN_POP_CONDOM_WASTAGE,t)/100.0);
            }

            
            case RN_COMP_SEX_EDUC://Comprehensive sexuality education
            {
              pop_reached=0;
              for(int a = 10; a < 19; ++a)
                 pop_reached +=  (c_dp.p_totpop(a, S_MALE)*p_hv.rn_pop_sizes(RN_POP_SEC_SCHOOL_MALE,t)+
                                c_dp.p_totpop(a, S_FEMALE)*p_hv.rn_pop_sizes(RN_POP_SEC_SCHOOL_FEMALE,t));  

              pop_reached *= 0.6 * p_hv.rn_coverage(i,t);
            }

             case RN_OUT_OF_SCHOOL://Out of school youthl
            {
              pop_reached=0;
              for(int a = 10; a < 19; ++a)
                 pop_reached +=(c_dp.p_totpop(a, S_MALE)+c_dp.p_totpop(a, S_FEMALE));

              pop_reached *= 0.6 * p_hv.rn_coverage(i,t);
            }


            case RN_ECON_STRENGTH://economic strengthening
            {
              pop_reached=0;
              for(int a = 15; a < 24; ++a)
                 pop_reached +=c_dp.p_totpop(a, S_FEMALE);

              pop_reached *= p_hv.rn_coverage(i,t);
            }

            case RN_FSW_OUTREACH:// Community mobilization
            {
              pop_reached = n_hv.adults(VAC_ALL,RG_MRH ,CD4_ALL,S_FEMALE)*p_hv.rn_coverage(i,t);
            }

            case RN_MSM_OUTREACH://MSM
            case RN_MSM_LUB:
            {
              pop_reached = (n_hv.adults(VAC_ALL,RG_MSM,CD4_ALL,S_MALE)+
                             n_hv.adults(VAC_ALL,RG_MSMLR,CD4_ALL,S_MALE)+
                             n_hv.adults(VAC_ALL,RG_MSMMR,CD4_ALL,S_MALE)+
                             n_hv.adults(VAC_ALL,RG_MSMHR,CD4_ALL,S_MALE)+
                             n_hv.adults(VAC_ALL,RG_MSMIDU,CD4_ALL,S_MALE)) * p_hv.rn_coverage(i,t);
            }

            case RN_IDU_HARM_RED://IDU
            case RN_IDU_CandT:
            case RN_IDU_OUTREACH:
            {
              pop_reached = (n_hv.adults(VAC_ALL,RG_IDU,CD4_ALL,S_MALE)+
                             n_hv.adults(VAC_ALL,RG_IDU,CD4_ALL,S_FEMALE)) * p_hv.rn_coverage(i,t);
            }

            case RN_IDU_NSEP:
            {
              pop_reached = (n_hv.adults(VAC_ALL,RG_IDU,CD4_ALL,S_MALE)+
                             n_hv.adults(VAC_ALL,RG_IDU,CD4_ALL,S_FEMALE)) * 
                             p_hv.rn_pop_sizes(RN_POP_NUM_INJECT_YEAR,t)/100.0 * //CDP check /100
                             p_hv.rn_coverage(i,t);
            }

            case RN_IDU_DRUG_SUB:
            {
              pop_reached = (n_hv.adults(VAC_ALL,RG_IDU,CD4_ALL,S_MALE)+
                             n_hv.adults(VAC_ALL,RG_IDU,CD4_ALL,S_FEMALE)) *
                             p_hv.rn_pop_sizes(RN_POP_IDU_OPIOD_DEP,t)/100.0 * //CDP check /100
                             p_hv.rn_coverage(i,t);
            }


            case RN_ADULT_ON_ART://adult ART
            {
              pop_reached = i_hv.total_art_adults;
            }

            case RN_CHILD_ON_ART://children ART
            {
              pop_reached = i_hv.total_art_children;
            }

            case RN_HIV_TEST_ANC://HIV testing for all women attending ANC
            {
              pop_reached = (i_hc.need_PMTCT>0.0) ? p_hc.total_births(t) * (i_hc.on_PMTCT/i_hc.need_PMTCT) : 0.0;
            }

            case RN_HIV_WOMAN_COUNS://Counseling costs for HIV+ women
            {
              pop_reached = i_hc.on_PMTCT;
            }

            case RN_EXPOSED_INFANT_Dx://early infant diagnosis
            {
              pop_reached = i_hc.on_PMTCT;
            }

            case RN_ANC_TESTING://testing at ANC
            {
              pop_reached = p_hc.total_births(t)*p_hv.rn_coverage(i,t);
            }

            case RN_MC15_49://adult VMMC
            {
              pop_reached = calc_vmmc_percent_to_number(t);
            }

            case RN_PrEP_OralDaily://PrEP
            case RN_PrEP_OralMonthly:
            case RN_PrEP_OralPlusCon:
            case RN_PrEP_Inject1Mo:
            case RN_PrEP_Inject2Mo:
            case RN_PrEP_Inject6Mo:
            case RN_PrEP_Ring:
            case RN_PrEP_bNABs:
            case RN_PrEP_Implant:
            case RN_PrEP_PEP:
            {
              int m = i-RN_PrEP_OralDaily;
              for (int rg = RG_LRH; rg <= RG_MSMIDU; ++rg)
              {
                  pop_reached += n_hv.adults(VAC_ALL,rg,CD4_NEG,S_MALE) *
                                 p_hv.prep_method_mix(S_MALE,rg,m,t)*
                                 p_hv.rn_coverage(i,t);
              }

              for (int rg = RG_LRH; rg <= RG_IDU; ++rg)
              {
                  pop_reached += n_hv.adults(VAC_ALL,rg,CD4_NEG,S_FEMALE)*
                                 p_hv.prep_method_mix(S_FEMALE,rg,m,t)*
                                 p_hv.rn_coverage(i,t);
              }

            }

            case RN_AHD_TX://treatment advanced HIV
            {
              pop_reached = i_hv.total_pop_hivpos*p_hv.rn_adh_treat_cov(t);
            }

            case RN_POC_CD4_INT://treatment advanced HIV
            {
              pop_reached = (i_hv.total_pop_hivpos+i_hv.total_art_adults+i_hv.total_art_children) *
                             p_hv.rn_adh_treat_cov(t);
            }

            case RN_POC_VL_INT://POC testing VL
            {
              pop_reached = (i_hv.total_art_adults+i_hv.total_art_children) *
                             p_hv.rn_poc_cov(POC_VL,t);
            }

            case RN_VACCINES://new vaccines
            {
              pop_reached = i_hv.new_vaccinations_total;
            }

            case RN_CURE://HIV cure
            {
              if(p_hv.rn_cure_coverage_type==CURE_COV_ALLRISK){
                pop_reached = (i_hv.total_pop_hivpos+i_hv.total_art_adults+i_hv.total_art_children) * 
                               p_hv.rn_cure_coverage_all(t);
              }
              else{
                for (int rg = RG_LRH; rg <= RG_MSMIDU; ++rg)
                {
                    pop_reached += (n_hv.adults(VAC_ALL,rg,CD4_ALL,S_MALE)-n_hv.adults(VAC_ALL,rg,CD4_NEG,S_MALE)) *
                                   p_hv.rn_cure_coverage_rg(rg,t);
                }                  

                for (int rg = RG_LRH; rg <= RG_IDU; ++rg)
                {
                    pop_reached += (n_hv.adults(VAC_ALL,rg,CD4_ALL,S_FEMALE)-n_hv.adults(VAC_ALL,rg,CD4_NEG,S_FEMALE))*
                                  p_hv.rn_cure_coverage_rg(rg,t);
                }

              }
            }

            default:
              // No action for other interventions in this translation.
              break;
        } // switch i

             n_hv.num_people_reached(i)=pop_reached;
             n_hv.resources_required(i)=pop_reached * p_hv.rn_unit_costs(i,t);
             total_direct_costs+=n_hv.resources_required(i);


    } // for i

    double program_support_markup=0.36;
    n_hv.resources_required(RN_DIRECT_COSTS)=total_direct_costs;
    n_hv.resources_required(RN_PROGRAM_COSTS)=total_direct_costs*(1+program_support_markup);
    n_hv.resources_required(RN_TOTAL_COSTS)=n_hv.resources_required(RN_DIRECT_COSTS)+n_hv.resources_required(RN_PROGRAM_COSTS);

} // calc_resource_needs

double calc_vmmc_percent_to_number(int t)
{
   const auto& c_dp = state_curr.dp;
   const auto& p_hv = pars.hv;

    double popCurrent = 0.0;
    double popLastYear = 0.0;

    for(int a = 15; a <= 49; ++a)
    {
        popCurrent +=c_dp.p_totpop(a, S_MALE);
         if(t>1){
          popLastYear +=c_dp.p_totpop(a, S_MALE);
         }
    }

    double vmmcTarget = popCurrent * p_hv.rn_coverage(RN_MC15_49,t);

    int calcYearIdx = 1;
    double vmmcTraditional = c_dp.p_totpop(15, S_MALE) * p_hv.rn_coverage(RN_MC15_49,calcYearIdx);

    double vmmcLastYear = 0.0;
    if(t>1)
    {
        double popExcludingUnder15 = popLastYear -c_dp.p_totpop(15, S_MALE);
        vmmcLastYear = popExcludingUnder15 * p_hv.rn_coverage(RN_MC15_49,t-1);
    }

    double result = vmmcTarget - vmmcLastYear - vmmcTraditional;

    //Ensure we never return a negative number.
    result = std::max(result, 0.0);

    return result;
}


};


} // namespace internal
} // namespace leapfrog
