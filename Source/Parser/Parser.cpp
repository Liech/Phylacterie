#include "Parser.h"

#include <stdio.h>
#include <ctype.h>
#include <vector>
#include <string>

#include "Token.h"

#include "AST/Number.h"
#include "AST/Variable.h"
#include "AST/Call.h"
#include "AST/Binary.h"
#include "AST/Function.h"

namespace PLang
{
  Parser::Parser(Lexer& inputLexer) : lexer(inputLexer) {
    BinopPrecedence['<'] = 10;
    BinopPrecedence['+'] = 20;
    BinopPrecedence['-'] = 20;
    BinopPrecedence['*'] = 40;
  }

  int Parser::getNextToken() { 
    return CurTok = lexer.gettok(); 
  }

  int Parser::GetTokPrecedence() {
    if (!isascii(CurTok))
      return -1;

    // Make sure it's a declared binop.
    int TokPrec = BinopPrecedence[CurTok];
    if (TokPrec <= 0)
      return -1;
    return TokPrec;
  }

  std::unique_ptr<PLang::Expression> Parser::LogError(const char* Str) {
    fprintf(stderr, "Error: %s\n", Str);
    return nullptr;
  }

  std::unique_ptr<PLang::FunctionDeclaration> Parser::LogErrorP(const char* Str) {
    LogError(Str);
    return nullptr;
  }

  /// numberexpr ::= number
  std::unique_ptr<PLang::Expression> Parser::ParseNumberExpr() {
    auto Result = std::make_unique<Number>(lexer.NumVal);
    getNextToken(); // consume the number
    return std::move(Result);
  }

  /// parenexpr ::= '(' expression ')'
  std::unique_ptr<PLang::Expression> Parser::ParseParenExpr() {
    getNextToken(); // eat (.
    auto V = ParseExpression();
    if (!V)
      return nullptr;

    if (CurTok != ')')
      return LogError("expected ')'");
    getNextToken(); // eat ).
    return V;
  }

  /// identifierexpr
  ///   ::= identifier
  ///   ::= identifier '(' expression* ')'
  std::unique_ptr<PLang::Expression> Parser::ParseIdentifierExpr() {
    std::string IdName = lexer.IdentifierStr;

    getNextToken(); // eat identifier.

    if (CurTok != '(') // Simple variable ref.
      return std::make_unique<PLang::Variable>(IdName);

    // Call.
    getNextToken(); // eat (
    std::vector<std::unique_ptr<PLang::Expression>> Args;
    if (CurTok != ')') {
      while (true) {
        if (auto Arg = ParseExpression())
          Args.push_back(std::move(Arg));
        else
          return nullptr;

        if (CurTok == ')')
          break;

        if (CurTok != ',')
          return LogError("Expected ')' or ',' in argument list");
        getNextToken();
      }
    }

    // Eat the ')'.
    getNextToken();

    return std::make_unique<PLang::Call>(IdName, std::move(Args));
  }

  /// primary
  ///   ::= identifierexpr
  ///   ::= numberexpr
  ///   ::= parenexpr
  std::unique_ptr<PLang::Expression> Parser::ParsePrimary() {
    switch (CurTok) {
    default:
      return LogError("unknown token when expecting an expression");
    case PLang::tok_identifier:
      return ParseIdentifierExpr();
    case PLang::tok_number:
      return ParseNumberExpr();
    case '(':
      return ParseParenExpr();
    }
  }

  /// binoprhs
  ///   ::= ('+' primary)*
  std::unique_ptr<PLang::Expression> Parser::ParseBinOpRHS(int ExprPrec, std::unique_ptr<PLang::Expression> LHS) {
    // If this is a binop, find its precedence.
    while (true) {
      int TokPrec = GetTokPrecedence();

      // If this is a binop that binds at least as tightly as the current binop,
      // consume it, otherwise we are done.
      if (TokPrec < ExprPrec)
        return LHS;

      // Okay, we know this is a binop.
      int BinOp = CurTok;
      getNextToken(); // eat binop

      // Parse the primary expression after the binary operator.
      auto RHS = ParsePrimary();
      if (!RHS)
        return nullptr;

      // If BinOp binds less tightly with RHS than the operator after RHS, let
      // the pending operator take RHS as its LHS.
      int NextPrec = GetTokPrecedence();
      if (TokPrec < NextPrec) {
        RHS = ParseBinOpRHS(TokPrec + 1, std::move(RHS));
        if (!RHS)
          return nullptr;
      }

      // Merge LHS/RHS.
      LHS = std::make_unique<PLang::Binary>(BinOp, std::move(LHS), std::move(RHS));
    }
  }

  /// expression
  ///   ::= primary binoprhs
  ///
  std::unique_ptr<PLang::Expression> Parser::ParseExpression() {
    auto LHS = ParsePrimary();
    if (!LHS)
      return nullptr;

    return ParseBinOpRHS(0, std::move(LHS));
  }

  /// prototype
  ///   ::= id '(' id* ')'
  std::unique_ptr<PLang::FunctionDeclaration> Parser::ParsePrototype() {
    if (CurTok != PLang::tok_identifier)
      return LogErrorP("Expected function name in prototype");

    std::string FnName = lexer.IdentifierStr;
    getNextToken();

    if (CurTok != '(')
      return LogErrorP("Expected '(' in prototype");

    std::vector<std::string> ArgNames;
    while (getNextToken() == PLang::tok_identifier)
      ArgNames.push_back(lexer.IdentifierStr);
    if (CurTok != ')')
      return LogErrorP("Expected ')' in prototype");

    // success.
    getNextToken(); // eat ')'.

    return std::make_unique<PLang::FunctionDeclaration>(FnName, std::move(ArgNames));
  }

  /// definition ::= 'def' prototype expression
  std::unique_ptr<PLang::Function> Parser::ParseDefinition() {
    getNextToken(); // eat def.
    auto Proto = ParsePrototype();
    if (!Proto)
      return nullptr;

    if (auto E = ParseExpression())
      return std::make_unique<PLang::Function>(std::move(Proto), std::move(E));
    return nullptr;
  }

  /// toplevelexpr ::= expression
  std::unique_ptr<PLang::Function> Parser::ParseTopLevelExpr() {
    if (auto E = ParseExpression()) {
      // Make an anonymous proto.
      auto Proto = std::make_unique<PLang::FunctionDeclaration>("__anon_expr",
        std::vector<std::string>());
      return std::make_unique<PLang::Function>(std::move(Proto), std::move(E));
    }
    return nullptr;
  }

  /// external ::= 'extern' prototype
  std::unique_ptr<PLang::FunctionDeclaration> Parser::ParseExtern() {
    getNextToken(); // eat extern.
    return ParsePrototype();
  }

  void Parser::HandleDefinition() {
    if (ParseDefinition()) {
      fprintf(stderr, "Parsed a function definition.\n");
    }
    else {
      // Skip token for error recovery.
      getNextToken();
    }
  }

  void Parser::HandleExtern() {
    if (ParseExtern()) {
      fprintf(stderr, "Parsed an extern\n");
    }
    else {
      // Skip token for error recovery.
      getNextToken();
    }
  }

  void Parser::HandleTopLevelExpression() {
    // Evaluate a top-level expression into an anonymous function.
    if (ParseTopLevelExpr()) {
      fprintf(stderr, "Parsed a top-level expr\n");
    }
    else {
      // Skip token for error recovery.
      getNextToken();
    }
  }
}