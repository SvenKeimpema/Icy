from enum import Enum, auto
import lexer
import subprocess
import dumpFunc

class operator(Enum):
    PUSH = auto()
    PLUS = auto()
    MINUS = auto()
    MUL = auto()
    DIV = auto()
    LET = auto()
    LESS = auto()
    GREATER = auto()
    DUMP = auto()
    NAME = auto()
    SETVAR = auto()
    EQUAL = auto()
    LESSEQUAL = auto()
    GREATEREQUAL = auto()
    IF = auto()
    ELSE = auto()
    END = auto()
    WHILE = auto()
    COUNTOPS = auto()


def push(x):
    return (operator.PUSH, x)

def plus():
    return (operator.PLUS, )

def minus():
    return (operator.MINUS, )

def dump():
    return (operator.DUMP, )

def multi():
    return (operator.MUL, )

def divide():
    return (operator.DIV, )

def let():
    return (operator.LET, )

def less():
    return(operator.LESS, )

def greater():
    return(operator.GREATER, )

def names(name):
    return (operator.NAME, name)

def setvar():
    return (operator.SETVAR, )

def equal():
    return (operator.EQUAL, )

def lessEqual():
    return (operator.LESSEQUAL, )

def greaterEqual():
    return (operator.GREATEREQUAL, )

def els():
    return (operator.ELSE, )

def ifOp():
    return (operator.IF, )

def end():
    return(operator.END, )

def whil():
    return(operator.WHILE, )

def checkAdded(added, tokenIdx):
    if added[tokenIdx] != -1:
        return True
    return False

def addToProgram(program, op):
    if op == '*':
        # Call the multi() function and add the result to the program list
        program.append(multi())
    elif op == '/':
        # Call the divide() function and add the result to the program list
        program.append(divide())
    elif op.isdigit():
        # Call the push() function with the integer value of the character and add the result to the program list
        program.append(push(int(op)))
    elif op == '+':
        # Call the plus() function and add the result to the program list
        program.append(plus())
    elif op == '-':
        # Call the minus() function and add the result to the program list
        program.append(minus())
    elif op == 'let':
        # Call the let() function and add the result to the program list
        program.append(let())
    elif op == '=':
        # Call the setvar() function and add the result to the program list
        program.append(setvar())
    elif op == '>':
        program.append(greater())
    elif op == '<':
        program.append(less())
    elif op == '==':
        program.append(equal())
    elif op == '>=':
        program.append(greaterEqual())
    elif op == '<=':
        program.append(lessEqual())
    elif op == 'if':
        program.append(ifOp())
    elif op == 'print':
        # Call the dump() function and add the result to the tempProgram list
        program.append(dump())
    elif op == 'else':
        program.append(els())
    elif op == 'while':
        program.append(whil())
    elif op == 'end':
        program.append(end())
    else:
        # Call the names() function with the character and add the result to the program list
        program.append(names(op))
    
    return program

def decompileLex(lex):
    # Initialize an empty list to store the final program
    program = []

    # Iterate through each code segment in the lexical analysis
    for i in range(len(lex)):
        code = lex[i]
        # Initialize the index to the last character in the code
        index = len(code)-1

        # Store index of bracket
        RBRACKET = -1

        # Iterate through the code segment backwards
        while index >= 0:
            if code[index] == ')':
                # Store the index of the close parenthesis
                RBRACKET = index
            elif code[index] == '(':
                # Store the index of the open parenthesis
                startIdx = index
                
                # Iterate through the characters between the parentheses
                for index2 in range(index+1, RBRACKET):
                    program = addToProgram(program, code[index2])
                # Remove the characters between the parentheses from the code segment
                del code[startIdx:RBRACKET+1]
                # Reset the index to the last character in the updated code segment
                index = len(code)-1
                # Skip to the next iteration
                continue
            # Decrement the index
            index -= 1

        program = addToProgram(program, code[index])

    # Return the final program list
    return program

def getVars(stack, program, variables={}):
    a = stack.pop()
    if a in variables:
        a = variables[a]
    b = -1
    if len(program) == 0 or (program[0][0] != operator.PUSH and program[0][0] != operator.NAME):
        b = stack.pop()
    else:
        b = program.pop(0)[1]

    if b in variables:
        b = variables[b]

    return a, b

def getNextVar(program):
    b = -1
    if len(program) == 0 or (program[0][0] != operator.PUSH and program[0][0] != operator.NAME):
        b = False
    else:
        b = program.pop(0)[1]
    
    return b

