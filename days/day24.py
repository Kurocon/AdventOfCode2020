from days import AOCDay, day

import re
from collections import defaultdict

@day(24)
class Day24(AOCDay):
    test_input = """sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew""".split("\n")

    direction_regex = re.compile(r"(se|sw|ne|nw|e|w)")

    tiles = []

    grid = defaultdict(lambda: True)

    NEIGHBOURS = [(1, 0), (1, -1), (0, 1), (-1, 0), (0, -1), (-1, 1)]

    def east(self, x, y):
        return x+1, y

    def southeast(self, x, y):
        return x+1, y-1

    def northeast(self, x, y):
        return x, y+1

    def west(self, x, y):
        return x-1, y

    def southwest(self, x, y):
        return x, y-1

    def northwest(self, x, y):
        return x-1, y+1

    DIRECTION_MAP = {
        "e": east,
        "se": southeast,
        "ne": northeast,
        "w": west,
        "sw": southwest,
        "nw": northwest
    }

    def get_tile(self, direction):
        position = (0, 0)
        for step in direction:
            position = self.DIRECTION_MAP[step](self, *position)
        return position

    def flip(self, direction):
        pos = self.get_tile(direction)
        self.grid[pos] = not self.grid[pos]

    def count_black_neighbours(self, x, y):
        black = 0
        for dx, dy in self.NEIGHBOURS:
            try:
                if not self.grid[(x + dx, y + dy)]:
                    black += 1
            except KeyError:
                pass
        return black

    @property
    def min_x(self):
        return min(self.grid.keys(), key=lambda x: x[0])[0]

    @property
    def max_x(self):
        return max(self.grid.keys(), key=lambda x: x[0])[0]

    @property
    def min_y(self):
        return min(self.grid.keys(), key=lambda x: x[1])[1]

    @property
    def max_y(self):
        return max(self.grid.keys(), key=lambda x: x[1])[1]

    def flip_day(self):
        new_grid = {}
        for x in range(self.min_x - 2, self.max_x + 2):
            for y in range(self.min_y - 2, self.max_y + 2):
                try:
                    tile = self.grid[(x, y)]
                except KeyError:
                    tile = True
                black = self.count_black_neighbours(x, y)
                if not tile and black == 0 or black > 2:
                    new_grid[(x, y)] = True
                elif tile and black == 2:
                    new_grid[(x, y)] = False
                else:
                    new_grid[(x, y)] = tile
        self.grid = new_grid

    def common(self, input_data):
        # input_data = self.test_input
        self.grid = defaultdict(lambda: True)
        self.tiles = []
        for line in input_data:
            self.tiles.append(self.direction_regex.findall(line))

    def part1(self, input_data):
        for tile in self.tiles:
            self.flip(tile)
        yield sum(not x for x in self.grid.values())

    def part2(self, input_data):
        for tile in self.tiles:
            self.flip(tile)
        self.grid = dict(self.grid)

        self.debug(f"Day 0: {sum(not x for x in self.grid.values())}")
        for i in range(100):
            self.flip_day()
            if i < 10 or (i+1) % 10 == 0:
                self.debug(f"Day {i+1}: {sum(not x for x in self.grid.values())}")
        yield sum(not x for x in self.grid.values())
