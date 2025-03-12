from collections import Counter
from Models.Deck import Deck
import math



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


def probability_distribution(current_hand, deck=None, dealer_cards=None):
    """
    Berechnet die Wahrscheinlichkeitsverteilung für eine Hand beim Ziehen einer weiteren Karte,
    unter Berücksichtigung bekannter Dealer-Karten.

    Args:
        current_hand (list[int]): Die aktuelle Hand.
        deck (Deck, optional): Eine Instanz des Decks, um die Kartenhäufigkeiten zu erhalten.
                               Wenn nicht angegeben, wird ein Standarddeck verwendet.
        dealer_cards (list[int], optional): Bekannte Karten des Dealers, die aus dem Deck entfernt werden.

    Returns:
        dict: Ein Dictionary mit den Wahrscheinlichkeiten für:
              - "≤16": Wahrscheinlichkeit für alle Werte 16 oder kleiner.
              - "17": Wahrscheinlichkeit genau 17 zu erreichen.
              - "18": Wahrscheinlichkeit genau 18 zu erreichen.
              - "19": Wahrscheinlichkeit genau 19 zu erreichen.
              - "20": Wahrscheinlichkeit genau 20 zu erreichen.
              - "21": Wahrscheinlichkeit genau 21 zu erreichen (ohne Blackjack).
              - "Blackjack": Wahrscheinlichkeit für einen Blackjack (nur mit zwei Karten).
              - "Bust": Wahrscheinlichkeit, die Hand zu überbieten (>21).
    """
    if deck is None:
        deck = Deck()

    if dealer_cards is None:
        dealer_cards = []

    minimum_value = hand_value(current_hand, minimum=True)

    # Wenn die Hand schon über 21 ist, sind alle Wahrscheinlichkeiten 0, außer "Bust"
    if minimum_value > 21:
        return {"<=16": 0.0, "17": 0.0, "18": 0.0, "19": 0.0, "20": 0.0, "21": 0.0, "Blackjack": 0.0, "Bust": 1.0}

    # Verbleibende Karten berechnen unter Berücksichtigung der bekannten Dealer-Karten
    remaining_frequencies = {
        card: max(0, deck.original_card_frequencies.get(card, 0) - current_hand.count(card) - dealer_cards.count(card))
        for card in deck.original_card_frequencies
    }

    total_cards_left = sum(remaining_frequencies.values())
    if total_cards_left <= 0:
        return {"<=16": 0.0, "17": 0.0, "18": 0.0, "19": 0.0, "20": 0.0, "21": 0.0, "Blackjack": 0.0, "Bust": 0.0}

    probabilities = {"<=16": 0.0, "17": 0.0, "18": 0.0, "19": 0.0, "20": 0.0, "21": 0.0, "Blackjack": 0.0, "Bust": 0.0}

    # Wahrscheinlichkeiten berechnen
    for card, count in remaining_frequencies.items():
        if count > 0:
            new_hand = current_hand + [card]
            new_value = hand_value(new_hand)

            if new_value <= 16:
                probabilities["<=16"] += count / total_cards_left
            elif new_value == 17:
                probabilities["17"] += count / total_cards_left
            elif new_value == 18:
                probabilities["18"] += count / total_cards_left
            elif new_value == 19:
                probabilities["19"] += count / total_cards_left
            elif new_value == 20:
                probabilities["20"] += count / total_cards_left
            elif new_value == 21:
                if len(current_hand) == 1:  # Falls genau zwei Karten genutzt werden → Blackjack
                    probabilities["Blackjack"] += count / total_cards_left
                else:
                    probabilities["21"] += count / total_cards_left
            else:  # Alles über 21 → Bust
                probabilities["Bust"] += count / total_cards_left

    return probabilities


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


