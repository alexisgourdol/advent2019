"""
After solving this problem I went back and refactored this code,
under the assumption that I'd probably have to use it again on a later day.
"""
from sys import displayhook
from typing import List, NamedTuple, Tuple
from enum import Enum
from itertools import permutations


class Opcode(Enum):
    ADD = 1
    MULTIPLY = 2
    STORE_INPUT = 3
    SEND_TO_OUTPUT = 4
    JUMP_IF_TRUE = 5
    JUMP_IF_FALSE = 6
    LESS_THAN = 7
    EQUALS = 8
    END_PROGRAM = 99


Modes = List[int]


def parse_opcode(opcode: int, num_modes: int = 3) -> Tuple[Opcode, Modes]:
    opcode_part = opcode % 100

    modes: List[int] = []
    opcode = opcode // 100

    for _ in range(num_modes):
        modes.append(opcode % 10)
        opcode = opcode // 10

    return Opcode(opcode_part), modes


Program = List[int]


def run_program(program: Program, input: List[int]) -> List[int]:
    program = program[:]
    output = []

    pos = 0

    def get_value(pos: int, mode: int) -> int:
        if mode == 0:
            # pointer mode
            return program[program[pos]]
        elif mode == 1:
            # immediate mode
            return program[pos]
        else:
            raise ValueError(f"unknown mode: {mode}")

    while True:
        opcode, modes = parse_opcode(program[pos])

        if opcode == Opcode.END_PROGRAM:
            break
        elif opcode == Opcode.ADD:
            value1 = get_value(pos + 1, modes[0])
            value2 = get_value(pos + 2, modes[1])
            program[program[pos + 3]] = value1 + value2
            pos += 4
        elif opcode == Opcode.MULTIPLY:
            value1 = get_value(pos + 1, modes[0])
            value2 = get_value(pos + 2, modes[1])
            program[program[pos + 3]] = value1 * value2
            pos += 4
        elif opcode == Opcode.STORE_INPUT:
            # Get input and store at location
            loc = program[pos + 1]
            input_value = input[0]
            input = input[1:]
            program[loc] = input_value
            pos += 2
        elif opcode == Opcode.SEND_TO_OUTPUT:
            # Get output from location
            value = get_value(pos + 1, modes[0])
            output.append(value)
            pos += 2

        elif opcode == Opcode.JUMP_IF_TRUE:
            # jump if true
            value1 = get_value(pos + 1, modes[0])
            value2 = get_value(pos + 2, modes[1])

            if value1 != 0:
                pos = value2
            else:
                pos += 3

        elif opcode == Opcode.JUMP_IF_FALSE:
            value1 = get_value(pos + 1, modes[0])
            value2 = get_value(pos + 2, modes[1])

            if value1 == 0:
                pos = value2
            else:
                pos += 3

        elif opcode == Opcode.LESS_THAN:
            value1 = get_value(pos + 1, modes[0])
            value2 = get_value(pos + 2, modes[1])

            if value1 < value2:
                program[program[pos + 3]] = 1
            else:
                program[program[pos + 3]] = 0
            pos += 4

        elif opcode == Opcode.EQUALS:
            value1 = get_value(pos + 1, modes[0])
            value2 = get_value(pos + 2, modes[1])

            if value1 == value2:
                program[program[pos + 3]] = 1
            else:
                program[program[pos + 3]] = 0
            pos += 4

        else:
            raise RuntimeError(f"invalid opcode: {opcode}")

    return output


def run_amplifier(
    program: Program, phase: int, input_signal: int = 0
) -> int:  # attention : phase 1st param, inp_sign 2nd
    inputs = [phase, input_signal]
    (output_val,) = run_program(program, inputs)
    return output_val


def run(program: Program, phases: List[int]):

    last_output = 0
    for phase in phases:
        last_output = run_amplifier(program, phase, last_output)

    return last_output


def best_output(program: Program) -> int:
    res = []
    for phase_list in permutations(range(5)):
        res.append(run(program, phase_list))

    return max(res)


def repeated_run(program: Program) -> int:
    res = 0
    for phase_list in permutations(range(5, 10)):
        res += best_output(program)
    return res


with open("day07.txt") as f:
    program = f.readline().strip().split(",")
    program = [int(c) for c in program]

    print(best_output(program))
    print(repeated_run(program))
