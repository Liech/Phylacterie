from .ExprAST import ExprAST
from .Token import *

from .Token import TokenKind

import llvmlite.ir as ir
import llvmlite.binding as llvm

class ScopeAST(ExprAST):
    def __init__(self, parent, body, typeVault):
        self.body = body
        self.parent = parent
        self.varNames = []
        self.oldBindings = []
        self.isGlobalScope = False;
        self.typeVault = typeVault
        self.types = {}

    def isScope(self):
      return True;

    def setIsGlobalScope(self,isGlobal):
      self.isGlobalScope = isGlobal;

    def setBody(self, newBody):
      self.body = newBody;

    def addVarNames(self, newVars):
      self.varNames.extend(newVars);

    def addOldBindings(self, oldBindings):
      self.oldBindings = oldBindings;

    def dump(self, indent=0):
        prefix = ' ' * indent
        s = '{0}{1}\n'.format(prefix, self.__class__.__name__)
        s += '{0} Body:\n'.format(prefix)
        s += self.body.dump(indent + 2)
        return s
      
    def getReturnType(self):
      if (len(self.body) == 0):
        return self.body.getReturnType();
      else:
        return self.body[-1].getReturnType();

    def parse(parser, parent,typeVault):
        result = ScopeAST(parent,None,typeVault);
        parser._match(TokenKind.SCOPESTART);
        
        body = []
        while parser.cur_tok.kind != TokenKind.SCOPEEND:
          body.append(parser._parse_expression(result,typeVault));

        parser._match(TokenKind.SCOPEEND);
        result.setBody(body);
        result.types = typeVault.getTypes()
        return result;

    def codegen(self, generator):      
        self.typeVault.setTypes(self.types)
        result = None;        
        # root scope may have multiple expressions (Hacky thing that should be replaced)
        if type(self.body) == list:
          for body in self.body:
            result = body.codegen(generator);
        else:
          result = self.body.codegen(generator)

        # Restore the old bindings.
        for i, name in enumerate(self.varNames):
            if len(self.oldBindings) > 0 and self.oldBindings[i] is not None:
                generator.getSymtab()[name] = self.oldBindings[i]
            else:
                del generator.getSymtab()[name]
                
        self.typeVault.pop();
        return result