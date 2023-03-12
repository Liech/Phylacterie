


class OperatorContainer(object):  
  def __init__(self):
    self.precedence_map = {'=': 2, '<': 10, '+': 20, '-': 20, '*': 40, '.' : 50}


  def setPrecedence(self, operator, precedence):
    self.precedence_map[operator] = precedence;

  def getPrecedence(self, operator):
    if (operator in self.precedence_map):
      return self.precedence_map[operator];
    else:
      return -1;



