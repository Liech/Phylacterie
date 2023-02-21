from .ExprAST import ExprAST
from .VariableExprAST import VariableExprAST
from .UnaryExprAST import UnaryExprAST
from .CodegenError import CodegenError
from .DatatypeAST import DatatypeAST
from .Token import TokenKind

import llvmlite.ir as ir
import llvmlite.binding as llvm

class ClassExprAST(ExprAST):
    def __init__(self, parent, classname, members, core):
        self.parent = parent
        self.core   = core
        self.classname = classname;
        self.members = members
        
    def getSyntax(self):
      return ['class']
            
    def getReturnType(self):      
      return None;

    def parse(parser, parent,core):
      assert(parser.cur_tok.kind == TokenKind.CLASS)
      parser._get_next_token()            
      assert(parser.cur_tok.kind == TokenKind.IDENTIFIER)
      classname = parser.cur_tok.value
      parser._get_next_token()            

      parser._match(TokenKind.SCOPESTART)

      members = []
      while(parser.cur_tok.kind != TokenKind.SCOPEEND):
        assert (parser.cur_tok.kind == TokenKind.IDENTIFIER);
        datatypeID = parser.cur_tok.value
        parser._get_next_token()      
        datatype = DatatypeAST.parse(parser,parent,datatypeID, core);
        name = parser.cur_tok.value
        parser._get_next_token()   
        members.append({'name':name, 'type':datatype });
        parser._match(TokenKind.OPERATOR, ';')

      parser._match(TokenKind.SCOPEEND)      
      result = ClassExprAST(parent,classname, members, core);
      parser.nextNeedsNoSemicolon();
      core.classes.registerClass(classname, result);
      return result;

    def getID(self):
      return 'class';

    def codegen(self, generator):        
      return None

    def getIRType(self):
      membertypes = [x['type'].getIRType() for x in self.members]
      datatype = ir.LiteralStructType(membertypes);
      return datatype;

    def getDefault(self):
      struct_type = self.getIRType();
      struct_val = struct_type(ir.Undefined)
      #for i, v in enumerate(self.members):
      #  struct_val = builder.insert_value(struct_val, v, i)
      return struct_val