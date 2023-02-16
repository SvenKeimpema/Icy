import astIce
import calculator

INDEX = -1
VARIABLES = {}

def setVar(out, push: bool, reg: str):
    if push:
        out.write(f"    push {reg}\n")
    elif reg != "rax":
        out.write(f"    mov rax, {reg}")

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
        out.write("    syscall\n\n")
        out.write("section .data\n")
        out.write("str: db \"hi\", 10\n")
        out.write("strlen: db 3\n")
        for name, value in VARIABLES.items():
            out.write(f"    {name}: dq {value}\n")

def writeValue(out, side, opSide, nextOp):
    reg = "rax" if side == "left" else "rbx"

    if opSide.kind == "BinaryExpr":
        writeProgram(out, opSide, nextOp)
        out.write(f"    pop {reg}\n")
    elif opSide.kind == "NumericLiteral":
        out.write(f"    mov {reg}, {opSide.value}\n")
    else:
        out.write(f"    mov {reg}, [{opSide.value}]\n")

def writeProgram(out, op, nextOp):
    global INDEX
    if op.kind == "BinaryExpr":
        if op.left.kind == "BinaryExpr":
            writeValue(out, "left", op.left, nextOp)
            writeValue(out, "right", op.right, nextOp)
        elif op.right.kind == "BinaryExpr":
            writeValue(out, "right", op.right, nextOp)
            writeValue(out, "left", op.left, nextOp)
        else:
            writeValue(out, "left", op.left, nextOp)
            writeValue(out, "right", op.right, nextOp)
        end = op.end
        oper = op.operator

        if oper == '+':
            out.write(f"    add rax, rbx\n")
            setVar(out, op.push, "rax")
        elif oper == '-':
            out.write(f"    sub rax, rbx\n")
            setVar(out, op.push, "rax")
        elif oper == '*':
            out.write(f"    mul rbx\n")
            setVar(out, op.push, "rax")
        elif oper == '/':
            out.write(f"    div rbx\n")
            setVar(out, op.push, "rax")
        elif oper == '<':
            if end == -1:
                out.write("    mov rcx, 0\n")
                out.write("    mov rdx, 1\n")
                out.write(f"    cmp rax, rbx\n")
                out.write("    cmovl rcx, rdx\n")
                setVar(out, op.push, "rcx")
            else:
                out.write(f"    cmp rax, rbx\n")
                out.write(f"    jl L{end}\n")
        elif oper == '>':
            if end == -1:
                out.write("    mov rcx, 0\n")
                out.write("    mov rdx, 1\n")
                out.write(f"    cmp rax, rbx\n")
                out.write("    cmovg rcx, rdx\n")
                setVar(out, op.push, "rcx")
            else:
                out.write(f"    cmp rax, rbx\n")
                out.write(f"    jg L{end}\n")
        elif oper == '<=':
            if end == -1:
                out.write("    mov rcx, 0\n")
                out.write("    mov rdx, 1\n")
                out.write(f"    cmp rax, rbx\n")
                out.write("    cmovle rcx, rdx\n")
                setVar(out, op.push, "rcx")
            else:
                out.write(f"    cmp rax, rbx\n")
                out.write(f"    jle L{end}\n")
        elif oper == '>=':
            if end == -1:
                out.write("    mov rcx, 0\n")
                out.write("    mov rdx, 1\n")
                out.write(f"    cmp rax, rbx\n")
                out.write("    cmovg rcx, rdx\n")
                setVar(out, op.push, "rcx")
            else:
                out.write(f"    cmp rax, rbx\n")
                out.write(f"    jge L{end}\n")
        return
    if op.kind == "Identifier":
        if op.value.kind == "BinaryExpr":
            op.value.push = False
        writeProgram(out, op.value, nextOp)
        out.write(f"    mov [{op.name}], rax\n")
    elif op.kind == "NumericLiteral" and (nextOp.kind != "BinaryExpr" if nextOp != None else True):
        out.write("    push %d\n" % op.value)
    elif op.kind == "Var" and (nextOp.kind != "BinaryExpr" if nextOp != None else True):
        out.write(f"    mov rax, [{op.value}]\n")
        out.write(f"    push rax\n")
    elif op.kind == "string":
        out.write(f"    mov rax, \"{op.value}\"\n")
        out.write(f"    mov rbx, {len(op.value)}\n")
        out.write(f"    mov [str], rax\n")
        out.write(f"    mov [strlen], rbx\n")

    elif op.kind == "Let":
            VARIABLES[op.name] = calculator.calculate(op.value)
    elif op.kind == "Function":
        if op.funcType == "print":
            if op.right.kind != "string":
                value = calculator.calculate(op.right)
                out.write(f"    mov rdi, {value}\n")
                out.write("    call dump\n")
            else:
                evalPrintExpr(out, op)
                out.write("    call printStr\n")
        elif op.funcType == "if":
            evalPrintExpr(out, op)
            out.write("    pop rax\n")
            out.write("    test rax, rax\n")
            out.write("    jz L%d\n" % op.end)
        elif op.funcType == "else":
            out.write("    jmp L%d\n" % op.end)
            out.write("L%d:\n" % INDEX)
        elif op.funcType == "elif":
            out.write("L%d:\n" % INDEX)
            evalPrintExpr(out, op)
            out.write("    pop rax\n")
            out.write("    test rax, rax\n")
            out.write("    jz L%d\n" % op.end)
        elif op.funcType == "end":
            out.write("    jmp L%d\n" % op.end)
            out.write("L%d:\n" % INDEX)
        elif op.funcType == "while":
            out.write("    jmp L%d\n" % INDEX)
            out.write("L%d:\n" % INDEX)
            evalPrintExpr(out, op)
            out.write("    jmp L%d\n" % op.end)
            out.write("L%d:\n" % (INDEX+1))

