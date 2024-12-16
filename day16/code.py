import os.path
import re


def read_input(input_file_name):
    input_file = os.path.join(os.path.dirname(__file__), input_file_name)
    with open(input_file, "r") as f:
        lines = f.readlines()
        return lines

# --- Day 16: Reindeer Maze ---

# It's time again for the Reindeer Olympics! This year, the big event is the 
# Reindeer Maze, where the Reindeer compete for the lowest score.

# You and The Historians arrive to search for the Chief right as the event is 
# about to start. It wouldn't hurt to watch a little, right?

# The Reindeer start on the Start Tile (marked S) facing East and need to 
# reach the End Tile (marked E). They can move forward one tile at a time 
# (increasing their score by 1 point), but never into a wall (#). They can 
# also rotate clockwise or counterclockwise 90 degrees at a time (increasing 
# their score by 1000 points).

# To figure out the best place to sit, you start by grabbing a map (your 
# puzzle input) from a nearby kiosk. For example:

###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############

# There are many paths through this maze, but taking any of the best paths 
# would incur a score of only 7036. This can be achieved by taking a total of 
# 36 steps forward and turning 90 degrees a total of 7 times:

###############
#.......#....E#
#.#.###.#.###^#
#.....#.#...#^#
#.###.#####.#^#
#.#.#.......#^#
#.#.#####.###^#
#..>>>>>>>>v#^#
###^#.#####v#^#
#>>^#.....#v#^#
#^#.#.###.#v#^#
#^....#...#v#^#
#^###.#.#.#v#^#
#S..#.....#>>^#
###############

# Here's a second example:

#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################

# In this maze, the best paths cost 11048 points; following one such path 
# would look like this:

#################
#...#...#...#..E#
#.#.#.#.#.#.#.#^#
#.#.#.#...#...#^#
#.#.#.#.###.#.#^#
#>>v#.#.#.....#^#
#^#v#.#.#.#####^#
#^#v..#.#.#>>>>^#
#^#v#####.#^###.#
#^#v#..>>>>^#...#
#^#v###^#####.###
#^#v#>>^#.....#.#
#^#v#^#####.###.#
#^#v#^........#.#
#^#v#^#########.#
#S#>>^..........#
#################

# Note that the path shown above includes one 90 degree turn as the very 
# first move, rotating the Reindeer from facing East to facing North.

# Analyze your map carefully. What is the lowest score a Reindeer could 
# possibly get?

def find_named_tile(map, name):
    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j] == name:
                return i, j

def turn_90_clk(dir):
    match dir:
        case '>':
            return 'v'
        case 'v':
            return '<'
        case '<':
            return '^'
        case '^':
            return '>'

def turn_90_cclk(dir):
    match dir:
        case '>':
            return '^'
        case '^':
            return '<'
        case '<':
            return 'v'
        case 'v':
            return '>'

def get_neighbor(i, j, dir):
    match dir:
        case '>':
            return i, j+1
        case '^':
            return i-1, j
        case '<':
            return i, j-1
        case 'v':
            return i+1, j

def shortest_path_distances(si, sj, ti, tj, map):
    queue = []
    dist = {}
    dist[(si, sj, '>')] = 0
    queue.append((si, sj, '>'))
    while len(queue) > 0:
        (i, j, dir) = queue.pop(0)
        ii, jj = get_neighbor(i, j, dir)
        if map[ii][jj] != '#':
            if (ii, jj, dir) in dist.keys() and dist[(ii, jj, dir)] <= dist[(i, j, dir)] + 1:
                pass
            else:
                dist[(ii, jj, dir)] = dist[(i, j, dir)] + 1
                queue.append((ii, jj, dir))
        for next_dir in [turn_90_clk(dir), turn_90_cclk(dir)]:
            if (i, j, next_dir) in dist.keys() and dist[(i, j, next_dir)] <= dist[(i, j, dir)] + 1000:
                pass
            else:
                dist[(i, j, next_dir)] = dist[(i, j, dir)] + 1000
                queue.append((i, j, next_dir))
    return dist

def print_map(map):
    for line in map:
        print("".join(line))
    print()

