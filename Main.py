from Models.Deck import Deck
from application.Hands import Hands
from application.db import DatabaseManager

def All_Hands_in_DB():
    # 1. Datenbank vorbereiten
    db_path = "Data/blackjack.db"
    db_manager = DatabaseManager(db_path)
    db_manager.drop_table()
    db_manager.create_table()

    # 2. Deck initialisieren
    deck_count = 1  # Anzahl der Decks
    deck = Deck(deck_count)  # Ein Deck

    # 3. Hands-Objekt erstellen
    hands_generator = Hands(deck,db_manager)

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

def count_3_card_hands():
    count = 0
    for card1 in range(1, 11):  # 1 repräsentiert Ass, 10 repräsentiert 10/J/Q/K
        for card2 in range(card1, 11):
            for card3 in range(card2, 11):
                if card1 + card2 + card3 <= 21:
                    count += 1
    return count

total_3_card_hands = count_3_card_hands()
print(f"Anzahl der nicht-busted Hände mit 3 Karten: {total_3_card_hands}")

if __name__ == "__main__":
    #All_Hands_in_DB()
    count_3_card_hands()

