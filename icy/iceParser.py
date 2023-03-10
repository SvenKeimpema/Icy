import astIce, lex

class Parser:
    def __init__(self):
        self.tokens = []

    def notEOF(self) -> bool:
        return self.tokens[0].type != lex.operators.EOF

    def at(self) -> lex.Token:
        return self.tokens[0]
    
    def eat(self) -> lex.Token:
        return self.tokens.pop(0)

    def produceAST(self) -> astIce.Program:
        self.tokens = lex.lex_file()
        program = astIce.Program()

        while self.notEOF():
            program.body.append(self.parse_stmt())

        return program

    def parse_stmt(self) -> astIce.Stmt:
        return self.parse_func()

    def parse_func(self):
        if self.at().type == lex.operators.FUNCTION:
            tok = self.eat()
            func = astIce.Function()
            func.funcType = tok.func
            if tok.func in ["print", "if"]:
                right = self.parse_expr()
                func.right = right
            return func
        else:
            return self.parse_expr()


    def parse_expr(self) -> astIce.Expr:
        return self.parse_additive_expr()
    
    def parse_additive_expr(self) -> astIce.Expr:
        left = self.parse_multiplicitive_expr()

        while self.at().value == '+' or self.at().value == '-':
            op = self.eat().value
            right = self.parse_multiplicitive_expr()
            left = astIce.BinaryExpr().setBinExpr(left, right, op)

        return left
    
    def parse_multiplicitive_expr(self) -> astIce.Expr:
        left = self.parsePrimeExpr()

        while self.at().value == '*' or self.at().value == '/':
            op = self.eat().value
            right = self.parsePrimeExpr()
            left = astIce.BinaryExpr().setBinExpr(left, right, op)

        return left

    def parsePrimeExpr(self):
        tk = self.at().type

        match tk:
            case lex.operators.IDENTIFIER:
                identifier = astIce.Identifier()
                identifier.symbol = self.eat().value
                return identifier
            case lex.operators.INT:
                identifier = astIce.NumericLiteral()
                identifier.value = self.eat().value
                return identifier
            case lex.operators.OPENPAREN:
                self.eat()
                value = self.parse_expr()
                self.eat()
                return value
            case _:
                assert False, "token unimplemented: " + str(tk)
    