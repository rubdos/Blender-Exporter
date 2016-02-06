project(thebounty-blender)
cmake_minimum_required (VERSION 2.6)

find_package(PythonLibs 3 REQUIRED)

include_directories(src)
include_directories(${PYTHON_INCLUDE_DIRS})
add_subdirectory(src)
