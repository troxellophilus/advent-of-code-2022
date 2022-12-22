from functools import reduce
import string
import sys


priority = {l: i + 1 for i, l in enumerate(string.ascii_letters)}


def main():
    rucksacks = sys.stdin.read().splitlines()

    # part a
    find_error = lambda r, l: (set(r[:l]) & set(r[l:])).pop()
    total = sum(priority[find_error(r, len(r) // 2)] for r in rucksacks)
    print(total)

    # part b
    groups = zip(*([iter(rucksacks)] * 3))
    items = (reduce(lambda x, y: x & y, map(set, g)).pop() for g in groups)
    total = sum(priority[x] for x in items)
    print(total)


if __name__ == "__main__":
    main()
