#pragma once

#include <vector>
#include <string>

#include "Expression.h"

namespace llvm {
  class Value;
  class Function;
}

namespace PLang
{
  class FunctionDeclaration {
  public:
    FunctionDeclaration(const std::string& Name, std::vector<std::string> Args);

    const std::string& getName() const;

    llvm::Function* codegen(Context& context);
  private:
    std::string Name;
    std::vector<std::string> Args;
  };
}