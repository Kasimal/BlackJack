import csv
from collections import defaultdict
from itertools import combinations, permutations
from Hand import Hand
from Deck import Deck

class Hands:
    def __init__(self, deck_count=1):
        self.deck = Deck(deck_count)
        self.hands = defaultdict(int)  # Speichert alle möglichen Hände: {Hand: frequency}

    def track_hands(self):
        """Berechnet alle möglichen Hände und deren Häufigkeiten."""
        # Schritt 1: Generiere alle möglichen Startkombinationen (zwei Karten, Reihenfolge egal)
        start_combinations = combinations(self.deck.deck, 2)

        for combo in start_combinations:
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

    def save_hands_to_file(self, filename="hands.csv"):
        """Speichert alle Hände in eine CSV-Datei."""
        hands_with_values = self.get_hands_with_values()
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            # Schreibe die Kopfzeile
            writer.writerow(["Start Hand", "Drawn Cards", "Value", "Frequency"])
            # Schreibe alle Hände
            for hand in hands_with_values:
                writer.writerow([
                    hand["start_hand"],
                    hand["drawn_cards"],
                    hand["value"],
                    hand["frequency"]
                ])


# Beispielnutzung
tracker = Hands(deck_count=1)
tracker.track_hands()
tracker.save_hands_to_file("blackjack_hands.csv")

print("Alle Hände wurden in die Datei 'blackjack_hands.csv' geschrieben.")