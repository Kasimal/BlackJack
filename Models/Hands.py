from Models.Deck import Deck
from Utility.DB import DatabaseManager
import Utility.Calculations as calc

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

    def generate_and_save_hands(self, missing_cards=None):
        """
        Generiert und speichert alle möglichen Hände mit einem maximalen minimum_value von 21.
        Die Hände werden sortiert generiert und gespeichert.

        Args:
            missing_cards (list, optional): Liste von Karten, deren Häufigkeit im Deck reduziert werden soll.
        """
        # Kopie der Originalfrequenzen, um Änderungen vorzunehmen
        adjusted_frequencies = self.deck.original_card_frequencies.copy()

        # Reduziere die Häufigkeit der fehlenden Karten
        if missing_cards:
            for card in missing_cards:
                if card in adjusted_frequencies:
                    adjusted_frequencies[card] = max(0, adjusted_frequencies[card] - 1)  # Verhindert negative Werte

        self.generate_hands_recursive([], 1, [], adjusted_frequencies)

    def generate_hands_recursive(self, current_hand=None, start_card=1, hands_to_insert=None, adjusted_frequencies=None):
        """
        Rekursive Funktion zur Generierung von Händen in sortierter Reihenfolge.

        Args:
            current_hand (list): Die aktuelle Hand als Liste der Kartenzahlen.
            start_card (int): Die minimale Karte, die in dieser Iteration hinzugefügt werden darf.
            hands_to_insert (list): Liste der gesammelten Hände für den Batch-Insert.
            adjusted_frequencies (dict): Angepasste Kartenzählung nach Abzug der missing_cards.
        """
        if current_hand is None:
            current_hand = []
        if hands_to_insert is None:
            hands_to_insert = []  # Initialisierung hier innerhalb der Methode
        if adjusted_frequencies is None:
            adjusted_frequencies = self.deck.original_card_frequencies.copy()  # Falls keine Änderungen nötig sind

        # Berechne den Minimalwert der aktuellen Hand
        minimum_value = calc.hand_value(current_hand, minimum=True)

        # Abbruchbedingung: Wenn der Mindestwert der Hand > 21 ist, keine weitere Berechnung
        if minimum_value > 21:
            return

        # Berechne den Gesamtwert der aktuellen Hand
        total_value = calc.hand_value(current_hand)

        # Eigenschaften der Hand berechnen
        is_starthand = len(current_hand) == 2
        is_blackjack = total_value == 21 and is_starthand
        is_busted = minimum_value > 21
        can_double = is_starthand and total_value < 21
        can_split = is_starthand and current_hand[0] == current_hand[1]

        # Häufigkeit der aktuellen Hand berechnen
        frequency = calc.hand_frequency(current_hand)

        # Wahrscheinlichkeit zu überbieten
        bust_chance = calc.bust_probability(current_hand)

        # Hand in die Liste aufnehmen
        hands_to_insert.append({
            "hands_type": "player",
            "hand": current_hand.copy(),
            "start_card": None,
            "total_value": total_value,
            "minimum_value": minimum_value,
            "is_blackjack": is_blackjack,
            "is_starthand": is_starthand,
            "is_busted": is_busted,
            "can_double": can_double,
            "can_split": can_split,
            "bust_chance": bust_chance,
            "frequency": frequency,
            "probability": 0.0  # nicht erforderlich
        })

        # Erzeuge neue Hände, indem jede mögliche Karte zur aktuellen Hand hinzugefügt wird
        for card in self.deck.get_available_cards():
            if card >= start_card:  # Nur Karten hinzufügen, die >= der letzten Karte sind
                next_hand = current_hand + [card]  # Füge die Karte zur aktuellen Hand hinzu

                # Überprüfe, ob die Karte noch verfügbar ist (nicht mehr als erlaubt vorhanden)
                if next_hand.count(card) <= adjusted_frequencies[card]:
                    self.generate_hands_recursive(next_hand, card, hands_to_insert,
                                                  adjusted_frequencies)  # Jetzt korrekt

        # Nach der Rekursion: Alle Hände auf einmal speichern
        if not current_hand:  # Nur nach der vollständigen Generierung speichern
            self.db_manager.save_hands("hands", hands_to_insert)
            print(f"{len(hands_to_insert)} Hände wurden erfolgreich gespeichert.")









