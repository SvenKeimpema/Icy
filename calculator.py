import astIce

stack = []

def calculate(op: astIce.Expr):
    if op.kind == "BinaryExpr":
        calculate(op.left)
        calculate(op.right)

        var1 = stack.pop()
        var2 = stack.pop()

        if op.operator == '+':
            stack.append(var2+var1)
        elif op.operator == '-':
            stack.append(var2-var1)
        elif op.operator == '*':
            stack.append(var2*var1)
        elif op.operator == '/':
            stack.append(var2/var1)

    elif op.kind == "NumericLiteral":
        stack.append(op.value)
    
    return stack[0]