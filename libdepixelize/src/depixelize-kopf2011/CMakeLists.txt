project(depixelize-kopf2011)

pkg_check_modules(POPT REQUIRED popt)

set(depixelize_SRC
  main.cpp)

link_directories(${POPT_LIBRARY_DIRS})

include_directories(${POPT_INCLUDE_DIRS})

add_executable(${PROJECT_NAME}
  ${depixelize_SRC})

target_link_libraries(${PROJECT_NAME}
  ${GDKMM_LIBRARIES}
  ${CMAKE_PROJECT_NAME}
  ${POPT_LIBRARIES})

# Install info
install(TARGETS "${PROJECT_NAME}"
    DESTINATION "bin"
)
