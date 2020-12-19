import re

from days import AOCDay, day

@day(19)
class Day19(AOCDay):
    print_debug = "c12"
    test_input = '''0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb'''.split("\n")

    rules = {}
    messages = []

    def common(self, input_data):
        parse_rules = True

        self.messages = []
        self.rules = {}

        for line in input_data:
            if parse_rules:
                if line == "":
                    parse_rules = False
                    continue
                rule_id, rule = line.split(": ", maxsplit=1)
                self.rules[rule_id] = rule
            else:
                self.messages.append(line)

    def get_regex(self, rule_num):
        rule = self.rules[rule_num]
        if re.fullmatch('"."', rule):
            return rule[1]
        else:
            parts = rule.split(" | ")
            result = []
            for part in parts:
                numbers = part.split(" ")
                result.append("".join(self.get_regex(n) for n in numbers))
            return f"(?:{'|'.join(result)})"

    def get_regex2(self, rule_num):
        if rule_num == "8":
            # 42 | 42 8 in regex is (42)+
            return f"{self.get_regex2('42')}+"
        elif rule_num == "11":
            # 42 31 | 42 11 31 in regex is ((42){n}(31){n}) with n > 1
            # We can assume n to be less than 100 (longest line in my input is 88),
            # but they need to be the same so we need to pre-generate all options
            rule_n_times = (f"{self.get_regex2('42')}{{{n}}}{self.get_regex2('31')}{{{n}}}" for n in range(1, 100))
            return f"(?:{'|'.join(rule_n_times)})"

        rule = self.rules[rule_num]
        if re.fullmatch('"."', rule):
            return rule[1]
        else:
            parts = rule.split(" | ")
            result = []
            for part in parts:
                numbers = part.split(" ")
                result.append("".join(self.get_regex2(n) for n in numbers))
            return f"(?:{'|'.join(result)})"

    def part1(self, input_data):
        regex_0 = re.compile(self.get_regex("0"))
        yield sum(regex_0.fullmatch(x) is not None for x in self.messages)

    def part2(self, input_data):
        regex_0 = re.compile(self.get_regex2("0"))
        yield sum(regex_0.fullmatch(x) is not None for x in self.messages)
