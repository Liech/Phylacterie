from .ExprAST import ExprAST
from .Token import *
from string2irType import string2irType
from ParseError import ParseError

import llvmlite.ir as ir
import llvmlite.binding as llvm

class VarExprAST(ExprAST):
    def __init__(self,parent, var, core):
        # vars is a sequence of (name, init) pairs
        self.var = var
        self.parent = parent
        self.core = core

    def getSyntax(self):
      return ['Type', 'identifier', '=', 'Expression'];

    def dump(self, indent=0):
        prefix = ' ' * indent
        s = '{0}{1}\n'.format(prefix, self.__class__.__name__)
        for name, init, datatype in [self.var]:
            s += '{0} {1}'.format(prefix, name)
            if init is None:
                s += '\n'
            else:
                s += '=\n' + init.dump(indent+2) + '\n'
        return s

    def parse(parser, parent, datatype,varName, core):
        vars = []

        # Parse the optional initializer
        if parser._cur_tok_is_operator('='):
            parser._get_next_token()  # consume the '='
            init = parser._parse_expression(parent, core)
        else:
            init = None

        core.typeContainer.registerType(varName,datatype)
        core.variables.registerVar(varName, {})
        return VarExprAST(parent, (varName, init, datatype), core)

    def codegen(self, generator):
        old_bindings = []
        names = []

        for name, init, datatype in [self.var]:
            # Emit the initializer before adding the variable to scope. This
            # prefents the initializer from referencing the variable itgenerator.
            if init is not None:
                init_val = init.codegen(generator)
            else:
                init_val = datatype.getDefault(); 

            old = generator.defineVariable(name,init_val);
            if (not old is None):
              old_bindings.append(old);        
            names.append(name);
            lastInitValue = init_val;


        # Cleanup of variables is done by parent scope
        self.parent.addOldBindings(old_bindings);
        self.parent.addVarNames(names);
        
        return lastInitValue