#pragma once

#include "Expression.h"

namespace PLang
{
  class Number : public PLang::Expression 
  {
  public:
    Number(double Val);

    virtual llvm::Value* codegen() override;

  private:
    double Val;
  };
}


