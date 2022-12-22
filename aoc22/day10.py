from collections import deque
import sys
import re


instr_pat = re.compile(r"(\w+)(?: (-?\d+)|)")


def run(lines, callback):
    """Run the instructions, calling callback during each cycle."""
    it = iter(lines)

    queue = deque()
    x = 1
    cycle = 1
    block = 0

    while True:
        if block:
            block -= 1
        else:
            if queue:
                x += queue.popleft()
            try:
                mo = instr_pat.match(next(it))
            except StopIteration:
                break
            if mo is None:
                break
            if mo.group(1) == "addx":
                queue.append(int(mo.group(2)))
                block = 1

        callback(cycle, x)
        cycle += 1


def part_a(lines):
    result = [0]

    def sample(cycle, x):
        if not (cycle - 20) % 40:
            result[0] += cycle * x

    run(lines, sample)

    return result[0]


def part_b(lines):
    class State:
        buf = []
        display = []

    state = State()

    def draw(_, x):
        state.buf.append("#" if x - 1 <= len(state.buf) <= x + 1 else ".")
        if len(state.buf) == 40:
            state.display.append("".join(state.buf))
            state.buf = []

    run(lines, draw)

    return "\n".join(state.display)


if __name__ == "__main__":
    lines = sys.stdin.readlines()
    print(part_a(lines))
    print(part_b(lines))
