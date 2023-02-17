from .ASTNode import ASTNode
from .PrototypeAST import PrototypeAST
from .ScopeAST import ScopeAST
from irType2string import irType2string
from .Token import *
import Core

import llvmlite.ir as ir
import llvmlite.binding as llvm

class FunctionAST(ASTNode):
    def __init__(self, parent, proto, body, core):
        self.proto = proto
        self.body = body
        self.parent = parent
        self.core = core
        self.types = {}

    _anonymous_function_counter = 0
    
    def getSyntax(self):
      return ['def','Prototype','Scope']

    @classmethod
    def create_anonymous(klass,parent, expr, core):
        """Create an anonymous function to hold an expression."""
        klass._anonymous_function_counter += 1
        return klass(parent,PrototypeAST(parent, '_anon{0}'.format(klass._anonymous_function_counter),[], False,0,expr.getReturnType(),core),expr,core)

    def is_anonymous(self):
        return self.proto.name.startswith('_anon')

    def parse(parser, parent,datatype,name, core):
        core.stack();
        proto = PrototypeAST.parse(parser,parent,datatype,name,core);
        expr = ScopeAST.parse(parser,parent,core);
        result = FunctionAST(parent, proto, expr,core)
        result.types = core.typeContainer.getTypes()
        typ = core.typeContainer.getType(proto.getID())
        core.pop()
        core.typeContainer.registerType(proto.getID(),typ)
        
        parser.nextNeedsNoSemicolon();
        return result

    def codegen(self, generator):
        # Reset the symbol table. Prototype generation will pre-populate it with
        # function arguments.
        self.core.typeContainer.setTypes(self.types);
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
            alloca = generator.getBuilder().alloca(self.proto.parameterTypes[i].getIRType(), name=arg.name)
            generator.getBuilder().store(arg, alloca)
            generator.getSymtab()[arg.name] = alloca

        retval = self.body.codegen(generator)
        generator.getBuilder().ret(retval)
        generator.popSymtab();
        generator.popBuilder();
        self.core.typeContainer.pop();
        return func
