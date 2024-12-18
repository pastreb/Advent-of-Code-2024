import os.path
import re


def read_input(input_file_name):
    input_file = os.path.join(os.path.dirname(__file__), input_file_name)
    with open(input_file, "r") as f:
        lines = f.readlines()   
        return lines

# --- Day 17: Chronospatial Computer ---

# The Historians push the button on their strange device, but this time, you 
# all just feel like you're falling.

# "Situation critical", the device announces in a familiar voice. 
# "Bootstrapping process failed. Initializing debugger...."

# The small handheld device suddenly unfolds into an entire computer! The 
# Historians look around nervously before one of them tosses it to you.

# This seems to be a 3-bit computer: its program is a list of 3-bit numbers 
# (0 through 7), like 0,1,2,3. The computer also has three registers named A, 
# B, and C, but these registers aren't limited to 3 bits and can instead 
# hold any integer.

# The computer knows eight instructions, each identified by a 3-bit number 
# (called the instruction's opcode). Each instruction also reads the 3-bit 
# number after it as an input; this is called its operand.

# A number called the instruction pointer identifies the position in the 
# program from which the next opcode will be read; it starts at 0, pointing 
# at the first 3-bit number in the program. Except for jump instructions, the 
# instruction pointer increases by 2 after each instruction is processed (to 
# move past the instruction's opcode and its operand). If the computer tries 
# to read an opcode past the end of the program, it instead halts.

# So, the program 0,1,2,3 would run the instruction whose opcode is 0 and 
# pass it the operand 1, then run the instruction having opcode 2 and pass 
# it the operand 3, then halt.

# There are two types of operands; each instruction specifies the type of its 
# operand. The value of a literal operand is the operand itself. For example, 
# the value of the literal operand 7 is the number 7. The value of a combo 
# operand can be found as follows:

# - Combo operands 0 through 3 represent literal values 0 through 3.
# - Combo operand 4 represents the value of register A.
# - Combo operand 5 represents the value of register B.
# - Combo operand 6 represents the value of register C.
# - Combo operand 7 is reserved and will not appear in valid programs.

# The eight instructions are as follows:

# The adv instruction (opcode 0) performs division. The numerator is the 
# value in the A register. The denominator is found by raising 2 to the power 
# of the instruction's combo operand. (So, an operand of 2 would divide A by 
# 4 (2^2); an operand of 5 would divide A by 2^B.) The result of the 
# division operation is truncated to an integer and then written to the A 
# register.

# The bxl instruction (opcode 1) calculates the bitwise XOR of register B 
# and the instruction's literal operand, then stores the result in register 
# B.

# The bst instruction (opcode 2) calculates the value of its combo operand 
# modulo 8 (thereby keeping only its lowest 3 bits), then writes that value 
# to the B register.

# The jnz instruction (opcode 3) does nothing if the A register is 0. 
# However, if the A register is not zero, it jumps by setting the 
# instruction pointer to the value of its literal operand; if this 
# instruction jumps, the instruction pointer is not increased by 2 after 
# this instruction.

# The bxc instruction (opcode 4) calculates the bitwise XOR of register B 
# and register C, then stores the result in register B. (For legacy reasons, 
# this instruction reads an operand but ignores it.)

# The out instruction (opcode 5) calculates the value of its combo operand 
# modulo 8, then outputs that value. (If a program outputs multiple values, 
# they are separated by commas.)

# The bdv instruction (opcode 6) works exactly like the adv instruction 
# except that the result is stored in the B register. (The numerator is still 
# read from the A register.)

# The cdv instruction (opcode 7) works exactly like the adv instruction 
# except that the result is stored in the C register. (The numerator is still 
# read from the A register.)

# Here are some examples of instruction operation:

# - If register C contains 9, the program 2,6 would set register B to 1.
# - If register A contains 10, the program 5,0,5,1,5,4 would output 0,1,2.
# - If register A contains 2024, the program 0,1,5,4,3,0 would output 
#   4,2,5,6,7,7,7,7,3,1,0 and leave 0 in register A.
# - If register B contains 29, the program 1,7 would set register B to 26.
# - If register B contains 2024 and register C contains 43690, the program 
#   4,0 would set register B to 44354.

# The Historians' strange device has finished initializing its debugger and 
# is displaying some information about the program it is trying to run (your 
# puzzle input). For example:

# Register A: 729
# Register B: 0
# Register C: 0

# Program: 0,1,5,4,3,0

