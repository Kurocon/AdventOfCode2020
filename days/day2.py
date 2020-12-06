import re
from collections import Counter

from days import AOCDay, day

@day(2)
class Day2(AOCDay):
    test_input = """1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc""".split("\n")

    passwords = []

    LINE_FORMAT = re.compile(r"([0-9]+)-([0-9]+) ([a-z]): ([a-z]+)")

    def common(self, input_data):
        self.passwords = []
        for line in input_data:
            if m := self.LINE_FORMAT.match(line):
                self.passwords.append((m.group(4), m.group(3), int(m.group(1)), int(m.group(2))))
            else:
                raise ValueError(f"Line {line} failed to parse!")

    def is_valid(self, password: str, letter: str, min: int, max: int):
        counters = Counter(password)
        return min <= counters[letter] <= max

    def is_valid_2(self, password: str, letter: str, pos1: int, pos2: int):
        return (password[pos1 - 1] == letter and password[pos2 - 1] != letter) or \
               (password[pos1 - 1] != letter and password[pos2 - 1] == letter)

    def test(self, input_data):
        self.common(self.test_input)
        assert sum(1 for password in self.passwords if self.is_valid(*password)) == 2, "Part 1 test fails"
        assert sum(1 for password in self.passwords if self.is_valid_2(*password)) == 1, "Part 2 test fails"

    def part1(self, input_data):
        yield sum(1 for password in self.passwords if self.is_valid(*password))

    def part2(self, input_data):
        yield sum(1 for password in self.passwords if self.is_valid_2(*password))
