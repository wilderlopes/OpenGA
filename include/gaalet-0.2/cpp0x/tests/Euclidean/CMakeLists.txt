project(Euclidean)
cmake_minimum_required(VERSION 2.8)
set(SRC ".")
aux_source_directory(${SRC} SRC_LIST)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -std=c++11")

#include_directories ("../../../include/cpp0x")

add_executable(${PROJECT_NAME} Euclidean.cpp)



