from dataclasses import dataclass
from enum import StrEnum


class TokenType(StrEnum):
    """トークンの種類を表す列挙型.予約語も含まれる."""

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
    """
    トークンは、字句解析器によって生成されたトークンを表す。
    トークンは、トークンの種類とそのリテラル値を持つ。

    Attributes:
        type (TokenType): トークンの種類
        literal (str): トークンのリテラル値
    """

    type: TokenType
    literal: str

    def __repr__(self):
        return f"Token ( type: {self.type}, literal: {self.literal} )"

    @staticmethod
    def lookup_table(literal: str) -> "TokenType":
        """リテラルが予約語だったら対応するトークンを返し、
        そうでなければユーザー定義のトークンと判断しIDENTを返す.
        """
        return PreservedKeywords.get(literal, TokenType.IDENT)


PreservedKeywords = {
    "func": TokenType.FUNCTION,
    "let": TokenType.LET,
    "true": TokenType.TRUE,
    "false": TokenType.FALSE,
    "if": TokenType.IF,
    "else": TokenType.ELSE,
    "return": TokenType.RETURN,
}
