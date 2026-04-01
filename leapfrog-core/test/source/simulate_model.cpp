#include <cstddef>
#include <cstdlib>
#include <filesystem>
#include <iostream>
#include <numeric>
#include <string>
#include <string_view>
#include <vector>

#include "H5Cpp.h"  // NOLINT(unused-includes)
#include "generated/cpp_interface/cpp_adapters.hpp"
#include "leapfrog.hpp"

namespace {
constexpr int kMaxSimYears = 61;
constexpr int kSimStartYear = 1970;
}  // namespace

int main(int argc, char* argv[]) {
  try {
    if (argc < 4) {
      std::cout
          << "Usage: simulate_model <sim_years> <params_file> <output_dir>"
          << "\n";
      return 1;
    }

    int sim_years = std::stoi(
        argv[1]  // NOLINT(cppcoreguidelines-pro-bounds-pointer-arithmetic)
    );
    std::string const params_file =
        argv[2];  // NOLINT(cppcoreguidelines-pro-bounds-pointer-arithmetic)
    std::string const output_dir =
        argv[3];  // NOLINT(cppcoreguidelines-pro-bounds-pointer-arithmetic)

    std::filesystem::path const params_abs =
        std::filesystem::absolute(params_file);
    if (!std::filesystem::exists(params_abs)) {
      std::cout << "Params file '" << params_file << "' does not exist."
                << "\n";
      return 1;
    }

    std::filesystem::path const output_abs =
        std::filesystem::absolute(output_dir);
    if (!std::filesystem::exists(output_abs)) {
      if (std::filesystem::create_directory(output_abs)) {
        std::cout << "Created output directory '" << std::string {output_abs}
                  << "'" << "\n";
      } else {
        std::cout << "Failed to create output directory '"
                  << std::string {output_abs} << "'" << "\n";
      }
    } else {
      std::cout << "Writing to existing output directory '"
                << std::string {output_abs} << "'" << "\n";
    }

    if (sim_years > kMaxSimYears) {
      std::cout << "Running to max no of sim years: " << kMaxSimYears << "\n\n";
      sim_years = kMaxSimYears;
    }

    std::vector<int> output_years(static_cast<size_t>(sim_years));
    std::iota(output_years.begin(), output_years.end(), kSimStartYear);

    const char* n_runs_char =
        std::getenv("N_RUNS");  // NOLINT(concurrency-mt-unsafe)
    size_t n_runs = 1;
    if (n_runs_char != nullptr) {
      // If we're profiling we want to get accurate info about where time is
      // spent during the main model fit. This runs so quickly though that just
      // going through once won't sample enough times for us to see. And it will
      // sample from the tensor file serialization/deserialization more. So we
      // run the actual model fit multiple times when profiling so the sampler
      // can actually pick up the slow bits.
      n_runs = std::stoul(n_runs_char);
      std::cout << "Running model fit " << n_runs << " times" << "\n";
    }

    using LF = leapfrog::
        Leapfrog<leapfrog::Cpp, double, leapfrog::HivFullAgeStratification>;
    using OP = leapfrog::internal::
        OwnedParsMixed<double, leapfrog::HivFullAgeStratification>;

    const auto opts = leapfrog::get_opts<double>(
        10, 30, std::string_view {"midyear"}, kSimStartYear, output_years
    );
    auto owned_pars = OP::parse_pars(params_abs, opts);
    const auto pars = LF::Cfg::get_pars(owned_pars);
    for (size_t i = 0; i < n_runs; ++i) {
      auto state = LF::run_model(pars, opts, output_years);
    }
    std::cout << "Fit complete" << "\n";

    auto state = LF::run_model(pars, opts, output_years);

    std::filesystem::path const output_file = output_abs / "output.h5";
    const H5std_string FILE_NAME(output_file);
    H5::H5File file(FILE_NAME, H5F_ACC_TRUNC);  // NOLINT(misc-include-cleaner)
    file.close();

    LF::Cfg::build_output(0, state, output_file);

    return 0;
  } catch (const std::exception& e) {
    std::cerr << "Error: " << e.what() << "\n";
    return 1;
  }
}
