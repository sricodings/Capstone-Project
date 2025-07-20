// Abstract Syntax Tree nodes for the multilingual programming language

export abstract class ASTNode {
  abstract accept<T>(visitor: ASTVisitor<T>): T;
}

export interface ASTVisitor<T> {
  visitProgram(node: Program): T;
  visitVarDeclaration(node: VarDeclaration): T;
  visitFunctionDeclaration(node: FunctionDeclaration): T;
  visitIfStatement(node: IfStatement): T;
  visitWhileStatement(node: WhileStatement): T;
  visitForStatement(node: ForStatement): T;
  visitReturnStatement(node: ReturnStatement): T;
  visitExpressionStatement(node: ExpressionStatement): T;
  visitBinaryExpression(node: BinaryExpression): T;
  visitUnaryExpression(node: UnaryExpression): T;
  visitCallExpression(node: CallExpression): T;
  visitIdentifier(node: Identifier): T;
  visitLiteral(node: Literal): T;
  visitAssignmentExpression(node: AssignmentExpression): T;
}

export class Program extends ASTNode {
  constructor(public statements: ASTNode[]) {
    super();
  }

  accept<T>(visitor: ASTVisitor<T>): T {
    return visitor.visitProgram(this);
  }
}

export class VarDeclaration extends ASTNode {
  constructor(public identifier: string, public initializer?: ASTNode) {
    super();
  }

  accept<T>(visitor: ASTVisitor<T>): T {
    return visitor.visitVarDeclaration(this);
  }
}

export class FunctionDeclaration extends ASTNode {
  constructor(
    public name: string,
    public parameters: string[],
    public body: ASTNode[]
  ) {
    super();
  }

  accept<T>(visitor: ASTVisitor<T>): T {
    return visitor.visitFunctionDeclaration(this);
  }
}

export class IfStatement extends ASTNode {
  constructor(
    public condition: ASTNode,
    public thenStatement: ASTNode,
    public elseStatement?: ASTNode
  ) {
    super();
  }

  accept<T>(visitor: ASTVisitor<T>): T {
    return visitor.visitIfStatement(this);
  }
}

export class WhileStatement extends ASTNode {
  constructor(public condition: ASTNode, public body: ASTNode) {
    super();
  }

  accept<T>(visitor: ASTVisitor<T>): T {
    return visitor.visitWhileStatement(this);
  }
}

export class ForStatement extends ASTNode {
  constructor(
    public initializer: ASTNode | null,
    public condition: ASTNode | null,
    public increment: ASTNode | null,
    public body: ASTNode
  ) {
    super();
  }

  accept<T>(visitor: ASTVisitor<T>): T {
    return visitor.visitForStatement(this);
  }
}

export class ReturnStatement extends ASTNode {
  constructor(public value?: ASTNode) {
    super();
  }

  accept<T>(visitor: ASTVisitor<T>): T {
    return visitor.visitReturnStatement(this);
  }
}

export class ExpressionStatement extends ASTNode {
  constructor(public expression: ASTNode) {
    super();
  }

  accept<T>(visitor: ASTVisitor<T>): T {
    return visitor.visitExpressionStatement(this);
  }
}

export class BinaryExpression extends ASTNode {
  constructor(
    public left: ASTNode,
    public operator: string,
    public right: ASTNode
  ) {
    super();
  }

  accept<T>(visitor: ASTVisitor<T>): T {
    return visitor.visitBinaryExpression(this);
  }
}

export class UnaryExpression extends ASTNode {
  constructor(public operator: string, public operand: ASTNode) {
    super();
  }

  accept<T>(visitor: ASTVisitor<T>): T {
    return visitor.visitUnaryExpression(this);
  }
}

export class CallExpression extends ASTNode {
  constructor(public callee: ASTNode, public args: ASTNode[]) {
    super();
  }

  accept<T>(visitor: ASTVisitor<T>): T {
    return visitor.visitCallExpression(this);
  }
}

export class Identifier extends ASTNode {
  constructor(public name: string) {
    super();
  }

  accept<T>(visitor: ASTVisitor<T>): T {
    return visitor.visitIdentifier(this);
  }
}

export class Literal extends ASTNode {
  constructor(public value: any, public type: 'number' | 'string' | 'boolean' | 'null') {
    super();
  }

  accept<T>(visitor: ASTVisitor<T>): T {
    return visitor.visitLiteral(this);
  }
}

export class AssignmentExpression extends ASTNode {
  constructor(public identifier: string, public value: ASTNode) {
    super();
  }

  accept<T>(visitor: ASTVisitor<T>): T {
    return visitor.visitAssignmentExpression(this);
  }
}

export class BlockStatement extends ASTNode {
  constructor(public statements: ASTNode[]) {
    super();
  }

  accept<T>(visitor: ASTVisitor<T>): T {
    // BlockStatement can be treated as a program for visiting purposes
    return visitor.visitProgram(new Program(this.statements));
  }
}