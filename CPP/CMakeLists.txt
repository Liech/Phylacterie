cmake_minimum_required(VERSION 3.23)
project(llvmPlayground)
include(FetchContent)

find_package(LLVM CONFIG REQUIRED)
message(STATUS "Found LLVM ${LLVM_PACKAGE_VERSION}")
message(STATUS "Using LLVMConfig.cmake in: ${LLVM_DIR}")
llvm_map_components_to_libnames(
  LLVM_LIBRARIES
  Core
  Support
  IRReader
  passes 
  orcjit
  native
  target
  orctargetprocess
  jitlink
  windowsmanifest
)

# aggressiveinstcombine all all-targets analysis asmparser asmprinter binaryformat bitreader bitstreamreader bitwriter cfguard codegen core coroutines
# coverage debuginfocodeview debuginfodwarf debuginfogsym debuginfomsf debuginfopdb demangle dlltooldriver dwarflinker dwp engine executionengine extensions
# filecheck frontendopenacc frontendopenmp fuzzmutate globalisel instcombine instrumentation interfacestub interpreter ipo irreader jitlink libdriver 
# lineeditor linker lto mc mca mcdisassembler mcjit mcparser mirparser native nativecodegen objcarcopts object objectyaml option orcjit orcshared 
# orctargetprocess passes profiledata remarks runtimedyld scalaropts selectiondag support symbolize tablegen target textapi transformutils vectorize
# windowsmanifest x86 x86asmparser x86codegen x86desc x86disassembler x86info xray

set(Source_Files
  "Source/LLVMPlayground.h"
  "Source/LLVMPlayground.cpp"
  "Source/Context.h"
  "Source/Context.cpp"
  "Source/main.cpp"
  "Source/KaleidoscopeJIT.h"
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

target_include_directories(llvmPlayground PRIVATE ${LLVM_INCLUDE_DIRS})
target_compile_definitions(llvmPlayground PRIVATE ${LLVM_DEFINITIONS})
target_link_libraries(llvmPlayground PRIVATE ${LLVM_LIBRARIES})

set_property(DIRECTORY PROPERTY VS_STARTUP_PROJECT llvmPlayground)