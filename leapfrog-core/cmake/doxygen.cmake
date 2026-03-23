# Adds a `docs` build target when LEAPFROG_ENABLE_DOXYGEN=ON.
# Run: cmake --build <build-dir> --target docs
if(LEAPFROG_ENABLE_DOXYGEN)
  find_package(Doxygen OPTIONAL_COMPONENTS dot)
  if(NOT DOXYGEN_FOUND)
    message(WARNING
      "LEAPFROG_ENABLE_DOXYGEN is ON but Doxygen was not found. "
      "Install it: sudo apt install doxygen"
    )
  else()
    message(STATUS "Doxygen: ${DOXYGEN_EXECUTABLE} — 'docs' target available")
    set(DOXYGEN_EXTRACT_ALL YES)
    set(DOXYGEN_BUILTIN_STL_SUPPORT YES)
    set(DOXYGEN_RECURSIVE YES)
    set(DOXYGEN_GENERATE_HTML YES)
    set(DOXYGEN_HTML_OUTPUT "${CMAKE_BINARY_DIR}/docs/html")
    doxygen_add_docs(
      docs
      "${PROJECT_SOURCE_DIR}/include"
      COMMENT "Generate API documentation"
    )
  endif()
endif()
