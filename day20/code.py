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

# --- Day 20: Race Condition ---

# The Historians are quite pixelated again. This time, a massive, black 
# building looms over you - you're right outside the CPU!

# While The Historians get to work, a nearby program sees that you're idle 
# and challenges you to a race. Apparently, you've arrived just in time for 
# the frequently-held race condition festival!

# The race takes place on a particularly long and twisting code path; 
# programs compete to see who can finish in the fewest picoseconds. The 
# winner even gets their very own mutex!

# They hand you a map of the racetrack (your puzzle input). For example:

###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############

# The map consists of track (.) - including the start (S) and end (E) 
# positions (both of which also count as track) - and walls (#).

# When a program runs through the racetrack, it starts at the start position. 
# Then, it is allowed to move up, down, left, or right; each such move takes 
# 1 picosecond. The goal is to reach the end position as quickly as possible. 
# In this example racetrack, the fastest time is 84 picoseconds.

# Because there is only a single path from the start to the end and the 
# programs all go the same speed, the races used to be pretty boring. To make 
# things more interesting, they introduced a new rule to the races: programs 
# are allowed to cheat.

# The rules for cheating are very strict. Exactly once during a race, a 
# program may disable collision for up to 2 picoseconds. This allows the 
# program to pass through walls as if they were regular track. At the end of 
# the cheat, the program must be back on normal track again; otherwise, it 
# will receive a segmentation fault and get disqualified.

# So, a program could complete the course in 72 picoseconds (saving 12 
# picoseconds) by cheating for the two moves marked 1 and 2:

###############
#...#...12....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############

# Or, a program could complete the course in 64 picoseconds (saving 20 
# picoseconds) by cheating for the two moves marked 1 and 2:

###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...12..#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############

# This cheat saves 38 picoseconds:

###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.####1##.###
#...###.2.#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############

# This cheat saves 64 picoseconds and takes the program directly to the end:

###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..21...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############

# Each cheat has a distinct start position (the position where the cheat is 
# activated, just before the first move that is allowed to go through walls) 
# and end position; cheats are uniquely identified by their start position 
# and end position.

# In this example, the total number of cheats (grouped by the amount of time 
# they save) are as follows:

# - There are 14 cheats that save 2 picoseconds.
# - There are 14 cheats that save 4 picoseconds.
# - There are 2 cheats that save 6 picoseconds.
# - There are 4 cheats that save 8 picoseconds.
# - There are 2 cheats that save 10 picoseconds.
# - There are 3 cheats that save 12 picoseconds.
# - There is one cheat that saves 20 picoseconds.
# - There is one cheat that saves 36 picoseconds.
# - There is one cheat that saves 38 picoseconds.
# - There is one cheat that saves 40 picoseconds.
# - There is one cheat that saves 64 picoseconds.

# You aren't sure what the conditions of the racetrack will be like, so to 
# give yourself as many options as possible, you'll need a list of the best 
# cheats. How many cheats would save you at least 100 picoseconds?

def print_map(map):
    for line in map:
        print("".join(line))
    print()

def find_position(pos_name, map):
    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j] == pos_name:
                return (i, j)
    return (-1, -1)

def get_all_neighbors(i, j, map):
    return [(ii, jj) for (ii, jj) in [(i-1, j), (i+1, j), (i, j-1), (i, j+1)] if ii >= 0 and ii < len(map) and jj >= 0 and jj < len(map[i])]

def get_track_neighbors(i, j, map):
    return [(ii, jj) for (ii, jj) in get_all_neighbors(i, j, map) if map[ii][jj] != '#']

def get_wall_neighbors(i, j, map):
    return [(ii, jj) for (ii, jj) in get_all_neighbors(i, j, map) if map[ii][jj] == '#']

def get_shortest_path_distances(si, sj, map):
    queue = [(si, sj)]
    shortest_path_distances = {
        (si, sj) : 0
    }
    while(len(queue) > 0):
        (i, j) = queue.pop(0)
        for ii, jj in get_track_neighbors(i, j, map):
            if (ii, jj) in shortest_path_distances:
                continue
            shortest_path_distances[(ii, jj)] = shortest_path_distances[(i, j)] + 1
            queue.append((ii, jj))
    return shortest_path_distances

def get_shortest_path_positions(ti, tj, shortest_path_distances, map):
    shortest_path_positions = [(ti, tj)]
    while shortest_path_distances[shortest_path_positions[-1]] != 0:
        (i, j) = shortest_path_positions[-1]
        for (ii, jj) in get_track_neighbors(i, j, map):
            if shortest_path_distances[(i, j)] == shortest_path_distances[(ii, jj)] + 1:
                shortest_path_positions.append((ii, jj))
    shortest_path_positions.reverse() # Starts with ['S', '.', ..., 'E']
    return shortest_path_positions

