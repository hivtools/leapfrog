#pragma once

#include "../options.hpp"
#include "../generated/config_mixer.hpp"

namespace leapfrog {
namespace internal {

template<typename Config>
concept HivDemographicProjectionEnabled = RunDemographicProjection<Config> && RunHivSimulation<Config>;

template<typename Config>
concept HivDpChildEnabled = HivDemographicProjectionEnabled<Config> && RunChildModel<Config>;

// ─── Shared implementation base ──────────────────────────────────────────────
// Holds all data members, the constructor, and the method implementations that
// are identical between the HIV-only and HIV+child model levels.

template<HivDemographicProjectionEnabled Config>
struct HivDpImplBase {
  using real_type = typename Config::real_type;
  using ModelVariant = typename Config::ModelVariant;
  using SS = Config::SS;
  using Pars = Config::Pars;
  using State = Config::State;
  using Intermediate = Config::Intermediate;
  using Args = Config::Args;

protected:
  static constexpr int NS = SS::NS;
  static constexpr int pAG = SS::pAG;
  static constexpr int hDS = SS::hDS;
  static constexpr int hTS = SS::hTS;
  static constexpr int hAG = SS::hAG;
  static constexpr auto hAG_span = SS::hAG_span;
  static constexpr int PROJPERIOD_MIDYEAR = SS::PROJPERIOD_MIDYEAR;
  static constexpr int p_idx_hiv_first_adult = SS::p_idx_hiv_first_adult;

  int t;
  const Pars& pars;
  const State& state_curr;
  State& state_next;
  Intermediate& intermediate;
  const Options<real_type>& opts;

public:
  HivDpImplBase(Args& args) :
    t(args.t),
    pars(args.pars),
    state_curr(args.state_curr),
    state_next(args.state_next),
    intermediate(args.intermediate),
    opts(args.opts)
  {}

  void run_hivpop_end_year_migration() {
    auto& n_ha = state_next.ha;
    auto& i_dp = intermediate.dp;

    for (int s = 0; s < NS; ++s) {
      for (int a = 0; a < pAG; ++a) {
        n_ha.p_net_migration_hivpop(a, s) = n_ha.p_hivpop(a, s) * i_dp.migration_rate(a, s);
        n_ha.p_hivpop(a, s) += n_ha.p_net_migration_hivpop(a, s);
      }
    }

    for (int s = 0; s < NS; ++s) {
      int a = p_idx_hiv_first_adult;
      for (int ha = 0; ha < hAG; ++ha) {
        real_type migration_num_ha = 0.0;
        real_type hivpop_ha_postmig = 0.0;
        for (int i = 0; i < hAG_span[ha]; ++i, ++a) {
          hivpop_ha_postmig += n_ha.p_hivpop(a, s);
          migration_num_ha += n_ha.p_net_migration_hivpop(a, s);
        }

        real_type migration_rate = 0.0;
        if (hivpop_ha_postmig > 0.0) {
          migration_rate = migration_num_ha / (hivpop_ha_postmig - migration_num_ha);
        }

        for (int hm = 0; hm < hDS; ++hm) {
          n_ha.h_hivpop(hm, ha, s) *= 1.0 + migration_rate;
          if (t >= opts.ts_art_start) {
            for (int hu = 0; hu < hTS; ++hu) {
              n_ha.h_artpop(hu, hm, ha, s) *= 1.0 + migration_rate;
            }
          }
        }
      }
    }
  }

protected:
  void run_hiv_ageing_and_mortality_impl() {
    const auto& p_dp = pars.dp;
    const auto& c_ha = state_curr.ha;
    auto& n_ha = state_next.ha;

    for (int s = 0; s < NS; ++s) {
      for (int a = 1; a < pAG; ++a) {
        const real_type surv = p_dp.survival_probability(a, s, t);
        n_ha.p_deaths_background_hivpop(a, s) = c_ha.p_hivpop(a - 1, s) * (1.0 - pwid_adjusted_surv(surv, a, s));
        n_ha.p_hivpop(a, s) = c_ha.p_hivpop(a - 1, s);
      }

      n_ha.p_deaths_background_hivpop(pAG - 1, s) +=
        c_ha.p_hivpop(pAG - 1, s) * (1 - p_dp.survival_probability(pAG, s, t));
      n_ha.p_hivpop(pAG - 1, s) += c_ha.p_hivpop(pAG - 1, s);
    }
  }

