from collections import defaultdict

from days import AOCDay, day

@day(15)
class Day15(AOCDay):
    test_input = """0,3,6"""

    numbers = []
    history = defaultdict(list)
    last_number = None
    turn = 0

    def common(self, input_data):
        self.numbers = list(map(int, input_data.split(",")))
        self.history = defaultdict(list)

    def part1(self, input_data):
        self.turn = 1
        for n in self.numbers:
            self.history[n] = [self.turn]
            self.debug(f"{self.turn}: {n} is spoken")
            self.turn += 1

        self.last_number = self.numbers[-1]
        while self.turn <= 2020:
            if len(self.history[self.last_number]) >= 2:
                h1, h2 = self.history[self.last_number][-2:]
                number = h2 - h1
                self.history[number].append(self.turn)
                self.last_number = number
                self.debug(f"{self.turn}: {number} is spoken")
            else:
                self.history[0].append(self.turn)
                self.last_number = 0
                self.debug(f"{self.turn}: 0 is spoken")
            self.turn += 1
        yield self.last_number

    def part2(self, input_data):
        self.turn = 1
        for n in self.numbers:
            self.history[n] = [self.turn]
            self.turn += 1

        self.last_number = self.numbers[-1]
        while self.turn <= 30000000:
            if self.turn % 10000 == 0:
                self.debug(f"Turn {self.turn} / 30000000")
            if len(self.history[self.last_number]) >= 2:
                h1, h2 = self.history[self.last_number][-2:]
                number = h2 - h1
                self.history[number].append(self.turn)
                self.last_number = number
            else:
                self.history[0].append(self.turn)
                self.last_number = 0
            self.turn += 1
        yield self.last_number

