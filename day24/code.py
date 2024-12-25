import os.path
import re


def read_input(input_file_name):
    input_file = os.path.join(os.path.dirname(__file__), input_file_name)
    with open(input_file, "r") as f:
        lines = f.readlines()
        return lines

# --- Day 24: Crossed Wires ---

# You and The Historians arrive at the edge of a large grove somewhere in the 
# jungle. After the last incident, the Elves installed a small device that 
# monitors the fruit. While The Historians search the grove, one of them asks 
# if you can take a look at the monitoring device; apparently, it's been 
# malfunctioning recently.

# The device seems to be trying to produce a number through some boolean 
# logic gates. Each gate has two inputs and one output. The gates all operate 
# on values that are either true (1) or false (0).

# - AND gates output 1 if both inputs are 1; if either input is 0, 
#   these gates output 0.
# - OR gates output 1 if one or both inputs is 1; if both inputs are 0, 
#   these gates output 0.
# - XOR gates output 1 if the inputs are different; if the inputs are the 
#   same, these gates output 0.

# Gates wait until both inputs are received before producing output; wires 
# can carry 0, 1 or no value at all. There are no loops; once a gate has 
# determined its output, the output will not change until the whole system is 
# reset. Each wire is connected to at most one gate output, but can be 
# connected to many gate inputs.

# Rather than risk getting shocked while tinkering with the live system, you 
# write down all of the gate connections and initial wire values (your puzzle 
# input) so you can consider them in relative safety. For example:

# x00: 1
# x01: 1
# x02: 1
# y00: 0
# y01: 1
# y02: 0

# x00 AND y00 -> z00
# x01 XOR y01 -> z01
# x02 OR y02 -> z02

# Because gates wait for input, some wires need to start with a value (as 
# inputs to the entire system). The first section specifies these values. For 
# example, x00: 1 means that the wire named x00 starts with the value 1 (as 
# if a gate is already outputting that value onto that wire).

# The second section lists all of the gates and the wires connected to them. 
# For example, x00 AND y00 -> z00 describes an instance of an AND gate which 
# has wires x00 and y00 connected to its inputs and which will write its 
# output to wire z00.

# In this example, simulating these gates eventually causes 0 to appear on 
# wire z00, 0 to appear on wire z01, and 1 to appear on wire z02.

# Ultimately, the system is trying to produce a number by combining the bits 
# on all wires starting with z. z00 is the least significant bit, then z01, 
# then z02, and so on.

# In this example, the three output bits form the binary number 100 which is 
# equal to the decimal number 4.

# Here's a larger example:

# x00: 1
# x01: 0
# x02: 1
# x03: 1
# x04: 0
# y00: 1
# y01: 1
# y02: 1
# y03: 1
# y04: 1

# ntg XOR fgs -> mjb
# y02 OR x01 -> tnw
# kwq OR kpj -> z05
# x00 OR x03 -> fst
# tgd XOR rvg -> z01
# vdt OR tnw -> bfw
# bfw AND frj -> z10
# ffh OR nrd -> bqk
# y00 AND y03 -> djm
# y03 OR y00 -> psh
# bqk OR frj -> z08
# tnw OR fst -> frj
# gnj AND tgd -> z11
# bfw XOR mjb -> z00
# x03 OR x00 -> vdt
# gnj AND wpb -> z02
# x04 AND y00 -> kjc
# djm OR pbm -> qhw
# nrd AND vdt -> hwm
# kjc AND fst -> rvg
# y04 OR y02 -> fgs
# y01 AND x02 -> pbm
# ntg OR kjc -> kwq
# psh XOR fgs -> tgd
# qhw XOR tgd -> z09
# pbm OR djm -> kpj
# x03 XOR y03 -> ffh
# x00 XOR y04 -> ntg
# bfw OR bqk -> z06
# nrd XOR fgs -> wpb
# frj XOR qhw -> z04
# bqk OR frj -> z07
# y03 OR x01 -> nrd
# hwm AND bqk -> z03
# tgd XOR rvg -> z12
# tnw OR pbm -> gnj

