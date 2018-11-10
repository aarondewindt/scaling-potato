cmake_minimum_required(VERSION 3.6)
project(scaling_potato)

set(CMAKE_CXX_STANDARD 11)

# Experimental code
set(EXP_SOURCE_FILES exp/main.cpp)
add_executable(exp ${EXP_SOURCE_FILES} ${PYTHON_FILES})

# Scaling potato code
set(SP_PYTHON_FILES
        scaling_potato/__init__.py
        scaling_potato/pid_control.py
        scaling_potato/quadcopter.py
        scaling_potato/world.py)

set(SP_SOURCES
        scaling_potato/scaling_potato_c/cpp_code/test_opencv.cpp scaling_potato/scaling_potato_c/cpp_code/test_opencv.h scaling_potato/scaling_potato_c/cpp_code/Camera.cpp scaling_potato/scaling_potato_c/cpp_code/Camera.h)

add_executable(scaling_potato ${SP_SOURCES} ${PYTHON_FILES})

find_package( OpenCV REQUIRED )
target_link_libraries(exp ${OpenCV_LIBS} )
