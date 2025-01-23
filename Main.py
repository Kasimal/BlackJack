from Models.Deck import Deck
from Application.Hands import Hands
from Application.db import DatabaseManager

def All_Hands_in_DB():
    # 1. Datenbank vorbereiten
    db_path = "Data/blackjack.db"
    db_manager = DatabaseManager(db_path)
    table_name = "Hands"
    db_manager.drop_table(table_name)
    db_manager.create_table_hands(table_name)
    db_manager.inspect_table_columns(table_name)

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

def Dealer_Hands_in_DB():
    # 1. Datenbank vorbereiten
    db_path = "Data/blackjack.db"
    db_manager = DatabaseManager(db_path)
    table_name = "Hands"
    db_manager.drop_table(table_name)
    db_manager.create_table_hands(table_name, dealer_hand=10)
    db_manager.inspect_table_columns(table_name)

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


if __name__ == "__main__":
    All_Hands_in_DB()

