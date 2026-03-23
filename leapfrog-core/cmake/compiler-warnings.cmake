# Adds recommended compiler warning flags to a target.
# Call leapfrog_set_compiler_warnings(<target>) after add_executable/add_library.
function(leapfrog_set_compiler_warnings target)
  if(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
    target_compile_options(${target} PRIVATE
      -Wall
      -Wextra
      -Wpedantic
      -Wconversion
      -Wsign-conversion
      -Wnull-dereference
      -Wdouble-promotion
      -Wformat=2
      "$<$<BOOL:${LEAPFROG_WARNINGS_AS_ERRORS}>:-Werror>"
    )
  elseif(CMAKE_CXX_COMPILER_ID STREQUAL "MSVC")
    target_compile_options(${target} PRIVATE
      /W4
      /permissive-
      "$<$<BOOL:${LEAPFROG_WARNINGS_AS_ERRORS}>:/WX>"
    )
  endif()
endfunction()
