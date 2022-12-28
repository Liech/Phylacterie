from .ExprAST import ExprAST

class UnaryExprAST(ExprAST):
    def __init__(self, op, operand):
        self.op = op
        self.operand = operand

    def dump(self, indent=0):
        s = '{0}{1}[{2}]\n'.format(
            ' ' * indent, self.__class__.__name__, self.op)
        s += self.operand.dump(indent + 2)
        return s
