from .ExprAST import ExprAST

import llvmlite.ir as ir
import llvmlite.binding as llvm

class ScopeAST(ExprAST):
    def __init__(self, parent, body):
        self.body = body
        self.parent = parent
        self.localVars = []
        self.oldBindings = []
        self.isGlobalScope = False;

    def setIsGlobalScope(self,isGlobal):
      self.isGlobalScope = isGlobal;

    def setBody(self, newBody):
      self.body = newBody;

    def addVars(self, newVars):
      self.localVars.extend(newVars);

    def addOldBindings(self, oldBindings):
      self.oldBindings = oldBindings;

    def dump(self, indent=0):
        prefix = ' ' * indent
        s = '{0}{1}\n'.format(prefix, self.__class__.__name__)
        s += '{0} Body:\n'.format(prefix)
        s += self.body.dump(indent + 2)
        return s

    def codegen(self, generator):      
        result = None;
        #root scope may have multiple expressions (Hacky thing that should be replaced)
        if type(self.body) == list:
          for body in self.body:
            result = body.codegen(generator);
        else:
          result = self.body.codegen(generator)

        #if (not self.isGlobalScope):
        #  # Restore the old bindings.
        #  for i, (name, _) in enumerate(self.localVars):
        #      if self.oldBindings[i] is not None:
        #          generator.func_symtab[name] = self.oldBindings[i]
        #      else:
        #          del generator.func_symtab[name]
                
        return result