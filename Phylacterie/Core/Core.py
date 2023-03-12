from sqlite3 import OperationalError
from .TypeContainer import TypeContainer
from .VariableContainer import VariableContainer
from .ClassContainer import ClassContainer
from .OperatorContainer import OperatorContainer

class Core(object):    
    def __init__(self):
      self.variables     = VariableContainer();
      self.classes       = ClassContainer();
      self.typeContainer = TypeContainer(self);
      self.operators     = OperatorContainer();

    def stack(self):
      self.typeContainer.stack();
      self.variables.stack();

    def pop(self):
      self.typeContainer.pop();
      self.variables.pop();