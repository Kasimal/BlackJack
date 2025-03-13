import time
from Models.Deck import Deck
from Models.Hands import Hands
from Models.Dealer_hands import DealerHands
from Utility.DB import DatabaseManager
import Utility.Calculations as calc


def All_Hands_in_DB(missing_cards=None):
    # 1. Datenbank vorbereiten
    db_path = "Data/blackjack.db"
    db_manager = DatabaseManager(db_path)
    table_name = "Hands"
    db_manager.drop_table(table_name)
    db_manager.create_table_hands(table_name)
    db_manager.inspect_table_columns(table_name)

    # 2. Deck initialisieren
    deck = Deck()  # Ein Deck

    # 3. Hands-Objekt erstellen
    hands_generator = Hands(deck, db_manager)

    # 4. Hände generieren und speichern
    print("Generiere und speichere alle möglichen Hände...")
    hands_generator.generate_and_save_hands(missing_cards)
    print("Alle Hände wurden erfolgreich generiert und gespeichert!")

    # 5. Statusbericht
    db_manager.print_hand_count(table_name)

    # 6. DB schließen
    db_manager.close()

def Dealer_Hands_in_DB(missing_cards=None):
    # 1. Datenbank vorbereiten
    db_path = "Data/blackjack.db"
    db_manager = DatabaseManager(db_path)
    table_name = "Dealer_Hands"
    db_manager.drop_table(table_name)
    db_manager.create_table_hands(table_name)

    # 2. Deck initialisieren
    deck = Deck()  # Ein Deck

    # 3. Dealer_Hands-Objekt erstellen
    hands_generator = DealerHands(deck, db_manager)

    # 4. Dealer-Hände generieren und speichern
    hands_generator.generate_dealer_hands(table_name, missing_cards)

    # 6. Statusbericht
    db_manager.print_hand_count(table_name)

    # 7. Dealerhände auswerten
    stats = db_manager.get_dealer_hand_statistics()
    for row in stats:
        print(row)  # (start_card, count_17, count_18, count_19, count_20, count_21, count_blackjack, count_busted)

    # 8. DB schließen
    db_manager.close()

def Dealer_Hands_statistics_from_DB():
    db_path = "Data/blackjack.db"
    db_manager = DatabaseManager(db_path)
    db_manager.update_dealer_hand_statistics()

def Full_Hands():
    db_path = "Data/blackjack.db"
    db_manager = DatabaseManager(db_path)
    table_name = "Full_player_hands"
    db_manager.drop_table(table_name)
    db_manager.create_table_full_player_hands(table_name)
    db_manager.inspect_table_columns(table_name)
    deck = Deck()
    hands_generator = Hands(deck, db_manager)
    start_time = time.time()  # Timer starten
    hands_generator.generate_and_save_full_player_hands()
    end_time = time.time()  # Timer stoppen
    print(f"Generierung der Dealer-Hände dauerte: {end_time - start_time:.4f} Sekunden")
    db_manager.close()

def EVs():
    db_path = "Data/blackjack.db"
    db_manager = DatabaseManager(db_path)
    table_name = "Full_player_hands"
    db_manager.calculate_ev_for_hands(table_name)

def Strategy_Overview():
    db_path = "Data/blackjack.db"
    db_manager = DatabaseManager(db_path)
    table_name = "Full_player_hands"
    db_manager.create_player_dealer_startcard_overview(table_name)
    db_manager.create_player_dealer_strategy_table()
    db_manager.create_player_dealer_strategy_table_soft()
    db_manager.close()


if __name__ == "__main__":
    #All_Hands_in_DB()
    #All_Hands_in_DB(missing_cards=[1, 1, 1])
    #Dealer_Hands_in_DB()
    #Dealer_Hands_in_DB(missing_cards=[1, 1, 1])
    #Dealer_Hands_statistics_from_DB()
    #Full_Hands()
    #EVs()
    #Strategy_Overview()
    # Gültige Werte
    probabilities = calc.card_draw_probabilities([10, 5], 7)  # Int direkt
    print(f"Berechnete Wahrscheinlichkeiten: {probabilities}")
    probabilities = calc.card_draw_probabilities([2, 3], "9")  # String-Konvertierung
    print(f"Berechnete Wahrscheinlichkeiten: {probabilities}")

    # Löst Fehler aus
    #calc.card_draw_probabilities([], "Blackjack")  # Konvertierung fehlgeschlagen
    #calc.card_draw_probabilities([], 12)  # Außerhalb 1-10

