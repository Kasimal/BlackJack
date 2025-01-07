import sqlite3

from Deck import Deck
from Hand import Hand


class Hands:
    def __init__(self, deck):
        """
        Initialisiert die Klasse Hands mit einem gegebenen Deck.
        Speichert alle möglichen Hände und deren Werte.
        """
        self.deck = deck
        self.all_hands = []

    def generate_all_hands(self):
        """
        Generiert alle möglichen Hände, indem Karten aus dem Deck gezogen werden.
        Stoppt das Ziehen, wenn der Wert einer Hand 21 oder mehr beträgt.
        """
        initial_hand = Hand()
        self._explore_hands(initial_hand, self.deck)

    def _explore_hands(self, current_hand, current_deck):
        """
        Rekursive Funktion, um alle möglichen Hände zu generieren.

        Args:
            current_hand (Hand): Die aktuelle Hand.
            current_deck (Deck): Der aktuelle Zustand des Decks.
        """
        # Berechne den Wert der aktuellen Hand
        current_value = current_hand.calculate_value()

        # Stoppe, wenn der Wert 21 oder mehr beträgt
        if current_value >= 21:
            self.all_hands.append((current_hand.cards[:], current_value))
            return

        # Für jede Karte im Deck, die noch verfügbar ist
        for card, frequency in current_deck.card_frequencies.items():
            if frequency > 0:
                # Erstelle Kopien von Hand und Deck
                new_hand = Hand()
                new_hand.cards = current_hand.cards[:]  # Kopiere die aktuelle Hand
                new_hand.add_card_from_deck(current_deck, card)

                new_deck = Deck(deck_count=current_deck.deck_count)
                new_deck.card_frequencies = current_deck.card_frequencies.copy()
                new_deck.remove_card(card)

                # Rekursiv die neuen Kombinationen erkunden
                self._explore_hands(new_hand, new_deck)

    def get_hands(self):
        """
        Gibt alle generierten Hände mit ihrem Wert zurück.
        """
        return self.all_hands

# Erstelle ein Deck
deck = Deck(deck_count=1)

# Erstelle eine Instanz von Hands
hands = Hands(deck)

# Generiere alle möglichen Hände
hands.generate_all_hands()

# Zeige die generierten Hände mit ihren Werten
for cards, value in hands.get_hands():
    print(f"Karten: {cards}, Wert: {value}")
