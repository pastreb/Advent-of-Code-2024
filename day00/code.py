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


def compute_part_1(input_file_name="input.txt"):
    input = read_input(input_file_name)
    numbers = [[int(x) for x in re.findall(r"\d+", line)] for line in input]
    return 0


def compute_part_2(input_file_name="input.txt"):
    input = read_input(input_file_name)
    return 0


if __name__ == "__main__":
    print(f"PART 1: {compute_part_1()}")
    print(f"PART 2: {compute_part_2()}")
