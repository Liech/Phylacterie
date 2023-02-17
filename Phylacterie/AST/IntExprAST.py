from .ExprAST import ExprAST

from .DatatypeAST import DatatypeAST
import llvmlite.ir as ir
import llvmlite.binding as llvm


class IntExprAST(ExprAST):
    def __init__(self, parent, val):
        self.val = val
        self.parent = parent
    
    def getSyntax(self):
      return ['Number']

    def codegen(self, generator):
        return ir.Constant(ir.IntType(32), int(self.val))
      
    def getReturnType(self):
      return DatatypeAST('int')