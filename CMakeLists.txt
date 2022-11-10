cmake_minimum_required(VERSION 2.8...3.23)
project(llvmPlayground)
include(FetchContent)

find_package(LLVM CONFIG REQUIRED)



set(Source_Files
  "Source/LLVMPlayground.h"
  "Source/LLVMPlayground.cpp"
  "Source/Context.h"
  "Source/Context.cpp"
  "Source/main.cpp"
)
source_group("Source" FILES ${Source_Files})

set(AST_Files
  "Source/AST/Expression.h"
  "Source/AST/Expression.cpp"
  "Source/AST/Number.h"
  "Source/AST/Number.cpp"
  "Source/AST/Expression.h"
  "Source/AST/Expression.cpp"
  "Source/AST/Variable.h"
  "Source/AST/Variable.cpp"
  "Source/AST/Binary.h"
  "Source/AST/Binary.cpp"
  "Source/AST/Call.h"
  "Source/AST/Call.cpp"
  "Source/AST/Function.h"
  "Source/AST/Function.cpp"
  "Source/AST/FunctionDeclaration.h"
  "Source/AST/FunctionDeclaration.cpp"
)
source_group("Source/AST" FILES ${AST_Files})

set(Parser_Files
  "Source/Parser/Parser.h"
  "Source/Parser/Parser.cpp"
  "Source/Parser/Lexer.h"
  "Source/Parser/Lexer.cpp"
  "Source/Parser/Token.h"
  "Source/Parser/Token.cpp"
)
source_group("Source/Parser" FILES ${Parser_Files})


set(ALL_FILES
    ${Source_Files}
    ${AST_Files}
    ${Parser_Files}
)

include_directories("Source")
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