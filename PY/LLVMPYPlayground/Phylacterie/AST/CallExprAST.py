from .ExprAST import ExprAST
from .CodegenError import CodegenError

import llvmlite.ir as ir
import llvmlite.binding as llvm

class CallExprAST(ExprAST):
    def __init__(self, parent, callee, args):
        self.callee = callee
        self.args = args
        self.parent = parent

    def dump(self, indent=0):
        s = '{0}{1}[{2}]\n'.format(
            ' ' * indent, self.__class__.__name__, self.callee)
        for arg in self.args:
            s += arg.dump(indent + 2) + '\n'
        return s[:-1]  # snip out trailing '\n'

    def codegen(self, generator):
        callee_func = generator.module.get_global(self.callee)
        if callee_func is None or not isinstance(callee_func, ir.Function):
            raise CodegenError('Call to unknown function', self.callee)
        if len(callee_func.args) != len(self.args):
            raise CodegenError('Call argument length mismatch', self.callee)
        call_args = [arg.codegen(generator) for arg in self.args]
        return generator.builder.call(callee_func, call_args, 'calltmp')