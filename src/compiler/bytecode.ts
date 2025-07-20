// Bytecode generation and virtual machine for the multilingual programming language
import * as AST from './ast';

export enum OpCode {
  // Stack operations
  LOAD_CONST = 'LOAD_CONST',
  LOAD_VAR = 'LOAD_VAR',
  STORE_VAR = 'STORE_VAR',
  
  // Arithmetic operations
  ADD = 'ADD',
  SUBTRACT = 'SUBTRACT',
  MULTIPLY = 'MULTIPLY',
  DIVIDE = 'DIVIDE',
  MODULO = 'MODULO',
  NEGATE = 'NEGATE',
  
  // Comparison operations
  EQUAL = 'EQUAL',
  NOT_EQUAL = 'NOT_EQUAL',
  LESS_THAN = 'LESS_THAN',
  GREATER_THAN = 'GREATER_THAN',
  LESS_EQUAL = 'LESS_EQUAL',
  GREATER_EQUAL = 'GREATER_EQUAL',
  
  // Logical operations
  AND = 'AND',
  OR = 'OR',
  NOT = 'NOT',
  
  // Control flow
  JUMP = 'JUMP',
  JUMP_IF_FALSE = 'JUMP_IF_FALSE',
  JUMP_IF_TRUE = 'JUMP_IF_TRUE',
  
  // Function operations
  CALL = 'CALL',
  RETURN = 'RETURN',
  
  // Built-in functions
  PRINT = 'PRINT',
  INPUT = 'INPUT',
  
  // Special
  POP = 'POP',
  HALT = 'HALT'
}

export interface Instruction {
  opcode: OpCode;
  operand?: any;
  line?: number;
}

export class BytecodeGenerator implements AST.ASTVisitor<void> {
  private instructions: Instruction[] = [];
  private constants: any[] = [];
  private variables: Map<string, number> = new Map();
  private functions: Map<string, { address: number; arity: number }> = new Map();
  private currentLine: number = 1;

  public generate(program: AST.Program): { instructions: Instruction[]; constants: any[] } {
    this.visitProgram(program);
    this.emit(OpCode.HALT);
    return {
      instructions: this.instructions,
      constants: this.constants
    };
  }

  private emit(opcode: OpCode, operand?: any): void {
    this.instructions.push({
      opcode,
      operand,
      line: this.currentLine
    });
  }

  private addConstant(value: any): number {
    const index = this.constants.indexOf(value);
    if (index !== -1) return index;
    
    this.constants.push(value);
    return this.constants.length - 1;
  }

  visitProgram(node: AST.Program): void {
    for (const statement of node.statements) {
      statement.accept(this);
    }
  }

  visitVarDeclaration(node: AST.VarDeclaration): void {
    if (node.initializer) {
      node.initializer.accept(this);
    } else {
      this.emit(OpCode.LOAD_CONST, this.addConstant(null));
    }
    
    const varIndex = this.variables.size;
    this.variables.set(node.identifier, varIndex);
    this.emit(OpCode.STORE_VAR, varIndex);
  }

  visitFunctionDeclaration(node: AST.FunctionDeclaration): void {
    const functionAddress = this.instructions.length;
    this.functions.set(node.name, {
      address: functionAddress,
      arity: node.parameters.length
    });
    
    // Store parameters as local variables
    for (let i = node.parameters.length - 1; i >= 0; i--) {
      const paramIndex = this.variables.size;
      this.variables.set(node.parameters[i], paramIndex);
      this.emit(OpCode.STORE_VAR, paramIndex);
    }
    
    // Generate function body
    for (const statement of node.body) {
      statement.accept(this);
    }
    
    // Implicit return null if no explicit return
    this.emit(OpCode.LOAD_CONST, this.addConstant(null));
    this.emit(OpCode.RETURN);
  }

  visitIfStatement(node: AST.IfStatement): void {
    node.condition.accept(this);
    
    const jumpIfFalse = this.instructions.length;
    this.emit(OpCode.JUMP_IF_FALSE, 0); // Placeholder
    
    node.thenStatement.accept(this);
    
    if (node.elseStatement) {
      const jump = this.instructions.length;
      this.emit(OpCode.JUMP, 0); // Placeholder
      
      // Patch the jump if false
      this.instructions[jumpIfFalse].operand = this.instructions.length;
      
      node.elseStatement.accept(this);
      
      // Patch the jump
      this.instructions[jump].operand = this.instructions.length;
    } else {
      // Patch the jump if false
      this.instructions[jumpIfFalse].operand = this.instructions.length;
    }
  }

  visitWhileStatement(node: AST.WhileStatement): void {
    const loopStart = this.instructions.length;
    
    node.condition.accept(this);
    
    const jumpIfFalse = this.instructions.length;
    this.emit(OpCode.JUMP_IF_FALSE, 0); // Placeholder
    
    node.body.accept(this);
    
    this.emit(OpCode.JUMP, loopStart);
    
    // Patch the jump if false
    this.instructions[jumpIfFalse].operand = this.instructions.length;
  }

