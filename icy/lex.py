from enum import IntEnum
from enum import auto

class operators(IntEnum): 
    INT = auto()
    BINOP = auto()
    OPENPAREN = auto()
    CLOSEPAREN = auto()
    DUMP = auto()
    IDENTIFIER = auto()
    FUNCTION = auto()
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
    
def lex_file():
    with open("code.ice", 'r') as inputData:
        assert operators.totalOps == 9, "need to add new ops for lex, totalOps = %d" % int(operators.totalOps)
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
                    if alpha == 'if':
                        tokens.append(Token(operators.FUNCTION, func="if"))
                    elif alpha == 'else':
                        tokens.append(Token(operators.FUNCTION, func="else"))
                    elif alpha == 'end':
                        tokens.append(Token(operators.FUNCTION, func="end"))
                    continue
                elif line[index] == '+':
                    tokens.append(Token(operators.BINOP, '+'))
                elif line[index] == '-':
                    tokens.append(Token(operators.BINOP, '-'))
                elif line[index] == '*':
                    tokens.append(Token(operators.BINOP, '*'))
                elif line[index] == '/':
                    tokens.append(Token(operators.BINOP, '/'))
                elif line[index] == '(':
                    tokens.append(Token(operators.OPENPAREN))
                elif line[index] == ')':
                    tokens.append(Token(operators.CLOSEPAREN))
                index += 1
            index = 0
        
    tokens.append(Token(operators.EOF))
    return tokens
    

