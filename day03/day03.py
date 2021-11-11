from collections import namedtuple
from typing import Tuple, List, Set


def move(instructions: List[str]) -> List[Tuple[int, int]]:
    """For each instruction, add the new points to the list `path`"""
    path = []
    position = (0, 0)

    for instruction in instructions:
        # steps= + 1 to offset properly the range values
        if instruction[0] == "U":
            steps = int(instruction[1:])
            for y in range(position[1] + 1, position[1] + steps + 1):
                path.append((position[0], y))
            position = (position[0], position[1] + steps)

        if instruction[0] == "D":
            steps = int(instruction[1:])
            for y in range(position[1] - 1, position[1] - steps - 1, -1):
                path.append((position[0], y))
            position = (position[0], position[1] - steps)

        if instruction[0] == "L":
            steps = int(instruction[1:])
            for x in range(position[0] - 1, position[0] - steps - 1, -1):
                path.append((x, position[1]))
            position = (position[0] - steps, position[1])

        if instruction[0] == "R":
            steps = int(instruction[1:])
            for x in range(position[0] + 1, position[0] + steps + 1):
                path.append((x, position[1]))
            position = (position[0] + steps, position[1])

    return path


def compare_paths(instructions_1: str, instructions_2: str) -> Set:
    path_1 = set(move(instructions_1))
    path_2 = set(move(instructions_2))
    return path_1.intersection(path_2)


def distance(instructions_1: str, instructions_2: str) -> int:
    comparison = compare_paths(instructions_1, instructions_2)
    min_distance = 99_999
    if not comparison:
        return min_distance
    comparison_sums = [abs(pairs[0]) + abs(pairs[1]) for pairs in comparison]
    return min(comparison_sums)


### PART 2
def move_until(instructions: List[str], intersection: Tuple) -> int:
    """For each instruction, add the new points to the list `path`"""
    path = []
    position = (0, 0)
    counter = 0

    for instruction in instructions:
        # steps= + 1 to offset properly the range values
        if instruction[0] == "U":
            steps = int(instruction[1:])
            for y in range(position[1] + 1, position[1] + steps + 1):
                new_position = (position[0], y)
                path.append(new_position)
                counter += 1
                if new_position == intersection:
                    return counter
            # might have to set position as path[-1]
            position = (position[0], position[1] + steps)

        if instruction[0] == "D":
            steps = int(instruction[1:])
            for y in range(position[1] - 1, position[1] - steps - 1, -1):
                new_position = (position[0], y)
                path.append(new_position)
                counter += 1
                if new_position == intersection:
                    return counter
            position = (position[0], position[1] - steps)

        if instruction[0] == "L":
            steps = int(instruction[1:])
            for x in range(position[0] - 1, position[0] - steps - 1, -1):
                new_position = (x, position[1])
                path.append(new_position)
                counter += 1
                if new_position == intersection:
                    return counter
            position = (position[0] - steps, position[1])

        if instruction[0] == "R":
            steps = int(instruction[1:])
            for x in range(position[0] + 1, position[0] + steps + 1):
                new_position = (x, position[1])
                path.append(new_position)
                counter += 1
                if new_position == intersection:
                    return counter
            position = (position[0] + steps, position[1])

    return 99_999


def best_steps(instructions_1: str, instructions_2: str) -> None:
    # determine crossing points -> compare_paths() already coded
    intersections = compare_paths(instructions_1, instructions_2)

    # count steps until each crossing point -> move_until
    steps_count = []
    for crossing_point in intersections:
        steps_1 = move_until(instructions_1, crossing_point)
        steps_2 = move_until(instructions_2, crossing_point)
        steps_count.append(steps_1 + steps_2)

    # compare lowest number of steps
    return min(steps_count)


if __name__ == "__main__":
    wire_1 = ["R8", "U5", "L5", "D3"]
    wire_2 = ["U7", "R6", "D4", "L4"]
    assert distance(wire_1, wire_2) == 6
    assert best_steps(wire_1, wire_2) == 30

    wire_3 = ["R75", "D30", "R83", "U83", "L12", "D49", "R71", "U7", "L72"]
    wire_4 = ["U62", "R66", "U55", "R34", "D71", "R55", "D58", "R83"]
    assert distance(wire_3, wire_4) == 159
    assert best_steps(wire_3, wire_4) == 610

    wire_5 = [
        "R98",
        "U47",
        "R26",
        "D63",
        "R33",
        "U87",
        "L62",
        "D20",
        "R33",
        "U53",
        "R51",
    ]
    wire_6 = ["U98", "R91", "D20", "R16", "D67", "R40", "U7", "R15", "U6", "R7"]
    assert distance(wire_5, wire_6) == 135
    # assert best_steps(wire_3, wire_4) == 410

    with open("day03.txt") as f:
        wires = f.readlines()
        wire_one, wire_two = [wire.split(",") for wire in wires]
        print(f"{distance(wire_one, wire_two)=}")
        print(f"{best_steps(wire_one, wire_two)=}")

"""
class Wire(NamedTuple):
    path: str
    instructions: List[str]
    position: Tuple[int, int] = (0, 0)
    possibilities: List[Tuple[int, int]] = []

    def parse(self) -> None:
        self.instructions = self.path.split(",")

    def move(self) -> None:
        for instruction in self.instructions:
            if instruction[0] == "U":
                steps = int(instruction[1])
                for y in range(self.position[1], self.position[1] + steps):
                    self.possibilities.append((self.position[0], y))

            if instruction[0] == "D":
                pass
            if instruction[0] == "L":
                pass
            if instruction[0] == "R":
                pass
"""
