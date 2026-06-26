from ast_nodes import *

class Optimizer:
    def __init__(self):
        pass

    def optimize(self, node):
        if isinstance(node, Program):
            optimized_statements = []
            for stmt in node.statements:
                opt_stmt = self.optimize(stmt)
                if opt_stmt:
                    optimized_statements.append(opt_stmt)
            return Program(optimized_statements)

        elif isinstance(node, FunctionDecl):
            node.body = [self.optimize(stmt) for stmt in node.body if self.optimize(stmt) is not None]
            return node

        elif isinstance(node, Assignment):
            node.value = self.optimize(node.value)
            return node

        elif isinstance(node, IfStatement):
            node.condition = self.optimize(node.condition)
            node.then_branch = [self.optimize(stmt) for stmt in node.then_branch if self.optimize(stmt) is not None]
            if node.else_branch:
                node.else_branch = [self.optimize(stmt) for stmt in node.else_branch if self.optimize(stmt) is not None]
            
            # Constant condition optimization
            if isinstance(node.condition, Boolean):
                if node.condition.value:
                    # Condition is always true, return then_branch (we flatten it slightly by just wrapping in a dummy block or returning statements - to keep it simple, we don't flatten but just keep if)
                    pass 
                else:
                    # Condition is always false, maybe remove then branch
                    pass
            return node

        elif isinstance(node, WhileStatement):
            node.condition = self.optimize(node.condition)
            node.body = [self.optimize(stmt) for stmt in node.body if self.optimize(stmt) is not None]
            return node

        elif isinstance(node, ReturnStatement):
            node.value = self.optimize(node.value)
            return node

        elif isinstance(node, PrintStatement):
            node.value = self.optimize(node.value)
            return node

        elif isinstance(node, InputStatement):
            return node

        elif isinstance(node, BinOp):
            node.left = self.optimize(node.left)
            node.right = self.optimize(node.right)
            
            # Constant Folding
            if isinstance(node.left, Number) and isinstance(node.right, Number):
                if node.op == '+':
                    return Number(node.left.value + node.right.value)
                elif node.op == '-':
                    return Number(node.left.value - node.right.value)
                elif node.op == '*':
                    return Number(node.left.value * node.right.value)
                elif node.op == '/':
                    if node.right.value != 0:
                        return Number(node.left.value / node.right.value)
                elif node.op == '==':
                    return Boolean(node.left.value == node.right.value)
                elif node.op == '!=':
                    return Boolean(node.left.value != node.right.value)
                elif node.op == '<':
                    return Boolean(node.left.value < node.right.value)
                elif node.op == '>':
                    return Boolean(node.left.value > node.right.value)
                elif node.op == '<=':
                    return Boolean(node.left.value <= node.right.value)
                elif node.op == '>=':
                    return Boolean(node.left.value >= node.right.value)
            
            return node

        elif isinstance(node, FunctionCall):
            node.args = [self.optimize(arg) for arg in node.args]
            return node

        elif isinstance(node, (Number, String, Boolean, Identifier)):
            return node
            
        return node

if __name__ == '__main__':
    print("Optimizer ready.")
