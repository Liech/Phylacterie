
import llvmlite.ir as ir

def _addPutchard(self, module):
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