  // The ageing implementation without the child entrant addition.
  // Level 3 calls add_child_entrants_to_adult_hiv() after this.
  void run_hiv_and_art_stratified_ageing_impl() {
    const auto& c_ha = state_curr.ha;
    auto& n_ha = state_next.ha;
    auto& i_ha = intermediate.ha;

    for (int s = 0; s < NS; ++s) {
      int a = p_idx_hiv_first_adult;
      for (int ha = 0; ha < (hAG - 1); ++ha) {
        for (int i = 0; i < hAG_span[ha]; ++i, ++a) {
          i_ha.hiv_age_up_prob(ha, s) += c_ha.p_hivpop(a, s);
        }

        if (i_ha.hiv_age_up_prob(ha, s) > 0) {
          i_ha.hiv_age_up_prob(ha, s) = c_ha.p_hivpop(a - 1, s) / i_ha.hiv_age_up_prob(ha, s);
        } else {
          i_ha.hiv_age_up_prob(ha, s) = 0.0;
        }
      }
    }

    for (int s = 0; s < NS; ++s) {
      for (int ha = 1; ha < hAG; ++ha) {
        for (int hm = 0; hm < hDS; ++hm) {
          n_ha.h_hivpop(hm, ha, s) = (1.0 - i_ha.hiv_age_up_prob(ha, s)) * c_ha.h_hivpop(hm, ha, s);
          n_ha.h_hivpop(hm, ha, s) += i_ha.hiv_age_up_prob(ha - 1, s) * c_ha.h_hivpop(hm, ha - 1, s);

          if (t > opts.ts_art_start) {
            for (int hu = 0; hu < hTS; ++hu) {
              n_ha.h_artpop(hu, hm, ha, s) = (1.0 - i_ha.hiv_age_up_prob(ha, s)) * c_ha.h_artpop(hu, hm, ha, s);
              n_ha.h_artpop(hu, hm, ha, s) += i_ha.hiv_age_up_prob(ha - 1, s) * c_ha.h_artpop(hu, hm, ha - 1, s);
            }
          }
        }
      }

      int ha = 0;
      for (int hm = 0; hm < hDS; ++hm) {
        n_ha.h_hivpop(hm, ha, s) = (1.0 - i_ha.hiv_age_up_prob(ha, s)) * c_ha.h_hivpop(hm, ha, s);
        if (t > opts.ts_art_start) {
          for (int hu = 0; hu < hTS; ++hu) {
            n_ha.h_artpop(hu, hm, ha, s) = (1.0 - i_ha.hiv_age_up_prob(ha, s)) * c_ha.h_artpop(hu, hm, ha, s);
          }
        }
      }
    }
    // TODO: implement static entrants to adult HIV population for case when child model not simulated
  }

