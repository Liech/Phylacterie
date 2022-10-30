#pragma once

#include <memory>

#include "Expression.h"

namespace PLang
{
  class BinaryExprAST : public PLang::Expression {
    char Op;
    std::unique_ptr<PLang::Expression> LHS, RHS;

  public:
    BinaryExprAST(char Op, std::unique_ptr<PLang::Expression> LHS,
      std::unique_ptr<PLang::Expression> RHS)
      : Op(Op), LHS(std::move(LHS)), RHS(std::move(RHS)) {}
  };
}


