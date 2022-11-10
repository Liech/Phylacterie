#include "Call.h"

#include "llvm/IR/Value.h"

#include "Context.h"

namespace PLang
{
  Call::Call(const std::string& Callee, std::vector<std::unique_ptr<PLang::Expression>> Args)
    : 
    Callee(Callee),
    Args(std::move(Args)) {
  }

  llvm::Value* Call::codegen(Context& context) {
    // Look up the name in the global module table.
    llvm::Function* CalleeF = context.mod->getFunction(Callee);
    if (!CalleeF)
      return context.LogErrorV("Unknown function referenced");

    // If argument mismatch error.
    if (CalleeF->arg_size() != Args.size())
      return context.LogErrorV("Incorrect # arguments passed");

    std::vector<llvm::Value*> ArgsV;
    for (unsigned i = 0, e = Args.size(); i != e; ++i) {
      ArgsV.push_back(Args[i]->codegen(context));
      if (!ArgsV.back())
        return nullptr;
    }

    return context.builder->CreateCall(CalleeF, ArgsV, "calltmp");
  }
}