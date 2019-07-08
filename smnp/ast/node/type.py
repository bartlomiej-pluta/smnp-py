from smnp.ast.node.access import AccessNode
from smnp.ast.node.iterable import abstractIterableParser
from smnp.ast.node.model import Node
from smnp.ast.parser import Parser
from smnp.token.type import TokenType
from smnp.type.model import Type


class TypeSpecifier(Node):

    @classmethod
    def _parse(cls, input):
        return abstractIterableParser(TypeSpecifier, TokenType.OPEN_ANGLE, TokenType.CLOSE_ANGLE,
                                      Parser.doAssert(cls._specifierItem(), "type"))(input)

    @classmethod
    def _specifierItem(cls):
        return Parser.oneOf(
            TypeNode.parse,
            cls.parse
        )


class TypeNode(AccessNode):
    def __init__(self, pos):
        super().__init__(pos)

    @property
    def type(self):
        return self[0]

    @type.setter
    def type(self, value):
        self[0] = value

    @property
    def specifier(self):
        return self[1]

    @specifier.setter
    def specifier(self, value):
        self[1] = value

    @classmethod
    def _parse(cls, input):
        def createNode(type, specifier):
            node = TypeNode(type.pos)
            node.type = Type[type.value.upper()]
            node.specifier = specifier
            return node

        return Parser.allOf(
            cls._rawTypeParser(),
            Parser.optional(TypeSpecifier.parse),
            createNode=createNode
        )(input)

    @classmethod
    def _rawTypeParser(cls):
        return Parser.terminalParser(TokenType.TYPE, lambda val, pos: TypeNode.withValue(val, pos))