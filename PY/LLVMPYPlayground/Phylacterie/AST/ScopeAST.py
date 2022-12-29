from .ExprAST import ExprAST

class ScopeAST(ExprAST):
    def __init__(self, body):
        self.body = body

    def dump(self, indent=0):
        prefix = ' ' * indent
        s = '{0}{1}\n'.format(prefix, self.__class__.__name__)
        s += '{0} Body:\n'.format(prefix)
        s += self.body.dump(indent + 2)
        return s