  void run_hiv_and_art_stratified_deaths_and_migration_impl() {
    auto& n_ha = state_next.ha;
    auto& i_ha = intermediate.ha;
    auto& i_dp = intermediate.dp;

    for (int s = 0; s < NS; ++s) {
      int a = p_idx_hiv_first_adult;
      for (int ha = 0; ha < hAG; ++ha) {
        for (int i = 0; i < hAG_span[ha]; ++i, ++a) {
          i_ha.p_coarse_ages_hivpop(ha, s) += n_ha.p_hivpop(a, s);
        }
      }
    }

    for (int s = 0; s < NS; ++s) {
      for (int a = 1; a < pAG; ++a) {
        n_ha.p_hivpop(a, s) -= n_ha.p_deaths_background_hivpop(a, s);
        if (opts.proj_period_int == PROJPERIOD_MIDYEAR) {
          n_ha.p_net_migration_hivpop(a, s) = n_ha.p_hivpop(a, s) * i_dp.migration_rate(a, s);
          n_ha.p_hivpop(a, s) += n_ha.p_net_migration_hivpop(a, s);
        }
      }
    }

    for (int s = 0; s < NS; ++s) {
      int a = p_idx_hiv_first_adult;
      for (int ha = 0; ha < hAG; ++ha) {
        real_type deaths_migrate = 0.0;
        for (int i = 0; i < hAG_span[ha]; ++i, ++a) {
          deaths_migrate -= n_ha.p_deaths_background_hivpop(a, s);
          if (opts.proj_period_int == PROJPERIOD_MIDYEAR) {
            deaths_migrate += n_ha.p_net_migration_hivpop(a, s);
          }
        }

        real_type deaths_migrate_rate = 0.0;
        if (i_ha.p_coarse_ages_hivpop(ha, s) > 0) {
          deaths_migrate_rate = deaths_migrate / i_ha.p_coarse_ages_hivpop(ha, s);
        }

        for (int hm = 0; hm < hDS; ++hm) {
          n_ha.h_hivpop(hm, ha, s) *= 1.0 + deaths_migrate_rate;
          if (t > opts.ts_art_start) {
            for (int hu = 0; hu < hTS; ++hu) {
              n_ha.h_artpop(hu, hm, ha, s) *= 1.0 + deaths_migrate_rate;
            }
          }
        }
      }
    }
  }

private:
  // Returns survival probability for HIV+ people at age a, adjusted down for PWID excess
  // mortality. Only applies to working ages 15-49; returns surv unchanged outside that range.
  real_type pwid_adjusted_surv(real_type surv, int a, int s) {
    const bool no_adjustment = pars.ha.incidence_model_choice == SS::INCIDMOD_DIRECTINCID_HTS ||
      a < p_idx_hiv_first_adult || a >= 50 ||
      pars.ha.pwid_sex_ratio(t) < 0.0;

    if (no_adjustment) return surv;

    const real_type sex_ratio = pars.ha.pwid_sex_ratio(t);
    const real_type pop_s     = state_curr.dp.p_totpop(a - 1, s);
    const real_type total_pop = state_curr.dp.p_totpop(a - 1, SS::MALE) + state_curr.dp.p_totpop(a - 1, SS::FEMALE);
    if (total_pop <= 0.0 || pop_s <= 0.0) return surv;

    const real_type ratio = (s == SS::MALE)
      ? 1.0 / (1.0 + sex_ratio)
      : sex_ratio / (1.0 + sex_ratio);
    const real_type background_mort = 1.0 - surv;
    const real_type raw_excess = pars.ha.pwid_hivpos_nonaids_mortality - background_mort;
    const real_type excess = (raw_excess > 0.0 ? raw_excess : 0.0)
      * pars.ha.pwid_prop_hivpop(t) * ratio / (pop_s / total_pop);
    return 1.0 - (background_mort + excess);
  }
};


// ─── Level 1: base no-op ─────────────────────────────────────────────────────
// Selected when run_hiv_simulation = false. All public methods are no-ops.

template<typename Config>
struct HivDemographicProjection {
  HivDemographicProjection(...) {}
  void run_hivpop_demographic_projection() {}
  void run_virginpop_demographic_projection() {}
  void run_hivpop_end_year_migration() {}
  void run_hc_hivpop_end_year_migration() {}
};


// ─── Level 2: HIV simulation on, child model off ─────────────────────────────
// Selected when run_hiv_simulation = true and run_child_model = false.
// Child and virgin methods are no-ops here.

template<HivDemographicProjectionEnabled Config>
struct HivDemographicProjection<Config> : HivDpImplBase<Config> {
  using HivDpImplBase<Config>::HivDpImplBase;
  using HivDpImplBase<Config>::run_hivpop_end_year_migration;

  void run_hivpop_demographic_projection() {
    this->run_hiv_ageing_and_mortality_impl();
    this->run_hiv_and_art_stratified_ageing_impl();
    this->run_hiv_and_art_stratified_deaths_and_migration_impl();
  }

  void run_virginpop_demographic_projection() {}
  void run_hc_hivpop_end_year_migration() {}
};


// ─── Level 3: HIV simulation + child model on ────────────────────────────────
// Selected when run_child_model = true (more constrained, subsumes Level 2).
// All methods have real implementations. Virgin is handled by if constexpr
// inside run_virginpop_demographic_projection since it always co-occurs with child.

template<HivDpChildEnabled Config>
struct HivDemographicProjection<Config> : HivDpImplBase<Config> {
  using HivDpImplBase<Config>::HivDpImplBase;
  using HivDpImplBase<Config>::run_hivpop_end_year_migration;

