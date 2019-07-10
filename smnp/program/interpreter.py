from smnp.ast.parser import parse
#from smnp.environment.factory import createEnvironment
from smnp.error.runtime import RuntimeException
from smnp.program.FileReader import readLines
from smnp.token.tokenizer import tokenize


class Interpreter:

    @staticmethod
    def interpretString(string, printTokens=False, printAst=False, execute=True, baseEnvironment=None):
        return Interpreter._interpret(string.splitlines(), printTokens, printAst, execute, baseEnvironment)

    @staticmethod
    def interpretFile(file, printTokens=False, printAst=False, execute=True, baseEnvironment=None):
        return Interpreter._interpret(readLines(file), printTokens, printAst, execute, baseEnvironment)

    @staticmethod
    def _interpret(lines, printTokens=False, printAst=False, execute=True, baseEnvironment=None):
        #environment = createEnvironment()
        #if baseEnvironment is not None:
        #    environment.extend(baseEnvironment)

        try:
            tokens = tokenize(lines)
            if printTokens:
                print(tokens)

            ast = parse(tokens)
            if printAst:
                ast.print()

            #if execute:
            #    evaluate(ast, environment)

            #return environment
        except RuntimeException as e:
            #e.environment = environment
            raise e