set(TBY_BLENDER_SRC
    python_class.cpp
    blender_render_settings.cpp
    tby_export.cpp
    tby_blender.cpp
    blender_scene.cpp)

add_library(tby_blender SHARED ${TBY_BLENDER_SRC})
target_compile_features(tby_blender PRIVATE cxx_range_for)
target_link_libraries(tby_blender ${PYTHON_LIBRARIES})
set_target_properties(tby_blender PROPERTIES PREFIX "")
install(TARGETS tby_blender LIBRARY DESTINATION ${CMAKE_SOURCE_DIR}/io)
