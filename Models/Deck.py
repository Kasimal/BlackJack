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
        self.original_card_frequencies = {
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

    def calculate_hand_value(self, missing_cards, minimum=False):
        """
        Berechnet den Wert der Hand basierend auf den fehlenden Karten.

        Args:
            missing_cards (dict): Ein Dictionary, das die Anzahl der fehlenden Karten angibt.
            minimum (bool): Wenn True, wird der minimale Wert der Hand berechnet (z. B. As = 1).

        Returns:
            int: Der Wert der Hand.
        """
        value = 0
        ace_count = 0

        for card, count in missing_cards.items():
            if card == 1:  # Ass
                ace_count += count
            else:
                value += card * count

        # Ass-Werte hinzufügen
        if minimum:
            value += ace_count  # Alle Asse als 1 zählen
        else:
            value += ace_count * 11  # Alle Asse als 11 zählen
            while value > 21 and ace_count > 0:
                value -= 10  # Reduziere Ass von 11 auf 1
                ace_count -= 1

        return value

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

    def get_missing_cards(self):
        """
        Berechnet die Differenz zwischen den ursprünglichen Karten und den verbleibenden Karten im Deck.

        Returns:
            dict: Ein Dictionary mit den fehlenden Karten und deren Anzahl.
        """
        missing_cards = {}
        for card, original_count in self.original_card_frequencies.items():
            current_count = self.card_frequencies.get(card, 0)
            if original_count > current_count:
                missing_cards[card] = original_count - current_count
        return missing_cards

    def get_card_counts(self):
        """
        Gibt die Häufigkeit jeder Karte im Deck in der Reihenfolge 1 bis 10 zurück.

        Returns:
            list: Eine Liste von Häufigkeiten für jede Karte von 1 bis 10.
        """
        return [self.card_frequencies.get(card, 0) for card in range(1, 11)]

    def calculate_hand_frequency(self, hand_cards):
        """
        Berechnet die Häufigkeit einer Hand basierend auf den verfügbaren Karten im Deck.

        Args:
            hand_cards (list): Eine Liste von Karten, die die Hand darstellen.

        Returns:
            int: Die Häufigkeit der Hand.
        """
        frequency = 1  # Start mit der Grundhäufigkeit

        # Erstelle eine Kopie der Frequenzen, um das Deck während der Berechnung nicht zu verändern
        available_frequencies = self.card_frequencies.copy()

        for card in hand_cards:
            if available_frequencies[card] <= 0:
                return 0  # Falls die Karte nicht mehr verfügbar ist, ist die Häufigkeit 0
            frequency *= available_frequencies[card]
            available_frequencies[card] -= 1  # Reduziere die Frequenz, da die Karte benutzt wurde

        # Dividiere durch die Permutationsmöglichkeiten der Karten in der Hand
        # Beispiel: Für zwei gleiche Karten wie [10, 10] muss durch 2 geteilt werden
        for card in set(hand_cards):
            count = hand_cards.count(card)
            if count > 1:
                for i in range(1, count + 1):
                    frequency //= i  # Reduziere die Häufigkeit für identische Karten

        return frequency

    def copy(self):
        """
        Erstellt eine tiefe Kopie des Decks.

        Returns:
            Deck: Eine Kopie des aktuellen Decks.
        """
        new_deck = Deck(deck_count=self.deck_count)
        new_deck.card_frequencies = self.card_frequencies.copy()
        return new_deck