import numpy as np
import sys
from collections import defaultdict
from collections import Counter
from typing import NamedTuple
from typing import List
from typing import Dict
from itertools import combinations
from itertools import permutations

from numpy.lib.function_base import place

np.set_printoptions(threshold=np.inf)


class Asteroid(NamedTuple):
    x: int
    y: int
    val: bool


def parse(s: str) -> np.array:
    lines = s.strip().split("\n")
    inp = [list(line) for line in lines]
    inp = [[1 if char == "#" else 0 for char in line] for line in inp]
    return np.array(inp)


def place_asteroids(arr: np.array) -> List[Asteroid]:
    return [
        Asteroid(i, j, arr[i, j])
        for i in range(arr.shape[0])
        for j in range(arr.shape[1])
    ]


def subset_asteroids(all_points: List[Asteroid]) -> List[Asteroid]:
    return [asteroid for asteroid in all_points if asteroid.val == 1]


def angle_between(p1, p2):
    """https://stackoverflow.com/questions/31735499/calculate-angle-clockwise-between-two-points"""
    # compute the counterclockwise angle (val in radians between -π and π)
    # between the origin and the point (x, y)
    ang1 = np.arctan2(*p1[::-1])
    ang2 = np.arctan2(*p2[::-1])
    # subtract to get the signed clockwise angular difference, res in [-2π, 2π]
    # take mod2π to get a positive angle between 0 and 2π
    # &  convert radians to degrees w/ np.rad2deg.
    return np.rad2deg((ang1 - ang2) % (2 * np.pi))


def all_angles(asteroids: List[Asteroid]) -> Dict[Asteroid, Dict[Asteroid, float]]:
    all_angles_dict = defaultdict(dict)
    for asteroid_1, asteroid_2 in permutations(asteroids, 2):
        angle = angle_between(
            (asteroid_1.x, asteroid_1.y), (asteroid_2.x, asteroid_2.y)
        )
        all_angles_dict[asteroid_1].update({asteroid_2: angle})
    return all_angles_dict


def count_visible(
    asteroids_dict: Dict[Asteroid, Dict[Asteroid, float]]
) -> Dict[Asteroid, int]:
    res = {}
    for asteroid, matching_pairs in asteroids_dict.items():
        n = len(asteroids_dict)
        all_possibilities = 2 * (n - 1)
        print(f"{n=},  {all_possibilities=}")
        # n=406,  all_possibilities=405 with comb
        # n=407,  all_possibilities=812 with perm 2 * (n-1)

        # check for duplicated angle values, meaning we have 2 asteroids in the same line => 1 less visible
        # potentially sum of [n - 1] for n number within the list comprehension
        # print(f"{asteroid=}, {len(matching_pairs.items())=}")  # asteroid=Asteroid(x=4, y=29, val=1), len(matching_pairs.items())=406

        duplicated_values = [
            val for val in Counter(matching_pairs.values()).values() if val > 1
        ]
        # print(f"{duplicated_values=}")
        n_duplicated_values = sum([n - 1 for n in duplicated_values])
        # print(f"{n_duplicated_values=}")
        visible = all_possibilities - n_duplicated_values
        # print(f"{visible=}")
        res[asteroid] = visible
    # max_key = max(res, key=res.get)
    return res


ASTEROID_1 = Asteroid(1, 2, None)
ASTEROID_2 = Asteroid(3, 2, None)
RAW = """.#..#
.....
#####
....#
...##"""
GRID = parse(RAW)
assert np.array_equal(
    GRID,
    np.array(
        [
            [0, 1, 0, 0, 1],
            [0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1],
            [0, 0, 0, 0, 1],
            [0, 0, 0, 1, 1],
        ]
    ),
)
assert place_asteroids(GRID) == [
    Asteroid(x=0, y=0, val=0),
    Asteroid(x=0, y=1, val=1),
    Asteroid(x=0, y=2, val=0),
    Asteroid(x=0, y=3, val=0),
    Asteroid(x=0, y=4, val=1),
    Asteroid(x=1, y=0, val=0),
    Asteroid(x=1, y=1, val=0),
    Asteroid(x=1, y=2, val=0),
    Asteroid(x=1, y=3, val=0),
    Asteroid(x=1, y=4, val=0),
    Asteroid(x=2, y=0, val=1),
    Asteroid(x=2, y=1, val=1),
    Asteroid(x=2, y=2, val=1),
    Asteroid(x=2, y=3, val=1),
    Asteroid(x=2, y=4, val=1),
    Asteroid(x=3, y=0, val=0),
    Asteroid(x=3, y=1, val=0),
    Asteroid(x=3, y=2, val=0),
    Asteroid(x=3, y=3, val=0),
    Asteroid(x=3, y=4, val=1),
    Asteroid(x=4, y=0, val=0),
    Asteroid(x=4, y=1, val=0),
    Asteroid(x=4, y=2, val=0),
    Asteroid(x=4, y=3, val=1),
    Asteroid(x=4, y=4, val=1),
]
# print(all_angles(subset_asteroids(place_asteroids(GRID))))

with open("day10.txt") as f:
    raw = f.read()
    arr = parse(raw)
    # keep only asteroids that are at this point on the grid (val == 1)
    asteroids = subset_asteroids(place_asteroids(arr))
    # compute all angles for pairs of asteroids
    all_angles_dict = all_angles(asteroids)
    all_visible = count_visible(all_angles_dict)
    print(all_visible)
    new_arr = np.zeros(shape=arr.shape, dtype=np.int8)
    to_populate = [
        (asteroid.x, asteroid.y, val) for asteroid, val in all_visible.items()
    ]
    for (i, j, val) in to_populate:
        print(i, j, val)
        new_arr[i, j] = val
