from days import AOCDay, day

FLOOR = 0
EMPTY_SEAT = 1
OCCUPIED_SEAT = 2

@day(11)
class Day11(AOCDay):
    print_debug = "c12"
    test_input = """L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL""".split("\n")

    seats = []

    def get_layout(self):
        res = ""
        for line in self.seats:
            for col in line:
                if col == FLOOR:
                    res += "."
                elif col == EMPTY_SEAT:
                    res += "L"
                elif col == OCCUPIED_SEAT:
                    res += "#"
            res += "\n"
        return res

    def common(self, input_data):
        self.seats = []
        for line in input_data:
            self.seats.append([])
            for c in line:
                if c == ".":
                    self.seats[-1].append(FLOOR)
                elif c == "L":
                    self.seats[-1].append(EMPTY_SEAT)
                elif c == "#":
                    self.seats[-1].append(OCCUPIED_SEAT)
                else:
                    raise ValueError(f"Invalid char {c}")

    def neighbours(self, x, y):
        ns = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        return [self.seats[y+ny][x+nx] for ny, nx in ns
                if 0 <= (y+ny) < len(self.seats) and 0 <= (x+nx) < len(self.seats[0])]

    def do_tick(self, neighbour_func, occupied_count = 4):
        # If a seat is empty (L) and there are no occupied seats adjacent to it, the seat becomes occupied.
        # If a seat is occupied (#) and four or more seats adjacent to it are also occupied, the seat becomes empty.
        # Otherwise, the seat's state does not change.
        new_layout = []
        changed = False
        for y, row in enumerate(self.seats):
            new_layout.append([])
            for x, col in enumerate(row):
                neighbours = neighbour_func(x, y)
                if col == EMPTY_SEAT and len(list(filter(lambda x: x == OCCUPIED_SEAT, neighbours))) == 0:
                    new_layout[-1].append(OCCUPIED_SEAT)
                    if not changed:
                        changed = True
                elif col == OCCUPIED_SEAT and len(list(filter(lambda x: x == OCCUPIED_SEAT, neighbours))) >= occupied_count:
                    new_layout[-1].append(EMPTY_SEAT)
                    if not changed:
                        changed = True
                else:
                    new_layout[-1].append(col)
        self.seats = new_layout
        return changed

    def test(self, input_data):
        self.common(self.test_input)
        assert next(self.part1(self.test_input)) == 37
        self.common(self.test_input)
        assert next(self.part2(self.test_input)) == 26

    def part1(self, input_data):
        changed = True
        while changed:
            changed = self.do_tick(self.neighbours)
        yield len(list(x for y in self.seats for x in y if x == OCCUPIED_SEAT))

    def neighbours2(self, x, y):
        ns = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        res = []
        for ny, nx in ns:
            c = FLOOR
            cx, cy = (x + nx), (y + ny)
            while 0 <= cy < len(self.seats) and 0 <= cx < len(self.seats[0]) and c == FLOOR:
                c = self.seats[cy][cx]
                cx, cy = (cx + nx), (cy + ny)
            res.append(c)
        return res

    def part2(self, input_data):
        changed = True
        while changed:
            changed = self.do_tick(self.neighbours2, 5)
        yield len(list(x for y in self.seats for x in y if x == OCCUPIED_SEAT))
