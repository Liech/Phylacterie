#include "Variable.h"

#include "llvm/IR/Value.h"

namespace PLang
{
  Variable::Variable(const std::string& Name) 
    :
    Name(Name) {
  }

  llvm::Value* Variable::codegen() {
    return nullptr;
  }
}