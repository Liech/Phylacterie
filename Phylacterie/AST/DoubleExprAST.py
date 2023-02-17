from .ExprAST import ExprAST
from .DatatypeAST import DatatypeAST

import llvmlite.ir as ir
import llvmlite.binding as llvm


class DoubleExprAST(ExprAST):
    def __init__(self, parent, val):
        self.val = val
        self.parent = parent
        
    def getSyntax(self):
      return ['Number','.','Number']

    def dump(self, indent=0):
        return '{0}{1}[{2}]'.format(
            ' ' * indent, self.__class__.__name__, self.val)

    def codegen(self, generator):
        return ir.Constant(ir.DoubleType(), float(self.val))
      
    def getReturnType(self):
      return DatatypeAST('double')