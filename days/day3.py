from days import AOCDay, day

TREE = "#"
EMPTY = "."

@day(3)
class Day3(AOCDay):
    test_input = """..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#""".split("\n")

    grid_size = (0, 0)

    def get_pos(self, input_data, x, y):
        return input_data[y][(x % self.grid_size[0])]

    def test(self, input_data):
        self.common(self.test_input)
        p1 = self.part1(self.test_input).__next__()
        assert p1 == 7, f"Part 1 test failing: {p1} != 7"
        p2 = self.part2(self.test_input).__next__()
        assert p2 == 336, f"Part 2 test failing: {p2} != 336"

    def common(self, input_data):
        self.grid_size = len(input_data[0]), len(input_data)

    def part1(self, input_data):
        cur_y = 0
        cur_x = 0
        num_trees = 0
        while cur_y < self.grid_size[1] - 1:
            cur_x += 3
            cur_y += 1
            if self.get_pos(input_data, cur_x, cur_y) == TREE:
                num_trees += 1
        yield num_trees

    def part2(self, input_data):
        mult = None
        for x in [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]:
            cur_y = 0
            cur_x = 0
            num_trees = 0
            while cur_y < self.grid_size[1] - 1:
                cur_x += x[0]
                cur_y += x[1]
                if self.get_pos(input_data, cur_x, cur_y) == TREE:
                    num_trees += 1
            if mult is None:
                mult = num_trees
            else:
                mult *= num_trees
        yield mult