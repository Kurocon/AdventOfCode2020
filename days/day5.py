from days import AOCDay, day

@day(5)
class Day5(AOCDay):
    test_input = """BFFFBBFRRR
FFFBBBFRRR
BBFFBBFRLL""".split("\n")

    def parse(self, x):
        x = x.replace("F", "0").replace("B", "1").replace("L", "0").replace("R", "1")
        row, col = int(x[:7], base=2), int(x[-3:], base=2)
        return (row * 8) + col

    def test(self, input_data):
        assert self.parse("FBFBBFFRLR") == 357
        assert self.parse("BFFFBBFRRR") == 567
        assert self.parse("FFFBBBFRRR") == 119
        assert self.parse("BBFFBBFRLL") == 820

    def common(self, input_data):
        self.input_data = [self.parse(x) for x in input_data]

    def part1(self, input_data):
        yield max(self.input_data)

    def part2(self, input_data):
        missing = [i for i in range(max(self.input_data)) if i not in self.input_data]
        for x in missing:
            if (x-1) not in missing and (x+1) not in missing:
                yield x
                break
