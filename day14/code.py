import os.path
import re
import time

def read_input(input_file_name):
    input_file = os.path.join(os.path.dirname(__file__), input_file_name)
    with open(input_file, "r") as f:
        lines = f.readlines()
        return lines

# --- Day 14: Restroom Redoubt ---
# One of The Historians needs to use the bathroom; fortunately, you know 
# there's a bathroom near an unvisited location on their list, and so you're 
# all quickly teleported directly to the lobby of Easter Bunny Headquarters.

# Unfortunately, EBHQ seems to have "improved" bathroom security again after 
# your last visit. The area outside the bathroom is swarming with robots!

# To get The Historian safely to the bathroom, you'll need a way to predict 
# where the robots will be in the future. Fortunately, they all seem to be 
# moving on the tile floor in predictable straight lines.

# You make a list (your puzzle input) of all of the robots' current positions 
# (p) and velocities (v), one robot per line. For example:

# p=0,4 v=3,-3
# p=6,3 v=-1,-3
# p=10,3 v=-1,2
# p=2,0 v=2,-1
# p=0,0 v=1,3
# p=3,0 v=-2,-2
# p=7,6 v=-1,-3
# p=3,0 v=-1,-2
# p=9,3 v=2,3
# p=7,3 v=-1,2
# p=2,4 v=2,-3
# p=9,5 v=-3,-3

# Each robot's position is given as p=x,y where x represents the number of 
# tiles the robot is from the left wall and y represents the number of tiles 
# from the top wall (when viewed from above). So, a position of p=0,0 means 
# the robot is all the way in the top-left corner.

# Each robot's velocity is given as v=x,y where x and y are given in tiles 
# per second. Positive x means the robot is moving to the right, and positive 
# y means the robot is moving down. So, a velocity of v=1,-2 means that each 
# second, the robot moves 1 tile to the right and 2 tiles up.

# The robots outside the actual bathroom are in a space which is 101 tiles 
# wide and 103 tiles tall (when viewed from above). However, in this example, 
# the robots are in a space which is only 11 tiles wide and 7 tiles tall.

# The robots are good at navigating over/under each other (due to a 
# combination of springs, extendable legs, and quadcopters), so they can 
# share the same tile and don't interact with each other. Visually, the 
# number of robots on each tile in this example looks like this:

# 1.12.......
# ...........
# ...........
# ......11.11
# 1.1........
# .........1.
# .......1...

# These robots have a unique feature for maximum bathroom security: they can 
# teleport. When a robot would run into an edge of the space they're in, they 
# instead teleport to the other side, effectively wrapping around the edges. 
# Here is what robot p=2,4 v=2,-3 does for the first few seconds:

# Initial state:
# ...........
# ...........
# ...........
# ...........
# ..1........
# ...........
# ...........

# After 1 second:
# ...........
# ....1......
# ...........
# ...........
# ...........
# ...........
# ...........

# After 2 seconds:
# ...........
# ...........
# ...........
# ...........
# ...........
# ......1....
# ...........

# After 3 seconds:
# ...........
# ...........
# ........1..
# ...........
# ...........
# ...........
# ...........

# After 4 seconds:
# ...........
# ...........
# ...........
# ...........
# ...........
# ...........
# ..........1

# After 5 seconds:
# ...........
# ...........
# ...........
# .1.........
# ...........
# ...........
# ...........

# The Historian can't wait much longer, so you don't have to simulate the 
# robots for very long. Where will the robots be after 100 seconds?

# In the above example, the number of robots on each tile after 100 seconds 
# has elapsed looks like this:

# ......2..1.
# ...........
# 1..........
# .11........
# .....1.....
# ...12......
# .1....1....

# To determine the safest area, count the number of robots in each quadrant 
# after 100 seconds. Robots that are exactly in the middle (horizontally or 
# vertically) don't count as being in any quadrant, so the only relevant 
# robots are:

# ..... 2..1.
# ..... .....
# 1.... .....
           
