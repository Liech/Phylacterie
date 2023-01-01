from Phylacterie import Phylacterie

# Evaluate some code.

allInput = "";
saveInput = False;

while True:
  print('>>');
  inp = input();
  phyl = Phylacterie()

  if (inp == 'cls'):
    allInput = "";
    continue;
  if (inp == 'save'):
    saveInput = not saveInput;
    continue;
  if (saveInput == False):
    allInput = "";

  allInput = allInput + inp

  if (len(inp) > 0):
    print('eval:');
    print(allInput);
    print('>>>>>');
    try:
      print(phyl.evaluate(allInput))
    except Exception as e:
      print(e);
      print('');
      print("Exception occured: Throw?");
      print('y/n');
      if (input() == 'y'):
        raise;
      allInput = '';
      print('cls');


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
