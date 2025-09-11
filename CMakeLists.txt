cmake_minimum_required(VERSION 3.15)
project(nethack_language_wrapper)
cmake_policy(SET CMP0148 OLD)

message(STATUS "Building nle_language_wrapper backend")

set(CMAKE_POSITION_INDEPENDENT_CODE ON)

include(FetchContent)
FetchContent_Declare(
  nle
  GIT_REPOSITORY https://github.com/jbcoe/nle-nethack.git
  GIT_TAG 88a8da68dbd95e55ae6dbdd2fd2f1810bbad8207)
FetchContent_MakeAvailable(nle)
find_package(pybind11 CONFIG REQUIRED)

pybind11_add_module(
  nle_language_obsv
  src/main.cpp )

target_compile_definitions(
  nle_language_obsv
  PRIVATE
  GCC_WARN
  NOCLIPPING
  NOMAIL
  NOTPARMDECL
  DEFAULT_WINDOW_SYS="rl"
  DLB
  NOCWD_ASSUMPTIONS)

target_compile_options(
  nle_language_obsv 
  PRIVATE -O3 -Wall -Wextra)

set_target_properties(
  nle_language_obsv
  PROPERTIES
  CXX_STANDARD 17
  POSITION_INDEPENDENT_CODE ON
  # Add relative rpath to enable finding the nethack shared library in site_packages/nle.
  LINK_FLAGS "-Wl,-rpath,'$ORIGIN/../nle'")

target_link_libraries(
  nle_language_obsv 
  PUBLIC 
  nethack)

install(TARGETS nle_language_obsv
  LIBRARY DESTINATION nle_language_wrapper)
