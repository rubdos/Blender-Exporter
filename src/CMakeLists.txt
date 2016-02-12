set(TBY_BLENDER_SRC
    blender/python_class.cpp
    blender/blender_render_settings.cpp
    blender/blender_image_settings.cpp
    blender/blender_camera.cpp
    blender/blender_bounty.cpp
    blender/blender_object.cpp
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

target_link_libraries(tby_blender
    tby_blender_backend
    ${PYTHON_LIBRARIES}
    ${THE_BOUNTY_LIBS})

set_target_properties(tby_blender PROPERTIES PREFIX "")
if(WIN32)
    set_target_properties(tby_blender
      PROPERTIES
      IMPORT_SUFFIX ".pyd"
      IMPORT_PREFIX ""
      PREFIX "")
endif(WIN32)

install(TARGETS tby_blender
        LIBRARY DESTINATION ${CMAKE_SOURCE_DIR}/bin
        RUNTIME DESTINATION ${CMAKE_SOURCE_DIR}/bin)
