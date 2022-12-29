from .ExprAST import ExprAST

import llvmlite.ir as ir
import llvmlite.binding as llvm


class NumberExprAST(ExprAST):
    def __init__(self, val):
        self.val = val

    def dump(self, indent=0):
        return '{0}{1}[{2}]'.format(
            ' ' * indent, self.__class__.__name__, self.val)

    def codegen(self, generator):
        return ir.Constant(ir.DoubleType(), float(self.val))