# After waiting for values on all wires starting with z, the wires in this 
# system have the following values:

# bfw: 1
# bqk: 1
# djm: 1
# ffh: 0
# fgs: 1
# frj: 1
# fst: 1
# gnj: 1
# hwm: 1
# kjc: 0
# kpj: 1
# kwq: 0
# mjb: 1
# nrd: 1
# ntg: 0
# pbm: 1
# psh: 1
# qhw: 1
# rvg: 0
# tgd: 0
# tnw: 1
# vdt: 1
# wpb: 0
# z00: 0
# z01: 0
# z02: 0
# z03: 1
# z04: 0
# z05: 1
# z06: 1
# z07: 1
# z08: 1
# z09: 1
# z10: 1
# z11: 0
# z12: 0

# Combining the bits from all wires starting with z produces the binary 
# number 0011111101000. Converting this number to decimal produces 2024.

# Simulate the system of gates and wires. What decimal number does it output 
# on the wires starting with z?

class Gate:
    
    def __init__(self, type, i1_name, i2_name, o_name):
        self.type = type
        self.i1_name = i1_name
        self.i2_name = i2_name
        self.o_name = o_name
        self.i1 = None
        self.i2 = None
    
    def __str__(self):
        return f"Gate {self.i1_name} {self.type} {self.i2_name} -> {self.o_name}"
    
    def __repr__(self):
        return f"Gate {self.i1_name} {self.type} {self.i2_name} -> {self.o_name}"

    def set_value(self, name, val):
        if name == self.i1_name:
            self.i1 = val
        if name == self.i2_name:
            self.i2 = val
    
    def check_ready(self):
        return self.i1 != None and self.i2 != None
    
    def evaluate(self):
        match self.type:
            case "AND":
                return self.i1 and self.i2
            case "OR":
                return self.i1 or self.i2
            case "XOR":
                return self.i1 != self.i2

def parse_input(input):
    values = {}
    gates = []
    for line in input:
        if ':' in line:
            values[line[0:3]] = True if ': 1' in line else False
        elif '->' in line:
            i1_name, type, i2_name, o_name = re.match(r"(\w+)\s+(XOR|AND|OR)\s+(\w+)\s+->\s+(\w+)", line).groups()
            gates.append(Gate(type, i1_name, i2_name, o_name))
    return values, gates

def compute_part_1(input_file_name="input.txt"):
    input = read_input(input_file_name)
    values, gates = parse_input(input)
    while(len(gates)) > 0:
        for gate in gates:
            for val in [gate.i1_name, gate.i2_name]:
                if val in values.keys():
                    gate.set_value(val, values[val])
            if gate.check_ready():
                values[gate.o_name] = gate.evaluate()
                # print(f"{gate.o_name}: {values[gate.o_name]}")
                gates.remove(gate)
    z_val_names = sorted([key for key in values.keys() if key[0] == 'z'], reverse=True)
    return int("".join([('1' if values[z_val_name] else '0') for z_val_name in z_val_names]), 2)

# 57588078076750
# That's the right answer! You are one gold star closer to finding the Chief 
# Historian.

# --- Part Two ---

# After inspecting the monitoring device more closely, you determine that the 
# system you're simulating is trying to add two binary numbers.

# Specifically, it is treating the bits on wires starting with x as one 
# binary number, treating the bits on wires starting with y as a second 
# binary number, and then attempting to add those two numbers together. The 
# output of this operation is produced as a binary number on the wires 
# starting with z. (In all three cases, wire 00 is the least significant 
# bit, then 01, then 02, and so on.)

# The initial values for the wires in your puzzle input represent just one 
# instance of a pair of numbers that sum to the wrong value. Ultimately, any 
# two binary numbers provided as input should be handled correctly. That is, 
# for any combination of bits on wires starting with x and wires starting 
# with y, the sum of the two numbers those bits represent should be produced 
# as a binary number on the wires starting with z.

