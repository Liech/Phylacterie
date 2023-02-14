from .ExprAST import ExprAST
from .Token import *

import llvmlite.ir as ir
import llvmlite.binding as llvm

class UnaryExprAST(ExprAST):
    def __init__(self, parent, op, operand, core):
        self.op = op
        self.operand = operand
        self.parent = parent
        self.core = core

    def getSyntax(self):
      return ['Operator', 'Expression'];


    def dump(self, indent=0):
        s = '{0}{1}[{2}]\n'.format(
            ' ' * indent, self.__class__.__name__, self.op)
        s += self.operand.dump(indent + 2)
        return s

    def parse(parser, parent, core):
        # no unary operator before a primary
        if (not parser.cur_tok.kind == TokenKind.OPERATOR or
            parser.cur_tok.value in ('(', ',')):
            return parser._parse_primary(parent,core)

        # unary operator
        op = parser.cur_tok.value
        parser._get_next_token()
        return UnaryExprAST(parent, op, UnaryExprAST.parse(parser, parent,core),core)

    def codegen(self, generator):
        operand = self.operand.codegen(generator)
        func = generator.getModule().get_global('unary{0}'.format(self.op))
        return generator.getBuilder().call(func, [operand], 'unop')