from rich import pretty

from ponkey.token import TokenType
from ponkey.tokenizer import Tokenizer


class REPL:
    PREFIX: str = "ponkey>> "
    pretty.install()

    def __init__(self) -> None:
        pass

    def start(self) -> None:
        while True:
            print(self.PREFIX, end="")
            line = input()
            tokenizer = Tokenizer(line)
            while True:
                token = tokenizer.next_token()
                if token.type == TokenType.EOF:
                    break
                print(token)
