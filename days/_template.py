from days import AOCDay, day

@day(0)
class DayTemplate(AOCDay):
    print_debug = "c12"
    test_input = """""".split("\n")

    def common(self, input_data):
        input_data = self.test_input

    def part1(self, input_data):
        pass

    def part2(self, input_data):
        pass
