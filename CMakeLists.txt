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


set_property(DIRECTORY PROPERTY VS_STARTUP_PROJECT llvmPlayground)