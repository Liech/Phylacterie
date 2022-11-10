#include "Variable.h"

#include "llvm/IR/Value.h"

namespace PLang
{
  VariableExprAST::VariableExprAST(const std::string& Name) 
    :
    Name(Name) {
  }

  llvm::Value* VariableExprAST::codegen() {
    return nullptr;
  }
}