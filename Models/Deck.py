from collections import Counter
import math

class Deck:
    def __init__(self, deck_count=1):
        """Erstellt ein Deck mit Kartenwerten von 1 bis 10 und ihren Häufigkeiten."""
        self.deck_count = deck_count
        # Häufigkeiten pro Karte in einem Standarddeck
        self.card_frequencies = {
            1: 4 * deck_count,  # Ass
            2: 4 * deck_count,
            3: 4 * deck_count,
            4: 4 * deck_count,
            5: 4 * deck_count,
            6: 4 * deck_count,
            7: 4 * deck_count,
            8: 4 * deck_count,
            9: 4 * deck_count,
            10: 16 * deck_count,  # 10, Bube, Dame, König
        }
        self.original_card_frequencies = self.card_frequencies.copy()

    def calculate_hand_value(self, hand, minimum=False):
        """
        Berechnet den Wert einer Hand.

        Args:
            hand (dict or list): Die Hand als Wörterbuch (Kartenwert -> Anzahl) oder Liste.
            minimum (bool): Wenn True, wird der minimale Wert der Hand berechnet.

        Returns:
            int: Der berechnete Wert der Hand.
        """
        # Wenn die Hand eine Liste ist, wandle sie in ein Wörterbuch um
        if isinstance(hand, list):
            hand = Counter(hand)

        # Berechnung basierend auf dem Wörterbuch
        total_value = sum(card * count for card, count in hand.items())
        if not minimum:
            ace_count = hand.get(1, 0)
            while ace_count > 0 and total_value <= 11:
                total_value += 10
                ace_count -= 1
        return total_value

    def calculate_hand_frequency(self, missing_cards):
        """
        Berechnet die Häufigkeit einer Hand basierend auf den fehlenden Karten.

        Args:
            missing_cards (list): Eine Liste mit den fehlenden Karten.

        Returns:
            int: Die Häufigkeit der Hand.
        """
        card_counts = Counter(missing_cards)  # Zähle, wie viele Karten welchen Typs fehlen
        frequency = 1

        # Berechne die Häufigkeit basierend auf den Karten im Deck
        for card, count in card_counts.items():
            original_count = self.original_card_frequencies[card]  # Anzahl der Karten im Deck

            # Berechne die Häufigkeit der Hand
            for i in range(count):
                frequency *= (original_count - i)  # Berücksichtige jede Karte der Hand
            frequency //= math.factorial(count)  # Teile durch die Anzahl der Permutationen

        return frequency

    def remove_card(self, card):
        """
        Entfernt eine Karte aus dem Deck, indem ihre Häufigkeit um 1 reduziert wird.

        Args:
            card (int): Die Karte, die entfernt werden soll (Wert zwischen 1 und 10).

        Raises:
            ValueError: Wenn die Karte nicht verfügbar ist.
        """
        if self.card_frequencies[card] > 0:
            self.card_frequencies[card] -= 1
        else:
            raise ValueError(f"Karte {card} ist nicht mehr im Deck verfügbar.")

    def restore_card(self, card):
        """Fügt eine Karte zurück ins Deck."""
        self.card_frequencies[card] += 1

    # def get_missing_cards(self):
    #     """
    #     Berechnet die Differenz zwischen den ursprünglichen Karten und den verbleibenden Karten im Deck.
    #
    #     Returns:
    #         dict: Ein Dictionary mit den fehlenden Karten und deren Anzahl.
    #     """
    #     missing_cards = {}
    #     for card, original_count in self.original_card_frequencies.items():
    #         current_count = self.card_frequencies.get(card, 0)
    #         if original_count > current_count:
    #             missing_cards[card] = original_count - current_count
    #     return missing_cards

    def get_available_cards(self):
        """
        Gibt eine Liste der Kartenwerte zurück, die im Deck verfügbar sind.
        """
        return [card for card, freq in self.original_card_frequencies.items() if freq > 0]

    def get_missing_cards(self):
        """
        Berechnet die Differenz zwischen dem ursprünglichen Deck und dem aktuellen Zustand des Decks.
        Gibt ein Wörterbuch zurück, das die fehlenden Karten und deren Häufigkeiten darstellt.
        """
        return {
            card: self.original_card_frequencies[card] - self.card_frequencies.get(card, 0)
            for card in self.original_card_frequencies
            if self.original_card_frequencies[card] > self.card_frequencies.get(card, 0)
        }

    def get_card_counts(self):
        """
        Gibt die Häufigkeit jeder Karte im Deck in der Reihenfolge 1 bis 10 zurück.

        Returns:
            list: Eine Liste von Häufigkeiten für jede Karte von 1 bis 10.
        """
        return [self.card_frequencies.get(card, 0) for card in range(1, 11)]

    def copy(self):
        """
        Erstellt eine tiefe Kopie des Decks.

        Returns:
            Deck: Eine Kopie des aktuellen Decks.
        """
        new_deck = Deck(deck_count=self.deck_count)
        new_deck.card_frequencies = self.card_frequencies.copy()
        return new_deck