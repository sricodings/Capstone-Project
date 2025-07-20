"""
Abstract Syntax Tree Node Definitions
Defines all AST node types for the programming language
"""

from abc import ABC, abstractmethod
from typing import List, Any, Optional

class ASTNode(ABC):
    """Base class for all AST nodes"""
    
    @abstractmethod
    def accept(self, visitor):
        """Accept a visitor for the visitor pattern"""
        pass
    
    @abstractmethod
    def __str__(self):
        """String representation of the node"""
        pass

class ProgramNode(ASTNode):
    """Root node representing the entire program"""
    
    def __init__(self, statements: List[ASTNode]):
        self.statements = [s for s in statements if s is not None]
    
    def accept(self, visitor):
        return visitor.visit_program(self)
    
    def __str__(self):
        return f"Program({len(self.statements)} statements)"

class AssignmentNode(ASTNode):
    """Variable assignment node"""
    
    def __init__(self, identifier: str, expression: ASTNode, is_declaration: bool = False):
        self.identifier = identifier
        self.expression = expression
        self.is_declaration = is_declaration
    
    def accept(self, visitor):
        return visitor.visit_assignment(self)
    
    def __str__(self):
        prefix = "var " if self.is_declaration else ""
        return f"Assignment({prefix}{self.identifier} = {self.expression})"

class IfNode(ASTNode):
    """Conditional if statement node"""
    
    def __init__(self, condition: ASTNode, then_statements: List[ASTNode], 
                 else_statements: Optional[List[ASTNode]] = None):
        self.condition = condition
        self.then_statements = then_statements or []
        self.else_statements = else_statements or []
    
    def accept(self, visitor):
        return visitor.visit_if(self)
    
    def __str__(self):
        return f"If({self.condition}, {len(self.then_statements)} then, {len(self.else_statements)} else)"

class WhileNode(ASTNode):
    """While loop node"""
    
    def __init__(self, condition: ASTNode, statements: List[ASTNode]):
        self.condition = condition
        self.statements = statements or []
    
    def accept(self, visitor):
        return visitor.visit_while(self)
    
    def __str__(self):
        return f"While({self.condition}, {len(self.statements)} statements)"

class ForNode(ASTNode):
    """For loop node"""
    
    def __init__(self, variable: str, start: ASTNode, end: ASTNode, statements: List[ASTNode]):
        self.variable = variable
        self.start = start
        self.end = end
        self.statements = statements or []
    
    def accept(self, visitor):
        return visitor.visit_for(self)
    
    def __str__(self):
        return f"For({self.variable}: {self.start} to {self.end}, {len(self.statements)} statements)"

class FunctionNode(ASTNode):
    """Function definition node"""
    
    def __init__(self, name: str, parameters: List[str], statements: List[ASTNode]):
        self.name = name
        self.parameters = parameters or []
        self.statements = statements or []
    
    def accept(self, visitor):
        return visitor.visit_function(self)
    
    def __str__(self):
        return f"Function({self.name}({', '.join(self.parameters)}), {len(self.statements)} statements)"

class ReturnNode(ASTNode):
    """Return statement node"""
    
    def __init__(self, expression: Optional[ASTNode] = None):
        self.expression = expression
    
    def accept(self, visitor):
        return visitor.visit_return(self)
    
    def __str__(self):
        return f"Return({self.expression if self.expression else 'void'})"

class PrintNode(ASTNode):
    """Print statement node"""
    
    def __init__(self, expression: ASTNode):
        self.expression = expression
    
    def accept(self, visitor):
        return visitor.visit_print(self)
    
    def __str__(self):
        return f"Print({self.expression})"

class ExpressionStatementNode(ASTNode):
    """Expression statement node"""
    
    def __init__(self, expression: ASTNode):
        self.expression = expression
    
    def accept(self, visitor):
        return visitor.visit_expression_statement(self)
    
    def __str__(self):
        return f"ExpressionStatement({self.expression})"

class BinaryOpNode(ASTNode):
    """Binary operation node"""
    
    def __init__(self, left: ASTNode, operator: str, right: ASTNode):
        self.left = left
        self.operator = operator
        self.right = right
    
    def accept(self, visitor):
        return visitor.visit_binary_op(self)
    
    def __str__(self):
        return f"BinaryOp({self.left} {self.operator} {self.right})"

class UnaryOpNode(ASTNode):
    """Unary operation node"""
    
    def __init__(self, operator: str, operand: ASTNode):
        self.operator = operator
        self.operand = operand
    
    def accept(self, visitor):
        return visitor.visit_unary_op(self)
    
    def __str__(self):
        return f"UnaryOp({self.operator}{self.operand})"

class LiteralNode(ASTNode):
    """Literal value node (numbers, strings, booleans)"""
    
    def __init__(self, value: Any):
        self.value = value
    
    def accept(self, visitor):
        return visitor.visit_literal(self)
    
    def __str__(self):
        return f"Literal({self.value})"

class IdentifierNode(ASTNode):
    """Identifier/variable reference node"""
    
    def __init__(self, name: str):
        self.name = name
    
    def accept(self, visitor):
        return visitor.visit_identifier(self)
    
    def __str__(self):
        return f"Identifier({self.name})"

class FunctionCallNode(ASTNode):
    """Function call node"""
    
    def __init__(self, name: str, arguments: List[ASTNode]):
        self.name = name
        self.arguments = arguments or []
    
    def accept(self, visitor):
        return visitor.visit_function_call(self)
    
    def __str__(self):
        return f"FunctionCall({self.name}({', '.join(str(arg) for arg in self.arguments)}))"