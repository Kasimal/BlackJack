class Hand:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def calculate_value(self, minimum=False):
        value = sum(self.cards)
        aces = self.cards.count(1)

        # Berechnung für den normalen Wert
        if not minimum:
            while value <= 11 and aces > 0:
                value += 10
                aces -= 1
        # Berechnung für den minimalen Wert (keine Aces als 11)
        else:
            while aces > 0:
                value += 1
                aces -= 1

        return value


    def probability_to_reach_or_exceed(self, deck):
        current_value = self.calculate_value(minimum=True)
        remaining_deck = deck.deck[:]
        total_cards = len(remaining_deck)

        if total_cards == 0:
            return 0.0, 0.0

        # Calculate probabilities
        reach = 0
        exceed = 0

        for card in remaining_deck:
            if card == 1:  # Handle Ace separately
                if current_value + 11 <= 21:
                    new_value = current_value + 11
                else:
                    new_value = current_value + 1
            else:
                new_value = current_value + card

            if new_value > 21:
                exceed += 1
            elif new_value <= 21:
                reach += 1

        return reach / total_cards, exceed / total_cards

    def __str__(self):
        return f"Cards: {self.cards}, Total value: {self.calculate_value()}"
