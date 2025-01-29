deck_count = 1  #Globale Variable für die Anzahl der Decks, Standard für Testzwecke ist 1 für ein Deck aus 52 Karten, Standard für Kasinos ist 6 Decks aus zusammen 312 Karten.

class Deck:
    def __init__(self):
        """Erstellt ein Deck mit Kartenwerten von 1 bis 10 und ihren Häufigkeiten."""
        self.deck_count = {deck_count}
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

    def get_available_cards(self):
        """
        Gibt eine Liste der Kartenwerte zurück, die im Deck verfügbar sind.
        """
        return [card for card, freq in self.original_card_frequencies.items() if freq > 0]

    def total_cards(self):
        """Berechnet die Gesamtzahl der Karten im Deck."""
        return sum(self.card_frequencies.values())

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
        new_deck = Deck()
        new_deck.card_frequencies = self.card_frequencies.copy()
        return new_deck