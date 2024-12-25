import os.path
import re

def read_input(input_file_name):
    input_file = os.path.join(os.path.dirname(__file__), input_file_name)
    with open(input_file, "r") as f:
        lines = f.readlines()
        return lines
    
# --- Day 23: LAN Party ---

# As The Historians wander around a secure area at Easter Bunny HQ, you come 
# across posters for a LAN party scheduled for today! Maybe you can find it; 
# you connect to a nearby datalink port and download a map of the local 
# network (your puzzle input).

# The network map provides a list of every connection between two computers. 
# For example:

# kh-tc
# qp-kh
# de-cg
# ka-co
# yn-aq
# qp-ub
# cg-tb
# vc-aq
# tb-ka
# wh-tc
# yn-cg
# kh-ub
# ta-co
# de-co
# tc-td
# tb-wq
# wh-td
# ta-ka
# td-qp
# aq-cg
# wq-ub
# ub-vc
# de-ta
# wq-aq
# wq-vc
# wh-yn
# ka-de
# kh-ta
# co-tc
# wh-qp
# tb-vc
# td-yn

# Each line of text in the network map represents a single connection; the 
# line kh-tc represents a connection between the computer named kh and the 
# computer named tc. Connections aren't directional; tc-kh would mean 
# exactly the same thing.

# LAN parties typically involve multiplayer games, so maybe you can locate it 
# by finding groups of connected computers. Start by looking for sets of 
# three computers where each computer in the set is connected to the other 
# two computers.

# In this example, there are 12 such sets of three inter-connected 
# computers:

# aq,cg,yn
# aq,vc,wq
# co,de,ka
# co,de,ta
# co,ka,ta
# de,ka,ta
# kh,qp,ub
# qp,td,wh
# tb,vc,wq
# tc,td,wh
# td,wh,yn
# ub,vc,wq

# If the Chief Historian is here, and he's at the LAN party, it would be 
# best to know that right away. You're pretty sure his computer's name starts 
# with t, so consider only sets of three computers where at least one 
# computer's name starts with t. That narrows the list down to 7 sets of 
# three inter-connected computers:

# co,de,ta
# co,ka,ta
# de,ka,ta
# qp,td,wh
# tb,vc,wq
# tc,td,wh
# td,wh,yn

# Find all the sets of three inter-connected computers. How many contain at 
# least one computer with a name that starts with t?

def get_network_map(connections):
    network_map = {}
    for connection in connections:
        c1 = connection[0:2]
        c2 = connection[3:5]
        network_map.setdefault(c1, []).append(c2)
        network_map.setdefault(c2, []).append(c1)
    return network_map

def compute_part_1(input_file_name="input.txt"):
    input = read_input(input_file_name)
    connections = ["".join([x for x in re.findall(r"[a-z]{2}\-[a-z]{2}", line)]) for line in input]
    network_map = get_network_map(connections)
    trios = []
    for c1 in network_map.keys():
        for c2 in network_map[c1]:
            if "t" not in c1[0]+c2[0]: # Exclude any connections that are not related to the chief Historian
                continue
            for c3 in [c3 for c3 in network_map[c1] if c3 in network_map[c2]]:
                if(sorted([c1, c2, c3]) not in trios):
                    trios.append(sorted([c1, c2, c3]))
    return len(trios)

# 1306
# That's the right answer! You are one gold star closer to finding the Chief 
# Historian.

def get_password(computers):
    out = ""
    sorted_computers = sorted(computers)
    for i in range(len(sorted_computers)):
        out += sorted_computers[i] + ("," if i < len(sorted_computers) -1 else "")
    return out

# --- Part Two ---

# There are still way too many results to go through them all. You'll have to 
# find the LAN party another way and go there yourself.

# Since it doesn't seem like any employees are around, you figure they must 
# all be at the LAN party. If that's true, the LAN party will be the largest 
# set of computers that are all connected to each other. That is, for each 
# computer at the LAN party, that computer will have a connection to every 
# other computer at the LAN party.

# In the above example, the largest set of computers that are all connected 
# to each other is made up of co, de, ka, and ta. Each computer in this set 
# has a connection to every other computer in the set:

# ka-co
# ta-co
# de-co
# ta-ka
# de-ta
# ka-de

# The LAN party posters say that the password to get into the LAN party is 
# the name of every computer at the LAN party, sorted alphabetically, then 
# joined together with commas. (The people running the LAN party are clearly 
# a bunch of nerds.) In this example, the password would be co,de,ka,ta.

# What is the password to get into the LAN party?

def compute_part_2(input_file_name="input.txt"):
    input = read_input(input_file_name)
    connections = ["".join([x for x in re.findall(r"[a-z]{2}\-[a-z]{2}", line)]) for line in input]
    network_map = get_network_map(connections)
    pairwise_connected_pcs = [[c] for c in network_map.keys()]
    for i in range(1, max([len(network_map[c]) for c in network_map.keys()]) + 1):
        print(f"{len(pairwise_connected_pcs)} sets of {i} pairwise connected Computers")
        next_pairwise_connected_pcs = []
        for c_list in pairwise_connected_pcs:
            candidates = [c_new for c_new in network_map[c_list[0]] if all(c_new in network_map[c] for c in c_list[1:])]
            for c_new in candidates:
                c_list_new = sorted(c_list + [c_new])
                if(c_list_new not in next_pairwise_connected_pcs):
                    next_pairwise_connected_pcs.append(c_list_new)
        if len(next_pairwise_connected_pcs) == 0:
            return get_password(pairwise_connected_pcs[0])
        pairwise_connected_pcs = next_pairwise_connected_pcs
    return -1

# Takes a bit of time to run:
# 520 sets of 1 pairwise connected Computers
# 3380 sets of 2 pairwise connected Computers
# 11011 sets of 3 pairwise connected Computers
# 26455 sets of 4 pairwise connected Computers
# 45045 sets of 5 pairwise connected Computers
# 55770 sets of 6 pairwise connected Computers
# 50622 sets of 7 pairwise connected Computers
# 33462 sets of 8 pairwise connected Computers
# 15730 sets of 9 pairwise connected Computers
# 5005 sets of 10 pairwise connected Computers
# 975 sets of 11 pairwise connected Computers
# 91 sets of 12 pairwise connected Computers
# 1 sets of 13 pairwise connected Computers)
# bd,dk,ir,ko,lk,nn,ob,pt,te,tl,uh,wj,yl
# That's the right answer! You are one gold star closer to finding the Chief 
# Historian.

if __name__ == "__main__":
    print(f"PART 1: {compute_part_1()}")
    print(f"PART 2: {compute_part_2()}")