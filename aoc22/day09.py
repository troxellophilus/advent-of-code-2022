import re
import sys
from typing import Iterable


class Knot:
    """A Knot can move up/down/left/right or follow another knot."""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Knot({self.x}, {self.y})"

    def move(self, direction: str):
        match direction:
            case "R":
                self.x += 1
            case "U":
                self.y -= 1
            case "L":
                self.x -= 1
            case "D":
                self.y += 1
            case _:
                raise ValueError("invalid direction")

    def follow(self, other):
        xdist = other.x - self.x
        ydist = other.y - self.y
        if abs(xdist) > 1 or abs(xdist) + abs(ydist) > 2:
            self.x += xdist // abs(xdist)
        if abs(ydist) > 1 or abs(xdist) + abs(ydist) > 2:
            self.y += ydist // abs(ydist)


instr_pat = re.compile(r"(\w) (\d+)")
"""Regex pattern to match instruction lines."""


def part_a(lines: Iterable[str]):
    head = Knot(0, 0)
    tail = Knot(0, 0)
    tail_visited: set[tuple[int, int]] = set([(0, 0)])

    for instr in lines:
        mo = instr_pat.match(instr)
        if mo is None:
            raise ValueError("bad instruction")

        direction, amount = mo.group(1, 2)
        for _ in range(int(amount)):
            head.move(direction)
            tail.follow(head)
            tail_visited.add((tail.x, tail.y))  # Record where tail's been

    return len(tail_visited)


def part_b(lines: Iterable[str]):
    num_knots = 10
    knots = [Knot(0, 0) for _ in range(num_knots)]
    tail_visited: set[tuple[int, int]] = set([(0, 0)])

    for instr in lines:
        mo = instr_pat.match(instr)
        if mo is None:
            raise ValueError("bad instruction")
        direction, amount = mo.group(1, 2)
        for _ in range(int(amount)):
            knots[0].move(direction)  # The head moves
            for k in range(1, num_knots):
                knots[k].follow(knots[k - 1])  # Other knots follow the one ahead each
            tail_visited.add((knots[-1].x, knots[-1].y))  # Record where tail's been

    return len(tail_visited)


if __name__ == "__main__":
    lines = sys.stdin.readlines()
    print(part_a(lines))
    print(part_b(lines))
