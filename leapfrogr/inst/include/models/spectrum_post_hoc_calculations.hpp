#pragma once

#include "../options.hpp"
#include "../generated/config_mixer.hpp"

namespace leapfrog {
namespace internal {

template<typename Config>
concept SpectrumPostHocCalculationsEnabled = RunDemographicProjection<Config> && RunHivSimulation<Config> && RunChildModel<Config> && RunSpectrumModel<Config>;

template<typename Config>
struct SpectrumPostHocCalculations {
  SpectrumPostHocCalculations(...) {};
};

template<SpectrumPostHocCalculationsEnabled Config>
struct SpectrumPostHocCalculations<Config> {
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
  static constexpr int pAG_5yr = SS::pAG_5yr;
  static constexpr int p_idx_hiv_first_adult = SS::p_idx_hiv_first_adult;
  static constexpr int hc1DS = SS::hc1DS;
  static constexpr int hc1AG = SS::hc1AG;
  static constexpr int hc2DS = SS::hc2DS;
  static constexpr int hc2AG = SS::hc2AG;
  static constexpr int hcTT = SS::hcTT;
  static constexpr int hc2_agestart = SS::hc2_agestart;

  // function args
  int t;
  const Pars& pars;
  const State& state_curr;
  State& state_next;
  Intermediate& intermediate;
  const Options<real_type>& opts;

  // only exposing the constructor and some methods
  public:
  SpectrumPostHocCalculations(Args& args):
    t(args.t),
    pars(args.pars),
    state_curr(args.state_curr),
    state_next(args.state_next),
    intermediate(args.intermediate),
    opts(args.opts)
  {};

  void run_spectrum_post_hoc_calulations() {
    calculate_nonaids_deaths();
    calculate_nonaids_excess_deaths();
    calculate_infections_5yr();
    calculate_hiv_deaths_5yr();
    calculate_deaths_5yr();
    calculate_median_cd4_init();
    calculate_plhiv_5yr();
    calculate_art_5yr();
  };

  // private methods that we don't want people to call
  private:
  void calculate_nonaids_deaths() {
    auto& n_ha = state_next.ha;
    auto& n_sp = state_next.sp;
    auto& i_sp = intermediate.sp;

    for (int s = 0; s < NS; ++s) {

      // Spectrum stores nonaids deaths by age but for children is always 0.
      // Only write values for a >= p_idx_hiv_first_adult
      // so that it is always 0 for children to match Spectrum.

      int a = p_idx_hiv_first_adult;
      for (int ha = 0; ha < hAG; ++ha) {
        i_sp.hiv_art_adult_sa = 0.0;
        i_sp.hiv_untreated_adult_sa = 0.0;

        for (int hm = 0; hm < hDS; ++hm) {
          i_sp.hiv_untreated_adult_sa += n_ha.h_hivpop(hm, ha, s);
          for (int hu = 0; hu < hTS; ++hu) {
            i_sp.hiv_art_adult_sa += n_ha.h_artpop(hu, hm, ha, s);
          }
        }

        if (i_sp.hiv_art_adult_sa + i_sp.hiv_untreated_adult_sa > 0) {
          i_sp.artcov_adult_sa = i_sp.hiv_art_adult_sa / (i_sp.hiv_art_adult_sa + i_sp.hiv_untreated_adult_sa);
        } else {
          i_sp.artcov_adult_sa = 0.0;
        }

        for (int i = 0; i < hAG_span[ha]; ++i, ++a) {
          n_sp.p_deaths_nonaids_artpop(a, s) = n_ha.p_deaths_background_hivpop(a, s) * i_sp.artcov_adult_sa;
          n_sp.p_deaths_nonaids_hivpop(a, s) = n_ha.p_deaths_background_hivpop(a, s) * (1.0 - i_sp.artcov_adult_sa);
        }
      }
    }
  };

