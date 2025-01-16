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
                    hand_text VARCHAR,
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

    def drop_table(self):
        """
        Löscht die Tabelle 'hands' aus der Datenbank, falls sie existiert.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                DROP TABLE IF EXISTS hands;
            ''')

    # def save_hand(self, hand, total_value, minimum_value, is_starthand, is_busted, can_double, can_split, frequency):
    #     """
    #     Speichert eine Hand in der Datenbank.
    #     """
    #     card_counts = [hand.count(card) for card in range(1, 11)]  # Zähle jede Karte in der Hand
    #     hand_text = ",".join(map(str, hand))  # Wandelt die Hand in einen Textstring um
    #     with self.connection as conn:
    #         cursor = conn.cursor()
    #         # Prüfen, ob die Hand bereits existiert
    #         cursor.execute(f'''
    #             SELECT frequency FROM hands WHERE {self._generate_where_clause(card_counts)}
    #         ''', card_counts)
    #         result = cursor.fetchone()
    #
    #         if result:
    #             # Häufigkeit aktualisieren, wenn Hand existiert
    #             new_frequency = result[0] + frequency
    #             cursor.execute(f'''
    #                 UPDATE hands
    #                 SET frequency = ?
    #                 WHERE {self._generate_where_clause(card_counts)}
    #             ''', [new_frequency] + card_counts)
    #         else:
    #             # Neue Hand einfügen
    #             cursor.execute(f'''
    #                 INSERT INTO hands ({", ".join(self.card_columns)}, hand_text, total_value, minimum_value,
    #                                    is_starthand, is_busted, can_double, can_split, frequency)
    #                 VALUES ({", ".join("?" for _ in range(len(self.card_columns) + 7))})
    #             ''', card_counts + [hand_text, total_value, minimum_value, is_starthand, is_busted, can_double, can_split,
    #                                 frequency])

    def save_hand(self, hand, total_value, minimum_value, is_starthand, is_busted, can_double, can_split, frequency):
        """
        Speichert eine Hand in der Datenbank.
        Args:
            hand (list): Die aktuelle Hand als Liste der Kartenzahlen.
            total_value (int): Der Gesamtwert der Hand.
            minimum_value (int): Der Mindestwert der Hand.
            is_starthand (bool): Ob die Hand eine Starthand ist.
            is_busted (bool): Ob die Hand über 21 ist.
            can_double (bool): Ob die Hand verdoppelt werden kann.
            can_split (bool): Ob die Hand gesplittet werden kann.
            frequency (int): Die Häufigkeit der Hand.
        """
        card_counts = [hand.count(card) for card in range(1, 11)]  # Zähle jede Karte in der Hand
        hand_text = ",".join(map(str, hand))  # Wandelt die Hand in einen Textstring um

        with self.connection as conn:
            cursor = conn.cursor()

            # Prüfen, ob die Hand bereits existiert
            cursor.execute(f'''
                SELECT frequency FROM hands WHERE {self._generate_where_clause(card_counts)}
            ''', card_counts)
            result = cursor.fetchone()

            if result:
                # Häufigkeit aktualisieren, wenn Hand existiert
                new_frequency = result[0] + frequency
                cursor.execute(f'''
                    UPDATE hands
                    SET frequency = ?
                    WHERE {self._generate_where_clause(card_counts)}
                ''', [new_frequency] + card_counts)
            else:
                # Neue Hand einfügen
                cursor.execute(f'''
                    INSERT INTO hands ({", ".join(self.card_columns)}, hand_text, total_value, minimum_value,
                                       is_starthand, is_busted, can_double, can_split, frequency)
                    VALUES ({", ".join("?" for _ in range(len(self.card_columns) + 8))})
                ''', card_counts + [hand_text, total_value, minimum_value, is_starthand, is_busted, can_double,
                                    can_split, frequency])

    def _generate_where_clause(self, card_counts):
        """
        Generiert eine WHERE-Bedingung für die Kartenzählungen.

        Args:
            card_counts (list): Eine Liste mit der Anzahl der Karten (1 bis 10).

        Returns:
            str: Die generierte WHERE-Bedingung.
        """
        conditions = []
        for i, count in enumerate(card_counts):
            conditions.append(f"c{i + 1} = ?")
        return " AND ".join(conditions)

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