  // Re-declare from Config: inherited names from template base classes require
  // explicit qualification or re-declaration for unqualified lookup in method bodies.
private:
  using real_type = typename Config::real_type;
  using ModelVariant = typename Config::ModelVariant;
  using SS = Config::SS;
  static constexpr int NS = SS::NS;
  static constexpr int hDS = SS::hDS;
  static constexpr int hTS = SS::hTS;
  static constexpr int PROJPERIOD_MIDYEAR = SS::PROJPERIOD_MIDYEAR;

public:

  void run_hivpop_demographic_projection() {
    this->run_hiv_ageing_and_mortality_impl();
    run_age_15_entrants();
    this->run_hiv_and_art_stratified_ageing_impl();
    add_child_entrants_to_adult_hiv();
    this->run_hiv_and_art_stratified_deaths_and_migration_impl();
    run_hc_hiv_and_art_stratified_deaths_and_migration();
  }

  void run_virginpop_demographic_projection() {
    if constexpr (ModelVariant::run_virgin) {
      const auto& p_dp = this->pars.dp;
      const auto& c_dp = this->state_curr.dp;
      const auto& i_dp = this->intermediate.dp;
      const auto& c_ha = this->state_curr.ha;
      const auto& c_vg = this->state_curr.vg;
      const auto& i_hc = this->intermediate.hc;
      const auto& p_hc = this->pars.hc;
      const auto& p_vg = this->pars.vg;
      auto& n_vg = this->state_next.vg;

      for (int s = 0; s < NS; ++s) {

        for (int va = 1; va < SS::vAG; ++va) {
          int a = va + SS::p_idx_virginpop_first;
          n_vg.p_totpop_virgin(va, s) = c_vg.p_totpop_virgin(va - 1, s) * p_dp.survival_probability(a, s, this->t);
          n_vg.p_hivpop_virgin(va, s) = c_vg.p_hivpop_virgin(va - 1, s) * p_dp.survival_probability(a, s, this->t);

          for (int hm = 0; hm < hDS; ++hm) {
            n_vg.h_hivpop_virgin(hm, va, s) += c_vg.h_hivpop_virgin(hm, va - 1, s) * p_dp.survival_probability(a, s, this->t);

            if (this->t > this->opts.ts_art_start) {
              for (int hu = 0; hu < hTS; ++hu) {
                n_vg.h_artpop_virgin(hu, hm, va, s) += c_vg.h_artpop_virgin(hu, hm, va - 1, s) * p_dp.survival_probability(a, s, this->t);
              }
            }
          }

          if (this->opts.proj_period_int == PROJPERIOD_MIDYEAR) {
            n_vg.p_totpop_virgin(va, s) *= 1.0 + i_dp.migration_rate(a, s);
            n_vg.p_hivpop_virgin(va, s) *= 1.0 + i_dp.migration_rate(a, s);

            for (int hm = 0; hm < hDS; ++hm) {
              n_vg.h_hivpop_virgin(hm, va, s) *= 1.0 + i_dp.migration_rate(a, s);

              if (this->t > this->opts.ts_art_start) {
                for (int hu = 0; hu < hTS; ++hu) {
                  n_vg.h_artpop_virgin(hu, hm, va, s) *= 1.0 + i_dp.migration_rate(a, s);
                }
              }
            }
          }
        }

        const int va0 = 0;
        const int a0 = SS::p_idx_virginpop_first;
        n_vg.p_totpop_virgin(va0, s) = c_dp.p_totpop(a0 - 1, s) * p_dp.survival_probability(a0, s, this->t);
        n_vg.p_hivpop_virgin(va0, s) = c_ha.p_hivpop(a0 - 1, s) * p_dp.survival_probability(a0, s, this->t);

        for (int hm = 0; hm < hDS; ++hm) {
          n_vg.h_hivpop_virgin(hm, va0, s) += i_hc.age15_hivpop(hm, s) * p_dp.survival_probability(a0, s, this->t);

          if (this->t > p_hc.hc_art_start) {
            for (int hu = 0; hu < hTS; ++hu) {
              if (this->t > this->opts.ts_art_start) {
                n_vg.h_artpop_virgin(hu, hm, va0, s) += i_hc.age15_artpop(hu, hm, s) * p_dp.survival_probability(a0, s, this->t);
              } else {
                n_vg.h_hivpop_virgin(hm, va0, s) += i_hc.age15_artpop(hu, hm, s) * p_dp.survival_probability(a0, s, this->t);
              }
            }
          }
        }

        if (this->opts.proj_period_int == PROJPERIOD_MIDYEAR) {
          n_vg.p_totpop_virgin(va0, s) *= 1.0 + i_dp.migration_rate(a0, s);
          n_vg.p_hivpop_virgin(va0, s) *= 1.0 + i_dp.migration_rate(a0, s);

          for (int hm = 0; hm < hDS; ++hm) {
            n_vg.h_hivpop_virgin(hm, va0, s) *= 1.0 + i_dp.migration_rate(a0, s);
            if (this->t > this->opts.ts_art_start) {
              for (int hu = 0; hu < hTS; ++hu) {
                n_vg.h_artpop_virgin(hu, hm, va0, s) *= 1.0 + i_dp.migration_rate(a0, s);
              }
            }
          }
        }

        for (int va = 0; va < SS::vAG; ++va) {
          n_vg.p_totpop_virgin(va, s) *= 1.0 - p_vg.sexdebut_annual_prob(va, s, this->t);
          n_vg.p_hivpop_virgin(va, s) *= 1.0 - p_vg.sexdebut_annual_prob(va, s, this->t);

          for (int hm = 0; hm < hDS; ++hm) {
            n_vg.h_hivpop_virgin(hm, va, s) *= 1.0 - p_vg.sexdebut_annual_prob(va, s, this->t);

            if (this->t > this->opts.ts_art_start) {
              for (int hu = 0; hu < hTS; ++hu) {
                n_vg.h_artpop_virgin(hu, hm, va, s) *= 1.0 - p_vg.sexdebut_annual_prob(va, s, this->t);
              }
            }
          }
        }
      }
    }
  }

