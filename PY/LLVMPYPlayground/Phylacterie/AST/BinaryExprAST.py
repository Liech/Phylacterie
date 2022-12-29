from .ExprAST import ExprAST
from .VariableExprAST import VariableExprAST
from .CodegenError import CodegenError

import llvmlite.ir as ir
import llvmlite.binding as llvm

class BinaryExprAST(ExprAST):
    def __init__(self, op, lhs, rhs):
        self.op = op
        self.lhs = lhs
        self.rhs = rhs

    def dump(self, indent=0):
        s = '{0}{1}[{2}]\n'.format(
            ' ' * indent, self.__class__.__name__, self.op)
        s += self.lhs.dump(indent + 2) + '\n'
        s += self.rhs.dump(indent + 2)
        return s

    def codegen(self, generator):
        # Assignment is handled specially because it doesn't follow the general
        # recipe of binary ops.
        if self.op == '=':
            if not isinstance(self.lhs, VariableExprAST):
                raise CodegenError('lhs of "=" must be a variable')
            var_addr = generator.func_symtab[self.lhs.name]
            rhs_val = self.rhs.codegen(generator)
            generator.builder.store(rhs_val, var_addr)
            return rhs_val

        lhs = self.lhs.codegen(generator)
        rhs = self.rhs.codegen(generator)

        if self.op == '+':
            return generator.builder.fadd(lhs, rhs, 'addtmp')
        elif self.op == '-':
            return generator.builder.fsub(lhs, rhs, 'subtmp')
        elif self.op == '*':
            return generator.builder.fmul(lhs, rhs, 'multmp')
        elif self.op == '<':
            cmp = generator.builder.fcmp_unordered('<', lhs, rhs, 'cmptmp')
            return generator.builder.uitofp(cmp, ir.DoubleType(), 'booltmp')
        else:
            # Note one of predefined operator, so it must be a user-defined one.
            # Emit a call to it.
            func = generator.module.get_global('binary{0}'.format(self.op))
            return generator.builder.call(func, [lhs, rhs], 'binop')