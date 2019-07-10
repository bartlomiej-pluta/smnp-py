from smnp.ast.node.expression import ExpressionNode
from smnp.ast.parser import Parser
from smnp.token.type import TokenType


class IntegerLiteralNode(ExpressionNode):
    def __init__(self, pos):
        super().__init__(pos)
        #TODO del self.children[1]


    # TODO: To Remove
    @classmethod
    def _parse(cls, input):
        return cls._literalParser()(input)

    @classmethod
    def _literalParser(cls):
        return Parser.oneOf(
            cls._negativeIntegerParser(),
            cls._positiveIntegerParser()
        )

    @classmethod
    def _negativeIntegerParser(cls):
        def createNode(minus, integer):
            return IntegerLiteralNode.withValue(-integer.value, minus.pos)

        return Parser.allOf(
            Parser.terminalParser(TokenType.MINUS),
            Parser.doAssert(cls._positiveIntegerParser(), "integer"),
            createNode=createNode
        )

    @classmethod
    def _positiveIntegerParser(cls):
        return Parser.terminalParser(TokenType.INTEGER, lambda val, pos: IntegerLiteralNode.withValue(int(val), pos))