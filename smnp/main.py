import sys

from smnp.error.base import SmnpException
from smnp.library.loader import loadStandardLibrary
from smnp.program.interpreter import Interpreter


def main():
    try:
        stdLibraryEnv = loadStandardLibrary()
        Interpreter.interpretFile(sys.argv[1], printTokens=False, printAst=False, execute=True, baseEnvironment=stdLibraryEnv)

    except SmnpException as e:
        print(e.message())

    except KeyboardInterrupt:
        print("Program interrupted")
