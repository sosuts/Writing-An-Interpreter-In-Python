use monkey::lexer::Lexer;
use monkey::token::Token;

mod tests {
    use super::*;

    #[test]
    fn test_next_token() {
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
        let l = Lexer::new(&input);
        // let result: Vec<Token> = input
        //     .chars()
        //     .map(|x| Token::tokenize(&x.to_string()))
        //     .collect();
        // assert_eq!(expected_tokens, result);
    }
}
