cmake_minimum_required(VERSION 3.10)

project(Paintball)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)
set(CMAKE_BUILD_TYPE Debug)

file(COPY data DESTINATION ./)

include_directories(${PROJECT_SOURCE_DIR})

add_executable(program Program.cpp)