
import llvmlite.ir as ir

class TypeContainer(object):
  def __init__(self):
    self._types = {}
    self._globalTypes = {}
    self._stack = []
    
    self._globalTypes['binary+_double_double_'] = ir.DoubleType();
    self._globalTypes['binary*_double_double_'] = ir.DoubleType();
    self._globalTypes['binary-_double_double_'] = ir.DoubleType();
    self._globalTypes['binary+_int_int_'] = ir.IntType(32);
    self._globalTypes['binary*_int_int_'] = ir.IntType(32);
    self._globalTypes['binary<_double_double_'] = ir.IntType(1);
    self._globalTypes['binary<_int_int_'] = ir.IntType(1);

  def getType(self, name):
    if (name in self._globalTypes):
      return self._globalTypes[name];
    return self._types[name];
  def registerType(self, name, type):      
      self._types[name] = type;
  def stack(self):
    self._stack.append(self._types)
    self._types = {};
  def pop(self):
    self._types = self._stack[-1]
    self._stack = self._stack[:-1]
  def setTypes(self,types):
    self.stack();
    self._types = types
  def getTypes(self):
    return self._types;
