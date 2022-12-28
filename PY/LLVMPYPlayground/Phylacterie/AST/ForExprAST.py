from .ExprAST import ExprAST

class ForExprAST(ExprAST):
    def __init__(self, id_name, start_expr, end_expr, step_expr, body):
        self.id_name = id_name
        self.start_expr = start_expr
        self.end_expr = end_expr
        self.step_expr = step_expr
        self.body = body

    def dump(self, indent=0):
        prefix = ' ' * indent
        s = '{0}{1}\n'.format(prefix, self.__class__.__name__)
        s += '{0} Start [{1}]:\n{2}\n'.format(
            prefix, self.id_name, self.start_expr.dump(indent + 2))
        s += '{0} End:\n{1}\n'.format(
            prefix, self.end_expr.dump(indent + 2))
        s += '{0} Step:\n{1}\n'.format(
            prefix, self.step_expr.dump(indent + 2))
        s += '{0} Body:\n{1}\n'.format(
            prefix, self.body.dump(indent + 2))
        return s
