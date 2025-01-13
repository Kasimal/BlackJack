from Models.Deck import Deck
from application.Hands import Hands
from application.db import DatabaseManager


# def Game():
#     print("Willkommen zu Blackjack!")
#     deck = Deck(deck_count=1)
#     hand = Hand()
#
#     # Initiale Hand
#     hand.draw_random_card_from_deck(deck)
#     hand.draw_random_card_from_deck(deck)
#     print("Ihre Starthand:")
#     print(hand)
#
#     def display_probabilities():
#         reach, exceed = hand.probability_to_reach_or_exceed(deck)
#         print(f"Eine weitere Karte nehmen, ohne Überbieten zu Überbieten: {reach:.2%} zu {exceed:.2%}")
#
#     display_probabilities()
#
#     # Spieler entscheidet, ob weitere Karten gezogen werden sollen
#     while True:
#         if hand.calculate_value() > 21:
#             print("Sie haben verloren! Ihre Hand hat einen Wert von mehr als 21.")
#             break
#
#         choice = input("Möchten Sie eine weitere Karte ziehen? (j/n): ").lower()
#         if choice == 'j':
#             hand.draw_random_card_from_deck(deck)
#             print("Ihre aktuelle Hand:")
#             print(hand)
#             display_probabilities()
#         elif choice == 'n':
#             print("Spiel beendet. Ihre finale Hand:")
#             print(hand)
#             if hand.calculate_value() <= 21:
#                 print("Sie haben gewonnen! 🎉")
#             break
#         else:
#             print("Ungültige Eingabe. Bitte 'j' oder 'n' eingeben.")
#
# def Hands_in_DB():
#     deck = Deck(deck_count=1)
#     hand1 = Hand([1, 1, 10])  # Zwei Asse und eine 10
#     hand2 = Hand([5, 5])  # Zwei Fünfen
#     hand3 = Hand([1, 1, 10])  # Dieselbe Hand wie hand1
#
#     hands = [Hand([1, 10]), Hand([1,9]), Hand([9,1]), Hand([2,3]), Hand([4]), Hand([10]) ]
#     # Initialisiere den DatabaseManager
#     db_manager = DatabaseManager()
#
#     # Speichere die Hände
#     db_manager.save_hand(hand1, deck)
#     db_manager.save_hand(hand2, deck)
#     db_manager.save_hand(hand3, deck)  # Diese Hand erhöht die Häufigkeit von hand1
#     db_manager.save_hands(hands, deck)
#
#     # Abrufen der gespeicherten Hände
#     for row in db_manager.fetch_all_hands():
#         print(row)
#
#     # Schließe die Verbindung zur Datenbank
#     db_manager.close()

def All_Hands_in_DB():
    # 1. Datenbank vorbereiten
    db_path = "Data/blackjack.db"
    db_manager = DatabaseManager(db_path)
    db_manager.create_table()

    # 2. Deck initialisieren
    deck_count = 1  # Anzahl der Decks

    # 3. Hands-Objekt erstellen
    hands_generator = Hands(deck_count)

    # 4. Hände generieren und speichern
    print("Generiere und speichere alle möglichen Hände...")
    hands_generator.generate_and_save_hands()
    print("Alle Hände wurden erfolgreich generiert und gespeichert!")

    # 5. Statusbericht
    print("Anzahl gespeicherter Hände:")
    with db_manager.connection:
        cursor = db_manager.connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM hands")
        count = cursor.fetchone()[0]
        print(f"{count} Hände sind in der Datenbank gespeichert.")


if __name__ == "__main__":
    #Game()
    #Hands_in_DB()
    All_Hands_in_DB()

