
import llvmlite.ir as ir
import llvmlite.binding as llvm

from ctypes import CFUNCTYPE, c_double
from .LLVMCodeGenerator import LLVMCodeGenerator
from .Parser import Parser
from .AST import *

class LanguageEvaluator(object):
    """Evaluator for Kaleidoscope expressions.

    Once an object is created, calls to evaluate() add new expressions to the
    module. Definitions (including externs) are only added into the IR - no
    JIT compilation occurs. When a toplevel expression is evaluated, the whole
    module is JITed and the result of the expression is returned.
    """
    def __init__(self):
        llvm.initialize()
        llvm.initialize_native_target()
        llvm.initialize_native_asmprinter()

        self.codegen = LLVMCodeGenerator()
        self.parser = Parser()
        self._add_builtins(self.codegen.module)

        self.target = llvm.Target.from_default_triple()

    def evaluate(self, codestr, optimize=True, llvmdump=False):
        """Evaluate code in codestr.

        Returns None for definitions and externs, and the evaluated expression
        value for toplevel expressions.
        """
        # Parse the given code and generate code from it
        ast = self.parser.parse_toplevel(codestr)
        self.codegen.generate_code(ast)

        if llvmdump:
            print('======== Unoptimized LLVM IR')
            print(str(self.codegen.module))

        # If we're evaluating a definition or extern declaration, don't do
        # anything else. If we're evaluating an anonymous wrapper for a toplevel
        # expression, JIT-compile the module and run the function to get its
        # result.
        if not (isinstance(ast, FunctionAST) and ast.is_anonymous()):
            return None

        # Convert LLVM IR into in-memory representation
        llvmmod = llvm.parse_assembly(str(self.codegen.module))

        # Optimize the module
        if optimize:
            pmb = llvm.create_pass_manager_builder()
            pmb.opt_level = 2
            pm = llvm.create_module_pass_manager()
            pmb.populate(pm)
            pm.run(llvmmod)

            if llvmdump:
                print('======== Optimized LLVM IR')
                print(str(llvmmod))

        # Create a MCJIT execution engine to JIT-compile the module. Note that
        # ee takes ownership of target_machine, so it has to be recreated anew
        # each time we call create_mcjit_compiler.
        target_machine = self.target.create_target_machine()
        with llvm.create_mcjit_compiler(llvmmod, target_machine) as ee:
            ee.finalize_object()

            if llvmdump:
                print('======== Machine code')
                print(target_machine.emit_assembly(llvmmod))

            fptr = CFUNCTYPE(c_double)(ee.get_function_address(ast.proto.name))
            result = fptr()
            return result

    def compile_to_object_code(self):
        """Compile previously evaluated code into an object file.

        The object file is created for the native target, and its contents are
        returned as a bytes object.
        """
        # We use the small code model here, rather than the default one
        # `jitdefault`.
        #
        # The reason is that only ELF format is supported under the `jitdefault`
        # code model on Windows. However, COFF is commonly used by compilers on
        # Windows.
        #
        # Please refer to https://github.com/numba/llvmlite/issues/181
        # for more information about this issue.
        target_machine = self.target.create_target_machine(codemodel='small')

        # Convert LLVM IR into in-memory representation
        llvmmod = llvm.parse_assembly(str(self.codegen.module))
        return target_machine.emit_object(llvmmod)

    def _add_builtins(self, module):
        # The C++ tutorial adds putchard() simply by defining it in the host C++
        # code, which is then accessible to the JIT. It doesn't work as simply
        # for us; but luckily it's very easy to define new "C level" functions
        # for our JITed code to use - just emit them as LLVM IR. This is what
        # this method does.

        # Add the declaration of putchar
        putchar_ty = ir.FunctionType(ir.IntType(32), [ir.IntType(32)])
        putchar = ir.Function(module, putchar_ty, 'putchar')

        # Add putchard
        putchard_ty = ir.FunctionType(ir.DoubleType(), [ir.DoubleType()])
        putchard = ir.Function(module, putchard_ty, 'putchard')
        irbuilder = ir.IRBuilder(putchard.append_basic_block('entry'))
        ival = irbuilder.fptoui(putchard.args[0], ir.IntType(32), 'intcast')
        irbuilder.call(putchar, [ival])
        irbuilder.ret(ir.Constant(ir.DoubleType(), 0))

