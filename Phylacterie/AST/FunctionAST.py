from .ASTNode import ASTNode
from .PrototypeAST import PrototypeAST
from .ScopeAST import ScopeAST
from ..string2irType import string2irType
from irType2string import irType2string
from .Token import *

import llvmlite.ir as ir
import llvmlite.binding as llvm

class FunctionAST(ASTNode):
    def __init__(self, parent, proto, body, typeVault):
        self.proto = proto
        self.body = body
        self.parent = parent
        self.typeVault = typeVault
        self.types = {}

    _anonymous_function_counter = 0

    @classmethod
    def create_anonymous(klass,parent, expr, typeVault):
        """Create an anonymous function to hold an expression."""
        klass._anonymous_function_counter += 1
        return klass(parent,PrototypeAST(parent, '_anon{0}'.format(klass._anonymous_function_counter),[], False,0,expr.getReturnType(),typeVault),expr,typeVault)

    def is_anonymous(self):
        return self.proto.name.startswith('_anon')

    def dump(self, indent=0):
        s = '{0}{1}[{2}]\n'.format(
            ' ' * indent, self.__class__.__name__, self.proto.dump())
        s += self.body.dump(indent + 2) + '\n'
        return s

    def parse(parser, parent,typeVault):
        parser._get_next_token()  # consume 'def'
        typeVault.stack();
        proto = PrototypeAST.parse(parser,parent,typeVault);
        expr = ScopeAST.parse(parser,parent,typeVault);
        result = FunctionAST(parent, proto, expr,typeVault)
        result.types = typeVault.getTypes()
        typ = typeVault.getType(proto.getID())
        typeVault.pop()
        typeVault.registerType(proto.getID(),typ)
        return result

    def codegen(self, generator):
        # Reset the symbol table. Prototype generation will pre-populate it with
        # function arguments.
        self.typeVault.setTypes(self.types);
        generator.storeSymtab();
        generator.storeBuilder();
        
        # Create the function skeleton from the prototype.
        func = self.proto.codegen(generator)
        # Create the entry BB in the function and set the builder to it.
        bb_entry = func.append_basic_block('entry')
        generator.setBuilder(ir.IRBuilder(bb_entry));
                
        # Add all arguments to the symbol table and create their allocas
        for i, arg in enumerate(func.args):
            arg.name = self.proto.argnames[i]
            alloca = generator.getBuilder().alloca(self.proto.parameterTypes[i], name=arg.name)
            generator.getBuilder().store(arg, alloca)
            generator.getSymtab()[arg.name] = alloca

        retval = self.body.codegen(generator)
        generator.getBuilder().ret(retval)
        generator.popSymtab();
        generator.popBuilder();
        self.typeVault.pop();
        return func
