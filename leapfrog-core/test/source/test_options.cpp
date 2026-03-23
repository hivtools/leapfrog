#include <catch2/catch_test_macros.hpp>
#include <stdexcept>
#include <vector>

#include "options.hpp"

TEST_CASE("get_opts builds correct Options struct", "[options]") {
  const std::vector<int> output_years = {1970, 1980, 1990, 2000, 2010, 2020, 2030};

  auto opts = leapfrog::get_opts<double>(10, 30, "midyear", 1970, output_years);

  REQUIRE(opts.hts_per_year == 10);
  REQUIRE(opts.dt == 1.0 / 10);
  REQUIRE(opts.ts_art_start == 30);
  REQUIRE(opts.proj_start_year == 1970);
  REQUIRE(opts.proj_end_year == 2030);
  REQUIRE(opts.proj_steps == 61);
}

TEST_CASE("get_opts rejects output year before projection start", "[options]") {
  const std::vector<int> output_years = {1969, 1980};
  REQUIRE_THROWS_AS(
    leapfrog::get_opts<double>(10, 30, "midyear", 1970, output_years),
    std::runtime_error
  );
}

TEST_CASE("get_opts rejects invalid projection period", "[options]") {
  const std::vector<int> output_years = {1970, 2030};
  REQUIRE_THROWS_AS(
    leapfrog::get_opts<double>(10, 30, "annual", 1970, output_years),
    std::invalid_argument
  );
}

TEST_CASE("get_opts accepts calendar projection period", "[options]") {
  const std::vector<int> output_years = {1970, 2030};
  REQUIRE_NOTHROW(leapfrog::get_opts<double>(10, 30, "calendar", 1970, output_years));
}
