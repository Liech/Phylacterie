
import llvmlite.ir as ir
import llvmlite.binding as llvm

from .AST import *

class CodeGenerator(object):
    def __init__(self):
        """Initialize the code generator.

        This creates a new LLVM module into which code is generated. The
        generate_code() method can be called multiple times. It adds the code
        generated for this node into the module, and returns the IR value for
        the node.

        At any time, the current LLVM module being constructed can be obtained
        from the module attribute.
        """
        self._module = ir.Module()

        # Current IR builder.
        self._builder = None

        # Manages a symbol table while a function is being codegen'd. Maps var
        # names to ir.Value which represents the var's address (alloca).
        self.func_symtab = {}

    def setBuilder(self, builder):
      self._builder = builder;

    def getBuilder(self):
      return self._builder;

    def getModule(self):
      return self._module

    def generate_code(self, node):
        return node.codegen(self)

    def defineVariable(self, name, value):
        # Create an alloca for the induction var and store the init value to
        # it. Save and restore location of our builder because
        # _create_entry_block_alloca may modify it (llvmlite issue #44).
        saved_block = self._builder.block
        var_addr = self._create_entry_block_alloca(name)
        self._builder.position_at_end(saved_block)
        self._builder.store(value, var_addr)
        
        # We're going to shadow this name in the symbol table now; remember
        # what to restore.
        result = self.func_symtab.get(name);
        self.func_symtab[name] = var_addr

        return result;

    def _create_entry_block_alloca(self, name):
        """Create an alloca in the entry BB of the current function."""
        _builder = ir.IRBuilder()
        _builder.position_at_start(self._builder.function.entry_basic_block)
        return _builder.alloca(ir.DoubleType(), size=None, name=name)
