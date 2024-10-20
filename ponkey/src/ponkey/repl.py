from rich import pretty

from ponkey.lexer import Lexer
from ponkey.token import Token, TokenType


class REPL:
    PREFIX: str = "ponkey>> "
    pretty.install()

    def __init__(self) -> None:
        pass

    def start(self):
        while True:
            print(self.PREFIX, end="")
            line = input()
            lexer = Lexer(line)
            while True:
                token = lexer.next_token()
                if token.type == TokenType.EOF:
                    break
                print(token)
