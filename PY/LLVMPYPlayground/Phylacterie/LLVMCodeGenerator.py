
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
        return self._codegen(node)

    def _create_entry_block_alloca(self, name):
        """Create an alloca in the entry BB of the current function."""
        builder = ir.IRBuilder()
        builder.position_at_start(self.builder.function.entry_basic_block)
        return builder.alloca(ir.DoubleType(), size=None, name=name)

    def _codegen(self, node):
        """Node visitor. Dispathces upon node type.

        For AST node of class Foo, calls self._codegen_Foo. Each visitor is
        expected to return a llvmlite.ir.Value.
        """
        method = '_codegen_' + node.__class__.__name__
        return getattr(self, method)(node)

    def _codegen_NumberExprAST(self, node):
        return node.codegen(self);

    def _codegen_VariableExprAST(self, node):
        return node.codegen(self);

    def _codegen_UnaryExprAST(self, node):
        return node.codegen(self);

    def _codegen_BinaryExprAST(self, node):
        return node.codegen(self);

    def _codegen_IfExprAST(self, node):
        return node.codegen(self)

    def _codegen_ForExprAST(self, node):
        return node.codegen(self)

    def _codegen_VarExprAST(self, node):
        return node.codegen(self)

    def _codegen_CallExprAST(self, node):
        return node.codegen(self)

    def _codegen_PrototypeAST(self, node):
        return node.codegen(self)

    def _codegen_FunctionAST(self, node):
        return node.codegen(self)