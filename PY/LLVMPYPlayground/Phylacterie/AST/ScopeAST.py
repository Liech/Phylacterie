from .ExprAST import ExprAST

import llvmlite.ir as ir
import llvmlite.binding as llvm

class ScopeAST(ExprAST):
    def __init__(self, parent, body):
        self.body = body
        self.parent = parent

    def dump(self, indent=0):
        prefix = ' ' * indent
        s = '{0}{1}\n'.format(prefix, self.__class__.__name__)
        s += '{0} Body:\n'.format(prefix)
        s += self.body.dump(indent + 2)
        return s

    def codegen(self, generator):
        return self.body.codegen(generator);