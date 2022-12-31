from .ExprAST import ExprAST

import llvmlite.ir as ir
import llvmlite.binding as llvm

class UnaryExprAST(ExprAST):
    def __init__(self, parent, op, operand):
        self.op = op
        self.operand = operand
        self.parent = parent

    def dump(self, indent=0):
        s = '{0}{1}[{2}]\n'.format(
            ' ' * indent, self.__class__.__name__, self.op)
        s += self.operand.dump(indent + 2)
        return s

    def codegen(self, generator):
        operand = self.operand.codegen(generator)
        func = generator.getModule().get_global('unary{0}'.format(self.op))
        return generator.getBuilder().call(func, [operand], 'unop')