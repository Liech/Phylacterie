from .AST import TokenKind
from .AST import Token

class Lexer(object):
    """Lexer for Kaleidoscope.

    Initialize the lexer with a string buffer. tokens() returns a generator that
    can be queried for tokens. The generator will emit an EOF token before
    stopping.
    """
    def __init__(self, buf):
        assert len(buf) >= 1
        self.buf = buf
        self.pos = 0
        self.lastchar = self.buf[0]

        self._keyword_map = {
            'def':      TokenKind.DEF,
            'extern':   TokenKind.EXTERN,
            'if':       TokenKind.IF,
            'else':     TokenKind.ELSE,
            'while':    TokenKind.WHILE,
            '{'    :    TokenKind.SCOPESTART,
            '}'    :    TokenKind.SCOPEEND,
            'binary':   TokenKind.BINARY,
            'unary':    TokenKind.UNARY,
            'var':      TokenKind.VAR,            
            'include':  TokenKind.INCLUDE,
            'true':     TokenKind.TRUE,
            'false':    TokenKind.FALSE,
        }

    def tokens(self):
        while self.lastchar:
            # Skip whitespace
            while self.lastchar.isspace():
                self._advance()
            # Identifier or keyword
            if self.lastchar.isalpha():
                id_str = ''
                while self.lastchar.isalnum():
                    id_str += self.lastchar
                    self._advance()
                if id_str in self._keyword_map:
                    yield Token(kind=self._keyword_map[id_str], value=id_str)
                else:
                    yield Token(kind=TokenKind.IDENTIFIER, value=id_str)
            # Number
            elif self.lastchar.isdigit() or self.lastchar == '.':
                num_str = ''
                while self.lastchar.isdigit() or self.lastchar == '.':
                    num_str += self.lastchar
                    self._advance()
                yield Token(kind=TokenKind.NUMBER, value=num_str)
            elif self.lastchar == '{':
                yield Token(kind=TokenKind.SCOPESTART, value=self.lastchar);   
                self._advance()
            elif self.lastchar == '}':
                yield Token(kind=TokenKind.SCOPEEND, value=self.lastchar);                
                self._advance()
            # Comment
            elif self.lastchar == '#':
                self._advance()
                while self.lastchar and self.lastchar not in '\r\n':
                    self._advance()
            elif self.lastchar:
                # Some other char
                result = ''
                operatorList = "+*~#\'-_.:,;!+?=$§²³`´%&/^°|<>"
                while self.lastchar and self.lastchar in operatorList:
                    result = result + self.lastchar
                    self._advance()
                if (len(result) == 0):
                  result = self.lastchar;
                  self._advance()
                yield Token(kind=TokenKind.OPERATOR, value=result)
        yield Token(kind=TokenKind.EOF, value='')

    def _advance(self):
        try:
            self.pos += 1
            self.lastchar = self.buf[self.pos]
        except IndexError:
            self.lastchar = ''
