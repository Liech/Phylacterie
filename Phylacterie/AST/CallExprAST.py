from .ExprAST import ExprAST
from .CodegenError import CodegenError
from .Token import *
from .VariableExprAST import VariableExprAST
from irType2string import irType2string

import llvmlite.ir as ir
import llvmlite.binding as llvm

class CallExprAST(ExprAST):
    def __init__(self, parent, callee, args):
        self.callee = callee
        self.args = args
        self.parent = parent

    def dump(self, indent=0):
        s = '{0}{1}[{2}]\n'.format(
            ' ' * indent, self.__class__.__name__, self.callee)
        for arg in self.args:
            s += arg.dump(indent + 2) + '\n'
        return s[:-1]  # snip out trailing '\n'
      
    def getReturnType(self):
      return ir.DoubleType();

    def parse(parser, parent):
        id_name = parser.cur_tok.value
        parser._get_next_token()
        # If followed by a '(' it's a call; otherwise, a simple variable ref.
        if not parser._cur_tok_is_operator('('):
            return VariableExprAST(parent, id_name)

        parser._get_next_token()
        args = []
        if not parser._cur_tok_is_operator(')'):
            while True:
                args.append(parser._parse_expression(parent))
                if parser._cur_tok_is_operator(')'):
                    break
                parser._match(TokenKind.OPERATOR, ',')

        parser._get_next_token()  # consume the ')'
        return CallExprAST(parent, id_name, args)


    def getID(self):
      args = ''.join([irType2string(t.getReturnType()) + '_' for t in self.args])
      return self.callee + '_' + args;

    def codegen(self, generator):
        callee_func = generator.getModule().get_global(self.getID())
        if callee_func is None or not isinstance(callee_func, ir.Function):
            raise CodegenError('Call to unknown function', self.getID())
        if len(callee_func.args) != len(self.args):
            raise CodegenError('Call argument length mismatch', self.getID())
        call_args = [arg.codegen(generator) for arg in self.args]
        return generator.getBuilder().call(callee_func, call_args, 'calltmp')