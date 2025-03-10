class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
    
    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None
    
    def consume(self, expected_type):
        if self.peek() and self.peek()[0] == expected_type:
            self.pos += 1
            return self.tokens[self.pos - 1]
        raise SyntaxError(f"Expected {expected_type}, got {self.peek()}")
    
    def parse_expression(self):
        isNot= False
        if self.peek()[0] == "NOT":
            isNot = True
            self.consume('NOT')
        
        if self.peek()[0] == 'NUMBER':
            left = self.consume('NUMBER')
        elif self.peek()[0] == 'STRING':
            left = self.consume("STRING")
        elif self.peek()[0] == 'IDENTIFIER':
            left = self.consume('IDENTIFIER')
        else:
            raise SyntaxError(f"Unexpected expression: {self.peek[1]}")
        if isNot:
                left = (left[0], "not "+left[1])
        while self.peek() and (self.peek()[0] == 'OPERATOR' or self.peek()[0] == "EQUALITY"):
            op = self.consume(self.peek()[0])
            if self.peek()[0]!="NUMBER" and self.peek()[0]!="STRING" and self.peek()[0]!="IDENTIFIER":
                raise SyntaxError(f"Unexpected expression: {self.peek[1]}")
            right = self.consume(self.peek()[0])
            left = ('BINARY_EXPR', op, left, right)
        return left
    
    def parse_assignment(self):
        identifier = self.consume('IDENTIFIER')
        self.consume('ASSIGN')
        expr = self.parse_expression()
        return ('ASSIGNMENT', identifier, expr)

    def parse_print(self):
        self.consume('PRINT')
        if self.peek()[0] != 'LPAREN':
            raise SyntaxError(f"Unexpected expression: {self.peek[1]}")
        self.consume('LPAREN')
        expr = self.parse_expression()
        if self.peek()[0] != 'RPAREN':
            raise SyntaxError(f"Unexpected expression: {self.peek[1]}")
        self.consume('RPAREN')
        return ('PRINT', expr)
    
    def parse_if(self):
        self.consume('IF')
        expr = self.parse_expression()
        return ('CHECK-IF', expr)

    def parse_while(self):
        self.consume('WHILE')
        expr = self.parse_expression()
        return ('WHILE', expr)
    
    def parse_else(self):
        self.consume('ELSE')
        if self.peek()[0]!="END":
            raise SyntaxError(f"Unexpected expression: {self.peek[1]}")
        return ('CHECK-ELSE', None)
    
    def parse(self):
        ast = []
        while self.pos < len(self.tokens):
            if self.peek()[0] == 'END':
                break
            elif self.peek()[0] == 'PRINT':
                ast.append(self.parse_print())
            elif self.peek()[0] == 'IF':
                ast.append(self.parse_if())
            elif self.peek()[0] == 'ELSE':
                ast.append(self.parse_else())
            elif self.peek()[0] == 'WHILE':
                ast.append(self.parse_while())
            else:
                ast.append(self.parse_assignment())
        return ast
