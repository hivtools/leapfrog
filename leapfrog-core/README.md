# leapfrog

A header-only C++20 library implementing a multistate population projection model for estimating
population, demographic indicators, and HIV epidemic dynamics. The library supports multiple
language bindings (C, C++, Python, R) via generated adapters.

## Prerequisites

- CMake 3.14+
- A C++20 compiler
- HDF5 (for the `simulate_model` tool and tests)

```sh
sudo apt-get install libhdf5-dev   # Debian/Ubuntu
brew install hdf5                  # macOS
```

## Building with presets

This project uses [CMake presets](https://cmake.org/cmake/help/latest/manual/cmake-presets.7.html).
Create a `CMakeUserPresets.json` at the project root (not checked in) to define your local presets.
Replace `ci-linux` with `ci-darwin` or `ci-win64` for your platform:

```json
{
  "version": 2,
  "cmakeMinimumRequired": { "major": 3, "minor": 14, "patch": 0 },
  "configurePresets": [
    {
      "name": "dev",
      "binaryDir": "${sourceDir}/build/dev",
      "inherits": ["dev-mode", "ci-linux"],
      "cacheVariables": { "CMAKE_BUILD_TYPE": "Debug" }
    },
    {
      "name": "release",
      "binaryDir": "${sourceDir}/build/release",
      "inherits": "ci-linux",
      "cacheVariables": { "CMAKE_BUILD_TYPE": "Release" }
    }
  ],
  "buildPresets": [
    { "name": "dev", "configurePreset": "dev", "configuration": "Debug" },
    { "name": "release", "configurePreset": "release", "configuration": "Release" }
  ],
  "testPresets": [
    {
      "name": "dev",
      "configurePreset": "dev",
      "configuration": "Debug",
      "output": { "outputOnFailure": true }
    }
  ]
}
```

Then configure, build, and test:

```sh
cmake --preset=dev
cmake --build --preset=dev
ctest --preset=dev
```

Or for a release build:

```sh
cmake --preset=release
cmake --build --preset=release
```

> **Note:** Some IDEs will auto-configure using presets. In CLion, ensure only your desired
> preset has "Enable profile" ticked under `File > Settings > Build, Execution, Deployment > CMake`.
> In Visual Studio, set "Never run configure step automatically" in `Tools > Options > CMake`
> before opening the project.

## simulate_model

`simulate_model` is a CLI tool for running the model fit from the command line, useful for
profiling and validating results without an R or Python runtime.

```sh
./build/dev/test/simulate_model <sim_years> <params_file> <output_dir>
```

Arguments:

- `sim_years` — number of simulation years, up to 61 (covering 1970–2030 inclusive)
- `params_file` — path to an HDF5 parameter file
- `output_dir` — directory where `output.h5` will be written (created if it does not exist)

Example:

```sh
./build/dev/test/simulate_model 61 ../leapfrogr/tests/testthat/testdata/adult_parms_full.h5 output
```

### Profiling

Set `N_RUNS` to run the model fit multiple times. A single run is too fast for a sampling
profiler to get meaningful samples:

```sh
N_RUNS=100 ./build/dev/test/simulate_model 61 params.h5 output
```

## Test data

The `simulate_model_test` CTest uses `adult_parms_full.h5` from
`leapfrogr/tests/testthat/testdata/`. The path defaults to
`../leapfrogr/tests/testthat/testdata` relative to this directory and can be overridden with
the `LEAPFROG_TEST_DATA_DIR` CMake cache variable.

## Developer mode targets

The `dev` preset enables developer mode. Additional build targets:

| Target | Description |
|---|---|
| `coverage` | Coverage report (requires `ENABLE_COVERAGE`) |
| `docs` | Doxygen + m.css documentation (requires `BUILD_MCSS_DOCS`) |
| `format-check` / `format-fix` | clang-format |

To run these pass an addition `-t <target> flag` e.g.

```sh
cmake --build --preset=dev -t format-fix
```

## Installing

```sh
cmake --build --preset=release --target install
```

The installed package can be consumed via CMake's `find_package`:

```cmake
find_package(leapfrog REQUIRED)
# Declare the imported target as a build requirement using PRIVATE, where
# project_target is a target created in the consuming project
target_link_libraries(my_target PRIVATE leapfrog::leapfrog)
```

## Headers

- `include/generated/` — auto-generated code, do not modify manually
- `include/models/` — model implementation code

When using leapfrog from an R package, add it to `LinkingTo:` in the package `DESCRIPTION`.
