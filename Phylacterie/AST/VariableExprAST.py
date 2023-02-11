from types import GenericAlias
from .ExprAST import ExprAST
from string2irType import string2irType

import llvmlite.ir as ir
import llvmlite.binding as llvm

class VariableExprAST(ExprAST):
    def __init__(self, parent, name):
        self.name = name
        self.parent = parent
        self.returnType = None;

    def dump(self, indent=0):
        return '{0}{1}[{2}]'.format(
            ' ' * indent, self.__class__.__name__, self.name)

    def getReturnType(self):
      return string2irType(self.returnType);

    def codegen(self,generator):
        var_addr = generator.getSymtab()[self.name]
        self.returnType = generator.getVariableType(self.name);
        return generator.getBuilder().load(var_addr, self.name)