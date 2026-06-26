import re
import sys

class Token:
    def __init__(self, type, value, line, column):
        self.type = type
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Token({self.type}, {repr(self.value)}, Line: {self.line}, Col: {self.column})"

class Lexer:
    def __init__(self, source_code):
        self.source_code = source_code
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens = []

        # Token specification
        self.token_specs = [
            ('NUMBER',      r'\d+(\.\d*)?'),              # Integer or decimal number
            ('STRING',      r'"[^"]*"'),                  # String literal
            ('KEYWORD',     r'\b(yen|liyane|baleni|fungsi|wangsul|bener|salah|lan|utawa)\b'), # Keywords
            ('BUILTIN',     r'\b(tulis)\b'),              # Builtin functions
            ('ID',          r'[A-Za-z_][A-Za-z0-9_]*'),   # Identifiers
            ('EQ',          r'=='),                       # Equal
            ('NEQ',         r'!='),                       # Not equal
            ('LEQ',         r'<='),                       # Less than or equal
            ('GEQ',         r'>='),                       # Greater than or equal
            ('ASSIGN',      r'='),                        # Assignment
            ('LT',          r'<'),                        # Less than
            ('GT',          r'>'),                        # Greater than
            ('PLUS',        r'\+'),                       # Addition
            ('MINUS',       r'-'),                        # Subtraction
            ('MUL',         r'\*'),                       # Multiplication
            ('DIV',         r'/'),                        # Division
            ('LPAREN',      r'\('),                       # Left Parenthesis
            ('RPAREN',      r'\)'),                       # Right Parenthesis
            ('LBRACE',      r'\{'),                       # Left Brace
            ('RBRACE',      r'\}'),                       # Right Brace
            ('COMMA',       r','),                        # Comma
            ('NEWLINE',     r'\n'),                       # Line endings
            ('SKIP',        r'[ \t]+'),                   # Skip over spaces and tabs
            ('MISMATCH',    r'.'),                        # Any other character
        ]
        self.regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in self.token_specs)

    def tokenize(self):
        for mo in re.finditer(self.regex, self.source_code):
            kind = mo.lastgroup
            value = mo.group()
            if kind == 'NEWLINE':
                self.line += 1
                self.column = 1
                continue
            elif kind == 'SKIP':
                self.column += len(value)
                continue
            elif kind == 'MISMATCH':
                print(f"Lexical error: Unexpected character {value!r} at line {self.line}, column {self.column}")
                sys.exit(1)
            
            # Remove quotes from string value
            if kind == 'STRING':
                value = value[1:-1]
                
            self.tokens.append(Token(kind, value, self.line, self.column))
            self.column += len(value)
        
        self.tokens.append(Token('EOF', '', self.line, self.column))
        return self.tokens

if __name__ == '__main__':
    code = '''
    fungsi tambah(a, b) {
        wangsul a + b
    }
    angka = 10
    tulis("Halo!")
    '''
    lexer = Lexer(code)
    for token in lexer.tokenize():
        print(token)
