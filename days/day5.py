from days import AOCDay, day


@day(5)
class Day5(AOCDay):
    test_input = """BFFFBBFRRR
FFFBBBFRRR
BBFFBBFRLL""".split("\n")

    def test(self, input_data):
        def parse(x):
            return int(x.replace("F", "0").replace("B", "1").replace("L", "0").replace("R", "1"), base=2)
        assert parse("FBFBBFFRLR") == 357
        assert parse("BFFFBBFRRR") == 567
        assert parse("FFFBBBFRRR") == 119
        assert parse("BBFFBBFRLL") == 820

    def common(self, input_data):
        self.input_data = [int(x.replace("F", "0").replace("B", "1").replace("L", "0").replace("R", "1"), base=2) for x in input_data]

    def part1(self, input_data):
        yield max(self.input_data)

    def part2(self, input_data):
        missing = [i for i in range(max(self.input_data)) if i not in self.input_data]
        for x in missing:
            if (x - 1) not in missing and (x + 1) not in missing:
                yield x
                break
