from .TypeContainer import TypeContainer
from .VariableContainer import VariableContainer
from .ClassContainer import ClassContainer

class Core(object):    
    def __init__(self):
      self.typeContainer = TypeContainer(self);
      self.variables     = VariableContainer();
      self.classes       = ClassContainer();

    def stack(self):
      self.typeContainer.stack();
      self.variables.stack();

    def pop(self):
      self.typeContainer.pop();
      self.variables.pop();