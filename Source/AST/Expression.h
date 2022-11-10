#pragma once

namespace llvm
{
  class Value; //#include "llvm/IR/Value.h"
}

namespace PLang
{
  class Expression {
  public:
    virtual ~Expression() = default;

    virtual llvm::Value* codegen() = 0;
  };
}


