from days import AOCDay, day

class Node:
    value = None
    next = None
    def __init__(self, value, next=None):
        self.value = value
        self.next = next

@day(23)
class Day23(AOCDay):
    print_debug = "c12"
    test_input = """389125467"""

    cups = []

    nodes = []
    current = None

    def common(self, input_data):
        self.cups = list(map(int, input_data))

        self.nodes = [Node(int(c)) for c in input_data]

        # Add 1000000 nodes to the list on top of the max value
        for value in range(10, 1000001):
            self.nodes.append(Node(value))
        assert len(self.nodes) == 1000000

        # Setup linked list
        for cur, next in zip(self.nodes, self.nodes[1:]):
            cur.next = next
        self.nodes[-1].next = self.nodes[0]

        # Setup value to node map
        self.value_map = {node.value: node for node in self.nodes}

        # Set current node to first
        self.current = self.nodes[0]

    def step(self):
        d_label = self.current.value
        pick_up = [self.cups.pop((self.current_index + 1) % len(self.cups)) for _ in range(3)]
        destination_cup = None
        i = 0
        while destination_cup is None:
            i += 1
            try:
                destination_cup = self.cups.index(((d_label - i - 1) % max(self.cups)) + 1)
            except ValueError:
                pass

        for i in pick_up[::-1]:
            self.cups.insert(destination_cup + 1, i)

        self.current_index = (self.current_index + 1) % len(self.cups)

        print(pick_up, destination_cup, self.cups, self.current_index)

    def part1(self, input_data):
        for _ in range(100):
            # 3 cups clockwise of current
            pick_up = self.cups[1:4]
            # Destination
            destination = self.cups[0] - 1
            if destination == 0:
                destination = 9
            while destination in pick_up:
                destination -= 1
                if destination == 0:
                    destination = 9
            # Cups without pickup
            new_cups = self.cups[:1] + self.cups[4:]

            # Insert pickup clockwise of destination cups
            new_index = new_cups.index(destination)
            new_cups = new_cups[:new_index + 1] + pick_up + new_cups[new_index + 1:]

            # New current cup clockwise of current, rotate list so new current is on front.
            self.cups = new_cups[1:] + new_cups[:1]

        # Labels on cups, clockwise from 1, excluding 1
        yield "".join(map(str, self.cups[self.cups.index(1) + 1:] + self.cups[:self.cups.index(1)]))

    def part2(self, input_data):
        for _ in range(10000000):
            # Pickup cups
            a = self.current.next
            b = a.next
            c = b.next
            # Remove those three from list
            self.current.next = c.next

            # Calculate destination cup
            used = {self.current.value, a.value, b.value, c.value}
            current_val = self.current.value
            while current_val in used:
                current_val -= 1
                if current_val == 0:
                    current_val = 1000000
            insert_after = self.value_map[current_val]
            next_node = insert_after.next

            # Insert pickup after destination
            insert_after.next = a
            c.next = next_node

            # Set new current
            self.current = self.current.next

        # Result is values of two cups after cup 1 multiplied
        cup1 = self.value_map[1]
        a = cup1.next
        b = a.next
        yield a.value * b.value
