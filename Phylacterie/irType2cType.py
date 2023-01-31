
import llvmlite.ir as ir
import llvmlite.binding as llvm

from ctypes import CFUNCTYPE, c_bool, c_double, c_int


def irType2cType(irType):
  if irType == ir.DoubleType():
    return c_double;
  if irType == ir.IntType(32):
    return c_int;
  elif irType == ir.IntType(1):
    return c_bool;
  else:
    raise ""