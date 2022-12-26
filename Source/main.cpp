#include "Parser/Token.h"
#include "Parser/Parser.h"
#include "Parser/Lexer.h"

#include "AST/Expression.h"
#include "AST/Number.h"
#include "AST/Variable.h"
#include "AST/Call.h"
#include "AST/Binary.h"
#include "AST/FunctionDeclaration.h"
#include "AST/Function.h"
#include "llvm/Support/TargetSelect.h"

static PLang::Lexer  lexer;
static PLang::Parser parser(lexer);

/// top ::= definition | external | expression | ';'
static void MainLoop() {
  while (true) {
    fprintf(stderr, "ready> ");
    switch (parser.CurTok) {
    case PLang::tok_eof:
      return;
    case ';': // ignore top-level semicolons.
      parser.getNextToken();
      break;
    case PLang::tok_def:
      parser.HandleDefinition();
      break;
    case PLang::tok_extern:
      parser.HandleExtern();
      break;
    default:
      parser.HandleTopLevelExpression();
      break;
    }
  }
}

int main() {
  fprintf(stderr, "ready> ");
  parser.getNextToken();
  MainLoop();
  return 0;
}