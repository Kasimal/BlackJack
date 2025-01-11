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

    def calculate_value(self, hand):
        """
        Berechnet den Gesamtwert einer Hand.

        Args:
            hand (list): Eine Liste von Karten (1-10), die die Hand repräsentiert.

        Returns:
            int: Der Gesamtwert der Hand.
        """
        total_value = 0
        ace_count = 0

        # Kartenwerte berechnen
        for card in hand:
            if card == 1:  # Ass
                ace_count += 1
                total_value += 11  # Zunächst zählt das Ass als 11
            else:
                total_value += card

        # Passe den Wert an, wenn die Hand über 21 geht
        while total_value > 21 and ace_count > 0:
            total_value -= 10  # Ass von 11 auf 1 reduzieren
            ace_count -= 1

        return total_value

    def remove_card(self, card):
        """Entfernt eine Karte aus dem Deck."""
        if self.card_frequencies[card] > 0:
            self.card_frequencies[card] -= 1
        else:
            raise ValueError(f"Karte {card} ist nicht mehr im Deck verfügbar.")

    def restore_card(self, card):
        """Fügt eine Karte zurück ins Deck."""
        self.card_frequencies[card] += 1

    def get_missing_cards(self, original_deck):
        """Berechnet die fehlenden Karten im Vergleich zum ursprünglichen Deck."""
        missing_cards = []
        for card, count in original_deck.card_frequencies.items():
            missing = count - self.card_frequencies[card]
            missing_cards.extend([card] * missing)
        return missing_cards
