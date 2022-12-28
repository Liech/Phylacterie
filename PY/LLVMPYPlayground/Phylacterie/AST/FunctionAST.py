from .ASTNode import ASTNode
from .PrototypeAST import PrototypeAST

class FunctionAST(ASTNode):
    def __init__(self, proto, body):
        self.proto = proto
        self.body = body

    _anonymous_function_counter = 0

    @classmethod
    def create_anonymous(klass, expr):
        """Create an anonymous function to hold an expression."""
        klass._anonymous_function_counter += 1
        return klass(
            PrototypeAST('_anon{0}'.format(klass._anonymous_function_counter),
                         []),
            expr)

    def is_anonymous(self):
        return self.proto.name.startswith('_anon')

    def dump(self, indent=0):
        s = '{0}{1}[{2}]\n'.format(
            ' ' * indent, self.__class__.__name__, self.proto.dump())
        s += self.body.dump(indent + 2) + '\n'
        return s
