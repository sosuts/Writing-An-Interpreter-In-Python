import pytest

from ponkey.lexer import Lexer
from ponkey.token import Token, TokenType


class TestLexerInit:
    def taest_next_token1(self):
        input = "=+(){},;"
        expected_results = [
            Token(TokenType.ASSIGN, "="),
            Token(TokenType.PLUS, "+"),
            Token(TokenType.LPAREN, "("),
            Token(TokenType.RPAREN, ")"),
            Token(TokenType.LBRACE, "{"),
            Token(TokenType.RBRACE, "}"),
            Token(TokenType.COMMA, ","),
            Token(TokenType.SEMICOLON, ";"),
            Token(TokenType.EOF, ""),
        ]

        lexer = Lexer(input)
        assert lexer.input == input
        assert lexer.position == 0
        assert lexer.read_position == 1
        assert lexer.ch == "="
        for i, expected_result in enumerate(expected_results):
            tok = lexer.next_token()
            assert tok == expected_result

    def test_next_token2(self):
        input = """let five = 5;
        let ten = 10;
        let add = func(x, y) {
            x + y;
        };
        let result = add(five, ten);
        """
        expected_results = [
            Token(TokenType.LET, "let"),
            Token(TokenType.IDENT, "five"),
            Token(TokenType.ASSIGN, "="),
            Token(TokenType.INT, "5"),
            Token(TokenType.SEMICOLON, ";"),
            Token(TokenType.LET, "let"),
            Token(TokenType.IDENT, "ten"),
            Token(TokenType.ASSIGN, "="),
            Token(TokenType.INT, "10"),
            Token(TokenType.SEMICOLON, ";"),
            Token(TokenType.LET, "let"),
            Token(TokenType.IDENT, "add"),
            Token(TokenType.ASSIGN, "="),
            Token(TokenType.FUNCTION, "func"),
            Token(TokenType.LPAREN, "("),
            Token(TokenType.IDENT, "x"),
            Token(TokenType.COMMA, ","),
            Token(TokenType.IDENT, "y"),
            Token(TokenType.RPAREN, ")"),
            Token(TokenType.LBRACE, "{"),
            Token(TokenType.IDENT, "x"),
            Token(TokenType.PLUS, "+"),
            Token(TokenType.IDENT, "y"),
            Token(TokenType.SEMICOLON, ";"),
            Token(TokenType.RBRACE, "}"),
            Token(TokenType.SEMICOLON, ";"),
            Token(TokenType.LET, "let"),
            Token(TokenType.IDENT, "result"),
            Token(TokenType.ASSIGN, "="),
            Token(TokenType.IDENT, "add"),
            Token(TokenType.LPAREN, "("),
            Token(TokenType.IDENT, "five"),
            Token(TokenType.COMMA, ","),
            Token(TokenType.IDENT, "ten"),
            Token(TokenType.RPAREN, ")"),
            Token(TokenType.SEMICOLON, ";"),
            Token(TokenType.EOF, ""),
        ]
        lexer = Lexer(input)
        for i, expected_result in enumerate(expected_results):
            tok = lexer.next_token()
            print(tok)
            assert tok == expected_result

    def test_empty_input(self):
        input = ""
        lexer = Lexer(input)
        assert lexer.input == input
        assert lexer.position == 0
        assert lexer.read_position == 1
        assert lexer.ch == ""
