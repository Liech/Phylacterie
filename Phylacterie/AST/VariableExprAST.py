from .ExprAST import ExprAST

import llvmlite.ir as ir
import llvmlite.binding as llvm

class VariableExprAST(ExprAST):
    def __init__(self, parent, name, core):
        self.name = name
        self.parent = parent
        self.core = core
        
    def getSyntax(self):
      return ['identifier'];

    def getReturnType(self):
      return self.core.typeContainer.getType(self.name);

    def parse(self, parent, id_name,core):
      return VariableExprAST(parent,id_name, core);

    def codegen(self,generator):
        var_addr = generator.getSymtab()[self.name]
        self.returnType = self.core.typeContainer.getType(self.name);
        return generator.getBuilder().load(var_addr, self.name)