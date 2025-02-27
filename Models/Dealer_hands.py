import Utility.Calculations as calc


class DealerHands:
    def __init__(self, deck, db_manager=None):
        # Initialisierung der Dealer-spezifischen Eigenschaften
        self.dealer_threshold = 17  # Mindestwert, ab dem der Dealer stoppt
        self.deck = deck
        if db_manager is not None: self.db_manager = db_manager


    def generate_dealer_hands(self, table_name, start_card=None, missing_cards=None):
        """
        Generiert und speichert alle möglichen Dealerhände für eine bestimmte Startkarte oder für alle Karten.

        Args:
            table_name (str): Name der Dealerhände-Tabelle.
            start_card (int, optional): Die Startkarte des Dealers (z. B. 1 für Ass, 2 für 2 usw.).
                                        Wenn None, werden alle Startkarten generiert.
            missing_cards (list, optional): Liste von Karten, deren Häufigkeit im Deck reduziert werden soll.
        """
        # Abrufen der Originalfrequenzen aus dem Deck (Kopie erstellen, um Original nicht zu verändern)
        original_frequencies = self.deck.original_card_frequencies.copy()

        # Reduziere die Häufigkeit der fehlenden Karten
        if missing_cards:
            for card in missing_cards:
                if card in original_frequencies:
                    original_frequencies[card] = max(0, original_frequencies[card] - 1)  # Verhindert negative Werte

        # Liste für Batch-Insert erstellen
        hands_to_insert = []

        if start_card:
            # Validierung der Startkarte
            if start_card not in self.deck.get_available_cards():
                raise ValueError(f"Ungültige Startkarte: {start_card}. Die Startkarte muss zwischen 1 und 10 liegen.")
            print(f"Generiere Dealerhände für Startkarte {start_card} in Tabelle '{table_name}'...")
            original_frequencies[start_card] -= 1
            self._generate_dealer_hands_recursive(table_name, [start_card], start_card, original_frequencies,
                                                  hands_to_insert)
        else:
            # Generiere Dealerhände für alle möglichen Startkarten
            for card in self.deck.get_available_cards():
                print(f"Generiere Dealerhände für Startkarte {card} in Tabelle '{table_name}'...")
                original_frequencies[card] -= 1
                self._generate_dealer_hands_recursive(table_name, [card], card, original_frequencies, hands_to_insert)
                original_frequencies[card] += 1

        # Alle Hände speichern, nachdem die Rekursion abgeschlossen ist
        if hands_to_insert:
            self.db_manager.save_hands(table_name, hands_to_insert)
            print(f"{len(hands_to_insert)} Dealerhände gespeichert in Tabelle '{table_name}'.")


    def _generate_dealer_hands_recursive(self, table_name, current_hand, start_card, original_frequencies,
                                         hands_to_insert):
        """
        Rekursive Methode zur Generierung aller möglichen Dealerhände.

        Args:
            table_name (str): Name der Tabelle.
            current_hand (list): Die aktuelle Hand (als Liste der Kartenwerte).
            start_card (int): Die Startkarte des Dealers.
            original_frequencies: Eine Kopie der Anzahlen des aktuellen Decks, um Karten zu entnehmen.
            hands_to_insert (list): Liste für das Batch-Speichern der Hände.
        """
        total_value = calc.hand_value(current_hand)
        is_blackjack = len(current_hand) == 2 and total_value == 21
        is_busted = total_value > 21

        # Hand speichern, wenn Dealer mindestens 17 hat
        if total_value >= self.dealer_threshold:
            print(f"Speichere Hand: {current_hand}")
            hands_to_insert.append({
                "hands_type": "dealer",
                "hand": current_hand.copy(),
                "start_card": start_card,
                "total_value": total_value,
                "minimum_value": None,
                "is_blackjack": is_blackjack,
                "is_starthand": False,
                "is_busted": is_busted,
                "can_double": False,
                "can_split": False,
                "bust_chance": 0,
                "frequency": calc.hand_frequency_with_order(current_hand, original_frequencies, cards_to_ignore=1),
                "probability": calc.hand_probability(current_hand)
            })
            return

        # Rekursive Erweiterung nur mit verfügbaren Karten
        for card in self.deck.get_available_cards():
            if original_frequencies[card] > 0:  # Nur Karten nutzen, die noch verfügbar sind
                next_hand = current_hand + [card]

                # Reduziere die Verfügbarkeit der Karte temporär
                original_frequencies[card] -= 1
                self._generate_dealer_hands_recursive(table_name, next_hand, start_card, original_frequencies, hands_to_insert)
                original_frequencies[card] += 1  # Wiederherstellung nach Rekursion

    def just_generate_dealer_hands(self, start_card, deck):
        """
        Generiert alle möglichen Dealer-Hände basierend auf einer Startkarte und berechnet deren Wahrscheinlichkeiten,
        ohne sie in die Datenbank zu speichern.

        Args:
            start_card (int): Die erste Karte des Dealers.
            deck (Deck): Instanz des Decks.

        Returns:
            dict: Verteilung der Dealer-Hände mit Wahrscheinlichkeiten für ≤16, 17, 18, 19, 20, 21, Blackjack und Bust.
        """
        dealer_hands = {}
        total_frequency = self.just_generate_dealer_hands_recursive([start_card], deck, dealer_hands, no_blackjack=True if start_card in [10, 1] else False)

        # Wahrscheinlichkeiten berechnen
        if total_frequency > 0:
            for key in dealer_hands:
                dealer_hands[key] /= total_frequency

        return dealer_hands

    def just_generate_dealer_hands_recursive(self, current_hand, deck, dealer_hands, no_blackjack=False):
        """
        Rekursive Funktion zur Generierung aller möglichen Dealer-Hände und deren Wahrscheinlichkeiten.

        Args:
            current_hand (list[int]): Aktuelle Karten der Dealer-Hand.
            deck (Deck): Instanz des Decks.
            dealer_hands (dict): Sammlung der Dealer-Hand-Wahrscheinlichkeiten.
            no_blackjack (bool): Falls True, werden keine Blackjacks generiert (nach Start mit 10 oder Ass).
        Returns:
            int: Gesamtanzahl der generierten Hände (inklusive ihrer Häufigkeiten).
        """
        # Berechne die Gesamtwerte
        total_value = calc.hand_value(current_hand)
        minimum_value = calc.hand_value(current_hand, minimum=True)

        # Wahrscheinlichkeit der aktuellen Hand berechnen
        hand_prob = calc.hand_probability(current_hand, self.deck)

        # Wenn die Hand über 21 geht, als Bust markieren
        if minimum_value > 21:
            dealer_hands["Bust"] = dealer_hands.get("Bust", 0) + hand_prob
            return hand_prob

        # Falls mindestens 17 erreicht wurde, Hand speichern
        if total_value >= 17:
            key = "Blackjack" if total_value == 21 and len(current_hand) == 2 else str(total_value)
            dealer_hands[key] = dealer_hands.get(key, 0) + hand_prob
            return hand_prob

        total_generated = 0
        # Nächste Karten ziehen
        for card in deck.get_available_cards():
            if len(current_hand) == 1 and no_blackjack and (
                    (current_hand[0] == 10 and card == 1) or (current_hand[0] == 1 and card == 10)):
                continue  # Verhindere Blackjack nach Start mit 10 oder Ass

            next_hand = current_hand + [card]
            if next_hand.count(card) <= deck.original_card_frequencies.get(card, 0):
                result = self.just_generate_dealer_hands_recursive(next_hand, deck, dealer_hands, no_blackjack)
                if result is not None:
                    total_generated += result

        return total_generated
