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
        Generiert alle möglichen Hände basierend auf dem Deck und speichert sie in die Datenbank.
        """
        # Bereite die Datenbank vor
        self.db_manager.create_table()

        # Iteriere über alle möglichen Kartenanzahlen
        for total_cards in range(2, 12):  # 2 bis maximal 11 Karten pro Hand
            print(f"Generiere Hände mit {total_cards} Karten...")
            self.generate_hands_recursive(total_cards, [])

    def generate_hands_recursive(self, cards_left, current_hand):
        """
        Rekursive Methode, um alle möglichen Hände mit einer bestimmten Anzahl von Karten zu generieren.

        Args:
            cards_left (int): Anzahl der noch zu ziehenden Karten.
            current_hand (list): Aktuelle Hand als Liste von Kartenanzahlen.
        """
        # Basisfall: Keine Karten mehr übrig, speichere die Hand
        if cards_left == 0:
            frequency = self.deck.calculate_hand_frequency(current_hand)
            self.db_manager.save_hand(self.deck, frequency)
            return

        # Rekursion: Ziehe Karten basierend auf den verbleibenden Frequenzen im Deck
        for card, frequency in self.deck.card_frequencies.items():
            if frequency > 0:  # Nur Karten mit verfügbarer Häufigkeit berücksichtigen
                # Aktualisiere die Frequenzen des Decks und der aktuellen Hand
                self.deck.card_frequencies[card] -= 1
                current_hand.append(card)

                # Rekursive Funktion aufrufen
                self.generate_hands_recursive(cards_left - 1, current_hand)

                # Rückgängig machen (Backtracking)
                current_hand.pop()
                self.deck.card_frequencies[card] += 1
