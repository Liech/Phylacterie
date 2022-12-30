
import llvmlite.ir as ir
import llvmlite.binding as llvm

from ctypes import CFUNCTYPE, c_double
from .LLVMCodeGenerator import LLVMCodeGenerator
from .Parser import Parser
from .AST import *
from .BuiltIn import BuiltIn

class Phylacterie(object):
    def __init__(self):
        llvm.initialize()
        llvm.initialize_native_target()
        llvm.initialize_native_asmprinter()

        self.codegen = LLVMCodeGenerator()
        self.parser = Parser()
        self._add_builtins(self.codegen.module)

        self.target = llvm.Target.from_default_triple()
        self.evaluate('def binary ; 1 (x y) {y}');


        # basic sanity tests
        self.evaluate('{1+1}');
        self.evaluate('var x = 1 { x*3 }');
        self.evaluate('if 1 then { 2 } else { 3 }')
        self.evaluate('for x = 1,x < 10, 1 { x }');


    def evaluate(self, codestr, optimize=True, llvmdump=False):
        expressions = self.parser.parse_toplevel(codestr)
        for ast in expressions:
            self.codegen.generate_code(ast)

        if llvmdump:
            print('======== Unoptimized LLVM IR')
            print(str(self.codegen.module))

        if not (isinstance(ast, FunctionAST) and ast.is_anonymous()):
            return None

        # Convert LLVM IR into in-memory representation
        llvmmod = llvm.parse_assembly(str(self.codegen.module))

        if optimize:
            pmb = llvm.create_pass_manager_builder()
            pmb.opt_level = 2
            pm = llvm.create_module_pass_manager()
            pmb.populate(pm)
            pm.run(llvmmod)

            if llvmdump:
                print('======== Optimized LLVM IR')
                print(str(llvmmod))

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
        for b in BuiltIn:
          b(self,module);