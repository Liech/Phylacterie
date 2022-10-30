cmake_minimum_required(VERSION 2.8...3.23)
project(llvmPlayground)
include(FetchContent)

find_package(LLVM CONFIG REQUIRED)



set(Header_Files
  "LLVMPlayground.h"
)
source_group("Header Files" FILES ${Header_Files})

set(Source_Files
    "main.cpp"
    "LLVMPlayground.cpp"
)
source_group("Source Files" FILES ${Source_Files})

set(ALL_FILES
    ${Header_Files}
    ${Source_Files}
)


add_executable(llvmPlayground ${ALL_FILES})
set_property(TARGET llvmPlayground PROPERTY CXX_STANDARD 20)

# LLVM
list(APPEND CMAKE_MODULE_PATH "${LLVM_CMAKE_DIR}")
include(HandleLLVMOptions)
add_definitions(${LLVM_DEFINITIONS})
target_include_directories(llvmPlayground PRIVATE ${LLVM_INCLUDE_DIRS})
llvm_map_components_to_libnames(llvm_libs Support Core IRReader)
target_link_libraries(llvmPlayground PRIVATE ${llvm_libs})


set_property(DIRECTORY PROPERTY VS_STARTUP_PROJECT llvmPlayground)