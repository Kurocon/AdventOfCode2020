from days import AOCDay, day

from collections import defaultdict

@day(22)
class Day22(AOCDay):
    test_input = """Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10""".split("\n")

    test_input2 = """Player 1:
43
19

Player 2:
2
29
14""".split("\n")

    decks = {}
    all_cards_len = 0
    round_counter = 0


    def common(self, input_data):
        # input_data = self.test_input2
        input_data = "\n".join(input_data).split("\n\n")
        self.decks = {}
        for player_data in input_data:
            lines = player_data.split("\n")
            player_name = lines[0].replace(":", "")
            cards = list(map(int, lines[1:]))
            self.decks[player_name] = cards
        self.all_cards_len = sum(len(x) for x in self.decks.values())
        self.round_counter = 0

    def do_round(self):
        self.debug(f"Round {self.round_counter}")
        self.debug(f"Decks: {self.decks}")
        top_cards = [(x[0], x[1].pop(0)) for x in self.decks.items()]
        self.debug(f"Plays: {top_cards}")
        top_player, top_card = max(top_cards, key=lambda x: x[1])
        self.debug(f"Winner: {top_player}")
        self.decks[top_player].extend(reversed(sorted([x[1] for x in top_cards])))
        self.debug("")
        if len(self.decks[top_player]) == self.all_cards_len:
            self.debug(f"Game over! Winner: {top_player}")
            return top_player
        else:
            return None

    def do_round_recursively(self, cards, game_number):
        top_cards = [(x[0], x[1].pop(0)) for x in cards.items()]

        if all(len(cards[x[0]]) >= x[1] for x in top_cards):
            top_player = self.play_subgame(cards, top_cards, game_number + 1)
            top_cards_dict = dict(top_cards)
            cards[top_player].append(top_cards_dict[top_player])
            cards[top_player].extend([top_cards_dict[x] for x in top_cards_dict.keys() if x != top_player])
        else:
            top_player = max(top_cards, key=lambda x: x[1])[0]
            cards[top_player].extend(reversed(sorted([x[1] for x in top_cards])))

        if len(cards[top_player]) == sum(len(x) for x in cards.values()):
            return top_player, cards
        else:
            return None, cards

    def play_subgame(self, cards, top_cards, game_number):
        winner = None
        cards = {x[0]: list(x[1])[:dict(top_cards)[x[0]]] for x in cards.items()}
        self.debug(f"\n== GAME {game_number} ==")
        round_cache = defaultdict(lambda: None)
        while winner is None:
            cache_key = tuple(tuple(x[1]) for x in cards.items())
            if round_cache[cache_key] is not None:
                self.debug("BREAKING RECURSION: Player 1 wins.")
                return "Player 1"
            round_cache[cache_key] = True
            winner, cards = self.do_round_recursively(cards, game_number)
        self.debug(f"{winner} wins sub-game {game_number}")
        return winner

    def get_score(self, cards):
        multiplier = 1
        result = 0
        for card in cards[::-1]:
            result += card * multiplier
            multiplier += 1
        return result

    def part1(self, input_data):
        winner = None
        while winner is None:
            self.round_counter += 1
            winner = self.do_round()
        yield self.get_score(self.decks[winner])

    def part2(self, input_data):
        winner = None
        round_cache = defaultdict(lambda: None)
        while winner is None:
            self.round_counter += 1
            cache_key = tuple(tuple(x[1]) for x in self.decks.items())
            if round_cache[cache_key] is not None:
                self.debug("BREAKING RECURSION: Player 1 wins.")
                winner = "Player 1"
                break
            round_cache[cache_key] = True
            winner, cards = self.do_round_recursively(self.decks, 1)

        self.debug("== Post game results ==")
        for player, cards in self.decks.items():
            self.debug(f"{player}'s deck: {cards}")

        yield self.get_score(self.decks[winner])
