import random
from Deck import Deck

class Hand:
    def __init__(self):
        """Erstellt eine leere Hand."""
        self.cards = []

    def add_card_from_deck(self, deck, card):
        """
        Fügt eine Karte aus dem Deck zur Hand hinzu.
        Reduziert die Häufigkeit der Karte im Deck.
        """
        if card in deck.card_frequencies and deck.card_frequencies[card] > 0:
            self.cards.append(card)
            deck.remove_card(card)
        else:
            raise ValueError(f"Karte {card} ist nicht im Deck verfügbar.")


    def draw_random_card_from_deck(self, deck):
        """
        Zieht eine zufällige Karte aus dem Deck und fügt sie der Hand hinzu.
        Reduziert die Häufigkeit der Karte im Deck.
        """
        total_cards = deck.total_cards()
        if total_cards == 0:
            raise ValueError("Das Deck ist leer, keine Karten verfügbar.")

        # Erstelle eine gewichtete Liste der Karten basierend auf ihren Häufigkeiten
        weighted_deck = [card for card, freq in deck.card_frequencies.items() for _ in range(freq)]

        # Ziehe eine zufällige Karte
        random_card = random.choice(weighted_deck)
        self.add_card_from_deck(deck, random_card)


    def calculate_value(self, minimum=False):
        """
        Berechnet den Wert der Hand.
        - Wenn `minimum=True`, wird Ass immer als 1 gezählt.
        - Sonst wird Ass als 11 gezählt, wenn der Gesamtwert ≤ 21 bleibt.
        """
        value = sum(self.cards)
        aces = self.cards.count(1)

        if not minimum:
            while value <= 11 and aces > 0:
                value += 10
                aces -= 1

        return value

    def probability_to_reach_or_exceed(self, deck, target_value=21):
        """
        Berechnet die Wahrscheinlichkeit, mit der der aktuelle Wert der Hand
        einen Zielwert (target_value) erreichen oder überschreiten kann.

        Args:
            deck (Deck): Das verbleibende Deck.
            target_value (int): Zielwert, der erreicht oder überschritten werden soll (standardmäßig 21).

        Returns:
            tuple: (reach_probability, exceed_probability)
                - reach_probability: Wahrscheinlichkeit, den Zielwert genau zu erreichen.
                - exceed_probability: Wahrscheinlichkeit, den Zielwert zu überschreiten.
        """
        current_value = self.calculate_value(minimum=True)
        remaining_deck = deck.card_frequencies
        total_cards = deck.total_cards()

        if total_cards == 0:
            return 0.0, 0.0

        reach = 0
        exceed = 0

        for card, frequency in remaining_deck.items():
            if frequency == 0:
                continue

            if card == 1:  # Sonderfall Ass
                new_value = current_value + 11 if current_value + 11 <= target_value else current_value + 1
            else:
                new_value = current_value + card

            if new_value > target_value:
                exceed += frequency
            elif new_value <= target_value:
                reach += frequency

        reach_probability = reach / total_cards
        exceed_probability = exceed / total_cards

        return reach_probability, exceed_probability

    def __repr__(self):
        return f"Hand(cards={self.cards}, value={self.calculate_value()})"
