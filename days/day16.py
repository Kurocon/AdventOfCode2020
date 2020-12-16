import re
from functools import reduce
from typing import Optional

from days import AOCDay, day

@day(16)
class Day16(AOCDay):
    test_input = """class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12""".split("\n")
    test_input2 = """class: 0-1 or 4-19
row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9""".split("\n")

    notes = {}
    my_ticket = []
    tickets = []

    VALS_RE = re.compile(r"([0-9]+)-([0-9]+) or ([0-9]+)-([0-9]+)")

    def common(self, input_data):
        notes, my_ticket, nearby_tickets = "\n".join(input_data).split("\n\n")
        self.notes = {}

        for line in notes.split("\n"):
            name, vals = line.split(": ")
            m = self.VALS_RE.match(vals)
            self.notes[name] = [
                (int(m.group(1)), int(m.group(2))),
                (int(m.group(3)), int(m.group(4)))
            ]

        self.my_ticket = list(map(int, my_ticket.split("\n")[1].split(",")))

        self.tickets = [
            list(map(int, ticket.split(",")))
            for ticket in nearby_tickets.split("\n")[1:]
        ]

    def get_always_invalid_field(self, ticket) -> Optional[int]:
        for field in ticket:
            valid = False
            for note in self.notes.values():
                for min, max in note:
                    if min <= field <= max:
                        valid = True
                        break
            if not valid:
                return field
        return None

    def part1(self, input_data):
        total = 0
        for ticket in self.tickets:
            field = self.get_always_invalid_field(ticket)
            if field is not None:
                total += field
        yield total

    def is_valid(self, rule, field):
        valid = False
        for min, max in rule:
            if min <= field <= max:
                valid = True
                break
        return valid

    def part2(self, input_data):
        valid_tickets = [ticket for ticket in self.tickets if self.get_always_invalid_field(ticket) is None]
        field_options = {x: [] for x in self.notes.keys()}

        # Which rules holds for all field values of a ticket
        for name, rule in self.notes.items():
            # For each field
            for field_index in range(len(self.my_ticket)):
                # Check if the rule holds for that field in all tickets
                valid = True
                self.debug(f"Checking rule {name} for index {field_index}")
                for ticket in valid_tickets:
                    if not self.is_valid(rule, ticket[field_index]):
                        self.debug(f"Not valid: {ticket[field_index]} fails {rule}")
                        valid = False
                        break
                if valid:
                    field_options[name].append(field_index)

        # Reduce options one by one
        field_map = {x: None for x in self.notes.keys()}

        # While not done
        while not all(field is not None for field in field_map.values()):

            # Find field option with only one value and fill that one in
            removed = None
            for name, options in field_options.items():
                if len(options) == 1:
                    field_map[name] = options[0]
                    removed = options[0]
                    self.debug(f"Matched {name} to field {options[0]}")
                    break
            # Remove option from other fields
            for name, options in field_options.items():
                if removed in options:
                    field_options[name] = list(filter(lambda x: x != removed, options))

        fields = [value for name, value in field_map.items() if name.startswith("departure")]
        yield reduce(lambda x, y: x * y, (self.my_ticket[x] for x in fields))