def evalPrintExpr(out, func):
    writeProgram(out, func.right, None)

def cross_refrence(tokens):
    stack = []
    for ip in range(len(tokens)):
        op = tokens[ip]
        if op.kind != "Function":
            continue
        if op.funcType in ["if", "while"]:
            stack.append(ip)
        elif op.funcType == "else":
            if_ip = stack.pop()
            assert tokens[if_ip].funcType in ["if", "elif"], "Else can only be used after if or elif-statement"
            tokens[if_ip].end = ip
            stack.append(ip)
        elif op.funcType == "elif":
            if_ip = stack.pop()
            assert tokens[if_ip].funcType in ["if", "elif"], "Else can only be used after if or elif-statement"
            tokens[if_ip].end = ip
            stack.append(ip)
        elif op.funcType == "end":
            block_ip = stack.pop()
            if tokens[block_ip].funcType == "while":
                tokens[block_ip].right.end = block_ip+1
                tokens[ip].end = block_ip
            else:
                tokens[ip].end = ip
            tokens[block_ip].end = ip
    return tokens








def start(out):
    out.write("section .text\n")
    out.write("dump:\n")
    out.write("    mov     r9, -3689348814741910323\n")
    out.write("    sub     rsp, 40\n")
    out.write("    mov     BYTE [rsp+31], 10\n")
    out.write("    lea     rcx, [rsp+30]\n\n")
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
    out.write("    ret\n\n")
    out.write("printStr:\n")
    out.write("    mov       rax, 1                  ; system call for write\n")
    out.write("    mov       rdi, 1                  ; file handle 1 is stdout\n")
    out.write("    mov       rsi, str                ; address of string to output\n")
    out.write("    mov       rdx, [strlen]             ; number of bytes\n")
    out.write("    syscall\n")
    out.write("    ret   \n\n\n\n\n\n")
    out.write("global _start\n")
    out.write("_start:\n")