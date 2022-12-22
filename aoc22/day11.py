from collections import deque
import io
import math
import operator as op
import re
import sys
from typing import Iterable, IO


class Item:
    def __init__(self, worry_level: int):
        self.worry_level = worry_level


_ops = {"+": op.add, "*": op.mul}


class Monkey:
    def __init__(
        self,
        id: int,
        opstring: str,
        divisor: int,
        throw_to: tuple[int, int],
        items: Iterable[Item],
    ):
        self.id = id
        self.opstring = opstring
        self.divisor = divisor
        self.throw_to = throw_to
        self.inspections = 0
        self.items = deque(items)

    def __repr__(self):
        return f"Monkey({self.id}, {self.opstring}, {self.divisor}, {self.throw_to})"

    def __str__(self):
        return (
            f"Monkey {self.id} {{{' '.join(str(x.worry_level) for x in self.items)}}}"
        )

    def inspect(self):
        """Pop an item, inspect it, and return it."""
        item = self.items.popleft()
        args = self.opstring.split()
        item.worry_level = _ops[args[0]](
            item.worry_level, int(args[1]) if args[1].isdigit() else item.worry_level
        )
        self.inspections += 1
        return item

    def throw(self, item: Item, monkeys: list["Monkey"]):
        """Throw the given item to a monkey in the list depending on this monkey's test."""
        if not item.worry_level % self.divisor:
            monkeys[self.throw_to[0]].items.append(item)
        else:
            monkeys[self.throw_to[1]].items.append(item)


pat = re.compile(
    r"""Monkey (\d+):
  Starting items: ([\d, ]+)
  Operation: new = old (.+)
  Test: divisible by (\d+)
    If true: throw to monkey (\d+)
    If false: throw to monkey (\d+)"""
)


def parse_monkeys(config: IO[str]) -> list[Monkey]:
    monkeys = []

    while True:
        raw = "".join(config.readline() for _ in range(7))
        if not raw:
            break

        mo = pat.match(raw)
        if mo is None:
            raise ValueError("could not parse monkey")

        monkey = Monkey(
            id=int(mo.group(1)),
            opstring=mo.group(3),
            divisor=int(mo.group(4)),
            throw_to=(int(mo.group(5)), int(mo.group(6))),
            items=(Item(int(x)) for x in mo.group(2).split(", ")),
        )
        monkeys.append(monkey)

    return monkeys


def part_a(monkeys: list[Monkey]):
    for _ in range(20):
        for monkey in monkeys:
            while monkey.items:
                item = monkey.inspect()
                item.worry_level //= 3
                monkey.throw(item, monkeys)

    return op.mul(*sorted(m.inspections for m in monkeys)[-2:])


def part_b(monkeys: list[Monkey]):
    lcm = math.lcm(*(m.divisor for m in monkeys))
    for _ in range(10000):
        for monkey in monkeys:
            while monkey.items:
                item = monkey.inspect()
                item.worry_level %= lcm
                monkey.throw(item, monkeys)

    return op.mul(*sorted(m.inspections for m in monkeys)[-2:])


if __name__ == "__main__":
    config = sys.stdin.read()
    monkeys = parse_monkeys(io.StringIO(config))
    print(part_a(monkeys))
    monkeys = parse_monkeys(io.StringIO(config))
    print(part_b(monkeys))
