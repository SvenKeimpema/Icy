from iceParser import Parser
import subprocess
import compiler
import sys
import os

if __name__ == "__main__":
    parser = Parser()

    assert len(sys.argv) >= 2, "need file path!"

    # TODO add file path
    program = compiler.compileProgram(parser.produceAST(sys.argv[1])) 
    subprocess.run(["nasm", "-f", "elf64", "output.asm"])
    subprocess.run(["ld", "output.o", "-o", "output"])