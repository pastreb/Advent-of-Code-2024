import os.path
import re


def read_input(input_file_name):
    input_file = os.path.join(os.path.dirname(__file__), input_file_name)
    with open(input_file, "r") as f:
        lines = f.readlines()
        return lines


class Dummy:
    def __init__(self):
        self.dummy = 0

    def setup(self, input):
        for set in re.findall(r"[^;]+", input):
            pass


# --- Day 8: Resonant Collinearity ---

# You find yourselves on the roof of a top-secret Easter Bunny installation.

# While The Historians do their thing, you take a look at the familiar huge 
# antenna. Much to your surprise, it seems to have been reconfigured to emit 
# a signal that makes people 0.1% more likely to buy Easter Bunny brand 
# Imitation Mediocre Chocolate as a Christmas gift! Unthinkable!

# Scanning across the city, you find that there are actually many such 
# antennas. Each antenna is tuned to a specific frequency indicated by a 
# single lowercase letter, uppercase letter, or digit. You create a map (your 
# puzzle input) of these antennas. For example:

# ............
# ........0...
# .....0......
# .......0....
# ....0.......
# ......A.....
# ............
# ............
# ........A...
# .........A..
# ............
# ............

# The signal only applies its nefarious effect at specific antinodes based 
# on the resonant frequencies of the antennas. In particular, an antinode 
# occurs at any point that is perfectly in line with two antennas of the same 
# frequency - but only when one of the antennas is twice as far away as the 
# other. This means that for any pair of antennas with the same frequency, 
# there are two antinodes, one on either side of them.

# So, for these two antennas with frequency a, they create the two antinodes 
# marked with #:

# ..........
# ...#......
# ..........
# ....a.....
# ..........
# .....a....
# ..........
# ......#...
# ..........
# ..........

# Adding a third antenna with the same frequency creates several more 
# antinodes. It would ideally add four antinodes, but two are off the right 
# side of the map, so instead it adds only two:

# ..........
# ...#......
# #.........
# ....a.....
# ........a.
# .....a....
# ..#.......
# ......#...
# ..........
# ..........

# Antennas with different frequencies don't create antinodes; A and a count 
# as different frequencies. However, antinodes can occur at locations that 
# contain antennas. In this diagram, the lone antenna with frequency capital 
# A creates no antinodes but has a lowercase-a-frequency antinode at its 
# location:

# ..........
# ...#......
# #.........
# ....a.....
# ........a.
# .....a....
# ..#.......
# ......A...
# ..........
# ..........

# The first example has antennas with two different frequencies, so the 
# antinodes they create look like this, plus an antinode overlapping the 
# topmost A-frequency antenna:

# ......#....#
# ...#....0...
# ....#0....#.
# ..#....0....
# ....0....#..
# .#....A.....
# ...#........
# #......#....
# ........A...
# .........A..
# ..........#.
# ..........#.

# Because the topmost A-frequency antenna overlaps with a 0-frequency 
# antinode, there are 14 total unique locations that contain an antinode 
# within the bounds of the map.

# Calculate the impact of the signal. How many unique locations within the 
# bounds of the map contain an antinode?

def collect_antenna_positions(map):
    antennas = {}
    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j] != '.':
                antennas[map[i][j]] = antennas[map[i][j]] + [(i, j)] if map[i][j] in antennas.keys() else [(i, j)]
    return antennas

def get_antinodes_on_map(same_frequency_antennas):
    antinodes = []
    for i in range(len(same_frequency_antennas)):
        for j in range(i+1, len(same_frequency_antennas)):
            pos1 = same_frequency_antennas[i]
            pos2 = same_frequency_antennas[j]
            # Assuming pos1 is "before" pos2
            dy = abs(pos1[0]-pos2[0])
            dx = abs(pos1[1]-pos2[1])
            an1 = (pos1[0] - dy, pos1[1] + dx if pos1[1] > pos2[1] else pos1[1] - dx)
            antinodes.append(an1)
            an2 = (pos2[0] + dy, pos2[1] + dx if pos1[1] < pos2[1] else pos2[1] - dx)
            antinodes.append(an2)
            # print(f"pos1: {pos1}, pos2: {pos2}, an1: {an1}, an2: {an2}")
    return antinodes
            

