
class TestParser(unittest.TestCase):
    def _flatten(self, ast):
        """Test helper - flattens the AST into a sexpr-like nested list."""
        if isinstance(ast, DoubleExprAST):
            return ['Number', ast.val]
        elif isinstance(ast, VariableExprAST):
            return ['Variable', ast.name]
        elif isinstance(ast, UnaryExprAST):
            return ['Unary', ast.op, self._flatten(ast.operand)]
        elif isinstance(ast, BinaryExprAST):
            return ['Binop', ast.op,
                    self._flatten(ast.lhs), self._flatten(ast.rhs)]
        elif isinstance(ast, VarExprAST):
            vars = [[name, self._flatten(init)] for name, init in ast.vars]
            return ['Var', vars, self._flatten(ast.body)]
        elif isinstance(ast, CallExprAST):
            args = [self._flatten(arg) for arg in ast.args]
            return ['Call', ast.callee, args]
        elif isinstance(ast, PrototypeAST):
            return ['Proto', ast.name, ' '.join(ast.argnames)]
        elif isinstance(ast, FunctionAST):
            return ['Function',
                    self._flatten(ast.proto), self._flatten(ast.body)]
        else:
            raise TypeError('unknown type in _flatten: {0}'.format(type(ast)))

    def _assert_body(self, toplevel, expected):
        """Assert the flattened body of the given toplevel function"""
        self.assertIsInstance(toplevel, FunctionAST)
        self.assertEqual(self._flatten(toplevel.body), expected)

    def test_assignment(self):
        p = Parser()
        ast = p.parse_toplevel('def text(x) x = 5')
        self._assert_body(ast,
            ['Binop', '=', ['Variable', 'x'], ['Number', '5']])

    def test_varexpr(self):
        p = Parser()
        ast = p.parse_toplevel('def foo(x y) var t = 1 in y')
        self._assert_body(ast,
             ['Var', [['t', ['Number', '1']]], ['Variable', 'y']])
        ast = p.parse_toplevel('def foo(x y) var t = x, p = y + 1 in y')
        self._assert_body(ast,
            ['Var',
                [['t', ['Variable', 'x']],
                 ['p', ['Binop', '+', ['Variable', 'y'], ['Number', '1']]]],
                ['Variable', 'y']])
