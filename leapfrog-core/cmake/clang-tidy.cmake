# Enables clang-tidy when LEAPFROG_ENABLE_CLANG_TIDY=ON.
# Prefers clang-tidy-18 so the version is explicit; falls back to clang-tidy.
if(LEAPFROG_ENABLE_CLANG_TIDY)
  find_program(CLANG_TIDY_EXE
    NAMES clang-tidy-18 clang-tidy
    DOC "Path to clang-tidy executable"
  )
  if(NOT CLANG_TIDY_EXE)
    message(WARNING
      "LEAPFROG_ENABLE_CLANG_TIDY is ON but no clang-tidy executable was found. "
      "Install clang-tidy-18: sudo apt install clang-tidy-18"
    )
  else()
    message(STATUS "clang-tidy: ${CLANG_TIDY_EXE}")
    set(CMAKE_CXX_CLANG_TIDY "${CLANG_TIDY_EXE}")
  endif()
endif()
