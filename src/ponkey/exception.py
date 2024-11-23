class UnexpectedToken(Exception):
    def __init__(self, expected, got):
        self.expected = expected
        self.got = got

    def __str__(self):
        return f"expected next token to be {self.expected}, got {self.got} instead"
