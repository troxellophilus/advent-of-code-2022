from itertools import zip_longest
import json
import sys

PacketData = list["PacketData"] | int

EMPTY = -1


def _lt(px: PacketData, py: PacketData):
    def _compare_recursive(px: PacketData, py: PacketData):
        if isinstance(px, int) and isinstance(py, int):
            yield px < py, px > py

        else:
            if isinstance(px, list) and isinstance(py, int):
                if py == EMPTY:  # right side ran out first
                    yield False, True
                else:
                    py = [py]
            elif isinstance(px, int) and isinstance(py, list):
                if px == EMPTY:  # left side ran out first
                    yield True, False
                else:
                    px = [px]

            assert isinstance(px, list) and isinstance(py, list)
            for px_, py_ in zip_longest(px, py, fillvalue=-1):
                yield from _compare_recursive(px_, py_)

    for lt, gt in _compare_recursive(px, py):
        if lt:
            return True
        elif gt:
            return False
        # elements were equal, keep going
    else:
        # all elements were equal
        return False


class Packet:
    def __init__(self, data: list[PacketData]):
        self.data = data

    def __repr__(self):
        return f"Packet({json.dumps(self.data)})"

    def __lt__(self, other: "Packet"):
        return not self.__eq__(other) and _lt(self.data, other.data)

    def __le__(self, other: "Packet"):
        return self.__eq__(other) or _lt(self.data, other.data)

    def __eq__(self, other: "Packet"):
        return self.data == other.data


def read_packets():
    data = sys.stdin.read()
    return list(
        Packet(json.loads(line))
        for raw_pair in data.strip().split("\n\n")
        for line in raw_pair.split("\n")
    )


def part_a(packets: list[Packet]):
    pairs = [tuple(p) for p in zip(*([iter(packets)] * 2), strict=True)]
    return sum(idx + 1 for idx, pair in enumerate(pairs) if pair[0] <= pair[1])


def part_b(packets: list[Packet]):
    dividers = [Packet([[2]]), Packet([[6]])]
    packets = sorted(packets + dividers)
    divider_indexes = tuple(i + 1 for i, p in enumerate(packets) if p in dividers)
    assert len(divider_indexes) == 2
    return divider_indexes[0] * divider_indexes[1]


if __name__ == "__main__":
    packets = read_packets()
    print(part_a(packets))
    print(part_b(packets))
