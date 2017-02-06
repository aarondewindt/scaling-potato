cmake_minimum_required(VERSION 3.6)
project(exp)

set(CMAKE_CXX_STANDARD 11)

set(SOURCE_FILES exp/main.cpp)
set(PYTHON_FILES scaling_potato/__init__.py)

add_executable(exp ${SOURCE_FILES} ${PYTHON_FILES})

find_package( OpenCV REQUIRED )
target_link_libraries(exp ${OpenCV_LIBS} )

