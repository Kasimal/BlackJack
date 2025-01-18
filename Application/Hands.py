from Models.Deck import Deck
from Application.db import DatabaseManager

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

    def generate_and_save_hands(self):
        """
        Generiert und speichert alle möglichen Hände mit einem maximalen minimum_value von 21.
        Die Hände werden sortiert generiert und gespeichert.
        """
        self.generate_hands_recursive([])

    def generate_hands_recursive(self, current_hand, start_card=1):
        """
        Rekursive Funktion zur Generierung von Händen in sortierter Reihenfolge.

        Args:
            current_hand (list): Die aktuelle Hand als Liste der Kartenzahlen.
            start_card (int): Die minimale Karte, die in dieser Iteration hinzugefügt werden darf.
        """
        # Berechne den Minimalwert der aktuellen Hand
        minimum_value = self.deck.calculate_hand_value(current_hand, minimum=True)

        # Abbruchbedingung: Wenn der Mindestwert der Hand > 21 ist, keine weitere Berechnung
        if minimum_value > 21:
            return

        # Berechne den Gesamtwert der aktuellen Hand
        total_value = self.deck.calculate_hand_value(current_hand)

        # Eigenschaften der Hand berechnen
        is_starthand = len(current_hand) == 2
        is_blackjack = total_value == 21 and is_starthand
        is_busted = minimum_value > 21
        can_double = is_starthand and total_value < 21
        can_split = is_starthand and current_hand[0] == current_hand[1]

        # Häufigkeit der aktuellen Hand berechnen
        frequency = self.deck.calculate_hand_frequency(current_hand)

        # Hand speichern
        self.db_manager.save_hand(
            current_hand, total_value, minimum_value, is_blackjack, is_starthand, is_busted, can_double, can_split, frequency
        )

        # Erzeuge neue Hände, indem jede mögliche Karte zur aktuellen Hand hinzugefügt wird
        for card in self.deck.get_available_cards():
            if card >= start_card:  # Nur Karten hinzufügen, die >= der letzten Karte sind
                next_hand = current_hand + [card]  # Füge die Karte zur aktuellen Hand hinzu
                if self.deck.original_card_frequencies[card] - next_hand.count(card) >= 0:
                    print(next_hand)
                    self.generate_hands_recursive(next_hand, start_card=card)






