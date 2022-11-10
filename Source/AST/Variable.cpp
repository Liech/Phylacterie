#include "Variable.h"

#include "Context.h"

#include "llvm/IR/Value.h"

namespace PLang
{
  Variable::Variable(const std::string& Name) 
    :
    Name(Name) {
  }

  llvm::Value* Variable::codegen(Context& context) {
    // Look this variable up in the function.
    llvm::Value* V = context.namedValues[Name];
    if (!V)
      context.LogErrorV("Unknown variable name");
    return V;
  }
}