#include "Context.h"

#include "AST/Expression.h"

#include "llvm/IR/LLVMContext.h"
#include "llvm/IR/IRBuilder.h"
#include "llvm/IR/Module.h"
#include "llvm/IR/LegacyPassManager.h"
#include "llvm/Support/TargetSelect.h"
#include "llvm/Target/TargetMachine.h"
#include "llvm/Transforms/InstCombine/InstCombine.h"
#include "llvm/Transforms/Scalar.h"
#include "llvm/Transforms/Scalar/GVN.h"

namespace PLang {
  Context::Context() {
    context = std::make_unique<llvm::LLVMContext>();
    builder = std::make_unique<llvm::IRBuilder<>>(*context);
    mod = std::make_unique<llvm::Module>("my cool jit", *context);

    fpm = std::make_unique<llvm::legacy::FunctionPassManager>(mod.get());
    
    fpm->add(llvm::createInstructionCombiningPass());
    fpm->add(llvm::createReassociatePass());
    fpm->add(llvm::createGVNPass());
    fpm->add(llvm::createCFGSimplificationPass());

    fpm->doInitialization();
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