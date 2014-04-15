set(lib_SRC
  kopftracer2011.cpp)

add_definitions(-Wall
    -Wextra
    -Wsequence-point
    -Wnarrowing
# The two warnings below are disabled because lib2geom will generate a lot of
# non-libdepixelize related warnings
#    -Wpedantic
#    -Weffc++
)

link_directories(
  ${GDKMM_LIBRARY_DIRS}
  ${2GEOM_LIBRARY_DIRS})

include_directories(
  ${GDKMM_INCLUDE_DIRS}
  ${2GEOM_INCLUDE_DIRS})

add_library(${PROJECT_NAME}
  ${lib_SRC})

target_link_libraries(${PROJECT_NAME}
  ${GDKMM_LIBRARIES}
  ${2GEOM_LIBRARIES})

# Configure options
option(BUILD_BINARIES
  "Generate binaries (will require popt)" ON
)
option(OUTPUT_PROFILE_INFO
  "Instructs libdepixelize to output profile info to the standard error output" OFF
)

if(BUILD_BINARIES)
  add_subdirectory(depixelize-kopf2011)
endif(BUILD_BINARIES)

if(OUTPUT_PROFILE_INFO)
  add_definitions(-DLIBDEPIXELIZE_PROFILE_KOPF2011)
endif(OUTPUT_PROFILE_INFO)
