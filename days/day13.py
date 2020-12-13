from days import AOCDay, day
from functools import reduce

@day(13)
class Day13(AOCDay):
    test_input = """939
7,13,x,x,59,x,31,19""".split("\n")
    test_input2 = """1
17,x,13,19""".split("\n")
    test_input3 = """1
67,7,59,61""".split("\n")
    test_input4 = """1
67,x,7,59,61""".split("\n")
    test_input5 = """1
67,7,x,59,61""".split("\n")
    test_input6 = """1
1789,37,47,1889""".split("\n")

    def common(self, input_data):
        self.earliest_timestamp = int(input_data[0])
        self.buses = list(map(lambda x: int(x) if x != "x" else None, input_data[1].split(",")))

    def test(self, input_data):
        self.common(self.test_input)
        assert next(self.part1(self.test_input)) == 295, "Part 1 test fails"
        assert next(self.part2(self.test_input)) == 1068781, "Part 2 test fails"

        self.common(self.test_input2)
        assert next(self.part2(self.test_input2)) == 3417, "Part 2 test 2 fails"
        self.common(self.test_input3)
        assert next(self.part2(self.test_input3)) == 754018, "Part 2 test 3 fails"
        self.common(self.test_input4)
        assert next(self.part2(self.test_input4)) == 779210, "Part 2 test 4 fails"
        self.common(self.test_input5)
        assert next(self.part2(self.test_input5)) == 1261476, "Part 2 test 5 fails"
        self.common(self.test_input6)
        assert next(self.part2(self.test_input6)) == 1202161486, "Part 2 test 6 fails"

    def part1(self, input_data):
        timestamp = self.earliest_timestamp
        while True:
            for bus in self.buses:
                if bus is not None and timestamp % bus == 0:
                    self.debug(f"Bus {bus}, delta-t {timestamp - self.earliest_timestamp}")
                    yield bus * (timestamp - self.earliest_timestamp)
                    return
            timestamp += 1

    def chinese_remainder(self, n, a):
        sum = 0
        prod = reduce(lambda a, b: a * b, n)
        for n_i, a_i in zip(n, a):
            p = prod // n_i
            sum += a_i * self.mul_inv(p, n_i) * p
        return sum % prod

    def mul_inv(self, a, b):
        b0 = b
        x0, x1 = 0, 1
        if b == 1: return 1
        while a > 1:
            q = a // b
            a, b = b, a % b
            x0, x1 = x1 - q * x0, x0
        if x1 < 0: x1 += b0
        return x1

    def part2(self, input_data):
        # Chinese Remainder Theorem - https://en.wikipedia.org/wiki/Chinese_remainder_theorem
        # https://rosettacode.org/wiki/Chinese_remainder_theorem#Python_3.6

        # Solves equations like: x == a[0] % n[0] && x == a[1] % n[1] && .. && x == a[k] % n[k]
        # So n[x] is the bus time, and a[x] is the start time required for that bus to start
        bus_times = []
        bus_start_times = []
        for i, time in enumerate(self.buses):
            if time:
                bus_times.append(time)
                bus_start_times.append(time - i)

        yield self.chinese_remainder(bus_times, bus_start_times)
