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

        # Spalten für die Datenbank definieren (1-10)
        self.card_columns = [f"card_{i}" for i in range(1, 11)]

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
                is_starthand INTEGER,
                is_busted BOOLEAN,
                can_double BOOLEAN,
                can_split BOOLEAN,
                frequency INTEGER,
                UNIQUE (card_1, card_2, card_3, card_4, card_5, card_6, card_7, card_8, card_9, card_10)
            )
        ''')
        self.connection.commit()

    def save_hand(self, hand, deck, previous_frequency):
        """
        Speichert die gegebene Hand in der Datenbank oder aktualisiert deren Häufigkeit,
        falls sie bereits existiert.

        Args:
            hand (Hand): Die Hand, die gespeichert werden soll.
            deck (Deck): Das aktuelle Deck.
            previous_frequency (float): Die Häufigkeit der Vorgängerhand.
        """
        # Berechne die Häufigkeit der aktuellen Hand
        frequency = hand.calculate_frequency(deck, previous_frequency)

        # Baue die Datenbankzeile für die Hand
        db_row = hand.to_db_row(frequency)

        # Überprüfen, ob die Hand bereits existiert
        cursor = self.connection.cursor()
        cursor.execute('''
            SELECT frequency FROM hands 
            WHERE ''' + ' AND '.join(f"{col} = ?" for col in self.card_columns) + '''
        ''', db_row[:10])  # Vergleich nur der Kartenanzahlen
        result = cursor.fetchone()

        if result:
            current_frequency = result[0]
            new_frequency = current_frequency + frequency
            cursor.execute('''
                UPDATE hands
                SET frequency = ?
                WHERE ''' + ' AND '.join(f"{col} = ?" for col in self.card_columns) + '''
            ''', [new_frequency] + list(db_row[:10]))
        else:
            cursor.execute('''
                INSERT INTO hands (''' + ', '.join(self.card_columns + [
                "total_value", "minimum_value",
                "is_starthand", "is_busted",
                "can_double", "can_split", "frequency"
            ]) + ''')
                VALUES (''' + ', '.join(['?'] * len(db_row)) + ''')
            ''', db_row)

        self.connection.commit()

    def save_hands(self, hands, deck):
        """
        Speichert eine Liste von Händen in der Datenbank.

        Args:
            hands (list of Hand): Eine Liste von Hand-Objekten.
            deck (Deck): Das aktuelle Deck.
        """
        for hand in hands:
            self.save_hand(hand, deck)

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