# For example, if you have an addition system with four x wires, four y 
# wires, and five z wires, you should be able to supply any four-bit number 
# on the x wires, any four-bit number on the y numbers, and eventually find 
# the sum of those two numbers as a five-bit number on the z wires. One of 
# the many ways you could provide numbers to such a system would be to pass 
# 11 on the x wires (1011 in binary) and 13 on the y wires (1101 in binary):

# x00: 1
# x01: 1
# x02: 0
# x03: 1
# y00: 1
# y01: 0
# y02: 1
# y03: 1

# If the system were working correctly, then after all gates are finished 
# processing, you should find 24 (11+13) on the z wires as the five-bit 
# binary number 11000:

# z00: 0
# z01: 0
# z02: 0
# z03: 1
# z04: 1

# Unfortunately, your actual system needs to add numbers with many more bits 
# and therefore has many more wires.

# Based on forensic analysis of scuff marks and scratches on the device, you 
# can tell that there are exactly four pairs of gates whose output wires 
# have been swapped. (A gate can only be in at most one such pair; no gate's 
# output was swapped multiple times.)

# For example, the system below is supposed to find the bitwise AND of the 
# six-bit number on x00 through x05 and the six-bit number on y00 through 
# y05 and then write the result as a six-bit number on z00 through z05:

# x00: 0
# x01: 1
# x02: 0
# x03: 1
# x04: 0
# x05: 1
# y00: 0
# y01: 0
# y02: 1
# y03: 1
# y04: 0
# y05: 1

# x00 AND y00 -> z05
# x01 AND y01 -> z02
# x02 AND y02 -> z01
# x03 AND y03 -> z03
# x04 AND y04 -> z04
# x05 AND y05 -> z00

# However, in this example, two pairs of gates have had their output wires 
# swapped, causing the system to produce wrong answers. The first pair of 
# gates with swapped outputs is x00 AND y00 -> z05 and x05 AND y05 -> z00; 
# the second pair of gates is x01 AND y01 -> z02 and x02 AND y02 -> z01. 
# Correcting these two swaps results in this system that works as intended 
# for any set of initial values on wires that start with x or y:

# x00 AND y00 -> z00
# x01 AND y01 -> z01
# x02 AND y02 -> z02
# x03 AND y03 -> z03
# x04 AND y04 -> z04
# x05 AND y05 -> z05

# In this example, two pairs of gates have outputs that are involved in a 
# swap. By sorting their output wires' names and joining them with commas, 
# the list of wires involved in swaps is z00,z01,z02,z05.

# Of course, your actual system is much more complex than this, and the gates 
# that need their outputs swapped could be anywhere, not just attached to a 
# wire starting with z. If you were to determine that you need to swap output 
# wires aaa with eee, ooo with z99, bbb with ccc, and aoc with z24, your 
# answer would be aaa,aoc,bbb,ccc,eee,ooo,z24,z99.

# Your system of gates and wires has four pairs of gates which need their 
# output wires swapped - eight wires in total. Determine which four pairs of 
# gates need their outputs swapped so that your system correctly performs 
# addition; what do you get if you sort the names of the eight wires involved 
# in a swap and then join those names with commas?

def evaluate_gates(values, gates):
    while(len(gates)) > 0:
        len_gates = len(gates)
        for gate in gates:
            for val in [gate.i1_name, gate.i2_name]:
                if val in values.keys():
                    gate.set_value(val, values[val])
            if gate.check_ready():
                values[gate.o_name] = gate.evaluate()
                # print(f"{gate.o_name}: {values[gate.o_name]}")
                gates.remove(gate)
        if len(gates) == len_gates:
            return values
    return values

