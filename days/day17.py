from collections import defaultdict

from days import AOCDay, day

ACTIVE = "#"
INACTIVE = "."

@day(17)
class Day17(AOCDay):
    test_input = """.#.
..#
###""".split("\n")

    universe = defaultdict(lambda: False)

    def test(self, input_data):
        self.common(self.test_input)
        assert len(self.neighbours(0, 0, 0)) == 26, "Num neighbours pt1 incorrect"
        assert len(self.neighbours2(0, 0, 0, 0)) == 80, "Num neighbours pt2 incorrect"
        assert next(self.part1(self.test_input)) == 112, "Test case for part 1 failed"
        self.common(self.test_input)
        assert next(self.part2(self.test_input)) == 848, "Test case for part 2 failed"

    def common(self, input_data):
        self.universe = defaultdict(lambda: False)
        for y, line in enumerate(input_data):
            for x, c in enumerate(line):
                self.universe[x, y, 0, 0] = c == ACTIVE

    def neighbours(self, x, y, z):
        return [
            (x+dx, y+dy, z+dz, 0)
            for dx in [-1, 0, 1] for dy in [-1, 0, 1] for dz in [-1, 0, 1] if (dx, dy, dz) != (0, 0, 0)
        ]

    def neighbours2(self, x, y, z, w):
        return [
            (x+dx, y+dy, z+dz, w+dw)
            for dx in [-1, 0, 1] for dy in [-1, 0, 1] for dz in [-1, 0, 1] for dw in [-1, 0, 1]
            if (dx, dy, dz, dw) != (0, 0, 0, 0)
        ]

    def active_neighbours(self, x, y, z):
        return sum(self.universe[n] for n in self.neighbours(x, y, z))

    def active_neighbours2(self, x, y, z, w):
        return sum(self.universe[n] for n in self.neighbours2(x, y, z, w))

    def minmax_coords(self):
        keys = self.universe.keys()
        minx = min(keys, key=lambda x: x[0])[0]
        maxx = max(keys, key=lambda x: x[0])[0]
        miny = min(keys, key=lambda x: x[1])[1]
        maxy = max(keys, key=lambda x: x[1])[1]
        minz = min(keys, key=lambda x: x[2])[2]
        maxz = max(keys, key=lambda x: x[2])[2]
        minw = min(keys, key=lambda x: x[3])[3]
        maxw = max(keys, key=lambda x: x[3])[3]
        return minx, maxx, miny, maxy, minz, maxz, minw, maxw

    def step(self):
        new_universe = defaultdict(lambda: False)
        minx, maxx, miny, maxy, minz, maxz, _, _ = self.minmax_coords()
        for z in range(minz - 1, maxz + 2):
            for y in range(miny - 1, maxy + 2):
                for x in range(minx - 1, maxx + 2):
                    is_active = self.universe[x, y, z, 0]
                    num_active = self.active_neighbours(x, y, z)
                    if is_active:
                        new_universe[x, y, z, 0] = num_active in [2, 3]
                    else:
                        new_universe[x, y, z, 0] = num_active == 3
        self.universe = new_universe

    def step2(self):
        new_universe = defaultdict(lambda: False)
        minx, maxx, miny, maxy, minz, maxz, minw, maxw = self.minmax_coords()
        for w in range(minw - 1, maxw + 2):
            for z in range(minz - 1, maxz + 2):
                for y in range(miny - 1, maxy + 2):
                    for x in range(minx - 1, maxx + 2):
                        is_active = self.universe[x, y, z, w]
                        num_active = self.active_neighbours2(x, y, z, w)
                        if is_active:
                            new_universe[x, y, z, w] = num_active in [2, 3]
                        else:
                            new_universe[x, y, z, w] = num_active == 3
        self.universe = new_universe

    def print_universe(self):
        minx, maxx, miny, maxy, minz, maxz, _, _ = self.minmax_coords()
        res = ""
        for z in range(minz, maxz + 1):
            res += f"z={z}\n"
            for y in range(miny, maxy + 1):
                for x in range(minx, maxx + 1):
                    res += ACTIVE if self.universe[x, y, z, 0] else INACTIVE
                res += "\n"
            res += "\n"
        self.debug(res)

    def print_universe2(self):
        minx, maxx, miny, maxy, minz, maxz, minw, maxw = self.minmax_coords()
        res = ""
        for w in range(minw, maxw + 1):
            for z in range(minz, maxz + 1):
                res += f"z={z}, w={w}\n"
                for y in range(miny, maxy + 1):
                    for x in range(minx, maxx + 1):
                        res += ACTIVE if self.universe[x, y, z, w] else INACTIVE
                    res += "\n"
                res += "\n"
        self.debug(res)

    def part1(self, input_data):
        assert len(self.neighbours(0, 0, 0)) == 26
        self.debug("Before cycles:")
        self.print_universe()
        for i in range(6):
            self.step()
            self.debug(f"After cycle {i+1}:")
            self.print_universe()
        yield sum(self.universe.values())

    def part2(self, input_data):
        assert len(self.neighbours2(0, 0, 0, 0)) == 80
        self.debug("Before cycles:")
        self.print_universe2()
        for i in range(6):
            self.step2()
            self.debug(f"After cycle {i+1}:")
            self.print_universe2()
        yield sum(self.universe.values())
