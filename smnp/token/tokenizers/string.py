from smnp.token.type import TokenType
from smnp.token.model import Token

def tokenizeString(input, current, line):
    if input[current] == '"':
        value = input[current]
        char = ''
        consumedChars = 1
        while char != '"':
            if char is None: #TODO!!!
                print("String not terminated")
            char = input[current + consumedChars]
            value += char
            consumedChars += 1
        return (consumedChars, Token(TokenType.STRING, value, (line, current)))
    return (0, None)