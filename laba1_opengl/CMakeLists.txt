cmake_minimum_required(VERSION 3.16)
project(laba1_opengl)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_subdirectory(external)

find_package(OpenGL REQUIRED)

add_executable(${PROJECT_NAME} src/main.cpp
        src/main.cpp)

target_link_libraries(${PROJECT_NAME}
        PRIVATE
        OpenGL::GL
        glfw
        glad
        glm
)