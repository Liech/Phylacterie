cmake_minimum_required(VERSION 2.8...3.23)
project(llvmPlayground)
include(FetchContent)

find_package(LLVM CONFIG REQUIRED)



set(Source_Files
  "Source/LLVMPlayground.h"
  "Source/Lexer/Token.h"
  "Source/main.cpp"
  "Source/LLVMPlayground.cpp"
  "Source/Lexer/Token.cpp"
)
source_group("Source" FILES ${Source_Files})

set(AST_Files
  "Source/AST/Expression.h"
  "Source/AST/Number.h"
  "Source/AST/Expression.h"
  "Source/AST/Variable.h"
  "Source/AST/Binary.h"
  "Source/AST/Call.h"
  "Source/AST/Function.h"
  "Source/AST/FunctionDeclaration.h"
)
source_group("Source/AST" FILES ${AST_Files})


set(ALL_FILES
    ${Source_Files}
    ${AST_Files}
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