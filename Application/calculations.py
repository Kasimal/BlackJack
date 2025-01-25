def calculate_hand_frequency_with_order(current_hand, original_frequencies):
    """
    Berechnet die Häufigkeit einer Hand, wobei die Reihenfolge der Karten berücksichtigt wird.

    Args:
        current_hand (list): Die aktuelle Hand (z. B. [1, 5, 10]).
        original_frequencies (dict): Die originalen Häufigkeiten der Karten im Deck
                                     (z. B. {1: 4, 2: 4, ..., 10: 16}).

    Returns:
        int: Die Häufigkeit der Hand unter Berücksichtigung der Reihenfolge.
    """
    # Wenn die Hand leer ist, gibt es keine Frequenz
    if not current_hand:
        return 0

    # Startwert für die Häufigkeit
    frequency = 1

    # Kopie der Frequenzen erstellen, damit sie nicht verändert wird
    available_frequencies = original_frequencies.copy()

    # Iteriere über die Karten in der aktuellen Hand in der Reihenfolge
    for card in current_hand:
        # Prüfe, ob die Karte noch verfügbar ist
        if available_frequencies[card] <= 0:
            return 0  # Wenn die Karte nicht verfügbar ist, ist die Häufigkeit 0

        # Multipliziere die Häufigkeit mit der Verfügbarkeit der Karte
        frequency *= available_frequencies[card]

        # Reduziere die Verfügbarkeit der Karte um 1
        available_frequencies[card] -= 1

    return frequency