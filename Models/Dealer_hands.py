import Utility.Calculations as calc


class DealerHands:
    def __init__(self, deck, db_manager):
        # Initialisierung der Dealer-spezifischen Eigenschaften
        self.dealer_threshold = 17  # Mindestwert, ab dem der Dealer stoppt
        self.deck = deck
        self.db_manager = db_manager

    def generate_dealer_hands(self, table_name, start_card=None):
        """
        Generiert und speichert alle möglichen Dealerhände für eine bestimmte Startkarte oder für alle Karten.

        Args:
            table_name (str): Name der Dealerhände-Tabelle.
            start_card (int, optional): Die Startkarte des Dealers (z. B. 1 für Ass, 2 für 2 usw.).
                                        Wenn None, werden alle Startkarten generiert.
        """
        # Abrufen der Originalfrequenzen aus dem Deck
        original_frequencies = self.deck.original_card_frequencies

        if start_card:
            # Validierung der Startkarte
            if start_card not in self.deck.get_available_cards():
                raise ValueError(f"Ungültige Startkarte: {start_card}. Die Startkarte muss zwischen 1 und 10 liegen.")
            print(f"Generiere Dealerhände für Startkarte {start_card} in Tabelle '{table_name}'...")
            self._generate_dealer_hands_recursive(table_name, [start_card], start_card, original_frequencies)
        else:
            # Generiere Dealerhände für alle möglichen Startkarten
            for card in self.deck.get_available_cards():
                print(f"Generiere Dealerhände für Startkarte {card} in Tabelle '{table_name}'...")
                self._generate_dealer_hands_recursive(table_name, [card], card, original_frequencies)

    def _generate_dealer_hands_recursive(self, table_name, current_hand, start_card, original_frequencies):
        """
        Rekursive Methode zur Generierung aller möglichen Dealerhände.

        Args:
            table_name (str): Name der Dealerhände-Tabelle.
            current_hand (list): Die aktuelle Hand (als Liste der Kartenwerte).
            start_card (int): Die Startkarte des Dealers.
            original_frequencies (dict): Originale Kartenhäufigkeiten im Deck (z. B. {1: 4, 2: 4, ..., 10: 16}).
        """
        # Berechne den Gesamtwert der aktuellen Hand
        total_value = calc.hand_value(current_hand)

        # Eigenschaften der Hand berechnen
        is_blackjack = len(current_hand) == 2 and total_value == 21
        is_busted = total_value > 21

        # Berechne die Häufigkeit der Hand mit Berücksichtigung der Reihenfolge
        frequency = calc.hand_frequency_with_order(current_hand, original_frequencies, cards_to_ignore = 1)

        # Hand speichern
        self.db_manager.save_hand(
            table_name=table_name,
            hands_type="dealer",
            hand=current_hand,
            start_card=start_card,  # Startkarte wird gespeichert
            total_value=total_value,
            minimum_value=None,  # Bei Dealerhänden bleibt dies leer
            is_blackjack=is_blackjack,
            is_starthand=False,  # Bei Dealerhänden spielt Starthand keine Rolle
            is_busted=is_busted,
            can_double=False,  # Dealerhände können nie verdoppeln
            can_split=False,  # Dealerhände können nie splitten
            bust_chance=0,  # Für Dealerhände optional
            frequency=frequency
        )

        # Abbruchbedingung: Wenn der Dealerhände-Wert >= 17 ist
        if total_value >= 17:
            return

        # Generiere neue Hände, indem jede mögliche Karte hinzugefügt wird
        for card in self.deck.get_available_cards():
            # Reduziere die Frequenz der Karte um 1, falls verfügbar
            if original_frequencies[card] > current_hand.count(card):
                next_hand = current_hand + [card]
                self._generate_dealer_hands_recursive(table_name, next_hand, start_card, original_frequencies)
