import random

class CardDeck:
    def __init__(self, num_decks=1):
        self.num_decks = num_decks
        self.reset_deck()

    def reset_deck(self):
        self.deck = [value for value in ([1, 10, 10, 10] + list(range(2, 10))) * 4] * self.num_decks
        random.shuffle(self.deck)

    def draw_card(self):
        if not self.deck:
            self.reset_deck()
        return self.deck.pop()

    def calculate_probabilities(self):
        total_cards = len(self.deck)
        probabilities = {}
        for value in range(1, 11):
            count = self.deck.count(value if value != 10 else 10) + (self.deck.count(10) if value == 10 else 0)
            probabilities[value] = count / total_cards if total_cards > 0 else 0
        return probabilities
