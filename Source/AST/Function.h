#pragma once

#include <vector>
#include <memory>
#include <string>

#include "FunctionDeclaration.h"

namespace PLang
{
  class Function {
  public:
    Function(std::unique_ptr<FunctionDeclaration> Proto, std::unique_ptr<PLang::Expression> Body);

  private:
    std::unique_ptr<FunctionDeclaration> Proto;
    std::unique_ptr<PLang::Expression> Body;
  };
}