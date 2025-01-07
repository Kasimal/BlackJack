from Deck import Deck
from Hand import Hand
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
    # Hands generieren
    deck = Deck(deck_count=1)
    hands = Hands(deck)
    hands.generate_all_hands()

    # Hände in die Datenbank speichern
    db_manager = DatabaseManager("BlackjackDB.db")
    db_manager.save_hands(hands.all_hands)

    # Alle Hände aus der Datenbank abrufen und anzeigen
    all_hands_from_db = db_manager.fetch_all_hands()
    for hand in all_hands_from_db:
        print(hand)

if __name__ == "__main__":
    #Game()
    Hands_in_DB()

