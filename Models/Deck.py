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

    def calculate_value(self, minimum=False):
        """
        Berechnet den Gesamtwert einer Hand basierend auf den fehlenden Karten im Deck.

        Args:
            minimum (bool): Wenn True, wird der minimale Wert (Ass = 1) berechnet.

        Returns:
            int: Der berechnete Wert der Hand.
        """
        total_value = 0
        missing_count = sum(self.original_card_frequencies[card] - self.card_frequencies.get(card, 0)
                            for card in self.original_card_frequencies if card > 0)

        for card in self.original_card_frequencies:
            count_in_hand = missing_count - (self.original_card_frequencies[card] - self.card_frequencies.get(card, 0))

            # Überspringe ungültige Karten (z. B. wenn card = 0 oder nicht im Deck)
            if card < 1 or card > 10:
                continue

            if card == 1:  # Ass
                total_value += count_in_hand * (1 if minimum else 11)
            else:
                total_value += count_in_hand * card

        # Anpassung, wenn der Wert 21 überschreitet und Asse vorhanden sind
        if not minimum and total_value > 21:
            # Berechne die Anzahl der fehlenden Asse
            ace_count = self.original_card_frequencies.get(1, 0) - self.card_frequencies.get(1, 0)

            while total_value > 21 and ace_count > 0:
                total_value -= 10  # Ass wird von 11 auf 1 reduziert
                ace_count -= 1

        return total_value

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

    def get_missing_cards(self, original_deck):
        """Berechnet die fehlenden Karten im Vergleich zum ursprünglichen Deck."""
        missing_cards = []
        for card, count in original_deck.card_frequencies.items():
            missing = count - self.card_frequencies[card]
            missing_cards.extend([card] * missing)
        return missing_cards

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