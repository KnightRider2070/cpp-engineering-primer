cmake_minimum_required(VERSION 3.22)
project(cpp_engineering_primer LANGUAGES CXX)

# -----------------------------------------------------------------------------
# Course-owned build file. You do not need to edit this.
#
# It is written so that it still works when my-game/ is completely empty,
# which is how the course starts. As you create files, more of it switches on.
# -----------------------------------------------------------------------------

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

if(NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
    set(CMAKE_BUILD_TYPE Debug CACHE STRING "" FORCE)
endif()

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

enable_testing()

# The contract. Header-only: anyone who links this can #include <ttt/Game.hpp>.
add_library(ttt_contract INTERFACE)
target_include_directories(ttt_contract INTERFACE
    ${CMAKE_CURRENT_SOURCE_DIR}/course/include
)

# Vendored third-party headers (cpp-httplib, nlohmann/json), course-owned.
add_library(ttt_vendor INTERFACE)
target_include_directories(ttt_vendor INTERFACE
    ${CMAKE_CURRENT_SOURCE_DIR}/course/vendor
)

# --- Testing --------------------------------------------------------------
# GoogleTest is fetched here, BEFORE my-game, so that your own tests can link
# against GTest::gtest_main exactly like the course's tests do. (Stages 0-2
# have no my-game/CMakeLists.txt yet, so nothing is downloaded until you
# actually start using CMake.)
if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/my-game/CMakeLists.txt")
    include(FetchContent)
    FetchContent_Declare(
        googletest
        URL https://github.com/google/googletest/archive/refs/tags/v1.14.0.zip
        URL_HASH SHA256=1f357c27ca988c3f7c6b4bf68a9395005ac6761f034046e9dde0896e3aba00e4
        DOWNLOAD_EXTRACT_TIMESTAMP TRUE
    )
    set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
    FetchContent_MakeAvailable(googletest)
endif()

# --- Your code -----------------------------------------------------------
# Stages 1 and 2 have no CMakeLists.txt in my-game/ at all -- you compile by
# hand with g++. Configuring must still succeed, so this is guarded.
if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/my-game/CMakeLists.txt")
    add_subdirectory(my-game)
endif()

# --- Things that need your code ------------------------------------------
# These only switch on once you have created the `my_game` target (Stage 3)
# and implemented ttt::createGame() (Stage 5).
if(TARGET my_game)
    add_subdirectory(course/server)
    add_subdirectory(course/checks/contract)
endif()

# --- Course exercises -----------------------------------------------------
# Small standalone programs used by specific stages (e.g. the dangling
# reference demo at Stage 6). They never depend on your code.
add_subdirectory(course/exercises)
