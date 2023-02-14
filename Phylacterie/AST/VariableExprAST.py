from .ExprAST import ExprAST
from string2irType import string2irType

import llvmlite.ir as ir
import llvmlite.binding as llvm

class VariableExprAST(ExprAST):
    def __init__(self, parent, name, core):
        self.name = name
        self.parent = parent
        self.core = core
        
    def getSyntax(self):
      return ['identifier'];

    def dump(self, indent=0):
        return '{0}{1}[{2}]'.format(
            ' ' * indent, self.__class__.__name__, self.name)

    def getReturnType(self):
      return self.core.typeContainer.getType(self.name);

    def codegen(self,generator):
        var_addr = generator.getSymtab()[self.name]
        self.returnType = self.core.typeContainer.getType(self.name);
        return generator.getBuilder().load(var_addr, self.name)