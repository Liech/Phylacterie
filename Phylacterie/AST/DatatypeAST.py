from .ExprAST import ExprAST

from .Token import *
import llvmlite.ir as ir
import llvmlite.binding as llvm
from string2irType import string2irType
from irType2cType import irType2cType

class DatatypeAST(ExprAST):
    def __init__(self, identifier, templateTypes = []):
        self.identifier = identifier;
        self.templateTypes = templateTypes;

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
          templateTypes.append(DatatypeAST.parse(parser,parent,subID,core));              
        parser._match(TokenKind.OPERATOR, '>')

      result = DatatypeAST(identifier, templateTypes);      
      return result;

    def codegen(self, generator):
        return None
      
    def getTypeString(self):
      return self.identifier;

    def getIRType(self):
      return string2irType(self.identifier);

    def getDefault(self):
      return ir.Constant(self.identifier, 0.0)

    def getCType(self):
      return irType2cType(self.getIRType());

    def toString(self):
      return self.identifier