  void run_hc_hivpop_end_year_migration() {
    static constexpr int hc2_agestart = SS::hc2_agestart;
    static constexpr int hcAG_end = SS::hcAG_end;
    static constexpr int hc1DS = SS::hc1DS;
    static constexpr int hc2DS = SS::hc2DS;
    static constexpr int hcTT = SS::hcTT;

    auto& n_ha = this->state_next.ha;
    auto& n_hc = this->state_next.hc;
    const auto& p_hc = this->pars.hc;

    for (int s = 0; s < NS; ++s) {
      for (int a = 0; a < hcAG_end; ++a) {
        real_type hc_migration_num = 0.0;
        real_type hc_hivpop_postmig = n_ha.p_hivpop(a, s);
        hc_migration_num = n_ha.p_net_migration_hivpop(a, s);

        real_type migration_rate = 0.0;
        if (hc_hivpop_postmig > 0.0) {
          migration_rate = hc_migration_num / (hc_hivpop_postmig - hc_migration_num);
        }

        if (a < hc2_agestart) {
          for (int cat = 0; cat < hcTT; ++cat) {
            for (int hd = 0; hd < hc1DS; ++hd) {
              n_hc.hc1_hivpop(hd, cat, a, s) *= 1.0 + migration_rate;
            }
          }
          if (this->t >= p_hc.hc_art_start) {
            for (int hd = 0; hd < hc1DS; ++hd) {
              for (int dur = 0; dur < hTS; ++dur) {
                n_hc.hc1_artpop(dur, hd, a, s) *= 1.0 + migration_rate;
              }
            }
          }
        } else {
          for (int hd = 0; hd < hc2DS; ++hd) {
            for (int cat = 0; cat < hcTT; ++cat) {
              n_hc.hc2_hivpop(hd, cat, a - hc2_agestart, s) *= 1.0 + migration_rate;
            }
            if (this->t >= p_hc.hc_art_start) {
              for (int dur = 0; dur < hTS; ++dur) {
                n_hc.hc2_artpop(dur, hd, a - hc2_agestart, s) *= 1.0 + migration_rate;
              }
            }
          }
        }
      }
    }
  }

private:
  void run_age_15_entrants() {
    constexpr int hcTT = SS::hcTT;
    constexpr int hc2AG = SS::hc2AG;
    constexpr int hc2DS = SS::hc2DS;

    const auto& p_hc = this->pars.hc;
    const auto& c_hc = this->state_curr.hc;
    auto& i_hc = this->intermediate.hc;

    for (int s = 0; s < NS; ++s) {
      for (int hm = 0; hm < hDS; ++hm) {
        i_hc.age15_hivpop(hm, s) = 0.0;
        for (int hm_adol = 0; hm_adol < hc2DS; ++hm_adol) {
          auto age15_hivpop_hm_adol = 0.0;
          for (int htm = 0; htm < hcTT; ++htm) {
            age15_hivpop_hm_adol += c_hc.hc2_hivpop(hm_adol, htm, (hc2AG - 1), s);
          }
          i_hc.age15_hivpop(hm, s) += age15_hivpop_hm_adol * SS::hc2_to_ha_cd4_transition[hm][hm_adol];
        }

        if (this->t > p_hc.hc_art_start) {
          for (int hu = 0; hu < hTS; ++hu) {
            i_hc.age15_artpop(hu, hm, s) = 0.0;
            for (int hm_adol = 0; hm_adol < hc2DS; ++hm_adol) {
              i_hc.age15_artpop(hu, hm, s) += c_hc.hc2_artpop(hu, hm_adol, (hc2AG - 1), s) * SS::hc2_to_ha_cd4_transition[hm][hm_adol];
            }
          }
        }
      }
    }
  }

