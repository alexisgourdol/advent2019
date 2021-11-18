from typing import List
from typing import Tuple
from typing import NamedTuple
import math


class Asteroid(NamedTuple):
    x: int
    y: int


Asteroids = List[Asteroid]


def parse(raw: str) -> Asteroids:
    return [
        Asteroid(x, y)
        for y, line in enumerate(raw.strip().split("\n"))
        for x, c in enumerate(line)
        if c == "#"
    ]


def count_visible(asteroids: Asteroids, station: Asteroid) -> int:
    """Pick any point and rewrite the coordinates of other points to make it the center
    Then compute the slopes and check the equivalent ones
    Also keep track of the direction"""

    # recenter
    slopes = set()
    for x, y in asteroids:
        dx = x - station.x
        dy = y - station.y

        gcd = math.gcd(dx, dy)

        # if the asteroid is already the station, pass
        if dx == dy == 0:
            pass
        # we don't want to divide by zero and gcd is only 0 when both dx and dy == 0 as above
        # so we're good to go
        else:
            # adding only one slope (dy / dx) will "merge" some entries that are on the same line
            # e.g. (-1.0, 0.0) and (1.0, 0.0) as one entry from As(1,2)
            # whereas adding a tuple normalized by gcd will preserve both entries
            slopes.add((dx / gcd, dy / gcd))
    return len(slopes)


def best_station(asteroids: Asteroids) -> Tuple[Asteroid, int]:
    best = (None, 0)
    for asteroid in asteroids:
        count = count_visible(asteroids, asteroid)
        best = (asteroid, count) if count > best[1] else best
    return best


RAW = """.#..#
.....
#####
....#
...##
"""

gcd_effect = """
    station=Asteroid(x=1, y=2)
    dx=-1, dy=0, gcd=1
    dx/gcd=-1.0, dy/gcd=0.0
    {(-1.0, 0.0), (0.0, -1.0), (3.0, -2.0)}

    station=Asteroid(x=1, y=2)
    dx=1, dy=0, gcd=1
    dx/gcd=1.0, dy/gcd=0.0
    {(-1.0, 0.0), (1.0, 0.0), (0.0, -1.0), (3.0, -2.0)}

    station=Asteroid(x=1, y=2)
    dx=2, dy=0, gcd=2
    dx/gcd=1.0, dy/gcd=0.0
    {(-1.0, 0.0), (1.0, 0.0), (0.0, -1.0), (3.0, -2.0)}

    station=Asteroid(x=1, y=2)
    dx=3, dy=0, gcd=3
    dx/gcd=1.0, dy/gcd=0.0
    {(-1.0, 0.0), (1.0, 0.0), (0.0, -1.0), (3.0, -2.0)}
    """

ASTEROIDS = parse(RAW)
assert best_station(ASTEROIDS) == (Asteroid(x=3, y=4), 8)

with open("day10.txt") as f:
    raw = f.read()

asteroids = parse(raw)
print(best_station(asteroids))
