from abc import ABCMeta, abstractmethod

from ponkey.token import Token, TokenType


class Node(metaclass=ABCMeta):
    """ASTを構成するノードの抽象基底クラス"""

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
    def statement_node(self):
        pass


class Expression(Node):
    """式ノード

    式と文をわけているのは、本来expressionを使うところでstatementを使ったときにエラーを教えてくれるようにできるかもしれないから
    """

    @abstractmethod
    def expression_node(self):
        pass


class Program(Node):
    """全てのASTのルート"""

    def __init__(self, statements: list[Statement] | None = None) -> None:
        if statements is None:
            self.statements = []
        else:
            self.statements = statements

    def token_literal(self) -> str:
        if self.statements:
            return self.statements[0].token_literal()
        else:
            return ""

    def string(self) -> str:
        return "".join([stmt.string() for stmt in self.statements])


class Identifier(Expression):
    def __init__(self, token: Token, value: str) -> None:
        self.token = token
        self.value = value

    def expression_node(self):
        pass

    def token_literal(self) -> str:
        return self.token.literal

    def string(self) -> str:
        return self.value


class LetStatement(Statement):
    """let文のASTノード

    let <identifier> = <expression>;

    LetStatementはnameとvalueを持つ。nameは子の束縛の識別を保持する。valueは式を保持する。
    """

    def __init__(
        self,
        token: Token,
        name: Identifier | None = None,
        value: Expression | None = None,
    ) -> None:
        if token.literal != TokenType.LET:
            raise ValueError(f"token.literal is not TokenType.LET {TokenType.LET}")
        self.token = token
        self.name = name
        self.value = value

    def statement_node(self) -> None:
        pass

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

    def statement_node(self):
        pass

    def token_literal(self) -> str:
        return self.token.literal

    def string(self) -> str:
        out = f"{self.token_literal()}"
        if self.return_value:
            out += self.return_value.string()
        out += ";"
        return out


class ExpressionStatement(Statement):
    def __init__(self, token: Token, expression: Expression) -> None:
        self.token = token
        self.expression = expression

    def expression_node(self):
        pass

    def token_literal(self) -> str:
        return self.token.literal

    def string(self) -> str:
        if not self.expression:
            return ""
        return self.expression.string()
