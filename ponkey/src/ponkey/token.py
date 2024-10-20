import keyword
from dataclasses import dataclass
from enum import StrEnum
from re import T


class TokenType(StrEnum):
    ASSIGN = "="
    PLUS = "+"
    FUNCTION = "func"
    LET = "let"
    LPAREN = "("
    RPAREN = ")"
    LBRACE = "{"
    RBRACE = "}"
    SEMICOLON = ";"
    COMMA = ","
    ILLEGAL = "ILLEGAL"
    EOF = ""
    IDENT = "IDENT"
    INT = "INT"


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
        }
        if ident in keywords:
            return keywords[ident]
        else:
            return TokenType.IDENT
