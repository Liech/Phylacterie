#include "Function.h"


#include "Context.h"

#include "llvm/ADT/APFloat.h"
#include "llvm/ADT/STLExtras.h"
#include "llvm/IR/BasicBlock.h"
#include "llvm/IR/Constants.h"
#include "llvm/IR/DerivedTypes.h"
#include "llvm/IR/Function.h"
#include "llvm/IR/IRBuilder.h"
#include "llvm/IR/LLVMContext.h"
#include "llvm/IR/Module.h"
#include "llvm/IR/Type.h"
#include "llvm/IR/Verifier.h"
#include "llvm/IR/LegacyPassManager.h"

#include <algorithm>
#include <cctype>
#include <cstdio>
#include <cstdlib>
#include <map>
#include <memory>
#include <string>
#include <vector>

#include <exception>

namespace PLang
{
  Function::Function(std::unique_ptr<FunctionDeclaration> Proto, std::unique_ptr<PLang::Expression> Body)
    : 
    Proto(std::move(Proto)),
    Body(std::move(Body)) {
  }

  llvm::Function* Function::codegen(Context& context) {
    // First, check for an existing function from a previous 'extern' declaration.
    llvm::Function* TheFunction = context.mod->getFunction(Proto->getName());

    if (!TheFunction)
      TheFunction = Proto->codegen(context);

    if (!TheFunction)
      return nullptr;

    if (!TheFunction->empty())
      return (llvm::Function*)context.LogErrorV("Function cannot be redefined.");

    // Create a new basic block to start insertion into.
    llvm::BasicBlock* BB = llvm::BasicBlock::Create(*context.context, "entry", TheFunction);
    context.builder->SetInsertPoint(BB);
    
    // Record the function arguments in the NamedValues map.
    context.namedValues.clear();
    for (auto& Arg : TheFunction->args())
      context.namedValues[std::string(Arg.getName())] = &Arg;
    
    if (llvm::Value* RetVal = Body->codegen(context)) {
      // Finish off the function.
      context.builder->CreateRet(RetVal);
    
      // Validate the generated code, checking for consistency.
      //llvm::verifyFunction(*TheFunction);
      llvm::verifyFunction(*TheFunction);

      context.fpm->run(*TheFunction);

      return TheFunction;
    }
    
    // Error reading body, remove function.
    TheFunction->eraseFromParent();
    return nullptr;
  }
}