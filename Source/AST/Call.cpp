#include "Call.h"

#include "llvm/IR/Value.h"

namespace PLang
{
  Call::Call(const std::string& Callee, std::vector<std::unique_ptr<PLang::Expression>> Args)
    : 
    Callee(Callee),
    Args(std::move(Args)) {
  }

  llvm::Value* Call::codegen() {
    return nullptr;
  }
}