import os.path
import re


def read_input(input_file_name):
    input_file = os.path.join(os.path.dirname(__file__), input_file_name)
    with open(input_file, "r") as f:
        lines = f.readlines()
        return lines
    

# --- Day 3: Mull It Over ---
# "Our computers are having issues, so I have no idea if we have any Chief 
# Historians in stock! You're welcome to check the warehouse, though," says 
# the mildly flustered shopkeeper at the North Pole Toboggan Rental Shop. 
# The Historians head out to take a look.

# The shopkeeper turns to you. "Any chance you can see why our computers 
# are having issues again?"

# The computer appears to be trying to run a program, but its memory (your 
# puzzle input) is corrupted. All of the instructions have been jumbled up!

# It seems like the goal of the program is just to multiply some numbers. It 
# does that with instructions like mul(X,Y), where X and Y are each 1-3 
# digit numbers. For instance, mul(44,46) multiplies 44 by 46 to get a 
# result of 2024. Similarly, mul(123,4) would multiply 123 by 4.

# However, because the program's memory has been corrupted, there are also 
# many invalid characters that should be ignored, even if they look like 
# part of a mul instruction. Sequences like mul(4*, mul(6,9!, ?(12,34), or 
# mul ( 2 , 4 ) do nothing.

# For example, consider the following section of corrupted memory:

# x*mul(2,4)*%&mul[3,7]!@^do_not_*mul(5,5)*+mul(32,64]then(*mul(11,8)**mul(8,5)*)

# Only the four with * highlighted sections are real mul instructions. Adding up 
# the result of each instruction produces 161 (2*4 + 5*5 + 11*8 + 8*5).

# Scan the corrupted memory for uncorrupted mul instructions. What do you get if you 
# add up all of the results of the multiplications?

def eval_multiplication(mul):
    numbers = [int(x) for x in re.findall(r"\d{1,3}", mul)]
    if len(numbers) != 2:
        exit(f"Issue: Found more numbers than expected in mul {mul}: {numbers}")
    return numbers[0] * numbers[1]

def compute_part_1(input_file_name="input.txt"):
    input = "".join(read_input(input_file_name)).replace('\n', ' ')
    multiplications = [x for x in re.findall(r"mul\(\d{1,3}\,\d{1,3}\)", input)]
    return sum([eval_multiplication(mul) for mul in multiplications])

# 170068701

# That's the right answer! You are one gold star closer to finding the Chief 
# Historian.

# --- Part Two ---
# As you scan through the corrupted memory, you notice that some of the 
# conditional statements are also still intact. If you handle some of the 
# uncorrupted conditional statements in the program, you might be able to get 
# an even more accurate result.

# There are two new instructions you'll need to handle:
# - The do() instruction enables future mul instructions.
# - The don't() instruction disables future mul instructions.

# Only the most recent do() or don't() instruction applies. At the beginning 
# of the program, mul instructions are enabled.

# For example:
# x*mul(2,4)*&mul[3,7]!^*don't*()_mul(5,5)+mul(32,64](mul(11,8)un*do()*?*mul(8,5)*)

# This corrupted memory is similar to the example from before, but this time 
# the mul(5,5) and mul(11,8) instructions are disabled because there is a 
# don't() instruction before them. The other mul instructions function 
# normally, including the one at the end that gets re-enabled by a do() 
# instruction.

# This time, the sum of the results is 48 (2*4 + 8*5).

# Handle the new instructions; what do you get if you add up all of the 
# results of just the enabled multiplications?

def compute_part_2(input_file_name="input.txt"):
    input = "".join(read_input(input_file_name)).replace('\n', ' ')
    do_input = [x for x in re.findall(r"do\(\)(.*?)don\'t\(\)", "do()" + input + "don't()")] # need the ? for lazy fetch and () for not matching the do()/don't()
    multiplications = [[x for x in re.findall(r"mul\(\d{1,3}\,\d{1,3}\)", line)] for line in do_input]
    return sum([sum([eval_multiplication(mul) for mul in line]) for line in multiplications])

# 78683433

# That's the right answer! You are one gold star closer to finding the Chief 
# Historian.

if __name__ == "__main__":
    print(f"PART 1: {compute_part_1()}")
    print(f"PART 2: {compute_part_2()}")