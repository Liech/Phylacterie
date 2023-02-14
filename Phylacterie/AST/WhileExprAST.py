from .ExprAST import ExprAST
from .Token import *

import llvmlite.ir as ir
import llvmlite.binding as llvm

class WhileExprAST(ExprAST):
    def __init__(self,parent, cond_expr, body, core):
        self.cond_expr = cond_expr
        self.body = body
        self.parent = parent
        self.core = core
        
    def getSyntax(self):
      return ['while','(','Expression',')', 'Scope'];

    def dump(self, indent=0):
        prefix = ' ' * indent
        s = '{0}{1}\n'.format(prefix, self.__class__.__name__)
        #s += '{0} Start [{1}]:\n{2}\n'.format(
        #    prefix, self.id_name, self.start_expr.dump(indent + 2))
        s += '{0} End:\n{1}\n'.format(
            prefix, self.cond_expr.dump(indent + 2))
        s += '{0} Body:\n{1}\n'.format(
            prefix, self.body.dump(indent + 2))
        return s

    def parse(parser, parent, core):
        parser._get_next_token()  # consume the 'for'

        parser._match(TokenKind.OPERATOR, '(')

        cond_expr = parser._parse_expression(parent,core)

        parser._match(TokenKind.OPERATOR, ')')

        body = parser._parse_expression(parent,core)
        
        return WhileExprAST(parent, cond_expr, body,core)

    def codegen(self, generator):
        loop_bb = generator.getBuilder().function.append_basic_block('loop')

        # Insert an explicit fall through from the current block to loop_bb
        generator.getBuilder().branch(loop_bb)
        generator.getBuilder().position_at_start(loop_bb)
       
        # Emit the body of the loop. This, like any other expr, can change the
        # current BB. Note that we ignore the value computed by the body.
        body_val = self.body.codegen(generator)

        # Compute the end condition
        cond = self.cond_expr.codegen(generator)
        cmp = generator.getBuilder().icmp_unsigned('!=', cond, ir.Constant(ir.IntType(1), 0),'loopcond')
        
        # Create the 'after loop' block and insert it
        after_bb = generator.getBuilder().function.append_basic_block('afterloop')

        # Insert the conditional branch into the end of loop_end_bb
        generator.getBuilder().cbranch(cmp, loop_bb, after_bb)

        # New code will be inserted into after_bb
        generator.getBuilder().position_at_start(after_bb)

        # The 'while' expression always returns 0
        return ir.Constant(ir.DoubleType(), 0.0)