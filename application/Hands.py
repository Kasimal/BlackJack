import csv
import json

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
        Generiert alle möglichen Hände, indem alle möglichen Starthände (zwei Karten) gebildet werden
        und anschließend alle möglichen Ziehungen simuliert werden.
        """
        # Generiere alle möglichen Starthände (zwei Karten)
        for card1, freq1 in self.deck.card_frequencies.items():
            for card2, freq2 in self.deck.card_frequencies.items():
                if card1 <= card2:
                    # Erstelle eine neue Starthand mit zwei Karten
                    temp_deck = Deck(self.deck.deck_count)
                    temp_deck.card_frequencies = self.deck.card_frequencies.copy()
                    starthand = Hand()
                    starthand.add_card_from_deck(temp_deck, card1)
                    starthand.add_card_from_deck(temp_deck, card2)

                    # Starte die Rekursion mit der Starthand
                    self.explore_hands(starthand, temp_deck)


    def explore_hands(self, current_hand, deck):
        """
        Rekursive Funktion, um alle möglichen Hände zu generieren.

        Args:
            current_hand (Hand): Die aktuelle Hand.
            deck (Deck): Der aktuelle Zustand des Decks.
        """
        # Berechne den Wert der aktuellen Hand
        current_value = current_hand.calculate_value()
        minimum_value = current_hand.calculate_value(minimum=True)

        # Füge die Hand (sortierte Starthand + gezogene Karten) und deren Wert hinzu
        self.all_hands.append((current_hand, current_value))

        # Stoppe das Ziehen, wenn der Wert der Hand über 21 beträgt
        if minimum_value >= 21:
            return

        # Für jede Karte im Deck, die noch verfügbar ist
        for card, frequency in deck.card_frequencies.items():
            if frequency > 0:
                # Erstelle eine Kopie der aktuellen Hand
                new_hand = Hand()
                new_hand.cards = current_hand.cards[:]  # Kopiere die aktuelle Hand
                new_hand.add_card_from_deck(deck, card)

                # # Erstelle ein neues Deck, indem die gezogene Karte entfernt wird
                # new_deck = Deck(deck_count=deck.deck_count)
                # new_deck.card_frequencies = deck.card_frequencies.copy()
                # new_deck.remove_card(card)

                # Rekursiv die neuen Kombinationen erkunden
                self.explore_hands(new_hand, deck)

                # Rückgängig machen, um Karte für weitere Kombinationen wieder verfügbar zu machen
                deck.add_card(card)

    def save_to_json(self, filename):
        """
        Speichert alle generierten Hände und deren Werte in eine Datei.

        Args:
            filename (str): Der Name der Datei, in die die Hände geschrieben werden.
        """
        with open(filename, "w") as file:
            json.dump(self.all_hands, file, indent=4)


    def save_to_csv(self, filename):
        """
        Speichert alle generierten Hände und deren Werte in eine CSV-Datei.

        Args:
            filename (str): Der Name der Datei, in die die Hände geschrieben werden.
        """
        with open(filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            # Schreibe die Header
            writer.writerow(["Starthand", "Gezogene Karten", "Wert"])

            # Schreibe alle Hände und deren Werte
            for current_hand, value in self.all_hands:
                starthand = sorted(current_hand.cards[:2])  # Erste zwei Karten sind die Starthand
                drawn_cards = current_hand.cards[2:]  # Alle restlichen Karten sind die gezogenen Karten
                writer.writerow([
                    ", ".join(map(str, starthand)),
                    ", ".join(map(str, drawn_cards)),
                    value
                ])


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
#for cards, value in hands.get_hands():
#    print(f"Karten: {cards}, Wert: {value}")

# Speichere die Hände in einer CSV-Datei
hands.save_to_csv("hands.csv")

# Speichere die Hände in einer Datei
#hands.save_to_json("hands.json")