def compute_part_1(input_file_name="input.txt"):
    input = read_input(input_file_name)
    map = [[x for x in line.replace('\n', '')] for line in input]
    si, sj = find_named_tile(map, 'S')
    ti, tj = find_named_tile(map, 'E')
    distances = shortest_path_distances(si, sj, ti, tj, map)
    return min([distances[(ti, tj, dir)] for dir in ['^', '>', 'v', '<'] if (ti, tj, dir) in distances.keys()])

# 98520
# That's the right answer! You are one gold star closer to finding the Chief 
# Historian.

# --- Part Two ---
# Now that you know what the best paths look like, you can figure out the 
# best spot to sit.

# Every non-wall tile (S, ., or E) is equipped with places to sit along the 
# edges of the tile. While determining which of these tiles would be the best 
# spot to sit depends on a whole bunch of factors (how comfortable the seats 
# are, how far away the bathrooms are, whether there's a pillar blocking your 
# view, etc.), the most important factor is whether the tile is on one of the 
# best paths through the maze. If you sit somewhere else, you'd miss all the 
# action!

# So, you'll need to determine which tiles are part of any best path through 
# the maze, including the S and E tiles.

# In the first example, there are 45 tiles (marked O) that are part of at 
# least one of the various best paths through the maze:

###############
#.......#....O#
#.#.###.#.###O#
#.....#.#...#O#
#.###.#####.#O#
#.#.#.......#O#
#.#.#####.###O#
#..OOOOOOOOO#O#
###O#O#####O#O#
#OOO#O....#O#O#
#O#O#O###.#O#O#
#OOOOO#...#O#O#
#O###.#.#.#O#O#
#O..#.....#OOO#
###############

# In the second example, there are 64 tiles that are part of at least one of 
# the best paths:

#################
#...#...#...#..O#
#.#.#.#.#.#.#.#O#
#.#.#.#...#...#O#
#.#.#.#.###.#.#O#
#OOO#.#.#.....#O#
#O#O#.#.#.#####O#
#O#O..#.#.#OOOOO#
#O#O#####.#O###O#
#O#O#..OOOOO#OOO#
#O#O###O#####O###
#O#O#OOO#..OOO#.#
#O#O#O#####O###.#
#O#O#OOOOOOO..#.#
#O#O#O#########.#
#O#OOO..........#
#################

# Analyze your map further. How many tiles are part of at least one of the 
# best paths through the maze?

def get_predecessor(i, j, dir):
    match dir:
        case '>':
            return i, j-1
        case '^':
            return i+1, j
        case '<':
            return i, j+1
        case 'v':
            return i-1, j

def backtrack_best_paths(si, sj, ti, tj, dist):
    tiles = []
    queue = []
    shortest_path_length = min([dist[(ti, tj, dir)] for dir in ['^', '>', 'v', '<'] if (ti, tj, dir) in dist.keys()])
    for dir in ['^', '>', 'v', '<']:
        if (ti, tj, dir) in dist.keys() and dist[(ti, tj, dir)] == shortest_path_length:
            queue.append((ti, tj, dir)) 
            tiles.append((ti, tj))
    while len(queue) > 0:
        (i, j, dir) = queue.pop(0)
        ii, jj = get_predecessor(i, j, dir)
        if (ii, jj, dir) in dist.keys() and dist[(ii, jj, dir)] == dist[(i, j, dir)]-1:
            if (ii, jj) not in tiles:
                tiles.append((ii, jj))
            queue.append((ii, jj, dir))
        for prev_dir in [turn_90_clk(dir), turn_90_cclk(dir)]:
            if (i, j, prev_dir) in dist.keys() and dist[(i, j, prev_dir)] == dist[(i, j, dir)]-1000:
                queue.append((i, j, prev_dir))
    return tiles


def compute_part_2(input_file_name="input.txt"):
    input = read_input(input_file_name)
    map = [[x for x in line.replace('\n', '')] for line in input]
    si, sj = find_named_tile(map, 'S')
    ti, tj = find_named_tile(map, 'E')
    distances = shortest_path_distances(si, sj, ti, tj, map)
    return len(backtrack_best_paths(si, sj, ti, tj, distances))

# 609
# That's the right answer! You are one gold star closer to finding the Chief 
# Historian.

if __name__ == "__main__":
    print(f"PART 1: {compute_part_1()}")
    print(f"PART 2: {compute_part_2()}")