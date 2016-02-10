FIND_PATH(THE_BOUNTY_INCLUDEDIR NAMES interface/yafrayinterface.h
    HINTS
    ${THE_BOUNTY_SOURCE_DIR}/include
    /usr/local/include
    /usr/include
)

FIND_PATH(THE_BOUNTY_BUILDDIR NAMES yaf_revision.h
    HINTS
    ${THE_BOUNTY_SOURCE_DIR}/build
    /usr/local/include
    /usr/include
)

FIND_LIBRARY(THE_BOUNTY_LIBS
    NAMES
        libyafarayplugin.so
        libyafarayplugin.dll
        yafarayplugin.dll
    HINTS
        /usr/local/lib
        /usr/local/bin
        /usr/lib
        /usr/bin
        ${CMAKE_SOURCE_DIR}/bin
)
IF(THE_BOUNTY_INCLUDEDIR AND THE_BOUNTY_LIBS)
    SET(THE_BOUNTY_INCLUDE_DIRS ${THE_BOUNTY_INCLUDEDIR}
        ${THE_BOUNTY_BUILDDIR})
    MESSAGE(STATUS "TheBounty found: ${THE_BOUNTY_INCLUDEDIR}")
    SET(THE_BOUNTY_FOUND TRUE)
ELSE()
    MESSAGE(FATAL_ERROR "TheBounty NOT found")
    SET(THE_BOUNTY_FOUND FALSE)
ENDIF()
