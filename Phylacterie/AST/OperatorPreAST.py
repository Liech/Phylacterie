from .ExprAST import ExprAST

import llvmlite.ir as ir
import llvmlite.binding as llvm

class OperatorPreAST(ExprAST):
  def __init__(self):
    raise Exception("Parser Error");

  def parse(parser, parent,core):
    pass
      
    
