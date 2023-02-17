from .ASTNode import ASTNode
from .CodegenError import CodegenError
from .Token import *
from .DatatypeAST import DatatypeAST
from string2irType import string2irType
from irType2string import irType2string
from ParseError import ParseError

import llvmlite.ir as ir
import llvmlite.binding as llvm

class PrototypeAST(ASTNode):
    def __init__(self, parent, name, arguments, isoperator, prec, returnType, core):
      assert(returnType)  
      self.name = name
      self.argnames = [i['name'] for i in arguments]
      self.isoperator = isoperator
      self.prec = prec
      self.parent = parent
      self.returnType = returnType
      self.parameterTypes =  [i['type'] for i in arguments]        
      self.core = core
      self.core.typeContainer.registerType(self.getID(),returnType);

    def getSyntax(self):
      #return ['Type', 'unary', 'operator','(',['Type','identifier',[',']],')'];
      #return ['Type', 'binary', 'operator','(',['Type','identifier',[',']],')'];
      return  ['Type', 'identifier','(',['Type','identifier',[',']],')'];


    def is_unary_op(self):
        return self.isoperator and len(self.argnames) == 1

    def is_binary_op(self):
        return self.isoperator and len(self.argnames) == 2

    def get_op_name(self):
        assert self.isoperator
        return self.name[-1]

    def dump(self, indent=0):
        s = '{0}{1} {2}({3})'.format(
            ' ' * indent, self.__class__.__name__, self.name,
            ', '.join(self.argnames))
        if self.isoperator:
            s += '[operator with prec={0}]'.format(self.prec)
        return s

    def parse(parser, parent,datatype,varName,core):
        prec = 30
        if varName.kind == TokenKind.IDENTIFIER:
            name = varName.value
        elif varName.kind == TokenKind.UNARY:
            if parser.cur_tok.kind != TokenKind.OPERATOR:
                raise ParseError('Expected operator after "unary"')
            name = 'unary{0}'.format(parser.cur_tok.value)
            parser._get_next_token()
        elif varName.kind == TokenKind.BINARY:
            if parser.cur_tok.kind != TokenKind.OPERATOR:
                raise ParseError('Expected operator after "binary"')
            name = 'binary{0}'.format(parser.cur_tok.value)
            parser._get_next_token()

            # Try to parse precedence
            if parser.cur_tok.kind == TokenKind.NUMBER:
                prec = int(parser.cur_tok.value)
                if not (0 < prec < 101):
                    raise ParseError('Invalid precedence', prec)
                parser._get_next_token()

            # Add the new operator to our precedence table so we can properly
            # parse it.
            parser._precedence_map[name[-1]] = prec

        parser._match(TokenKind.OPERATOR, '(')
        argnames = []
        while (parser.cur_tok.kind == TokenKind.IDENTIFIER and len(argnames) == 0) or (len(argnames) > 0 and parser._cur_tok_is_operator(',')):
            if(len(argnames)> 0):
              parser._match(TokenKind.OPERATOR, ',')
            if not parser.cur_tok.kind == TokenKind.IDENTIFIER:
              raise ParseError('Expected datatype identifier')
            dataType = DatatypeAST.parse(parent, parser.cur_tok.value, core);
            parser._get_next_token()
            if not parser.cur_tok.kind == TokenKind.IDENTIFIER:
              raise ParseError('Expected variablename identifier')
            argName = parser.cur_tok.value
            parser._get_next_token()
            argnames.append({'name':argName, 'type':dataType})
        parser._match(TokenKind.OPERATOR, ')')

        if name.startswith('binary') and len(argnames) != 2:
            raise ParseError('Expected binary operator to have 2 operands')
        elif name.startswith('unary') and len(argnames) != 1:
            raise ParseError('Expected unary operator to have one operand')

        core.typeContainer.registerType(name, datatype)
        for i in range(0,len(argnames)):
          core.typeContainer.registerType(argnames[i]['name'],argnames[i]['type'])
          core.variables.registerVar(argnames[i]['name'],{})

        return PrototypeAST(parent, name, argnames, name.startswith(('unary', 'binary')), prec, datatype,core)

    def getID(self):
      args = ''.join([t.toString() + '_' for t in self.parameterTypes])
      return self.name + '_' + args;

    def codegen(self,generator):
        funcname = self.name
        funcID = self.getID();
        # Create a function type
        types = [x.getIRType() for x in self.parameterTypes]
        func_ty = ir.FunctionType(self.returnType.getIRType(),  types)

        # If a function with this name already exists in the module...
        if funcID in generator.getModule().globals:
            # We only allow the case in which a declaration exists and now the
            # function is defined (or redeclared) with the same number of args.
            existing_func = generator.getModule().globals[funcID]
            if not isinstance(existing_func, ir.Function):
                raise CodegenError('Function/Global name collision', funcID)
            if not existing_func.is_declaration:
                raise CodegenError('Redifinition of {0}'.format(funcID))
            if len(existing_func.function_type.args) != len(func_ty.args):
                raise CodegenError(
                    'Redifinition with different number of arguments')
            func = generator.getModule().globals[funcID]
        else:
            # Otherwise create a new function
            func = ir.Function(generator.getModule(), func_ty, funcID)
        return func