#          Player               Win/Loss/Draw Matrix
# Dealer | <=16  | 17    | 18    | 19    | 20    | 21    | Blackjack | Bust
# -------|-------|-------|-------|-------|-------|-------|-----------|------
# Bust   | Win   | Win   | Win   | Win   | Win   | Win   | Win       | Loss
# 17     | Loss  | Draw  | Win   | Win   | Win   | Win   | Win       | Loss
# 18     | Loss  | Loss  | Draw  | Win   | Win   | Win   | Win       | Loss
# 19     | Loss  | Loss  | Loss  | Draw  | Win   | Win   | Win       | Loss
# 20     | Loss  | Loss  | Loss  | Loss  | Draw  | Win   | Win       | Loss
# 21     | Loss  | Loss  | Loss  | Loss  | Loss  | Draw  | Win       | Loss
# Black- | Loss  | Loss  | Loss  | Loss  | Loss  | Loss  | Draw      | Loss
# jack   |       |       |       |       |       |       |           |

def calculate_hit_probabilities(dealer_hand_distribution, probabilities):
    """
    Berechnet die Gewinn-, Verlust- und Unentschieden-Wahrscheinlichkeiten für die Hit-Aktion.

    Args:
        dealer_hand_distribution (dict): Ein Dictionary mit den Wahrscheinlichkeiten für die möglichen Dealer-Hände.
        probabilities (dict): Ein Dictionary mit den Wahrscheinlichkeiten für die möglichen Spieler-Outcomes nach einem Hit.

    Returns:
        tuple: Ein Tupel (win_prob, loss_prob, draw_prob) mit den Wahrscheinlichkeiten für Gewinn, Verlust und Unentschieden.
    """
    win_prob, loss_prob, draw_prob = 0.0, 0.0, 0.0

    for dealer_outcome, dealer_prob in dealer_hand_distribution.items():
        for player_outcome, player_prob in probabilities.items():
            probability = dealer_prob * player_prob

            if player_outcome == 'Bust':
                loss_prob += probability
            elif dealer_outcome == 'Bust':
                win_prob += probability
            elif player_outcome == '<=16':
                loss_prob += probability
            elif player_outcome == 'Blackjack':
                if dealer_outcome == 'Blackjack':
                    draw_prob += probability
                else:
                    win_prob += probability
            elif dealer_outcome == 'Blackjack':
                loss_prob += probability
            else:  # Beide haben numerische Werte (17-21)
                dealer_value = int(dealer_outcome)
                player_value = int(player_outcome)
                if player_value > dealer_value:
                    win_prob += probability
                elif player_value < dealer_value:
                    loss_prob += probability
                else:
                    draw_prob += probability

    return win_prob, loss_prob, draw_prob

def calculate_stand_probabilities(total_value, is_blackjack, dealer_hand_distribution):
    """
    Berechnet die Gewinn-, Verlust- und Unentschieden-Wahrscheinlichkeiten für die Stand-Aktion.

    Args:
        total_value (int): Der Gesamtwert der Spielerhand.
        is_blackjack (bool): Gibt an, ob der Spieler ein Blackjack hat.
        dealer_hand_distribution (dict): Ein Dictionary mit den Wahrscheinlichkeiten für die möglichen Dealer-Hände.

    Returns:
        tuple: Ein Tupel (win_prob, loss_prob, draw_prob) mit den Wahrscheinlichkeiten für Gewinn, Verlust und Unentschieden.
    """
    win_prob, loss_prob, draw_prob = 0.0, 0.0, 0.0

    for dealer_outcome, dealer_prob in dealer_hand_distribution.items():
        if dealer_outcome == 'Bust':
            win_prob += dealer_prob
        elif is_blackjack:
            if dealer_outcome == 'Blackjack':
                draw_prob += dealer_prob
            else:
                win_prob += dealer_prob
        elif dealer_outcome == 'Blackjack':
            loss_prob += dealer_prob
        else:  # Beide haben numerische Werte
            dealer_value = int(dealer_outcome)
            if total_value > dealer_value:
                win_prob += dealer_prob
            elif total_value < dealer_value:
                loss_prob += dealer_prob
            else:
                draw_prob += dealer_prob

    return win_prob, loss_prob, draw_prob


