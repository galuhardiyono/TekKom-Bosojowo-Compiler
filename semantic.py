import sys
from ast_nodes import *

class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = [{}] # Stack of scopes, starting with global scope
        self.functions = {} # name -> FunctionDecl

    def enter_scope(self):
        self.symbol_table.append({})

    def leave_scope(self):
        self.symbol_table.pop()

    def declare_var(self, name):
        self.symbol_table[-1][name] = True

    def is_var_declared(self, name):
        for scope in reversed(self.symbol_table):
            if name in scope:
                return True
        return False

    def analyze(self, node):
        if isinstance(node, Program):
            for stmt in node.statements:
                # Pre-declare functions
                if isinstance(stmt, FunctionDecl):
                    if stmt.name in self.functions:
                        print(f"Semantic error: Function '{stmt.name}' is already defined.")
                        sys.exit(1)
                    self.functions[stmt.name] = stmt
            
            for stmt in node.statements:
                self.analyze(stmt)

        elif isinstance(node, FunctionDecl):
            self.enter_scope()
            for param in node.params:
                self.declare_var(param)
            for stmt in node.body:
                self.analyze(stmt)
            self.leave_scope()

        elif isinstance(node, Assignment):
            self.analyze(node.value)
            self.declare_var(node.name)

        elif isinstance(node, IfStatement):
            self.analyze(node.condition)
            self.enter_scope()
            for stmt in node.then_branch:
                self.analyze(stmt)
            self.leave_scope()
            
            if node.else_branch is not None:
                self.enter_scope()
                for stmt in node.else_branch:
                    self.analyze(stmt)
                self.leave_scope()

        elif isinstance(node, WhileStatement):
            self.analyze(node.condition)
            self.enter_scope()
            for stmt in node.body:
                self.analyze(stmt)
            self.leave_scope()

        elif isinstance(node, ReturnStatement):
            self.analyze(node.value)

        elif isinstance(node, PrintStatement):
            self.analyze(node.value)

        elif isinstance(node, InputStatement):
            pass

        elif isinstance(node, BinOp):
            self.analyze(node.left)
            self.analyze(node.right)

        elif isinstance(node, FunctionCall):
            if node.name in ['mlebu', 'mlebu_angka']:
                for arg in node.args:
                    self.analyze(arg)
                return

            if node.name not in self.functions:
                print(f"Semantic error: Function '{node.name}' is not defined.")
                sys.exit(1)
            
            func_decl = self.functions[node.name]
            if len(node.args) != len(func_decl.params):
                print(f"Semantic error: Function '{node.name}' expects {len(func_decl.params)} arguments, but got {len(node.args)}.")
                sys.exit(1)
                
            for arg in node.args:
                self.analyze(arg)

        elif isinstance(node, Identifier):
            if not self.is_var_declared(node.name):
                print(f"Semantic error: Variable '{node.name}' is not defined.")
                sys.exit(1)

        elif isinstance(node, (Number, String, Boolean)):
            pass
        else:
            print(f"Unknown node: {type(node)}")
            sys.exit(1)

if __name__ == '__main__':
    print("Semantic analyzer ready.")
