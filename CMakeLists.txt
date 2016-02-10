project(thebounty-blender)
cmake_minimum_required (VERSION 2.6)
set(CMAKE_MODULE_PATH "${CMAKE_SOURCE_DIR}/CMakeModules")

find_package(PythonLibs 3 REQUIRED)
find_package(TheBounty REQUIRED)

if(CMAKE_SYSTEM_PROCESSOR MATCHES "x86_64")
    add_definitions(-fPIC)
endif(CMAKE_SYSTEM_PROCESSOR MATCHES "x86_64")

include_directories(src)
include_directories(${PYTHON_INCLUDE_DIRS})
include_directories(${THE_BOUNTY_INCLUDE_DIRS})
add_subdirectory(src)