def simulate(decompiledLex):
    currStack = []
    variables = {}
    assert operator.COUNTOPS.value == 19, "operator not implemented in func \"simulate\""
    for program in decompiledLex:
        # print(program, currStack)
        while len(program) > 0:
            op = program.pop(0)
            if op[0] == operator.LET:
                name = program.pop(0)[1]
                program.pop(0)
                value = simulate([program])
                if type(value) == str:
                    raise Exception("Wrong type, type should be (int, double, float) not string")
                variables[name] = value
                program = []
            elif op[0] == operator.PUSH:
                currStack.append(op[1])
            elif op[0] == operator.PLUS:
                a, b = getVars(currStack, program, variables)
                
                currStack.append(a+b)
            elif op[0] == operator.MINUS:
                a, b = getVars(currStack, program, variables)
                
                currStack.append(a-b)
            elif op[0] == operator.MUL:
                a, b = getVars(currStack, program, variables)

                currStack.append(a*b)
            elif op[0] == operator.DIV:
                a, b = getVars(currStack, program, variables)

                # TODO betere error handling
                assert b == 0, "tried to divide by 0"

                currStack.append(a/b)
            elif op[0] == operator.GREATER:
                a, b = getVars(currStack, program, variables)
                
                currStack.append(a>b)
            elif op[0] == operator.LESS:
                a, b = getVars(currStack, program, variables)
                
                currStack.append(a<b)
            elif op[0] == operator.EQUAL:
                a, b = getVars(currStack, program, variables)

                currStack.append(a==b)

            elif op[0] == operator.GREATEREQUAL:
                a, b = getVars(currStack, program, variables)

                currStack.append(a>=b)
            elif op[0] == operator.LESSEQUAL:
                a, b = getVars(currStack, program, variables)

                currStack.append(a<=b)

            elif op[0] == operator.IF:
                var = currStack.pop()
            elif op[0] == operator.DUMP:
                if len(currStack) == 0:
                    raise Exception("Cannot print because nothing is in the stack, line: ")
                item = currStack.pop()
                if item in variables:
                    print(variables[item])
                else:
                    print(item)
            else:
                currStack.append(op[1])

    if len(currStack) > 0:
        return currStack.pop()
    else:
        return 0

def ends(program):
    endOps = []
    elseOps = []
    line = 0
    while line < len(program):
        op = program[line]
        if op[0] == operator.END: 
            endOps.append(line)
        elif op[0] == operator.ELSE:
            elseOps.append(line)
        line += 1
    return endOps, elseOps
        
