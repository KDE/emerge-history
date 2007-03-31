# - Find zlib
# Find the native ZLIB includes and library
#
#  ZLIB_INCLUDE_DIR - where to find zlib.h, etc.
#  ZLIB_LIBRARIES   - List of libraries when using zlib.
#  ZLIB_FOUND       - True if zlib found.


IF (ZLIB_INCLUDE_DIR)
  # Already in cache, be silent
  SET(ZLIB_FIND_QUIETLY TRUE)
ENDIF (ZLIB_INCLUDE_DIR)

FIND_PATH(ZLIB_INCLUDE_DIR zlib.h
  /usr/local/include
  /usr/include
  ${WIN32LIBS_INSTALL_PREFIX}/include
)

SET(ZLIB_NAMES z zlib zdll)
FIND_LIBRARY(ZLIB_LIBRARY
  NAMES ${ZLIB_NAMES}
  PATHS /usr/lib /usr/local/lib
  ${WIN32LIBS_INSTALL_PREFIX}/lib
)

IF (ZLIB_INCLUDE_DIR AND ZLIB_LIBRARY)
   SET(ZLIB_FOUND TRUE)
    SET( ZLIB_LIBRARIES ${ZLIB_LIBRARY} )
ELSE (ZLIB_INCLUDE_DIR AND ZLIB_LIBRARY)
   SET(ZLIB_FOUND FALSE)
   SET( ZLIB_LIBRARIES )
ENDIF (ZLIB_INCLUDE_DIR AND ZLIB_LIBRARY)

IF (ZLIB_FOUND)
   IF (NOT ZLIB_FIND_QUIETLY)
      MESSAGE(STATUS "Found ZLIB: ${ZLIB_LIBRARY}")
   ENDIF (NOT ZLIB_FIND_QUIETLY)
ELSE (ZLIB_FOUND)
   IF (ZLIB_FIND_REQUIRED)
      MESSAGE(STATUS "Looked for Z libraries named ${ZLIBS_NAMES}.")
      MESSAGE(FATAL_ERROR "Could NOT find z library")
   ENDIF (ZLIB_FIND_REQUIRED)
ENDIF (ZLIB_FOUND)

MARK_AS_ADVANCED(
  ZLIB_LIBRARY
  ZLIB_INCLUDE_DIR
  )
