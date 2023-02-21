from .TypeContainer import TypeContainer
from .VariableContainer import VariableContainer
from .ClassContainer import ClassContainer

class Core(object):    
    def __init__(self):
      self.variables     = VariableContainer();
      self.classes       = ClassContainer();
      self.typeContainer = TypeContainer(self);

    def stack(self):
      self.typeContainer.stack();
      self.variables.stack();

    def pop(self):
      self.typeContainer.pop();
      self.variables.pop();