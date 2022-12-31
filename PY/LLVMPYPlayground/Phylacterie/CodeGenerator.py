
import llvmlite.ir as ir
import llvmlite.binding as llvm

from .AST import *

class CodeGenerator(object):
    def __init__(self):
        self._module = ir.Module()
        self._builder = None
        self._func_symtab = {}

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

    def defineVariable(self, name, value):
        saved_block = self._builder.block
        var_addr = self._create_entry_block_alloca(name)
        self._builder.position_at_end(saved_block)
        self._builder.store(value, var_addr)
        
        result = self.getSymtab().get(name);
        self.getSymtab()[name] = var_addr

        return result;

    def _create_entry_block_alloca(self, name):
        #_builder = ir.IRBuilder()
        #_builder.position_at_start(self._builder.function.entry_basic_block)
        return self._builder.alloca(ir.DoubleType(), size=None, name=name)
