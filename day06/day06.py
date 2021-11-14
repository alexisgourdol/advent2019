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

RAW_2 = """COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
K)YOU
I)SAN"""


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


def count_ancestors(child: str, parents: Dict[str, str], stop: str = "COM") -> int:
    count = 0
    while child != stop:
        count += 1
        child = parents[child]
    return count


ORBITS = [Orbit.from_string(s) for s in RAW_2.split("\n")]
TREE = make_tree(ORBITS)
COUNTER = sum([count_ancestors(child, TREE) for child in TREE.keys()])

# assert (count_ancestors("D", TREE)) == 3
# assert (count_ancestors("L", TREE)) == 7
# assert (count_ancestors("COM", TREE)) == 0
# assert COUNTER == 42

## PART 2
def find_common_ancestor(parents: Dict[str, str]) -> str:
    you_ancestors = []
    santa_ancestors = []
    for k in parents.keys():
        if k == "YOU":
            while k != "COM":
                you_ancestors.append(parents[k])
                k = parents[k]
        if k == "SAN":
            while k != "COM":
                santa_ancestors.append(parents[k])
                k = parents[k]

    all_ancestors = set(you_ancestors).intersection(set(santa_ancestors))
    all_ancestors_count = [(a, count_ancestors(a, parents)) for a in all_ancestors]
    all_ancestors_dict = {c: a for (a, c) in all_ancestors_count}
    m = max(all_ancestors_dict.keys())
    stop = all_ancestors_dict[m]

    return stop


def count_steps(parents: Dict[str, str]) -> int:
    stop = find_common_ancestor(parents)
    return (
        count_ancestors("YOU", parents, stop=stop)
        + count_ancestors("SAN", parents, stop=stop)
        - 2
    )


if __name__ == "__main__":
    with open("day06.txt") as f:
        orbits = [Orbit.from_string(s) for s in f.readlines()]
        tree = make_tree(orbits)
        count = sum([count_ancestors(child, tree) for child in tree.keys()])
        print(f"{count=}")
        print(f"{count_steps(tree)=}")
