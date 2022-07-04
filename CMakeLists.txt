cmake_minimum_required(VERSION 3.15)
project(nethack_language_wrapper)

message(STATUS "Building nle_language_wrapper backend")

set(CMAKE_POSITION_INDEPENDENT_CODE ON)

add_compile_definitions(
  GCC_WARN
  NOCLIPPING
  NOMAIL
  NOTPARMDECL
  DEFAULT_WINDOW_SYS="rl"
  DLB
  NOCWD_ASSUMPTIONS)

set(CMAKE_CXX_FLAGS "-O3 -Wall -Wextra")

set(NLE_BASE ${PYTHON_SRC_PARENT}/nle/nle)
set(NLE_INC ${PYTHON_SRC_PARENT}/nle/)
set(NLE_INC_GEN ${PYTHON_SRC_PARENT}/nle/build/temp.linux-x86_64-3.9/include)

add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/pybind11)
pybind11_add_module(
  nle_language_obsv
  src/main.cpp )

set_target_properties(nle_language_obsv PROPERTIES CXX_STANDARD 17)
target_link_directories(nle_language_obsv PUBLIC ${NLE_BASE})
target_include_directories(nle_language_obsv PUBLIC ${NLE_INC})
target_include_directories(nle_language_obsv PUBLIC ${NLE_INC_GEN})
target_link_libraries(nle_language_obsv PUBLIC nethack)
