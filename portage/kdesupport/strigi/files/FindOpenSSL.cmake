# - Try to find the OpenSSL encryption library
# Once done this will define
#
#  OPENSSL_FOUND - system has the OpenSSL library
#  OPENSSL_INCLUDE_DIR - the OpenSSL include directory
#  OPENSSL_LIBRARIES - The libraries needed to use OpenSSL
#  OPENSSL_EAY_LIBRARIES - The additional libraries needed to use OpenSSL on windows
# Copyright (c) 2006, Alexander Neundorf, <neundorf@kde.org>
#
# Redistribution and use is allowed according to the terms of the BSD license.
# For details see the accompanying COPYING-CMAKE-SCRIPTS file.

# on win32 we additional need to link to libeay32.lib
MACRO(OPENSSL_ADD_LIB_EAY_LIBS)
   IF(MSVC)
      # /MD and /MDd are the standard values - if somone wants to use
      # others, the libnames have to change here too
      # use also eay and libeay32 in debug as fallback for openssl < 0.9.8b

      FIND_LIBRARY(LIB_EAY_DEBUG NAMES libeay32MDd eay libeay libeay32)
      FIND_LIBRARY(LIB_EAY_RELEASE NAMES libeay32MD eay libeay libeay32)

      IF(MSVC_IDE)
         IF(LIB_EAY_DEBUG AND LIB_EAY_RELEASE)
            SET(OPENSSL_EAY_LIBRARIES optimized ${LIB_EAY_RELEASE} debug ${LIB_EAY_DEBUG})
         ELSE(LIB_EAY_DEBUG AND LIB_EAY_RELEASE)
            MESSAGE(FATAL_ERROR "Could not find the debug and release version of openssl (libeay)")
         ENDIF(LIB_EAY_DEBUG AND LIB_EAY_RELEASE)
      ELSE(MSVC_IDE)
         STRING(TOLOWER ${CMAKE_BUILD_TYPE} CMAKE_BUILD_TYPE_TOLOWER)
         IF(CMAKE_BUILD_TYPE_TOLOWER MATCHES debug)
            SET(OPENSSL_EAY_LIBRARIES ${LIB_EAY_DEBUG})
         ELSE(CMAKE_BUILD_TYPE_TOLOWER MATCHES debug)
            SET(OPENSSL_EAY_LIBRARIES ${LIB_EAY_RELEASE})
         ENDIF(CMAKE_BUILD_TYPE_TOLOWER MATCHES debug)
      ENDIF(MSVC_IDE)
      MARK_AS_ADVANCED(LIB_EAY_DEBUG LIB_EAY_RELEASE)
   ELSE(MSVC)
       FIND_LIBRARY(OPENSSL_EAY_LIBRARIES NAMES eay libeay libeay32 )
   ENDIF(MSVC)
ENDMACRO(OPENSSL_ADD_LIB_EAY_LIBS)

IF(OPENSSL_LIBRARIES)
   SET(OpenSSL_FIND_QUIETLY TRUE)
ENDIF(OPENSSL_LIBRARIES)

IF(SSL_EAY_DEBUG AND SSL_EAY_RELEASE)
   SET(LIB_FOUND 1)
ENDIF(SSL_EAY_DEBUG AND SSL_EAY_RELEASE)

FIND_PATH(OPENSSL_INCLUDE_DIR openssl/ssl.h
   ${WIN32LIBS_INSTALL_PREFIX}/include
)

IF(WIN32 AND MSVC)
   # /MD and /MDd are the standard values - if somone wants to use
   # others, the libnames have to change here too
   # use also ssl and ssleay32 in debug as fallback for openssl < 0.9.8b

   FIND_LIBRARY(SSL_EAY_DEBUG NAMES ssleay32MDd ssl ssleay32)
   FIND_LIBRARY(SSL_EAY_RELEASE NAMES ssleay32MD ssl ssleay32)

   IF(MSVC_IDE)
      IF(SSL_EAY_DEBUG AND SSL_EAY_RELEASE)
         SET(OPENSSL_LIBRARIES optimized ${SSL_EAY_RELEASE} debug ${SSL_EAY_DEBUG})
      ELSE(SSL_EAY_DEBUG AND SSL_EAY_RELEASE)
         MESSAGE(FATAL_ERROR "Could not find the debug and release version of openssl")
      ENDIF(SSL_EAY_DEBUG AND SSL_EAY_RELEASE)
   ELSE(MSVC_IDE)
      STRING(TOLOWER ${CMAKE_BUILD_TYPE} CMAKE_BUILD_TYPE_TOLOWER)
      IF(CMAKE_BUILD_TYPE_TOLOWER MATCHES debug)
         SET(OPENSSL_LIBRARIES ${SSL_EAY_DEBUG})
      ELSE(CMAKE_BUILD_TYPE_TOLOWER MATCHES debug)
         SET(OPENSSL_LIBRARIES ${SSL_EAY_RELEASE})
      ENDIF(CMAKE_BUILD_TYPE_TOLOWER MATCHES debug)
   ENDIF(MSVC_IDE)
   MARK_AS_ADVANCED(SSL_EAY_DEBUG SSL_EAY_RELEASE)
ELSE(WIN32 AND MSVC)

   FIND_LIBRARY(OPENSSL_LIBRARIES NAMES ssl ssleay32 ssleay32MD
      PATHS ${WIN32LIBS_INSTALL_PREFIX}/bin
   )

ENDIF(WIN32 AND MSVC)

IF(WIN32)
   OPENSSL_ADD_LIB_EAY_LIBS()
   IF(OPENSSL_INCLUDE_DIR AND OPENSSL_LIBRARIES AND OPENSSL_EAY_LIBRARIES)
      SET(OPENSSL_FOUND TRUE)
   ELSE(OPENSSL_INCLUDE_DIR AND OPENSSL_LIBRARIES AND OPENSSL_EAY_LIBRARIES)
      SET(OPENSSL_FOUND FALSE)
   ENDIF (OPENSSL_INCLUDE_DIR AND OPENSSL_LIBRARIES AND OPENSSL_EAY_LIBRARIES)
ELSE(WIN32)
   IF(OPENSSL_INCLUDE_DIR AND OPENSSL_LIBRARIES)
      SET(OPENSSL_FOUND TRUE)
   ELSE(OPENSSL_INCLUDE_DIR AND OPENSSL_LIBRARIES)
      SET(OPENSSL_FOUND FALSE)
   ENDIF (OPENSSL_INCLUDE_DIR AND OPENSSL_LIBRARIES)
ENDIF(WIN32)

IF (OPENSSL_FOUND)
   IF (NOT OpenSSL_FIND_QUIETLY)
      MESSAGE(STATUS "Found OpenSSL: ${OPENSSL_LIBRARIES}")
   ENDIF (NOT OpenSSL_FIND_QUIETLY)
ELSE (OPENSSL_FOUND)
   IF (OpenSSL_FIND_REQUIRED)
      MESSAGE(FATAL_ERROR "Could NOT find OpenSSL")
   ENDIF (OpenSSL_FIND_REQUIRED)
ENDIF (OPENSSL_FOUND)

MARK_AS_ADVANCED(OPENSSL_INCLUDE_DIR OPENSSL_LIBRARIES)

