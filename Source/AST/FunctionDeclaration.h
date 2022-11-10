#pragma once

#include <vector>
#include <string>

#include "Expression.h"

namespace PLang
{
  class FunctionDeclaration {
  public:
    FunctionDeclaration(const std::string& Name, std::vector<std::string> Args);

    const std::string& getName() const;

  private:
    std::string Name;
    std::vector<std::string> Args;
  };
}