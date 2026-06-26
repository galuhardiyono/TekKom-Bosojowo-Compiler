from ast_nodes import *

class CodeGenerator:
    def __init__(self):
        self.code = []
        self.indent_level = 0

    def get_code(self):
        return "\n".join(self.code)

    def add_line(self, line):
        indentation = "    " * self.indent_level
        self.code.append(indentation + line)

    def generate(self, node):
        if isinstance(node, Program):
            self.add_line("def mlebu(prompt=''): return input(prompt)")
            self.add_line("def mlebu_angka(prompt=''):")
            self.add_line("    try:")
            self.add_line("        return float(input(prompt))")
            self.add_line("    except ValueError:")
            self.add_line("        return 0.0")
            self.add_line("")
            for stmt in node.statements:
                self.generate(stmt)

        elif isinstance(node, FunctionDecl):
            params_str = ", ".join(node.params)
            self.add_line(f"def {node.name}({params_str}):")
            self.indent_level += 1
            if not node.body:
                self.add_line("pass")
            else:
                for stmt in node.body:
                    self.generate(stmt)
            self.indent_level -= 1
            self.add_line("") # Empty line after function

        elif isinstance(node, Assignment):
            val_str = self.visit_expr(node.value)
            self.add_line(f"{node.name} = {val_str}")

        elif isinstance(node, IfStatement):
            cond_str = self.visit_expr(node.condition)
            self.add_line(f"if {cond_str}:")
            self.indent_level += 1
            if not node.then_branch:
                self.add_line("pass")
            else:
                for stmt in node.then_branch:
                    self.generate(stmt)
            self.indent_level -= 1
            
            if node.else_branch is not None:
                self.add_line("else:")
                self.indent_level += 1
                if not node.else_branch:
                    self.add_line("pass")
                else:
                    for stmt in node.else_branch:
                        self.generate(stmt)
                self.indent_level -= 1

        elif isinstance(node, WhileStatement):
            cond_str = self.visit_expr(node.condition)
            self.add_line(f"while {cond_str}:")
            self.indent_level += 1
            if not node.body:
                self.add_line("pass")
            else:
                for stmt in node.body:
                    self.generate(stmt)
            self.indent_level -= 1

        elif isinstance(node, ReturnStatement):
            val_str = self.visit_expr(node.value)
            self.add_line(f"return {val_str}")

        elif isinstance(node, PrintStatement):
            val_str = self.visit_expr(node.value)
            self.add_line(f"print({val_str})")



        elif isinstance(node, FunctionCall):
            args_str = ", ".join(self.visit_expr(arg) for arg in node.args)
            self.add_line(f"{node.name}({args_str})")
            
        else:
            raise Exception(f"Unknown statement node: {type(node)}")

    def visit_expr(self, node):
        if isinstance(node, BinOp):
            left = self.visit_expr(node.left)
            right = self.visit_expr(node.right)
            op = node.op
            if op == 'lan': op = 'and'
            if op == 'utawa': op = 'or'
            return f"({left} {op} {right})"
            
        elif isinstance(node, FunctionCall):
            args_str = ", ".join(self.visit_expr(arg) for arg in node.args)
            return f"{node.name}({args_str})"
            
        elif isinstance(node, Identifier):
            return node.name
            
        elif isinstance(node, Number):
            return str(node.value)
            
        elif isinstance(node, String):
            return f'"{node.value}"'
            
        elif isinstance(node, Boolean):
            return "True" if node.value else "False"
            
        else:
            raise Exception(f"Unknown expression node: {type(node)}")

if __name__ == '__main__':
    print("Code Generator ready.")
