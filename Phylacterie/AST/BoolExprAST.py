from ctypes.wintypes import BOOL
from xmlrpc.client import boolean
from .ExprAST import ExprAST

import llvmlite.ir as ir
import llvmlite.binding as llvm


class BoolExprAST(ExprAST):
    def __init__(self, parent, val):
        self.val = val
        self.parent = parent

    def dump(self, indent=0):
        return '{0}{1}[{2}]'.format(
            ' ' * indent, self.__class__.__name__, self.val)

    def codegen(self, generator):
        return ir.Constant(ir.IntType(1), int(self.val))
      
    def getReturnType(self):
      return ir.IntType(1);