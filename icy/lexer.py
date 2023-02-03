def getDigit(line, index) -> str:
    num = ""
    while index != len(line) and line[index].isdigit():
        num += line[index]
        index += 1
    return num, index

def getAlpha(line, index) -> str:
    func = ""
    while index != len(line) and (line[index].isdigit() or line[index].isalpha()):
        func += line[index]
        index += 1
    return func, index

def ParenFix(tokens, paren1, paren2, r1, r2, r3, offset=0):

    if tokens[r1] == paren1:
        RPAREN = 0
        for i in range(r1, r2, r3):
            if tokens[i] == paren1:
                RPAREN += 1
            if tokens[i] == paren2:
                RPAREN -= 1
                if RPAREN == 0:
                    if i == len(tokens)-1:
                        tokens.append(paren2)
                    else:
                        tokens.insert(i+offset, paren2)
                    
                    break
    else:
        tokens.insert(r1+offset, paren2)
    return tokens

def lex_line(line):
    tokens = [] 
    index = 0

    while index < len(line):
        # pak alle digits
        if line[index].isdigit():
            num, index = getDigit(line, index)
            tokens.append(num, )
            continue
        # functions
        elif line[index].isalpha():
            func, index = getAlpha(line, index)
            tokens.append(func)
            continue
        elif line[index] == '(':
            tokens.append('(')
        elif line[index] == ')':
            tokens.append(')')
        elif line[index] == '+':
            tokens.append('+')
        elif line[index] == '-':
            tokens.append('-')
        elif line[index] == '*':
            tokens.append('*')
        elif line[index] == '/':
            tokens.append('/')
        elif line[index] == '=':
            if line[index+1] == '=':
                tokens.append('==')
                index += 2
                continue
            tokens.append('=')
        elif line[index] == '>':
            if line[index+1] == '=':
                tokens.append('>=')
                index += 2
                continue
            tokens.append('>')
        elif line[index] == '<':
            if line[index+1] == '=':
                tokens.append('<=')
                index += 2
                continue
            tokens.append('<')
        index += 1

    i = 0
    while i < len(tokens)-1:
        if tokens[i] == '*':
            tokens = ParenFix(tokens, ')', '(', i-1, -1, -1)
            i += 1
            tokens = ParenFix(tokens, '(', ')', i+1, len(tokens), 1, offset=1)
        elif tokens[i] == '/':
            tokens = ParenFix(tokens, ')', '(', i-1, -1, -1)
            i += 1
            tokens = ParenFix(tokens, '(', ')', i+1, len(tokens), 1, offset=1)
        i+=1
    return tokens
            

def lex_file(filePath):
    with open(filePath, 'r') as f:
        program = []

        for line in f.readlines():
            tokens = lex_line(line)
            program.append(tokens)
    
        return program