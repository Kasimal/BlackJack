import sqlite3
import os
from Models.Hand import Hand


class DatabaseManager:
    def __init__(self, db_name="Blackjack.db"):
        """
        Initialisiert den DatabaseManager mit einer SQLite-Datenbank im Ordner 'Data'.

        Args:
            db_name (str): Der Name der SQLite-Datenbankdatei (standardmäßig 'Blackjack.db').
        """
        # Sicherstellen, dass der Ordner 'Data' existiert
        self.data_dir = "Data"
        os.makedirs(self.data_dir, exist_ok=True)

        # Pfad zur Datenbankdatei
        self.db_path = os.path.join(self.data_dir, db_name)
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()

        # Tabelle erstellen, falls sie nicht existiert
        self.create_table()

    def create_table(self):
        """
        Erstellt die Tabelle für Hände in der Datenbank, falls sie noch nicht existiert.
        """
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS hands (
                card_1 INTEGER,
                card_2 INTEGER,
                card_3 INTEGER,
                card_4 INTEGER,
                card_5 INTEGER,
                card_6 INTEGER,
                card_7 INTEGER,
                card_8 INTEGER,
                card_9 INTEGER,
                card_10 INTEGER,
                total_value INTEGER,
                minimum_value INTEGER,
                is_busted BOOLEAN,
                is_starthand BOOLEAN,
                can_double BOOLEAN,
                can_split BOOLEAN,
                frequency INTEGER
            )
        ''')
        self.connection.commit()

    def save_hand(self, hand):
        """
        Speichert eine Hand in der Datenbank.

        Args:
            hand (Hand): Die Hand, die gespeichert werden soll.
        """
        db_row = hand.to_db_row()
        self.cursor.execute('''
            INSERT INTO hands (
                card_1, card_2, card_3, card_4, card_5, card_6, card_7, card_8, card_9, card_10,
                total_value, minimum_value, is_busted, is_starthand, can_double, can_split, frequency
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', db_row)
        self.connection.commit()

    def save_hands(self, hands):
        """
        Speichert eine Liste von Händen in der Datenbank.

        Args:
            hands (list of Hand): Eine Liste von Hand-Objekten.
        """
        for hand in hands:
            self.save_hand(hand)

    def fetch_all_hands(self):
        """
        Ruft alle Hände aus der Datenbank ab.

        Returns:
            list: Eine Liste von Tupeln, die die gespeicherten Hände repräsentieren.
        """
        self.cursor.execute('SELECT * FROM hands')
        return self.cursor.fetchall()

    def close(self):
        """
        Schließt die Verbindung zur Datenbank.
        """
        self.connection.close()
