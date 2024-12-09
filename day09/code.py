import os.path
import re


def read_input(input_file_name):
    input_file = os.path.join(os.path.dirname(__file__), input_file_name)
    with open(input_file, "r") as f:
        lines = f.readlines()
        return lines


# --- Day 9: Disk Fragmenter ---

# Another push of the button leaves you in the familiar hallways of some 
# friendly amphipods! Good thing you each somehow got your own personal mini 
# submarine. The Historians jet away in search of the Chief, mostly by 
# driving directly into walls.

# While The Historians quickly figure out how to pilot these things, you 
# notice an amphipod in the corner struggling with his computer. He's trying 
# to make more contiguous free space by compacting all of the files, but his 
# program isn't working; you offer to help.

# He shows you the disk map (your puzzle input) he's already generated. For 
# example:

# 2333133121414131402

# The disk map uses a dense format to represent the layout of files and free 
# space on the disk. The digits alternate between indicating the length of a 
# file and the length of free space.

# So, a disk map like 12345 would represent a one-block file, two blocks of 
# free space, a three-block file, four blocks of free space, and then a five-
# block file. A disk map like 90909 would represent three nine-block files 
# in a row (with no free space between them).

# Each file on disk also has an ID number based on the order of the files as 
# they appear before they are rearranged, starting with ID 0. So, the disk 
# map 12345 has three files: a one-block file with ID 0, a three-block file 
# with ID 1, and a five-block file with ID 2. Using one character for each 
# block where digits are the file ID and . is free space, the disk map 12345 
# represents these individual blocks:

# 0..111....22222

# The first example above, 2333133121414131402, represents these individual 
# blocks:

# 00...111...2...333.44.5555.6666.777.888899

# The amphipod would like to move file blocks one at a time from the end of 
# the disk to the leftmost free space block (until there are no gaps 
# remaining between file blocks). For the disk map 12345, the process looks 
# like this:

# 0..111....22222
# 02.111....2222.
# 022111....222..
# 0221112...22...
# 02211122..2....
# 022111222......

# The first example requires a few more steps:

# 00...111...2...333.44.5555.6666.777.888899
# 009..111...2...333.44.5555.6666.777.88889.
# 0099.111...2...333.44.5555.6666.777.8888..
# 00998111...2...333.44.5555.6666.777.888...
# 009981118..2...333.44.5555.6666.777.88....
# 0099811188.2...333.44.5555.6666.777.8.....
# 009981118882...333.44.5555.6666.777.......
# 0099811188827..333.44.5555.6666.77........
# 00998111888277.333.44.5555.6666.7.........
# 009981118882777333.44.5555.6666...........
# 009981118882777333644.5555.666............
# 00998111888277733364465555.66.............
# 0099811188827773336446555566..............

# The final step of this file-compacting process is to update the filesystem 
# checksum. To calculate the checksum, add up the result of multiplying each 
# of these blocks' position with the file ID number it contains. The leftmost 
# block is in position 0. If a block contains free space, skip it instead.

# Continuing the first example, the first few blocks' position multiplied by 
# its file ID number are 0 * 0 = 0, 1 * 0 = 0, 2 * 9 = 18, 3 * 9 = 27, 
# 4 * 8 = 32, and so on. In this example, the checksum is the sum of these, 
# 1928.

# Compact the amphipod's hard drive using the process he requested. What is
# the resulting filesystem checksum? (Be careful copy/pasting the input for 
# this puzzle; it is a single, very long line.)

def make_blocks(disk_map):
    blocks = []
    file_index = 0
    for i in range(len(disk_map)):
        if i%2 == 0:
            for k in range(disk_map[i]):
                blocks.append(file_index)
            file_index += 1
        else:
            for k in range(disk_map[i]):
                blocks.append(-1) # model . as -1
    return blocks

def move_blocks(blocks):
    head = 0
    tail = len(blocks)-1
    while head < tail:
        if blocks[head] != -1:
            head += 1
        elif blocks[tail] == -1:
            tail -= 1
        else:
            blocks[head], blocks[tail] = blocks[tail], blocks[head]


def compute_part_1(input_file_name="input.txt"):
    input = read_input(input_file_name)
    if len(input) != 1:
        exit(f"Input formatting issues; should be of length 1 but is {len(input)}.")
    disk_map = [int(x) for x in input[0]]
    blocks = make_blocks(disk_map)
    move_blocks(blocks)
    return sum([i*blocks[i] if blocks[i] >= 0 else 0 for i in range(len(blocks))])

# 6299243228569
# That's the right answer! You are one gold star closer to finding the Chief 
# Historian.

# --- Part Two ---

# Upon completion, two things immediately become clear. First, the disk 
# definitely has a lot more contiguous free space, just like the amphipod 
# hoped. Second, the computer is running much more slowly! Maybe introducing 
# all of that file system fragmentation was a bad idea?

# The eager amphipod already has a new plan: rather than move individual 
# blocks, he'd like to try compacting the files on his disk by moving whole 
# files instead.

# This time, attempt to move whole files to the leftmost span of free space 
# blocks that could fit the file. Attempt to move each file exactly once in 
# order of decreasing file ID number starting with the file with the highest 
# file ID number. If there is no span of free space to the left of a file 
# that is large enough to fit the file, the file does not move.

# The first example from above now proceeds differently:

# 00...111...2...333.44.5555.6666.777.888899
# 0099.111...2...333.44.5555.6666.777.8888..
# 0099.1117772...333.44.5555.6666.....8888..
# 0099.111777244.333....5555.6666.....8888..
# 00992111777.44.333....5555.6666.....8888..

# The process of updating the filesystem checksum is the same; now, this 
# example's checksum would be 2858.

# Start over, now compacting the amphipod's hard drive using this new method 
# instead. What is the resulting filesystem checksum?

def move_files(blocks):
    tail = len(blocks) - 1
    visited_files = []
    while tail >= 0:
        file_id = blocks[tail]
        if file_id in visited_files:
            tail -= 1
            continue
        visited_files.append(file_id)
        file_len = 1
        while tail-1 >= 0 and blocks[tail-1] == file_id:
            tail -= 1
            file_len += 1
        head = 0
        while head < tail:
            if all([block == -1 for block in blocks[head:head+file_len]]):
                for k in range(file_len):
                    blocks[head+k] = file_id
                    blocks[tail+k] = -1
                break
            head += 1
        tail -= 1
        print(f"Moving Blocks as Files {len(blocks)-tail}/{len(blocks)}")


def compute_part_2(input_file_name="input.txt"):
    input = read_input(input_file_name)
    if len(input) != 1:
        exit(f"Input formatting issues; should be of length 1 but is {len(input)}.")
    disk_map = [int(x) for x in input[0]]
    blocks = make_blocks(disk_map)
    move_files(blocks)
    return sum([i*blocks[i] if blocks[i] >= 0 else 0 for i in range(len(blocks))])

# 6326952672104
# That's the right answer! You are one gold star closer to finding the Chief 
# Historian.

if __name__ == "__main__":
    print(f"PART 1: {compute_part_1()}")
    print(f"PART 2: {compute_part_2()}")
