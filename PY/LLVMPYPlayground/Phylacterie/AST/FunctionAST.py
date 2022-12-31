from .ASTNode import ASTNode
from .PrototypeAST import PrototypeAST

import llvmlite.ir as ir
import llvmlite.binding as llvm

class FunctionAST(ASTNode):
    def __init__(self, parent, proto, body):
        self.proto = proto
        self.body = body
        self.parent = parent

    _anonymous_function_counter = 0

    @classmethod
    def create_anonymous(klass,parent, expr):
        """Create an anonymous function to hold an expression."""
        klass._anonymous_function_counter += 1
        return klass(parent,
            PrototypeAST(parent, '_anon{0}'.format(klass._anonymous_function_counter),
                         []),
            expr)

    def is_anonymous(self):
        return self.proto.name.startswith('_anon')

    def dump(self, indent=0):
        s = '{0}{1}[{2}]\n'.format(
            ' ' * indent, self.__class__.__name__, self.proto.dump())
        s += self.body.dump(indent + 2) + '\n'
        return s

    def codegen(self, generator):
        # Reset the symbol table. Prototype generation will pre-populate it with
        # function arguments.
        #generator.setSymtab({});

        # Create the function skeleton from the prototype.
        func = self.proto.codegen(generator)
        # Create the entry BB in the function and set the builder to it.
        bb_entry = func.append_basic_block('entry')
        generator.setBuilder(ir.IRBuilder(bb_entry));
        
        old_bindings = []
        names = []

        for i, arg in enumerate(func.args):
            arg.name = self.proto.argnames[i]

            old = generator.defineVariable(arg.name,arg);
            old_bindings.append(old);        
            names.append(arg.name);


        scope = self.body;
        if (not scope.isScope()):
          scope = self.parent;

        scope.addOldBindings(old_bindings);
        scope.addVarNames(names);
        
        retval = self.body.codegen(generator)
        generator.getBuilder().ret(retval)
        return func
