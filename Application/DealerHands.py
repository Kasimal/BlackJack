class DealerHands:
    def __init__(self, deck, db_manager):
        # Initialisierung der Dealer-spezifischen Eigenschaften
        self.dealer_threshold = 17  # Mindestwert, ab dem der Dealer stoppt
        self.deck = deck
        self.db_manager = db_manager

    def generate_dealer_hands(self, table_name, start_card=None):
        """
        Generiert mögliche Dealer-Hände, beginnend mit einer angegebenen Startkarte.

        Args:
            start_card (int or None): Die Startkarte, mit der die Hände generiert werden sollen.
                                      Wenn None, werden alle möglichen Startkarten (1 bis 10) verwendet.
        """
        # Prüfen, ob eine spezifische Startkarte übergeben wurde
        if start_card:
            starting_hand = [start_card]
            self._generate_dealer_hands_recursive(table_name, starting_hand)
        else:
            # Wenn keine Startkarte angegeben ist, durchlaufe alle 10 sichtbaren Karten
            for card in self.deck.get_available_cards():
                starting_hand = [card]
                self._generate_dealer_hands_recursive(table_name, starting_hand)

    def _generate_dealer_hands_recursive(self, table_name, current_hand):
        """
        Rekursive Funktion zur Generierung und Analyse von Dealer-Händen.

        Args:
            current_hand (list): Die aktuelle Dealer-Hand (Startkarte + mögliche weitere Karten).
        """
        # Berechne den Minimalwert der aktuellen Hand
        minimum_value = self.deck.calculate_hand_value(current_hand, minimum=True)

        # Abbruchbedingung: Wenn der Mindestwert der Hand > 21 ist, ist die Hand gebustet
        if minimum_value > 21:
            self.db_manager.save_dealer_hand(table_name, current_hand[0], "bust")
            return

        # Berechne den Gesamtwert der aktuellen Hand
        total_value = self.deck.calculate_hand_value(current_hand)

        # Abbruchbedingung: Wenn der Dealer 17 oder mehr hat, Hand speichern
        if total_value >= self.dealer_threshold:
            if total_value == 21 and len(current_hand) == 2:
                hand_result = "blackjack"
            else:
                hand_result = f"total_{total_value}"  # Konvertiere Ergebnis in das korrekte Format

            self.db_manager.save_dealer_hand(table_name, current_hand[0], hand_result)
            return

        # Erzeuge neue Hände, indem jede mögliche Karte zur aktuellen Hand hinzugefügt wird
        for card in range(1, 11):  # Ass (1) bis 10
            # Berechne die Häufigkeit der Karte basierend auf der verbleibenden Anzahl
            if current_hand.count(card) < self.deck.original_card_frequencies[card]:
                next_hand = current_hand + [card]
                self._generate_dealer_hands_recursive(table_name, next_hand)

    def calculate_outcomes(self):
        """
        Berechne Wahrscheinlichkeiten für Dealer-Werte 17-21, Blackjack und Busted.
        """
        outcomes = {
            "17": 0,
            "18": 0,
            "19": 0,
            "20": 0,
            "21": 0,
            "Blackjack": 0,
            "Busted": 0
        }
        for total_value, frequency in self.db_manager.fetch_all_hands():
            if total_value > 21:
                outcomes["Busted"] += frequency
            elif total_value == 21 and len([card for card in range(1, 11) if card == 1]) == 1:
                outcomes["Blackjack"] += frequency
            elif 17 <= total_value <= 21:
                outcomes[str(total_value)] += frequency
        return outcomes

    def analyze_dealer_hands(self, start_card = None):
        """Analysiert die Verteilungen für eine gegebene Startkarte."""
        starthand = [start_card]  # Startkarte als Hand definieren
        remaining_deck = self.deck.derive_deck_from_hand(start_card, starthand)  # Restdeck berechnen

        distributions = {
            "17": 0, "18": 0, "19": 0, "20": 0, "21": 0,
            "blackjack": 0, "bust": 0
        }

        def recursive_analyze(current_hand, remaining_deck):
            total_value = self.deck.calculate_value(current_hand)

            if total_value > 21:
                distributions["bust"] += 1
            elif total_value >= 17:
                distributions[str(total_value)] += 1
            else:
                for card, count in remaining_deck.items():
                    if count > 0:
                        new_deck = remaining_deck.copy()
                        new_deck[card] -= 1
                        recursive_analyze(current_hand + [card], new_deck)

        recursive_analyze(starthand, remaining_deck)
        return distributions

        # Simuliere alle möglichen Folgekarten
    # def recursive_analyze(self, current_hand, remaining_deck):
    #     value = deck.calculate_value(current_hand)
    #     if value > 21:
    #         distributions["bust"] += 1
    #     elif value >= 17:
    #         distributions[str(value)] += 1
    #     else:
    #         for card, count in remaining_deck.items():
    #             if count > 0:
    #                 new_deck = remaining_deck.copy()
    #                 new_deck[card] -= 1
    #                 recursive_analyze(current_hand + [card], new_deck)
    #
    # recursive_analyze([start_card], deck.card_frequencies.copy())
    # return distributions