from smnp.token.tools import tokenizeKeyword
from smnp.token.type import TokenType

def tokenizeFunction(input, current, line):
    return tokenizeKeyword(TokenType.FUNCTION, 'library', input, current, line)