import operator as op
import sys


shapes = {"A": 1, "X": 1, "B": 2, "Y": 2, "C": 3, "Z": 3}


def main():
    values = (tuple(shapes[s] for s in l.strip().split()) for l in sys.stdin)
    win_loss = lambda x, y: {1: op.lt, 2: op.gt}[abs(x - y)](x, y)
    total = sum((3 if x == y else 6 if win_loss(x, y) else 0) + y for x, y in values)
    print(total)


if __name__ == "__main__":
    main()
