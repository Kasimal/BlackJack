from Models.Deck import Deck
from Models.Hands import Hands
from Models.Dealer_hands import DealerHands
from Utility.Calculations import probability_distribution
from Utility.DB import DatabaseManager


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
    db_manager.inspect_table_columns("Full_player_hands")
    deck = Deck()  # Ein Deck
    hands_generator = Hands(deck, db_manager)
    hands_generator.generate_and_save_full_player_hands()
    db_manager.close()

def Full_Hands():
    db_path = "Data/blackjack.db"
    db_manager = DatabaseManager(db_path)
    db_manager.create_table_full_player_hands()
    deck = Deck()
    hands_generator = Hands(deck, db_manager)
    hands_generator.generate_and_save_full_player_hands()
    db_manager.close()


if __name__ == "__main__":
    #All_Hands_in_DB()
    #All_Hands_in_DB(missing_cards=[1, 1, 1])
    #Dealer_Hands_in_DB()
    #Dealer_Hands_in_DB(missing_cards=[1, 1, 1])
    #Dealer_Hands_statistics_from_DB()
    Full_Hands()

    # hand = [1, 1, 5]  # Hand auszuwerten
    # probabilities = probability_distribution(hand)
    # for key, value in probabilities.items():
    #     print(f"{key}: {value:.2%}")
