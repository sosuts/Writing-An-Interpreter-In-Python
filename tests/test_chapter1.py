from ponkey.token import Token, TokenType
from ponkey.tokenizer import Tokenizer


class TestTokenizerInit:
    def test_next_token1(self):
        input = "=+(){},;"
        expected_results = [
            Token(TokenType.ASSIGN, "="),
            Token(TokenType.PLUS, "+"),
            Token(TokenType.LPAREN, "("),
            Token(TokenType.RPAREN, ")"),
            Token(TokenType.LBRACE, "{"),
            Token(TokenType.RBRACE, "}"),
            Token(TokenType.COMMA, ","),
            Token(TokenType.SEMICOLON, ";"),
            Token(TokenType.EOF, ""),
        ]

        tokenizer = Tokenizer(input=input)
        assert tokenizer.input == input
        assert tokenizer.position == 0
        assert tokenizer.read_position == 1
        assert tokenizer.ch == "="
        for i, expected_result in enumerate(expected_results):
            tok = tokenizer.next_token()
            assert tok == expected_result

    def test_next_token2(self):
        input = """let five = 5;
        let ten = 10;
        let add = func(x, y) {
            x + y;
        };
        let result = add(five, ten);
        """
        expected_results = [
            Token(TokenType.LET, "let"),
            Token(TokenType.IDENT, "five"),
            Token(TokenType.ASSIGN, "="),
            Token(TokenType.INT, "5"),
            Token(TokenType.SEMICOLON, ";"),
            Token(TokenType.LET, "let"),
            Token(TokenType.IDENT, "ten"),
            Token(TokenType.ASSIGN, "="),
            Token(TokenType.INT, "10"),
            Token(TokenType.SEMICOLON, ";"),
            Token(TokenType.LET, "let"),
            Token(TokenType.IDENT, "add"),
            Token(TokenType.ASSIGN, "="),
            Token(TokenType.FUNCTION, "func"),
            Token(TokenType.LPAREN, "("),
            Token(TokenType.IDENT, "x"),
            Token(TokenType.COMMA, ","),
            Token(TokenType.IDENT, "y"),
            Token(TokenType.RPAREN, ")"),
            Token(TokenType.LBRACE, "{"),
            Token(TokenType.IDENT, "x"),
            Token(TokenType.PLUS, "+"),
            Token(TokenType.IDENT, "y"),
            Token(TokenType.SEMICOLON, ";"),
            Token(TokenType.RBRACE, "}"),
            Token(TokenType.SEMICOLON, ";"),
            Token(TokenType.LET, "let"),
            Token(TokenType.IDENT, "result"),
            Token(TokenType.ASSIGN, "="),
            Token(TokenType.IDENT, "add"),
            Token(TokenType.LPAREN, "("),
            Token(TokenType.IDENT, "five"),
            Token(TokenType.COMMA, ","),
            Token(TokenType.IDENT, "ten"),
            Token(TokenType.RPAREN, ")"),
            Token(TokenType.SEMICOLON, ";"),
            Token(TokenType.EOF, ""),
        ]
        tokenizer = Tokenizer(input=input)
        for i, expected_result in enumerate(expected_results):
            tok = tokenizer.next_token()
            assert tok == expected_result

    def test_next_token3(self):
        """Test for 1.4 - Extending our Token Set and Tokenizer"""
        input = """let five = 5;
        let ten = 10;
        let add = func(x, y) {
            x + y;
        };
        let result = add(five, ten);
        !-/*5;
        5 < 10 > 5;

        if (5 < 10) {
            return true;
        } else {
            return false;
        }

        10 == 10;
        10 != 9;
        """
        expected_results = [
            Token(TokenType.LET, "let"),
            Token(TokenType.IDENT, "five"),
            Token(TokenType.ASSIGN, "="),
            Token(TokenType.INT, "5"),
            Token(TokenType.SEMICOLON, ";"),
            Token(TokenType.LET, "let"),
            Token(TokenType.IDENT, "ten"),
            Token(TokenType.ASSIGN, "="),
            Token(TokenType.INT, "10"),
            Token(TokenType.SEMICOLON, ";"),
            Token(TokenType.LET, "let"),
            Token(TokenType.IDENT, "add"),
            Token(TokenType.ASSIGN, "="),
            Token(TokenType.FUNCTION, "func"),
            Token(TokenType.LPAREN, "("),
            Token(TokenType.IDENT, "x"),
            Token(TokenType.COMMA, ","),
            Token(TokenType.IDENT, "y"),
            Token(TokenType.RPAREN, ")"),
            Token(TokenType.LBRACE, "{"),
            Token(TokenType.IDENT, "x"),
            Token(TokenType.PLUS, "+"),
            Token(TokenType.IDENT, "y"),
            Token(TokenType.SEMICOLON, ";"),
            Token(TokenType.RBRACE, "}"),
            Token(TokenType.SEMICOLON, ";"),
            Token(TokenType.LET, "let"),
            Token(TokenType.IDENT, "result"),
            Token(TokenType.ASSIGN, "="),
            Token(TokenType.IDENT, "add"),
            Token(TokenType.LPAREN, "("),
            Token(TokenType.IDENT, "five"),
            Token(TokenType.COMMA, ","),
            Token(TokenType.IDENT, "ten"),
            Token(TokenType.RPAREN, ")"),
            Token(TokenType.SEMICOLON, ";"),
            Token(TokenType.BANG, "!"),
            Token(TokenType.MINUS, "-"),
            Token(TokenType.SLASH, "/"),
            Token(TokenType.ASTERISK, "*"),
            Token(TokenType.INT, "5"),
            Token(TokenType.SEMICOLON, ";"),
            Token(TokenType.INT, "5"),
            Token(TokenType.LT, "<"),
            Token(TokenType.INT, "10"),
            Token(TokenType.GT, ">"),
            Token(TokenType.INT, "5"),
            Token(TokenType.SEMICOLON, ";"),
            Token(TokenType.IF, "if"),
            Token(TokenType.LPAREN, "("),
            Token(TokenType.INT, "5"),
            Token(TokenType.LT, "<"),
            Token(TokenType.INT, "10"),
            Token(TokenType.RPAREN, ")"),
            Token(TokenType.LBRACE, "{"),
            Token(TokenType.RETURN, "return"),
            Token(TokenType.TRUE, "true"),
            Token(TokenType.SEMICOLON, ";"),
            Token(TokenType.RBRACE, "}"),
            Token(TokenType.ELSE, "else"),
            Token(TokenType.LBRACE, "{"),
            Token(TokenType.RETURN, "return"),
            Token(TokenType.FALSE, "false"),
            Token(TokenType.SEMICOLON, ";"),
            Token(TokenType.RBRACE, "}"),
            Token(TokenType.INT, "10"),
            Token(TokenType.EQ, "=="),
            Token(TokenType.INT, "10"),
            Token(TokenType.SEMICOLON, ";"),
            Token(TokenType.INT, "10"),
            Token(TokenType.NEQ, "!="),
            Token(TokenType.INT, "9"),
            Token(TokenType.SEMICOLON, ";"),
            Token(TokenType.EOF, ""),
        ]
        tokenizer = Tokenizer(input)
        for expected_result in expected_results:
            tok = tokenizer.next_token()
            assert tok == expected_result

    def test_empty_input(self):
        input = ""
        expected_results = [
            Token(TokenType.EOF, ""),
        ]
        tokenizer = Tokenizer(input=input)
        for expected_result in expected_results:
            tok = tokenizer.next_token()
            assert tok == expected_result
