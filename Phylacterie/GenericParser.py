from .Lexer import Lexer

class GenericParser(object):    
    def __init__(self):
        self.lexer = None
        self.current = None

    def parseTopLevel(self, root, buf, core):
        self.lexer = Lexer(buf).tokens()
        self.current = None
        self.proceed()
        
    def proceed(self):
        self.current = next(self.token_generator)