import os.path
import re
from scipy.optimize import linprog


def read_input(input_file_name):
    input_file = os.path.join(os.path.dirname(__file__), input_file_name)
    with open(input_file, "r") as f:
        lines = f.readlines()
        return lines

# --- Day 13: Claw Contraption ---

# Next up: the lobby of a resort on a tropical island. The Historians take a 
# moment to admire the hexagonal floor tiles before spreading out.

# Fortunately, it looks like the resort has a new arcade! Maybe you can win 
# some prizes from the claw machines?

# The claw machines here are a little unusual. Instead of a joystick or 
# directional buttons to control the claw, these machines have two buttons 
# labeled A and B. Worse, you can't just put in a token and play; it costs 3 
# tokens to push the A button and 1 token to push the B button.

# With a little experimentation, you figure out that each machine's buttons 
# are configured to move the claw a specific amount to the right (along the 
# X axis) and a specific amount forward (along the Y axis) each time that 
# button is pressed.

# Each machine contains one prize; to win the prize, the claw must be 
# positioned exactly above the prize on both the X and Y axes.

# You wonder: what is the smallest number of tokens you would have to spend 
# to win as many prizes as possible? You assemble a list of every machine's 
# button behavior and prize location (your puzzle input). For example:

# Button A: X+94, Y+34
# Button B: X+22, Y+67
# Prize: X=8400, Y=5400

# Button A: X+26, Y+66
# Button B: X+67, Y+21
# Prize: X=12748, Y=12176

# Button A: X+17, Y+86
# Button B: X+84, Y+37
# Prize: X=7870, Y=6450

# Button A: X+69, Y+23
# Button B: X+27, Y+71
# Prize: X=18641, Y=10279

# This list describes the button configuration and prize location of four 
# different claw machines.

# For now, consider just the first claw machine in the list:

# - Pushing the machine's A button would move the claw 94 units along the 
#   X axis and 34 units along the Y axis.
# - Pushing the B button would move the claw 22 units along the X axis and 
#   67 units along the Y axis.
# - The prize is located at X=8400, Y=5400; this means that from the 
#   claw's initial position, it would need to move exactly 8400 units 
#   along the X axis and exactly 5400 units along the Y axis to be 
#   perfectly aligned with the prize in this machine.

# The cheapest way to win the prize is by pushing the A button 80 times and 
# the B button 40 times. This would line up the claw along the X axis 
# (because 80*94 + 40*22 = 8400) and along the Y axis (because 
# 80*34 + 40*67 = 5400). Doing this would cost 80*3 tokens for the A presses 
# and 40*1 for the B presses, a total of 280 tokens.

# For the second and fourth claw machines, there is no combination of A and B 
# presses that will ever win a prize.

# For the third claw machine, the cheapest way to win the prize is by pushing 
# the A button 38 times and the B button 86 times. Doing this would cost a 
# total of 200 tokens.

# So, the most prizes you could possibly win is two; the minimum tokens you 
# would have to spend to win all (two) prizes is 480.

# You estimate that each button would need to be pressed no more than 100 
# times to win a prize. How else would someone be expected to play?

# Figure out how to win as many prizes as possible. What is the fewest tokens 
# you would have to spend to win all possible prizes?

def brute_force(button_a, button_b, prize, limit):
    min_tokens = 4 * limit + 1
    for i in range(limit):
        for j in range(limit):
            if i * button_a[0] + j * button_b[0] == prize[0] and i * button_a[1] + j * button_b[1] == prize[1]:
                min_tokens = min(min_tokens, 3*i+j)
    return min_tokens

def compute_part_1(input_file_name="input.txt"):
    input = read_input(input_file_name)
    numbers = [[int(x) for x in re.findall(r"\d+", line)] for line in input if line != '\n']
    limit = 100
    sum_tokens = 0
    while(len(numbers) > 0):
        button_a = numbers.pop(0)
        button_b = numbers.pop(0)
        prize = numbers.pop(0)
        tokens = brute_force(button_a, button_b, prize, limit)
        sum_tokens += tokens if tokens < 4 * limit + 1 else 0
    return sum_tokens

# 34787
# That's the right answer! You are one gold star closer to finding the Chief 
# Historian.

# --- Part Two ---
# As you go to win the first prize, you discover that the claw is nowhere 
# near where you expected it would be. Due to a unit conversion error in your 
# measurements, the position of every prize is actually 10000000000000 
# higher on both the X and Y axis!

# Add 10000000000000 to the X and Y position of every prize. After making 
# this change, the example above would now look like this:

# Button A: X+94, Y+34
# Button B: X+22, Y+67
# Prize: X=10000000008400, Y=10000000005400

# Button A: X+26, Y+66
# Button B: X+67, Y+21
# Prize: X=10000000012748, Y=10000000012176

# Button A: X+17, Y+86
# Button B: X+84, Y+37
# Prize: X=10000000007870, Y=10000000006450

# Button A: X+69, Y+23
# Button B: X+27, Y+71
# Prize: X=10000000018641, Y=10000000010279

# Now, it is only possible to win a prize on the second and fourth claw 
# machines. Unfortunately, it will take many more than 100 presses to do so.

# Using the corrected prize coordinates, figure out how to win as many prizes 
# as possible. What is the fewest tokens you would have to spend to win all 
# possible prizes?

def compute_part_2(input_file_name="input.txt"):
    input = read_input(input_file_name)
    numbers = [[int(x) for x in re.findall(r"\d+", line)] for line in input if line != '\n']
    sum_tokens = 0
    while(len(numbers) > 0):
        a = numbers.pop(0)
        b = numbers.pop(0)
        p = numbers.pop(0)
        p[0] += 10000000000000
        p[1] += 10000000000000
        # i*a[0] + j*b[0] = p[0]
        # <=> i = (p[0] - j*b[0])/a[0]
        # i*a[1] + j*b[1] = p[1]
        # => (p[0] - j*b[0])/a[0] * a[1] + j*b[1] = p[1]
        # <=> ...
        # <=> j = (p[1]*a[0] - a[1]*p[0])/(b[1]*a[0] - a[1]*b[0])
        j = (p[1]*a[0] - a[1]*p[0])/(b[1]*a[0] - a[1]*b[0])
        i = (p[0] - j*b[0])/a[0]
        if int(i) == i and int(j) == j:
            sum_tokens += 3*int(i)+int(j)
    return sum_tokens

# 85644161121698
# That's the right answer! You are one gold star closer to finding the Chief 
# Historian.

if __name__ == "__main__":
    print(f"PART 1: {compute_part_1()}")
    print(f"PART 2: {compute_part_2()}")

# Linear Program (leads to floating point errors):
# Constraint 1: i*button_a[0] + j*button_b[0] = prize[0]
# Constraint 2: i*button_a[1] + j*button_b[1] = prize[1]
# Objective Function Coefficients: 3i + j => [3,1]
# A_eq = [
#     [button_a[0], button_b[0]],  # Coefficients for the first constraint
#     [button_a[1], button_b[1]]   # Coefficients for the second constraint
# ]
# b_eq = prize # Right-hand side values for the equality constraints
# Solve linear program
# result = linprog([3, 1], A_eq=A_eq, b_eq=b_eq, method='highs', integrality=[1,1])
# if result.success:
#     sum_tokens += 3*int(result.x[0]) + int(result.x[1])