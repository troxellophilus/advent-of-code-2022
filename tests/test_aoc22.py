from pathlib import Path

from aoc22 import day04


def get_test_data(filename):
    return (Path(__file__).parent / "data" / filename).read_text()


def test_day04():
    data = get_test_data("day04.txt")
    lines = data.splitlines()
    assert day04.part_a(lines) == 2
    assert day04.part_b(lines) == 4
