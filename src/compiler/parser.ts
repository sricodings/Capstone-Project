// Parser for the multilingual programming language
import { Token, TokenType } from './lexer';
import * as AST from './ast';

export class ParseError extends Error {
  constructor(message: string, public token: Token) {
    super(message);
    this.name = 'ParseError';
  }
}

export class Parser {
  private tokens: Token[];
  private current: number;

  constructor(tokens: Token[]) {
    this.tokens = tokens.filter(token => token.type !== TokenType.NEWLINE);
    this.current = 0;
  }

  private peek(): Token {
    return this.tokens[this.current] || this.tokens[this.tokens.length - 1];
  }

  private previous(): Token {
    return this.tokens[this.current - 1];
  }

  private isAtEnd(): boolean {
    return this.peek().type === TokenType.EOF;
  }

  private advance(): Token {
    if (!this.isAtEnd()) this.current++;
    return this.previous();
  }

  private check(type: TokenType): boolean {
    if (this.isAtEnd()) return false;
    return this.peek().type === type;
  }

  private match(...types: TokenType[]): boolean {
    for (const type of types) {
      if (this.check(type)) {
        this.advance();
        return true;
      }
    }
    return false;
  }

  private consume(type: TokenType, message: string): Token {
    if (this.check(type)) return this.advance();
    throw new ParseError(message, this.peek());
  }

  public parse(): AST.Program {
    const statements: AST.ASTNode[] = [];
    
    while (!this.isAtEnd()) {
      try {
        const stmt = this.declaration();
        if (stmt) statements.push(stmt);
      } catch (error) {
        if (error instanceof ParseError) {
          // Synchronize on error
          this.synchronize();
          throw error;
        }
        throw error;
      }
    }
    
    return new AST.Program(statements);
  }

  private synchronize(): void {
    this.advance();
    
    while (!this.isAtEnd()) {
      if (this.previous().type === TokenType.SEMICOLON) return;
      
      switch (this.peek().type) {
        case TokenType.VAR:
        case TokenType.FUNCTION:
        case TokenType.IF:
        case TokenType.WHILE:
        case TokenType.FOR:
        case TokenType.RETURN:
          return;
      }
      
      this.advance();
    }
  }

  private declaration(): AST.ASTNode | null {
    if (this.match(TokenType.VAR)) return this.varDeclaration();
    if (this.match(TokenType.FUNCTION)) return this.functionDeclaration();
    return this.statement();
  }

  private varDeclaration(): AST.VarDeclaration {
    const name = this.consume(TokenType.IDENTIFIER, "Expected variable name").value;
    
    let initializer: AST.ASTNode | undefined;
    if (this.match(TokenType.ASSIGN)) {
      initializer = this.expression();
    }
    
    this.consume(TokenType.SEMICOLON, "Expected ';' after variable declaration");
    return new AST.VarDeclaration(name, initializer);
  }

  private functionDeclaration(): AST.FunctionDeclaration {
    const name = this.consume(TokenType.IDENTIFIER, "Expected function name").value;
    
    this.consume(TokenType.LPAREN, "Expected '(' after function name");
    const parameters: string[] = [];
    
    if (!this.check(TokenType.RPAREN)) {
      do {
        parameters.push(this.consume(TokenType.IDENTIFIER, "Expected parameter name").value);
      } while (this.match(TokenType.COMMA));
    }
    
    this.consume(TokenType.RPAREN, "Expected ')' after parameters");
    this.consume(TokenType.LBRACE, "Expected '{' before function body");
    
    const body: AST.ASTNode[] = [];
    while (!this.check(TokenType.RBRACE) && !this.isAtEnd()) {
      const stmt = this.declaration();
      if (stmt) body.push(stmt);
    }
    
    this.consume(TokenType.RBRACE, "Expected '}' after function body");
    return new AST.FunctionDeclaration(name, parameters, body);
  }

  private statement(): AST.ASTNode {
    if (this.match(TokenType.IF)) return this.ifStatement();
    if (this.match(TokenType.WHILE)) return this.whileStatement();
    if (this.match(TokenType.FOR)) return this.forStatement();
    if (this.match(TokenType.RETURN)) return this.returnStatement();
    if (this.match(TokenType.LBRACE)) return this.blockStatement();
    
    return this.expressionStatement();
  }

  private ifStatement(): AST.IfStatement {
    this.consume(TokenType.LPAREN, "Expected '(' after 'if'");
    const condition = this.expression();
    this.consume(TokenType.RPAREN, "Expected ')' after if condition");
    
    const thenStatement = this.statement();
    let elseStatement: AST.ASTNode | undefined;
    
    if (this.match(TokenType.ELSE)) {
      elseStatement = this.statement();
    }
    
    return new AST.IfStatement(condition, thenStatement, elseStatement);
  }

  private whileStatement(): AST.WhileStatement {
    this.consume(TokenType.LPAREN, "Expected '(' after 'while'");
    const condition = this.expression();
    this.consume(TokenType.RPAREN, "Expected ')' after while condition");
    const body = this.statement();
    
    return new AST.WhileStatement(condition, body);
  }

  private forStatement(): AST.ForStatement {
    this.consume(TokenType.LPAREN, "Expected '(' after 'for'");
    
    let initializer: AST.ASTNode | null = null;
    if (this.match(TokenType.SEMICOLON)) {
      initializer = null;
    } else if (this.match(TokenType.VAR)) {
      initializer = this.varDeclaration();
    } else {
      initializer = this.expressionStatement();
    }
    
    let condition: AST.ASTNode | null = null;
    if (!this.check(TokenType.SEMICOLON)) {
      condition = this.expression();
    }
    this.consume(TokenType.SEMICOLON, "Expected ';' after for loop condition");
    
    let increment: AST.ASTNode | null = null;
    if (!this.check(TokenType.RPAREN)) {
      increment = this.expression();
    }
    this.consume(TokenType.RPAREN, "Expected ')' after for clauses");
    
    const body = this.statement();
    
    return new AST.ForStatement(initializer, condition, increment, body);
  }

