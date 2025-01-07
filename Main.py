
from Models.Deck import Deck
from Models.Hand import Hand
from application.Hands import Hands
from application.db import DatabaseManager


def Game():
    print("Willkommen zu Blackjack!")
    deck = Deck(deck_count=1)
    hand = Hand()

    # Initiale Hand
    hand.draw_random_card_from_deck(deck)
    hand.draw_random_card_from_deck(deck)
    print("Ihre Starthand:")
    print(hand)

    def display_probabilities():
        reach, exceed = hand.probability_to_reach_or_exceed(deck)
        print(f"Eine weitere Karte nehmen, ohne Überbieten zu Überbieten: {reach:.2%} zu {exceed:.2%}")

    display_probabilities()

    # Spieler entscheidet, ob weitere Karten gezogen werden sollen
    while True:
        if hand.calculate_value() > 21:
            print("Sie haben verloren! Ihre Hand hat einen Wert von mehr als 21.")
            break

        choice = input("Möchten Sie eine weitere Karte ziehen? (j/n): ").lower()
        if choice == 'j':
            hand.draw_random_card_from_deck(deck)
            print("Ihre aktuelle Hand:")
            print(hand)
            display_probabilities()
        elif choice == 'n':
            print("Spiel beendet. Ihre finale Hand:")
            print(hand)
            if hand.calculate_value() <= 21:
                print("Sie haben gewonnen! 🎉")
            break
        else:
            print("Ungültige Eingabe. Bitte 'j' oder 'n' eingeben.")

def Hands_in_DB():
    # Erstelle ein Hand-Objekt
    hand1 = Hand([1, 1])  # Zwei Asse
    hand2 = Hand([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])  # von jedem eins

    # Initialisiere den DatabaseManager
    db_manager = DatabaseManager()

    # Speichere einzelne Hände
    db_manager.save_hand(hand1)
    db_manager.save_hand(hand2)

    # Speichere mehrere Hände
    hands = [Hand([7, 7, 7]), Hand([10, 10]), Hand([2, 3, 6])]
    db_manager.save_hands(hands)

    # Abrufen der gespeicherten Hände
    for row in db_manager.fetch_all_hands():
        print(row)

    # Schließe die Verbindung zur Datenbank
    db_manager.close()

if __name__ == "__main__":
    #Game()
    Hands_in_DB()

