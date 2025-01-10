import random
from Models.Deck import Deck


class Hand:

    def __init__(self, cards=None):
        """
        Initialisiert eine Hand mit optionalen Karten.

        Args:
            cards (list): Eine Liste der Karten in der Hand (Standard: leer).
        """
        self.cards = cards if cards else []


    def add_card(self, card):
        """
        Fügt eine Karte zur Hand hinzu.

        Args:
            card (int): Die hinzuzufügende Karte.
        """
        self.cards.append(card)

    def add_card_from_deck(self, deck, card):
        """
        Fügt eine Karte aus dem Deck zur Hand hinzu.
        Reduziert die Häufigkeit der Karte im Deck.
        """
        if card in deck.card_frequencies and deck.card_frequencies[card] > 0:
            self.cards.append(card)
            deck.remove_card(card)
        else:
            raise ValueError(f"Karte {card} ist nicht im Deck verfügbar.")

    def draw_random_card_from_deck(self, deck):
        """
        Zieht eine zufällige Karte aus dem Deck und fügt sie der Hand hinzu.
        Reduziert die Häufigkeit der Karte im Deck.
        """
        total_cards = deck.total_cards()
        if total_cards == 0:
            raise ValueError("Das Deck ist leer, keine Karten verfügbar.")

        # Erstelle eine gewichtete Liste der Karten basierend auf ihren Häufigkeiten
        weighted_deck = [card for card, freq in deck.card_frequencies.items() for _ in range(freq)]

        # Ziehe eine zufällige Karte
        random_card = random.choice(weighted_deck)
        self.add_card_from_deck(deck, random_card)

    def calculate_value(self, minimum=False):
        """
        Berechnet den Gesamtwert der Hand.

        Args:
            minimum (bool): Wenn True, wird der minimal mögliche Wert berechnet (z. B. Ass = 1).

        Returns:
            int: Der Gesamtwert der Hand.
        """
        value = 0
        aces = 0

        for card in self.cards:
            if card == 1:
                aces += 1
                value += 11
            else:
                value += min(card, 10)

        while value > 21 and aces > 0:
            value -= 10
            aces -= 1

        return value if not minimum else value - 10 * aces

    def is_busted(self):
        """
        Prüft, ob die Hand über 21 Punkte hat.

        Returns:
            bool: True, wenn die Hand überzogen ist, sonst False.
        """
        return self.calculate_value() > 21

    def is_starthand(self):
        """
        Prüft, ob die Hand eine Starthand ist (zwei Karten).

        Returns:
            bool: True, wenn die Hand eine Starthand ist, sonst False.
        """
        return len(self.cards) == 2

    def can_double(self):
        """
        Prüft, ob ein Double möglich ist (jede Starthand außer 21).

        Returns:
            bool: True, wenn Double möglich ist, sonst False.
        """
        return self.is_starthand() and self.calculate_value() != 21

    def can_split(self):
        """
        Prüft, ob ein Split möglich ist (zwei gleiche Karten in der Starthand).

        Returns:
            bool: True, wenn Split möglich ist, sonst False.
        """
        return self.is_starthand() and len(set(self.cards)) == 1

    def card_counts(self):
        """
        Gibt ein Dictionary mit der Häufigkeit jeder Karte in der Hand zurück.

        Returns:
            dict: Ein Dictionary mit den Kartenwerten (1 bis 10) und ihrer Häufigkeit.
        """
        counts = {card: 0 for card in range(1, 11)}
        for card in self.cards:
            counts[card] += 1
        return counts

    def calculate_frequency(self, deck, previous_frequency=1):
        """
        Berechnet die Häufigkeit dieser Hand basierend auf der Häufigkeit der Vorgängerhand
        und der Häufigkeit der neu hinzugefügten Karte.

        Args:
            deck (Deck): Das aktuelle Deck.
            previous_frequency (float): Die Häufigkeit der Vorgängerhand.

        Returns:
            float: Die Häufigkeit dieser Hand.
        """
        # Bestimme die zuletzt hinzugefügte Karte
        last_card = self.cards[-1] if self.cards else None

        card_count_in_hand = self.cards.count(last_card)

        if last_card is None or card_count_in_hand == 0:
            return previous_frequency  # Keine Karte hinzugefügt

        # Häufigkeit der Karte im Deck
        card_frequency_in_deck = deck.card_frequencies[last_card]

        # Neue Häufigkeit berechnen
        return int(previous_frequency * card_frequency_in_deck / card_count_in_hand)

    def probability_to_reach_or_exceed(self, deck, target_value=21):
        """
        Berechnet die Wahrscheinlichkeit, mit der der aktuelle Wert der Hand
        einen Zielwert (target_value) erreichen oder überschreiten kann.

        Args:
            deck (Deck): Das verbleibende Deck.
            target_value (int): Zielwert, der erreicht oder überschritten werden soll (standardmäßig 21).

        Returns:
            tuple: (reach_probability, exceed_probability)
                - reach_probability: Wahrscheinlichkeit, den Zielwert genau zu erreichen.
                - exceed_probability: Wahrscheinlichkeit, den Zielwert zu überschreiten.
        """
        current_value = self.calculate_value(minimum=True)
        remaining_deck = deck.card_frequencies
        total_cards = deck.total_cards()

        if total_cards == 0:
            return 0.0, 0.0

        reach = 0
        exceed = 0

        for card, frequency in remaining_deck.items():
            if frequency == 0:
                continue

            if card == 1:  # Sonderfall Ass
                new_value = current_value + 11 if current_value + 11 <= target_value else current_value + 1
            else:
                new_value = current_value + card

            if new_value > target_value:
                exceed += frequency
            elif new_value <= target_value:
                reach += frequency

        reach_probability = reach / total_cards
        exceed_probability = exceed / total_cards

        return reach_probability, exceed_probability

    def to_db_row(self, frequency):
        """
        Konvertiert die Hand in das Format für den Datenbankeintrag.

        Args:
            frequency (integer): Die Häufigkeit der Hand.

        Returns:
            tuple: Ein Tupel, das die Spalten der Datenbanktabelle repräsentiert.
        """
        counts = self.card_counts()
        total_value = self.calculate_value()
        minimum_value = self.calculate_value(minimum=True)
        return (
            counts[1], counts[2], counts[3], counts[4], counts[5],
            counts[6], counts[7], counts[8], counts[9], counts[10],
            total_value, minimum_value,
            self.is_busted(), self.is_starthand(), self.can_double(), self.can_split(), frequency
        )

    def __repr__(self):
        return f"Hand(cards={self.cards}, value={self.calculate_value()})"
