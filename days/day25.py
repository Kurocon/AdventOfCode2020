from days import AOCDay, day

@day(25)
class Day25(AOCDay):
    test_input = """5764801
17807724""".split("\n")

    card_pubkey = None
    door_pubkey = None

    def common(self, input_data):
        # input_data = self.test_input
        self.card_pubkey, self.door_pubkey = map(int, input_data)

    def part1(self, input_data):
        def transform(subject_number, loop_size):
            # Python pow has a modulo parameter
            return pow(subject_number, loop_size, 20201227)

        card_loop_size = 0
        while transform(7, card_loop_size) != self.card_pubkey:
            card_loop_size += 1
        self.debug(f"Card loop size: {card_loop_size}")

        door_loop_size = 0
        while transform(7, door_loop_size) != self.door_pubkey:
            door_loop_size += 1
        self.debug(f"Door loop size: {door_loop_size}")

        encryption_key = transform(self.card_pubkey, door_loop_size)
        assert encryption_key == transform(self.door_pubkey, card_loop_size)
        self.debug(f"Encryption key: {encryption_key}")
        yield encryption_key

    def part2(self, input_data):
        yield "Merry christmas!"
