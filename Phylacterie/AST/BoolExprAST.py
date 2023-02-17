from ctypes.wintypes import BOOL
from xmlrpc.client import boolean
from .ExprAST import ExprAST
from .Token import *
from .DatatypeAST import DatatypeAST

import llvmlite.ir as ir
import llvmlite.binding as llvm


class BoolExprAST(ExprAST):
    def __init__(self, parent, val):
        self.val = val
        self.parent = parent
        
    def getSyntax(self):
      #return ['true']
      return ['false']

    def dump(self, indent=0):
        return '{0}{1}[{2}]'.format(
            ' ' * indent, self.__class__.__name__, self.val)

    def parse(parser, parent):
      if (parser.cur_tok.kind == TokenKind.FALSE):
        parser._get_next_token()
        return BoolExprAST(parent,0);
      elif (parser.cur_tok.kind == TokenKind.TRUE):
        parser._get_next_token()
        return BoolExprAST(parent,1);
      else:
        raise ParseError("Expected boolean true/false");

    def codegen(self, generator):
        return ir.Constant(ir.IntType(1), int(self.val))
      
    def getReturnType(self):
      return DatatypeAST('bool')