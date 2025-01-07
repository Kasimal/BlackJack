import sqlite3

class DatabaseManager:
    """
    Verwalterklasse für die Speicherung und Verwaltung von Hand-Daten in einer SQL-Datenbank.
    """

    def __init__(self, db_filename):
        """
        Initialisiert die Datenbankverbindung und stellt sicher, dass die Tabelle existiert.

        Args:
            db_filename (str): Der Name der SQLite-Datenbankdatei.
        """
        self.db_filename = db_filename
        self._create_table()

    def _create_table(self):
        """
        Erstellt die Tabelle `hands` in der Datenbank, falls sie nicht existiert.
        """
        conn = sqlite3.connect(self.db_filename)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS hands (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                card_1 INTEGER DEFAULT 0,
                card_2 INTEGER DEFAULT 0,
                card_3 INTEGER DEFAULT 0,
                card_4 INTEGER DEFAULT 0,
                card_5 INTEGER DEFAULT 0,
                card_6 INTEGER DEFAULT 0,
                card_7 INTEGER DEFAULT 0,
                card_8 INTEGER DEFAULT 0,
                card_9 INTEGER DEFAULT 0,
                card_10 INTEGER DEFAULT 0,
                total_value INTEGER NOT NULL,
                minimum_value INTEGER NOT NULL,
                is_busted BOOLEAN NOT NULL,
                is_starthand BOOLEAN NOT NULL,
                can_double BOOLEAN NOT NULL,
                can_split BOOLEAN NOT NULL,
                frequency INTEGER NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    def save_hands(self, all_hands):
        """
        Speichert die generierten Hände in der Datenbank.

        Args:
            all_hands (list): Liste von Händen mit deren Details [(Hand, Wert)].
        """
        conn = sqlite3.connect(self.db_filename)
        cursor = conn.cursor()

        for hand, total_value in all_hands:
            # Kartenanzahl vorbereiten
            card_counts = {card: hand.count(card) for card in range(1, 11)}

            # Minimalen Wert berechnen
            minimum_value = hand.calculate_value(minimum=True)

            # Eigenschaften bestimmen
            is_busted = total_value > 21
            is_starthand = len(hand.cards) == 2
            can_double = is_starthand and total_value != 21
            can_split = is_starthand and hand.cards[0] == hand.cards[1]

            # Daten einfügen
            cursor.execute('''
                INSERT INTO hands (
                    card_1, card_2, card_3, card_4, card_5, card_6, card_7, card_8, card_9, card_10,
                    total_value, minimum_value, is_busted, is_starthand, can_double, can_split, frequency
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                card_counts[1], card_counts[2], card_counts[3], card_counts[4], card_counts[5],
                card_counts[6], card_counts[7], card_counts[8], card_counts[9], card_counts[10],
                total_value, minimum_value, is_busted, is_starthand, can_double, can_split, 1
            ))

        conn.commit()
        conn.close()

    def fetch_all_hands(self):
        """
        Ruft alle gespeicherten Hände aus der Datenbank ab.

        Returns:
            list: Eine Liste von Dictionaries mit den Daten der Hände.
        """
        conn = sqlite3.connect(self.db_filename)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM hands')
        rows = cursor.fetchall()
        conn.close()

        # Spaltennamen abrufen und Daten in ein Dictionary umwandeln
        columns = [
            "id", "card_1", "card_2", "card_3", "card_4", "card_5", "card_6",
            "card_7", "card_8", "card_9", "card_10", "total_value", "minimum_value",
            "is_busted", "is_starthand", "can_double", "can_split", "frequency"
        ]
        return [dict(zip(columns, row)) for row in rows]