
import llvmlite.ir as ir
import llvmlite.binding as llvm

from ctypes import CFUNCTYPE, c_bool, c_double


def irType2cType(irType):
  if irType == ir.DoubleType():
    return c_double;
  elif irType == ir.IntType(1):
    return c_bool;
  else:
    raise ""