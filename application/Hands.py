from Models.Deck import Deck
from Models.Hand import Hand


class Hands:
    def __init__(self, deck, db_manager):
        """
        Initialisiert die Klasse Hands mit einem gegebenen Deck.
        Speichert alle möglichen Hände und deren Werte.
        """
        self.deck = deck
        self.all_hands = []
        self.db_manager = db_manager

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

    def generate_and_save_hands(self, deck):
        """
        Generiert alle möglichen Hände und speichert sie iterativ in der Datenbank.
        Args:
            deck (Deck): Das Deck, das für die Berechnung verwendet wird.
        """
        # Schritt 1: Generiere alle Starthände (2 Karten)
        hands = []
        for card1, freq1 in deck.card_frequencies.items():
            for card2, freq2 in deck.card_frequencies.items():
                if card1 <= card2:  # Verhindert doppelte Kombinationen
                    starthand = Hand(cards=[card1, card2], is_starthand=True)
                    starthand.frequency = starthand.calculate_frequency(deck)
                    hands.append(starthand)
                    self.db_manager.save_hand(starthand, deck)  # Speichere Starthand

        # Schritt 2: Iterativ weitere Karten hinzufügen
        # while hands:
        #     new_hands = []
        #     for hand in hands:
        #         for card, frequency in deck.card_frequencies.items():
        #             if frequency > hand.cards.count(card):  # Prüfe, ob die Karte verfügbar ist
        #                 new_hand = Hand(cards=hand.cards + [card])
        #                 new_hand.frequency = new_hand.calculate_frequency(deck)
        #                 new_hands.append(new_hand)
        #                 self.db_manager.save_hand(new_hand, deck)  # Speichere Hand
        #     hands = new_hands  # Aktualisiere die Liste für die nächste Iteration

    # def explore_and_save_hands(self, current_hand, deck, previous_frequency):
    #     """
    #     Rekursive Funktion, um alle möglichen Hände zu generieren und zu speichern.
    #
    #     Args:
    #         current_hand (Hand): Die aktuelle Hand.
    #         deck (Deck): Der aktuelle Zustand des Decks.
    #         previous_frequency (float): Die Häufigkeit der Vorgängerhand.
    #     """
    #     # Berechne den Wert der aktuellen Hand
    #     minimum_value = current_hand.calculate_value(minimum=True)
    #
    #     # Stoppe das Ziehen, wenn die minimale Hand bereits überzogen ist
    #     if minimum_value >= 21:
    #         return
    #
    #     # Iteriere über alle verfügbaren Karten im Deck
    #     for card, frequency in deck.card_frequencies.items():
    #         if frequency > 0:
    #             # Erstelle eine Kopie der aktuellen Hand und füge die Karte hinzu
    #             new_hand = Hand()
    #             new_hand.cards = current_hand.cards[:]
    #             new_hand.add_card_from_deck(deck, card)
    #
    #             # Erstelle ein neues Deck mit der Karte entfernt
    #             new_deck = Deck(deck.deck_count)
    #             new_deck.card_frequencies = deck.card_frequencies.copy()
    #             new_deck.remove_card(card)
    #
    #             # Berechne die neue Häufigkeit und speichere die Hand
    #             new_frequency = new_hand.calculate_frequency(deck, previous_frequency)
    #             self.db_manager.save_hand(new_hand, new_deck, previous_frequency=new_frequency)
    #
    #             # Rekursiv die neuen Kombinationen erkunden
    #             self.explore_and_save_hands(new_hand, new_deck, previous_frequency=new_frequency)

# # Erstelle ein Deck
# deck = Deck(deck_count=1)
#
# # Erstelle eine Instanz von Hands
# hands = Hands(deck)
#
# # Generiere alle möglichen Hände
# hands.generate_all_hands()
#
# # Zeige die generierten Hände mit ihren Werten
# for cards, value in hands.get_hands():
# print(f"Karten: {cards}, Wert: {value}")
