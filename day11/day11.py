from dataclasses import dataclass
from dataclasses import field
from typing import List
from typing import Dict
from intcode import run

# from enum import Enum

# class Direction(Enum):
#     UP = 1
#     LEFT = 2
#     DOWN = 3
#     RIGHT = 4


@dataclass(frozen=True)
class Panel:
    x: int
    y: int


@dataclass
class Robot:
    x: int = 0
    y: int = 0
    compass: str = "up"
    visited: Dict = field(default_factory=dict)

    def paint(self, color: int) -> None:
        if color in (0, 1):
            self.visited[Panel(self.x, self.y)] = color
        else:
            raise ValueError(f"Invalid color : {color}")

    def rotate(self, new_direction: int) -> None:
        if new_direction not in (0, 1):
            raise ValueError(f"Invalid new_direction : {new_direction}")

        if new_direction == 0:
            if self.compass == "up":
                self.compass = "left"
            elif self.compass == "left":
                self.compass = "down"
            elif self.compass == "down":
                self.compass = "right"
            elif self.compass == "right":
                self.compass = "up"

        if new_direction == 1:
            if self.compass == "up":
                self.compass = "right"
            elif self.compass == "left":
                self.compass = "up"
            elif self.compass == "down":
                self.compass = "left"
            elif self.compass == "right":
                self.compass = "down"

    def move(self) -> None:
        # Grid shape is unkown, we only move relative to initial position (0, 0)
        if self.compass == "up":
            self.y += 1
        if self.compass == "left":
            self.x -= 1
        if self.compass == "down":
            self.y -= 1
        if self.compass == "right":
            self.x += 1


if __name__ == "__main__":
    fake_inputs = [(1, 0), (0, 1), (1, 1), (1, 1)]
    r = Robot()
    r.paint(0)
    for instruction in fake_inputs:
        r.rotate(instruction[1])
        r.move()
        r.paint(instruction[0])
    print(r)

    with open("day11.txt") as f:
        inp = f.read().strip()
    program = [int(el) for el in inp.split(",")]
    print(program)
    run(program, [0])
