"""
Bytecode Generator for Multilingual Programming Language
Generates intermediate bytecode for WORA execution
"""

from typing import List, Dict, Any, Optional
from .ast_nodes import *

class BytecodeInstruction:
    """Represents a single bytecode instruction"""
    
    def __init__(self, opcode: str, arg: Any = None, line: int = 0):
        self.opcode = opcode
        self.arg = arg
        self.line = line
    
    def __str__(self):
        if self.arg is not None:
            return f"{self.opcode} {self.arg}"
        return self.opcode
    
    def __repr__(self):
        return self.__str__()

class BytecodeGenerator:
    """Generates bytecode from AST using visitor pattern"""
    
    def __init__(self):
        self.instructions = []
        self.constants = []
        self.variables = {}
        self.functions = {}
        self.current_line = 1
    
    def generate(self, ast: ProgramNode) -> List[BytecodeInstruction]:
        """Generate bytecode from AST"""
        self.instructions = []
        self.constants = []
        self.variables = {}
        self.functions = {}
        
        ast.accept(self)
        return self.instructions
    
    def add_instruction(self, opcode: str, arg: Any = None):
        """Add instruction to bytecode"""
        instruction = BytecodeInstruction(opcode, arg, self.current_line)
        self.instructions.append(instruction)
        return len(self.instructions) - 1
    
    def add_constant(self, value: Any) -> int:
        """Add constant and return its index"""
        if value not in self.constants:
            self.constants.append(value)
        return self.constants.index(value)
    
    def visit_program(self, node: ProgramNode):
        """Visit program node"""
        for statement in node.statements:
            if statement:
                statement.accept(self)
        self.add_instruction('HALT')
    
    def visit_assignment(self, node: AssignmentNode):
        """Visit assignment node"""
        # Evaluate expression
        node.expression.accept(self)
        
        # Store in variable
        if node.is_declaration:
            var_index = len(self.variables)
            self.variables[node.identifier] = var_index
            self.add_instruction('STORE_VAR', var_index)
        else:
            if node.identifier in self.variables:
                var_index = self.variables[node.identifier]
                self.add_instruction('STORE_VAR', var_index)
            else:
                raise NameError(f"Variable '{node.identifier}' not defined")
    
    def visit_if(self, node: IfNode):
        """Visit if node"""
        # Evaluate condition
        node.condition.accept(self)
        
        # Jump if false
        else_label = self.add_instruction('JUMP_IF_FALSE', None)
        
        # Then block
        for statement in node.then_statements:
            if statement:
                statement.accept(self)
        
        if node.else_statements:
            # Jump over else block
            end_label = self.add_instruction('JUMP', None)
            
            # Update else label
            self.instructions[else_label].arg = len(self.instructions)
            
            # Else block
            for statement in node.else_statements:
                if statement:
                    statement.accept(self)
            
            # Update end label
            self.instructions[end_label].arg = len(self.instructions)
        else:
            # Update else label to point to end
            self.instructions[else_label].arg = len(self.instructions)
    
    def visit_while(self, node: WhileNode):
        """Visit while node"""
        # Loop start
        loop_start = len(self.instructions)
        
        # Evaluate condition
        node.condition.accept(self)
        
        # Jump if false (exit loop)
        exit_label = self.add_instruction('JUMP_IF_FALSE', None)
        
        # Loop body
        for statement in node.statements:
            if statement:
                statement.accept(self)
        
        # Jump back to start
        self.add_instruction('JUMP', loop_start)
        
        # Update exit label
        self.instructions[exit_label].arg = len(self.instructions)
    
    def visit_for(self, node: ForNode):
        """Visit for node"""
        # Initialize loop variable
        node.start.accept(self)
        var_index = len(self.variables)
        self.variables[node.variable] = var_index
        self.add_instruction('STORE_VAR', var_index)
        
        # Loop start
        loop_start = len(self.instructions)
        
        # Load loop variable and end value
        self.add_instruction('LOAD_VAR', var_index)
        node.end.accept(self)
        
        # Compare (variable <= end)
        self.add_instruction('BINARY_OP', '<=')
        
        # Jump if false (exit loop)
        exit_label = self.add_instruction('JUMP_IF_FALSE', None)
        
        # Loop body
        for statement in node.statements:
            if statement:
                statement.accept(self)
        
        # Increment loop variable
        self.add_instruction('LOAD_VAR', var_index)
        self.add_instruction('LOAD_CONST', self.add_constant(1))
        self.add_instruction('BINARY_OP', '+')
        self.add_instruction('STORE_VAR', var_index)
        
        # Jump back to start
        self.add_instruction('JUMP', loop_start)
        
        # Update exit label
        self.instructions[exit_label].arg = len(self.instructions)
    
    def visit_function(self, node: FunctionNode):
        """Visit function node"""
        # Store function start address
        self.functions[node.name] = len(self.instructions)
        
        # Function prologue
        self.add_instruction('FUNCTION_START', len(node.parameters))
        
        # Function body
        for statement in node.statements:
            if statement:
                statement.accept(self)
        
        # Default return if no explicit return
        self.add_instruction('LOAD_CONST', self.add_constant(None))
        self.add_instruction('RETURN')
    
    def visit_return(self, node: ReturnNode):
        """Visit return node"""
        if node.expression:
            node.expression.accept(self)
        else:
            self.add_instruction('LOAD_CONST', self.add_constant(None))
        self.add_instruction('RETURN')
    
    def visit_print(self, node: PrintNode):
        """Visit print node"""
        node.expression.accept(self)
        self.add_instruction('PRINT')
    
    def visit_expression_statement(self, node: ExpressionStatementNode):
        """Visit expression statement node"""
        node.expression.accept(self)
        self.add_instruction('POP')  # Discard result
    
    def visit_binary_op(self, node: BinaryOpNode):
        """Visit binary operation node"""
        node.left.accept(self)
        node.right.accept(self)
        self.add_instruction('BINARY_OP', node.operator)
    
    def visit_unary_op(self, node: UnaryOpNode):
        """Visit unary operation node"""
        node.operand.accept(self)
        self.add_instruction('UNARY_OP', node.operator)
    
    def visit_literal(self, node: LiteralNode):
        """Visit literal node"""
        const_index = self.add_constant(node.value)
        self.add_instruction('LOAD_CONST', const_index)
    
    def visit_identifier(self, node: IdentifierNode):
        """Visit identifier node"""
        if node.name in self.variables:
            var_index = self.variables[node.name]
            self.add_instruction('LOAD_VAR', var_index)
        else:
            raise NameError(f"Variable '{node.name}' not defined")
    
    def visit_function_call(self, node: FunctionCallNode):
        """Visit function call node"""
        # Push arguments
        for arg in node.arguments:
            arg.accept(self)
        
        # Call function
        if node.name in self.functions:
            func_addr = self.functions[node.name]
            self.add_instruction('CALL', func_addr)
        else:
            # Built-in function
            self.add_instruction('CALL_BUILTIN', node.name)
    
    def get_bytecode_listing(self) -> str:
        """Get human-readable bytecode listing"""
        lines = []
        lines.append("=== CONSTANTS ===")
        for i, const in enumerate(self.constants):
            lines.append(f"{i}: {repr(const)}")
        
        lines.append("\n=== VARIABLES ===")
        for name, index in self.variables.items():
            lines.append(f"{index}: {name}")
        
        lines.append("\n=== FUNCTIONS ===")
        for name, addr in self.functions.items():
            lines.append(f"{name}: {addr}")
        
        lines.append("\n=== BYTECODE ===")
        for i, instruction in enumerate(self.instructions):
            lines.append(f"{i:3d}: {instruction}")
        
        return "\n".join(lines)