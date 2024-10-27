from ponkey.lexer import Lexer
from ponkey.parser import Parser


class TestStatements:
    def _test_let_statement(self, statement, name) -> bool:
        if statement.token_literal() != "let":
            return False
        if statement.name.value != name:
            return False
        if statement.name.token_literal() != name:
            return False
        return True

    def test_statements(self):
        input_ = """
        let x 5;
        let = 10;
        let 838838;
        """
        expected_identifiers = ["x", "y", "foobar"]
        # expected_values = ["5", "10", "838838"]

        lexer = Lexer(input_)
        parser = Parser(lexer)
        program = parser.parse_program()
        self.check_parser_errors(parser)
        for i, expected_identifier in enumerate(expected_identifiers):
            assert (
                self._test_let_statement(program.statements[i], expected_identifier)
                is True
            )

    def check_parser_errors(self, parser):
        errors = parser.errors
        if not errors:
            return
        print("parser has {} errors".format(len(errors)))
        for error in errors:
            print("parser error: {}".format(error))
        assert False
