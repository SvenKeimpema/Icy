from iceParser import Parser
import compiler

if __name__ == "__main__":
    parser = Parser()
    program = compiler.compileProgram(parser.produceAST())