import math
from queue import Queue
import string
import sys
from typing import Optional, Sequence


class Elevation:
    """An elevation in the height map."""

    _heightvals = {l: i for i, l in enumerate(string.ascii_lowercase)}
    _heightvals["S"] = 0
    _heightvals["E"] = 25

    def __init__(self, elevation: str):
        self.elevation = elevation
        self.value = self._heightvals[elevation]

    def __str__(self):
        return self.elevation

    def __int__(self):
        return self.value

    def __sub__(self, other):
        return int(self) - int(other)

    def __eq__(self, other):
        return int(self) == int(other)


class HeightMap:
    """Map of coordinates to elevations."""

    def __init__(self, data: Sequence[Sequence[str]]):
        self.width = len(data[0])
        self.height = len(data)
        self._map = {
            (x, y): Elevation(v) for y, r in enumerate(data) for x, v in enumerate(r)
        }
        self.start = next(k for k in self._map if self._map[k].elevation == "S")
        self.end = next(k for k in self._map if self._map[k].elevation == "E")
        self._cache: dict[tuple[int, int], int] = {}
        self._explore()

    def __getitem__(self, key):
        return self._map[key]

    def _paths(self, x: int, y: int):
        curr = self[(x, y)]
        if x - 1 >= 0 and curr - self[(x - 1, y)] <= 1:
            yield (x - 1, y)
        if y - 1 >= 0 and curr - self[(x, y - 1)] <= 1:
            yield (x, y - 1)
        if x + 1 < self.width and curr - self[(x + 1, y)] <= 1:
            yield (x + 1, y)
        if y + 1 < self.height and curr - self[(x, y + 1)] <= 1:
            yield (x, y + 1)

    def _explore(self):
        """explore the map and cache fewest steps to the end location"""
        queue = Queue()

        visited = set()
        queue.put((0, self.end))

        while item := queue.get():
            steps, loc = item

            self._cache[loc] = steps

            if loc not in visited:
                visited.add(loc)
                for next_loc in self._paths(*loc):
                    if next_loc in visited:
                        continue
                    new_item = (steps + 1, next_loc)
                    queue.put(new_item)

            if queue.empty():
                break

    def fewest_steps(self, start: Optional[tuple[int, int]] = None):
        """number of steps for the shortest path (w/o climbing gear) from start to end"""
        start = start or self.start
        return self._cache.get(start, math.inf)

    def zeroes(self):
        """locations at 0 elevation"""
        yield from (x for x in self._map if self._map[x] == 0)


def part_a(data: str):
    height_map = HeightMap(data.splitlines())
    shortest = height_map.fewest_steps()
    return shortest


def part_b(data: str):
    height_map = HeightMap(data.splitlines())
    shortest = min(height_map.fewest_steps(s) for s in height_map.zeroes())
    return shortest


if __name__ == "__main__":
    data = sys.stdin.read()
    print(part_a(data))
    print(part_b(data))
