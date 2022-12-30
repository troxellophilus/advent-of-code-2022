import itertools as it
import sys


Rock = tuple[int, ...]

rocks: tuple[Rock, ...] = (
    (0b0011110,),
    (
        0b0001000,
        0b0011100,
        0b0001000,
    ),
    (
        0b0011100,
        0b0000100,
        0b0000100,
    ),
    (
        0b0010000,
        0b0010000,
        0b0010000,
        0b0010000,
    ),
    (
        0b0011000,
        0b0011000,
    ),
)

rock_iter = it.cycle(rocks)

gas_iter = it.cycle(sys.stdin.read())

chamber: list[int] = [0b1111111]

rock = next(rock_iter)
rocks_stopped = 0
rock_lvl = len(chamber) + 3
while True:
    match next(gas_iter):
        case ">":
            if not any(r & 1 for r in rock):
                test_rock = tuple(r >> 1 for r in rock)
                if not any(r & c for r, c in zip(test_rock, chamber[rock_lvl:])):
                    rock = test_rock
        case "<":
            if not any(r & 64 for r in rock):
                test_rock = tuple(r << 1 for r in rock)
                if not any(r & c for r, c in zip(test_rock, chamber[rock_lvl:])):
                    rock = test_rock
        case _:
            raise ValueError("invalid gas")

    rock_lvl -= 1

    if any(r & c for r, c in zip(rock, chamber[rock_lvl:])):
        for i, (r, c) in enumerate(zip(rock, chamber[rock_lvl + 1 :])):
            chamber[rock_lvl + 1 + i] |= r
        chamber.extend(rock[len(chamber[rock_lvl:]) - 1 :])
        rocks_stopped += 1
        if rocks_stopped == 1000000000000:
            break
        if not rocks_stopped % 1000000:
            print(rocks_stopped)
        # drop a new rock
        rock_lvl = len(chamber) + 3
        rock = next(rock_iter)


for item in chamber[::-1][:-1]:
    print(
        "".join(
            "#" if x == "1" else "."
            for x in "0" * (7 - len(bin(item)[2:])) + bin(item)[2:]
        )
    )
    # print(bin(item))

print(len(chamber) - 1)
