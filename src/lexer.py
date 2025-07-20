"""
Lexer for Multilingual Programming Language
Uses PLY (Python Lex-Yacc) for tokenization with language-aware keywords
"""

import ply.lex as lex
from typing import List, Dict, Any
from .language_definitions import LanguageDefinitions

class MultilingualLexer:
    """Multilingual lexer with language-aware tokenization"""
    
    def __init__(self, language: str = 'english'):
        self.language_defs = LanguageDefinitions()
        self.current_language = language
        self.tokens = []
        self.lexer = None
        self._setup_tokens()
        self._build_lexer()
    
    def _setup_tokens(self):
        """Setup token definitions"""
        # Basic tokens
        self.tokens = [
            'NUMBER',
            'STRING', 
            'IDENTIFIER',
            'PLUS',
            'MINUS',
            'TIMES',
            'DIVIDE',
            'MODULO',
            'ASSIGN',
            'EQ',
            'NE', 
            'LT',
            'LE',
            'GT',
            'GE',
            'LPAREN',
            'RPAREN',
            'LBRACE',
            'RBRACE',
            'LBRACKET',
            'RBRACKET',
            'SEMICOLON',
            'COMMA',
            'DOT',
            'COLON',
            'NEWLINE'
        ]
        
        # Add language-specific keyword tokens
        keywords = self.language_defs.get_keywords_for_language(self.current_language)
        for eng_keyword in keywords.keys():
            token_name = eng_keyword.upper()
            if token_name not in self.tokens:
                self.tokens.append(token_name)
    
    def _build_lexer(self):
        """Build the lexer with current language settings"""
        
        # Token rules
        t_PLUS = r'\+'
        t_MINUS = r'-'
        t_TIMES = r'\*'
        t_DIVIDE = r'/'
        t_MODULO = r'%'
        t_ASSIGN = r'='
        t_EQ = r'=='
        t_NE = r'!='
        t_LT = r'<'
        t_LE = r'<='
        t_GT = r'>'
        t_GE = r'>='
        t_LPAREN = r'\('
        t_RPAREN = r'\)'
        t_LBRACE = r'\{'
        t_RBRACE = r'\}'
        t_LBRACKET = r'\['
        t_RBRACKET = r'\]'
        t_SEMICOLON = r';'
        t_COMMA = r','
        t_DOT = r'\.'
        t_COLON = r':'
        
        # Ignored characters (spaces and tabs)
        t_ignore = ' \t'
        
        def t_NUMBER(t):
            r'\d+'
            t.value = int(t.value)
            return t
        
        def t_STRING(t):
            r'"([^"\\]|\\.)*"'
            t.value = t.value[1:-1]  # Remove quotes
            return t
        
        def t_IDENTIFIER(t):
            r'[a-zA-Z_][a-zA-Z_0-9]*'
            # Check if identifier is a keyword in current language
            keywords = self.language_defs.get_keywords_for_language(self.current_language)
            reverse_keywords = {v: k for k, v in keywords.items()}
            
            if t.value in reverse_keywords:
                t.type = reverse_keywords[t.value].upper()
            else:
                t.type = 'IDENTIFIER'
            return t
        
        def t_NEWLINE(t):
            r'\n+'
            t.lexer.lineno += len(t.value)
            return t
        
        def t_error(t):
            print(f"Illegal character '{t.value[0]}' at line {t.lineno}")
            t.lexer.skip(1)
        
        # Set up the lexer
        self.lexer = lex.lex()
    
    def change_language(self, new_language: str):
        """Change the lexer language and rebuild"""
        if new_language in self.language_defs.get_language_list():
            self.current_language = new_language
            self._setup_tokens()
            self._build_lexer()
    
    def tokenize(self, code: str) -> List[Dict[str, Any]]:
        """Tokenize code and return list of tokens"""
        self.lexer.input(code)
        tokens = []
        
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            
            tokens.append({
                'type': tok.type,
                'value': tok.value,
                'lineno': tok.lineno,
                'lexpos': tok.lexpos
            })
        
        return tokens
    
    def get_syntax_highlighting_rules(self) -> Dict[str, str]:
        """Get syntax highlighting rules for current language"""
        keywords = self.language_defs.get_keywords_for_language(self.current_language)
        
        return {
            'keywords': list(keywords.values()),
            'operators': ['+', '-', '*', '/', '%', '=', '==', '!=', '<', '<=', '>', '>='],
            'delimiters': ['(', ')', '{', '}', '[', ']', ';', ',', '.', ':'],
            'comments': ['#', '//'],
            'strings': ['"', "'"]
        }