"""
Virtual Machine for Multilingual Programming Language
Executes bytecode with WORA capabilities
"""

from typing import List, Dict, Any, Optional
from .bytecode_generator import BytecodeInstruction

class VMError(Exception):
    """Virtual machine execution error"""
    pass

class VirtualMachine:
    """Stack-based virtual machine for bytecode execution"""
    
    def __init__(self):
        self.stack = []
        self.variables = {}
        self.call_stack = []
        self.pc = 0  # Program counter
        self.instructions = []
        self.constants = []
        self.output = []
        self.input_buffer = []
        self.halted = False
    
    def load_bytecode(self, instructions: List[BytecodeInstruction], constants: List[Any]):
        """Load bytecode and constants into VM"""
        self.instructions = instructions
        self.constants = constants
        self.reset()
    
    def reset(self):
        """Reset VM state"""
        self.stack = []
        self.variables = {}
        self.call_stack = []
        self.pc = 0
        self.output = []
        self.halted = False
    
    def push(self, value: Any):
        """Push value onto stack"""
        self.stack.append(value)
    
    def pop(self) -> Any:
        """Pop value from stack"""
        if not self.stack:
            raise VMError("Stack underflow")
        return self.stack.pop()
    
    def peek(self) -> Any:
        """Peek at top of stack without popping"""
        if not self.stack:
            raise VMError("Stack is empty")
        return self.stack[-1]
    
    def set_input(self, input_lines: List[str]):
        """Set input buffer for input operations"""
        self.input_buffer = input_lines.copy()
    
    def get_output(self) -> List[str]:
        """Get accumulated output"""
        return self.output.copy()
    
    def execute(self, max_instructions: int = 10000) -> bool:
        """Execute bytecode"""
        instruction_count = 0
        
        while not self.halted and self.pc < len(self.instructions) and instruction_count < max_instructions:
            instruction = self.instructions[self.pc]
            self.execute_instruction(instruction)
            instruction_count += 1
        
        if instruction_count >= max_instructions:
            raise VMError("Execution limit exceeded - possible infinite loop")
        
        return self.halted
    
    def execute_instruction(self, instruction: BytecodeInstruction):
        """Execute a single instruction"""
        opcode = instruction.opcode
        arg = instruction.arg
        
        if opcode == 'LOAD_CONST':
            self.push(self.constants[arg])
        
        elif opcode == 'LOAD_VAR':
            if arg in self.variables:
                self.push(self.variables[arg])
            else:
                raise VMError(f"Undefined variable at index {arg}")
        
        elif opcode == 'STORE_VAR':
            value = self.pop()
            self.variables[arg] = value
        
        elif opcode == 'BINARY_OP':
            right = self.pop()
            left = self.pop()
            result = self.apply_binary_op(left, arg, right)
            self.push(result)
        
        elif opcode == 'UNARY_OP':
            operand = self.pop()
            result = self.apply_unary_op(arg, operand)
            self.push(result)
        
        elif opcode == 'JUMP':
            self.pc = arg
            return
        
        elif opcode == 'JUMP_IF_FALSE':
            condition = self.pop()
            if not self.is_truthy(condition):
                self.pc = arg
                return
        
        elif opcode == 'JUMP_IF_TRUE':
            condition = self.pop()
            if self.is_truthy(condition):
                self.pc = arg
                return
        
        elif opcode == 'PRINT':
            value = self.pop()
            self.output.append(str(value))
        
        elif opcode == 'INPUT':
            if self.input_buffer:
                value = self.input_buffer.pop(0)
                self.push(value)
            else:
                self.push("")  # Empty input
        
        elif opcode == 'POP':
            self.pop()
        
        elif opcode == 'HALT':
            self.halted = True
            return
        
        elif opcode == 'FUNCTION_START':
            # Function prologue - arg is parameter count
            pass
        
        elif opcode == 'RETURN':
            if self.call_stack:
                return_value = self.pop()
                return_address = self.call_stack.pop()
                self.pc = return_address
                self.push(return_value)
                return
            else:
                self.halted = True
                return
        
        elif opcode == 'CALL':
            # Save return address
            self.call_stack.append(self.pc + 1)
            self.pc = arg
            return
        
        elif opcode == 'CALL_BUILTIN':
            self.call_builtin(arg)
        
        else:
            raise VMError(f"Unknown opcode: {opcode}")
        
        self.pc += 1
    
    def apply_binary_op(self, left: Any, op: str, right: Any) -> Any:
        """Apply binary operation"""
        try:
            if op == '+':
                return left + right
            elif op == '-':
                return left - right
            elif op == '*':
                return left * right
            elif op == '/':
                if right == 0:
                    raise VMError("Division by zero")
                return left / right
            elif op == '%':
                return left % right
            elif op == '==':
                return left == right
            elif op == '!=':
                return left != right
            elif op == '<':
                return left < right
            elif op == '<=':
                return left <= right
            elif op == '>':
                return left > right
            elif op == '>=':
                return left >= right
            elif op == 'and':
                return self.is_truthy(left) and self.is_truthy(right)
            elif op == 'or':
                return self.is_truthy(left) or self.is_truthy(right)
            else:
                raise VMError(f"Unknown binary operator: {op}")
        except Exception as e:
            raise VMError(f"Error in binary operation {left} {op} {right}: {e}")
    
    def apply_unary_op(self, op: str, operand: Any) -> Any:
        """Apply unary operation"""
        try:
            if op == '-':
                return -operand
            elif op == 'not':
                return not self.is_truthy(operand)
            else:
                raise VMError(f"Unknown unary operator: {op}")
        except Exception as e:
            raise VMError(f"Error in unary operation {op} {operand}: {e}")
    
    def is_truthy(self, value: Any) -> bool:
        """Determine if value is truthy"""
        if value is None or value is False:
            return False
        if isinstance(value, (int, float)) and value == 0:
            return False
        if isinstance(value, str) and value == "":
            return False
        return True
    
    def call_builtin(self, name: str):
        """Call built-in function"""
        if name == 'input':
            if self.input_buffer:
                value = self.input_buffer.pop(0)
                self.push(value)
            else:
                self.push("")
        elif name == 'len':
            arg = self.pop()
            self.push(len(arg))
        elif name == 'str':
            arg = self.pop()
            self.push(str(arg))
        elif name == 'int':
            arg = self.pop()
            try:
                self.push(int(arg))
            except ValueError:
                self.push(0)
        elif name == 'float':
            arg = self.pop()
            try:
                self.push(float(arg))
            except ValueError:
                self.push(0.0)
        else:
            raise VMError(f"Unknown built-in function: {name}")
    
    def get_stack_trace(self) -> str:
        """Get current stack trace for debugging"""
        lines = []
        lines.append(f"PC: {self.pc}")
        lines.append(f"Stack: {self.stack}")
        lines.append(f"Variables: {self.variables}")
        lines.append(f"Call Stack: {self.call_stack}")
        if self.pc < len(self.instructions):
            lines.append(f"Current Instruction: {self.instructions[self.pc]}")
        return "\n".join(lines)