  // Adds the age-15 child entrants (computed by run_age_15_entrants) into the
  // ha = 0 adult HIV/ART arrays. Called after run_hiv_and_art_stratified_ageing_impl.
  void add_child_entrants_to_adult_hiv() {
    auto& n_ha = this->state_next.ha;
    const auto& i_hc = this->intermediate.hc;
    const auto& p_hc = this->pars.hc;

    for (int s = 0; s < NS; ++s) {
      for (int hm = 0; hm < hDS; ++hm) {
        n_ha.h_hivpop(hm, 0, s) += i_hc.age15_hivpop(hm, s);

        if (this->t > p_hc.hc_art_start) {
          for (int hu = 0; hu < hTS; ++hu) {
            if (this->t > this->opts.ts_art_start) {
              n_ha.h_artpop(hu, hm, 0, s) += i_hc.age15_artpop(hu, hm, s);
            } else {
              // child ART started but adult ART has not: put into untreated adult HIV population
              n_ha.h_hivpop(hm, 0, s) += i_hc.age15_artpop(hu, hm, s);
            }
          }
        }
      }
    }
  }

  void run_hc_hiv_and_art_stratified_deaths_and_migration() {
    static constexpr int hc2_agestart = SS::hc2_agestart;
    static constexpr int hcAG_end = SS::hcAG_end;
    static constexpr int hc1DS = SS::hc1DS;
    static constexpr int hc2DS = SS::hc2DS;
    static constexpr int hcTT = SS::hcTT;

    auto& n_ha = this->state_next.ha;
    auto& n_hc = this->state_next.hc;
    const auto& p_hc = this->pars.hc;

    for (int s = 0; s < NS; ++s) {
      for (int a = 0; a < hcAG_end; ++a) {
        real_type deaths_migrate = 0.0;
        deaths_migrate -= n_ha.p_deaths_background_hivpop(a, s);
        if (this->opts.proj_period_int == PROJPERIOD_MIDYEAR) {
          deaths_migrate += n_ha.p_net_migration_hivpop(a, s);
        }
        if (n_ha.p_hivpop(a, s) > 0) {
          deaths_migrate /= n_ha.p_hivpop(a, s);
        }
        if (a < hc2_agestart) {
          for (int cat = 0; cat < hcTT; ++cat) {
            for (int hd = 0; hd < hc1DS; ++hd) {
              n_hc.hc1_hivpop(hd, cat, a, s) *= 1.0 + deaths_migrate;
            }
          }
          if (this->t > p_hc.hc_art_start) {
            for (int hd = 0; hd < hc1DS; ++hd) {
              for (int dur = 0; dur < hTS; ++dur) {
                n_hc.hc1_artpop(dur, hd, a, s) *= 1.0 + deaths_migrate;
              }
            }
          }
        } else {
          for (int hd = 0; hd < hc2DS; ++hd) {
            for (int cat = 0; cat < hcTT; ++cat) {
              n_hc.hc2_hivpop(hd, cat, a - hc2_agestart, s) *= 1.0 + deaths_migrate;
            }
            if (this->t > p_hc.hc_art_start) {
              for (int dur = 0; dur < hTS; ++dur) {
                n_hc.hc2_artpop(dur, hd, a - hc2_agestart, s) *= 1.0 + deaths_migrate;
              }
            }
          }
        }
      }
    }
  }
};

}
}