  void calculate_nonaids_excess_deaths() {
    auto& n_ha = state_next.ha;
    auto& n_sp = state_next.sp;

    for (int s = 0; s < NS; ++s) {

      // Spectrum stores nonaids-excess deaths by age but for children
      // is always 0. Only write values for a >= p_idx_hiv_first_adult
      // so that it is always 0 for children to match Spectrum.

      int a = p_idx_hiv_first_adult;
      for (int ha = 0; ha < hAG; ++ha) {

        // Aggregate excess deaths and population in coarse age group
        auto excess_deaths_nonaids_no_art_ha = 0.0;
        auto excess_deaths_nonaids_on_art_ha = 0.0;
        auto hivpop_ha = 0.0;

        for (int hm = 0; hm < hDS; ++hm) {
          excess_deaths_nonaids_no_art_ha += n_ha.h_deaths_excess_nonaids_no_art(hm, ha, s);
          hivpop_ha += n_ha.h_hivpop(hm, ha, s);

          if (t > opts.ts_art_start) {
            for (int hu = 0; hu < hTS; ++hu) {
              excess_deaths_nonaids_on_art_ha += n_ha.h_deaths_excess_nonaids_on_art(hu, hm, ha, s);
              hivpop_ha += n_ha.h_artpop(hu, hm, ha, s);
            }
          }
        }


	      // Distribute deaths from coarse age group ha to single age group a proportional
	      // to distribution of HIV population in age group a
        for (int i = 0; i < hAG_span[ha]; ++i, ++a) {

          if (hivpop_ha > 0) {
            const auto hivpop_proportion_a = n_ha.p_hivpop(a, s) / hivpop_ha;
            n_sp.p_excess_deaths_nonaids_no_art(a, s) = excess_deaths_nonaids_no_art_ha * hivpop_proportion_a;

            if (t > opts.ts_art_start) {
              n_sp.p_excess_deaths_nonaids_on_art(a, s) += excess_deaths_nonaids_on_art_ha *  hivpop_proportion_a;
            }
          } else {
            n_sp.p_excess_deaths_nonaids_no_art(a, s) = 0.0;
            n_sp.p_excess_deaths_nonaids_on_art(a, s) = 0.0;
          }
        }
      }
    }
  }

  // Aggregate new HIV infections from single ages to 5-year age groups.
  // p_infections includes both adult (horizontal) and child (vertical) infections
  // since the child model writes age-0 MTCT infections into n_ha.p_infections.
  void calculate_infections_5yr() {
    auto& n_ha = state_next.ha;
    auto& n_sp = state_next.sp;

    for (int s = 0; s < NS; ++s) {
      for (int a = 0; a < pAG; ++a) {
        n_sp.p5_infections(a / 5, s) += n_ha.p_infections(a, s);
      }
    }
  }

  // Aggregate HIV (AIDS) deaths from single ages to 5-year age groups.
  // p_hiv_deaths includes both adult deaths (from the adult model) and
  // child deaths (added by the child model via fill_total_pop_outputs).
  void calculate_hiv_deaths_5yr() {
    auto& n_ha = state_next.ha;
    auto& n_sp = state_next.sp;

    for (int s = 0; s < NS; ++s) {
      for (int a = 0; a < pAG; ++a) {
        n_sp.p5_hiv_deaths(a / 5, s) += n_ha.p_hiv_deaths(a, s);
      }
    }
  }

  // Aggregate background (non-AIDS) deaths from single ages to 5-year age groups.
  void calculate_deaths_5yr() {
    auto& n_dp = state_next.dp;
    auto& n_sp = state_next.sp;

    for (int s = 0; s < NS; ++s) {
      for (int a = 0; a < pAG; ++a) {
        n_sp.p5_deaths(a / 5, s) += n_dp.p_deaths_background_totpop(a, s);
      }
    }
  }

  // Compute the median CD4 count at ART initiation from h_art_initiation.
  // The 7 CD4 categories (hDS=7), from highest to lowest CD4:
  //   hm=0: >500, hm=1: 350-500, hm=2: 250-349, hm=3: 200-249,
  //   hm=4: 100-199, hm=5: 50-99, hm=6: <50
  void calculate_median_cd4_init() {
    auto& n_ha = state_next.ha;
    auto& n_sp = state_next.sp;

    // Lower bounds of each CD4 category (index 0 = highest CD4).
    // The "upper bound" of hm is the lower bound of hm-1.
    // For hm=0 (>500) we use 1000 as a notional upper bound.
    constexpr real_type cd4_lower[hDS] = {500, 350, 250, 200, 100, 50, 0};
    constexpr real_type cd4_upper_gt500 = 1000;

    real_type total_by_cd4[hDS] = {};
    for (int s = 0; s < NS; ++s) {
      for (int ha = 0; ha < hAG; ++ha) {
        for (int hm = 0; hm < hDS; ++hm) {
          total_by_cd4[hm] += n_ha.h_art_initiation(hm, ha, s);
        }
      }
    }

    real_type total = 0.0;
    for (int hm = 0; hm < hDS; ++hm) {
      total += total_by_cd4[hm];
    }

    if (total <= 0.0) {
      n_sp.median_cd4_init = 0.0;
      return;
    }

    real_type prop[hDS] = {};
    for (int hm = 0; hm < hDS; ++hm) {
      prop[hm] = total_by_cd4[hm] / total;
    }

    // Iterate from lowest CD4 (hm = hDS-1) upward, accumulating proportions
    // until we exceed 0.5 (matching the Spectrum CalcMedianCd4 logic).
    real_type cumulative = 0.0;
    int median_hm = 0;
    for (int hm = hDS - 1; hm >= 0; --hm) {
      cumulative += prop[hm];
      if (cumulative >= 0.5) {
        median_hm = hm;
        break;
      }
    }
    // Back out the last addition to get cumulative before the median category.
    cumulative -= prop[median_hm];

    if (prop[median_hm] > 0.0) {
      real_type lower = cd4_lower[median_hm];
      real_type upper = (median_hm > 0) ? cd4_lower[median_hm - 1] : cd4_upper_gt500;
      n_sp.median_cd4_init = lower + (upper - lower) * (0.5 - cumulative) / prop[median_hm];
    } else {
      n_sp.median_cd4_init = 0.0;
    }
  }

