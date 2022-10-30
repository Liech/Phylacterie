#pragma once

#include <vector>
#include <string>

#include "Expression.h"

namespace PLang
{
  class FunctionDeclaration {
    std::string Name;
    std::vector<std::string> Args;

  public:
    FunctionDeclaration(const std::string& Name, std::vector<std::string> Args)
      : Name(Name), Args(std::move(Args)) {}

    const std::string& getName() const { return Name; }
  };
}