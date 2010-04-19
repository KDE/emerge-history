#
# check mingw compiler version
# 
# Copyright (c) 2010, Ralf Habacker
#
# Redistribution and use is allowed according to the terms of the BSD license.
#
if (NOT MINGW32 AND NOT MINGW64)
    exec_program(
        gcc
        ARGS -dumpmachine
        OUTPUT_VARIABLE _machine
    )
    if (_machine STREQUAL mingw32)
        set (MINGW32 1)
        message(STATUS "found mingw 32 bit compiler")
    elseif (_machine STREQUAL x86_64-w64-mingw32)
        set (MINGW64 1)
        message(STATUS "found mingw 64 bit compiler")
    endif (_machine STREQUAL mingw32)
endif (NOT MINGW32 AND NOT MINGW64)
