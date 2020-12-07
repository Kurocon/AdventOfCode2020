import re
from collections import defaultdict

from days import AOCDay, day

@day(7)
class Day7(AOCDay):
    test_input = """light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.""".split("\n")
    test_input2 = """shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags.""".split("\n")

    PATTERN = re.compile(r"([a-z]+) ([a-z]+) bags contain ((([0-9]+) ([a-z]+) ([a-z]+) bags?[,.] ?)+|(no other bags.))")
    CONTAIN_PATTERN = re.compile(r"([0-9]+) ([a-z]+) ([a-z]+) bags?.?")

    bags = defaultdict(list)
    contain_bag = defaultdict(list)

    def common(self, input_data):
        self.bags = defaultdict(list)
        self.contain_bag = defaultdict(list)
        for line in input_data:
            m = self.PATTERN.match(line)
            if m:
                if m.group(3) != "no other bags.":
                    for p in m.group(3).split(", "):
                        n = self.CONTAIN_PATTERN.match(p)
                        if n:
                            params = n.groups()
                            self.bags[(m.group(1), m.group(2))].append((int(params[0]), params[1], params[2]))
                            self.contain_bag[n.group(2), n.group(3)].append((m.group(1), m.group(2)))
                        else:
                            self.error(f"Subline {p} failed to parse.")
                else:
                    pass  # No bags in this one
            else:
                self.error(f"Line {line} failed to parse.")

    def part1(self, input_data):
        bags = set()
        queue = [("shiny", "gold")]
        visited = []
        while queue:
            bag = queue.pop(0)
            self.debug(f"visiting {bag}, contained in: {self.contain_bag[bag]}")
            for contain in self.contain_bag[bag]:
                if contain not in visited:
                    bags.add(contain)
                    queue.append(contain)
                    visited.append(bag)
        yield len(bags)

    def recurse_count(self, pattern, colour):
        sum = 0
        self.debug(f"visiting {(pattern, colour)}, has: {self.bags[(pattern, colour)]}")
        for contain in self.bags[(pattern, colour)]:
            sum += (self.recurse_count(contain[1], contain[2]) * contain[0]) + contain[0]
            self.debug(f"new sum: {sum}")

        self.debug(f"{pattern} {colour} has {sum} bags")
        return sum

    def part2(self, input_data):
        yield self.recurse_count("shiny", "gold")
