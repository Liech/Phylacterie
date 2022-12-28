#pragma once

#include <memory>
#include <map>
#include <string>

#include "llvm/IR/IRBuilder.h"

namespace llvm {
  class LLVMContext;
  class Value;
  class Module;
  namespace legacy {
    class FunctionPassManager;
  }
}

namespace PLang {
  class Expression;

  class Context {
  public:
    Context();
    virtual ~Context() = default;

    llvm::Value* LogErrorV(const char* Str);

    std::unique_ptr<llvm::LLVMContext >                context;
    std::unique_ptr<llvm::IRBuilder<>>                 builder;
    std::unique_ptr<llvm::Module>                      mod;
    std::map<std::string, llvm::Value*>                namedValues;
    std::unique_ptr<llvm::legacy::FunctionPassManager> fpm;
  private:
    std::unique_ptr<Expression> LogError(const char* Str);
  };
}