class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = {}
    
    def analyze(self, ast):
        for statement in ast:
            self.check_statement(statement)
    
    def check_statement(self, statement):
        if statement[0] == 'ASSIGNMENT':
            _, identifier, expression = statement
            self.check_expression(expression)
            self.symbol_table[identifier[1]] = expression
        elif statement[0] == 'PRINT' or statement[0] == 'CHECK-IF' or statement[0] == 'WHILE':
            _, expression = statement
            self.check_expression(expression)
        elif statement[0] == 'CHECK-ELSE':
            return
        else:
            raise ValueError(f"Unknown statement type: {statement[0]}")
    
    def check_expression(self, expression):
        if not isinstance(expression, tuple):
            ValueError(f"Invalid expression: {expression}")
        if expression[0] == 'BINARY_EXPR':
            _, operator, left, right = expression
            self.check_expression(left)
            self.check_expression(right)
        elif expression[0] == 'IDENTIFIER':
            found = False
            for i in self.symbol_table:
                if expression[1]==""+i or expression[1]=="not "+i:
                    found = True
                    break
            if not found:
                raise NameError(f"Undefined variable: {expression[1]}")
        elif expression[0] == 'NUMBER' or expression[0]=='STRING':
            pass
        else:
            raise ValueError(f"Invalid expression: {expression}")
    
    def is_number(self, expr):
        return isinstance(expr, tuple) and expr[0] == 'NUMBER'
