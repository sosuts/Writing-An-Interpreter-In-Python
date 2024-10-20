use monkey::token::Token;

fn main() {
    let input = String::from("=+(){},;");
    let expected_tokens: Vec<Token> = vec![
        Token::ASSIGN,
        Token::PLUS,
        Token::LPAREN,
        Token::RPAREN,
        Token::LBRACE,
        Token::RBRACE,
        Token::COMMA,
        Token::SEMICOLON,
    ];
    for v in input.split("").collect::<Vec<&str>>() {
        println!("{}", v)
    }
}
