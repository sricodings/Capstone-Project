"""
Parser for Multilingual Programming Language
Uses PLY yacc for parsing with AST generation
"""

import ply.yacc as yacc
from typing import List, Dict, Any, Optional
from .lexer import MultilingualLexer
from .ast_nodes import *

class MultilingualParser:
    """Multilingual parser with AST generation"""
    
    def __init__(self, language: str = 'english'):
        self.lexer = MultilingualLexer(language)
        self.tokens = self.lexer.tokens
        self.parser = None
        self.current_language = language
        self._build_parser()
    
    def _build_parser(self):
        """Build the parser with grammar rules"""
        
        # Grammar rules
        def p_program(p):
            '''program : statement_list'''
            p[0] = ProgramNode(p[1])
        
        def p_statement_list(p):
            '''statement_list : statement_list statement
                             | statement'''
            if len(p) == 2:
                p[0] = [p[1]]
            else:
                p[0] = p[1] + [p[2]]
        
        def p_statement(p):
            '''statement : assignment_statement
                        | if_statement
                        | while_statement
                        | for_statement
                        | function_definition
                        | return_statement
                        | print_statement
                        | expression_statement
                        | NEWLINE'''
            if p[1] != '\n':
                p[0] = p[1]
            else:
                p[0] = None
        
        def p_assignment_statement(p):
            '''assignment_statement : VAR IDENTIFIER ASSIGN expression NEWLINE
                                   | IDENTIFIER ASSIGN expression NEWLINE'''
            if len(p) == 6:
                p[0] = AssignmentNode(p[2], p[4], is_declaration=True)
            else:
                p[0] = AssignmentNode(p[1], p[3], is_declaration=False)
        
        def p_if_statement(p):
            '''if_statement : IF expression COLON NEWLINE statement_list
                           | IF expression COLON NEWLINE statement_list ELSE COLON NEWLINE statement_list'''
            if len(p) == 6:
                p[0] = IfNode(p[2], p[5], None)
            else:
                p[0] = IfNode(p[2], p[5], p[9])
        
        def p_while_statement(p):
            '''while_statement : WHILE expression COLON NEWLINE statement_list'''
            p[0] = WhileNode(p[2], p[5])
        
        def p_for_statement(p):
            '''for_statement : FOR IDENTIFIER ASSIGN expression COLON expression COLON NEWLINE statement_list'''
            p[0] = ForNode(p[2], p[4], p[6], p[9])
        
        def p_function_definition(p):
            '''function_definition : FUNCTION IDENTIFIER LPAREN parameter_list RPAREN COLON NEWLINE statement_list'''
            p[0] = FunctionNode(p[2], p[4], p[8])
        
        def p_parameter_list(p):
            '''parameter_list : parameter_list COMMA IDENTIFIER
                             | IDENTIFIER
                             | empty'''
            if len(p) == 2:
                if p[1] is None:
                    p[0] = []
                else:
                    p[0] = [p[1]]
            else:
                p[0] = p[1] + [p[3]]
        
        def p_return_statement(p):
            '''return_statement : RETURN expression NEWLINE
                               | RETURN NEWLINE'''
            if len(p) == 3:
                p[0] = ReturnNode(None)
            else:
                p[0] = ReturnNode(p[2])
        
        def p_print_statement(p):
            '''print_statement : PRINT expression NEWLINE'''
            p[0] = PrintNode(p[2])
        
        def p_expression_statement(p):
            '''expression_statement : expression NEWLINE'''
            p[0] = ExpressionStatementNode(p[1])
        
        def p_expression(p):
            '''expression : logical_or_expression'''
            p[0] = p[1]
        
        def p_logical_or_expression(p):
            '''logical_or_expression : logical_or_expression OR logical_and_expression
                                    | logical_and_expression'''
            if len(p) == 2:
                p[0] = p[1]
            else:
                p[0] = BinaryOpNode(p[1], 'or', p[3])
        
        def p_logical_and_expression(p):
            '''logical_and_expression : logical_and_expression AND equality_expression
                                     | equality_expression'''
            if len(p) == 2:
                p[0] = p[1]
            else:
                p[0] = BinaryOpNode(p[1], 'and', p[3])
        
        def p_equality_expression(p):
            '''equality_expression : equality_expression EQ relational_expression
                                  | equality_expression NE relational_expression
                                  | relational_expression'''
            if len(p) == 2:
                p[0] = p[1]
            else:
                p[0] = BinaryOpNode(p[1], p[2], p[3])
        
        def p_relational_expression(p):
            '''relational_expression : relational_expression LT additive_expression
                                    | relational_expression LE additive_expression
                                    | relational_expression GT additive_expression
                                    | relational_expression GE additive_expression
                                    | additive_expression'''
            if len(p) == 2:
                p[0] = p[1]
            else:
                p[0] = BinaryOpNode(p[1], p[2], p[3])
        
        def p_additive_expression(p):
            '''additive_expression : additive_expression PLUS multiplicative_expression
                                  | additive_expression MINUS multiplicative_expression
                                  | multiplicative_expression'''
            if len(p) == 2:
                p[0] = p[1]
            else:
                p[0] = BinaryOpNode(p[1], p[2], p[3])
        
        def p_multiplicative_expression(p):
            '''multiplicative_expression : multiplicative_expression TIMES unary_expression
                                        | multiplicative_expression DIVIDE unary_expression
                                        | multiplicative_expression MODULO unary_expression
                                        | unary_expression'''
            if len(p) == 2:
                p[0] = p[1]
            else:
                p[0] = BinaryOpNode(p[1], p[2], p[3])
        
        def p_unary_expression(p):
            '''unary_expression : NOT unary_expression
                               | MINUS unary_expression
                               | primary_expression'''
            if len(p) == 2:
                p[0] = p[1]
            else:
                p[0] = UnaryOpNode(p[1], p[2])
        
        def p_primary_expression(p):
            '''primary_expression : NUMBER
                                 | STRING
                                 | TRUE
                                 | FALSE
                                 | IDENTIFIER
                                 | function_call
                                 | LPAREN expression RPAREN'''
            if len(p) == 2:
                if isinstance(p[1], str) and p[1] in ['true', 'false']:
                    p[0] = LiteralNode(p[1] == 'true')
                else:
                    p[0] = LiteralNode(p[1]) if not isinstance(p[1], str) else IdentifierNode(p[1])
            elif len(p) == 4:
                p[0] = p[2]
            else:
                p[0] = p[1]
        
        def p_function_call(p):
            '''function_call : IDENTIFIER LPAREN argument_list RPAREN'''
            p[0] = FunctionCallNode(p[1], p[3])
        
        def p_argument_list(p):
            '''argument_list : argument_list COMMA expression
                            | expression
                            | empty'''
            if len(p) == 2:
                if p[1] is None:
                    p[0] = []
                else:
                    p[0] = [p[1]]
            else:
                p[0] = p[1] + [p[3]]
        
        def p_empty(p):
            '''empty :'''
            p[0] = None
        
        def p_error(p):
            if p:
                print(f"Syntax error at token {p.type} ('{p.value}') at line {p.lineno}")
            else:
                print("Syntax error at EOF")
        
        self.parser = yacc.yacc()
    
    def parse(self, code: str) -> Optional[ProgramNode]:
        """Parse code and return AST"""
        try:
            result = self.parser.parse(code, lexer=self.lexer.lexer)
            return result
        except Exception as e:
            print(f"Parser error: {e}")
            return None
    
    def change_language(self, new_language: str):
        """Change parser language"""
        self.lexer.change_language(new_language)
        self.current_language = new_language
        self.tokens = self.lexer.tokens
        self._build_parser()