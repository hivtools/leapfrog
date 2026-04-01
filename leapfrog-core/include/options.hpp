#pragma once

#include <algorithm>
#include <cmath>
#include <stdexcept>
#include <string>
#include <string_view>
#include <vector>

#include "generated/state_space.hpp"

namespace leapfrog {
namespace internal {

inline void validate_output_years(
    const std::vector<int>& output_years, const int proj_start_year
) {
  const auto first_year =
      std::min_element(std::begin(output_years), std::end(output_years));
  if (*first_year < proj_start_year) {
    throw std::runtime_error(
        "Trying to output for year: '" + std::to_string(*first_year)
        + "' which is before the projection start year: '"
        + std::to_string(proj_start_year) + "'."
    );
  }
}

inline int get_proj_end_year(const std::vector<int>& output_years) {
  const auto last_year =
      std::max_element(std::begin(output_years), std::end(output_years));
  return *last_year;
}

inline int get_proj_period_enum(std::string_view projection_period) {
  if (projection_period == "midyear") {
    return BaseSS::PROJPERIOD_MIDYEAR;
  }

  if (projection_period == "calendar") {
    return BaseSS::PROJPERIOD_CALENDAR;
  }

  throw std::invalid_argument(
      "Invalid projection period: '" + std::string(projection_period)
      + "'. Allowed values are: 'midyear' or 'calendar'."
  );
}

}  // namespace internal

template<typename real_type>
struct Options {
  int hts_per_year;
  double dt;
  int ts_art_start;
  int proj_period_int;
  int proj_start_year;
  int proj_end_year;
  int proj_steps;

  Options(
      int _hts_per_year,
      int _ts_art_start,
      int _proj_period_int,
      int _proj_start_year,
      int _proj_end_year
  ) :
      hts_per_year(_hts_per_year),
      dt(1.0 / _hts_per_year),
      ts_art_start(_ts_art_start),
      proj_period_int(_proj_period_int),
      proj_start_year(_proj_start_year),
      proj_end_year(_proj_end_year),
      proj_steps(_proj_end_year - _proj_start_year + 1) {}
};

template<typename real_type>
const Options<real_type> get_opts(
    const int hiv_steps,
    const int t_ART_start,
    const std::string_view projection_period,
    const int proj_start_year,
    const std::vector<int>& output_years
) {
  internal::validate_output_years(output_years, proj_start_year);
  const int proj_period = internal::get_proj_period_enum(projection_period);
  const int proj_end_year = internal::get_proj_end_year(output_years);
  const Options<real_type> opts = {
      hiv_steps, t_ART_start, proj_period, proj_start_year, proj_end_year
  };
  return opts;
}

}  // namespace leapfrog
