# - Try to find the directory in which the kdewin32 library and other win32 related libraries lives
# 
# Once done this will define
#
#  KDEWIN32_FOUND - system has KDEWIN32
#  KDEWIN32_INCLUDES - the KDEWIN32 include directories
#  KDEWIN32_LIBRARIES - The libraries needed to use KDEWIN32
#
# Copyright (c) 2006, Alexander Neundorf, <neundorf@kde.org>
#
# Redistribution and use is allowed according to the terms of the BSD license.
# For details see the accompanying COPYING-CMAKE-SCRIPTS file.


if (WIN32)

  if (NOT KDEWIN32_DIR)
    if(NOT QT4_FOUND)
      find_package(Qt4 REQUIRED)
    endif(NOT QT4_FOUND)

    # check for enviroment variable first
    file(TO_CMAKE_PATH "$ENV{KDEWIN32_DIR}" KDEWIN32_DIR)

    # then check default installation dir
    if (NOT KDEWIN32_DIR)
      file(TO_CMAKE_PATH "$ENV{PROGRAMFILES}" _progFiles)
      find_file(KDEWIN32_DIR_tmp kdewin32
        PATHS
          "${_progFiles}"
      )
      set (KDEWIN32_DIR ${KDEWIN32_DIR_tmp})
    endif (NOT KDEWIN32_DIR)
  endif (NOT KDEWIN32_DIR)

  find_path(KDEWIN32_INCLUDE_DIR winposix_export.h
    ${KDEWIN32_DIR}/include 
    ${CMAKE_INSTALL_PREFIX}/include
    ${KDEWIN32_INSTALL_PREFIX}/include
  )

  # at first find the kdewin32 library, this has to be compiled and installed before kdelibs/
  # search for kdewin32 in the default install directory for applications (default of (n)make install)

  find_library(KDEWIN32_LIBRARY_DEBUG NAMES kdewin32d
    PATHS 
      ${KDEWIN32_DIR}/lib
      ${CMAKE_INSTALL_PREFIX}/lib
      ${KDEWIN32_INSTALL_PREFIX}/lib
    NO_SYSTEM_ENVIRONMENT_PATH
  )

  find_library(KDEWIN32_LIBRARY_RELEASE NAMES kdewin32
    PATHS 
      ${KDEWIN32_DIR}/lib
      ${CMAKE_INSTALL_PREFIX}/lib
      ${KDEWIN32_INSTALL_PREFIX}/lib
    NO_SYSTEM_ENVIRONMENT_PATH
  )
  
  # msvc makes a difference between debug and release
  if(MSVC)
    find_library(KDEWIN32_LIBRARY_DEBUG NAMES kdewin32d
      PATHS 
        ${KDEWIN32_DIR}/lib 
        ${CMAKE_INSTALL_PREFIX}/lib
      NO_SYSTEM_ENVIRONMENT_PATH
    )
    if(MSVC_IDE)
      # the ide needs the debug and release version
      if( NOT KDEWIN32_LIBRARY_DEBUG OR NOT KDEWIN32_LIBRARY_RELEASE)
        message(FATAL_ERROR "\nCould NOT find the debug AND release version of the KDEWIN32 library.\nYou need to have both to use MSVC projects.\nPlease build and install both kdelibs/win/ libraries first.\n")
      endif( NOT KDEWIN32_LIBRARY_DEBUG OR NOT KDEWIN32_LIBRARY_RELEASE)
      SET(KDEWIN32_LIBRARY optimized ${KDEWIN32_LIBRARY_RELEASE} debug ${KDEWIN32_LIBRARY_DEBUG})
    else(MSVC_IDE)
      string(TOLOWER ${CMAKE_BUILD_TYPE} CMAKE_BUILD_TYPE_TOLOWER)
      if(CMAKE_BUILD_TYPE_TOLOWER MATCHES debug)
        set(KDEWIN32_LIBRARY ${KDEWIN32_LIBRARY_DEBUG})
      else(CMAKE_BUILD_TYPE_TOLOWER MATCHES debug)
        set(KDEWIN32_LIBRARY ${KDEWIN32_LIBRARY_RELEASE})
      endif(CMAKE_BUILD_TYPE_TOLOWER MATCHES debug)
    endif(MSVC_IDE) 
  else(MSVC)
    if(KDEWIN32_LIBRARY_RELEASE)
	  set(KDEWIN32_LIBRARY ${KDEWIN32_LIBRARY_RELEASE})
	else(KDEWIN32_LIBRARY_RELEASE)
	  set(KDEWIN32_LIBRARY ${KDEWIN32_LIBRARY_DEBUG})
	endif(KDEWIN32_LIBRARY_RELEASE)
  endif(MSVC)

  # kdelibs/win/ has to be built before the rest of kdelibs/
  # eventually it will be moved out from kdelibs/
  if (KDEWIN32_LIBRARY AND KDEWIN32_INCLUDE_DIR)
    set(KDEWIN32_FOUND TRUE)
    # add needed system libs
    set(KDEWIN32_LIBRARIES ${KDEWIN32_LIBRARY} user32 shell32 ws2_32)

    if (MINGW)
      #mingw compiler
      set(KDEWIN32_INCLUDES ${KDEWIN32_INCLUDE_DIR} ${KDEWIN32_INCLUDE_DIR}/mingw ${QT_INCLUDES})
    else (MINGW)
      # msvc compiler
      # add the MS SDK include directory if available
      file(TO_CMAKE_PATH "$ENV{MSSDK}" MSSDK_DIR)
      set(KDEWIN32_INCLUDES ${KDEWIN32_INCLUDE_DIR} ${KDEWIN32_INCLUDE_DIR}/msvc  ${QT_INCLUDES} ${MSSDK_DIR})
    endif (MINGW)

  endif (KDEWIN32_LIBRARY AND KDEWIN32_INCLUDE_DIR)

  if (KDEWIN32_FOUND)
    if (NOT KDEWIN32_FIND_QUIETLY)
      message(STATUS "Found KDEWIN32: ${KDEWIN32_LIBRARY}")
    endif (NOT KDEWIN32_FIND_QUIETLY)
  else (KDEWIN32_FOUND)
    if (KDEWIN32_FIND_REQUIRED)
      message(FATAL_ERROR "Could NOT find KDEWIN32 library\nPlease install it first")
    endif (KDEWIN32_FIND_REQUIRED)
  endif (KDEWIN32_FOUND)

  # add include path and library to all targets, this is required because 
  # cmake's 2.4.6 FindZLib.cmake does not use CMAKE_REQUIRED... vars
  set(CMAKE_INCLUDE_PATH ${CMAKE_INCLUDE_PATH} ${KDEWIN32_INCLUDES})
  set(CMAKE_LIBRARY_PATH ${CMAKE_LIBRARY_PATH} ${KDEWIN32_DIR}/lib)

  set(CMAKE_REQUIRED_INCLUDES ${CMAKE_REQUIRED_INCLUDES} ${KDEWIN32_INCLUDES})
  set(CMAKE_REQUIRED_LIBRARIES ${CMAKE_REQUIRED_LIBRARIES} ${KDEWIN32_LIBRARIES})

endif (WIN32)
