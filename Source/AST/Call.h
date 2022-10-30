#pragma once

#include <vector>
#include <memory>
#include <string>

#include "Expression.h"

namespace PLang
{
  class CallExprAST : public PLang::Expression {
    std::string Callee;
    std::vector<std::unique_ptr<PLang::Expression>> Args;

  public:
    CallExprAST(const std::string& Callee,
      std::vector<std::unique_ptr<PLang::Expression>> Args)
      : Callee(Callee), Args(std::move(Args)) {}
  };
}