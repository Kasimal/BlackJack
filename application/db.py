import sqlite3

class DatabaseManager:
    def __init__(self, db_path="Data/Blackjack.db"):
        """
        Initialisiert den Datenbank-Manager mit einer Verbindung zur angegebenen SQLite-Datenbank.

        Args:
            db_path (str): Pfad zur SQLite-Datenbankdatei.
        """
        self.db_path = db_path
        self.card_columns = [f"c{i}" for i in range(1, 11)]
        self.connection = sqlite3.connect(self.db_path)
        self.create_table()

    def create_table(self):
        """
        Erstellt die Tabelle für Blackjack-Hände, falls sie nicht bereits existiert.
        """
        with self.connection as conn:
            conn.execute(f'''
                CREATE TABLE IF NOT EXISTS hands (
                    {", ".join(f"{col} INTEGER" for col in self.card_columns)},
                    total_value INTEGER,
                    minimum_value INTEGER,
                    is_starthand BOOLEAN,
                    is_busted BOOLEAN,
                    can_double BOOLEAN,
                    can_split BOOLEAN,
                    frequency INTEGER,
                    UNIQUE ({", ".join(self.card_columns)})
                )
            ''')

    def save_hand(self, deck, total_value, minimum_value, is_starthand, is_busted, can_double, can_split, frequency):
        """
        Speichert eine Hand in die Datenbank oder erhöht die Häufigkeit, falls sie bereits existiert.
        """
        card_counts = deck.get_card_counts()

        # Verbindung zur Datenbank herstellen
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Überprüfe, ob die Hand bereits existiert
            cursor.execute(f'''
                SELECT frequency FROM hands
                WHERE {" AND ".join(f"{col} = ?" for col in self.card_columns)}
            ''', card_counts)

            result = cursor.fetchone()

            if result:
                # Hand existiert bereits -> Häufigkeit erhöhen
                current_frequency = result[0]
                new_frequency = current_frequency + frequency
                cursor.execute(f'''
                    UPDATE hands
                    SET frequency = ?
                    WHERE {" AND ".join(f"{col} = ?" for col in self.card_columns)}
                ''', [new_frequency] + card_counts)
            else:
                # Hand existiert noch nicht -> Einfügen
                cursor.execute(f'''
                    INSERT INTO hands ({", ".join(self.card_columns)}, total_value, minimum_value,
                                       is_starthand, is_busted, can_double, can_split, frequency)
                    VALUES ({", ".join("?" for _ in range(len(self.card_columns) + 7))})
                ''', card_counts + [total_value, minimum_value, int(is_starthand), int(is_busted), int(can_double),
                                    int(can_split), frequency])

    def fetch_all_hands(self):
        """
        Ruft alle gespeicherten Hände aus der Datenbank ab.

        Returns:
            list: Eine Liste von Tupeln, die alle Hände und deren Eigenschaften repräsentieren.
        """
        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM hands')
            return cursor.fetchall()

    def close(self):
        """
        Schließt die Verbindung zur Datenbank.
        """
        self.connection.close()
