from collections import Counter
import math

from Models.Deck import Deck


def hand_frequency_with_order(current_hand, original_frequencies, cards_to_ignore=1):
    """
    Berechnet die Häufigkeit einer Hand unter Berücksichtigung der Reihenfolge,
    wobei die Startkarte nicht in die Berechnung einbezogen wird.

    Args:
        current_hand (list): Die aktuelle Hand (als Liste der Kartenwerte).
        original_frequencies (dict): Originale Häufigkeiten der Karten.
        cards_to_ignore (int): Wie viele Startkarten nicht in die Rechnung einbezogen werden sollen. Default ist 1 für die Startkarte.

    Returns:
        int: Die Häufigkeit der Hand unter Berücksichtigung der Reihenfolge.
    """
    if not current_hand or len(current_hand) < 2:
        return 0  # Eine Hand ohne Karten oder nur mit der Startkarte hat keine Häufigkeit

    # Die erste Karte wird als Startkarte ignoriert
    remaining_hand = current_hand[cards_to_ignore:]  # Alle Karten außer der Startkarte

    # Kopie der Originalfrequenzen erstellen, um Veränderungen zu vermeiden
    temp_frequencies = original_frequencies.copy()

    # Berechnung der Häufigkeit
    frequency = 1
    for card in remaining_hand:
        if temp_frequencies[card] > 0:
            frequency *= temp_frequencies[card]
            temp_frequencies[card] -= 1
        else:
            return 0  # Ungültige Hand, wenn eine Karte nicht verfügbar ist

    return frequency

def hand_frequency(cards, deck=None):
    """
    Berechnet die Häufigkeit einer Hand basierend auf den fehlenden Karten.

    Args:
        cards (list): Eine Liste mit den fehlenden Karten.
        deck (Deck, optional): Eine Instanz des Decks, um die Kartenhäufigkeiten zu erhalten.
                               Wenn nicht angegeben, wird ein Standarddeck verwendet.

    Returns:
        int: Die Häufigkeit der Hand.
    """
    if deck is None:
        deck = Deck()

    # Hole die ursprünglichen Frequenzen aus dem Deck
    original_card_frequencies = deck.card_frequencies

    card_counts = Counter(cards)  # Zähle, wie viele Karten welchen Typs fehlen
    frequency = 1

    # Berechne die Häufigkeit basierend auf den Karten im Deck
    for card, count in card_counts.items():
        original_count = original_card_frequencies[card]  # Anzahl der Karten im Deck

        # Berechne die Häufigkeit der Hand
        for i in range(count):
            frequency *= (original_count - i)  # Berücksichtige jede Karte der Hand
        frequency //= math.factorial(count)  # Teile durch die Anzahl der Permutationen

    return frequency

def bust_probability(current_hand, deck=None):
    """
    Berechnet die Wahrscheinlichkeit, dass eine Hand überboten wird.
    Args:
        current_hand (list[int]): Die aktuelle Hand.
        deck (Deck, optional): Eine Instanz des Decks, um die Kartenhäufigkeiten zu erhalten.
                       Wenn nicht angegeben, wird ein Standarddeck verwendet.
    Returns:
        float: Wahrscheinlichkeit, dass die Hand überboten wird.
    """
    if deck is None:
        deck = Deck()

    minimum_value = hand_value(current_hand, minimum=True)

    if minimum_value <=11:
        return 0.0  # Es ist nicht möglich zu überbieten
    if minimum_value >=21:
        return 1.0  # Jede Karte überbietet

    # Berechne verbleibende Karten im Deck basierend auf `original_card_frequencies`
    remaining_frequencies = {
        card: deck.original_card_frequencies.get(card, 0) - current_hand.count(card)
        for card in deck.original_card_frequencies
    }

    # Gesamte Anzahl verbleibender Karten
    total_cards_left = sum(remaining_frequencies.values())
    if total_cards_left <= 0:
        return 0.0  # Keine Karten mehr im Deck, überbieten nicht möglich

    # Finde Karten, die die Hand über 21 bringen
    bust_cards = [card for card in remaining_frequencies if minimum_value + card > 21]
    bust_card_count = sum(remaining_frequencies.get(card, 0) for card in bust_cards)

    # Berechne die Wahrscheinlichkeit
    return bust_card_count / total_cards_left

def hand_value(hand, minimum=False):
    """
    Berechnet den Wert einer Hand.

    Args:
        hand (dict or list): Die Hand als Wörterbuch (Kartenwert -> Anzahl) oder Liste.
        minimum (bool): Wenn True, wird der minimale Wert der Hand berechnet.

    Returns:
        int: Der berechnete Wert der Hand.
    """
    # Wenn die Hand eine Liste ist, wandle sie in ein Wörterbuch um
    if isinstance(hand, list):
        hand = Counter(hand)

    # Berechnung basierend auf dem Wörterbuch
    total_value = sum(card * count for card, count in hand.items())
    if not minimum:
        ace_count = hand.get(1, 0)
        while ace_count > 0 and total_value <= 11:
            total_value += 10
            ace_count -= 1
    return total_value

def hand_probability(hand, deck=None, start_cards=None):
    """
    Berechnet die Wahrscheinlichkeit einer bestimmten Hand basierend auf der Häufigkeit der Karten im Deck,
    wobei mögliche Startkarten ausgeschlossen werden.

    Args:
        hand (list): Eine Liste von Karten in der Hand (z.B. [10, 2, 1, 1, 1, 1, 5]).
        deck (Deck): Eine Deck-Instanz, die die Häufigkeit jeder Karte enthält.
        start_cards (list, optional): Eine Liste von Karten, die als Startkarten genutzt werden und aus der Berechnung ausgeschlossen werden sollen.

    Returns:
        float: Die Wahrscheinlichkeit, die gegebene Hand zu ziehen, unter Berücksichtigung der Deckzusammensetzung.
    """
    probability = 1.0
    if deck is None:
        deck_copy = Deck()
    else:
        deck_copy = deck.copy()  # Hole eine Kopie des Decks
    total_cards = deck_copy.total_cards()  # Gesamtzahl der Karten im Deck

    # Zählt, wie oft jede Startkarte in der Hand vorkommt
    start_card_counts = {card: start_cards.count(card) for card in set(start_cards)} if start_cards else {}

    # Berechnung der Wahrscheinlichkeit für die Hand
    for card in hand:
        if card in start_card_counts and start_card_counts[card] > 0:
            start_card_counts[card] -= 1  # Ignoriere genau eine Instanz dieser Karte
            continue

        if deck_copy.card_frequencies[card] > 0:
            probability *= deck_copy.card_frequencies[card] / total_cards
            deck_copy.remove_card(card)  # Entferne die gezogene Karte aus der Kopie des Decks
            total_cards -= 1
        else:
            return 0  # Falls eine Karte nicht mehr verfügbar ist, ist die Wahrscheinlichkeit 0

    return probability