def compile(program, out):
    print(program)
    with open(out, "w") as out:
        out.write("section .text\n")
        dumpFunc.writeDumpASM(out)

        out.write("global _start\n")
        out.write("_start:\n")
        assert operator.COUNTOPS.value == 19, "operator not implemented in func \"compile\""
        endOps, elseOps = ends(program)
        VARS = []
        whiles = []
        line = 0
        while len(program) > 0:
            op = program.pop(0)
            if op[0] == operator.LET:
                # TODO let fix + sim
                NAME = program.pop(0)[1]
                program.pop(0)
                VALUE = simulate([program])
                VARS.append((NAME, VALUE))
            elif op[0] == operator.PUSH:
                out.write("    push %d\n" % op[1])
            elif op[0] == operator.PLUS:
                b = getNextVar(program)
                if not b:
                    out.write("    pop rax\n")
                else:
                    out.write("    mov rax, %d\n" % b)
                out.write("    pop rbx\n")
                out.write("    add rbx, rax\n")
                out.write("    push rbx\n")

            elif op[0] == operator.MINUS:
                b = getNextVar(program)
                if not b:
                    out.write("    pop rax\n")
                else:
                    out.write("    mov rax, %d\n" % b)
                out.write("    pop rbx\n")
                out.write("    sub rbx, rax\n")
                out.write("    push rbx\n")
            elif op[0] == operator.MUL:
                b = getNextVar(program)
                if not b:
                    out.write("    pop rax\n")
                else:
                    out.write("    mov rax, %d\n" % b)
                out.write("    pop rbx\n")
                out.write("    mul rbx\n")
                out.write("    push rax\n")
            elif op[0] == operator.DIV:
                b = getNextVar(program)
                if b == False and type(b) == bool:
                    out.write("    pop rax\n")
                else:
                    if b == 0:
                        raise ZeroDivisionError("tried to divide by 0")
                    out.write("    mov rax, %d\n" % b)
                out.write("    pop rbx\n")
                out.write("    div rbx\n")
                out.write("    push rax\n")
            elif op[0] == operator.GREATER:
                b = getNextVar(program)
                if not b:
                    out.write("    pop rax\n")
                else:
                    out.write("    mov rax, %d\n" % b)
                out.write("    mov rcx, 0\n")
                out.write("    mov rdx, 1\n")
                out.write("    pop rbx\n")
                out.write("    cmp rbx, rax\n")
                out.write("    CMOVG rcx, rdx\n")
                out.write("    push  rcx\n")
            elif op[0] == operator.LESS:
                b = getNextVar(program)
                if not b:
                    out.write("    pop rax\n")
                else:
                    out.write("    mov rax, %d\n" % b)
                out.write("    mov rcx, 0\n")
                out.write("    mov rdx, 1\n")
                out.write("    pop rbx\n")
                out.write("    cmp rbx, rax\n")
                out.write("    cmovl rcx, rdx\n")
                out.write("    push  rcx\n")
            elif op[0] == operator.EQUAL:
                b = getNextVar(program)
                if not b:
                    out.write("    pop rax\n")
                else:
                    out.write("    mov   rax, %d\n" % b)
                out.write("    mov   rcx, 0\n")
                out.write("    mov   rdx, 1\n")
                out.write("    pop   rbx\n")
                out.write("    cmp   rbx, rax\n")
                out.write("    cmove rcx, rdx\n")
                out.write("    push  rcx\n")
            elif op[0] == operator.GREATEREQUAL:
                b = getNextVar(program)
                if not b:
                    out.write("    pop rax\n")
                else:
                    out.write("    mov   rax, %d\n" % b)
                out.write("    mov   rcx, 0\n")
                out.write("    mov   rdx, 1\n")
                out.write("    pop   rbx\n")
                out.write("    cmp   rbx, rax\n")
                out.write("    cmovge rcx, rdx\n")
                out.write("    push  rcx\n")
            elif op[0] == operator.LESSEQUAL:
                b = getNextVar(program)
                if not b:
                    out.write("    pop rax\n")
                else:
                    out.write("    mov   rax, %d\n" % b)
                out.write("    mov   rcx, 0\n")
                out.write("    mov   rdx, 1\n")
                out.write("    pop   rbx\n")
                out.write("    cmp   rax, rbx\n")
                out.write("    cmovle rcx, rdx\n")
                out.write("    push  rcx\n")
            elif op[0] == operator.IF:
                out.write("    pop rax\n")
                out.write("    test rax, rax\n")
                end = elseOps.pop(len(elseOps)-1) if len(elseOps) > 0 else endOps.pop(0)
                out.write("    je L%d\n" % end)
                out.write("    jmp L%d\n" % line)
                out.write("L%d:\n" % line)
                continue
            elif op[0] == operator.ELSE:
                end = endOps.pop(0)
                out.write("    jmp L%d\n" % end)
                out.write("L%d:\n" % line)
            elif op[0] == operator.END:
                if len(whiles) > 0:
                    l = whiles.pop(0)
                    out.write("    jmp WH%d\n" % l)
                    out.write("L%d:\n" % int(line+1))
                else:
                    out.write("    jmp L%d\n" % line)
                    out.write("L%d:\n" % line)
            elif op[0] == operator.WHILE:
                out.write("    jmp WH%d\n" % line)
                out.write("WH%d:\n" % line)
                out.write("    pop rax\n")
                out.write("    test rax, rax\n")

                end = endOps.pop(0)
                out.write("    je L%d\n" % end)
                out.write("    jmp L%d\n" % int(end+1))

                out.write("L%d:\n" % end)
                whiles.append(line)
            elif op[0] == operator.DUMP:
                out.write("    pop rdi\n")
                out.write("    call dump\n")
            else:
                out.write("    push " + str(op[1]) + "\n")
        line += 1
            
        out.write("    mov       rax, 60\n")                 
        out.write("    xor       rdi, rdi\n")                
        out.write("    syscall\n")

        out.write("section .data\n")
        for item in VARS:
            out.write(str(item[0]) + " DD %d\n" % VALUE)
if __name__ == '__main__':
    lex = lexer.lex_file("code.ice")
    program = decompileLex(lex)
    compile(program, "output.asm")
    subprocess.call(["nasm", "-felf64", "output.asm"])
    subprocess.call(["ld", "-o", "output", "output.o"])
    # simulate(program)
