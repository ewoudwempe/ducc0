cmake_minimum_required(VERSION 3.20)
project(ducc)

add_library(ducc)
set(SOURCES 
  healpix/healpix_base.cc
  healpix/healpix_tables.cc
  infra/communication.cc
  infra/mav.cc
  infra/string_utils.cc
  infra/system.cc
  infra/threading.cc
  infra/types.cc
  math/geom_utils.cc
  math/gl_integrator.cc
  math/gridding_kernel.cc
  math/pointing.cc
  math/space_filling.cc
  sht/sht.cc
  wgridder/wgridder.cc
)
list(TRANSFORM SOURCES PREPEND ${CMAKE_CURRENT_SOURCE_DIR}/src/ducc0/)
target_sources(ducc PRIVATE ${SOURCES})
target_include_directories(ducc PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/src>
  $<INSTALL_INTERFACE:src>  
)
