from days import AOCDay, day

@day(12)
class Day12(AOCDay):
    test_input = """F10
N3
F7
R90
F11""".split("\n")

    x = 0
    y = 0
    w_x = 0
    w_y = 0
    direction = 90
    instructions = []

    # Action N means to move north by the given value.
    def north(self, value):
        self.y += value

    # Action S means to move south by the given value.
    def south(self, value):
        self.y -= value

    # Action E means to move east by the given value.
    def east(self, value):
        self.x += value

    # Action W means to move west by the given value.
    def west(self, value):
        self.x -= value

    # Action L means to turn left the given number of degrees.
    def left(self, value):
        self.direction = (self.direction - value) % 360

    # Action R means to turn right the given number of degrees.
    def right(self, value):
        self.direction = (self.direction + value) % 360

    # Action F means to move forward by the given value in the direction the ship is currently facing.
    def forward(self, value):
        if self.direction == 0:
            self.north(value)
        elif self.direction == 90:
            self.east(value)
        elif self.direction == 180:
            self.south(value)
        elif self.direction == 270:
            self.west(value)
        else:
            raise ValueError(f"Invalid direction {self.direction}")

    # Action N means to move the waypoint north by the given value.
    def north_2(self, value):
        self.w_y += value

    # Action S means to move the waypoint south by the given value.
    def south_2(self, value):
        self.w_y -= value

    # Action E means to move the waypoint east by the given value.
    def east_2(self, value):
        self.w_x += value

    # Action W means to move the waypoint west by the given value.
    def west_2(self, value):
        self.w_x -= value

    # Action L means to rotate the waypoint around the ship left (counter-clockwise) the given number of degrees.
    def left_2(self, value):
        while value > 0:
            value -= 90
            self.w_x, self.w_y = -self.w_y, self.w_x

    # Action R means to rotate the waypoint around the ship right (clockwise) the given number of degrees.
    def right_2(self, value):
        while value > 0:
            value -= 90
            self.w_x, self.w_y = self.w_y, -self.w_x

    # Action F means to move forward to the waypoint a number of times equal to the given value.
    def forward_2(self, value):
        self.x = self.x + (self.w_x * value)
        self.y = self.y + (self.w_y * value)

    FMAP = {
        "N": (north, north_2),
        "S": (south, south_2),
        "E": (east, east_2),
        "W": (west, west_2),
        "L": (left, left_2),
        "R": (right, right_2),
        "F": (forward, forward_2)
    }

    def test(self, input_data):
        self.common(self.test_input)
        assert next(self.part1(self.test_input)) == 25, "Part 1 test failed"
        assert next(self.part2(self.test_input)) == 286, "Part 2 test failed"

    def common(self, input_data):
        self.instructions = [(x[0], int(x[1:])) for x in input_data]

    def part1(self, input_data):
        self.x = 0
        self.y = 0
        self.direction = 90
        for i, value in self.instructions:
            self.FMAP[i][0](self, value)
        yield abs(self.x) + abs(self.y)

    def part2(self, input_data):
        self.x = 0
        self.y = 0
        self.w_x = 10
        self.w_y = 1
        for i, value in self.instructions:
            self.FMAP[i][1](self, value)
        yield abs(self.x) + abs(self.y)
