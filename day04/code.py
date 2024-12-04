import os.path


def read_input(input_file_name):
    input_file = os.path.join(os.path.dirname(__file__), input_file_name)
    with open(input_file, "r") as f:
        lines = f.readlines()
        return lines


# --- Day 4: Ceres Search ---
# "Looks like the Chief's not here. Next!" One of The Historians pulls out a 
# device and pushes the only button on it. After a brief flash, you recognize 
# the interior of the Ceres monitoring station!

# As the search for the Chief continues, a small Elf who lives on the station 
# tugs on your shirt; she'd like to know if you could help her with her word 
# search (your puzzle input). She only has to find one word: XMAS.

# This word search allows words to be horizontal, vertical, diagonal, written 
# backwards, or even overlapping other words. It's a little unusual, though, 
# as you don't merely need to find one instance of XMAS - you need to find 
# all of them. Here are a few ways XMAS might appear, where irrelevant 
# characters have been replaced with .:


# ..X...
# .SAMX.
# .A..A.
# XMAS.S
# .X....

# The actual word search will be full of letters instead. For example:

# MMMSXXMASM
# MSAMXMSMSA
# AMXSXMAAMM
# MSAMASMSMX
# XMASAMXAMM
# XXAMMXXAMA
# SMSMSASXSS
# SAXAMASAAA
# MAMMMXMMMM
# MXMXAXMASX

# In this word search, XMAS occurs a total of 18 times; here's the same word search again, but where letters not involved in any XMAS have been replaced with .:

# ....XXMAS.
# .SAMXMS...
# ...S..A...
# ..A.A.MS.X
# XMASAMX.MM
# X.....XA.A
# S.S.S.S.SS
# .A.A.A.A.A
# ..M.M.M.MM
# .X.X.XMASX

# Take a look at the little Elf's word search. How many times does XMAS appear?

def compute_part_1(input_file_name="input.txt"):
    input = read_input(input_file_name)
    input = [line.replace("\n", "") for line in input]
    n = len(input[0]) # width
    m = len(input) # height
    horizontal = ["".join(line) for line in input]
    vertical = ["".join([line[i] for line in input]) for i in range(m)]
    diagonal_1 = ["".join([input[k-i][i] for i in range(k+1)]) for k in range(0, m)] \
        + ["".join([input[m-i-1][n-k+i-1] for i in range(k+1)]) for k in range(0, m-1)]
    diagonal_2 = ["".join([input[m-i-1][k-i] for i in range(k+1)]) for k in range(0, m)] \
        + ["".join([input[k-i][n-i-1] for i in range(k+1)]) for k in range(0, m-1)]
    all = horizontal + vertical + diagonal_1 + diagonal_2
    # print(f"Horizontal: {horizontal}")
    # print(f"Vertical: {vertical}")
    # print(f"Diagonal_1: {diagonal_1}")
    # print(f"Diagonal_2: {diagonal_2}")
    # print(f"All: {all}")
    return sum([line.count("XMAS") + line.count("SAMX") for line in all])

# 2567
# That's the right answer! You are one gold star closer to finding the Chief 
# Historian.

# --- Part Two ---
#The Elf looks quizzically at you. Did you misunderstand the assignment?

#Looking for the instructions, you flip over the word search to find that 
# this isn't actually an XMAS puzzle; it's an X-MAS puzzle in which you're 
# supposed to find two MAS in the shape of an X. One way to achieve that is 
# like this:

# M.S
# .A.
# M.S

# Irrelevant characters have again been replaced with . in the above diagram. 
# Within the X, each MAS can be written forwards or backwards.

# Here's the same example from before, but this time all of the X-MASes have 
# been kept instead:

# .M.S......
# ..A..MSMS.
# .M.S.MAA..
# ..A.ASMSM.
# .M.S.M....
# ..........
# S.S.S.S.S.
# .A.A.A.A..
# M.M.M.M.M.

# ..........

# In this example, an X-MAS appears 9 times.

# Flip the word search from the instructions back over to the word search 
# side and try again. How many times does an X-MAS appear?

def compute_part_2(input_file_name="input.txt"):
    input = read_input(input_file_name)
    input = [line.replace("\n", "") for line in input]
    n = len(input[0]) # width
    m = len(input) # height
    crosses = [(["".join([input[i][j], input[i+1][j+1], input[i+2][j+2], input[i+2][j], input[i+1][j+1], input[i][j+2]]) for i in range(n-2)]) for j in range(m-2)]
    return sum([cross.count("MASMAS") + cross.count("MASSAM") + cross.count("SAMMAS") + cross.count("SAMSAM") for cross in crosses])

# 2029
# That's the right answer! You are one gold star closer to finding the Chief 
# Historian.

if __name__ == "__main__":
    print(f"PART 1: {compute_part_1()}")
    print(f"PART 2: {compute_part_2()}")
