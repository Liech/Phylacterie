from .ExprAST import ExprAST

from .Token import TokenKind
import llvmlite.ir as ir
import llvmlite.binding as llvm
from ctypes import CFUNCTYPE, c_bool, c_double, c_int

class DatatypeAST(ExprAST):
    def __init__(self, core, identifier, templateTypes = []):
        self.identifier    = identifier;
        self.templateTypes = templateTypes;        
        if (core.classes.hasClass(identifier)):
          self.classObject = core.classes.getClass(identifier);
        else:
          self.classObject = None

    def getSyntax(self):
      return ['Datatype']

    def parse(parser,parent,identifier, core):
      templateTypes = []
      if(parser._cur_tok_is_operator('<')):
        parser._get_next_token()
        while (parser.cur_tok.kind == TokenKind.IDENTIFIER and len(templateTypes) == 0) or (len(templateTypes) > 0 and parser._cur_tok_is_operator(',')):
          if(len(templateTypes)> 0):
            parser._match(TokenKind.OPERATOR, ',')
          subID = parser.cur_tok.value
          parser._get_next_token()
          templateTypes.append(DatatypeAST.parse(core,parser,parent,subID,core));              
        parser._match(TokenKind.OPERATOR, '>')

      result = DatatypeAST(core, identifier, templateTypes);      
      return result;

    def codegen(self, generator):
        return None
      
    def getTypeString(self):
      return self.identifier;

    def getIRType(self):
      if self.identifier == 'double':
        return ir.DoubleType();
      elif self.identifier == 'bool':
        return ir.IntType(1);
      elif self.identifier == 'int':
        return ir.IntType(32);
      elif self.classObject != None:
        self.classObject.getIRType();
      else:
        raise BaseException("unkown type")

    def getDefault(self):
      if self.classObject != None:
        return self.classObject.getDefault();
      else:
        return ir.Constant(self.identifier, 0.0)

    def getCType(self):
      if self.getIRType() == ir.DoubleType():
        return c_double;
      if self.getIRType() == ir.IntType(32):
        return c_int;
      elif self.getIRType() == ir.IntType(1):
        return c_bool;
      else:
        raise "return type not convertible to c type"

    def toString(self):
      return self.identifier