  // Compute PLHIV (HIV-positive population) by 5-year age group.
  // For adults (ages 15+): p_hivpop already tracks total PLHIV including those on ART.
  // For children (ages 0-4): sum hc1_hivpop + hc1_artpop over all CD4/transmission categories.
  // For children (ages 5-14): sum hc2_hivpop + hc2_artpop over all CD4/transmission categories.
  void calculate_plhiv_5yr() {
    auto& n_ha = state_next.ha;
    auto& n_hc = state_next.hc;
    auto& n_sp = state_next.sp;

    // Adults
    for (int s = 0; s < NS; ++s) {
      for (int a = p_idx_hiv_first_adult; a < pAG; ++a) {
        n_sp.p5_plhiv(a / 5, s) += n_ha.p_hivpop(a, s);
      }
    }

    // Children ages 0-4 (hc1 model)
    for (int s = 0; s < NS; ++s) {
      for (int a = 0; a < hc2_agestart; ++a) {
        for (int hd = 0; hd < hc1DS; ++hd) {
          for (int cat = 0; cat < hcTT; ++cat) {
            n_sp.p5_plhiv(a / 5, s) += n_hc.hc1_hivpop(hd, cat, a, s);
          }
          for (int dur = 0; dur < hTS; ++dur) {
            n_sp.p5_plhiv(a / 5, s) += n_hc.hc1_artpop(dur, hd, a, s);
          }
        }
      }
    }

    // Children ages 5-14 (hc2 model)
    for (int s = 0; s < NS; ++s) {
      for (int a = hc2_agestart; a < p_idx_hiv_first_adult; ++a) {
        for (int hd = 0; hd < hc2DS; ++hd) {
          for (int cat = 0; cat < hcTT; ++cat) {
            n_sp.p5_plhiv(a / 5, s) += n_hc.hc2_hivpop(hd, cat, a - hc2_agestart, s);
          }
          for (int dur = 0; dur < hTS; ++dur) {
            n_sp.p5_plhiv(a / 5, s) += n_hc.hc2_artpop(dur, hd, a - hc2_agestart, s);
          }
        }
      }
    }
  }

  // Compute number on ART by 5-year age group.
  // For adults (ages 15+): sum h_artpop over treatment stages and CD4 categories.
  //   hAG_span is all 1s in the Spectrum model variant, so ha = a - p_idx_hiv_first_adult.
  // For children (ages 0-4): sum hc1_artpop over all treatment stages and CD4 categories.
  // For children (ages 5-14): sum hc2_artpop over all treatment stages and CD4 categories.
  void calculate_art_5yr() {
    auto& n_ha = state_next.ha;
    auto& n_hc = state_next.hc;
    auto& n_sp = state_next.sp;

    // Adults
    for (int s = 0; s < NS; ++s) {
      int a = p_idx_hiv_first_adult;
      for (int ha = 0; ha < hAG; ++ha) {
        for (int i = 0; i < hAG_span[ha]; ++i, ++a) {
          for (int hm = 0; hm < hDS; ++hm) {
            for (int hu = 0; hu < hTS; ++hu) {
              n_sp.p5_art(a / 5, s) += n_ha.h_artpop(hu, hm, ha, s);
            }
          }
        }
      }
    }

    // Children ages 0-4 (hc1 model)
    for (int s = 0; s < NS; ++s) {
      for (int a = 0; a < hc2_agestart; ++a) {
        for (int hd = 0; hd < hc1DS; ++hd) {
          for (int dur = 0; dur < hTS; ++dur) {
            n_sp.p5_art(a / 5, s) += n_hc.hc1_artpop(dur, hd, a, s);
          }
        }
      }
    }

    // Children ages 5-14 (hc2 model)
    for (int s = 0; s < NS; ++s) {
      for (int a = hc2_agestart; a < p_idx_hiv_first_adult; ++a) {
        for (int hd = 0; hd < hc2DS; ++hd) {
          for (int dur = 0; dur < hTS; ++dur) {
            n_sp.p5_art(a / 5, s) += n_hc.hc2_artpop(dur, hd, a - hc2_agestart, s);
          }
        }
      }
    }
  }
};

}
}
