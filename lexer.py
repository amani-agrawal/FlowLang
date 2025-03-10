import re
from typing import List, Tuple
import parser
import SemanticAnalyzer
import CodeGenerator

TOKEN_SPECIFICATION = [
    ('WHILE', r'\bwhile\b'),
    ('EQUALITY', r'\bis\b'),
    ('NOT', r'\bnot\b'),
    ('IF', r'\bif\b'),
    ('ELSE', r'\belse\b'),
    ('PRINT', r'\bprint\b'),  # Print statement
    ('STRING', r'"[^"]*"'),   # String literal
    ('NUMBER', r'\b\d+(\.\d*)?\b'),  # Integer or decimal number
    ('IDENTIFIER', r'\b[a-zA-Z_][a-zA-Z_0-9]*\b'),  # Identifiers/Variables
    ('ASSIGN', r'='),        # Assignment operator
    ('OPERATOR', r'[+\-*/^<>]'), # Arithmetic operators
    ('LPAREN', r'\('),       # Left parenthesis
    ('RPAREN', r'\)'),       # Right parenthesis
    ('WHITESPACE', r'\s+'),  # Whitespace (ignored)
    ('UNKNOWN', r'.')        # Any other character (unknown token)
]

TOKEN_REGEX = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_SPECIFICATION)

def lexer(code: str) -> List[Tuple[str, str]]:
    tokens = []
    for match in re.finditer(TOKEN_REGEX, code):
        kind = match.lastgroup
        value = match.group()
        if kind == 'WHITESPACE':
            continue
        elif kind == 'UNKNOWN':
            raise ValueError(f"Unexpected character: {value}")
        elif value=='^':
            value = '**'            #Because ^ in python is **
        elif value=="is":
            value = "=="
        tokens.append((kind, value))
    tokens.append(('END', ';'))
    return tokens

if __name__ == "__main__":
    final_code= ""
    analyzer = SemanticAnalyzer.SemanticAnalyzer()
    with open("/Users/amaniagrawal/Downloads/tester.txt", "r") as file:
        while (line := file.readline()):
            code = line.strip()
            if not code or code[0]=="/":
                continue
            
            tokens = lexer(line)
            print("Lexer:")
            print(tokens)

            token = tokens
            parsed = parser.Parser(token)
            ast = parsed.parse()
            print("Parser:")
            print(ast)

            
            analyzer.analyze(ast)
            print("Semantic analysis passed.")

            spaces = ""
            for i in line:
                if i==" ":
                    spaces+=" "
                else:
                    break

            generator = CodeGenerator.CodeGenerator(spaces)
            final_code += generator.generate(ast)+"\n"
    print(final_code)
    exec(final_code, {}, {})