from .ExprAST import ExprAST
from .VariableExprAST import VariableExprAST
from .UnaryExprAST import UnaryExprAST
from .CodegenError import CodegenError
from .Token import *
from irType2string import irType2string

import llvmlite.ir as ir
import llvmlite.binding as llvm

class BinaryExprAST(ExprAST):
    def __init__(self, parent, core):
        self.parent = parent
        self.core   = core
        
    def getSyntax(self):
      return ['class']
            
    def getReturnType(self):      
      return None;

    def parse(parser, parent,core):
        return None

    def getID(self):
      return 'class';

    def codegen(self, generator):
        return None

