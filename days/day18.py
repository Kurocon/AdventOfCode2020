from typing import Tuple

from days import AOCDay, day

@day(18)
class Day18(AOCDay):
    test_input = """1 + 2 * 3 + 4 * 5 + 6
1 + (2 * 3) + (4 * (5 + 6))
2 * 3 + (4 * 5)
5 + (8 * 3 + 9 + 3 * 4 * 3)
5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))
((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2""".split("\n")
    test_input2 = """1 + (2 * 3) + (4 * (5 + 6))
2 * 3 + (4 * 5)
5 + (8 * 3 + 9 + 3 * 4 * 3)
5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))
((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2""".split("\n")

    def test(self, input_data):
        assert next(self.part1(self.test_input)) == 26457, "Part 1 tests fail"
        assert next(self.part2(self.test_input2)) == 693942, "Part 2 tests fail"

    def solve(self, input) -> Tuple[int, int]:
        result = 0
        index = 0
        operation = None
        while index < len(input):
            self.debug(f"-> {input[index:]}")
            c = input[index]
            if c == "(":
                num, r_i = self.solve(input[index+1:])
                index += r_i + 1
            elif c == ")":
                index += 1
                self.debug(f"RES2 {result}, {input[index:]}, {index}")
                return result, index
            elif c == " ":
                index += 1
            elif c in "+*":
                operation = c
                index += 1
            else:
                num = int(c)
                index += 1

            if c not in " +*":
                if operation is None:
                    self.debug(f" = {num}")
                    result = num
                elif operation == "+":
                    self.debug(f" {result} + {num}")
                    result += num
                elif operation == "*":
                    self.debug(f" {result} * {num}")
                    result *= num
                else:
                    raise ValueError(f"Unknown operation {operation}")

        self.debug(f"RES1 {result}")
        return result, index + 1

    def replace_and_calculate(self, input):
        while "+" in input:
            input = self.solve_plus(input)
            self.debug("-> " + input)
        return eval(input)

    def solve_plus(self, input: str):
        index = input.index("+") - 2
        if input[index] == ")":
            # Find index of "(" belonging to this bracket
            indent_level = 1
            ci = index - 1
            while indent_level > 0:
                c = input[ci]
                if c == ")":
                    indent_level += 1
                if c == "(":
                    indent_level -= 1
                ci -= 1
            ci += 1

            # Replace and calculate that part of the sum
            new_string = input[:ci]
            n1 = self.replace_and_calculate(input[ci+1:index])
            index += 4
        else:
            n1 = input[index]
            ni = index - 1
            while ni >= 0 and input[ni] in "1234567890":
                n1 = input[ni] + n1
                ni -= 1
            n1 = int(n1)
            new_string = input[:max(ni + 1, 0)]
            index += 4

        if input[index] == "(":
            # Find index of ")" belonging to this bracket
            indent_level = 1
            ci = index + 1
            while indent_level > 0:
                c = input[ci]
                if c == ")":
                    indent_level -= 1
                if c == "(":
                    indent_level += 1
                ci += 1
            ci -= 1

            # Replace and calculate that part of the sum
            new_string2 = input[ci+1:]
            n2 = self.replace_and_calculate(input[index+1:ci])
            index += 4

        else:
            new_string2 = input[index+1:]
            n2 = input[index]
            index += 1
            while index < len(input) and input[index] in "1234567890":
                n2 += input[index]
                index += 1
            n2 = int(n2)

        return new_string + str(n1 + n2) + new_string2

    def part1(self, input_data):
        sum = 0
        for line in input_data:
            sum += self.solve(line)[0]
        yield sum

    def part2(self, input_data):
        sum = 0
        for line in input_data:
            sum += self.replace_and_calculate(line)
        yield sum
