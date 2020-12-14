import re
from collections import defaultdict

from days import AOCDay, day

@day(14)
class Day14(AOCDay):
    test_input = """mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0""".split("\n")
    test_input2 = """mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1""".split("\n")

    instrs = []
    mem = {}
    masks = None, None, None

    LINE_RE = re.compile(r"mem\[([0-9]+)\] = ([0-9]+)")

    def test(self, input_data):
        self.common(self.test_input)
        assert next(self.part1(self.test_input)) == 165, "Part 1 test fails"
        self.common(self.test_input2)
        assert next(self.part2(self.test_input)) == 208, "Part 2 test fails"

    def common(self, input_data):
        self.instrs = []
        self.mem = {}
        self.masks = None, None, None
        for line in input_data:
            m = self.LINE_RE.match(line)
            if m:
                self.instrs.append((int(m.group(1)), int(m.group(2))))
            else:
                mask = line.split(" = ")[1]
                self.instrs.append((None, (int(mask.replace("X", "0"), base=2), int(mask.replace("X", "1"), base=2), mask)))

    def part1(self, input_data):
        for loc, value in self.instrs:
            if loc is not None:
                self.mem[loc] = (value & self.masks[1]) | self.masks[0]
            else:
                self.masks = value
        yield sum(self.mem.values())

    def replace(self, mask: str):
        if "X" in mask:
            mask1, mask2 = mask.replace("X", "0", 1), mask.replace("X", "1", 1)
            masks = self.replace(mask1)
            masks += self.replace(mask2)
            if masks != []:
                return masks
            else:
                return [mask1, mask2]
        return []

    def part2(self, input_data):
        for loc, value in self.instrs:
            if loc is not None:
                # First apply regular mask
                loc = loc | self.masks[1]
                # Then generate possible locations
                loc_mask = list("{0:036b}".format(loc))
                for i, c in enumerate(self.masks[2]):
                    if c == "X":
                        loc_mask[i] = "X"
                locs = self.replace("".join(loc_mask))
                # And set those locations
                for loc in locs:
                    self.mem[int(loc, base=2)] = value
            else:
                self.masks = value
        yield sum(self.mem.values())
