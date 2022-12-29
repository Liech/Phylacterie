from .ASTNode import ASTNode
from .PrototypeAST import PrototypeAST

import llvmlite.ir as ir
import llvmlite.binding as llvm

class FunctionAST(ASTNode):
    def __init__(self, proto, body):
        self.proto = proto
        self.body = body

    _anonymous_function_counter = 0

    @classmethod
    def create_anonymous(klass, expr):
        """Create an anonymous function to hold an expression."""
        klass._anonymous_function_counter += 1
        return klass(
            PrototypeAST('_anon{0}'.format(klass._anonymous_function_counter),
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
        generator.func_symtab = {}
        # Create the function skeleton from the prototype.
        func = self.proto.codegen(generator)
        # Create the entry BB in the function and set the builder to it.
        bb_entry = func.append_basic_block('entry')
        generator.builder = ir.IRBuilder(bb_entry)

        # Add all arguments to the symbol table and create their allocas
        for i, arg in enumerate(func.args):
            arg.name = self.proto.argnames[i]
            alloca = generator.builder.alloca(ir.DoubleType(), name=arg.name)
            generator.builder.store(arg, alloca)
            generator.func_symtab[arg.name] = alloca

        retval = self.body.codegen(generator)
        generator.builder.ret(retval)
        return func
