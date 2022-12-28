from .ExprAST import ExprAST

class BinaryExprAST(ExprAST):
    def __init__(self, op, lhs, rhs):
        self.op = op
        self.lhs = lhs
        self.rhs = rhs

    def dump(self, indent=0):
        s = '{0}{1}[{2}]\n'.format(
            ' ' * indent, self.__class__.__name__, self.op)
        s += self.lhs.dump(indent + 2) + '\n'
        s += self.rhs.dump(indent + 2)
        return s

