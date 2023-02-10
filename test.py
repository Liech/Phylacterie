
from Phylacterie import Phylacterie


def baseDataTypes(phyl):  
  result = phyl.evaluate('int 1')
  assert(result == 1)
  
  result = phyl.evaluate('bool true')
  assert(result == True)
  result = phyl.evaluate('bool false')
  assert(result == False)
  
  result = phyl.evaluate('double 1.0')
  assert(result == 1.0)
  result = phyl.evaluate('double 1.0+1.0')
  assert(result == 2.0)

def variable(phyl):  
  result = phyl.evaluate('int var int x = 123 x')
  assert(result == 123)
  result = phyl.evaluate('double var double x = 123.0 x')
  assert(result == 123.0)
  result = phyl.evaluate('bool var bool x = true x')
  assert(result == True)

def loop(phyl):  
  result = phyl.evaluate('double var double x = 0.0 while(x < 5.0) {x=x+1.0} x')
  assert(result == 5)

def func(phyl):
  #result = phyl.evaluate('double def double wub() { 123.0 } wub()')
  #assert(result == 123.0)
  result = phyl.evaluate('double def double wub(double x) { x } wub(123.0)')
  assert(result == 123.0)

def test():
  phyl = Phylacterie()

  baseDataTypes(phyl);
  variable(phyl);
  loop(phyl);
  func(phyl);