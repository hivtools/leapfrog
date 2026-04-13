cmake_minimum_required(VERSION 3.14)

include(cmake/prelude.cmake)

project(
    leapfrog
    VERSION 0.1.0
    DESCRIPTION "Multistate population projection model for estimating population, demographic indicators, and HIV epidemic."
    HOMEPAGE_URL "hivtools.github.io/leapfrog/"
    LANGUAGES NONE
)

include(cmake/project-is-top-level.cmake)
include(cmake/variables.cmake)

# ---- Declare library ----

add_library(leapfrog_leapfrog INTERFACE)
add_library(leapfrog::leapfrog ALIAS leapfrog_leapfrog)

set_property(
    TARGET leapfrog_leapfrog PROPERTY
    EXPORT_NAME leapfrog
)

target_include_directories(
    leapfrog_leapfrog ${warning_guard}
    INTERFACE
    "\$<BUILD_INTERFACE:${PROJECT_SOURCE_DIR}/include>"
)

target_compile_features(leapfrog_leapfrog INTERFACE cxx_std_20)

# ---- Install rules ----

if(NOT CMAKE_SKIP_INSTALL_RULES)
  include(cmake/install-rules.cmake)
endif()

# ---- Developer mode ----

if(NOT leapfrog_DEVELOPER_MODE)
  return()
elseif(NOT PROJECT_IS_TOP_LEVEL)
  message(
      AUTHOR_WARNING
      "Developer mode is intended for developers of leapfrog"
  )
endif()

include(cmake/dev-mode.cmake)
