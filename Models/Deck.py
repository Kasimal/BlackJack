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

    def remove_card(self, card):
        """Entfernt eine Karte aus dem Deck, reduziert ihre Häufigkeit."""
        if card in self.card_frequencies and self.card_frequencies[card] > 0:
            self.card_frequencies[card] -= 1

    def add_card(self, card):
        """Fügt eine Karte zurück ins Deck, erhöht ihre Häufigkeit."""
        if card in self.card_frequencies:
            self.card_frequencies[card] += 1

    def total_cards(self, card=None):
        """
        Gibt die Gesamtanzahl der verbleibenden Karten im Deck zurück.
        Wenn eine bestimmte Karte angegeben wird, wird deren Häufigkeit zurückgegeben.
        """
        if card is not None:
            return self.card_frequencies.get(card, 0)
        return sum(self.card_frequencies.values())

    def __repr__(self):
        return f"Deck({self.card_frequencies})"
