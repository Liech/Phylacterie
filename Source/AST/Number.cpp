#include "Number.h"

#include "llvm/IR/Value.h"

namespace PLang
{
  Number::Number(double Val) 
    :
    Val(Val) {
  }

  llvm::Value* Number::codegen() {
    return nullptr;
  }
}