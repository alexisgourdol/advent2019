from intcode import parse_opcode
from intcode import run
from intcode import Program
from typing import List
from typing import Tuple
from itertools import permutations


def possible_phase_settings() -> List[Tuple]:
    return permutations(list(range(5)).reverse, 5)


def amplify(program: Program, phase: int, input_signal: int) -> int:
    import ipdb

    ipdb.set_trace()
    prog = program[:]
    prog[0] = phase
    result = run(prog, [input_signal])
    return result


# assert amplify_sequence("4,3,2,1,0", "3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0") == 43210
# assert amplify_sequence("0,1,2,3,4", "3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0") == 54321
# assert amplify_sequence("1,0,4,3,2", "3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0") == 65210
# assert amplify_sequence("4,3,2,1,0", "3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0") == 43210

if __name__ == "__main__":
    p = [int(c) for c in "3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0".split(",")]
    print(amplify(p, 4, 0))
