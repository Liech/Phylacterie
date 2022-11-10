#include "Binary.h"

#include "llvm/IR/Value.h"

namespace PLang
{
  Binary::Binary(char Op, std::unique_ptr<PLang::Expression> LHS, std::unique_ptr<PLang::Expression> RHS)
    :
    Op(Op), 
    LHS(std::move(LHS)),
    RHS(std::move(RHS)) {
  }

  llvm::Value* Binary::codegen() {
    return nullptr;
  }
}