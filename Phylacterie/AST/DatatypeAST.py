from .ExprAST import ExprAST

import llvmlite.ir as ir
import llvmlite.binding as llvm
from string2irType import string2irType
from irType2cType import irType2cType

class DatatypeAST(ExprAST):
    def __init__(self, identifier):
        self.identifier = identifier;

    def getSyntax(self):
      return ['Datatype']

    def dump(self, indent=0):
        return '{0}{1}[{2}]'.format(
            ' ' * indent, self.__class__.__name__, self.val)

    def parse(parent, identifier, core):
      return DatatypeAST(identifier);

    def codegen(self, generator):
        return None
      
    def getTypeString(self):
      return self.identifier;

    def getIRType(self):
      return string2irType(self.identifier);

    def getDefault(self):
      return ir.Constant(self.identifier, 0.0)

    def getCType(self):
      return irType2cType(self.getIRType());

    def toString(self):
      return self.identifier