def get_stop_cheat_positions(c1i, c1j, initial_candidates, cheat_distance, map):
    # Collect all track positions that are reachable from (c1i, c1j) while cheating for at most cheat_distance
    queue = [(c1i, c1j)]
    dist = {
        (c1i, c1j) : 0
    }
    while(len(queue) > 0):
        (i, j) = queue.pop(0)
        if dist[(i, j)] >= cheat_distance:
            continue
        for (ii, jj) in get_all_neighbors(i, j, map):
            if (ii, jj) in dist:
                continue
            dist[(ii, jj)] = dist[(i, j)] + 1
            queue.append((ii, jj))
    return {pos : dist[pos] for pos in dist.keys() if pos in initial_candidates}

def compute(map, cheat_distance, min_time_to_save):
    (si, sj) = find_position("S", map)
    (ti, tj) = find_position("E", map)
    shortest_path_distances_to_s = get_shortest_path_distances(si, sj, map)
    shortest_path_distances_to_t = get_shortest_path_distances(ti, tj, map)
    orginial_distance = shortest_path_distances_to_s[(ti, tj)]
    cheats = {}
    # Cheat start position needs to be reachable from S; cheat end positions needs to reach t
    for (c1i, c1j) in shortest_path_distances_to_s.keys():
        c2s = get_stop_cheat_positions(c1i, c1j, shortest_path_distances_to_t.keys(), cheat_distance, map)
        for (c2i, c2j) in c2s.keys():
            dist = shortest_path_distances_to_s[c1i, c1j] + c2s[c2i, c2j] + shortest_path_distances_to_t[c2i, c2j]
            if dist <= orginial_distance - min_time_to_save:
                cheats[(c1i, c1j, c2i, c2j)] = dist
    return len(cheats)

def compute_part_1(input_file_name="input.txt"):
    input = read_input(input_file_name)
    map = [[x for x in re.findall(r"\.|\#|S|E", line)] for line in input]
    return compute(map, 2, 100)
    
# 1321
# That's the right answer! You are one gold star closer to finding the Chief 
# Historian.

# --- Part Two ---

# The programs seem perplexed by your list of cheats. Apparently, the two-
# picosecond cheating rule was deprecated several milliseconds ago! The 
# latest version of the cheating rule permits a single cheat that instead 
# lasts at most 20 picoseconds.

# Now, in addition to all the cheats that were possible in just two 
# picoseconds, many more cheats are possible. This six-picosecond cheat saves 
# 76 picoseconds:

###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#1#####.#.#.###
#2#####.#.#...#
#3#####.#.###.#
#456.E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############

# Because this cheat has the same start and end positions as the one above, 
# it's the same cheat, even though the path taken during the cheat is 
# different:

###############
#...#...#.....#
#.#.#.#.#.###.#
#S12..#.#.#...#
###3###.#.#.###
###4###.#.#...#
###5###.#.###.#
###6.E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############

# Cheats don't need to use all 20 picoseconds; cheats can last any amount of 
# time up to and including 20 picoseconds (but can still only end when the 
# program is on normal track). Any cheat time not used is lost; it can't be 
# saved for another cheat later.

# You'll still need a list of the best cheats, but now there are even more 
# to choose between. Here are the quantities of cheats in this example that save 
# 50 picoseconds or more:

# There are 32 cheats that save 50 picoseconds.
# There are 31 cheats that save 52 picoseconds.
# There are 29 cheats that save 54 picoseconds.
# There are 39 cheats that save 56 picoseconds.
# There are 25 cheats that save 58 picoseconds.
# There are 23 cheats that save 60 picoseconds.
# There are 20 cheats that save 62 picoseconds.
# There are 19 cheats that save 64 picoseconds.
# There are 12 cheats that save 66 picoseconds.
# There are 14 cheats that save 68 picoseconds.
# There are 12 cheats that save 70 picoseconds.
# There are 22 cheats that save 72 picoseconds.
# There are 4 cheats that save 74 picoseconds.
# There are 3 cheats that save 76 picoseconds.

# Find the best cheats using the updated cheating rules. How many cheats 
# would save you at least 100 picoseconds?

def compute_part_2(input_file_name="input.txt"):
    input = read_input(input_file_name)
    map = [[x for x in re.findall(r"\.|\#|S|E", line)] for line in input]
    return compute(map, 20, 100)

# 971737
# That's the right answer! You are one gold star closer to finding the Chief 
# Historian.

if __name__ == "__main__":
    print(f"PART 1: {compute_part_1()}")
    print(f"PART 2: {compute_part_2()}")
