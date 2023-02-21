from .ExprAST import ExprAST
from .DoubleExprAST import DoubleExprAST
from .Token import *

import llvmlite.ir as ir
import llvmlite.binding as llvm

class IfExprAST(ExprAST):
    def __init__(self, parent, cond_expr, then_expr, else_expr, core):
        self.cond_expr = cond_expr
        self.then_expr = then_expr
        self.else_expr = else_expr
        self.parent = parent
        self.core = core
        
    def getSyntax(self):
      return ['if','(','Expression',')', 'Expression', ['else', 'Expression']]
          
    def getReturnType(self):
      return self.then_expr.getReturnType();

    def parse(parser, parent, core):
        parser._get_next_token()  # consume the 'if'        
        parser._match(TokenKind.OPERATOR, '(')
        cond_expr = parser._parse_expression(parent, core)
        parser._match(TokenKind.OPERATOR, ')')
        then_expr = parser._parse_expression(parent, core)
        parser.semicolon();
        if parser.cur_tok.kind == TokenKind.ELSE:
          parser._match(TokenKind.ELSE)
          else_expr = parser._parse_expression(parent, core)
          parser.semicolon();
          result = IfExprAST(parent, cond_expr, then_expr, else_expr, core)
        else:
          result = IfExprAST(parent, cond_expr, then_expr, None, core)
        parser.nextNeedsNoSemicolon();
        return result;

    def codegen(self, generator):
        if (self.else_expr is None):
          self.else_expr = DoubleExprAST(self.core, self.parent,0);

        # Emit comparison value
        cond_val = self.cond_expr.codegen(generator)
        cmp = generator.getBuilder().icmp_unsigned(
            '!=', cond_val, ir.Constant(ir.IntType(1), 0))

        # Create basic blocks to express the control flow, with a conditional
        # branch to either then_bb or else_bb depending on cmp. else_bb and
        # merge_bb are not yet attached to the function's list of BBs because
        # if a nested IfExpr is generated we want to have a reasonably nested
        # order of BBs generated into the function.
        then_bb = generator.getBuilder().function.append_basic_block('then')
        else_bb = ir.Block(generator.getBuilder().function, 'else')
        merge_bb = ir.Block(generator.getBuilder().function, 'ifcont')
        generator.getBuilder().cbranch(cmp, then_bb, else_bb)

        # Emit the 'then' part
        generator.getBuilder().position_at_start(then_bb)
        then_val = self.then_expr.codegen(generator)
        generator.getBuilder().branch(merge_bb)

        # Emission of then_val could have modified the current basic block. To
        # properly set up the PHI, remember which block the 'then' part ends in.
        then_bb = generator.getBuilder().block

        # Emit the 'else' part
        generator.getBuilder().function.basic_blocks.append(else_bb)
        generator.getBuilder().position_at_start(else_bb)
        else_val = self.else_expr.codegen(generator)

        # Emission of else_val could have modified the current basic block.
        else_bb = generator.getBuilder().block
        generator.getBuilder().branch(merge_bb)

        # Emit the merge ('ifcnt') block
        generator.getBuilder().function.basic_blocks.append(merge_bb)
        generator.getBuilder().position_at_start(merge_bb)

        assert(self.then_expr.getReturnType().toString() == self.else_expr.getReturnType().toString());
        phi = generator.getBuilder().phi(self.then_expr.getReturnType().getIRType(), 'iftmp')
        phi.add_incoming(then_val, then_bb)
        phi.add_incoming(else_val, else_bb)
        return phi