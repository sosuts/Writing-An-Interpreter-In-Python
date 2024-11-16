from ponkey.ast import Identifier, LetStatement, Program
from ponkey.token import Token, TokenType


def test_string():
    statements = [
        LetStatement(
            Token(TokenType.LET, "let"),
            Identifier(Token(TokenType.IDENT, "myVar"), "myVar"),
            Identifier(Token(TokenType.IDENT, "anotherVar"), "anotherVar"),
        )
    ]
    program = Program(statements=statements)
    assert program.string() == "let myVar = anotherVar;"
