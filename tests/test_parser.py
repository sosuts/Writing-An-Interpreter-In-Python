from pytest import CaptureFixture

from ponkey.ast import Expression, ExpressionStatement, LetStatement, PrefixExpression
from ponkey.parser import Parser
from ponkey.token import TokenType
from ponkey.tokenizer import Tokenizer


def check_parser_errors(parser: Parser) -> None:
    errors = parser.errors
    if not errors:
        return
    print("parser has {} errors".format(len(errors)))
    for error in errors:
        print("parser error: {}".format(error))


class TestLetStatements:
    def _test_let_statement(self, statement: LetStatement, name: str) -> bool:
        if statement.token_literal() != TokenType.LET:
            return False
        if statement.name.value != name:
            return False
        if statement.name.token_literal() != name:
            return False
        return True

    def test_statements(self) -> None:
        input_ = """
        let x = 5;
        let y = 10;
        let foobar = 838838;
        """
        expected_identifiers = ["x", "y", "foobar"]

        tokenizer = Tokenizer(input_)
        parser = Parser(tokenizer)
        program = parser.parse_program()
        check_parser_errors(parser)
        for i, expected_identifier in enumerate(expected_identifiers):
            self._test_let_statement(program.statements[i], expected_identifier)

    def test_error_messages(self, capsys: CaptureFixture[str]) -> None:
        input_ = """
        let x 5;
        let = 10;
        let 838838;
        """
        expected_error_messages = (
            "parser has 4 errors\n"
            "parser error: expected next token to be =, got INT instead\n"
            "parser error: expected next token to be IDENT, got = instead\n"
            "parser error: no prefix parse function for = found\n"
            "parser error: expected next token to be IDENT, got INT instead\n"
        )

        tokenizer = Tokenizer(input_)
        parser = Parser(tokenizer)
        parser.parse_program()
        check_parser_errors(parser)
        captured = capsys.readouterr()
        from pprint import pprint

        pprint(captured.out)
        pprint(len(parser.errors))
        assert captured.out == expected_error_messages


class TestReturnStatement:
    def test_statements(self) -> None:
        input_ = """
        return 5;
        return 10;
        return 838838;
        """
        expected_values = [5, 10, 838838]

        tokenizer = Tokenizer(input_)
        parser = Parser(tokenizer)
        program = parser.parse_program()
        check_parser_errors(parser)
        assert len(program.statements) == len(expected_values)
        for i, _ in enumerate(expected_values):
            assert program.statements[i].token_literal() == TokenType.RETURN


class TestIdentifierExpression:
    def test_expression(self) -> None:
        input_ = "foobar;"
        expected_value = "foobar"

        tokenizer = Tokenizer(input_)
        parser = Parser(tokenizer)
        program = parser.parse_program()
        check_parser_errors(parser)
        assert len(program.statements) == 1
        assert program.statements[0].token_literal() == expected_value


class TestIntegerLiteralExpression:
    def test_integer_literal_expression(self) -> None:
        input_ = "5;"
        expected_value = 5

        tokenizer = Tokenizer(input_)
        parser = Parser(tokenizer)
        program = parser.parse_program()
        check_parser_errors(parser)
        assert len(program.statements) == 1
        assert isinstance(program.statements[0], ExpressionStatement)
        assert isinstance(program.statements[0].expression, Expression)
        assert program.statements[0].token_literal() == str(expected_value)
        assert program.statements[0].expression.value == 5


class TestParsingPrefixExpressions:
    def test_simple_cases(self) -> None:
        expected_operators = ["!", "-"]
        expected_integer_values = [5, 11]
        inputs: list[dict[str, str | int]] = [
            {"input": "!5;", "operator": "!", "integer_value": 5},
            {"input": "-11;", "operator": "-", "integer_value": 11},
        ]
        for i, operator, value in zip(
            inputs, expected_operators, expected_integer_values
        ):
            tokenizer = Tokenizer(i["input"])
            parser = Parser(tokenizer)
            program = parser.parse_program()
            check_parser_errors(parser)
            assert len(program.statements) == 1

            stmt = program.statements[0]
            assert isinstance(stmt, ExpressionStatement)
            assert isinstance(stmt.expression, PrefixExpression)
            assert isinstance(stmt.expression, Expression)
            assert i["operator"] == operator
            assert i["integer_value"] == value
            # TODO: 2025/1/20 ast.PrefixExpressionは未定義
