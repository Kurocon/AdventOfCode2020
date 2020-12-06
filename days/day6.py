from collections import Counter

from days import AOCDay, day

@day(6)
class Day6(AOCDay):
    test_input = """abc

a
b
c

ab
ac

a
a
a
a

b""".split("\n")

    groups = []

    def test(self, input_data):
        self.common(self.test_input)
        assert next(self.part1(self.test_input)) == 11, "Part 1 test fails"
        assert next(self.part2(self.test_input)) == 6, "Part 2 test fails"

    def common(self, input_data):
        input_data = "\n".join(input_data).split("\n\n")
        self.groups = []
        for group in input_data:
            # (group size, counter per letter)
            self.groups.append((len(group.split("\n")), Counter("".join(group.split("\n")))))

    def part1(self, input_data):
        # Sum uniquely answered questions (number of unique keys)
        yield sum(len(group[1].keys()) for group in self.groups)

    def part2(self, input_data):
        # Sum commonly answered questions (counter for question equals group size)
        yield sum(1 for group in self.groups for key in group[1].keys() if group[1][key] == group[0])
