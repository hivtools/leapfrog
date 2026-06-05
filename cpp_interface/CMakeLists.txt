cmake_minimum_required(VERSION 3.19)
project(standalone_model)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(HDF5 REQUIRED COMPONENTS C CXX)
add_executable(simulate_model simulate_model.cpp)
target_link_libraries(simulate_model HDF5::HDF5)
<<<<<<< HEAD
target_include_directories(simulate_model PRIVATE ../leapfrogr/inst/include/)
=======
target_include_directories(simulate_model PRIVATE ../leapfrog-core/include/)
>>>>>>> 66b296cb6502fc8d02f65f1349ba8ba9bfb290a7

