# Faster register complete binaries for ndt

cmake_minimum_required(VERSION 3.18)

project("nameless-dt-binaries"
    VERSION 1.0
    LANGUAGES CXX
    DESCRIPTION "Faster register complete binaries for nameless-deploy-tools."
    HOMEPAGE_URL "https://github.com/NitorCreations/nameless-deploy-tools"
)

set(CMAKE_CXX_STANDARD 20)

# Export compile commands for clang-tidy
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

message(STATUS "CMake version: ${CMAKE_VERSION}")
message(STATUS "CMake source dir: ${CMAKE_SOURCE_DIR}")

include_directories(n_utils)

add_executable(nameless-dt-register-complete
    n_utils/nameless-dt-register-complete.cpp
)

add_executable(nameless-dt-print-aws-profiles
    n_utils/nameless-dt-print-aws-profiles.cpp
)

if (MSVC)
    # https://docs.microsoft.com/en-us/cpp/build/reference/permissive-standards-conformance
    target_compile_options(nameless-dt-register-complete PRIVATE
        /W4 /permissive-
    )
    target_compile_options(nameless-dt-print-aws-profiles PRIVATE
        /W4 /permissive-
    )
else()
    target_compile_options(nameless-dt-register-complete PRIVATE
        -Wall -Wextra -pedantic
    )
    target_compile_options(nameless-dt-print-aws-profiles PRIVATE
        -Wall -Wextra -pedantic
    )
endif()
