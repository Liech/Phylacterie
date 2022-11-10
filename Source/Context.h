#pragma once

#include <memory>
#include <map>
#include <string>

#include "llvm/IR/IRBuilder.h"

namespace llvm {
  class LLVMContext;
  class Value;
  class Module;
}

namespace PLang {
  class Expression;

  class Context {
  public:
    Context();

    llvm::Value* LogErrorV(const char* Str);

    std::unique_ptr<llvm::LLVMContext > context;
    std::unique_ptr<llvm::IRBuilder<>>  builder;
    std::unique_ptr<llvm::Module>       mod;
    std::map<std::string, llvm::Value*> namedValues;
  private:
    std::unique_ptr<Expression> LogError(const char* Str);
  };
}