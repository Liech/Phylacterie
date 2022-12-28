#include "Binary.h"

#include "llvm/IR/Value.h"
#include "llvm/IR/LLVMContext.h"
#include "llvm/IR/Type.h"

#include "Context.h"

namespace PLang
{
  Binary::Binary(char Op, std::unique_ptr<PLang::Expression> LHS, std::unique_ptr<PLang::Expression> RHS)
    :
    Op(Op), 
    LHS(std::move(LHS)),
    RHS(std::move(RHS)) {
  }

  llvm::Value* Binary::codegen(Context& context) {
    llvm::Value* L = LHS->codegen(context);
    llvm::Value* R = RHS->codegen(context);
    if (!L || !R)
      return nullptr;

    switch (Op) {
    case '+':
      return context.builder->CreateFAdd(L, R, "addtmp");
    case '-':
      return context.builder->CreateFSub(L, R, "subtmp");
    case '*':
      return context.builder->CreateFMul(L, R, "multmp");
    case '<':
      L = context.builder->CreateFCmpULT(L, R, "cmptmp");
      // Convert bool 0/1 to double 0.0 or 1.0
      return context.builder->CreateUIToFP(L, llvm::Type::getDoubleTy(*context.context),
        "booltmp");
    default:
      return context.LogErrorV("invalid binary operator");
    }
  }
}