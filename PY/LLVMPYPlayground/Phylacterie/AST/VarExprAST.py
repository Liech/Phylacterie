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
        names = []

        for name, init in self.vars:
            # Emit the initializer before adding the variable to scope. This
            # prefents the initializer from referencing the variable itgenerator.
            if init is not None:
                init_val = init.codegen(generator)
            else:
                init_val = ir.Constant(ir.DoubleType(), 0.0)

            old = generator.defineVariable(name,init_val);
            old_bindings.append(old);        
            names.append(name);

        # Cleanup of variables is done by parent scope
        self.parent.addOldBindings(old_bindings);
        self.parent.addVarNames(names);

        return self.body.codegen(generator)