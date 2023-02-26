import astIce, lex

class Parser:
    def __init__(self):
        self.tokens = []

    def notEOF(self) -> bool:
        return self.tokens[0].type != lex.operators.EOF

    def at(self) -> lex.Token:
        return self.tokens[0] if len(self.tokens) > 0  else None
    
    def eat(self) -> lex.Token:
        return self.tokens.pop(0) if len(self.tokens) > 0  else None

    def produceAST(self, filePath) -> astIce.Program:
        self.tokens = lex.lex_file(filePath)
        self.program = astIce.Program()

        while self.notEOF():
            self.program.body.append(self.parse_stmt())

        return self.program

    def parse_stmt(self) -> astIce.Stmt:
        return self.parse_func()

    def parse_func(self):
        if self.at().type == lex.operators.FUNCTION:
            tok = self.eat()
            func = astIce.Function()
            func.funcType = tok.func
            if tok.func in ["print", "if", "elif", "while"]:
                right = self.parse_expr()
                func.right = right
            return func
        else:
            return self.parse_expr()


    def parse_expr(self) -> astIce.Expr:
        return self.parse_conditional_expr()
    
    def parse_conditional_expr(self):
        left = self.parse_additive_expr()

        while self.at().value in ['>', '>=', '<=', '<', '=', '==']:
            op = self.eat().value
            right = self.parse_additive_expr()
            left = astIce.BinaryExpr().setBinExpr(left, right, op)

        return left

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
            case lex.operators.STRING:
                string = astIce.String()
                string.value = self.eat().value
                return string
            case lex.operators.OPENPAREN:
                self.eat()
                value = self.parse_expr()
                self.eat()
                return value
            case lex.operators.LET:
                let = astIce.Let()
                self.eat()
                let.name = self.eat().value
                evalLet = self.eat()
                if evalLet.value == '=':
                    self.eat
                    let.value = self.parse_expr()
                    return let
                elif evalLet.value == '[':
                    let.value = None
                    let.arrvalue = self.eat()
                    self.eat()
                    return let
                else:
                    assert False, "Unimplented token for let, tokType=" + str(evalLet.value)
            case lex.operators.LETNAME:
                var = astIce.Var()
                var.value = self.eat().value
                if len(self.tokens) > 0 and self.at().type == lex.operators.IDENTIFIER:
                    self.eat()
                    identifier = astIce.Identifier()
                    identifier.name = var.value
                    identifier.value = self.parse_expr()
                    return identifier
                elif len(self.tokens) > 0 and self.at().type == lex.operators.OPENARRPAREN:
                    self.eat()
                    arrVar = astIce.ArrVar()
                    arrVar.name = var.value
                    arrVar.arrIndex = self.eat()
                    self.eat()
                    if len(self.tokens) > 0 and self.at().type == lex.operators.IDENTIFIER:
                        self.eat()
                        identifier = astIce.Identifier()
                        identifier.name = var.value
                        identifier.value = self.parse_expr()
                        identifier.arrIndex = arrVar.arrIndex
                        return identifier
                    return arrVar
                return var
            case _:
                assert False, "token unimplemented: " + str(tk)
    