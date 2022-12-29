from .ExprAST import ExprAST

import llvmlite.ir as ir
import llvmlite.binding as llvm

class IfExprAST(ExprAST):
    def __init__(self, cond_expr, then_expr, else_expr):
        self.cond_expr = cond_expr
        self.then_expr = then_expr
        self.else_expr = else_expr

    def dump(self, indent=0):
        prefix = ' ' * indent
        s = '{0}{1}\n'.format(prefix, self.__class__.__name__)
        s += '{0} Condition:\n{1}\n'.format(
            prefix, self.cond_expr.dump(indent + 2))
        s += '{0} Then:\n{1}\n'.format(
            prefix, self.then_expr.dump(indent + 2))
        s += '{0} Else:\n{1}'.format(
            prefix, self.else_expr.dump(indent + 2))
        return s

    def codegen(self, generator):
        # Emit comparison value
        cond_val = self.cond_expr.codegen(generator)
        cmp = generator.builder.fcmp_ordered(
            '!=', cond_val, ir.Constant(ir.DoubleType(), 0.0))

        # Create basic blocks to express the control flow, with a conditional
        # branch to either then_bb or else_bb depending on cmp. else_bb and
        # merge_bb are not yet attached to the function's list of BBs because
        # if a nested IfExpr is generated we want to have a reasonably nested
        # order of BBs generated into the function.
        then_bb = generator.builder.function.append_basic_block('then')
        else_bb = ir.Block(generator.builder.function, 'else')
        merge_bb = ir.Block(generator.builder.function, 'ifcont')
        generator.builder.cbranch(cmp, then_bb, else_bb)

        # Emit the 'then' part
        generator.builder.position_at_start(then_bb)
        then_val = self.then_expr.codegen(generator)
        generator.builder.branch(merge_bb)

        # Emission of then_val could have modified the current basic block. To
        # properly set up the PHI, remember which block the 'then' part ends in.
        then_bb = generator.builder.block

        # Emit the 'else' part
        generator.builder.function.basic_blocks.append(else_bb)
        generator.builder.position_at_start(else_bb)
        else_val = self.else_expr.codegen(generator)

        # Emission of else_val could have modified the current basic block.
        else_bb = generator.builder.block
        generator.builder.branch(merge_bb)

        # Emit the merge ('ifcnt') block
        generator.builder.function.basic_blocks.append(merge_bb)
        generator.builder.position_at_start(merge_bb)
        phi = generator.builder.phi(ir.DoubleType(), 'iftmp')
        phi.add_incoming(then_val, then_bb)
        phi.add_incoming(else_val, else_bb)
        return phi