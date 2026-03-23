# leapfrog-core

C++20 header-only library implementing the Leapfrog demographic simulation engine.

## Directory layout

```
leapfrog-core/
  include/          # Public headers (the library itself)
    generated/      # Auto-generated from model schemas — do not edit by hand
    models/         # Model implementation
    array/          # N-dimensional array libary [nda](https://github.com/dsharlet/array)
  src/
    simulate_model.cpp   # CLI entry point for running the model
  test/
    CMakeLists.txt       # CTest integration tests
  cmake/                 # CMake helper modules
```

## Prerequisites

| Tool | Minimum version | Notes |
|------|----------------|-------|
| CMake | 3.25 | `sudo apt install cmake` or [cmake.org](https://cmake.org/download/) |
| C++ compiler | GCC 13 / Clang 16 / MSVC 2022 | C++20 required |
| HDF5 (dev) | any recent | `sudo apt install libhdf5-dev` |
| clang-tidy | 18 (optional) | `sudo apt install clang-tidy-18` |
| cppcheck | any (optional) | `sudo apt install cppcheck` |
| Doxygen | any (optional) | `sudo apt install doxygen` |

### Generating headers

The `include/generated/` directory is produced by the codegen step and is not
committed to the repository.  Before building, run codegen from the repo root:

```sh
cd codegen
uv run src/main.py
```

Or use the `scripts/generate` helper from the repo root.

## Building

The project uses [CMake presets](https://cmake.org/cmake/help/latest/manual/cmake-presets.7.html).

### Development build (debug + tests)

```sh
cmake --preset dev          # configure
cmake --build --preset dev  # compile
ctest --preset dev          # run tests
```

The compiled binary is at `build/dev/simulate_model`.

### Release build

```sh
cmake --preset release
cmake --build --preset release
```

### With static analysis (clang-tidy + cppcheck)

```sh
cmake --preset dev-tools
cmake --build --preset dev-tools
```

Requires `clang-tidy-18` and `cppcheck` to be installed.

### API documentation

```sh
cmake --preset dev -DLEAPFROG_ENABLE_DOXYGEN=ON
cmake --build build/dev --target docs
# open build/dev/docs/html/index.html
```

## Running the model

```
simulate_model <sim_years> <params_file> <output_dir>
```

| Argument | Description |
|----------|-------------|
| `sim_years` | Number of years to simulate (max 61, covering 1970–2030) |
| `params_file` | Path to HDF5 parameter file |
| `output_dir` | Directory where `output.h5` will be written (created if absent) |

Example using the R package test data:

```sh
./build/dev/simulate_model 61 \
  ../leapfrogr/tests/testthat/testdata/adult_parms_full.h5 \
  /tmp/leapfrog_output
```

### Benchmarking

Set `N_RUNS` to run the model fit multiple times (useful for profiling):

```sh
N_RUNS=100 ./build/release/simulate_model 61 params.h5 /tmp/out
```

Or via CTest (runs 10 times by default):

```sh
ctest --preset dev -R benchmark --verbose
```

## Tests

The test suite uses CTest. Tests require the R package test data to be
available at `../leapfrogr/tests/testthat/testdata/adult_parms_full.h5`
(resolved automatically when building inside the monorepo).

To point at a different params file:

```sh
cmake --preset dev -DTEST_DATA_FILE=/path/to/params.h5
```

Run all tests:

```sh
ctest --preset dev
```

Run only integration tests:

```sh
ctest --preset dev -L integration
```

## VSCode setup

1. Install the [CMake Tools](https://marketplace.visualstudio.com/items?itemName=ms-vscode.cmake-tools) extension.
2. Open the `leapfrog-core/` folder in VSCode.
3. When prompted, select a kit (compiler). If not prompted run configuration from command palette `CMake: Configure` CMake Tools will detect the presets automatically.
4. Select the `dev` configure preset from the status bar or Command Palette (`CMake: Select Configure Preset`).
5. Build with `CMake: Build` (F7) or the status bar button.
6. Run tests with `CMake: Run Tests` or `ctest --preset dev` in the terminal.

Recommended extensions:

- [C/C++ Extension Pack](https://marketplace.visualstudio.com/items?itemName=ms-vscode.cpptools-extension-pack) — IntelliSense, debugging
- [CMake Tools](https://marketplace.visualstudio.com/items?itemName=ms-vscode.cmake-tools) — configure/build/test integration
- [clangd](https://marketplace.visualstudio.com/items?itemName=llvm-vs-code-extensions.vscode-clangd) — fast, accurate C++ IntelliSense (alternative to ms-vscode.cpptools)

For clangd you need to configure once first (`cmake --preset dev`) so that `build/dev/compile_commands.json` is generated, then set in `.vscode/settings.json`:

```json
{
  "clangd.arguments": ["--compile-commands-dir=${workspaceFolder}/leapfrog-core/build/dev"]
}
```

If you use clangd best to disable the C/C++ IntelliSense in your `settings.json`:

```
"C_Cpp.intelliSenseEngine": "disabled",
```
