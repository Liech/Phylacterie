
from AST import OperatorType


class OperatorContainer(object):  
  def __init__(self):
    self.precedence_map = {'=': 2, '<': 10, '+': 20, '-': 20, '*': 40, '.' : 50}
    self.operatorType =  {'=': OperatorType.LHAND, '<': OperatorType.BINARY, '+': OperatorType.BINARY, '-': OperatorType.BINARY, '*': OperatorType.BINARY, '.' : OperatorType.LHAND}

  def setOperatorType(self, operator, type):
    if (not operator in self.operatorType):
      return OperatorType.UNKNOWN;
    self.operatorType[operator] = type;

  def getOperatorType(self, operator):
    return self.operatorType[operator];

  def setPrecedence(self, operator, precedence):
    self.precedence_map[operator] = precedence;

  def getPrecedence(self, operator):
    if (operator in self.precedence_map):
      return self.precedence_map[operator];
    else:
      return -1;



