#include "FunctionDeclaration.h"

#include "llvm/IR/Value.h"
#include "llvm/IR/Type.h"

#include "Context.h"

namespace PLang
{
  FunctionDeclaration::FunctionDeclaration(const std::string& Name, std::vector<std::string> Args)
    : 
    Name(Name),
    Args(std::move(Args)) {
  }

  const std::string& FunctionDeclaration::getName() const{
    return Name; 
  }
  
  llvm::Function* FunctionDeclaration::codegen(Context& context) {
    // Make the function type:  double(double,double) etc.
    std::vector<llvm::Type*> Doubles(Args.size(), llvm::Type::getDoubleTy(*context.context));
    llvm::FunctionType* FT = llvm::FunctionType::get(llvm::Type::getDoubleTy(*context.context), Doubles, false);

    llvm::Function* F = llvm::Function::Create(FT, llvm::Function::ExternalLinkage, Name, context.mod.get());

    // Set names for all arguments.
    unsigned Idx = 0;
    for (auto& Arg : F->args())
      Arg.setName(Args[Idx++]);

    return F;
  }
}