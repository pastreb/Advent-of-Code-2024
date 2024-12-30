import os.path
import functools

def read_input(input_file_name):
    input_file = os.path.join(os.path.dirname(__file__), input_file_name)
    with open(input_file, "r") as f:
        lines = f.readlines()
        return lines

# --- Day 21: Keypad Conundrum ---

# As you teleport onto Santa's Reindeer-class starship, The Historians begin 
# to panic: someone from their search party is missing. A quick life-form 
# scan by the ship's computer reveals that when the missing Historian 
# teleported, he arrived in another part of the ship.

# The door to that area is locked, but the computer can't open it; it can 
# only be opened by physically typing the door codes (your puzzle input) on 
# the numeric keypad on the door.

# The numeric keypad has four rows of buttons: 789, 456, 123, and finally an 
# empty gap followed by 0A. Visually, they are arranged like this:

# +---+---+---+
# | 7 | 8 | 9 |
# +---+---+---+
# | 4 | 5 | 6 |
# +---+---+---+
# | 1 | 2 | 3 |
# +---+---+---+
#     | 0 | A |
#     +---+---+

# Unfortunately, the area outside the door is currently depressurized and 
# nobody can go near the door. A robot needs to be sent instead.

# The robot has no problem navigating the ship and finding the numeric 
# keypad, but it's not designed for button pushing: it can't be told to push 
# a specific button directly. Instead, it has a robotic arm that can be 
# controlled remotely via a directional keypad.

# The directional keypad has two rows of buttons: a gap / ^ (up) / A 
# (activate) on the first row and < (left) / v (down) / > (right) on the 
# second row. Visually, they are arranged like this:

#     +---+---+
#     | ^ | A |
# +---+---+---+
# | < | v | > |
# +---+---+---+

# When the robot arrives at the numeric keypad, its robotic arm is pointed at 
# the A button in the bottom right corner. After that, this directional 
# keypad remote control must be used to maneuver the robotic arm: the up / 
# down / left / right buttons cause it to move its arm one button in that 
# direction, and the A button causes the robot to briefly move forward, 
# pressing the button being aimed at by the robotic arm.

# For example, to make the robot type 029A on the numeric keypad, one 
# sequence of inputs on the directional keypad you could use is:

# - < to move the arm from A (its initial position) to 0.
# - A to push the 0 button.
# - ^A to move the arm to the 2 button and push it.
# - >^^A to move the arm to the 9 button and push it.
# - vvvA to move the arm to the A button and push it.

# In total, there are three shortest possible sequences of button presses on 
# this directional keypad that would cause the robot to type 029A: 
# <A^A>^^AvvvA, <A^A^>^AvvvA, and <A^A^^>AvvvA.

# Unfortunately, the area containing this directional keypad remote control 
# is currently experiencing high levels of radiation and nobody can go near 
# it. A robot needs to be sent instead.

# When the robot arrives at the directional keypad, its robot arm is pointed 
# at the A button in the upper right corner. After that, a second, different 
# directional keypad remote control is used to control this robot (in the 
# same way as the first robot, except that this one is typing on a 
# directional keypad instead of a numeric keypad).

# There are multiple shortest possible sequences of directional keypad button 
# presses that would cause this robot to tell the first robot to type 029A on 
# the door. One such sequence is v<<A>>^A<A>AvA<^AA>A<vAAA>^A.

# Unfortunately, the area containing this second directional keypad remote 
# control is currently -40 degrees! Another robot will need to be sent to 
# type on that directional keypad, too.

# There are many shortest possible sequences of directional keypad button 
# presses that would cause this robot to tell the second robot to tell the 
# first robot to eventually type 029A on the door. One such sequence is 
# <vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A.

# Unfortunately, the area containing this third directional keypad remote 
# control is currently full of Historians, so no robots can find a clear path 
# there. Instead, you will have to type this sequence yourself.

# Were you to choose this sequence of button presses, here are all of the 
# buttons that would be pressed on your directional keypad, the two robots' 
# directional keypads, and the numeric keypad:

# <vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A
# v<<A>>^A<A>AvA<^AA>A<vAAA>^A
# <A^A>^^AvvvA
# 029A

# In summary, there are the following keypads:
# - One directional keypad that you are using.
# - Two directional keypads that robots are using.
# - One numeric keypad (on a door) that a robot is using.

