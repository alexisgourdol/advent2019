from __future__ import annotations
from typing import NamedTuple, List, Dict

"""
        G - H       J - K - L
       /           /
COM - B - C - D - E - F
               \
                I
"""

RAW = """COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L"""


class Orbit(NamedTuple):
    parent: str
    child: str

    @staticmethod
    def from_string(s: str) -> Orbit:
        parent, child = s.strip().split(")")
        return Orbit(parent, child)


def make_tree(orbits: List[Orbit]) -> Dict:
    parents = {}
    for o in orbits:
        parents[o.child] = o.parent
    return parents


def count_ancestors(child: str, parents: Dict[str, str]) -> int:
    count = 0
    while child != "COM":
        count += 1
        child = parents[child]
    return count


ORBITS = [Orbit.from_string(s) for s in RAW.split("\n")]
TREE = make_tree(ORBITS)
COUNTER = sum([count_ancestors(child, TREE) for child in TREE.keys()])

assert (count_ancestors("D", TREE)) == 3
assert (count_ancestors("L", TREE)) == 7
assert (count_ancestors("COM", TREE)) == 0
assert COUNTER == 42

if __name__ == "__main__":
    with open("day06.txt") as f:
        orbits = [Orbit.from_string(s) for s in f.readlines()]
        tree = make_tree(orbits)
        count = sum([count_ancestors(child, tree) for child in tree.keys()])
        print(f"{count=}")
