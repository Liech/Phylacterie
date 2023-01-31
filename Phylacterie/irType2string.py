
import llvmlite.ir as ir
import llvmlite.binding as llvm

from ctypes import CFUNCTYPE, c_bool, c_double


def irType2string(irType):
  if irType == ir.IntType(1):
    return 'bool';
  elif irType == ir.IntType(32):
    return 'int';
  elif irType == ir.DoubleType():
    return 'double';
  else:
    raise ""