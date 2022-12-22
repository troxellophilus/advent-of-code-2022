from collections.abc import Sequence
import itertools as it
import sys


def part_a(lines: Sequence[str]):
    h = len(lines)
    w = len(lines[0])

    vis = set()
    for i, row in enumerate(lines[1:-1]):
        vis |= set((i + 1, j) for j in range(1, w - 1) if row[j] > max(row[:j]))
        vis |= set((i + 1, j) for j in range(1, w - 1) if row[j] > max(row[j + 1 :]))

    cols = list(map(list, zip(*lines)))
    for i, col in enumerate(cols[1:-1]):
        vis |= set((j, i + 1) for j in range(1, h - 1) if col[j] > max(col[:j]))
        vis |= set((j, i + 1) for j in range(1, h - 1) if col[j] > max(col[j + 1 :]))

    return (2 * (h + w) - 4) + len(vis)


def part_b(lines: Sequence[str]):
    h, w = len(lines), len(lines[0])
    cols = list(map(list, zip(*lines)))

    def view_score(ht, seq):
        return min(len(seq), 1 + sum(1 for _ in it.takewhile(lambda t: ht > t, seq)))

    def scenic_score(r: int, c: int):
        ht = lines[r][c]
        left = view_score(ht, lines[r][:c][::-1])
        right = view_score(ht, lines[r][c + 1 :])
        up = view_score(ht, cols[c][:r][::-1])
        down = view_score(ht, cols[c][r + 1 :])
        return left * right * up * down

    return max(scenic_score(r, c) for r in range(h) for c in range(w))


if __name__ == "__main__":
    lines = sys.stdin.read().splitlines()
    print(part_a(lines))
    print(part_b(lines))
