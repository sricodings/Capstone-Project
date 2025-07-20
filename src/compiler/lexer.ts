// Lexer for the multilingual programming language
import { LanguageDefinition } from '../language/definitions';

export enum TokenType {
  // Literals
  NUMBER = 'NUMBER',
  STRING = 'STRING',
  IDENTIFIER = 'IDENTIFIER',
  
  // Keywords
  IF = 'IF',
  ELSE = 'ELSE',
  WHILE = 'WHILE',
  FOR = 'FOR',
  FUNCTION = 'FUNCTION',
  RETURN = 'RETURN',
  VAR = 'VAR',
  TRUE = 'TRUE',
  FALSE = 'FALSE',
  NULL = 'NULL',
  
  // Operators
  ASSIGN = 'ASSIGN',
  EQUAL = 'EQUAL',
  NOT_EQUAL = 'NOT_EQUAL',
  LESS_THAN = 'LESS_THAN',
  GREATER_THAN = 'GREATER_THAN',
  LESS_EQUAL = 'LESS_EQUAL',
  GREATER_EQUAL = 'GREATER_EQUAL',
  PLUS = 'PLUS',
  MINUS = 'MINUS',
  MULTIPLY = 'MULTIPLY',
  DIVIDE = 'DIVIDE',
  MODULO = 'MODULO',
  AND = 'AND',
  OR = 'OR',
  NOT = 'NOT',
  
  // Delimiters
  LPAREN = 'LPAREN',
  RPAREN = 'RPAREN',
  LBRACE = 'LBRACE',
  RBRACE = 'RBRACE',
  SEMICOLON = 'SEMICOLON',
  COMMA = 'COMMA',
  
  // Special
  NEWLINE = 'NEWLINE',
  EOF = 'EOF',
  UNKNOWN = 'UNKNOWN'
}

export interface Token {
  type: TokenType;
  value: string;
  line: number;
  column: number;
}

export class Lexer {
  private source: string;
  private position: number;
  private line: number;
  private column: number;
  private language: LanguageDefinition;

  constructor(source: string, language: LanguageDefinition) {
    this.source = source;
    this.position = 0;
    this.line = 1;
    this.column = 1;
    this.language = language;
  }

  private peek(offset: number = 0): string {
    const pos = this.position + offset;
    return pos < this.source.length ? this.source[pos] : '';
  }

  private advance(): string {
    if (this.position < this.source.length) {
      const char = this.source[this.position];
      this.position++;
      if (char === '\n') {
        this.line++;
        this.column = 1;
      } else {
        this.column++;
      }
      return char;
    }
    return '';
  }

  private skipWhitespace(): void {
    while (this.position < this.source.length) {
      const char = this.peek();
      if (char === ' ' || char === '\t' || char === '\r') {
        this.advance();
      } else {
        break;
      }
    }
  }

  private readNumber(): Token {
    const start = this.position;
    const startColumn = this.column;
    let value = '';
    
    while (this.position < this.source.length) {
      const char = this.peek();
      if (/[0-9.]/.test(char)) {
        value += this.advance();
      } else {
        break;
      }
    }
    
    return {
      type: TokenType.NUMBER,
      value,
      line: this.line,
      column: startColumn
    };
  }

  private readString(): Token {
    const startColumn = this.column;
    let value = '';
    const quote = this.advance(); // Skip opening quote
    
    while (this.position < this.source.length) {
      const char = this.peek();
      if (char === quote) {
        this.advance(); // Skip closing quote
        break;
      } else if (char === '\\') {
        this.advance();
        const escaped = this.advance();
        switch (escaped) {
          case 'n': value += '\n'; break;
          case 't': value += '\t'; break;
          case 'r': value += '\r'; break;
          case '\\': value += '\\'; break;
          case '"': value += '"'; break;
          case "'": value += "'"; break;
          default: value += escaped; break;
        }
      } else {
        value += this.advance();
      }
    }
    
    return {
      type: TokenType.STRING,
      value,
      line: this.line,
      column: startColumn
    };
  }

