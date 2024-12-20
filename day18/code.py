import os.path
import re


def read_input(input_file_name):
    input_file = os.path.join(os.path.dirname(__file__), input_file_name)
    with open(input_file, "r") as f:
        lines = f.readlines()
        return lines

# --- Day 18: RAM Run ---

# You and The Historians look a lot more pixelated than you remember. You're 
# inside a computer at the North Pole!

# Just as you're about to check out your surroundings, a program runs up to 
# you. "This region of memory isn't safe! The User misunderstood what a 
# pushdown automaton is and their algorithm is pushing whole bytes down on 
# top of us! Run!"

# The algorithm is fast - it's going to cause a byte to fall into your memory 
# space once every nanosecond! Fortunately, you're faster, and by quickly 
# scanning the algorithm, you create a list of which bytes will fall (your 
# puzzle input) in the order they'll land in your memory space.

# Your memory space is a two-dimensional grid with coordinates that range 
# from 0 to 70 both horizontally and vertically. However, for the sake of 
# example, suppose you're on a smaller grid with coordinates that range from 
# 0 to 6 and the following list of incoming byte positions:

# 5,4
# 4,2
# 4,5
# 3,0
# 2,1
# 6,3
# 2,4
# 1,5
# 0,6
# 3,3
# 2,6
# 5,1
# 1,2
# 5,5
# 2,5
# 6,5
# 1,4
# 0,4
# 6,4
# 1,1
# 6,1
# 1,0
# 0,5
# 1,6
# 2,0

# Each byte position is given as an X,Y coordinate, where X is the distance 
# from the left edge of your memory space and Y is the distance from the top 
# edge of your memory space.

# You and The Historians are currently in the top left corner of the memory 
# space (at 0,0) and need to reach the exit in the bottom right corner (at 
# 70,70 in your memory space, but at 6,6 in this example). You'll need to 
# simulate the falling bytes to plan out where it will be safe to run; for 
# now, simulate just the first few bytes falling into your memory space.

# As bytes fall into your memory space, they make that coordinate corrupted. 
# Corrupted memory coordinates cannot be entered by you or The Historians, so 
# you'll need to plan your route carefully. You also cannot leave the 
# boundaries of the memory space; your only hope is to reach the exit.

# In the above example, if you were to draw the memory space after the first 
# 12 bytes have fallen (using . for safe and # for corrupted), it would look 
# like this:

# ...#...
# ..#..#.
# ....#..
# ...#..#
# ..#..#.
# .#..#..
# #.#....

# You can take steps up, down, left, or right. After just 12 bytes have 
# corrupted locations in your memory space, the shortest path from the top 
# left corner to the exit would take 22 steps. Here (marked with O) is one 
# such path:

# OO.#OOO
# .O#OO#O
# .OOO#OO
# ...#OO#
# ..#OO#.
# .#.O#..
# #.#OOOO

# Simulate the first kilobyte (1024 bytes) falling onto your memory space. 
# Afterward, what is the minimum number of steps needed to reach the exit?

def print_memory(memory):
    for line in memory:
        print("".join(line))
    print()

def get_neighbors(x, y, memory):
    return [(xx, yy) for (xx, yy) in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)] if yy >= 0 and yy < len(memory) and xx >= 0 and xx < len(memory[yy])]

def shortest_path(sx, sy, tx, ty, memory):
    queue = [(sx, sy)]
    dist = {
        (sx, sy) : 0
    }
    while(len(queue) > 0):
        (x, y) = queue.pop(0)
        for xx, yy in get_neighbors(x, y, memory):
            if (xx, yy) in dist:
                continue
            if memory[xx][yy] == '.':
                dist[(xx, yy)] = dist[(x, y)] + 1
                queue.append((xx, yy))
    return dist[(tx, ty)] if (tx, ty) in dist else -1
        
def size_2_list_to_pair(size_2_list):
    if len(size_2_list) != 2:
        exit(f"Tried transforming list {size_2_list} of size {len(size_2_list)} to pair.")
    return (size_2_list[0], size_2_list[1])

def compute_part_1(input_file_name="input.txt"):
    input = read_input(input_file_name)
    bytes = [size_2_list_to_pair([int(x) for x in re.findall(r"\d+", line)]) for line in input][:1024]
    grid_size = 71
    memory = [['#' if (x, y) in bytes else '.' for x in range(grid_size)] for y in range(grid_size)]
    return shortest_path(0, 0, grid_size-1, grid_size-1, memory)

# 264
# That's the right answer! You are one gold star closer to finding the Chief 
# Historian.

# --- Part Two ---
# The Historians aren't as used to moving around in this pixelated universe 
# as you are. You're afraid they're not going to be fast enough to make it to 
# the exit before the path is completely blocked.

# To determine how fast everyone needs to go, you need to determine the first 
# byte that will cut off the path to the exit.

# In the above example, after the byte at 1,1 falls, there is still a path to 
# the exit:

# O..#OOO
# O##OO#O
# O#OO#OO
# OOO#OO#
# ###OO##
# .##O###
# #.#OOOO

# However, after adding the very next byte (at 6,1), there is no longer a path to the exit:

# ...#...
# .##..##
# .#..#..
# ...#..#
# ###..##
# .##.###
# #.#....

# So, in this example, the coordinates of the first byte that prevents the 
# exit from being reachable are 6,1.

# Simulate more of the bytes that are about to corrupt your memory space. 
# What are the coordinates of the first byte that will prevent the exit from 
# being reachable from your starting position? (Provide the answer as two 
# integers separated by a comma with no other characters.)

def compute_part_2(input_file_name="input.txt"):
    input = read_input(input_file_name)
    bytes = [size_2_list_to_pair([int(x) for x in re.findall(r"\d+", line)]) for line in input]
    grid_size = 71
    memory = [['#' if (x, y) in bytes[:1024] else '.' for x in range(grid_size)] for y in range(grid_size)]
    print_memory(memory)
    for i in range(1024, len(bytes)):
        memory[bytes[i][1]][bytes[i][0]] = '#'
        # print(f"Simulating byte {i}: {bytes[i]}")
        shortest_path_length = shortest_path(0, 0, grid_size-1, grid_size-1, memory)
        if shortest_path_length == -1:
            return f"{bytes[i][0]},{bytes[i][1]}"
    return "-1,-1"

# 41,26
# That's the right answer! You are one gold star closer to finding the Chief 
# Historian.

if __name__ == "__main__":
    print(f"PART 1: {compute_part_1()}")
    print(f"PART 2: {compute_part_2()}")
