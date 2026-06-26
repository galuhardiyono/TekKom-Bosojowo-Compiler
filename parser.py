import sys
from ast_nodes import *

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current_token(self):
        return self.tokens[self.pos]

    def eat(self, token_type):
        if self.current_token().type == token_type:
            token = self.current_token()
            self.pos += 1
            return token
        else:
            print(f"Syntax error: Expected {token_type}, but got {self.current_token().type} at line {self.current_token().line}")
            sys.exit(1)

    def parse(self):
        statements = []
        while self.current_token().type != 'EOF':
            statements.append(self.parse_statement())
        return Program(statements)

    def parse_statement(self):
        token = self.current_token()
        if token.type == 'KEYWORD':
            if token.value == 'fungsi':
                return self.parse_function_decl()
            elif token.value == 'yen':
                return self.parse_if_statement()
            elif token.value == 'baleni':
                return self.parse_while_statement()
            elif token.value == 'wangsul':
                return self.parse_return_statement()
        elif token.type == 'BUILTIN':
            if token.value == 'tulis':
                return self.parse_print_statement()
        
        # If it's an ID, it could be an assignment or a function call
        if token.type == 'ID':
            next_token = self.tokens[self.pos + 1]
            if next_token.type == 'ASSIGN':
                return self.parse_assignment()
            elif next_token.type == 'LPAREN':
                # Can be a standalone function call
                expr = self.parse_function_call()
                return expr
        
        # Fallback (though standalone expressions aren't usually statements, we'll parse them just in case)
        return self.parse_expression()

    def parse_function_decl(self):
        self.eat('KEYWORD') # fungsi
        name = self.eat('ID').value
        self.eat('LPAREN')
        params = []
        if self.current_token().type == 'ID':
            params.append(self.eat('ID').value)
            while self.current_token().type == 'COMMA':
                self.eat('COMMA')
                params.append(self.eat('ID').value)
        self.eat('RPAREN')
        self.eat('LBRACE')
        body = []
        while self.current_token().type != 'RBRACE':
            body.append(self.parse_statement())
        self.eat('RBRACE')
        return FunctionDecl(name, params, body)

    def parse_if_statement(self):
        self.eat('KEYWORD') # yen
        self.eat('LPAREN')
        condition = self.parse_expression()
        self.eat('RPAREN')
        self.eat('LBRACE')
        then_branch = []
        while self.current_token().type != 'RBRACE':
            then_branch.append(self.parse_statement())
        self.eat('RBRACE')
        
        else_branch = None
        if self.current_token().type == 'KEYWORD' and self.current_token().value == 'liyane':
            self.eat('KEYWORD') # liyane
            self.eat('LBRACE')
            else_branch = []
            while self.current_token().type != 'RBRACE':
                else_branch.append(self.parse_statement())
            self.eat('RBRACE')
            
        return IfStatement(condition, then_branch, else_branch)

    def parse_while_statement(self):
        self.eat('KEYWORD') # baleni
        self.eat('LPAREN')
        condition = self.parse_expression()
        self.eat('RPAREN')
        self.eat('LBRACE')
        body = []
        while self.current_token().type != 'RBRACE':
            body.append(self.parse_statement())
        self.eat('RBRACE')
        return WhileStatement(condition, body)

    def parse_return_statement(self):
        self.eat('KEYWORD') # wangsul
        expr = self.parse_expression()
        return ReturnStatement(expr)

    def parse_print_statement(self):
        self.eat('BUILTIN') # tulis
        self.eat('LPAREN')
        expr = self.parse_expression()
        self.eat('RPAREN')
        return PrintStatement(expr)



    def parse_assignment(self):
        name = self.eat('ID').value
        self.eat('ASSIGN')
        value = self.parse_expression()
        return Assignment(name, value)

    def parse_expression(self):
        return self.parse_logical()

    def parse_logical(self):
        node = self.parse_equality()
        while self.current_token().type == 'KEYWORD' and self.current_token().value in ('lan', 'utawa'):
            op = self.eat('KEYWORD').value
            right = self.parse_equality()
            node = BinOp(node, op, right)
        return node

    def parse_equality(self):
        node = self.parse_relational()
        while self.current_token().type in ('EQ', 'NEQ'):
            op = self.eat(self.current_token().type).value
            right = self.parse_relational()
            node = BinOp(node, op, right)
        return node

    def parse_relational(self):
        node = self.parse_additive()
        while self.current_token().type in ('LT', 'GT', 'LEQ', 'GEQ'):
            op = self.eat(self.current_token().type).value
            right = self.parse_additive()
            node = BinOp(node, op, right)
        return node

    def parse_additive(self):
        node = self.parse_multiplicative()
        while self.current_token().type in ('PLUS', 'MINUS'):
            op = self.eat(self.current_token().type).value
            right = self.parse_multiplicative()
            node = BinOp(node, op, right)
        return node

    def parse_multiplicative(self):
        node = self.parse_primary()
        while self.current_token().type in ('MUL', 'DIV'):
            op = self.eat(self.current_token().type).value
            right = self.parse_primary()
            node = BinOp(node, op, right)
        return node

    def parse_primary(self):
        token = self.current_token()
        if token.type == 'NUMBER':
            self.eat('NUMBER')
            if '.' in token.value:
                return Number(float(token.value))
            return Number(int(token.value))
        elif token.type == 'STRING':
            self.eat('STRING')
            return String(token.value)
        elif token.type == 'KEYWORD':
            if token.value == 'bener':
                self.eat('KEYWORD')
                return Boolean(True)
            elif token.value == 'salah':
                self.eat('KEYWORD')
                return Boolean(False)
        elif token.type == 'ID':
            # Check if it's a function call
            if self.tokens[self.pos + 1].type == 'LPAREN':
                return self.parse_function_call()
            else:
                self.eat('ID')
                return Identifier(token.value)
        elif token.type == 'LPAREN':
            self.eat('LPAREN')
            node = self.parse_expression()
            self.eat('RPAREN')
            return node
        
        print(f"Syntax error: Unexpected token {token.type} ({token.value}) at line {token.line}")
        sys.exit(1)

    def parse_function_call(self):
        name = self.eat('ID').value
        self.eat('LPAREN')
        args = []
        if self.current_token().type != 'RPAREN':
            args.append(self.parse_expression())
            while self.current_token().type == 'COMMA':
                self.eat('COMMA')
                args.append(self.parse_expression())
        self.eat('RPAREN')
        return FunctionCall(name, args)

if __name__ == '__main__':
    from lexer import Lexer
    code = '''
    angka = 10
    yen (angka > 5) {
        tulis("Gede")
    }
    '''
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    print("Parsed successfully!")