# It is important to remember that these robots are not designed for button 
# pushing. In particular, if a robot arm is ever aimed at a gap where no 
# button is present on the keypad, even for an instant, the robot will panic 
# unrecoverably. So, don't do that. All robots will initially aim at the 
# keypad's A key, wherever it is.

# To unlock the door, five codes will need to be typed on its numeric keypad. 
# For example:

# 029A
# 980A
# 179A
# 456A
# 379A

# For each of these, here is a shortest sequence of button presses you could 
# type to cause the desired code to be typed on the numeric keypad:

# 029A: <vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A
# 980A: <v<A>>^AAAvA^A<vA<AA>>^AvAA<^A>A<v<A>A>^AAAvA<^A>A<vA>^A<A>A
# 179A: <v<A>>^A<vA<A>>^AAvAA<^A>A<v<A>>^AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A
# 456A: <v<A>>^AA<vA<A>>^AAvAA<^A>A<vA>^A<A>A<vA>^A<A>A<v<A>A>^AAvA<^A>A
# 379A: <v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A

# The Historians are getting nervous; the ship computer doesn't remember 
# whether the missing Historian is trapped in the area containing a giant 
# electromagnet or molten lava. You'll need to make sure that for each of the 
# five codes, you find the shortest sequence of button presses necessary.

# The complexity of a single code (like 029A) is equal to the result of 
# multiplying these two values:
# - The length of the shortest sequence of button presses you need to type 
#   on your directional keypad in order to cause the code to be typed on 
#   the numeric keypad; for 029A, this would be 68.
# - The numeric part of the code (ignoring leading zeroes); for 029A, this 
#   would be 29.

# In the above example, complexity of the five codes can be found by 
# calculating 68 * 29, 60 * 980, 68 * 179, 64 * 456, and 64 * 379. Adding 
# these together produces 126384.

# Find the fewest number of button presses you'll need to perform in order to 
# cause the robot in front of the door to type each code. What is the sum of 
# the complexities of the five codes on your list?

# Returns the optimal sequence from getting from s to t on the directional keypad
def get_optimal_sequence(s, t):

        if s == t:
            return "A"
        
        match s + t:
            
            case "A^":
                return "<A"
            case "A<":
                return "v<<A"
            case "Av":
                return "<vA"
            case "A>":
                return "vA"
            
            case "^A":
                return ">A"
            case "^v":
                exit("Makes no sense")
            case "^<":
                return "v<A" 
            case "^>":
                return "v>A"
            
            case "<A":
                return ">>^A"
            case "<^":
                return ">^A"
            case "<v":
                return ">A"
            case "<>":
                exit("Makes no sense")

            case "vA":
                return "^>A"
            case "v^":
                exit("Makes no sense")
            case "v<":
                return "<A"
            case "v>":
                return ">A"
            
            case ">A":
                return "^A"
            case ">^":
                return "<^A"
            case "><":
                exit("Makes no sense")
            case ">v":
                return "<A"

        exit("Unexpected transition")

# Get all possible sequences that form a shortest path from current_pos to the pos with target_button
# Only use this for the Numeric Keypad
def get_shortest_path_sequences(target_button, current_pos, keypad):
        queue = [current_pos]
        sequences = {current_pos : ['']}
        # We are in fact only interested in the "best" sequence, but finding that is a bit difficult
        # since there are not only rules to follow (e.g. never go over the empty space) but also
        # orders of operations that are better than others (e.g. '<<^' better than '<^<' and more complicated).
        # Since there are not that many possibilities for entering the number on the Numeric Keybad, we just
        # look at all of them.
        while len(queue) > 0:
            (i, j) = queue.pop(0)
            for ii, jj, dir in [(i-1, j, '^'), (i, j+1, '>'), (i+1, j, 'v'), (i, j-1, '<')]:
                if ii >= 0 and ii < len(keypad) and jj >= 0 and jj < len(keypad[ii]) and keypad[ii][jj] != '':
                    if (ii, jj) not in sequences.keys():
                        queue.append((ii, jj))
                        sequences[(ii, jj)] = []
                        for seq in sequences[(i, j)]:
                            if (seq + dir) not in sequences[(ii, jj)]: 
                                sequences[(ii, jj)].append(seq + dir)
                    elif len(sequences[(ii,jj)][0]) >= len(sequences[(i,j)][0]) + 1:
                        queue.append((ii, jj))
                        for seq in sequences[(i, j)]:
                            if (seq + dir) not in sequences[(ii, jj)]: 
                                sequences[(ii, jj)].append(seq + dir)
        return [seq + 'A' for seq in sequences[find_pos(target_button, keypad)]]

