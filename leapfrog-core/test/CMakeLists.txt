cmake_minimum_required(VERSION 3.14)

project(leapfrogTests LANGUAGES CXX)

include(../cmake/project-is-top-level.cmake)
include(../cmake/folders.cmake)

# ---- Dependencies ----

if(PROJECT_IS_TOP_LEVEL)
  find_package(leapfrog REQUIRED)
  enable_testing()
endif()

find_package(HDF5 REQUIRED COMPONENTS C CXX)

# ---- simulate_model ----

set(
    LEAPFROG_TEST_DATA_DIR
    "${PROJECT_SOURCE_DIR}/../leapfrogr/tests/testthat/testdata"
    CACHE PATH "Path to leapfrog test data directory containing adult_parms_full.h5"
)

add_executable(simulate_model source/simulate_model.cpp)
target_link_libraries(simulate_model PRIVATE leapfrog::leapfrog ${HDF5_C_LIBRARIES} ${HDF5_CXX_LIBRARIES})
target_include_directories(simulate_model PRIVATE ${HDF5_INCLUDE_DIRS})
target_include_directories(simulate_model SYSTEM PRIVATE "${PROJECT_SOURCE_DIR}/../include/array")
target_compile_features(simulate_model PRIVATE cxx_std_20)

add_test(
    NAME simulate_model_test
    COMMAND simulate_model 61
      "${LEAPFROG_TEST_DATA_DIR}/adult_parms_full.h5"
      "${CMAKE_CURRENT_BINARY_DIR}/simulate_model_output"
)

# ---- End-of-file commands ----

add_folders(Test)
