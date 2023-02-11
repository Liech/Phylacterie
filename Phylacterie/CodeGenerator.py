
import llvmlite.ir as ir
import llvmlite.binding as llvm

from .AST import *
from .irType2string import *

class CodeGenerator(object):
    def __init__(self):
        self._module = ir.Module()
        self._builder = None;
        self._func_symtab = {}
        self._symStack = [];
        self._builderStack = [];
        self._variableTypes = {}

    def getVariableType(self, name):
      return self._variableTypes[name];

    def registerVariableType(self, name, type):      
        self._variableTypes[name] = type;

    def setBuilder(self, builder):
      self._builder = builder;

    def getBuilder(self):
      return self._builder;

    def getModule(self):
      return self._module

    def generate_code(self, node):
        return node.codegen(self)

    def getSymtab(self):
      return self._func_symtab;

    def setSymtab(self, newSymtab):
      self._func_symtab = newSymtab;

    def storeSymtab(self):
      self._symStack.append(self._func_symtab);
      self._symStack = [];

    def popSymtab(self):
      if (len(self._symStack) > 0):
        self._func_symtab = self._symStack[-1];
        self._symStack = self._symStack[:-1] 

    def storeBuilder(self):
      self._builderStack.append(self.getBuilder())
      self._builder = None;

    def popBuilder(self):
      self._builder = self._builderStack[-1];
      self._builderStack = self._builderStack[:-1] 

    def defineVariable(self, name, value):
        saved_block = self._builder.block
        var_addr = self._create_entry_block_alloca(name, value.type)
        self._builder.position_at_end(saved_block)
        self._variableTypes[name] = irType2string(value.type);
        self._builder.store(value, var_addr)
        
        result = self.getSymtab().get(name);
        self.getSymtab()[name] = var_addr

        return result;

    def _create_entry_block_alloca(self, name, datatype):
        _builder = ir.IRBuilder()
        _builder.position_at_start(self._builder.function.entry_basic_block)
        return self._builder.alloca(datatype, size=None, name=name)
