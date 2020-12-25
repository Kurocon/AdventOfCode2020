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

    def get_loop_size(self, subject_number, pub_key):
        loop_size = 0
        value = 1
        while value != pub_key:
            loop_size += 1
            value = (value * subject_number) % 20201227
        return loop_size

    def get_encryption_key(self, subject_number, loop_size):
        value = 1
        for _ in range(loop_size):
            value = (value * subject_number) % 20201227
        return value

    def part1(self, input_data):
        card_loop_size = self.get_loop_size(7, self.card_pubkey)
        self.debug(f"Card loop size: {card_loop_size}")

        door_loop_size = self.get_loop_size(7, self.door_pubkey)
        self.debug(f"Door loop size: {door_loop_size}")

        encryption_key = self.get_encryption_key(self.card_pubkey, door_loop_size)
        assert encryption_key == self.get_encryption_key(self.door_pubkey, card_loop_size)
        self.debug(f"Encryption key: {encryption_key}")
        yield encryption_key

    def part2(self, input_data):
        yield "Merry christmas!"
