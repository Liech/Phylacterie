#include "Context.h"

#include "AST/Expression.h"

#include "llvm/IR/LLVMContext.h"
#include "llvm/IR/IRBuilder.h"
#include "llvm/IR/Module.h"

namespace PLang {
  Context::Context() {
    context = std::make_unique<llvm::LLVMContext>();
    builder = std::make_unique<llvm::IRBuilder<>>(*context);
    mod = std::make_unique<llvm::Module>("my cool jit", *context);
  }

  llvm::Value* Context::LogErrorV(const char* Str) {
    LogError(Str);
    return nullptr;
  }

  std::unique_ptr<Expression> Context::LogError(const char* Str) {
    fprintf(stderr, "Error: %s\n", Str);
    return nullptr;
  }
}