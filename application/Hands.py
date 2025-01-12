from Models.Deck import Deck
from application.db import DatabaseManager


class Hands:
    def __init__(self, deck_count=6):
        """
        Initialisiert die Hands-Klasse mit einem Deck und einem DatabaseManager.

        Args:
            deck_count (int): Anzahl der Kartensätze im Deck.
        """
        self.deck = Deck(deck_count)
        self.db_manager = DatabaseManager()

    def generate_and_save_hands(self):
        """
        Generiert alle möglichen Hände und speichert sie in der Datenbank.
        """
        for card1, freq1 in self.deck.card_frequencies.items():
            for card2, freq2 in self.deck.card_frequencies.items():
                if card1 <= card2:  # Doppelte Kombinationen vermeiden
                    # Erstelle eine Starthand
                    starting_hand = [card1, card2]
                    deck_copy = Deck(self.deck.deck_count)
                    deck_copy.remove_card(card1)
                    deck_copy.remove_card(card2)

                    # Starte die Rekursion
                    self.generate_hands_recursive(starting_hand, deck_copy)

    def generate_hands_recursive(self, current_hand, deck, depth=0):
        """
        Rekursive Funktion, um alle möglichen Hände zu generieren und in die Datenbank zu speichern.

        Args:
            current_hand (list): Die aktuelle Hand, dargestellt als Liste von Karten.
            deck (Deck): Der aktuelle Zustand des Decks.
            depth (int): Die Tiefe der Rekursion (Anzahl der bisher gezogenen Karten).
        """
        # Berechne Werte und Eigenschaften der aktuellen Hand
        total_value = deck.calculate_value()
        minimum_value = deck.calculate_value( minimum=True)
        is_starthand = (depth == 2)
        is_busted = (minimum_value > 21)
        can_double = is_starthand and total_value != 21
        can_split = is_starthand and current_hand[0] == current_hand[1]
        frequency = deck.calculate_hand_frequency(current_hand)

        # Speicher die Hand in der Datenbank
        card_counts = [current_hand.count(card) for card in range(1, 11)]
        self.db_manager.save_hand(card_counts, total_value, minimum_value, is_starthand, is_busted, can_double, can_split, frequency)

        # Stoppe, wenn die Hand gebustet ist
        if is_busted:
            return

        # Rekursiv weitere Karten ziehen
        for card, count in deck.card_frequencies.items():
            if count > 0:
                # Erstelle eine Kopie des Decks und ziehe die Karte
                new_deck = Deck(deck.deck_count)
                new_deck.card_frequencies = deck.card_frequencies.copy()
                new_deck.restore_card(card)

                # Erstelle die neue Hand
                new_hand = current_hand + [card]

                # Rekursiver Aufruf
                self.generate_hands_recursive(new_hand, new_deck, depth + 1)