def check_addition(values):
    x_val_names = sorted([key for key in values.keys() if key[0] == 'x'], reverse=True)
    x = int("".join([('1' if values[x_val_name] else '0') for x_val_name in x_val_names]), 2)
    y_val_names = sorted([key for key in values.keys() if key[0] == 'y'], reverse=True)
    y = int("".join([('1' if values[y_val_name] else '0') for y_val_name in y_val_names]), 2)
    z_val_names = sorted([key for key in values.keys() if key[0] == 'z'], reverse=True)
    z = int("".join([('1' if values[z_val_name] else '0') for z_val_name in z_val_names]), 2) if len(z_val_names) > 0 else 0
    # print(f"Expected: {x} + {y} = {x+y} | Actual: {x} + {y} = {z}")
    return x + y == z

def reset(gates):
    for gate in gates:
        gate.i1 = None
        gate.i2 = None

def test_fix_gate_combinations(values, gates, potentially_faulty_gates):
    if len(potentially_faulty_gates) == 0:
        out = check_addition(evaluate_gates(values.copy(), gates.copy()))
        reset(gates)
        return out
    else:
        for i in range(len(potentially_faulty_gates)):
            for j in range(i+1, len(potentially_faulty_gates)):
                gi = potentially_faulty_gates[i]
                gj = potentially_faulty_gates[j]
                gi.o_name, gj.o_name = gj.o_name, gi.o_name
                # Check rules for potentially early abortion
                if check_rule_1(gi) or check_rule_1(gj) or check_rule_2(gi) or check_rule_2(gj):
                    gj.o_name, gi.o_name = gi.o_name, gj.o_name
                    continue
                pfg = potentially_faulty_gates.copy()
                pfg.remove(gi)
                pfg.remove(gj)
                if test_fix_gate_combinations(values, gates, pfg):
                    return True
                gj.o_name, gi.o_name = gi.o_name, gj.o_name
    return False

def check_rule_1(gate): # returns True in case of rule violation
    return gate.o_name[0] == 'z' and gate.type != "XOR" and gate.o_name != "z45"

def check_rule_2(gate): # returns True in case of rule violation
    return gate.o_name[0] != 'z' and ((gate.i1_name[0]+gate.i2_name[0]) not in ["xy", "yx"]) and gate.type == "XOR"

def compute_part_2(input_file_name="input.txt"):
    input = read_input(input_file_name)
    values, gates = parse_input(input)
    # Rules for finding errors (based on how a Ripple Carry Adder is supposed to work):
    # - If a gate outputs z.., then the operation has to be XOR unless it is the last bit.
    # - If a gate does not output z.. and the inputs are not x.. and y.. then it has to be AND / OR, but not XOR.
    faulty_gates_rule_1 = []
    faulty_gates_rule_2 = []
    remaining_gates = []
    for gate in gates:
        if check_rule_1(gate):
            faulty_gates_rule_1.append(gate)
        elif check_rule_2(gate):
            faulty_gates_rule_2.append(gate)
        else:
            remaining_gates.append(gate)
    # This produces 6 faulty gates
    # For any reminding errors, we use brute force
    for i in range(len(remaining_gates)):
        for j in range(len(remaining_gates)):
            potentially_faulty_gates = faulty_gates_rule_1 + faulty_gates_rule_2 + [remaining_gates[i], remaining_gates[j]]
            print(f"{i*len(remaining_gates) + j}/{len(remaining_gates)*len(remaining_gates)//2}") # Result found at i*n_gates + j = 1016
            if test_fix_gate_combinations(values, gates, potentially_faulty_gates):
                return "".join(sorted([gate.o_name + ',' for gate in potentially_faulty_gates]))[:-1]
    return 0

# kcd,pfn,shj,tpk,wkb,z07,z23,z27
# That's the right answer! You are one gold star closer to finding the Chief 
# Historian.

if __name__ == "__main__":
    print(f"PART 1: {compute_part_1()}")
    print(f"PART 2: {compute_part_2()}")
