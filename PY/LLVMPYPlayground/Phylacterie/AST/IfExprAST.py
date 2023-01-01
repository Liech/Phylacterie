from .ExprAST import ExprAST
from .NumberExprAST import NumberExprAST

import llvmlite.ir as ir
import llvmlite.binding as llvm

class IfExprAST(ExprAST):
    def __init__(self, parent, cond_expr, then_expr, else_expr):
        self.cond_expr = cond_expr
        self.then_expr = then_expr
        self.else_expr = else_expr
        self.parent = parent

    def dump(self, indent=0):
        prefix = ' ' * indent
        s = '{0}{1}\n'.format(prefix, self.__class__.__name__)
        s += '{0} Condition:\n{1}\n'.format(
            prefix, self.cond_expr.dump(indent + 2))
        s += '{0} Then:\n{1}\n'.format(
            prefix, self.then_expr.dump(indent + 2))
        return s

    def codegen(self, generator):
        if (self.else_expr is None):
          self.else_expr = NumberExprAST(self.parent,0);

        # Emit comparison value
        cond_val = self.cond_expr.codegen(generator)
        cmp = generator.getBuilder().fcmp_ordered(
            '!=', cond_val, ir.Constant(ir.DoubleType(), 0.0))

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
        phi = generator.getBuilder().phi(ir.DoubleType(), 'iftmp')
        phi.add_incoming(then_val, then_bb)
        phi.add_incoming(else_val, else_bb)
        return phi