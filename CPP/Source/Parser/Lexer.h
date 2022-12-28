#pragma once

#include <string>

namespace PLang {
  class Lexer {
  public:
    int gettok();

    std::string IdentifierStr; // Filled in if tok_identifier
    double NumVal;             // Filled in if tok_number
  private:
  };
}