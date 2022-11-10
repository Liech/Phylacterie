#pragma once

#include <memory>

#include "Expression.h"

namespace PLang
{
  class BinaryExprAST : public PLang::Expression {
  public:
    BinaryExprAST(char Op, std::unique_ptr<PLang::Expression> LHS, std::unique_ptr<PLang::Expression> RHS);

    virtual llvm::Value* codegen() override;
  private:
    char Op;
    std::unique_ptr<PLang::Expression> LHS, RHS;
  };
}


