# Enables cppcheck when LEAPFROG_ENABLE_CPPCHECK=ON.
if(LEAPFROG_ENABLE_CPPCHECK)
  find_program(CPPCHECK_EXE
    NAMES cppcheck
    DOC "Path to cppcheck executable"
  )
  if(NOT CPPCHECK_EXE)
    message(WARNING
      "LEAPFROG_ENABLE_CPPCHECK is ON but cppcheck was not found. "
      "Install it: sudo apt install cppcheck"
    )
  else()
    message(STATUS "cppcheck: ${CPPCHECK_EXE}")
    set(CMAKE_CXX_CPPCHECK
      "${CPPCHECK_EXE}"
      "--enable=all"
      "--suppress=missingInclude"
      "--suppress=missingIncludeSystem"
      "--inline-suppr"
      "--std=c++20"
    )

  endif()
endif()
