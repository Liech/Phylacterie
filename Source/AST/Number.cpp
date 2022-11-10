#include "Number.h"

#include "llvm/IR/Value.h"

namespace PLang
{
  NumberExprAST::NumberExprAST(double Val) 
    :
    Val(Val) {
  }

  llvm::Value* NumberExprAST::codegen() {
    return nullptr;
  }
}