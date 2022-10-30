#pragma once

#include <vector>
#include <memory>
#include <string>

#include "FunctionDeclaration.h"

namespace PLang
{
  class Function {
    std::unique_ptr<FunctionDeclaration> Proto;
    std::unique_ptr<PLang::Expression> Body;

  public:
    Function(std::unique_ptr<FunctionDeclaration> Proto,
      std::unique_ptr<PLang::Expression> Body)
      : Proto(std::move(Proto)), Body(std::move(Body)) {}
  };
}