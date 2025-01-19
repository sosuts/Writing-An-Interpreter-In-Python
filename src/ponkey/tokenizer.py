"""
字句解析器(Lexer, Tokenizer)の実装
"""

from dataclasses import dataclass, field
from typing import ClassVar

from ponkey.token import Token, TokenType


@dataclass
class Tokenizer:
    """Ponkey言語の字句解析器.

    文字列をトークンに分割する.

    Attributes:
        input (str): 字句解析器が解析する文字列
        position (int): 現在の文字の位置
        read_position (int): 次の文字の位置
        ch (str): 現在の文字
    """

    input: str
    position: int = 0
    read_position: int = 0
    ch: str | None = field(init=False)

    WHITESPACES: ClassVar[list[str]] = [" ", "\t", "\n", "\r"]

    def __post_init__(self) -> None:
        self.read_char()

    def peek_char(self) -> str | None:
        if self.read_position >= len(self.input):
            return None
        else:
            return self.input[self.read_position]

    def read_char(self) -> None:
        """
        現在の読み取り位置から1文字を読み込み、`self.ch`に設定します。
        読み取り位置が入力の長さを超えている場合、`self.ch`は空文字列になります。
        その後、`self.position`を現在の読み取り位置に更新し、`self.read_position`を1つ進めます。

        Returns:
            None
        """
        if self.read_position >= len(self.input):
            self.ch = None
        else:
            self.ch = self.input[self.read_position]
        self.position = self.read_position
        self.read_position = self.position + 1

    def read_number(self) -> str:
        """Read until the next non-number character"""
        start_position = self.position
        while self._is_number(self.ch):
            self.read_char()
        return self.input[start_position : self.position]

    def read_identifier(self) -> str:
        """Read until the next non-letter character"""
        start_position = self.position
        while self._is_letter(self.ch):
            self.read_char()
        return self.input[start_position : self.position]

    def next_token(self) -> Token:
        """次のトークンを返す

        手順:
            1. 空白をスキップ
            2. 現在の文字が特定の文字の場合、その文字に対応するトークンを返す
            3. 現在の文字が英字の場合、識別子を読み取り、その識別子に対応するトークンを返す
            4. 現在の文字が数字の場合、数字を読み取り、その数字に対応するトークンを返す
            5. それ以外の場合、ILLEGALトークンを返す
        """
        # 空白をスキップ
        self._skip_whitespace()
        # 現在の文字が特定の文字の場合、その文字に対応するトークンを返す
        match self.ch:
            case "=":
                # 次の文字をpeekして、== か = かを判定する
                if self.peek_char() == "=":
                    # 次の文字が = の場合、== としてトークンを生成する
                    ch: str = self.ch
                    # 次の文字に進める
                    self.read_char()
                    literal = ch + self.ch
                    tok = Token(TokenType.EQ, literal)
                else:
                    # 次の文字が = でない場合、= としてトークンを生成する
                    tok = Token(TokenType.ASSIGN, "=")
            case "+":
                tok = Token(TokenType.PLUS, "+")
            case "-":
                tok = Token(TokenType.MINUS, "-")
            case "!":
                # 次の文字をpeekして、!= か ! かを判定する
                if self.peek_char() == "=":
                    # 次の文字が = の場合、!= としてトークンを生成する
                    ch: str = self.ch  # type: ignore[no-redef]
                    self.read_char()
                    literal = ch + self.ch
                    tok = Token(TokenType.NEQ, literal)
                else:
                    tok = Token(TokenType.BANG, "!")
            case "*":
                tok = Token(TokenType.ASTERISK, "*")
            case "/":
                tok = Token(TokenType.SLASH, "/")
            case "<":
                tok = Token(TokenType.LT, "<")
            case ">":
                tok = Token(TokenType.GT, ">")
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
            case None:
                tok = Token(TokenType.EOF, "")
            # 現在の文字が英字の場合、識別子を読み取り、その識別子に対応するトークンを返す
            case _:
                # 英字の場合、識別子を読み取る
                if self._is_letter(self.ch):
                    literal = self.read_identifier()
                    # 識別子に対応するトークンを返す
                    tok = Token(
                        Token.lookup_table(literal),
                        literal,
                    )
                    return tok
                elif self._is_number(self.ch):
                    literal = self.read_number()
                    tok = Token(TokenType.INT, literal)
                    return tok
                else:
                    tok = Token(TokenType.ILLEGAL, self.ch)
        self.read_char()
        return tok

    @staticmethod
    def _is_letter(ch: str | None) -> bool:
        """文字が英字かアンダースコアかどうかを判定する

        Args:
            ch (str): 判定したい文字
        """
        if ch is None:
            raise ValueError("ch is None")
        return ("a" <= ch <= "z") | ("A" <= ch <= "Z") | (ch == "_")

    @staticmethod
    def _is_number(ch: str | None) -> bool:
        if ch is None:
            raise ValueError("ch is None")
        """chが数字かどうかを判定する"""
        return "0" <= ch <= "9"

    def _skip_whitespace(self) -> None:
        """Tokenizer.WHITESPACESに定義された空文字をスキップする"""
        while self.ch in self.WHITESPACES:
            self.read_char()
