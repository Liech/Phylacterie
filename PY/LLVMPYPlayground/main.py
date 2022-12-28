from Phylacterie import Phylacterie


# Evaluate some code.
phyl = Phylacterie()
phyl.evaluate('''
    def foo(x y z)
        var s1 = x + y, s2 = z + y in
            s1 * s2
    ''')
print(phyl.evaluate('foo(1, 2, 3)'))
