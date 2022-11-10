#pragma once

#include "Expression.h"

namespace PLang
{
  class NumberExprAST : public PLang::Expression 
  {
  public:
    NumberExprAST(double Val);

    virtual llvm::Value* codegen() override;

  private:
    double Val;
  };
}


