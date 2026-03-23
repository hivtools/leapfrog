# ---- Unit tests (Catch2, auto-discovered) ------------------------------------
#
# Any .cpp file added under test/source/ is picked up automatically — no
# CMakeLists changes required.  Each Catch2 TEST_CASE becomes its own CTest
# test entry via catch_discover_tests().

include(FetchContent)
FetchContent_Declare(
  Catch2
  GIT_REPOSITORY https://github.com/catchorg/Catch2.git
  GIT_TAG        v3.8.0
)
FetchContent_MakeAvailable(Catch2)

file(GLOB_RECURSE unit_test_sources CONFIGURE_DEPENDS
  "${CMAKE_CURRENT_SOURCE_DIR}/source/*.cpp"
)

if(unit_test_sources)
  add_executable(unit_tests ${unit_test_sources})
  target_link_libraries(unit_tests PRIVATE leapfrog::core Catch2::Catch2WithMain)
  leapfrog_set_compiler_warnings(unit_tests)

  list(APPEND CMAKE_MODULE_PATH "${catch2_SOURCE_DIR}/extras")
  include(Catch)
  catch_discover_tests(unit_tests PROPERTIES LABELS "unit")
endif()

# ---- Integration tests -------------------------------------------------------
#
# The smoke test runs simulate_model against real parameter data to verify the
# full pipeline compiles and executes correctly.  The test data lives alongside
# the R package; when building inside the monorepo the path resolves
# automatically.  Override TEST_DATA_FILE on the command line to point at any
# valid HDF5 params file when building outside the monorepo.

set(TEST_DATA_FILE
  "${CMAKE_SOURCE_DIR}/../leapfrogr/tests/testthat/testdata/adult_parms_full.h5"
  CACHE FILEPATH "HDF5 parameter file used by the smoke test"
)

set(TEST_OUTPUT_DIR "${CMAKE_BINARY_DIR}/test_output")
file(MAKE_DIRECTORY "${TEST_OUTPUT_DIR}")

if(NOT EXISTS "${TEST_DATA_FILE}")
  message(WARNING
    "Test data not found at:\n  ${TEST_DATA_FILE}\n"
    "The smoke_test will fail unless TEST_DATA_FILE is set to a valid path.\n"
    "When building inside the monorepo this resolves automatically."
  )
endif()

add_test(
  NAME smoke_test
  COMMAND simulate_model 61 "${TEST_DATA_FILE}" "${TEST_OUTPUT_DIR}/smoke_test"
)
set_tests_properties(smoke_test PROPERTIES
  PASS_REGULAR_EXPRESSION "Fit complete"
  LABELS "integration"
  TIMEOUT 120
)

# ---- Benchmarking -----------------------------------------------------------
#
# Run the model fit N times to gather profiling data.  Not a normal test;
# invoke explicitly via:
#   N_RUNS=100 ctest -R benchmark --verbose
#
# Or run the binary directly:
#   N_RUNS=100 ./build/dev/simulate_model 61 <params.h5> <output_dir>

add_test(
  NAME benchmark
  COMMAND simulate_model 61 "${TEST_DATA_FILE}" "${TEST_OUTPUT_DIR}/benchmark"
)
set_tests_properties(benchmark PROPERTIES
  ENVIRONMENT "N_RUNS=10"
  PASS_REGULAR_EXPRESSION "Fit complete"
  LABELS "benchmark"
  TIMEOUT 300
)
