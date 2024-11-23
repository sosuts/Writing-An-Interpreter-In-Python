from ponkey.lexer import Lexer
from ponkey.parser import Parser
from ponkey.token import TokenType


def check_parser_errors(parser):
    errors = parser.errors
    if not errors:
        return
    print("parser has {} errors".format(len(errors)))
    for error in errors:
        print("parser error: {}".format(error))


class TestLetStatements:
    def _test_let_statement(self, statement, name) -> bool:
        if statement.token_literal() != TokenType.LET:
            return False
        if statement.name.value != name:
            return False
        if statement.name.token_literal() != name:
            return False
        return True

    def test_statements(self):
        input_ = """
        let x = 5;
        let y = 10;
        let foobar = 838838;
        """
        expected_identifiers = ["x", "y", "foobar"]

        lexer = Lexer(input_)
        parser = Parser(lexer)
        program = parser.parse_program()
        assert check_parser_errors(parser) is None
        for i, expected_identifier in enumerate(expected_identifiers):
            self._test_let_statement(program.statements[i], expected_identifier)

    def test_error_messages(self, capsys):
        input_ = """
        let x 5;
        let = 10;
        let 838838;
        """
        expected_error_messages = (
            "parser has 3 errors\n"
            "parser error: expected next token to be =, got INT instead\n"
            "parser error: expected next token to be IDENT, got = instead\n"
            "parser error: expected next token to be IDENT, got INT instead\n"
        )

        lexer = Lexer(input_)
        parser = Parser(lexer)
        parser.parse_program()
        check_parser_errors(parser)
        captured = capsys.readouterr()
        assert captured.out == expected_error_messages


class TestReturnStatement:
    def test_statements(self):
        input_ = """
        return 5;
        return 10;
        return 838838;
        """
        expected_values = [5, 10, 838838]

        lexer = Lexer(input_)
        parser = Parser(lexer)
        program = parser.parse_program()
        check_parser_errors(parser)
        for i, _ in enumerate(expected_values):
            assert program.statements[i].token_literal() == TokenType.RETURN


class TestIdentifierExpression:
    def test_expression(self):
        input_ = "foobar;"
        expected_value = "foobar"

        lexer = Lexer(input_)
        parser = Parser(lexer)
        program = parser.parse_program()
        check_parser_errors(parser)
        assert len(program.statements) == 1
        assert program.statements[0].expression.value == expected_value
