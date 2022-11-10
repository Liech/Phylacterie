#include "Call.h"

#include "llvm/IR/Value.h"

namespace PLang
{
  CallExprAST::CallExprAST(const std::string& Callee, std::vector<std::unique_ptr<PLang::Expression>> Args)
    : 
    Callee(Callee),
    Args(std::move(Args)) {
  }

  llvm::Value* CallExprAST::codegen() {
    return nullptr;
  }
}