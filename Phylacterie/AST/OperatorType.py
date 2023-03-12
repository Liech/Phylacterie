
from collections import namedtuple
from enum import Enum

class OperatorType(Enum):
    BINARY  = -1
    UNARY   = -2
    LHAND   = -3
    UNKNOWN = -4
