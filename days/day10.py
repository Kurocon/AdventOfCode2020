from functools import lru_cache
from typing import List

from days import AOCDay, day

@day(10)
class Day10(AOCDay):
    print_debug = "c12"
    test_input = """16
10
15
5
1
11
7
19
6
12
4""".split("\n")
    test_input2 = """28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3""".split("\n")

    def common(self, input_data):
        # input_data = self.test_input2
        self.input_data = list(map(int, input_data))

    def check_smallest_adapter_recurse(self, current_rating, target_rating, adapters_left) -> List[int]:
        options = [current_rating + i for i in range(1, 4)]
        for option in options:
            if option in adapters_left:
                difference = option - current_rating
                current_rating = option
                if current_rating + 3 == target_rating:
                    return [difference, 3]
                new_adapters = adapters_left[:]
                new_adapters.remove(option)
                return self.check_smallest_adapter_recurse(current_rating, target_rating, new_adapters) + [difference]

    def part1(self, input_data):
        current_rating = 0
        target_rating = max(self.input_data) + 3
        adapters_left = self.input_data[:]
        differences = self.check_smallest_adapter_recurse(current_rating, target_rating, adapters_left)
        yield len([x for x in differences if x == 1]) * len([x for x in differences if x == 3])

    @lru_cache
    def check_adapter_recurse(self, current_rating, target_rating, adapters) -> int:
        if current_rating == target_rating:
            return 1
        options = [i for i in adapters if 1 <= i - current_rating <= 3]
        count = 0
        for option in options:
            count += self.check_adapter_recurse(option, target_rating, adapters)
        return count

    def part2(self, input_data):
        current_rating = 0
        target_rating = max(self.input_data) + 3
        adapters_plus_builtin = tuple(self.input_data[:] + [target_rating])
        differences = self.check_adapter_recurse(current_rating, target_rating, adapters_plus_builtin)
        yield differences
