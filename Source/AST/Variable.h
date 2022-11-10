#pragma once

#include <string>

#include "Expression.h"

namespace PLang
{
  class VariableExprAST : public PLang::Expression {
  public:
    VariableExprAST(const std::string& Name);

    virtual llvm::Value* codegen() override;

  private:
    std::string Name;
  };
}


