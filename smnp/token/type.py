from enum import Enum, auto


class TokenType(Enum):
    OPEN_PAREN = auto()
    CLOSE_PAREN = auto()
    ASTERISK = auto()
    STRING = auto()
    IDENTIFIER = auto()
    COMMA = auto()
    INTEGER = auto()
    OPEN_BRACKET = auto()
    CLOSE_BRACKET = auto()
    ASSIGN = auto()
    NOTE = auto()
    COMMENT = auto()
    PERCENT = auto()
    MINUS = auto()
    FUNCTION = auto()
    RETURN = auto()
    DOT = auto()
    OPEN_SQUARE = auto()
    CLOSE_SQUARE = auto()
    TYPE = auto()
