#pragma once

#include "Expression.h"

namespace PLang
{
  class NumberExprAST : public PLang::Expression {
    double Val;

  public:
    NumberExprAST(double Val) : Val(Val) {}
  };
}


