class CodeGenerator:
    def __init__(self, spaces):
        self.instructions = []
        self.indentation = spaces
    
    def generate(self, ast):
        for statement in ast:
            self.process_statement(statement)
        return '\n'.join(self.instructions)
    
    def process_statement(self, statement):
        if statement[0] == 'ASSIGNMENT':
            _, identifier, expression = statement
            code = self.process_expression(expression)
            self.instructions.append(f"{self.indentation}{identifier[1]} = {code}")
        elif statement[0] == 'PRINT':
            _, expression = statement
            code = self.process_expression(expression)
            self.instructions.append(f"{self.indentation}print({code})")
        elif statement[0] == 'CHECK-IF':
            _, expression = statement
            code = self.process_expression(expression)
            self.instructions.append(f"{self.indentation}if {code}:")
        elif statement[0] == 'CHECK-ELSE':
            self.instructions.append(f"{self.indentation}else:")
        elif statement[0] == 'WHILE':
            _, expression = statement
            code = self.process_expression(expression)
            self.instructions.append(f"{self.indentation}while {code}:")
        else:
            raise ValueError(f"Unknown statement type: {statement[0]}")
    
    def process_expression(self, expression):
        if expression[0] == 'NUMBER':
            return expression[1]
        elif expression[0] == 'STRING':
            return expression[1]
        elif expression[0] == 'IDENTIFIER':
            return expression[1]
        elif expression[0] == 'BINARY_EXPR':
            _, operator, left, right = expression
            left_code = self.process_expression(left)
            right_code = self.process_expression(right)
            return f"({left_code} {operator[1]} {right_code})"
        else:
            raise ValueError(f"Invalid expression: {expression}")