  visitForStatement(node: AST.ForStatement): void {
    // Initializer
    if (node.initializer) {
      node.initializer.accept(this);
      if (node.initializer instanceof AST.ExpressionStatement) {
        this.emit(OpCode.POP); // Pop the result if it's an expression
      }
    }
    
    const loopStart = this.instructions.length;
    
    // Condition
    if (node.condition) {
      node.condition.accept(this);
    } else {
      this.emit(OpCode.LOAD_CONST, this.addConstant(true));
    }
    
    const jumpIfFalse = this.instructions.length;
    this.emit(OpCode.JUMP_IF_FALSE, 0); // Placeholder
    
    // Body
    node.body.accept(this);
    
    // Increment
    if (node.increment) {
      node.increment.accept(this);
      this.emit(OpCode.POP); // Pop the result
    }
    
    this.emit(OpCode.JUMP, loopStart);
    
    // Patch the jump if false
    this.instructions[jumpIfFalse].operand = this.instructions.length;
  }

  visitReturnStatement(node: AST.ReturnStatement): void {
    if (node.value) {
      node.value.accept(this);
    } else {
      this.emit(OpCode.LOAD_CONST, this.addConstant(null));
    }
    this.emit(OpCode.RETURN);
  }

  visitExpressionStatement(node: AST.ExpressionStatement): void {
    node.expression.accept(this);
    this.emit(OpCode.POP); // Pop the result since it's not used
  }

  visitBinaryExpression(node: AST.BinaryExpression): void {
    node.left.accept(this);
    node.right.accept(this);
    
    switch (node.operator) {
      case '+': this.emit(OpCode.ADD); break;
      case '-': this.emit(OpCode.SUBTRACT); break;
      case '*': this.emit(OpCode.MULTIPLY); break;
      case '/': this.emit(OpCode.DIVIDE); break;
      case '%': this.emit(OpCode.MODULO); break;
      case '==': this.emit(OpCode.EQUAL); break;
      case '!=': this.emit(OpCode.NOT_EQUAL); break;
      case '<': this.emit(OpCode.LESS_THAN); break;
      case '>': this.emit(OpCode.GREATER_THAN); break;
      case '<=': this.emit(OpCode.LESS_EQUAL); break;
      case '>=': this.emit(OpCode.GREATER_EQUAL); break;
      case '&&': this.emit(OpCode.AND); break;
      case '||': this.emit(OpCode.OR); break;
    }
  }

  visitUnaryExpression(node: AST.UnaryExpression): void {
    node.operand.accept(this);
    
    switch (node.operator) {
      case '-': this.emit(OpCode.NEGATE); break;
      case '!': this.emit(OpCode.NOT); break;
    }
  }

  visitCallExpression(node: AST.CallExpression): void {
    // Handle built-in functions
    if (node.callee instanceof AST.Identifier) {
      if (node.callee.name === 'print' || node.callee.name === 'achchidu') {
        for (const arg of node.args) {
          arg.accept(this);
        }
        this.emit(OpCode.PRINT, node.args.length);
        return;
      }
      
      if (node.callee.name === 'input' || node.callee.name === 'ulle') {
        this.emit(OpCode.INPUT);
        return;
      }
    }
    
    // Regular function call
    for (const arg of node.args) {
      arg.accept(this);
    }
    
    node.callee.accept(this);
    this.emit(OpCode.CALL, node.args.length);
  }

  visitIdentifier(node: AST.Identifier): void {
    const varIndex = this.variables.get(node.name);
    if (varIndex !== undefined) {
      this.emit(OpCode.LOAD_VAR, varIndex);
    } else {
      // Check if it's a function
      const func = this.functions.get(node.name);
      if (func) {
        this.emit(OpCode.LOAD_CONST, this.addConstant(func.address));
      } else {
        throw new Error(`Undefined variable: ${node.name}`);
      }
    }
  }

  visitLiteral(node: AST.Literal): void {
    const constIndex = this.addConstant(node.value);
    this.emit(OpCode.LOAD_CONST, constIndex);
  }

  visitAssignmentExpression(node: AST.AssignmentExpression): void {
    node.value.accept(this);
    
    let varIndex = this.variables.get(node.identifier);
    if (varIndex === undefined) {
      varIndex = this.variables.size;
      this.variables.set(node.identifier, varIndex);
    }
    
    this.emit(OpCode.STORE_VAR, varIndex);
  }
}

export class VirtualMachine {
  private stack: any[] = [];
  private variables: any[] = [];
  private callStack: { returnAddress: number; frameStart: number }[] = [];
  private pc: number = 0; // Program counter
  private instructions: Instruction[] = [];
  private constants: any[] = [];
  private output: string[] = [];

