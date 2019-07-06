from smnp.ast.node.access import AccessNode
from smnp.ast.node.args import ArgumentsListNode
from smnp.ast.node.assignment import AssignmentNode
from smnp.ast.node.expression import ExpressionNode
from smnp.ast.node.invocation import FunctionCall
from smnp.ast.parser import Parser
from smnp.token.type import TokenType


class IdentifierNode(AccessNode):
    def __init__(self, pos):
        super().__init__(pos)
        del self.children[1]

    @classmethod
    def _literalParser(cls):
        return Parser.oneOf(
            IdentifierNode._functionCallParser(),
            IdentifierNode._assignmentParser(),
            IdentifierNode.identifierParser()
        )

    @staticmethod
    def _assignmentParser():
        def createNode(target, assignment, value):
            node = AssignmentNode(assignment.pos)
            node.target = target
            node.value = value
            return node

        return Parser.allOf(
            IdentifierNode.identifierParser(),
            Parser.terminalParser(TokenType.ASSIGN),
            ExpressionNode.parse,
            createNode=createNode
        )

    @staticmethod
    def _functionCallParser():
        def createNode(name, arguments):
            node = FunctionCall(name.pos)
            node.name = name
            node.arguments = arguments
            return node

        return Parser.allOf(
            IdentifierNode.identifierParser(),
            ArgumentsListNode.parse,
            createNode=createNode
        )

    @staticmethod
    def identifierParser():
        return Parser.terminalParser(TokenType.IDENTIFIER, lambda val, pos: IdentifierNode.withValue(val, pos))