# ..... .....
# ...12 .....
# .1... 1....

# In this example, the quadrants contain 1, 3, 4, and 1 robot. Multiplying 
# these together gives a total safety factor of 12.

# Predict the motion of the robots in your list within a space which is 101 
# tiles wide and 103 tiles tall. What will the safety factor be after exactly 
# 100 seconds have elapsed?

class Robot:
    def __init__(self, p, v, limits):
        self.p = p
        self.v = v
        self.limits = limits

    def __str__(self):
        return(f"Robot at position p = {self.p}, v = {self.v}")

    def move(self):
        for i in range(2):
            self.p[i] += self.v[i]
            self.p[i] %= self.limits[i]
    
    def get_quadrant(self):
        if self.p[0] < self.limits[0]//2 and self.p[1] < self.limits[1]//2:
            return 1
        if self.p[0] < self.limits[0]//2 and self.p[1] > self.limits[1]//2:
            return 2
        if self.p[0] > self.limits[0]//2 and self.p[1] < self.limits[1]//2:
            return 3
        if self.p[0] > self.limits[0]//2 and self.p[1] > self.limits[1]//2:
            return 4
        return 0

def compute_part_1(input_file_name="input.txt"):
    input = read_input(input_file_name)
    numbers = [[int(x) for x in re.findall(r"-?\d+", line)] for line in input]
    robots = [Robot([line[0], line[1]], [line[2], line[3]], [101, 103]) for line in numbers]
    for i in range(100):
        for robot in robots:
            robot.move()
    quadrants = [0, 0, 0, 0, 0]
    for robot in robots:
        quadrants[robot.get_quadrant()] += 1
    return quadrants[1] * quadrants[2] * quadrants[3] * quadrants[4]

# 225648864
# That's the right answer! You are one gold star closer to finding the Chief 
# Historian.

# --- Part Two ---
# During the bathroom break, someone notices that these robots seem awfully 
# similar to ones built and used at the North Pole. If they're the same type 
# of robots, they should have a hard-coded Easter egg: very rarely, most of 
# the robots should arrange themselves into a picture of a Christmas tree.

# What is the fewest number of seconds that must elapse for the robots to 
# display the Easter egg?

def sum_of_distances_all_to_all(robots):
    sum_of_distances = 0
    for i in range(len(robots)):
        for j in range(i+1, len(robots)):
            sum_of_distances += abs(robots[i].p[0] - robots[j].p[0]) + abs(robots[i].p[1] - robots[j].p[1])
    return sum_of_distances

def print_map(map):
    for i in range(len(map)):
        print("".join(map[i]))
    print()

def get_easter_egg(robots):
    for i in range(7847):
        for robot in robots:
            robot.move()
    map = [['.' for _ in range(103)] for _ in range(102)]
    for robot in robots:
        map[robot.p[0]][robot.p[1]] = "X"
    print_map(map)

def compute_part_2(input_file_name="input.txt"):
    input = read_input(input_file_name)
    numbers = [[int(x) for x in re.findall(r"-?\d+", line)] for line in input]
    robots = [Robot([line[0], line[1]], [line[2], line[3]], [101, 103]) for line in numbers]
    sum_of_distances = sum_of_distances_all_to_all(robots)
    for i in range(10000):
        map = [['.' for _ in range(103)] for _ in range(102)]
        for robot in robots:
            robot.move()
            map[robot.p[0]][robot.p[1]] = "X"
        print(i)
        curr_sum_of_distances = sum_of_distances_all_to_all(robots)
        if curr_sum_of_distances < sum_of_distances:
            print_map(map)
            sum_of_distances = curr_sum_of_distances
            time.sleep(0.5)
    return 0

# 7847
# That's the right answer! You are one gold star closer to finding the Chief 
# Historian.

if __name__ == "__main__":
    print(f"PART 1: {compute_part_1()}")
    print(f"PART 2: {compute_part_2()}")