  private readIdentifier(): Token {
    const startColumn = this.column;
    let value = '';
    
    while (this.position < this.source.length) {
      const char = this.peek();
      if (/[a-zA-Z0-9_]/.test(char)) {
        value += this.advance();
      } else {
        break;
      }
    }
    
    // Check if it's a keyword in the current language
    const tokenType = this.getKeywordTokenType(value);
    
    return {
      type: tokenType,
      value,
      line: this.line,
      column: startColumn
    };
  }

  private getKeywordTokenType(value: string): TokenType {
    const keywords = this.language.keywords;
    
    for (const [englishKeyword, translatedKeyword] of Object.entries(keywords)) {
      if (value === translatedKeyword) {
        switch (englishKeyword) {
          case 'if': return TokenType.IF;
          case 'else': return TokenType.ELSE;
          case 'while': return TokenType.WHILE;
          case 'for': return TokenType.FOR;
          case 'function': return TokenType.FUNCTION;
          case 'return': return TokenType.RETURN;
          case 'var': return TokenType.VAR;
          case 'true': return TokenType.TRUE;
          case 'false': return TokenType.FALSE;
          case 'null': return TokenType.NULL;
        }
      }
    }
    
    return TokenType.IDENTIFIER;
  }

  public tokenize(): Token[] {
    const tokens: Token[] = [];
    
    while (this.position < this.source.length) {
      this.skipWhitespace();
      
      if (this.position >= this.source.length) {
        break;
      }
      
      const char = this.peek();
      const startColumn = this.column;
      
      // Numbers
      if (/[0-9]/.test(char)) {
        tokens.push(this.readNumber());
        continue;
      }
      
      // Strings
      if (char === '"' || char === "'") {
        tokens.push(this.readString());
        continue;
      }
      
      // Identifiers and keywords
      if (/[a-zA-Z_]/.test(char)) {
        tokens.push(this.readIdentifier());
        continue;
      }
      
      // Two-character operators
      if (this.position + 1 < this.source.length) {
        const twoChar = char + this.peek(1);
        let tokenType: TokenType | null = null;
        
        switch (twoChar) {
          case '==': tokenType = TokenType.EQUAL; break;
          case '!=': tokenType = TokenType.NOT_EQUAL; break;
          case '<=': tokenType = TokenType.LESS_EQUAL; break;
          case '>=': tokenType = TokenType.GREATER_EQUAL; break;
          case '&&': tokenType = TokenType.AND; break;
          case '||': tokenType = TokenType.OR; break;
        }
        
        if (tokenType) {
          tokens.push({
            type: tokenType,
            value: twoChar,
            line: this.line,
            column: startColumn
          });
          this.advance();
          this.advance();
          continue;
        }
      }
      
      // Single-character tokens
      let tokenType: TokenType | null = null;
      
      switch (char) {
        case '=': tokenType = TokenType.ASSIGN; break;
        case '<': tokenType = TokenType.LESS_THAN; break;
        case '>': tokenType = TokenType.GREATER_THAN; break;
        case '+': tokenType = TokenType.PLUS; break;
        case '-': tokenType = TokenType.MINUS; break;
        case '*': tokenType = TokenType.MULTIPLY; break;
        case '/': tokenType = TokenType.DIVIDE; break;
        case '%': tokenType = TokenType.MODULO; break;
        case '!': tokenType = TokenType.NOT; break;
        case '(': tokenType = TokenType.LPAREN; break;
        case ')': tokenType = TokenType.RPAREN; break;
        case '{': tokenType = TokenType.LBRACE; break;
        case '}': tokenType = TokenType.RBRACE; break;
        case ';': tokenType = TokenType.SEMICOLON; break;
        case ',': tokenType = TokenType.COMMA; break;
        case '\n': tokenType = TokenType.NEWLINE; break;
      }
      
      if (tokenType) {
        tokens.push({
          type: tokenType,
          value: char,
          line: this.line,
          column: startColumn
        });
        this.advance();
      } else {
        // Unknown character
        tokens.push({
          type: TokenType.UNKNOWN,
          value: char,
          line: this.line,
          column: startColumn
        });
        this.advance();
      }
    }
    
    tokens.push({
      type: TokenType.EOF,
      value: '',
      line: this.line,
      column: this.column
    });
    
    return tokens;
  }
}