from collections import defaultdict
from itertools import combinations, permutations

class Hand:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def calculate_value(self, minimum=False):
        value = sum(self.cards)
        aces = self.cards.count(1)

        if not minimum:
            while value <= 11 and aces > 0:
                value += 10
                aces -= 1
        return value

    def __repr__(self):
        return f"Hand(cards={self.cards})"


class Deck:
    def __init__(self, deck_count=1):
        self.deck_count = deck_count
        self.card_values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]  # Kartenwerte inkl. Bildkarten
        self.deck = self.card_values * 4 * deck_count


class BlackjackHandTracker:
    def __init__(self, deck_count=1):
        self.deck = Deck(deck_count)
        self.hands = defaultdict(int)  # Speichert alle möglichen Hände: {Hand: frequency}

    def track_hands(self, max_hands=5):
        """Berechnet eine begrenzte Anzahl von Händen und deren Häufigkeiten."""
        # Schritt 1: Generiere alle möglichen Startkombinationen (zwei Karten, Reihenfolge egal)
        start_combinations = combinations(self.deck.deck, 2)

        count = 0
        for combo in start_combinations:
            if count >= max_hands:
                break

            hand = Hand()
            hand.add_card(combo[0])
            hand.add_card(combo[1])
            sorted_hand = tuple(sorted(combo))
            self.hands[(sorted_hand, ())] += 1

            # Schritt 2: Generiere mögliche Reihenfolgen für gezogene Karten
            reduced_deck = self.deck.deck[:]
            reduced_deck.remove(combo[0])
            reduced_deck.remove(combo[1])

            for draw_count in range(1, len(reduced_deck) + 1):  # Anzahl gezogener Karten
                for drawn_cards in permutations(reduced_deck, draw_count):
                    self.hands[(sorted_hand, drawn_cards)] += 1
            count += 1

    def get_hands_with_values(self):
        """Gibt eine Liste aller Hände mit ihrem Wert und ihrer Häufigkeit zurück."""
        hands_with_values = []
        for (start_hand, drawn_cards), freq in self.hands.items():
            hand = Hand()
            for card in start_hand:
                hand.add_card(card)
            for card in drawn_cards:
                hand.add_card(card)

            value = hand.calculate_value()
            hands_with_values.append({
                "start_hand": start_hand,
                "drawn_cards": drawn_cards,
                "value": value,
                "frequency": freq
            })
        return hands_with_values


# Beispielnutzung
tracker = BlackjackHandTracker(deck_count=1)
tracker.track_hands(max_hands=5)  # Verarbeite nur die ersten 5 Starthände
hands_with_values = tracker.get_hands_with_values()

# Ausgabe der Hände
for hand in hands_with_values:
    print(f"Start Hand: {hand['start_hand']}, Drawn Cards: {hand['drawn_cards']}, "
          f"Value: {hand['value']}, Frequency: {hand['frequency']}")
