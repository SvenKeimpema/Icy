from iceParser import Parser
import subprocess
import compiler

if __name__ == "__main__":
    parser = Parser()
    program = compiler.compileProgram(parser.produceAST())
    subprocess.run(["nasm", "-f", "elf64", "output.asm"])
    subprocess.run(["ld", "output.o", "-o", "output"])