def get_sequences_from_numeric_keypad(code, numeric_keypad):
    pos = find_pos("A", numeric_keypad)
    sequences = [""]
    for x in code:
        new_sequences = []
        for base in sequences:
            for seq in get_shortest_path_sequences(x, pos, numeric_keypad):
                new_sequences.append(base + seq)
        sequences = new_sequences
        pos = find_pos(x, numeric_keypad)
    return sequences

def find_pos(button_value, keypad):
        for i in range(len(keypad)):
            for j in range(len(keypad[i])):
                if keypad[i][j] == button_value:
                    return (i, j)
        return (-1, -1)

# Basically do one step of applying a Directional Keypad without actually generating the
# new sequence and instead updating the count of all possible subsequences. 
def evolve_sequence_counts(sequence_counts):
    new_sequence_counts = {}
    for key in sequence_counts.keys():
        sequence = "A" + key # since any sequence for pressing a button starts and ends with A, we can look at them in isolation
        for k in range(len(sequence)-1):
            directional_sequence = get_optimal_sequence(sequence[k], sequence[k+1])
            new_sequence_counts[directional_sequence] = new_sequence_counts.get(directional_sequence, 0) + sequence_counts[key]
    return new_sequence_counts

def get_sequence_counts(n_evolutions, start_sequence):
    sequence_counts = {}
    sequence = "A" + start_sequence
    for k in range(len(sequence)-1):
        directional_sequence = get_optimal_sequence(sequence[k], sequence[k+1])
        sequence_counts[directional_sequence] = sequence_counts.get(directional_sequence, 0) + 1
    for k in range(n_evolutions-1):
        sequence_counts = evolve_sequence_counts(sequence_counts)
    return sequence_counts

def n_button_presses_from_sequence_counts(sequence_counts):
    return sum([sequence_counts[key] * len(key) for key in sequence_counts.keys()])

def compute(codes, n_directional_keypads):
    numeric_keypad = [['7', '8', '9'], ['4', '5', '6'], ['1', '2', '3'], ['', '0', 'A']]
    sum_of_complexities = 0
    for code in codes:
        start_sequences = get_sequences_from_numeric_keypad(code, numeric_keypad) # check all possibilities
        button_counts = []
        for start_sequence in start_sequences:
            # Only maintain counts of independent (sub-)sequences; not the actual sequence itself (that grows exponentially)
            sequence_counts = get_sequence_counts(n_directional_keypads, start_sequence)
            button_counts.append(n_button_presses_from_sequence_counts(sequence_counts))
        # print(f"{min(button_counts)} * {int(code.replace('A', ''))}")
        sum_of_complexities += min(button_counts) * int(code.replace('A', ''))
    return sum_of_complexities

def compute_part_1(input_file_name="input.txt"):
    input = read_input(input_file_name)
    codes = [line.replace('\n', '') for line in input]
    return compute(codes, 2)

# 136780
# That's the right answer! You are one gold star closer to finding the Chief 
# Historian.

# --- Part Two ---

# Just as the missing Historian is released, The Historians realize that a 
# second member of their search party has also been missing this entire 
# time!

# A quick life-form scan reveals the Historian is also trapped in a locked 
# area of the ship. Due to a variety of hazards, robots are once again 
# dispatched, forming another chain of remote control keypads managing 
# robotic-arm-wielding robots.

# This time, many more robots are involved. In summary, there are the 
# following keypads:

# - One directional keypad that you are using.
# - 25 directional keypads that robots are using.
# - One numeric keypad (on a door) that a robot is using.

# The keypads form a chain, just like before: your directional keypad 
# controls a robot which is typing on a directional keypad which controls a 
# robot which is typing on a directional keypad... and so on, ending with the 
# robot which is typing on the numeric keypad.

# The door codes are the same this time around; only the number of robots and 
# directional keypads has changed.

# Find the fewest number of button presses you'll need to perform in order to 
# cause the robot in front of the door to type each code. What is the sum of 
# the complexities of the five codes on your list?

def compute_part_2(input_file_name="input.txt"):
    input = read_input(input_file_name)
    codes = [line.replace('\n', '') for line in input]
    return compute(codes, 25)

# 167538833832712
# That's the right answer! You are one gold star closer to finding the Chief 
# Historian.

if __name__ == "__main__":
    print(f"PART 1: {compute_part_1()}")
    print(f"PART 2: {compute_part_2()}")
