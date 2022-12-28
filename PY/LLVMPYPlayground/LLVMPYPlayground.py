from Phylacterie import *


# Evaluate some code.
kalei = LanguageEvaluator()
kalei.evaluate('def binary: 1 (x y) y')
kalei.evaluate('''
    def foo(x y z)
        var s1 = x + y, s2 = z + y in
            s1 * s2
    ''')
print(kalei.evaluate('foo(1, 2, 3)'))

obj = kalei.compile_to_object_code()

# Output object code to a file.
filename = 'output.o'
with open(filename, 'wb') as obj_file:
    obj_file.write(obj)
    print('Wrote ' + filename)
