project(GA-LMS)
cmake_minimum_required(VERSION 2.8)
set(SRC ".")
aux_source_directory(${SRC} SRC_LIST)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -std=c++11")

find_package(PCL 1.7.0 REQUIRED)
find_package(Boost 1.36.0 COMPONENTS iostreams system filesystem)

include_directories(${SRC_LIST})
include_directories(${PCL_INCLUDE_DIRS})
include_directories(${Boost_INCLUDE_DIRS})

link_directories(${PCL_LIBRARY_DIRS})
link_directories(${Boost_LIBRARY_DIRS})

add_definitions(${PCL_DEFINITIONS})
add_executable(${PROJECT_NAME} main.cpp)
target_link_libraries(${PROJECT_NAME} ${Boost_LIBRARIES})
target_link_libraries(${PROJECT_NAME} ${PCL_LIBRARIES})
