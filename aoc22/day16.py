from collections import deque
from dataclasses import dataclass, field
import heapq
import itertools as it
import re
import sys
from typing import Iterable, Optional


class Valve:
    def __init__(self, label: str, flow_rate: int):
        self.label = label
        self.flow_rate = flow_rate
        self.tunnels: list[Valve] = []
        self.navtimes: dict[str, int] = {}
        self.opened: Optional[int] = None

    def __repr__(self):
        return f"Valve('{self.label}', {self.flow_rate})"

    def __str__(self):
        return f"Valve {self.label}: flow_rate={self.flow_rate}, tunnels=({', '.join(t.label for t in self.tunnels)});"

    def update_navigation_times(self):
        """Calculate and store the minutes to reachable valves from this valve."""
        visited = set([self.label])
        queue: deque[tuple[int, Valve]] = deque([(0, self)])
        while queue:
            time, curr = queue.popleft()
            visited.add(curr.label)
            if time != 0:
                self.navtimes[curr.label] = time
            for valve in curr.tunnels:
                if valve.label not in visited:
                    queue.append((time + 1, valve))


@dataclass(order=True)
class PathNode:
    minute: int
    cost: int
    label: str
    prev: Optional["PathNode"] = field(default=None, compare=False)

    def visited(self, label: str):
        """Check if the path has visited the provided label."""
        if self.label == label:
            return True
        node = self
        while node := node.prev:
            if node.label == label:
                return True
        return False

    def path(self):
        """Materialize the path to this node as a list, minus the start node AA."""
        if self.label == "AA":
            return []
        node = self
        path = [node]
        while node := node.prev:
            if node.label != "AA":
                path.append(node)
        return path


class ValveSystem:
    _scan_pat = re.compile(
        r"Valve (\w\w) has flow rate=(\d+); tunnel[s]? lead[s]? to valve[s]? ([\w, ]+)"
    )

    def __init__(self, valves: Iterable[Valve]):
        self.valves = {v.label: v for v in valves}

    @classmethod
    def scan(cls, f):
        """Scan the file-obj for valve data to initialize a ValveSystem."""
        flow_rates = {}
        tunnels = {}
        valves = {}

        for line in f:
            mo = cls._scan_pat.match(line)
            if mo is None:
                raise ValueError("invalid valve scan")

            label = mo.group(1)
            flow_rates[label] = int(mo.group(2))
            tunnels[label] = mo.group(3).split(", ")

        valves = {l: Valve(l, f) for l, f in flow_rates.items()}
        for label, to_labels in tunnels.items():
            valves[label].tunnels.extend(valves[l] for l in to_labels)

        for valve in valves.values():
            valve.update_navigation_times()

        return cls(list(sorted(valves.values(), key=lambda v: v.label)))

    def find_paths(self, total_time: int):
        """Find the PathNode endpoints of all valve-opening paths that can be navigated in the alotted time."""
        heap: list[PathNode] = [PathNode(0, 0, "AA")]
        endpoints: list[PathNode] = []

        while heap:
            curr = heapq.heappop(heap)
            curr_valve = self.valves[curr.label]

            options: list[tuple[int, Valve]] = []
            for label, navtime in curr_valve.navtimes.items():
                valve = self.valves[label]
                if curr.visited(label) or valve.flow_rate == 0:
                    continue
                time_opened = 1 + curr.minute + navtime
                if time_opened > total_time:
                    continue
                options.append((time_opened, valve))

            if options:
                for time_opened, valve in options:
                    time_remaining = total_time - time_opened
                    node = PathNode(
                        time_opened,
                        curr.cost + -1 * time_remaining * valve.flow_rate,
                        valve.label,
                        prev=curr,
                    )
                    heapq.heappush(heap, node)

            if curr.label != "AA":
                # every non-start node is a possible endpoint
                endpoints.append(curr)

        return endpoints


def part_a(valve_system: ValveSystem):
    """Maximum pressure that can be released by 1 worker in 30 minutes."""
    endpoints = valve_system.find_paths(30)
    endpoints = sorted(endpoints, key=lambda e: e.cost)
    return -1 * endpoints[0].cost


def part_b(valve_system: ValveSystem):
    """Maximum pressure that can be released by 2 workers in 26 minutes."""
    # find the max pressure for each distinct set of valves opened by a worker
    #   e.g. opening JJ, BB, CC will release more pressure than BB, CC, JJ
    paths: dict[frozenset[str], PathNode] = {}
    for path in valve_system.find_paths(26):
        key = frozenset(p.label for p in path.path())
        if key not in paths or path.cost < paths[key].cost:
            paths[key] = path

    # 2 workers will never open the same valve, so identify disjoint paths
    disjoint_paths = ((a, b) for a, b in it.combinations(paths, 2) if not a & b)

    cost = min(paths[a].cost + paths[b].cost for a, b in disjoint_paths)
    return -1 * cost


if __name__ == "__main__":
    valve_system = ValveSystem.scan(sys.stdin)
    print(part_a(valve_system))
    print(part_b(valve_system))
