# echo EXPORTS > libjasper.def
# nm libjasper.dll | grep " T _" | sed "s/.* T _//" >> libjasper.def
# lib /machine:i386 /def:libjasper.def
project(jasper)

find_package(jpeg REQUIRED)

set(jasper_base_SRCS
    ${CMAKE_SOURCE_DIR}/base/jas_cm.c
    ${CMAKE_SOURCE_DIR}/base/jas_debug.c
    ${CMAKE_SOURCE_DIR}/base/jas_getopt.c
    ${CMAKE_SOURCE_DIR}/base/jas_icc.c
    ${CMAKE_SOURCE_DIR}/base/jas_iccdata.c
    ${CMAKE_SOURCE_DIR}/base/jas_image.c
    ${CMAKE_SOURCE_DIR}/base/jas_init.c
    ${CMAKE_SOURCE_DIR}/base/jas_malloc.c
    ${CMAKE_SOURCE_DIR}/base/jas_seq.c
    ${CMAKE_SOURCE_DIR}/base/jas_stream.c
    ${CMAKE_SOURCE_DIR}/base/jas_string.c
    ${CMAKE_SOURCE_DIR}/base/jas_tvp.c
    ${CMAKE_SOURCE_DIR}/base/jas_version.c
)

set(jasper_bmp_SRCS
    ${CMAKE_SOURCE_DIR}/bmp/bmp_cod.c
    ${CMAKE_SOURCE_DIR}/bmp/bmp_dec.c
    ${CMAKE_SOURCE_DIR}/bmp/bmp_enc.c
)

set(jasper_jp2_SRCS
    ${CMAKE_SOURCE_DIR}/jp2/jp2_cod.c
    ${CMAKE_SOURCE_DIR}/jp2/jp2_dec.c
    ${CMAKE_SOURCE_DIR}/jp2/jp2_enc.c
)

set(jasper_jpc_SRCS
    ${CMAKE_SOURCE_DIR}/jpc/jpc_bs.c
    ${CMAKE_SOURCE_DIR}/jpc/jpc_cs.c
    ${CMAKE_SOURCE_DIR}/jpc/jpc_dec.c
    ${CMAKE_SOURCE_DIR}/jpc/jpc_enc.c
    ${CMAKE_SOURCE_DIR}/jpc/jpc_math.c
    ${CMAKE_SOURCE_DIR}/jpc/jpc_mct.c
    ${CMAKE_SOURCE_DIR}/jpc/jpc_mqcod.c
    ${CMAKE_SOURCE_DIR}/jpc/jpc_mqdec.c
    ${CMAKE_SOURCE_DIR}/jpc/jpc_mqenc.c
    ${CMAKE_SOURCE_DIR}/jpc/jpc_qmfb.c
    ${CMAKE_SOURCE_DIR}/jpc/jpc_t1cod.c
    ${CMAKE_SOURCE_DIR}/jpc/jpc_t1dec.c
    ${CMAKE_SOURCE_DIR}/jpc/jpc_t1enc.c
    ${CMAKE_SOURCE_DIR}/jpc/jpc_t2cod.c
    ${CMAKE_SOURCE_DIR}/jpc/jpc_t2dec.c
    ${CMAKE_SOURCE_DIR}/jpc/jpc_t2enc.c
    ${CMAKE_SOURCE_DIR}/jpc/jpc_tagtree.c
    ${CMAKE_SOURCE_DIR}/jpc/jpc_tsfb.c
    ${CMAKE_SOURCE_DIR}/jpc/jpc_util.c
)

set(jasper_jpg_SRCS
#    ${CMAKE_SOURCE_DIR}/jpg/jpg_dec.c
    ${CMAKE_SOURCE_DIR}/jpg/jpg_dummy.c
#    ${CMAKE_SOURCE_DIR}/jpg/jpg_enc.c
    ${CMAKE_SOURCE_DIR}/jpg/jpg_val.c
)

set(jasper_mif_SRCS
    ${CMAKE_SOURCE_DIR}/mif/mif_cod.c
)

set(jasper_pgx_SRCS
    ${CMAKE_SOURCE_DIR}/pgx/pgx_cod.c
    ${CMAKE_SOURCE_DIR}/pgx/pgx_dec.c
    ${CMAKE_SOURCE_DIR}/pgx/pgx_enc.c
)

set(jasper_pnm_SRCS
    ${CMAKE_SOURCE_DIR}/pnm/pnm_cod.c
    ${CMAKE_SOURCE_DIR}/pnm/pnm_dec.c
    ${CMAKE_SOURCE_DIR}/pnm/pnm_enc.c
)

set(jasper_ras_SRCS
    ${CMAKE_SOURCE_DIR}/ras/ras_cod.c
    ${CMAKE_SOURCE_DIR}/ras/ras_dec.c
    ${CMAKE_SOURCE_DIR}/ras/ras_enc.c
)

file(GLOB jasper_headers include/jasper/*.h)

include_directories(include ${JPEG_INCLUDE_DIR})

set(CMAKE_DEBUG_POSTFIX "d")

add_library(jasper SHARED ${jasper_base_SRCS}
                          ${jasper_bmp_SRCS}
                          ${jasper_jp2_SRCS}
                          ${jasper_jpc_SRCS}
                          ${jasper_jpg_SRCS}
                          ${jasper_mif_SRCS}
                          ${jasper_pgx_SRCS}
                          ${jasper_pnm_SRCS}
                          ${jasper_ras_SRCS}
           )

target_link_libraries(jasper ${JPEG_LIBRARY} )

install(TARGETS jasper
                RUNTIME DESTINATION bin
                LIBRARY DESTINATION lib
                ARCHIVE DESTINATION lib
)
install(FILES ${jasper_headers} DESTINATION include/jasper)