# Your first task is to determine what the program is trying to output. To 
# do this, initialize the registers to the given values, then run the given 
# program, collecting any output produced by out instructions. (Always join 
# the values produced by out instructions with commas.) After the above 
# program halts, its final output will be 4,6,3,5,6,3,5,2,1,0.

# Using the information provided by the debugger, initialize the registers to 
# the given values, then run the program. Once it halts, what do you get if 
# you use commas to join the values it output into a single string?

class Computer:
    def __init__(self, registers, program):
        self.dummy = 0
        self.ip = 0
        self.output = ""
        self.output_list = []
        self.reg_a = registers[0]
        self.reg_b = registers[1]
        self.reg_c = registers[2]
        self.program = program
    
    def run(self):
        while self.ip < len(self.program):
            opcode, operand = self.program[self.ip], self.program[self.ip+1]
            if opcode == 0:
                self.adv(operand)
            elif opcode == 1:
                self.bxl(operand)
            elif opcode == 2:
                self.bst(operand)
            elif opcode == 3:
                self.jnz(operand)
                continue
            elif opcode == 4:
                self.bxc(operand)
            elif opcode == 5:
                self.out(operand)
            elif opcode == 6:
                self.bdv(operand)
            elif opcode == 7:
                self.cdv(operand)
            self.ip += 2

    def combo(self, x):
        if x <= 3:
            return x
        elif x == 4:
            return self.reg_a
        elif x == 5:
            return self.reg_b
        elif x == 6:
            return self.reg_c
        exit(f"Invalid program; encountered combo operand {7}")

    def adv(self, operand):
        self.reg_a = self.reg_a//pow(2, self.combo(operand))

    def bxl(self, operand):
        self.reg_b = self.reg_b ^ operand
    
    def bst(self, operand):
        self.reg_b = self.combo(operand) % 8

    def jnz(self, operand):
        if self.reg_a == 0:
            self.ip += 2
        else:
            self.ip = operand
    
    def bxc(self, operand):
        self.reg_b = self.reg_b ^ self.reg_c

    def out(self, operand):
        self.output += ("," if len(self.output) > 0 else "") + str(self.combo(operand)%8)
        self.output_list.append(self.combo(operand)%8)
    
    def bdy(self, operand):
        self.reg_b = self.reg_a//pow(2, self.combo(operand))
    
    def cdv(self, operand):
        self.reg_c = self.reg_a//pow(2, self.combo(operand))

def compute_part_1(input_file_name="input.txt"):
    input = read_input(input_file_name)
    registers = [[int(x) for x in re.findall(r"\d+", line)][0] for line in input if "Register" in line]
    program = [[int(x) for x in re.findall(r"\d+", line)] for line in input if "Program" in line][0]
    computer = Computer(registers, program)
    computer.run()
    return computer.output

# 2,1,4,0,7,4,0,2,3
# That's the right answer! You are one gold star closer to finding the Chief 
# Historian.

# --- Part Two ---
# Digging deeper in the device's manual, you discover the problem: this 
# program is supposed to output another copy of the program! Unfortunately, 
# the value in register A seems to have been corrupted. You'll need to find a 
# new value to which you can initialize register A so that the program's 
# output instructions produce an exact copy of the program itself.

# For example:

# Register A: 2024
# Register B: 0
# Register C: 0

# Program: 0,3,5,4,3,0

# This program outputs a copy of itself if register A is instead initialized 
# to 117440. (The original initial value of register A, 2024, is ignored.)

# What is the lowest positive initial value for register A that causes the 
# program to output a copy of itself?

def compute_part_2(input_file_name="input.txt"):
    input = read_input(input_file_name)
    registers = [[int(x) for x in re.findall(r"\d+", line)][0] for line in input if "Register" in line]
    program = [[int(x) for x in re.findall(r"\d+", line)] for line in input if "Program" in line][0]
    reg_a = 0 # Insight: If reg_a increases, so does the length of the output
    n_correct_digits = 0
    while True:
        computer = Computer(registers, program)
        computer.reg_a = reg_a
        computer.run()
        if computer.output_list == program:
            return reg_a
        if computer.output_list[-(n_correct_digits+1):] == program[-(n_correct_digits+1):]:
            print(f"{reg_a}: {computer.output_list} vs {program}")
            reg_a *= 8 # Insight: If all digits match, we can safely multiply by 8
            n_correct_digits += 1
        else:
            reg_a += 1

# 258394985014171
# That's the right answer! You are one gold star closer to finding the Chief 
# Historian.

if __name__ == "__main__":
    print(f"PART 1: {compute_part_1()}")
    print(f"PART 2: {compute_part_2()}")