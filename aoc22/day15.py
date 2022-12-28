import itertools as it
import re
import sys


PART_A_Y = 2000000
PART_B_XY_MAX = 4000000


_sensor_report_pat = re.compile(
    r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)"
)


def _parse_sensor_beacon(line: str):
    if mo := _sensor_report_pat.match(line):
        return (
            (int(mo.group(1)), int(mo.group(2))),
            (int(mo.group(3)), int(mo.group(4))),
        )
    raise ValueError("invalid sensor report")


def _distance(p1: tuple[int, int], p2: tuple[int, int]):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


class Sensor:
    def __init__(self, loc: tuple[int, int], beacon: tuple[int, int]):
        self.loc = loc
        self.beacon = beacon
        self.distance = _distance(self.loc, self.beacon)
        self.ybound = (loc[1] - self.distance, loc[1] + self.distance)
        self.xbound = (loc[0] - self.distance, loc[0] + self.distance)
        self.box = (
            (self.xbound[0], loc[1]),
            (loc[0], self.ybound[0]),
            (self.xbound[1], loc[1]),
            (loc[0], self.ybound[1]),
        )

    def xbound_at(self, y: int):
        xbound = []
        for v1, v2 in it.pairwise((self.box[-1],) + self.box):
            inside_ybound = (v1[1] > y) != (v2[1] > y)
            if not inside_ybound:
                continue
            xbound.append(int((v2[0] - v1[0]) * (y - v1[1]) / (v2[1] - v1[1]) + v1[0]))
        return tuple(xbound)

    def __contains__(self, p: tuple[int, int]):
        if (
            p[0] < self.xbound[0]
            or p[0] > self.xbound[1]
            or p[1] < self.ybound[0]
            or p[1] > self.ybound[1]
        ):
            return False

        contains = False
        for x in self.xbound_at(p[1]):
            if p[0] == x:
                return True  # the point is on the boundary
            if p[0] < x:
                contains = not contains

        return contains


def _read_sensors():
    sensors: list[Sensor] = []
    for line in sys.stdin:
        sensors.append(Sensor(*_parse_sensor_beacon(line)))

    sensors = sorted(sensors, key=lambda s: s.distance, reverse=True)

    unique_sensors = [sensors[0]]
    for sensor in sensors[1:]:
        if any(all(v in s for v in sensor.box) for s in unique_sensors):
            continue
        unique_sensors.append(sensor)

    return unique_sensors


def part_a(sensors: list[Sensor], y=PART_A_Y):
    sensors = sorted(sensors, key=lambda s: s.xbound[0])
    xbounds = [s.xbound_at(y) for s in sensors]

    no_beacon = 0
    x = min(xb[0] for xb in xbounds if xb)
    for xbound in xbounds:
        if xbound and xbound[0] <= x <= xbound[1]:
            no_beacon += 1 + xbound[1] - x
            x = xbound[1] + 1

    beacons = set(s.beacon for s in sensors)
    return no_beacon - sum(b[1] == y for b in beacons)


def part_b(sensors: list[Sensor], xy_max=PART_B_XY_MAX):
    sensors = sorted(sensors, key=lambda s: s.loc[0])
    signal = None
    for y in range(xy_max + 1):
        x = 0
        sensors_ = sensors.copy()
        while x <= xy_max:
            for sensor in sensors_:
                if (x, y) in sensor:
                    x = sensor.xbound_at(y)[1] + 1
                    sensors_.remove(sensor)
                    break
            else:
                signal = (x, y)
                break
        if signal:
            break

    assert signal is not None
    return signal[0] * 4000000 + signal[1]


if __name__ == "__main__":
    sensors = _read_sensors()
    print(part_a(sensors))
    print(part_b(sensors))
