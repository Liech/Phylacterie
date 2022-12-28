#pragma once

#include <vector>
#include <memory>
#include <string>

#include "FunctionDeclaration.h"

namespace llvm {
  class Value;
  class Function;
}

namespace PLang
{
  class Function {
  public:
    Function(std::unique_ptr<FunctionDeclaration> Proto, std::unique_ptr<PLang::Expression> Body);

    llvm::Function* codegen(Context& context);
  private:
    std::unique_ptr<FunctionDeclaration> Proto;
    std::unique_ptr<PLang::Expression> Body;
  };
}