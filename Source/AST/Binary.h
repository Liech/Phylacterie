#pragma once

#include <memory>

#include "Expression.h"

namespace PLang
{
  class Binary : public PLang::Expression {
  public:
    Binary(char Op, std::unique_ptr<PLang::Expression> LHS, std::unique_ptr<PLang::Expression> RHS);

    virtual llvm::Value* codegen(Context&) override;
  private:
    char Op;
    std::unique_ptr<PLang::Expression> LHS, RHS;
  };
}


