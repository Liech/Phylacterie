
import llvmlite.ir as ir
import llvmlite.binding as llvm

from .AST import *

class LLVMCodeGenerator(object):
    def __init__(self):
        """Initialize the code generator.

        This creates a new LLVM module into which code is generated. The
        generate_code() method can be called multiple times. It adds the code
        generated for this node into the module, and returns the IR value for
        the node.

        At any time, the current LLVM module being constructed can be obtained
        from the module attribute.
        """
        self.module = ir.Module()

        # Current IR builder.
        self.builder = None

        # Manages a symbol table while a function is being codegen'd. Maps var
        # names to ir.Value which represents the var's address (alloca).
        self.func_symtab = {}

    def generate_code(self, node):
        assert isinstance(node, (PrototypeAST, FunctionAST))
        return node.codegen(self)

    def _create_entry_block_alloca(self, name):
        """Create an alloca in the entry BB of the current function."""
        builder = ir.IRBuilder()
        builder.position_at_start(self.builder.function.entry_basic_block)
        return builder.alloca(ir.DoubleType(), size=None, name=name)
