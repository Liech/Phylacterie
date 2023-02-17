
class VariableContainer(object):
  def __init__(self):
    self._vars = {}
    self._stack = []

  def hasVar(self, name):
    return name in self._vars;
  def getVar(self, name):
    return self._vars[name];
  def registerVar(self, name, data):      
      self._vars[name] = type;
  def stack(self):
    self._stack.append(self._vars)
    self._vars = {};
  def pop(self):
    self._vars = self._stack[-1]
    self._stack = self._stack[:-1]
  def setVars(self,types):
    self.stack();
    self._vars = types
  def getVars(self):
    return self._vars;
