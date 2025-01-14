from Models.Deck import Deck
from application.Hands import Hands
from application.db import DatabaseManager

def All_Hands_in_DB():
    # 1. Datenbank vorbereiten
    db_path = "Data/blackjack.db"
    db_manager = DatabaseManager(db_path)
    db_manager.create_table()

    # 2. Deck initialisieren
    deck_count = 1  # Anzahl der Decks
    deck = Deck(deck_count)  # Ein Deck
    missing_cards_ass_2 = [1, 2]  # Ass und 2
    missing_cards_ass_ass = [1, 1]  # Zwei Asse
    missing_cards_10_10_10 = [10, 10, 10]  # 3 Zehnen
    missing_cards_10_10_10 = [10, 10, 10]  # 3 Zehnen

    frequency_ass_2 = deck.calculate_hand_frequency(missing_cards_ass_2)
    frequency_ass_ass = deck.calculate_hand_frequency(missing_cards_ass_ass)
    frequency_10_10_10 = deck.calculate_hand_frequency(missing_cards_10_10_10)

    print(f"Häufigkeit von Ass 2: {frequency_ass_2}")  # Erwartet: 16
    print(f"Häufigkeit von Ass Ass: {frequency_ass_ass}")  # Erwartet: 6
    print(f"Häufigkeit von 10 10 10: {frequency_10_10_10}")  # Erwartet: 560


    # 3. Hands-Objekt erstellen
    hands_generator = Hands(deck,db_manager)

    # 4. Hände generieren und speichern
    print("Generiere und speichere alle möglichen Hände...")
    hands_generator.generate_and_save_hands(max_cards=3)
    print("Alle Hände wurden erfolgreich generiert und gespeichert!")

    # 5. Statusbericht
    print("Anzahl gespeicherter Hände:")
    with db_manager.connection:
        cursor = db_manager.connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM hands")
        count = cursor.fetchone()[0]
        print(f"{count} Hände sind in der Datenbank gespeichert.")


if __name__ == "__main__":
    All_Hands_in_DB()

