import sys


scores = {"A": 1, "B": 2, "C": 3, "X": 0, "Y": 3, "Z": 6}
shape_vals = {"A": 1, "B": 2, "C": 4}
val_shapes = {y: x for x, y in shape_vals.items()}
rol = lambda x: 7 & (x << 1 | x >> 2)
ror = lambda x: 7 & (x >> 1 | x << 2)


def main():
    total = 0
    for shape, res in (l.strip().split() for l in sys.stdin):
        if res != "Y":
            shape = val_shapes[(ror if res == "X" else rol)(shape_vals[shape])]
        total += scores[shape] + scores[res]
    print(total)


if __name__ == "__main__":
    main()
