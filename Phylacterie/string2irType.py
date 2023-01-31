
import llvmlite.ir as ir
import llvmlite.binding as llvm

from ctypes import CFUNCTYPE, c_bool, c_double


def string2irType(stringType):
  if stringType == 'double':
    return ir.DoubleType();
  elif stringType == 'bool':
    return ir.IntType(1);
  elif stringType == 'int':
    return ir.IntType(32);
  else:
    raise BaseException("unkown type")