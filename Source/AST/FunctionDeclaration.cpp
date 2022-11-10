#include "FunctionDeclaration.h"

#include "llvm/IR/Value.h"

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
}