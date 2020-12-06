from days import AOCDay, day

@day(1)
class Day1(AOCDay):
    test_input = """1721
979
366
299
675
1456""".split("\n")

    def test(self, input_data):
        self.input_data = list(map(int, self.test_input))
        assert list(self.part1(self.input_data)) == [514579], f'{list(self.part1(self.input_data))} != [514579]'
        assert list(self.part2(self.input_data)) == [241861950], f'{list(self.part2(self.input_data))} != [241861950]'

    def common(self, input_data):
        self.input_data = list(map(int, input_data))

    def part1(self, input_data):
        for x in self.input_data:
            if (2020 - x) in self.input_data:
                yield x * (2020 - x)
                return

    def part2(self, input_data):
        for x in self.input_data:
            for y in self.input_data:
                if (2020 - x - y) in self.input_data:
                    yield x * y * (2020 - x - y)
                    return
