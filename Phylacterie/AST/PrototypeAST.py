from .ASTNode import ASTNode
from .CodegenError import CodegenError

import llvmlite.ir as ir
import llvmlite.binding as llvm

class PrototypeAST(ASTNode):
    def __init__(self, parent, name, arguments, isoperator, prec, returnType):
        self.name = name
        self.argnames = [i['name'] for i in arguments]
        self.isoperator = isoperator
        self.prec = prec
        self.parent = parent
        self.returnType = returnType
        self.parameterTypes =  [i['type'] for i in arguments]

    def is_unary_op(self):
        return self.isoperator and len(self.argnames) == 1

    def is_binary_op(self):
        return self.isoperator and len(self.argnames) == 2

    def get_op_name(self):
        assert self.isoperator
        return self.name[-1]

    def dump(self, indent=0):
        s = '{0}{1} {2}({3})'.format(
            ' ' * indent, self.__class__.__name__, self.name,
            ', '.join(self.argnames))
        if self.isoperator:
            s += '[operator with prec={0}]'.format(self.prec)
        return s

    def codegen(self,generator):
        funcname = self.name
        # Create a function type
        func_ty = ir.FunctionType(self.returnType,  self.parameterTypes)

        # If a function with this name already exists in the module...
        if funcname in generator.getModule().globals:
            # We only allow the case in which a declaration exists and now the
            # function is defined (or redeclared) with the same number of args.
            existing_func = generator.getModule().globals[funcname]
            if not isinstance(existing_func, ir.Function):
                raise CodegenError('Function/Global name collision', funcname)
            if not existing_func.is_declaration:
                raise CodegenError('Redifinition of {0}'.format(funcname))
            if len(existing_func.function_type.args) != len(func_ty.args):
                raise CodegenError(
                    'Redifinition with different number of arguments')
            func = generator.getModule().globals[funcname]
        else:
            # Otherwise create a new function
            func = ir.Function(generator.getModule(), func_ty, funcname)
        return func