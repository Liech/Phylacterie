
from Phylacterie import Phylacterie


def baseDataTypes():  
  result = Phylacterie().evaluate('1;')
  assert(result == 1)
  
  result = Phylacterie().evaluate('true;')
  assert(result == True)
  result = Phylacterie().evaluate('false;')
  assert(result == False)
  
  result = Phylacterie().evaluate('1.0;')
  assert(result == 1.0)
  result = Phylacterie().evaluate('1.0+1.0;')
  assert(result == 2.0)

def variable():  
  result = Phylacterie().evaluate('int x = 123; x;')
  assert(result == 123)
  result = Phylacterie().evaluate('double x = 123.0; x;')
  assert(result == 123.0)
  result = Phylacterie().evaluate('bool x = true; x;')
  assert(result == True)

def loop():  
  result = Phylacterie().evaluate('''
  double x = 0.0;
  while(x < 5.0) {
    x=x+1.0;
  }
  x;
  ''')
  assert(result == 5)

def func():
  result = Phylacterie().evaluate('''
  double wub2(double x, double y) {
    x*y*y;
  }
  wub2(123.0,5.0);
  ''');
  assert(result == 123.0*5*5)
  result = Phylacterie().evaluate(''' 
  double wub(double x) { 
    x;
  }
  wub(123.0);
  ''')
  assert(result == 123.0)
  result = Phylacterie().evaluate('''
  double binary @ (double x, double y){
    x*y*y;
  }
  2.0@2.0;
  ''')
  assert(result == 8.0);

def overload():  
  result = Phylacterie().evaluate('''
     double wub(double x) {
       x;
     }
     double wub(double x, double y){
       x*y;
     }
     wub(wub(1.0),2.0);
  ''')
  assert(result == 2)

  result = Phylacterie().evaluate('''
  double binary $ (double x, double y){
    x*y*y;
  }
  int binary $ (int x, int y){
    x;
  }
  bool binary $ (bool x, bool y){
    if(x) {
      if(y) 
        true;
      else
        false;
      }
      else {
        false;
      }
  }
  if(true$true){
    2.0$2.0;
  }
  else 
    0.0;
  ''');
  assert(result == 2*2*2)

def ifs():
  result = Phylacterie().evaluate('''
  if (false) 
    false; 
  else 
    {{{{{true;}}}}}
  ''')
  assert(result == True)

def test():
  func();
  baseDataTypes();
  variable();
  loop();
  overload();
  ifs();