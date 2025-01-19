from abc import ABCMeta, abstractmethod

from ponkey.token import Token, TokenType


class Node(metaclass=ABCMeta):
    """ASTを構成するノードの抽象基底クラス

    token_literalメソッドは、ノードが関連付けられているトークンのリテラル値を返す。
    stringメソッドは、ノードのデバッグ用文字列表現を返す。
    """

    @abstractmethod
    def token_literal(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def string(self) -> str:
        raise NotImplementedError


class Statement(Node):
    """文ノード

    式と文をわけているのは、本来expressionを使うところでstatementを使ったときに
    エラーを教えてくれるようにできるかもしれないから
    """

    @abstractmethod
    def statement_node(self) -> None:
        raise NotImplementedError

    def string(self) -> str:
        raise NotImplementedError


class Expression(Node):
    """式ノード

    式と文をわけているのは、本来expressionを使うところでstatementを使ったときに
    エラーを教えてくれるようにできるかもしれないから
    """

    @abstractmethod
    def expression_node(self) -> None:
        raise NotImplementedError

    def string(self) -> str:
        raise NotImplementedError


class Program(Node):
    """
    AST（抽象構文木）のルートノードを表すクラス

    Nodeクラスの具体クラスであるため、token_literalメソッドとstringメソッドを実装している。
    Ponkeyのプログラムは複数の文(statement)から構成されるため、statements属性にStatementのリストを持つ。

    Attributes:
        statements (list[Statement]): プログラム内の文のリスト。

    Methods:
        token_literal() -> str:
            最初の文のトークンリテラルを返します。文がない場合は空文字列を返します。

        string() -> str:
            プログラム内のすべての文を連結した文字列を返します。
    """

    def __init__(self, statements: list[Statement] | None = None) -> None:
        if statements is None:
            self.statements = []
        else:
            self.statements = statements

    def token_literal(self) -> str:
        """最初の文のトークンリテラルを返す

        Returns:
            str: self.statementsが空でない場合は、最初の文のトークンリテラルを返す。
                 空の場合は空文字列を返す。
        """
        if self.statements:
            return self.statements[0].token_literal()
        else:
            return ""

    def string(self) -> str:
        return "".join([stmt.string() for stmt in self.statements])


class Identifier(Expression):
    def __init__(self, token: Token, value: str) -> None:
        if token.type != TokenType.IDENT:
            raise ValueError(f"token.type is not TokenType.IDENT {TokenType.IDENT}")
        self.token = token  # TokenType.IDENT
        self.value = value

    def expression_node(self) -> None:
        raise NotImplementedError

    def token_literal(self) -> str:
        return self.token.literal

    def string(self) -> str:
        return self.value


class LetStatement(Statement):
    """
    let文を表現するためのASTノード

    token_literalとstringメソッドを実装しているため、Nodeクラスの具体クラスである。
    statement_nodeを実装しているため、Statementクラスの具体クラスである。

    nameは束縛の識別子を表し、valueはその識別子に束縛される式を表す。

    Attributes:
        token (Token): 'let'キーワードを表すトークン。
        name (Identifier | None): 変数名を表す識別子。デフォルトはNone。
            nameは束縛の識別子を表し、valueはその識別子に束縛される式を表す。
        value (Expression | None): 変数に代入される式。デフォルトはNone。

    Methods:
        statement_node() -> None:
            ステートメントノードを示すメソッド。実装はされていません。

        token_literal() -> str:
            トークンのリテラル値を返します。

        string() -> str:
            'let'文を文字列として返します。nameがNoneの場合はValueErrorを発生させます。
    """

    def __init__(
        self,
        token: Token,
        name: Identifier | None = None,
        value: Expression | None = None,
    ) -> None:
        if token.literal != TokenType.LET:
            raise ValueError(f"token.literal is not TokenType.LET {TokenType.LET}")
        self.token = token  # TokenType.LET
        self.name = name
        self.value = value

    def statement_node(self) -> None:
        raise NotImplementedError

    def token_literal(self) -> str:
        return self.token.literal

    def string(self) -> str:
        if self.name is None:
            raise ValueError("self.name is None")
        out = f"{self.token_literal()} {self.name.string()} = "
        if self.value:
            out += self.value.string()
        out += ";"
        return out


class ReturnStatement(Statement):
    """return文のASTノード

    return <expression>;

    ReturnStatementはreturnのトークンと式を保持する。
    """

    def __init__(self, token: Token) -> None:
        if token.literal != TokenType.RETURN:
            raise ValueError(
                f"token.literal is not TokenType.RETURN {TokenType.RETURN}"
            )
        self.token = token
        self.return_value: Expression | None = None

    def statement_node(self) -> None:
        raise NotImplementedError

    def token_literal(self) -> str:
        return self.token.literal

    def string(self) -> str:
        out = f"{self.token_literal()}"
        if self.return_value:
            out += self.return_value.string()
        out += ";"
        return out


class ExpressionStatement(Statement):
    """式文のASTノード

    式文はx+10;のような式だけの文を表す。

    Attributes:
        token (Token): 式文の最初のトークン
        expression (Expression | None): 式文の式
    """

    def __init__(
        self, token: Token | None, expression: Expression | None = None
    ) -> None:
        self.token = token
        self.expression = expression

    def statement_node(self) -> None:
        raise NotImplementedError

    def expression_node(self) -> None:
        raise NotImplementedError

    def token_literal(self) -> str:
        if not self.token:
            return ""
        return self.token.literal

    def string(self) -> str:
        if not self.expression:
            return ""
        return self.expression.string()


class IntegerLiteral(Expression):
    def __init__(self, token: Token, value: int | None = None) -> None:
        if token.type != TokenType.INT:
            raise ValueError(f"token.type is not TokenType.INT {TokenType.INT}")
        self.token = token
        self.value = value

    def expression_node(self) -> None:
        raise NotImplementedError

    def token_literal(self) -> str:
        return self.token.literal

    def string(self) -> str:
        return self.token.literal
