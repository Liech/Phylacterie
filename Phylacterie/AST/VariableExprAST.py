from .ExprAST import ExprAST

import llvmlite.ir as ir
import llvmlite.binding as llvm

class VariableExprAST(ExprAST):
    def __init__(self, parent, name):
        self.name = name
        self.parent = parent

    def dump(self, indent=0):
        return '{0}{1}[{2}]'.format(
            ' ' * indent, self.__class__.__name__, self.name)

    def codegen(self,generator):
        var_addr = generator.getSymtab()[self.name]
        return generator.getBuilder().load(var_addr, self.name)