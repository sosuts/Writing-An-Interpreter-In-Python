from dataclasses import dataclass
from enum import StrEnum


class TokenType(StrEnum):
    ASSIGN = "="

    PLUS = "+"
    MINUS = "-"
    BANG = "!"
    ASTERISK = "*"
    SLASH = "/"
    LT = "<"
    GT = ">"
    EQ = "=="
    NEQ = "!="

    FUNCTION = "func"
    LET = "let"
    TRUE = "true"
    FALSE = "false"
    IF = "if"
    ELSE = "else"
    RETURN = "return"

    INT = "INT"
    LPAREN = "("
    RPAREN = ")"
    LBRACE = "{"
    RBRACE = "}"

    SEMICOLON = ";"
    COMMA = ","

    IDENT = "IDENT"
    EOF = ""

    ILLEGAL = "ILLEGAL"


@dataclass
class Token:
    type: TokenType
    literal: str

    @staticmethod
    def lookup_table(ident: str) -> "TokenType":
        """ユーザー定義の識別子とキーワードを区別する"""
        keywords = {
            "func": TokenType.FUNCTION,
            "let": TokenType.LET,
            "true": TokenType.TRUE,
            "false": TokenType.FALSE,
            "if": TokenType.IF,
            "else": TokenType.ELSE,
            "return": TokenType.RETURN,
        }
        if ident in keywords:
            return keywords[ident]
        else:
            return TokenType.IDENT
