from collections import deque
import itertools as it
import sys
from typing import IO


START = (500, 0)


def _options(loc: tuple[int, int]):
    yield loc[0], loc[1] + 1
    yield loc[0] - 1, loc[1] + 1
    yield loc[0] + 1, loc[1] + 1


def _scan_rock_traces(fobj: IO[str]):
    """parse input into (((x, y), ...), ...)"""
    coord_gen = ((y.split(",") for y in x.strip().split(" -> ")) for x in fobj)
    return ((tuple(map(int, y)) for y in x) for x in coord_gen)


class Cave:
    def __init__(self):
        self._rock = set()
        self._sand = set()
        self.scan_floor = 0
        self.floor = 0

    @classmethod
    def scan(cls, fobj: IO[str]):
        cave = cls()
        for trace in _scan_rock_traces(fobj):
            for start, stop in it.pairwise(trace):
                if start[0] == stop[0]:
                    for y in range(min(start[1], stop[1]), max(start[1], stop[1]) + 1):
                        cave._rock.add((start[0], y))
                elif start[1] == stop[1]:
                    for x in range(min(start[0], stop[0]), max(start[0], stop[0]) + 1):
                        cave._rock.add((x, start[1]))
                else:
                    raise ValueError("lines must be vertical or horizontal")
        cave.scan_floor = max(y for _, y in cave._rock)
        cave.floor = cave.scan_floor + 2
        return cave

    def filled(self, loc: tuple[int, int]):
        return loc in self._rock or loc in self._sand

    def pour(self):
        start = START
        while True:
            loc = next(it.filterfalse(self.filled, _options(start)), None)
            if loc and loc[1] < self.floor:
                start = loc
            else:
                self._sand.add(start)
                yield start
                if start[1] > 0:
                    start = START
                else:
                    break

    @property
    def sand(self):
        return len(self._sand)


def part_a(cave: Cave):
    deque(it.takewhile(lambda l: l[1] < cave.scan_floor, cave.pour()), 0)
    return cave.sand - 1


def part_b(cave: Cave):
    deque(cave.pour(), 0)  # efficiently exhaust the iterator
    return cave.sand


if __name__ == "__main__":
    cave = Cave.scan(sys.stdin)
    print(part_a(cave))
    print(part_b(cave))
