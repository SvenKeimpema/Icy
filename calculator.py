import astIce

stack = []

def calculate(op: astIce.Expr):
    print(op.kind)
    if op.kind == "BinaryExpr":
        print("test")
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
        elif op.operator == '=':
            stack.append(var1==var2)
        elif op.operator == '>':
            stack.append(var1>var2)
        elif op.operator == '<':
            stack.append(var1<var2)
        elif op.operator == '>=':
            stack.append(var1>=var2)
        elif op.operator == '<=':
            stack.append(var1<=var2)

    elif op.kind == "NumericLiteral":
        stack.append(op.value)
    else:
        stack.append(op.value)
    
    return stack[0]