#pragma once

#include <string>

#include "Expression.h"

namespace PLang
{
  class VariableExprAST : public PLang::Expression {
    std::string Name;

  public:
    VariableExprAST(const std::string& Name) : Name(Name) {}
  };
}


