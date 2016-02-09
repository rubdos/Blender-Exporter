project(thebounty-blender)
cmake_minimum_required (VERSION 2.6)

find_package(PythonLibs 3 REQUIRED)

if(CMAKE_SYSTEM_PROCESSOR MATCHES "x86_64")
    add_definitions(-fPIC)
endif(CMAKE_SYSTEM_PROCESSOR MATCHES "x86_64")

include_directories(src)
include_directories(${PYTHON_INCLUDE_DIRS})
add_subdirectory(src)
