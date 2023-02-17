from .ExprAST import ExprAST
from .CodegenError import CodegenError
from .Token import *
from .VariableExprAST import VariableExprAST
from .VarExprAST import VarExprAST

import llvmlite.ir as ir
import llvmlite.binding as llvm

class CallExprAST(ExprAST):
    def __init__(self, parent, callee, args, core):
        self.callee = callee
        self.args = args
        self.parent = parent
        self.core = core
        
    def getSyntax(self):
      return ['identifier','(',['Expression',[',']],')']
      
    def getReturnType(self):
      return self.core.typeContainer.getType(self.getID());

    def parse(parser, parent,id_name, core):
        parser._get_next_token() # '('
        args = []
        if not parser._cur_tok_is_operator(')'):
            while True:
                args.append(parser._parse_expression(parent,core))
                if parser._cur_tok_is_operator(')'):
                    break
                parser._match(TokenKind.OPERATOR, ',')

        parser._get_next_token()  # consume the ')'
        return CallExprAST(parent, id_name, args,core)


    def getID(self):
      args = ''.join([t.getReturnType().toString() + '_' for t in self.args])
      return self.callee + '_' + args;

    def codegen(self, generator):
        call_args = [arg.codegen(generator) for arg in self.args]
        callee_func = generator.getModule().get_global(self.getID())
        if callee_func is None or not isinstance(callee_func, ir.Function):
            raise CodegenError('Call to unknown function', self.getID())
        if len(callee_func.args) != len(self.args):
            raise CodegenError('Call argument length mismatch', self.getID())
        return generator.getBuilder().call(callee_func, call_args, 'calltmp')