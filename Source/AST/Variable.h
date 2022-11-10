#pragma once

#include <string>

#include "Expression.h"

namespace PLang
{
  class Variable : public PLang::Expression {
  public:
    Variable(const std::string& Name);

    virtual llvm::Value* codegen(Context& context) override;

  private:
    std::string Name;
  };
}


