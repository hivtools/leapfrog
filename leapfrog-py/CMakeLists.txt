cmake_minimum_required(VERSION 3.15...3.27)
project(${SKBUILD_PROJECT_NAME} LANGUAGES CXX)

# Try to import all Python components potentially needed by nanobind
find_package(Python 3.10
  REQUIRED COMPONENTS Interpreter Development.Module
  OPTIONAL_COMPONENTS Development.SABIModule)

# Import nanobind through CMake's find_package mechanism
find_package(nanobind CONFIG REQUIRED)

# set C++ to require 20
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

nanobind_add_module(_core MODULE src/main.cpp)
<<<<<<< HEAD
target_include_directories(_core PRIVATE ../leapfrogr/inst/include)
=======
target_include_directories(_core PRIVATE ../leapfrog-core/include)
>>>>>>> 11ae9f4be0fefc897892a8eb6689b4043c7c0bd7
install(TARGETS _core DESTINATION ${SKBUILD_PROJECT_NAME})
