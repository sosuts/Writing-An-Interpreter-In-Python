from typing import Callable

from ponkey.ast import (
    Expression,
    Identifier,
    LetStatement,
    Program,
    ReturnStatement,
    Statement,
)
from ponkey.exception import UnexpectedToken
from ponkey.lexer import Lexer
from ponkey.token import Token, TokenType

PrefixParseFn = Callable[[], Expression]
InfixParseFn = Callable[[Expression], Expression]


class Parser:
    """Lexerがtokenizeした結果をもとにASTを生成する"""

    def __init__(self, lexer: Lexer) -> None:
        """
        Initializes the Parser with a given Lexer instance.
        next_tokenメソッドを2回実行する理由は、パーサーが現在のトークン(current_token)と
        次のトークン(peek_token)の両方を保持するため。
        これにより、パーサーは次に何が来るかを確認しながら現在のトークンを処理できる。これを先読みと呼ぶ。

        Args:
            lexer (Lexer): The lexer instance used to tokenize the input.

        Attributes:
            current_token (Token | None): The current token being processed.
            peek_token (Token | None): The next token to be processed.
            lexer (Lexer): The lexer instance used to tokenize the input.
        """
        self.lexer = lexer
        self.errors: list[UnexpectedToken] = []
        self.current_token: Token | None = None
        self.peek_token: Token | None = None

        self.prefix_parse_functions: dict[TokenType, PrefixParseFn] = {}
        self.infix_parse_functions: dict[TokenType, InfixParseFn] = {}
        self.init_tokens()

    def init_tokens(self) -> None:
        """current_tokenとpeek_tokenを初期化する"""
        # self.current_token = None, self.peek_token = 1つ目のトークン
        self.next_token()
        # self.current_token = 1つ目のトークン, self.peek_token = 2つ目のトークン
        self.next_token()

    def next_token(self):
        """current_tokenとpeek_tokenを1つずつ進める"""
        self.current_token = self.peek_token
        self.peek_token = self.lexer.next_token()

    def parse_statement(self) -> Statement | None:
        """statementをパースする.

        self.current_tokenがparse_functionsに入っていたらその関数でパースする.
        なければNoneを返す.
        """
        if self.current_token is None:
            raise ValueError("current_token is None")

        parse_functions = {
            TokenType.LET: self.parse_let_statement,
            TokenType.RETURN: self.parse_return_statement,
        }

        parse_function = parse_functions.get(self.current_token.type, lambda: None)
        return parse_function()

    def parse_let_statement(self) -> Statement | None:
        if self.current_token is None:
            raise ValueError("current_token is None")
        stmt = LetStatement(token=self.current_token)
        if not self.expect_peek(TokenType.IDENT):
            return None
        stmt.name = Identifier(
            token=self.current_token, value=self.current_token.literal
        )
        if not self.expect_peek(TokenType.ASSIGN):
            return None
        while self.current_token.type != TokenType.SEMICOLON:
            self.next_token()
        return stmt

    def parse_return_statement(self) -> Statement | None:
        if self.current_token is None:
            raise ValueError("current_token is None")
        stmt = ReturnStatement(token=self.current_token)
        while self.current_token.type != TokenType.SEMICOLON:
            self.next_token()
        return stmt

    def current_token_is(self, token_type: TokenType) -> bool:
        if self.peek_token is None:
            raise ValueError("peek_token is None")
        if self.current_token is None:
            raise ValueError("current_token is None")
        return self.current_token.type == token_type

    def peek_token_is(self, token_type: TokenType) -> bool:
        if self.peek_token is None:
            raise ValueError("peek_token is None")
        return self.peek_token.type == token_type

    def expect_peek(self, token_type: TokenType) -> bool:
        if self.peek_token_is(token_type):
            self.next_token()
            return True
        else:
            self.peek_error(token_type)
            return False

    def peek_error(self, token_type: TokenType) -> None:
        if self.peek_token is None:
            raise ValueError("peek_token is None")
        self.errors.append(UnexpectedToken(token_type, self.peek_token.type))

    def parse_program(self) -> Program:
        """
        1. ASTのルートノードであるProgramノードを生成する
        2. ループを使って、EOFトークンに達するまでトークンを読み込む
        """
        program = Program()
        while (
            self.current_token is not None and self.current_token.type != TokenType.EOF
        ):
            stmt = self.parse_statement()
            if stmt:
                program.statements.append(stmt)
            self.next_token()
        return program

    def register_prefix(self, token_type: TokenType, fn: PrefixParseFn) -> None:
        self.prefix_parse_functions[token_type] = fn

    def register_infix(self, token_type: TokenType, fn: InfixParseFn) -> None:
        self.infix_parse_functions[token_type] = fn