def compute_part_1(input_file_name="input.txt"):
    input = read_input(input_file_name)
    map = [[x for x in line.replace('\n', '')] for line in input]
    map_height = len(map)
    map_width = len(map[0])
    antennas = collect_antenna_positions(map)
    antinodes = []
    for frequency in antennas.keys():
        for antinode in get_antinodes_on_map(antennas[frequency]):
            if antinode[0] >= 0 and antinode[0] < map_height and antinode[1] >= 0 and antinode[1] < map_width and antinode not in antinodes:
                antinodes.append(antinode)
    return len(antinodes)

# 426
# That's the right answer! You are one gold star closer to finding the Chief 
# Historian.


# --- Part Two ---
# Watching over your shoulder as you work, one of The Historians asks if you 
# took the effects of resonant harmonics into your calculations.

# Whoops!

# After updating your model, it turns out that an antinode occurs at any grid 
# position exactly in line with at least two antennas of the same frequency, 
# regardless of distance. This means that some of the new antinodes will 
# occur at the position of each antenna (unless that antenna is the only one 
# of its frequency).

# So, these three T-frequency antennas now create many antinodes:

# T....#....
# ...T......
# .T....#...
# .........#
# ..#.......
# ..........
# ...#......
# ..........
# ....#.....
# ..........

# In fact, the three T-frequency antennas are all exactly in line with two 
# antennas, so they are all also antinodes! This brings the total number of 
# antinodes in the above example to 9.

# The original example now has 34 antinodes, including the antinodes that 
# appear on every antenna:

# ##....#....#
# .#.#....0...
# ..#.#0....#.
# ..##...0....
# ....0....#..
# .#...#A....#
# ...#..#.....
# #....#.#....
# ..#.....A...
# ....#....A..
# .#........#.
# ...#......##

# Calculate the impact of the signal using this updated model. How many 
# unique locations within the bounds of the map contain an antinode?

def get_more_antinodes_on_map(same_frequency_antennas, max):
    antinodes = []
    for i in range(len(same_frequency_antennas)):
        for j in range(i+1, len(same_frequency_antennas)):
            pos1 = same_frequency_antennas[i]
            pos2 = same_frequency_antennas[j]
            # Assuming pos1 is "before" pos2
            dy = abs(pos1[0]-pos2[0])
            dx = abs(pos1[1]-pos2[1])
            for k in range(max): # just scale dx and dy
                an1 = (pos1[0] - k*dy, pos1[1] + k*dx if pos1[1] > pos2[1] else pos1[1] - k*dx)
                antinodes.append(an1)
                an2 = (pos2[0] + k*dy, pos2[1] + k*dx if pos1[1] < pos2[1] else pos2[1] - k*dx)
                antinodes.append(an2)
    return antinodes

def compute_part_2(input_file_name="input.txt"):
    input = read_input(input_file_name)
    map = [[x for x in line.replace('\n', '')] for line in input]
    map_height = len(map)
    map_width = len(map[0])
    antennas = collect_antenna_positions(map)
    antinodes = []
    for frequency in antennas.keys():
        for antinode in get_more_antinodes_on_map(antennas[frequency], max(map_height, map_width)):
            if antinode[0] >= 0 and antinode[0] < map_height and antinode[1] >= 0 and antinode[1] < map_width and antinode not in antinodes:
                antinodes.append(antinode)
    return len(antinodes)


# 1359
# That's the right answer! You are one gold star closer to finding the Chief 
# Historian.

if __name__ == "__main__":
    print(f"PART 1: {compute_part_1()}")
    print(f"PART 2: {compute_part_2()}")
