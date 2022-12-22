import itertools as it
import sys


def main():
    lines = sys.stdin.read().splitlines()
    elves = sorted(sum(map(int, g[1])) for g in it.groupby(lines, bool) if g[0])
    print(elves[-1])  # most held by one elf
    print(sum(elves[-3:]))  # total held by top 3


if __name__ == "__main__":
    main()
