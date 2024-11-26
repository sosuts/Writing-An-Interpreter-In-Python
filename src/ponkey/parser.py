from enum import IntEnum
from typing import Callable

from ponkey.ast import (
    Expression,
    ExpressionStatement,
    Identifier,
    IntegerLiteral,
    LetStatement,
    Program,
    ReturnStatement,
    Statement,
)
from ponkey.exception import UnexpectedToken
from ponkey.token import Token, TokenType
from ponkey.tokenizer import Tokenizer

PrefixParseFn = Callable[[], Expression]
InfixParseFn = Callable[[Expression], Expression]


class Precedence(IntEnum):
    """式の優先順位を表す"""

    LOWEST = 1
    EQUALS = 2  # ==
    LESSGREATER = 3  # > または <
    SUM = 4  # +
    PRODUCT = 5  # *
    PREFIX = 6  # -X または !X
    CALL = 7  # mu_function(X)


class Parser:
    def __init__(self, tokenizer: Tokenizer) -> None:
        """
        Tokenizerがtokenizeした結果をもとにASTを生成するクラス

        next_tokenメソッドを2回実行する理由は、パーサーが現在のトークン(current_token)と
        次のトークン(peek_token)の両方を保持するため。
        これにより、パーサーは次に何が来るかを確認しながら現在のトークンを処理できる。これを先読みと呼ぶ。

        Args:
            tokenizer (Tokenizer): The tokenizer instance used to tokenize the input.

        Attributes:
            current_token (Token | None): The current token being processed.
            peek_token (Token | None): The next token to be processed.
            tokenizer (Tokenizer): The tokenizer instance used to tokenize the input.
        """
        self.tokenizer = tokenizer
        self.errors: list[UnexpectedToken] = []
        self.current_token: Token | None = None
        self.peek_token: Token | None = None

        self.prefix_parse_functions: dict[TokenType, PrefixParseFn] = {}
        self.infix_parse_functions: dict[TokenType, InfixParseFn] = {}
        self.register_prefix(TokenType.IDENT, self.parse_identifier)
        self.register_prefix(TokenType.INT, self.parse_integer_literal)
        self._init_tokens()

    def next_token(self) -> None:
        """current_tokenとpeek_tokenを1つずつ進める"""
        self.current_token = self.peek_token
        self.peek_token = self.tokenizer.next_token()

    def _init_tokens(self) -> None:
        """current_tokenとpeek_tokenを初期化する"""
        # self.current_token = None, self.peek_token = 1つ目のトークン
        self.next_token()
        # self.current_token = 1つ目のトークン, self.peek_token = 2つ目のトークン
        self.next_token()

    def parse_statement(self) -> Statement | None:
        """
        現在のトークンに基づいて文(statement)を解析する

        Returns:
            Statement | None: 解析された文オブジェクト、または解析できなかった場合はNoneを返します。

        Raises:
            ValueError: current_tokenがNoneの場合に発生します。
        """
        if self.current_token is None:
            raise ValueError("current_token is None")

        # _parse_functions = {
        #     TokenType.LET: self.parse_let_statement,
        #     TokenType.RETURN: self.parse_return_statement,
        # }
        match self.current_token.type:
            case TokenType.LET:
                return self.parse_let_statement()
            case TokenType.RETURN:
                return self.parse_return_statement()
            case _:
                return self.parse_expression_statement()

    def parse_let_statement(self) -> Statement | None:
        """
        let文を解析し、LetStatementオブジェクトを返します。

        Returns:
            Statement | None: 解析されたLetStatementオブジェクト、またはNone。

        Raises:
            ValueError: current_tokenがNoneの場合。

        処理の流れ:
        1. current_tokenがNoneの場合、ValueErrorを発生させます。
        2. LetStatementオブジェクトを作成し、current_tokenを設定します。
        3. 次のトークンがIDENT型であることを確認し、そうでない場合はNoneを返します。
        4. LetStatementオブジェクトのname属性にIdentifierオブジェクトを設定します。
        5. 次のトークンがASSIGN型であることを確認し、そうでない場合はNoneを返します。
        6. current_tokenがSEMICOLON型になるまでトークンを進めます。
        7. 解析されたLetStatementオブジェクトを返します。
        """
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
        """
        return文を解析してReturnStatementオブジェクトを生成します。

        現在のトークンがNoneの場合、ValueErrorを発生させます。
        セミコロンに到達するまでトークンを進めます。

        Returns:
            Statement | None: 生成されたReturnStatementオブジェクト。
        """
        if self.current_token is None:
            raise ValueError("current_token is None")
        stmt = ReturnStatement(token=self.current_token)
        while self.current_token.type != TokenType.SEMICOLON:
            self.next_token()
        return stmt

    def parse_expression(self, precedence: Precedence) -> Expression | None:
        if self.current_token is None:
            raise ValueError("current_token is None")
        prefix = self.prefix_parse_functions.get(self.current_token.type)
        if prefix is None:
            return None
        left_expression = prefix()
        return left_expression

    def parse_expression_statement(self) -> ExpressionStatement | None:
        stmt = ExpressionStatement(token=self.current_token, expression=None)
        expression = self.parse_expression(Precedence.LOWEST)
        if expression is not None:
            stmt.expression = expression
        if self.peek_token_is(TokenType.SEMICOLON):
            self.next_token()
        return stmt

    def parse_identifier(self) -> Expression:
        if self.current_token is None:
            raise ValueError("current_token is None")
        return Identifier(token=self.current_token, value=self.current_token.literal)

    def parse_integer_literal(self) -> Expression:
        if self.current_token is None:
            raise ValueError("current_token is None")
        lit = IntegerLiteral(token=self.current_token, value=None)
        try:
            lit.value = int(self.current_token.literal)
        except ValueError:
            self.errors.append(
                UnexpectedToken(
                    f"could not parse {self.current_token.literal} as integer"
                )
            )
        return lit

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

    def _is_end_of_statement(self) -> bool:
        """
        現在のトークンが文の終わりでないことを確認する

        Returns:
            bool: 現在のトークンがNoneでなく、かつトークンのタイプがセミコロンでない場合にTrueを返します。
        """
        return (
            # 現在のトークンがNone、またはEOFトークンの場合はEOFに達していると判断する
            self.current_token is None or self.current_token.type == TokenType.EOF
        )

    def parse_program(self) -> Program:
        """
        1. ASTのルートノードであるProgramノードを生成する
        2. ループを使って、EOFトークンに達するまでトークンを読み込む
        """
        program = Program()
        while not self._is_end_of_statement():
            stmt = self.parse_statement()
            if stmt:
                program.statements.append(stmt)
            self.next_token()
        return program

    def register_prefix(self, token_type: TokenType, fn: PrefixParseFn) -> None:
        self.prefix_parse_functions[token_type] = fn

    def register_infix(self, token_type: TokenType, fn: InfixParseFn) -> None:
        self.infix_parse_functions[token_type] = fn
