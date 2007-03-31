# - Try to find BZip2
# Once done this will define
#
#  BZIP2_FOUND - system has BZip2
#  BZIP2_INCLUDE_DIR - the BZip2 include directory
#  BZIP2_LIBRARIES - Link these to use BZip2
#  BZIP2_DEFINITIONS - Compiler switches required for using BZip2
#  BZIP2_NEED_PREFIX - this is set if the functions are prefixed with BZ2_

# Copyright (c) 2006, Alexander Neundorf, <neundorf@kde.org>
#
# Redistribution and use is allowed according to the terms of the BSD license.
# For details see the accompanying COPYING-CMAKE-SCRIPTS file.


IF (BZIP2_INCLUDE_DIR AND BZIP2_LIBRARIES)
    SET(BZip2_FIND_QUIETLY TRUE)
ENDIF (BZIP2_INCLUDE_DIR AND BZIP2_LIBRARIES)

FIND_PATH(BZIP2_INCLUDE_DIR bzlib.h
    ${WIN32LIBS_INSTALL_PREFIX}/include
)

FIND_LIBRARY(BZIP2_LIBRARIES NAMES bz2 bzip2
    PATHS ${WIN32LIBS_INSTALL_PREFIX}/bin
)

IF (BZIP2_INCLUDE_DIR AND BZIP2_LIBRARIES)
   SET(BZIP2_FOUND TRUE)
   INCLUDE(CheckLibraryExists)
   CHECK_LIBRARY_EXISTS(${BZIP2_LIBRARIES} BZ2_bzCompressInit "" BZIP2_NEED_PREFIX)
ELSE (BZIP2_INCLUDE_DIR AND BZIP2_LIBRARIES)
   SET(BZIP2_FOUND FALSE)
ENDIF (BZIP2_INCLUDE_DIR AND BZIP2_LIBRARIES)

IF (BZIP2_FOUND)
  IF (NOT BZip2_FIND_QUIETLY)
    MESSAGE(STATUS "Found BZip2: ${BZIP2_LIBRARIES}")
  ENDIF (NOT BZip2_FIND_QUIETLY)
ELSE (BZIP2_FOUND)
  IF (BZip2_FIND_REQUIRED)
    MESSAGE(FATAL_ERROR "Could NOT find BZip2. Please install libbz2-dev")
  ENDIF (BZip2_FIND_REQUIRED)
ENDIF (BZIP2_FOUND)

MARK_AS_ADVANCED(BZIP2_INCLUDE_DIR BZIP2_LIBRARIES)

