
import llvmlite.ir as ir
import llvmlite.binding as llvm

from ast import parse
from .Lexer import Lexer
from .AST import *
from .ParseError import ParseError
from .string2irType import string2irType

class Parser(object):
    """Parser for the Kaleidoscope language.

    After the parser is created, invoke parse_toplevel multiple times to parse
    Kaleidoscope source into an AST.
    """
    def __init__(self):
        self.token_generator = None
        self.cur_tok = None

    # toplevel ::= definition | external | expression | ';'
    def parse_toplevel(self, root, buf):
        """Given a string, returns an AST node representing it."""
        self.token_generator = Lexer(buf).tokens()
        self.cur_tok = None
        self._get_next_token()
        
        if not self.cur_tok.kind == TokenKind.IDENTIFIER:
          raise ParseError('Expected datatype identifier')
        dataType = self.cur_tok.value
        self._get_next_token()

        result = [];
        while self.cur_tok.kind != TokenKind.EOF:
            if self.cur_tok.kind == TokenKind.EXTERN:
                result.append(self._parse_external(root))
            elif self.cur_tok.kind == TokenKind.DEF:
                result.append(FunctionAST.parse(self, root))
            elif self.cur_tok.kind == TokenKind.SCOPESTART:
                result.append(ScopeAST.parse(self,root))
            elif self.cur_tok.kind == TokenKind.FALSE or self.cur_tok.kind == TokenKind.TRUE:
                result.append(BoolExprAST.parse(self,root))
            else:
                result.append(self._parse_expression(root))                
        root.setBody(result);
        return FunctionAST.create_anonymous(None, root, string2irType(dataType))

    def _get_next_token(self):
        self.cur_tok = next(self.token_generator)

    def _match(self, expected_kind, expected_value=None):
        """Consume the current token; verify that it's of the expected kind.

        If expected_kind == TokenKind.OPERATOR, verify the operator's value.
        """
        if (expected_kind == TokenKind.OPERATOR and
            not self._cur_tok_is_operator(expected_value)):
            raise ParseError('Expected "{0}"'.format(expected_value))
        elif expected_kind != self.cur_tok.kind:
            raise ParseError('Expected "{0}"'.format(expected_kind))
        self._get_next_token()

    _precedence_map = {'=': 2, '<': 10, '+': 20, '-': 20, '*': 40}

    def _cur_tok_precedence(self):
        """Get the operator precedence of the current token."""
        try:
            return self._precedence_map[self.cur_tok.value]
        except KeyError:
            return -1

    def _cur_tok_is_operator(self, op):
        """Query whether the current token is the operator op"""
        return (self.cur_tok.kind == TokenKind.OPERATOR and
                self.cur_tok.value == op)

    # identifierexpr
    #   ::= identifier
    #   ::= identifier '(' expression* ')'
    def _parse_identifier_expr(self,parent):
      return CallExprAST.parse(self, parent);

    # numberexpr ::= number
    def _parse_number_expr(self,parent):
        if('.' in self.cur_tok.value):
          result = DoubleExprAST(parent, self.cur_tok.value)
        else:
          result = IntExprAST(parent, self.cur_tok.value)
        self._get_next_token()  # consume the number
        return result

    # parenexpr ::= '(' expression ')'
    def _parse_paren_expr(self, parent):
        self._get_next_token()  # consume the '('
        expr = self._parse_expression(parent)
        self._match(TokenKind.OPERATOR, ')')
        return expr

    # primary
    #   ::= identifierexpr
    #   ::= numberexpr
    #   ::= parenexpr
    #   ::= ifexpr
    #   ::= forexpr
    def _parse_primary(self,parent):
        if self.cur_tok.kind == TokenKind.IDENTIFIER:
            return self._parse_identifier_expr(parent)
        elif self.cur_tok.kind == TokenKind.NUMBER:
            return self._parse_number_expr(parent)
        elif self._cur_tok_is_operator('('):
            return self._parse_paren_expr(parent)
        elif self.cur_tok.kind == TokenKind.IF:
            return IfExprAST.parse(self,parent);
        elif self.cur_tok.kind == TokenKind.WHILE:
            return WhileExprAST.parse(self,parent);
        elif self.cur_tok.kind == TokenKind.VAR:
            return VarExprAST.parse(self, parent);
        elif self.cur_tok.kind == TokenKind.SCOPESTART:
            return ScopeAST.parse(self,parent);
        elif self.cur_tok.kind == TokenKind.DEF:
            return FunctionAST.parse(self, parent);
        elif self.cur_tok.kind == TokenKind.TRUE:
            return BoolExprAST.parse(self,parent);
        elif self.cur_tok.kind == TokenKind.FALSE:
            return BoolExprAST.parse(self,parent);
        else:
            raise ParseError('Unknown token when expecting an expression')

    # expression ::= primary binoprhs
    def _parse_expression(self, parent):
        if (self.cur_tok.kind == TokenKind.SCOPESTART):
           return ScopeAST.parse(self,parent);

        lhs = UnaryExprAST.parse(self, parent);
        # Start with precedence 0 because we want to bind any operator to the
        # expression at this point.
        result = BinaryExprAST.parse(self,  0, lhs, parent)

        return result;

    # external ::= 'extern' prototype
    def _parse_external(self,parent):
        self._get_next_token()  # consume 'extern'
        return PrototypeAST.parse(self,parent);
