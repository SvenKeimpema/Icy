from enum import IntEnum
from enum import auto

class operators(IntEnum): 
    STRING = auto()
    INT = auto()
    BINOP = auto()
    OPENPAREN = auto()
    CLOSEPAREN = auto()
    OPENARRPAREN = auto()
    CLOSEARRPAREN = auto()
    DUMP = auto()
    IDENTIFIER = auto()
    FUNCTION = auto()
    LET = auto()
    LETNAME = auto()
    EOF = auto()
    totalOps = auto()

class Token:
    def __init__(self, type:int, value=None, func=""):
        self.value = value
        self.type = type
        self.func = func
        self.end = -1
        # add something for error handling
    
    def __str__(self):
        return "operator = " + str(operators(self.type).name) + ", value = " + str(self.value)

def getDigit(line: str, index: int):
    num: str = ""
    while index < len(line) and line[index].isnumeric():
        num += line[index]
        index += 1
    return int(num), index

def getAlpha(line: str, index: int):
    alpha: str = ""
    while  index < len(line) and (line[index].isalpha() or line[index].isnumeric()):
        alpha += line[index]
        index += 1
    return alpha, index
    
def lex_file(filePath):
    with open(filePath, 'r') as inputData:
        assert operators.totalOps == 14, "need to add new ops for lex, totalOps = %d" % int(operators.totalOps)
        tokens = []
        index = 0
        for line in inputData:
            while index < len(line):
                if line[index].isnumeric():
                    num, index = getDigit(line, index)
                    tokens.append(Token(operators.INT, num))
                    continue
                elif line[index].isalpha():
                    alpha, index = getAlpha(line, index)
                    if alpha == 'print':
                        tokens.append(Token(operators.FUNCTION, func="print"))
                    elif alpha == 'if':
                        tokens.append(Token(operators.FUNCTION, func="if"))
                    elif alpha == 'else':
                        tokens.append(Token(operators.FUNCTION, func="else"))
                    elif alpha == 'elif':
                        tokens.append(Token(operators.FUNCTION, func="elif"))
                    elif alpha == 'while':
                        tokens.append(Token(operators.FUNCTION, func="while"))
                    elif alpha == 'end':
                        tokens.append(Token(operators.FUNCTION, func="end"))
                    elif alpha == 'let':
                        tokens.append(Token(operators.LET))
                    else:
                        tokens.append(Token(operators.LETNAME, value=alpha))
                    continue
                elif line[index] == '"':
                    index += 1
                    string = ""
                    while line[index] != '"':
                        string += line[index]
                        index += 1
                    tokens.append(Token(operators.STRING, value=string))
                elif line[index] == '+':
                    tokens.append(Token(operators.BINOP, '+'))
                elif line[index] == '-':
                    tokens.append(Token(operators.BINOP, '-'))
                elif line[index] == '*':
                    tokens.append(Token(operators.BINOP, '*'))
                elif line[index] == '/':
                    tokens.append(Token(operators.BINOP, '/'))
                elif line[index] == '>':
                    if line[index+1] == '=':
                        tokens.append(Token(operators.BINOP, '>='))
                        index += 1
                    else:
                        tokens.append(Token(operators.BINOP, '>'))
                elif line[index] == '<':
                    if line[index+1] == '=':
                        tokens.append(Token(operators.BINOP, '<='))
                        index += 1
                    else:
                        tokens.append(Token(operators.BINOP, '<'))
                elif line[index] == '(':
                    tokens.append(Token(operators.OPENPAREN))
                elif line[index] == ')':
                    tokens.append(Token(operators.CLOSEPAREN))
                elif line[index] == '[':
                    tokens.append(Token(operators.OPENARRPAREN, '['))
                elif line[index] == ']':
                    tokens.append(Token(operators.CLOSEARRPAREN, ']'))
                elif line[index] == '(':
                    tokens.append(Token(operators.OPENPAREN))
                elif line[index] == ')':
                    tokens.append(Token(operators.CLOSEPAREN))
                elif line[index] == '=':
                    if line[index+1] == '=':
                        tokens.append(Token(operators.BINOP, '=='))
                        index += 1
                    else:
                        tokens.append(Token(operators.IDENTIFIER, '='))
                elif line[index] == '#':
                    break
                index += 1
            index = 0
        
    tokens.append(Token(operators.EOF))
    return tokens
    

