
from collections import namedtuple
from enum import Enum

class TokenKind(Enum):
    EOF = -1
    DEF = -2
    EXTERN = -3
    IDENTIFIER = -4
    NUMBER = -5
    OPERATOR = -6
    IF = -7
    ELSE = -9
    WHILE = -10
    SCOPESTART = -11
    BINARY = -12
    UNARY = -13
    VAR = -14
    SCOPEEND = -15
    INCLUDE = -16
    TRUE = -17
    FALSE = -18
Token = namedtuple('Token', 'kind value')