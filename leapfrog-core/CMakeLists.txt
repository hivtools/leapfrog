cmake_minimum_required(VERSION 3.25)

project(
  leapfrog-core
  VERSION 0.1.0
  DESCRIPTION "Leapfrog simulation engine - C++ header-only library"
  HOMEPAGE_URL "https://github.com/hivtools/leapfrog"
  LANGUAGES CXX
)

if(PROJECT_SOURCE_DIR STREQUAL PROJECT_BINARY_DIR)
  message(FATAL_ERROR
    "In-source builds are not allowed. "
    "Run cmake from a separate build directory, e.g.:\n"
    "  cmake --preset dev"
  )
endif()

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Export compile commands for clangd / IDE tooling
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# ---- Options ----------------------------------------------------------------

option(BUILD_TESTING "Build tests" ON)
option(LEAPFROG_ENABLE_CLANG_TIDY "Enable clang-tidy static analysis" OFF)
option(LEAPFROG_ENABLE_CPPCHECK "Enable cppcheck static analysis" OFF)
option(LEAPFROG_ENABLE_DOXYGEN "Build API documentation with Doxygen" OFF)
option(LEAPFROG_WARNINGS_AS_ERRORS "Treat compiler warnings as errors" OFF)

# ---- CMake modules ----------------------------------------------------------

list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake")
include(compiler-warnings)
include(clang-tidy)
include(cppcheck)
include(doxygen)

# ---- Dependencies -----------------------------------------------------------

find_package(HDF5 REQUIRED COMPONENTS C CXX)

# ---- Header-only library target ---------------------------------------------

add_library(leapfrog-core INTERFACE)
add_library(leapfrog::core ALIAS leapfrog-core)

# Mark the include directory as SYSTEM so the compiler suppresses warnings from
# vendored third-party headers (e.g. array/array.h). Clang-tidy still analyses
# our own headers via HeaderFilterRegex, so static analysis quality is unchanged.
target_include_directories(leapfrog-core SYSTEM INTERFACE
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
)
target_compile_features(leapfrog-core INTERFACE cxx_std_20)
target_link_libraries(leapfrog-core INTERFACE HDF5::HDF5)

# ---- Executables ------------------------------------------------------------

add_executable(simulate_model src/simulate_model.cpp)
target_link_libraries(simulate_model PRIVATE leapfrog::core)
leapfrog_set_compiler_warnings(simulate_model)

# ---- Tests ------------------------------------------------------------------

if(BUILD_TESTING)
  enable_testing()
  add_subdirectory(test)
endif()
