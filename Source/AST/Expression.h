#pragma once

namespace llvm
{
  class Value; //#include "llvm/IR/Value.h"
  class LLVMContext;
}

namespace PLang
{
  class Context;

  class Expression {
  public:
    virtual ~Expression() = default;

    virtual llvm::Value* codegen(Context&) = 0;
  };
}


