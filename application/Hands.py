from Models.Deck import Deck
from application.db import DatabaseManager
import copy

class Hands:
    def __init__(self, deck, db_manager):
        """
        Initialisiert die Hands-Klasse.

        Args:
            deck (Deck): Das ursprüngliche Deck, das für die Hand-Generierung verwendet wird.
            db_manager (DatabaseManager): Datenbankmanager zum Speichern der generierten Hände.
        """
        self.deck = deck
        self.db_manager = db_manager

    def generate_and_save_hands(self, max_cards):
        """
        Generiert und speichert alle möglichen Hände bis zur angegebenen maximalen Kartenanzahl.

        Args:
            max_cards (int): Die maximale Anzahl an Karten in einer Hand.
        """
        for total_cards in range(2, max_cards + 1):
            self.generate_hands_recursive(total_cards, [])

    def generate_hands_recursive(self, total_cards, current_hand):
        """
        Rekursive Funktion, um alle möglichen Hände zu generieren und zu speichern.

        Args:
            total_cards (int): Die maximale Anzahl an Karten in einer Hand.
            current_hand (list): Die aktuell generierte Hand.
        """
        # Basisfall: Maximale Anzahl an Karten erreicht
        if len(current_hand) == total_cards:
            # Erstelle eine Kopie des Decks und entferne die aktuellen Karten
            deck = self.deck.copy()
            for card in current_hand:
                deck.remove_card(card)

            # Berechne die Eigenschaften der Hand
            missing_cards = deck.get_missing_cards()
            total_value = deck.calculate_hand_value(missing_cards)
            minimum_value = deck.calculate_hand_value(missing_cards, minimum=True)
            is_starthand = len(current_hand) == 2
            is_busted = total_value > 21
            can_double = is_starthand and total_value != 21
            can_split = is_starthand and current_hand[0] == current_hand[1]
            frequency = deck.calculate_hand_frequency(current_hand)

            # Speichere die Hand in der Datenbank
            self.db_manager.save_hand(
                deck,
                total_value,
                minimum_value,
                is_starthand,
                is_busted,
                can_double,
                can_split,
                frequency
            )
            return

        # Rekursionsschritt: Hand mit einer weiteren Karte erweitern
        for card, frequency in self.deck.card_frequencies.items():
            if frequency > 0:
                next_hand = current_hand + [card]
                self.generate_hands_recursive(total_cards, next_hand)


