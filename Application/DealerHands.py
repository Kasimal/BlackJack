from Hands import Hands

class DealerHands(Hands):
    def __init__(self, deck, db_manager):
        super().__init__(deck, db_manager)
        # Zusätzliche Eigenschaften für Dealer-spezifische Logik
        self.dealer_threshold = 17  # Mindestwert, ab dem der Dealer stoppt

    def generate_dealer_hands(self):
        """
        Generiere nur mögliche Dealer-Hände.
        """
        # Nur die 10 sichtbaren Karten für die Starthand verwenden
        for card in self.deck.get_available_cards():
            starting_hand = [card]
            self.generate_hands_recursive(starting_hand)

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
        for total_value, frequency in self.db_manager.get_all_hands():
            if total_value > 21:
                outcomes["Busted"] += frequency
            elif total_value == 21 and len([card for card in range(1, 11) if card == 1]) == 1:
                outcomes["Blackjack"] += frequency
            elif 17 <= total_value <= 21:
                outcomes[str(total_value)] += frequency
        return outcomes