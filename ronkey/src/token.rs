#[derive(Debug, PartialEq)]
pub enum Token {
    ILLEGAL,
    EOF,
    IDENT,
    INT,
    ASSIGN,
    PLUS,
    COMMA,
    SEMICOLON,
    LPAREN,
    RPAREN,
    LBRACE,
    RBRACE,
    FUNCTION,
    LET,
}

impl Token {
    pub fn tokenize(str: &str) -> Self {
        match str {
            "=" => Self::ASSIGN,
            "+" => Self::PLUS,
            "func" => Self::FUNCTION,
            "let" => Self::LET,
            "(" => Self::LPAREN,
            ")" => Self::RPAREN,
            "{" => Self::LBRACE,
            "}" => Self::RBRACE,
            ";" => Self::SEMICOLON,
            "," => Self::COMMA,
            _ => Self::ILLEGAL,
        }
    }
}
