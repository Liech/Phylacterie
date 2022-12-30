from .ExprAST import ExprAST

import llvmlite.ir as ir
import llvmlite.binding as llvm

class ForExprAST(ExprAST):
    def __init__(self,parent, id_name, start_expr, end_expr, step_expr, body):
        self.id_name = id_name
        self.start_expr = start_expr
        self.end_expr = end_expr
        self.step_expr = step_expr
        self.body = body
        self.parent = parent

    def dump(self, indent=0):
        prefix = ' ' * indent
        s = '{0}{1}\n'.format(prefix, self.__class__.__name__)
        s += '{0} Start [{1}]:\n{2}\n'.format(
            prefix, self.id_name, self.start_expr.dump(indent + 2))
        s += '{0} End:\n{1}\n'.format(
            prefix, self.end_expr.dump(indent + 2))
        s += '{0} Step:\n{1}\n'.format(
            prefix, self.step_expr.dump(indent + 2))
        s += '{0} Body:\n{1}\n'.format(
            prefix, self.body.dump(indent + 2))
        return s

    def codegen(self, generator):
        # Output this as:
        #   var = alloca double
        #   ...
        #   start = startexpr
        #   store start -> var
        #   goto loop
        # loop:
        #   ...
        #   bodyexpr
        #   ...
        # loopend:
        #   step = stepexpr
        #   endcond = endexpr
        #   curvar = load var
        #   nextvariable = curvar + step
        #   store nextvar -> var
        #   br endcond, loop, afterloop
        # afterloop:

        # Create an alloca for the induction var. Save and restore location of
        # our builder because _create_entry_block_alloca may modify it (llvmlite
        # issue #44).
        saved_block = generator.getBuilder().block
        var_addr = generator._create_entry_block_alloca(self.id_name)
        generator.getBuilder().position_at_end(saved_block)

        # Emit the start expr first, without the variable in scope. Store it
        # into the var.
        start_val = self.start_expr.codegen(generator)
        generator.getBuilder().store(start_val, var_addr)
        loop_bb = generator.getBuilder().function.append_basic_block('loop')

        # Insert an explicit fall through from the current block to loop_bb
        generator.getBuilder().branch(loop_bb)
        generator.getBuilder().position_at_start(loop_bb)

        # Within the loop, the variable now refers to our alloca slot. If it
        # shadows an existing variable, we'll have to restore, so save it now.
        old_var_addr = generator.func_symtab.get(self.id_name)
        generator.func_symtab[self.id_name] = var_addr

        # Emit the body of the loop. This, like any other expr, can change the
        # current BB. Note that we ignore the value computed by the body.
        body_val = self.body.codegen(generator)

        # Compute the end condition
        endcond = self.end_expr.codegen(generator)
        cmp = generator.getBuilder().fcmp_ordered(
            '!=', endcond, ir.Constant(ir.DoubleType(), 0.0),
            'loopcond')

        if self.step_expr is None:
            stepval = ir.Constant(ir.DoubleType(), 1.0)
        else:
            stepval = self.step_expr.codegen(generator)
        cur_var = generator.getBuilder().load(var_addr, self.id_name)
        nextval = generator.getBuilder().fadd(cur_var, stepval, 'nextvar')
        generator.getBuilder().store(nextval, var_addr)

        # Create the 'after loop' block and insert it
        after_bb = generator.getBuilder().function.append_basic_block('afterloop')

        # Insert the conditional branch into the end of loop_end_bb
        generator.getBuilder().cbranch(cmp, loop_bb, after_bb)

        # New code will be inserted into after_bb
        generator.getBuilder().position_at_start(after_bb)

        # Restore the old var address if it was shadowed.
        if old_var_addr is not None:
            generator.func_symtab[self.id_name] = old_var_addr
        else:
            del generator.func_symtab[self.id_name]

        # The 'for' expression always returns 0
        return ir.Constant(ir.DoubleType(), 0.0)