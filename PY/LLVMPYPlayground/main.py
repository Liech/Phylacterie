from Phylacterie import Phylacterie

# Evaluate some code.
phyl = Phylacterie()

while True:
  print(phyl.evaluate(input()))

phyl.evaluate('''
    def foo(x y z)
        var s1 = x + y, s2 = z + y in
            s1 * s2
    ''')
phyl.evaluate('''
    extern putchard

    def print(x)
        putchard(x)

''')
print(phyl.evaluate('print(foo(1, 2, 3))'))
