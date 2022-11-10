#pragma once

#include <vector>
#include <memory>
#include <string>

#include "Expression.h"

namespace PLang
{
  class CallExprAST : public PLang::Expression {
  public:
    CallExprAST(const std::string& Callee, std::vector<std::unique_ptr<PLang::Expression>> Args);

    virtual llvm::Value* codegen() override;
  private:
    std::string Callee;
    std::vector<std::unique_ptr<PLang::Expression>> Args;
  };
}