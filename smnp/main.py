import sys

from smnp.error.base import SmnpException
from smnp.program.interpreter import Interpreter


def main():
    try:
        #stdLibraryEnv = loadStandardLibrary()
        Interpreter.interpretFile(sys.argv[1], printTokens=True, printAst=True, execute=False, baseEnvironment=None)
        #draft()
        #tokens = tokenize(['function a(b...) { x+y}'])
        #FunctionDefinitionParser(tokens).node.print()

    except SmnpException as e:
        print(e.message())

    except KeyboardInterrupt:
        print("Program interrupted")
