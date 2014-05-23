project(depixelize)

cmake_minimum_required(VERSION 2.8)
find_package(PkgConfig REQUIRED)

pkg_check_modules(GDKMM REQUIRED gdkmm-2.4)
pkg_check_modules(2GEOM REQUIRED 2geom)

add_subdirectory(src)
