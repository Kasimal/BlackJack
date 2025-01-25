from Models.Deck import Deck
from Application.Hands import Hands
from Application.db import DatabaseManager
from Application.DealerHands import DealerHands

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
    db_manager.print_hand_count(table_name)

def Dealer_Hands_in_DB():
    # 1. Datenbank vorbereiten
    db_path = "Data/blackjack.db"
    db_manager = DatabaseManager(db_path)
    table_name = "Dealer_Hands"
    db_manager.drop_table(table_name)
    db_manager.create_table_hands(table_name, dealer_hand=True)

    # 2. Deck initialisieren
    deck_count = 1  # Anzahl der Decks
    deck = Deck(deck_count)  # Ein Deck

    # 3. Dealer_Hands-Objekt erstellen
    hands_generator = DealerHands(deck, db_manager)

    # 4. Dealer-Hände generieren und speichern
    hands_generator.generate_dealer_hands(table_name, start_card=10)

    # 5. Dealer-Hände analysieren
    #hands_generator.analyze_dealer_hands()

    # 6. Statusbericht
    db_manager.print_hand_count(table_name)


if __name__ == "__main__":
    Dealer_Hands_in_DB()

