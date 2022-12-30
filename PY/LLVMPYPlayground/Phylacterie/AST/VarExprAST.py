from .ExprAST import ExprAST

import llvmlite.ir as ir
import llvmlite.binding as llvm

class VarExprAST(ExprAST):
    def __init__(self,parent, vars, body):
        # vars is a sequence of (name, init) pairs
        self.vars = vars
        self.body = body
        self.parent = parent

    def dump(self, indent=0):
        prefix = ' ' * indent
        s = '{0}{1}\n'.format(prefix, self.__class__.__name__)
        for name, init in self.vars:
            s += '{0} {1}'.format(prefix, name)
            if init is None:
                s += '\n'
            else:
                s += '=\n' + init.dump(indent+2) + '\n'
        s += '{0} Body:\n'.format(prefix)
        s += self.body.dump(indent + 2)
        return s

    def codegen(self, generator):
        old_bindings = []

        for name, init in self.vars:
            # Emit the initializer before adding the variable to scope. This
            # prefents the initializer from referencing the variable itgenerator.
            if init is not None:
                init_val = init.codegen(generator)
            else:
                init_val = ir.Constant(ir.DoubleType(), 0.0)

            # Create an alloca for the induction var and store the init value to
            # it. Save and restore location of our builder because
            # _create_entry_block_alloca may modify it (llvmlite issue #44).
            saved_block = generator.builder.block
            var_addr = generator._create_entry_block_alloca(name)
            generator.builder.position_at_end(saved_block)
            generator.builder.store(init_val, var_addr)

            # We're going to shadow this name in the symbol table now; remember
            # what to restore.
            old_bindings.append(generator.func_symtab.get(name))
            generator.func_symtab[name] = var_addr
        

        # Cleanup of variables is done by parent scope
        self.parent.addOldBindings(old_bindings);
        self.parent.addVars(self.vars);

        return self.body.codegen(generator)