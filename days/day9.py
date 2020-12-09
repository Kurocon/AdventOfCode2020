from itertools import combinations

from days import AOCDay, day

@day(9)
class Day9(AOCDay):
    test_input = """35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576""".split("\n")

    preamble_length = 25
    data = []
    invalid_number = None

    def test(self, input_data):
        old_preamble_length, self.preamble_length = self.preamble_length, 5
        self.common(self.test_input)
        assert next(self.part1(self.test_input)) == 127, "Part 1 test case failed"
        assert next(self.part2(self.test_input)) == 62, "Part 1 test case failed"
        self.preamble_length = old_preamble_length

    def common(self, input_data):
        self.data = list(map(int, input_data))

    def part1(self, input_data):
        for index, x in enumerate(self.data[self.preamble_length:]):
            da = self.data[index:index+self.preamble_length]
            self.debug(f"{index}: {x} - {da}")
            for i, j in combinations(da, 2):
                if i + j == x:
                    break
            else:
                self.invalid_number = x
                yield x
                break

    def part2(self, input_data):
        invalid_number = self.invalid_number
        if invalid_number is None:
            invalid_number = next(self.part1(input_data))
        for index in range(len(self.data)):
            sum_set = [self.data[index]]
            offset = 0
            while sum(sum_set) < invalid_number:
                offset += 1
                sum_set.append(self.data[index+offset])
            if sum(sum_set) == invalid_number:
                self.debug(sum_set)
                yield min(sum_set) + max(sum_set)
                break
