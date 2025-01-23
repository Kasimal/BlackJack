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
        self.create_table_hands()

    def create_table_hands(self):
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
                    is_blackjack BOOLEAN,
                    is_starthand BOOLEAN,
                    is_busted BOOLEAN,
                    can_double BOOLEAN,
                    can_split BOOLEAN,
                    bust_chance FLOAT,
                    frequency INTEGER,
                    UNIQUE ({", ".join(self.card_columns)})
                )
            ''')

    def create_table_dealer_hands(self, start_card):
        """
        Erstellt eine Tabelle für Dealer-Hände basierend auf der Startkarte.

        Args:
            start_card (int): Die Startkarte (1 bis 10), für die die Tabelle erstellt wird.
        """
        if not (1 <= start_card <= 10):
            raise ValueError("Startkarte muss zwischen 1 und 10 liegen.")

        table_name = f"dealer_hands_{start_card}"  # Dynamischer Tabellenname
        cursor = self.connection.cursor()
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                hand_text TEXT NOT NULL,
                result TEXT NOT NULL,
                frequency INTEGER NOT NULL
            )
        ''')
        self.connection.commit()
        print(f"Tabelle '{table_name}' wurde erstellt.")

    def inspect_table_columns(self, table_name):
        """Inspects the columns of a given table."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()

            print("Tabellenstruktur:")
            for col in columns:
                print(
                    f"Spalten-ID: {col[0]}, Name: {col[1]}, Typ: {col[2]}, Not Null: {col[3]}, Default: {col[4]}, Primary Key: {col[5]}")

    def drop_table(self, table_name):
        """
        Löscht die angegebene Tabelle aus der Datenbank, falls sie existiert.

        Args:
            table_name (str): Der Name der Tabelle, die gelöscht werden soll.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(f'''
                DROP TABLE IF EXISTS {table_name};
            ''')
            print(f"Tabelle '{table_name}' wurde gelöscht (falls sie existierte).")

    def save_hand(self, hand, total_value, minimum_value, is_blackjack, is_starthand, is_busted, can_double, can_split, bust_chance, frequency):
        """
        Speichert eine Hand in der Datenbank.
        Args:
            hand (list): Die aktuelle Hand als Liste der Kartenzahlen.
            total_value (int): Der Gesamtwert der Hand.
            minimum_value (int): Der Mindestwert der Hand.
            is_blackjack (bool): Ob die Hand ein Blackjack ist.
            is_starthand (bool): Ob die Hand eine Starthand ist.
            is_busted (bool): Ob die Hand über 21 ist.
            can_double (bool): Ob die Hand verdoppelt werden kann.
            can_split (bool): Ob die Hand gesplittet werden kann.
            bust_chance (float): Wahrscheinlichkeit mit der nächsten Karte zu überbieten
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
                #print(f"Columns: {len(self.card_columns) + 10}, Values: {len(card_counts + [hand_text, total_value, minimum_value, is_blackjack, is_starthand, is_busted, can_double, can_split, bust_chance, frequency])}")
                #print(f"Values: {card_counts + [hand_text, total_value, minimum_value, is_blackjack, is_starthand, is_busted, can_double, can_split, bust_chance, frequency]}")
                cursor.execute(f'''
                    INSERT INTO hands ({", ".join(self.card_columns)}, hand_text, total_value, minimum_value,
                                       is_blackjack, is_starthand, is_busted, can_double, can_split, bust_chance, frequency)
                    VALUES ({", ".join("?" for _ in range(len(self.card_columns) + 10))})
                ''', card_counts + [hand_text, total_value, minimum_value, is_blackjack, is_starthand, is_busted,
                                    can_double, can_split, bust_chance, frequency])

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

    def save_dealer_hand(self, hand, result):
        """
        Speichert die Dealer-Hand in der Datenbank.

        Args:
            hand (list): Die Karten in der Hand.
            result (str): Das Ergebnis der Hand (z. B. '17', '18', ..., '21', 'blackjack', 'bust').
        """
        hand_text = ",".join(map(str, hand))  # Hand als Text speichern
        cursor = self.connection.cursor()
        cursor.execute(f'''
            INSERT INTO dealer_hands (hand_text, result)
            VALUES (?, ?)
        ''', (hand_text, result))
        self.connection.commit()

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
