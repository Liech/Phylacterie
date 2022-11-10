#include "Function.h"

#include "llvm/IR/Value.h"

namespace PLang
{
  Function::Function(std::unique_ptr<FunctionDeclaration> Proto, std::unique_ptr<PLang::Expression> Body)
    : 
    Proto(std::move(Proto)),
    Body(std::move(Body)) {
  }
}