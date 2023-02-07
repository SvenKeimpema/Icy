from enum import IntEnum
from enum import auto

class NodeType(IntEnum): 
    Program = auto()
    NumericLiteral = auto()
    Identifier = auto()
    BinaryExpr = auto()

class Stmt:
    def __init__(self):
        self.kind: NodeType = None

class Program(Stmt):
    def __init__(self):
        self.kind: NodeType = "Program"
        self.body: Stmt = []

class Expr(Stmt):
    def __init__(self):
        pass

class BinaryExpr(Expr):
    def __init__(self):
        self.kind: NodeType = "BinaryExpr"
        self.left: Expr = None
        self.right: Expr = None
        self.operator: str = ""
    
    def setBinExpr(self, left, right, op):
        self.left = left
        self.right = right
        self.operator = op
        return self

class Identifier(Expr):
    def __init__(self):
        self.kind: NodeType = "Identifier"
        self.symbol: str = None

class Function(Expr):
    def __init__(self):
        self.kind: NodeType = "Function"
        self.funcType: str = ""
        self.end: int = -1
        self.right: Expr = None

class NumericLiteral(Expr):
    def __init__(self):
        self.kind: NodeType = "NumericLiteral"
        self.value: int
    
    def setValue(self, x):
        self.value = x
        return self

    def __str__(self):
        return str(self.value)