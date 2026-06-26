class ASTNode:
    pass

class Program(ASTNode):
    def __init__(self, statements):
        self.statements = statements

class FunctionDecl(ASTNode):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

class Assignment(ASTNode):
    def __init__(self, name, value):
        self.name = name
        self.value = value

class IfStatement(ASTNode):
    def __init__(self, condition, then_branch, else_branch=None):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

class WhileStatement(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class ReturnStatement(ASTNode):
    def __init__(self, value):
        self.value = value

class PrintStatement(ASTNode):
    def __init__(self, value):
        self.value = value

class InputStatement(ASTNode):
    def __init__(self, prompt=""):
        self.prompt = prompt

class Expression(ASTNode):
    pass

class BinOp(Expression):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class UnOp(Expression):
    def __init__(self, op, operand):
        self.op = op
        self.operand = operand

class FunctionCall(Expression):
    def __init__(self, name, args):
        self.name = name
        self.args = args

class Number(Expression):
    def __init__(self, value):
        self.value = value

class String(Expression):
    def __init__(self, value):
        self.value = value

class Boolean(Expression):
    def __init__(self, value):
        self.value = value

class Identifier(Expression):
    def __init__(self, name):
        self.name = name
