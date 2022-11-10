#pragma once

#include <map>
#include <memory>

#include "Lexer.h"

namespace PLang
{
  class Expression;
  class FunctionDeclaration;
  class Function;

  class Parser {
  public:
    Parser(Lexer&);

    int getNextToken();
    int GetTokPrecedence();

    std::unique_ptr<Expression>          LogError (const char* Str);
    std::unique_ptr<FunctionDeclaration> LogErrorP(const char* Str);
    std::unique_ptr<Expression>          ParseNumberExpr();
    std::unique_ptr<Expression>          ParseParenExpr();
    std::unique_ptr<Expression>          ParseIdentifierExpr();
    std::unique_ptr<Expression>          ParsePrimary();
    std::unique_ptr<Expression>          ParseBinOpRHS(int ExprPrec, std::unique_ptr<PLang::Expression> LHS);
    std::unique_ptr<Expression>          ParseExpression();
    std::unique_ptr<FunctionDeclaration> ParsePrototype();
    std::unique_ptr<Function>            ParseDefinition();
    std::unique_ptr<Function>            ParseTopLevelExpr();
    std::unique_ptr<FunctionDeclaration> ParseExtern();

    void HandleDefinition();
    void HandleExtern();
    void HandleTopLevelExpression();

    int CurTok;
    std::map<char, int> BinopPrecedence;
  private:

    Lexer& lexer;
  };
}