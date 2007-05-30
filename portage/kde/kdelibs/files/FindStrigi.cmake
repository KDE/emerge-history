# - Try to find Strigi
# Once done this will define
#
#  STRIGI_FOUND - system has Strigi
#  STRIGI_INCLUDE_DIR - the Strigi include directory
#  STRIGI_STREAMANALYZER_LIBRARY - Link these to use Strigi streamanalyzer
#  STRIGI_STREAMS_LIBRARY - Link these to use Strigi streams
#  STRIGI_LIBRARIES - Link these to use both Strigi libraries



if (WIN32)
  file(TO_CMAKE_PATH "$ENV{PROGRAMFILES}" _program_FILES_DIR)
endif(WIN32)

FIND_PATH(STRIGI_INCLUDE_DIR strigi/streamanalyzer.h
  PATHS
  $ENV{STRIGI_HOME}/include
  ${INCLUDE_INSTALL_DIR}
  ${_program_FILES_DIR}/strigi/include
  ${STRIGI_INSTALL_PREFIX}/include
)
FIND_LIBRARY(STRIGI_STREAMANALYZER_LIBRARY NAMES streamanalyzer
  PATHS
  $ENV{STRIGI_HOME}/lib
  ${LIB_INSTALL_DIR}
  ${_program_FILES_DIR}/strigi/lib
  ${STRIGI_INSTALL_PREFIX}/lib
)
FIND_LIBRARY(STRIGI_STREAMS_LIBRARY NAMES streams
  PATHS
  $ENV{STRIGI_HOME}/lib
  ${LIB_INSTALL_DIR}
  ${_program_FILES_DIR}/strigi/lib
  ${STRIGI_INSTALL_PREFIX}/lib
)

# for compatibility, remove ASAP (next BC monday), Alex
SET(STREAMANALYZER_LIBRARY ${STRIGI_STREAMANALYZER_LIBRARY} )
SET(STREAMS_LIBRARY ${STRIGI_STREAMS_LIBRARY})

IF(STRIGI_INCLUDE_DIR AND STRIGI_STREAMANALYZER_LIBRARY AND STRIGI_STREAMS_LIBRARY)
   SET(STRIGI_FOUND TRUE)
ENDIF(STRIGI_INCLUDE_DIR AND STRIGI_STREAMANALYZER_LIBRARY AND STRIGI_STREAMS_LIBRARY)

IF(STRIGI_FOUND)
  SET(STRIGI_LIBRARIES ${STRIGI_STREAMANALYZER_LIBRARY} ${STRIGI_STREAMS_LIBRARY})
  IF(NOT Strigi_FIND_QUIETLY)
    MESSAGE(STATUS "Found Strigi: ${STRIGI_STREAMANALYZER_LIBRARY}")
    MESSAGE(STATUS "Found Strigi: ${STRIGI_STREAMS_LIBRARY}")
    MESSAGE(STATUS "Make sure Strigi is a recent SVN version!")
    MESSAGE(STATUS "** svn://anonsvn.kde.org/home/kde/trunk/kdesupport/strigi")
  ENDIF(NOT Strigi_FIND_QUIETLY)
ELSE(STRIGI_FOUND)
  IF(Strigi_FIND_REQUIRED)
    MESSAGE(FATAL_ERROR "Could not find Strigi")
  ENDIF(Strigi_FIND_REQUIRED)
ENDIF(STRIGI_FOUND)

