set(TBY_BLENDER_SRC
    blender/python_class.cpp
    blender/blender_render_settings.cpp
    blender/blender_camera.cpp
    blender/blender_bounty.cpp
    blender/blender_scene.cpp)

set(TBY_EXPORTER_SRC
    tby_export.cpp
    tby_blender.cpp
    )

include_directories(blender)

add_library(tby_blender_backend STATIC ${TBY_BLENDER_SRC})
add_library(tby_blender SHARED ${TBY_EXPORTER_SRC})

target_compile_features(tby_blender_backend PRIVATE cxx_range_for)
target_compile_features(tby_blender PRIVATE cxx_range_for)

target_link_libraries(tby_blender tby_blender_backend ${PYTHON_LIBRARIES})
set_target_properties(tby_blender PROPERTIES PREFIX "")
install(TARGETS tby_blender LIBRARY DESTINATION ${CMAKE_SOURCE_DIR}/io)
