from collections.abc import Iterable
import sys


def part_a(lines: Iterable[str]):
    ends = (tuple(int(c) for s in l.split(",") for c in s.split("-")) for l in lines)
    check = lambda x: x[2] <= x[0] and x[1] <= x[3] or x[2] >= x[0] and x[1] >= x[3]
    return sum(check(x) for x in ends)


def part_b(lines: Iterable[str]):
    ends = (tuple(int(c) for s in l.split(",") for c in s.split("-")) for l in lines)
    check = (
        lambda x: x[2] <= x[0] <= x[3]
        or x[2] <= x[1] <= x[3]
        or x[0] <= x[2] <= x[1]
        or x[0] <= x[3] <= x[1]
    )
    return sum(check(x) for x in ends)


def main():
    lines = sys.stdin.read().splitlines()
    print(part_a(lines))
    print(part_b(lines))


if __name__ == "__main__":
    main()
