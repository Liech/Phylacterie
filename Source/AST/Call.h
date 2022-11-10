#pragma once

#include <vector>
#include <memory>
#include <string>

#include "Expression.h"

namespace PLang
{
  class Call : public PLang::Expression {
  public:
    Call(const std::string& Callee, std::vector<std::unique_ptr<PLang::Expression>> Args);

    virtual llvm::Value* codegen() override;
  private:
    std::string Callee;
    std::vector<std::unique_ptr<PLang::Expression>> Args;
  };
}