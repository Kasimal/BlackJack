class DealerHands:
    def __init__(self, deck, db_manager):
        # Initialisierung der Dealer-spezifischen Eigenschaften
        self.dealer_threshold = 17  # Mindestwert, ab dem der Dealer stoppt
        self.deck = deck
        self.db_manager = db_manager

    def generate_dealer_hands(self, table_name, start_card=None):
        """
        Generiert und speichert alle möglichen Dealerhände für eine bestimmte Startkarte.

        Args:
            table_name (str): Name der Dealerhände-Tabelle.
            start_card (int, optional): Die Startkarte des Dealers (z. B. 1 für Ass, 2 für 2 usw.).
                                        Wenn None, werden alle Startkarten generiert.
        """
        if start_card:
            print(f"Generiere Dealerhände für Startkarte {start_card} in Tabelle '{table_name}'...")
            self._generate_dealer_hands_recursive(table_name, [start_card], start_card)
        else:
            # Wenn keine Startkarte angegeben ist, durchlaufe alle 10 sichtbaren Karten
            for card in self.deck.get_available_cards():
                print(f"Generiere Dealerhände für Startkarte {card} in Tabelle '{table_name}'...")
                self._generate_dealer_hands_recursive(table_name, [card], card)

    def _generate_dealer_hands_recursive(self, table_name, current_hand, start_card):
        """
        Rekursive Methode zur Generierung aller möglichen Dealerhände.

        Args:
            table_name (str): Name der Dealerhände-Tabelle.
            current_hand (list): Die aktuelle Hand (als Liste der Kartenwerte).
            start_card (int): Die Startkarte des Dealers.
        """
        # Berechne den Gesamtwert der aktuellen Hand
        total_value = self.deck.calculate_hand_value(current_hand)

        # Eigenschaften der Hand berechnen
        is_blackjack = len(current_hand) == 2 and total_value == 21
        is_busted = total_value > 21

        # Hand speichern, wenn sie gültig ist
        if total_value <= 21 or is_busted:  # Nur speichern, wenn Hand gültig
            self.db_manager.save_hand(
                table_name=table_name,
                hand=current_hand,
                start_card=start_card,
                total_value=total_value,
                minimum_value=None,  # Bei Dealerhänden bleibt dies leer
                is_blackjack=is_blackjack,
                is_starthand=False,  # Dealerhände sind keine Starthände
                is_busted=is_busted,
                can_double=False,  # Dealerhände können nie verdoppeln
                can_split=False,  # Dealerhände können nie splitten
                bust_chance=0,  # Für Dealerhände optional
                frequency=None  # Wird später berechnet
            )

        # Abbruchbedingung: Wenn total_value >= 17, endet die Hand (Dealer zieht nicht mehr)
        if total_value >= 17:
            return

        # Generiere neue Hände, indem jede mögliche Karte hinzugefügt wird
        for card in self.deck.get_available_cards():
            # Füge die Karte zur aktuellen Hand hinzu
            next_hand = current_hand + [card]
            # Rekursiver Aufruf
            self._generate_dealer_hands_recursive(table_name, next_hand, start_card)

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