  public execute(bytecode: { instructions: Instruction[]; constants: any[] }): { output: string[]; error?: string } {
    this.instructions = bytecode.instructions;
    this.constants = bytecode.constants;
    this.pc = 0;
    this.stack = [];
    this.variables = [];
    this.callStack = [];
    this.output = [];

    try {
      while (this.pc < this.instructions.length) {
        const instruction = this.instructions[this.pc];
        this.executeInstruction(instruction);
        this.pc++;
      }
      
      return { output: this.output };
    } catch (error) {
      return { 
        output: this.output, 
        error: error instanceof Error ? error.message : String(error) 
      };
    }
  }

  private executeInstruction(instruction: Instruction): void {
    switch (instruction.opcode) {
      case OpCode.LOAD_CONST:
        this.stack.push(this.constants[instruction.operand]);
        break;
        
      case OpCode.LOAD_VAR:
        if (instruction.operand >= this.variables.length) {
          throw new Error(`Undefined variable at index ${instruction.operand}`);
        }
        this.stack.push(this.variables[instruction.operand]);
        break;
        
      case OpCode.STORE_VAR:
        const value = this.stack.pop();
        while (this.variables.length <= instruction.operand) {
          this.variables.push(null);
        }
        this.variables[instruction.operand] = value;
        this.stack.push(value); // Keep value on stack for chaining
        break;
        
      case OpCode.ADD:
        const b = this.stack.pop();
        const a = this.stack.pop();
        this.stack.push(a + b);
        break;
        
      case OpCode.SUBTRACT:
        const sub_b = this.stack.pop();
        const sub_a = this.stack.pop();
        this.stack.push(sub_a - sub_b);
        break;
        
      case OpCode.MULTIPLY:
        const mul_b = this.stack.pop();
        const mul_a = this.stack.pop();
        this.stack.push(mul_a * mul_b);
        break;
        
      case OpCode.DIVIDE:
        const div_b = this.stack.pop();
        const div_a = this.stack.pop();
        if (div_b === 0) throw new Error("Division by zero");
        this.stack.push(div_a / div_b);
        break;
        
      case OpCode.MODULO:
        const mod_b = this.stack.pop();
        const mod_a = this.stack.pop();
        this.stack.push(mod_a % mod_b);
        break;
        
      case OpCode.NEGATE:
        this.stack.push(-this.stack.pop());
        break;
        
      case OpCode.EQUAL:
        const eq_b = this.stack.pop();
        const eq_a = this.stack.pop();
        this.stack.push(eq_a === eq_b);
        break;
        
      case OpCode.NOT_EQUAL:
        const neq_b = this.stack.pop();
        const neq_a = this.stack.pop();
        this.stack.push(neq_a !== neq_b);
        break;
        
      case OpCode.LESS_THAN:
        const lt_b = this.stack.pop();
        const lt_a = this.stack.pop();
        this.stack.push(lt_a < lt_b);
        break;
        
      case OpCode.GREATER_THAN:
        const gt_b = this.stack.pop();
        const gt_a = this.stack.pop();
        this.stack.push(gt_a > gt_b);
        break;
        
      case OpCode.LESS_EQUAL:
        const le_b = this.stack.pop();
        const le_a = this.stack.pop();
        this.stack.push(le_a <= le_b);
        break;
        
      case OpCode.GREATER_EQUAL:
        const ge_b = this.stack.pop();
        const ge_a = this.stack.pop();
        this.stack.push(ge_a >= ge_b);
        break;
        
      case OpCode.AND:
        const and_b = this.stack.pop();
        const and_a = this.stack.pop();
        this.stack.push(and_a && and_b);
        break;
        
      case OpCode.OR:
        const or_b = this.stack.pop();
        const or_a = this.stack.pop();
        this.stack.push(or_a || or_b);
        break;
        
      case OpCode.NOT:
        this.stack.push(!this.stack.pop());
        break;
        
      case OpCode.JUMP:
        this.pc = instruction.operand - 1; // -1 because pc will be incremented
        break;
        
      case OpCode.JUMP_IF_FALSE:
        if (!this.stack.pop()) {
          this.pc = instruction.operand - 1;
        }
        break;
        
      case OpCode.JUMP_IF_TRUE:
        if (this.stack.pop()) {
          this.pc = instruction.operand - 1;
        }
        break;
        
      case OpCode.PRINT:
        const argCount = instruction.operand || 1;
        const args = [];
        for (let i = 0; i < argCount; i++) {
          args.unshift(this.stack.pop());
        }
        this.output.push(args.map(arg => String(arg)).join(' '));
        break;
        
      case OpCode.INPUT:
        // For web environment, we'll simulate input
        const input = prompt("Enter input:") || "";
        this.stack.push(input);
        break;
        
      case OpCode.POP:
        this.stack.pop();
        break;
        
      case OpCode.HALT:
        return;
        
      default:
        throw new Error(`Unknown opcode: ${instruction.opcode}`);
    }
  }
}