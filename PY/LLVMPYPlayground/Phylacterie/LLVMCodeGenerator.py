
import llvmlite.ir as ir
import llvmlite.binding as llvm

from .AST import *

class LLVMCodeGenerator(object):
    def __init__(self):
        """Initialize the code generator.

        This creates a new LLVM module into which code is generated. The
        generate_code() method can be called multiple times. It adds the code
        generated for this node into the module, and returns the IR value for
        the node.

        At any time, the current LLVM module being constructed can be obtained
        from the module attribute.
        """
        self.module = ir.Module()

        # Current IR builder.
        self.builder = None

        # Manages a symbol table while a function is being codegen'd. Maps var
        # names to ir.Value which represents the var's address (alloca).
        self.func_symtab = {}

    def generate_code(self, node):
        assert isinstance(node, (PrototypeAST, FunctionAST))
        return self._codegen(node)

    def _create_entry_block_alloca(self, name):
        """Create an alloca in the entry BB of the current function."""
        builder = ir.IRBuilder()
        builder.position_at_start(self.builder.function.entry_basic_block)
        return builder.alloca(ir.DoubleType(), size=None, name=name)

    def _codegen(self, node):
        """Node visitor. Dispathces upon node type.

        For AST node of class Foo, calls self._codegen_Foo. Each visitor is
        expected to return a llvmlite.ir.Value.
        """
        method = '_codegen_' + node.__class__.__name__
        return getattr(self, method)(node)

    def _codegen_NumberExprAST(self, node):
        return ir.Constant(ir.DoubleType(), float(node.val))

    def _codegen_VariableExprAST(self, node):
        var_addr = self.func_symtab[node.name]
        return self.builder.load(var_addr, node.name)

    def _codegen_UnaryExprAST(self, node):
        operand = self._codegen(node.operand)
        func = self.module.get_global('unary{0}'.format(node.op))
        return self.builder.call(func, [operand], 'unop')

    def _codegen_BinaryExprAST(self, node):
        # Assignment is handled specially because it doesn't follow the general
        # recipe of binary ops.
        if node.op == '=':
            if not isinstance(node.lhs, VariableExprAST):
                raise CodegenError('lhs of "=" must be a variable')
            var_addr = self.func_symtab[node.lhs.name]
            rhs_val = self._codegen(node.rhs)
            self.builder.store(rhs_val, var_addr)
            return rhs_val

        lhs = self._codegen(node.lhs)
        rhs = self._codegen(node.rhs)

        if node.op == '+':
            return self.builder.fadd(lhs, rhs, 'addtmp')
        elif node.op == '-':
            return self.builder.fsub(lhs, rhs, 'subtmp')
        elif node.op == '*':
            return self.builder.fmul(lhs, rhs, 'multmp')
        elif node.op == '<':
            cmp = self.builder.fcmp_unordered('<', lhs, rhs, 'cmptmp')
            return self.builder.uitofp(cmp, ir.DoubleType(), 'booltmp')
        else:
            # Note one of predefined operator, so it must be a user-defined one.
            # Emit a call to it.
            func = self.module.get_global('binary{0}'.format(node.op))
            return self.builder.call(func, [lhs, rhs], 'binop')

    def _codegen_IfExprAST(self, node):
        # Emit comparison value
        cond_val = self._codegen(node.cond_expr)
        cmp = self.builder.fcmp_ordered(
            '!=', cond_val, ir.Constant(ir.DoubleType(), 0.0))

        # Create basic blocks to express the control flow, with a conditional
        # branch to either then_bb or else_bb depending on cmp. else_bb and
        # merge_bb are not yet attached to the function's list of BBs because
        # if a nested IfExpr is generated we want to have a reasonably nested
        # order of BBs generated into the function.
        then_bb = self.builder.function.append_basic_block('then')
        else_bb = ir.Block(self.builder.function, 'else')
        merge_bb = ir.Block(self.builder.function, 'ifcont')
        self.builder.cbranch(cmp, then_bb, else_bb)

        # Emit the 'then' part
        self.builder.position_at_start(then_bb)
        then_val = self._codegen(node.then_expr)
        self.builder.branch(merge_bb)

        # Emission of then_val could have modified the current basic block. To
        # properly set up the PHI, remember which block the 'then' part ends in.
        then_bb = self.builder.block

        # Emit the 'else' part
        self.builder.function.basic_blocks.append(else_bb)
        self.builder.position_at_start(else_bb)
        else_val = self._codegen(node.else_expr)

        # Emission of else_val could have modified the current basic block.
        else_bb = self.builder.block
        self.builder.branch(merge_bb)

        # Emit the merge ('ifcnt') block
        self.builder.function.basic_blocks.append(merge_bb)
        self.builder.position_at_start(merge_bb)
        phi = self.builder.phi(ir.DoubleType(), 'iftmp')
        phi.add_incoming(then_val, then_bb)
        phi.add_incoming(else_val, else_bb)
        return phi

    def _codegen_ForExprAST(self, node):
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
        saved_block = self.builder.block
        var_addr = self._create_entry_block_alloca(node.id_name)
        self.builder.position_at_end(saved_block)

        # Emit the start expr first, without the variable in scope. Store it
        # into the var.
        start_val = self._codegen(node.start_expr)
        self.builder.store(start_val, var_addr)
        loop_bb = self.builder.function.append_basic_block('loop')

        # Insert an explicit fall through from the current block to loop_bb
        self.builder.branch(loop_bb)
        self.builder.position_at_start(loop_bb)

        # Within the loop, the variable now refers to our alloca slot. If it
        # shadows an existing variable, we'll have to restore, so save it now.
        old_var_addr = self.func_symtab.get(node.id_name)
        self.func_symtab[node.id_name] = var_addr

        # Emit the body of the loop. This, like any other expr, can change the
        # current BB. Note that we ignore the value computed by the body.
        body_val = self._codegen(node.body)

        # Compute the end condition
        endcond = self._codegen(node.end_expr)
        cmp = self.builder.fcmp_ordered(
            '!=', endcond, ir.Constant(ir.DoubleType(), 0.0),
            'loopcond')

        if node.step_expr is None:
            stepval = ir.Constant(ir.DoubleType(), 1.0)
        else:
            stepval = self._codegen(node.step_expr)
        cur_var = self.builder.load(var_addr, node.id_name)
        nextval = self.builder.fadd(cur_var, stepval, 'nextvar')
        self.builder.store(nextval, var_addr)

        # Create the 'after loop' block and insert it
        after_bb = self.builder.function.append_basic_block('afterloop')

        # Insert the conditional branch into the end of loop_end_bb
        self.builder.cbranch(cmp, loop_bb, after_bb)

        # New code will be inserted into after_bb
        self.builder.position_at_start(after_bb)

        # Restore the old var address if it was shadowed.
        if old_var_addr is not None:
            self.func_symtab[node.id_name] = old_var_addr
        else:
            del self.func_symtab[node.id_name]

        # The 'for' expression always returns 0
        return ir.Constant(ir.DoubleType(), 0.0)

    def _codegen_VarExprAST(self, node):
        old_bindings = []

        for name, init in node.vars:
            # Emit the initializer before adding the variable to scope. This
            # prefents the initializer from referencing the variable itself.
            if init is not None:
                init_val = self._codegen(init)
            else:
                init_val = ir.Constant(ir.DoubleType(), 0.0)

            # Create an alloca for the induction var and store the init value to
            # it. Save and restore location of our builder because
            # _create_entry_block_alloca may modify it (llvmlite issue #44).
            saved_block = self.builder.block
            var_addr = self._create_entry_block_alloca(name)
            self.builder.position_at_end(saved_block)
            self.builder.store(init_val, var_addr)

            # We're going to shadow this name in the symbol table now; remember
            # what to restore.
            old_bindings.append(self.func_symtab.get(name))
            self.func_symtab[name] = var_addr

        # Now all the vars are in scope. Codegen the body.
        body_val = self._codegen(node.body)

        # Restore the old bindings.
        for i, (name, _) in enumerate(node.vars):
            if old_bindings[i] is not None:
                self.func_symtab[name] = old_bindings[i]
            else:
                del self.func_symtab[name]

        return body_val

    def _codegen_CallExprAST(self, node):
        callee_func = self.module.get_global(node.callee)
        if callee_func is None or not isinstance(callee_func, ir.Function):
            raise CodegenError('Call to unknown function', node.callee)
        if len(callee_func.args) != len(node.args):
            raise CodegenError('Call argument length mismatch', node.callee)
        call_args = [self._codegen(arg) for arg in node.args]
        return self.builder.call(callee_func, call_args, 'calltmp')

    def _codegen_PrototypeAST(self, node):
        funcname = node.name
        # Create a function type
        func_ty = ir.FunctionType(ir.DoubleType(),
                                  [ir.DoubleType()] * len(node.argnames))

        # If a function with this name already exists in the module...
        if funcname in self.module.globals:
            # We only allow the case in which a declaration exists and now the
            # function is defined (or redeclared) with the same number of args.
            existing_func = self.module[funcname]
            if not isinstance(existing_func, ir.Function):
                raise CodegenError('Function/Global name collision', funcname)
            if not existing_func.is_declaration():
                raise CodegenError('Redifinition of {0}'.format(funcname))
            if len(existing_func.function_type.args) != len(func_ty.args):
                raise CodegenError(
                    'Redifinition with different number of arguments')
            func = self.module.globals[funcname]
        else:
            # Otherwise create a new function
            func = ir.Function(self.module, func_ty, funcname)
        return func

    def _codegen_FunctionAST(self, node):
        # Reset the symbol table. Prototype generation will pre-populate it with
        # function arguments.
        self.func_symtab = {}
        # Create the function skeleton from the prototype.
        func = self._codegen(node.proto)
        # Create the entry BB in the function and set the builder to it.
        bb_entry = func.append_basic_block('entry')
        self.builder = ir.IRBuilder(bb_entry)

        # Add all arguments to the symbol table and create their allocas
        for i, arg in enumerate(func.args):
            arg.name = node.proto.argnames[i]
            alloca = self.builder.alloca(ir.DoubleType(), name=arg.name)
            self.builder.store(arg, alloca)
            self.func_symtab[arg.name] = alloca

        retval = self._codegen(node.body)
        self.builder.ret(retval)
        return func
