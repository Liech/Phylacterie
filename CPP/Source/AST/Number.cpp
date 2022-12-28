#include "Number.h"

#include "Context.h"

#include "llvm/IR/Value.h"
#include "llvm/IR/Constants.h"

namespace PLang
{
  Number::Number(double Val) 
    :
    Val(Val) {
  }

  llvm::Value* Number::codegen(Context& context) {
    return llvm::ConstantFP::get(*context.context, llvm::APFloat(Val));
  }
}