  private returnStatement(): AST.ReturnStatement {
    let value: AST.ASTNode | undefined;
    if (!this.check(TokenType.SEMICOLON)) {
      value = this.expression();
    }
    
    this.consume(TokenType.SEMICOLON, "Expected ';' after return value");
    return new AST.ReturnStatement(value);
  }

  private blockStatement(): AST.BlockStatement {
    const statements: AST.ASTNode[] = [];
    
    while (!this.check(TokenType.RBRACE) && !this.isAtEnd()) {
      const stmt = this.declaration();
      if (stmt) statements.push(stmt);
    }
    
    this.consume(TokenType.RBRACE, "Expected '}' after block");
    return new AST.BlockStatement(statements);
  }

  private expressionStatement(): AST.ExpressionStatement {
    const expr = this.expression();
    this.consume(TokenType.SEMICOLON, "Expected ';' after expression");
    return new AST.ExpressionStatement(expr);
  }

  private expression(): AST.ASTNode {
    return this.assignment();
  }

  private assignment(): AST.ASTNode {
    const expr = this.or();
    
    if (this.match(TokenType.ASSIGN)) {
      const value = this.assignment();
      
      if (expr instanceof AST.Identifier) {
        return new AST.AssignmentExpression(expr.name, value);
      }
      
      throw new ParseError("Invalid assignment target", this.previous());
    }
    
    return expr;
  }

  private or(): AST.ASTNode {
    let expr = this.and();
    
    while (this.match(TokenType.OR)) {
      const operator = this.previous().value;
      const right = this.and();
      expr = new AST.BinaryExpression(expr, operator, right);
    }
    
    return expr;
  }

  private and(): AST.ASTNode {
    let expr = this.equality();
    
    while (this.match(TokenType.AND)) {
      const operator = this.previous().value;
      const right = this.equality();
      expr = new AST.BinaryExpression(expr, operator, right);
    }
    
    return expr;
  }

  private equality(): AST.ASTNode {
    let expr = this.comparison();
    
    while (this.match(TokenType.NOT_EQUAL, TokenType.EQUAL)) {
      const operator = this.previous().value;
      const right = this.comparison();
      expr = new AST.BinaryExpression(expr, operator, right);
    }
    
    return expr;
  }

  private comparison(): AST.ASTNode {
    let expr = this.term();
    
    while (this.match(TokenType.GREATER_THAN, TokenType.GREATER_EQUAL, TokenType.LESS_THAN, TokenType.LESS_EQUAL)) {
      const operator = this.previous().value;
      const right = this.term();
      expr = new AST.BinaryExpression(expr, operator, right);
    }
    
    return expr;
  }

  private term(): AST.ASTNode {
    let expr = this.factor();
    
    while (this.match(TokenType.MINUS, TokenType.PLUS)) {
      const operator = this.previous().value;
      const right = this.factor();
      expr = new AST.BinaryExpression(expr, operator, right);
    }
    
    return expr;
  }

  private factor(): AST.ASTNode {
    let expr = this.unary();
    
    while (this.match(TokenType.DIVIDE, TokenType.MULTIPLY, TokenType.MODULO)) {
      const operator = this.previous().value;
      const right = this.unary();
      expr = new AST.BinaryExpression(expr, operator, right);
    }
    
    return expr;
  }

  private unary(): AST.ASTNode {
    if (this.match(TokenType.NOT, TokenType.MINUS)) {
      const operator = this.previous().value;
      const right = this.unary();
      return new AST.UnaryExpression(operator, right);
    }
    
    return this.call();
  }

  private call(): AST.ASTNode {
    let expr = this.primary();
    
    while (true) {
      if (this.match(TokenType.LPAREN)) {
        expr = this.finishCall(expr);
      } else {
        break;
      }
    }
    
    return expr;
  }

  private finishCall(callee: AST.ASTNode): AST.CallExpression {
    const args: AST.ASTNode[] = [];
    
    if (!this.check(TokenType.RPAREN)) {
      do {
        args.push(this.expression());
      } while (this.match(TokenType.COMMA));
    }
    
    this.consume(TokenType.RPAREN, "Expected ')' after arguments");
    return new AST.CallExpression(callee, args);
  }

  private primary(): AST.ASTNode {
    if (this.match(TokenType.TRUE)) {
      return new AST.Literal(true, 'boolean');
    }
    
    if (this.match(TokenType.FALSE)) {
      return new AST.Literal(false, 'boolean');
    }
    
    if (this.match(TokenType.NULL)) {
      return new AST.Literal(null, 'null');
    }
    
    if (this.match(TokenType.NUMBER)) {
      const value = parseFloat(this.previous().value);
      return new AST.Literal(value, 'number');
    }
    
    if (this.match(TokenType.STRING)) {
      return new AST.Literal(this.previous().value, 'string');
    }
    
    if (this.match(TokenType.IDENTIFIER)) {
      return new AST.Identifier(this.previous().value);
    }
    
    if (this.match(TokenType.LPAREN)) {
      const expr = this.expression();
      this.consume(TokenType.RPAREN, "Expected ')' after expression");
      return expr;
    }
    
    throw new ParseError("Expected expression", this.peek());
  }
}