import astIce

INDEX = -1

def compileProgram(program: astIce.Program):
    global INDEX
    program.body = cross_refrence(program.body)
    with open("output.asm", "w") as out:
        start(out)
        
        for index in range(len(program.body)):
            INDEX = index
            writeProgram(out, program.body[index], program.body[index+1] if index+1 < len(program.body) else None)
        
        out.write("    mov       rax, 60\n")                 
        out.write("    xor       rdi, rdi\n")                
        out.write("    syscall\n")

def writeProgram(out, op, nextOp):
    global INDEX
    if type(op) == str:
        if op == '+':
            out.write("    pop rax\n")
            out.write("    pop rbx\n")
            out.write("    add rbx, rax\n")
            out.write("    push rbx\n")
        elif op == '-':
            out.write("    pop rax\n")
            out.write("    pop rbx\n")
            out.write("    sub rbx, rax\n")
            out.write("    push rbx\n")
        elif op == '*':
            out.write("    pop rax\n")
            out.write("    pop rbx\n")
            out.write("    mul rbx\n")
            out.write("    push rax\n")
        elif op == '/':
            out.write("    pop rax\n")
            out.write("    pop rbx\n")
            out.write("    div rbx\n")
            out.write("    push rax\n")
        return
    if op.kind == "NumericLiteral" and (nextOp.kind != "BinaryExpr" if nextOp != None else True):
        out.write("    push %d\n" % op.value)
    elif op.kind == "BinaryExpr":
        evalBinExpr(out, op)
    elif op.kind == "Function":
        if op.funcType == "print":
            evalPrintExpr(out, op)
            out.write("    pop rdi\n")
            out.write("    call dump\n")
        elif op.funcType == "if":
            evalPrintExpr(out, op)
            out.write("    pop rax\n")
            out.write("    test rax, rax\n")
            out.write("    jz L%d\n" % op.end)
        elif op.funcType == "else":
            out.write("    jmp L%d\n" % op.end)
            out.write("L%d:\n" % INDEX)
        elif op.funcType == "end":
            out.write("    jmp L%d\n" % INDEX)
            out.write("L%d:\n" % INDEX)

def evalPrintExpr(out, func):
    writeProgram(out, func.right, None)

def evalBinExpr(out, binOp):
    writeProgram(out, binOp.left, None)
    writeProgram(out, binOp.right, None)
    writeProgram(out, binOp.operator, None)

def cross_refrence(tokens):
    stack = []
    for ip in range(len(tokens)):
        op = tokens[ip]
        if op.funcType == "if":
            stack.append(ip)
        elif op.funcType == "else":
            if_ip = stack.pop()
            assert tokens[if_ip].funcType == "if", "Else can only be used after if-statement"
            tokens[if_ip].end = ip
            stack.append(ip)
        elif op.funcType == "end":
            block_ip = stack.pop()
            tokens[block_ip].end = ip
    return tokens








def start(out):
    out.write("section .text\n")
    out.write("dump:\n")
    out.write("    mov     r9, -3689348814741910323\n")
    out.write("    sub     rsp, 40\n")
    out.write("    mov     BYTE [rsp+31], 10\n")
    out.write("    lea     rcx, [rsp+30]\n")
    out.write(".L2:\n")
    out.write("    mov     rax, rdi\n")
    out.write("    lea     r8, [rsp+32]\n")
    out.write("    mul     r9\n")
    out.write("    mov     rax, rdi\n")
    out.write("    sub     r8, rcx\n")
    out.write("    shr     rdx, 3\n")
    out.write("    lea     rsi, [rdx+rdx*4]\n")
    out.write("    add     rsi, rsi\n")
    out.write("    sub     rax, rsi\n")
    out.write("    add     eax, 48\n")
    out.write("    mov     BYTE [rcx], al\n")
    out.write("    mov     rax, rdi\n")
    out.write("    mov     rdi, rdx\n")
    out.write("    mov     rdx, rcx\n")
    out.write("    sub     rcx, 1\n")
    out.write("    cmp     rax, 9\n")
    out.write("    ja      .L2\n")
    out.write("    lea     rax, [rsp+32]\n")
    out.write("    mov     edi, 1\n")
    out.write("    sub     rdx, rax\n")
    out.write("    xor     eax, eax\n")
    out.write("    lea     rsi, [rsp+32+rdx]\n")
    out.write("    mov     rdx, r8\n")
    out.write("    mov     rax, 1\n")
    out.write("    syscall\n")
    out.write("    add     rsp, 40\n")
    out.write("    ret\n")
    out.write("global _start\n")
    out.write("_start:\n")