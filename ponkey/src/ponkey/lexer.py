from math import e

from ponkey.token import Token, TokenType


class Lexer:
    def __init__(self, input: str) -> None:
        self.input: str = input
        self.position: int = -1
        self.read_position: int = self.position + 1
        self.to_next_char()

    def to_next_char(self) -> None:
        if self.read_position >= len(self.input):
            self.ch = ""
        else:
            self.ch = self.input[self.read_position]
        self.position = self.read_position
        self.read_position = self.position + 1

    def skip_whitespace(self) -> None:
        while self.ch in [" ", "\t", "\n", "\r"]:
            self.to_next_char()

    @staticmethod
    def is_letter(ch: str) -> bool:
        """Check if a character is a letter/underscore

        Args:
            ch (str): The character to check
        """
        return ("a" <= ch) & (ch <= "z") | ("A" <= ch) & (ch <= "Z") | (ch == "_")

    @staticmethod
    def is_number(ch: str) -> bool:
        return "0" <= ch <= "9"

    def read_number(self) -> str:
        start_position = self.position
        while self.is_number(self.ch):
            self.to_next_char()
        return self.input[start_position : self.position]

    def read_identifier(self) -> str:
        """Read until the next non-letter character"""
        start_position = self.position
        while self.is_letter(self.ch):
            self.to_next_char()
        return self.input[start_position : self.position]

    def next_token(self) -> Token:
        self.skip_whitespace()
        match self.ch:
            case "=":
                tok = Token(TokenType.ASSIGN, "=")
            case "+":
                tok = Token(TokenType.PLUS, "+")
            case "(":
                tok = Token(TokenType.LPAREN, "(")
            case ")":
                tok = Token(TokenType.RPAREN, ")")
            case "{":
                tok = Token(TokenType.LBRACE, "{")
            case "}":
                tok = Token(TokenType.RBRACE, "}")
            case ",":
                tok = Token(TokenType.COMMA, ",")
            case ";":
                tok = Token(TokenType.SEMICOLON, ";")
            case "":
                tok = Token(TokenType.EOF, "")
            case _:
                if self.is_letter(self.ch):
                    literal = self.read_identifier()
                    tok = Token(
                        Token.lookup_table(literal),
                        literal,
                    )
                    return tok
                elif self.is_number(self.ch):
                    literal = self.read_number()
                    tok = Token(TokenType.INT, literal)
                    return tok
                else:
                    tok = Token(TokenType.ILLEGAL, self.ch)
        self.to_next_char()
        return tok
