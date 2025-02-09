import sqlite3
from Models.Deck import Deck

class DatabaseManager:
    def __init__(self, db_path="Data/Blackjack.db"):
        """
        Initialisiert den Datenbank-Manager mit einer Verbindung zur angegebenen SQLite-Datenbank.

        Args:
            db_path (str): Pfad zur SQLite-Datenbankdatei.
        """
        self.deck = Deck()
        self.db_path = db_path
        self.card_columns = [f"c{card}" for card in self.deck.get_available_cards()]
        self.connection = sqlite3.connect(self.db_path)
        self._create_stats_table()

    def create_table_hands(self, table_name):
        """
        Erstellt eine einheitliche Tabelle für Blackjack-Hände, die sowohl Spieler- als auch Dealerhände abdecken kann.

        Args:
            table_name (str): Name der Tabelle.
        """
        with self.connection as conn:
            cursor = conn.cursor()

            # SQL für einheitliche Hände-Tabelle
            sql = f'''
                CREATE TABLE IF NOT EXISTS {table_name} (
                    hand_id INTEGER PRIMARY KEY AUTOINCREMENT,-- Eindeutige ID
                    hand_type TEXT NOT NULL,                  -- Typ der Hand: 'player' oder 'dealer'
                    start_card INTEGER,                       -- Startkarte der Hand
                    {", ".join(f"{col} INTEGER" for col in self.card_columns)},
                    hand_text VARCHAR UNIQUE,                 -- Textuelle Darstellung der Hand
                    total_value INTEGER,                      -- Gesamtwert der Hand
                    minimum_value INTEGER,                    -- Minimalwert der Hand
                    is_blackjack BOOLEAN,                     -- Ob die Hand ein Blackjack ist
                    is_starthand BOOLEAN,                     -- Ob die Hand eine Starthand ist
                    is_busted BOOLEAN,                        -- Ob die Hand über 21 liegt
                    can_double BOOLEAN DEFAULT 0,             -- Ob die Hand verdoppelt werden kann (immer False für Dealer)
                    can_split BOOLEAN DEFAULT 0,              -- Ob die Hand gesplittet werden kann (immer False für Dealer)
                    bust_chance FLOAT,                        -- Wahrscheinlichkeit, die Hand zu überbieten
                    frequency INTEGER,                        -- Häufigkeit der Hand
                    probability FLOAT                         -- relative Wahrscheinlichleit der Hand
                )
            '''
            print(f"Einheitliche Hände-Tabelle '{table_name}' wird erstellt.")

            # Ausführung der SQL-Anweisung
            cursor.execute(sql)
            print(f"Tabelle '{table_name}' wurde erfolgreich erstellt.")

    def _create_stats_table(self):
        """Erstellt die Tabelle für die Dealerhand-Statistiken mit relativen Häufigkeiten, falls sie nicht existiert."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS dealer_hand_stats (
                start_card TEXT PRIMARY KEY,
                count_17 REAL DEFAULT 0,
                count_18 REAL DEFAULT 0,
                count_19 REAL DEFAULT 0,
                count_20 REAL DEFAULT 0,
                count_21 REAL DEFAULT 0,
                count_blackjack REAL DEFAULT 0,
                count_busted REAL DEFAULT 0
            )
        """)
        conn.commit()
        conn.close()

    def update_dealer_hand_statistics(self):
        """Berechnet die relativen Häufigkeiten der Dealerhände nach Startkarte."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Basis-Query zur Berechnung der absoluten Häufigkeiten
        query = "SELECT start_card,\n"

        for value in range(17, 21):
            query += f"    SUM(CASE WHEN total_value = {value} THEN probability ELSE 0 END) AS count_{value},\n"

        query += """
            SUM(CASE WHEN total_value = 21 AND NOT is_blackjack THEN probability ELSE 0 END) AS count_21,
            SUM(CASE WHEN is_blackjack THEN probability ELSE 0 END) AS count_blackjack,
            SUM(CASE WHEN is_busted THEN probability ELSE 0 END) AS count_busted,
            SUM(probability) AS total_hands
        FROM dealer_hands
        GROUP BY start_card
        ORDER BY start_card;
        """

        cursor.execute(query)
        results = cursor.fetchall()

        # Tabelle leeren, um alte Werte zu überschreiben
        cursor.execute("DELETE FROM dealer_hand_stats")

        # Ergebnisse mit relativen Häufigkeiten speichern
        for row in results:
            start_card, count_17, count_18, count_19, count_20, count_21, count_blackjack, count_busted, total_hands = row

            # Berechnung der relativen Häufigkeiten (0 falls total_hands = 0)
            relative_values = [
                start_card,
                count_17 / total_hands if total_hands else 0,
                count_18 / total_hands if total_hands else 0,
                count_19 / total_hands if total_hands else 0,
                count_20 / total_hands if total_hands else 0,
                count_21 / total_hands if total_hands else 0,
                count_blackjack / total_hands if total_hands else 0,
                count_busted / total_hands if total_hands else 0
            ]

            cursor.execute("""
                INSERT INTO dealer_hand_stats (start_card, count_17, count_18, count_19, count_20, count_21, count_blackjack, count_busted)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, relative_values)

        conn.commit()
        conn.close()

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

    def save_hand(self, table_name, hand_data):
        """
        Speichert eine einzelne Hand in der angegebenen Tabelle.

        Args:
            table_name (str): Name der Tabelle.
            hand_data (dict): Ein Dictionary mit den Attributen der Hand.
        """
        # Spalten definieren
        columns = ["hand_type", "start_card"] + [f"c{i}" for i in range(1, 11)] + [
            "hand_text", "total_value", "minimum_value",
            "is_blackjack", "is_starthand", "is_busted",
            "can_double", "can_split", "bust_chance", "frequency", "probability"
        ]

        # SQL-Anweisung vorbereiten
        placeholders = ", ".join(["?"] * len(columns))
        sql = f'''
            INSERT INTO {table_name} ({", ".join(columns)})
            VALUES ({placeholders})
        '''

        # Werte vorbereiten
        hand_text = ",".join(map(str, hand_data["hand"]))
        card_frequencies = [hand_data["hand"].count(i) for i in range(1, 11)]

        values = [
            hand_data["hands_type"],
            hand_data["start_card"] if hand_data["hands_type"] == "dealer" else None,
            *card_frequencies,
            hand_text,
            hand_data["total_value"],
            hand_data["minimum_value"],
            hand_data["is_blackjack"],
            hand_data["is_starthand"],
            hand_data["is_busted"],
            hand_data["can_double"],
            hand_data["can_split"],
            hand_data["bust_chance"],
            hand_data["frequency"],
            hand_data["probability"]
        ]

        # Datenbank-Insert
        try:
            with self.connection as conn:
                conn.execute(sql, values)  # Einzelne Hand einfügen
            print("Hand erfolgreich gespeichert.")
        except sqlite3.IntegrityError as e:
            print(f"Fehler beim Speichern der Hand: {e}")

    def save_hands(self, table_name, hands):
        """
        Speichert mehrere Hände auf einmal in der angegebenen Tabelle (Batch-Insert).

        Args:
            table_name (str): Name der Tabelle.
            hands (list of dict): Eine Liste von Händen mit ihren Attributen.
        """
        if not hands:
            return  # Falls keine Hände übergeben wurden, nichts tun

        # Spalten definieren
        columns = ["hand_type", "start_card"] + [f"c{i}" for i in range(1, 11)] + [
            "hand_text", "total_value", "minimum_value",
            "is_blackjack", "is_starthand", "is_busted",
            "can_double", "can_split", "bust_chance", "frequency", "probability"
        ]

        # SQL-Anweisung vorbereiten
        placeholders = ", ".join(["?"] * len(columns))
        sql = f'''
            INSERT INTO {table_name} ({", ".join(columns)})
            VALUES ({placeholders})
        '''

        # Werte für Batch-Insert vorbereiten
        values = []
        for hand_data in hands:
            hand_text = ",".join(map(str, hand_data["hand"]))
            card_frequencies = [hand_data["hand"].count(i) for i in range(1, 11)]

            values.append([
                hand_data["hands_type"],
                hand_data["start_card"] if hand_data["hands_type"] == "dealer" else None,
                *card_frequencies,
                hand_text,
                hand_data["total_value"],
                hand_data["minimum_value"],
                hand_data["is_blackjack"],
                hand_data["is_starthand"],
                hand_data["is_busted"],
                hand_data["can_double"],
                hand_data["can_split"],
                hand_data["bust_chance"],
                hand_data["frequency"],
                hand_data["probability"]
            ])
        # Datenbank-Insert in einer einzigen Transaktion
        try:
            with self.connection as conn:
                conn.executemany(sql, values)  # Alle Hände auf einmal einfügen
            print(f"{len(hands)} Hände erfolgreich in '{table_name}' gespeichert.")
        except sqlite3.IntegrityError as e:
            print(f"Fehler beim Speichern der Hände: {e}")

    def print_hand_count(self, table_name):
        """
        Gibt die Anzahl der gespeicherten Hände in der angegebenen Tabelle aus.

        Args:
            table_name (str): Name der Tabelle, in der die Hände gespeichert sind.
        """
        print(f"Anzahl gespeicherter Hände in der Tabelle '{table_name}':")
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")  # Tabellennamen korrekt einfügen
            count = cursor.fetchone()[0]
            print(f"{count} Hände sind in der Datenbank gespeichert.")

    def get_dealer_hand_statistics(self):
        """Gibt eine Auswertung der Dealerhände nach Startkarte zurück."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Basis-Query
        query = "SELECT start_card,\n"

        # Dynamische Erstellung der Summen-Abfragen für 17 bis 20
        for value in range(17, 21):
            query += f"    SUM(CASE WHEN total_value = {value} AND NOT is_blackjack AND NOT is_busted THEN probability ELSE 0 END) AS count_{value},\n"

        # Ergänzung für 21, Blackjack und Busted
        query += """
            SUM(CASE WHEN total_value = 21 AND NOT is_blackjack AND NOT is_busted THEN probability ELSE 0 END) AS count_21,
            SUM(CASE WHEN is_blackjack THEN probability ELSE 0 END) AS count_blackjack,
            SUM(CASE WHEN is_busted THEN probability ELSE 0 END) AS count_busted
        FROM dealer_hands
        GROUP BY start_card
        ORDER BY start_card;
        """

        cursor.execute(query)
        results = cursor.fetchall()
        conn.close()

        return results

    def fetch_all_hands(self, table_name):
        """
        Ruft alle gespeicherten Hände aus der Datenbank ab.

        Returns:
            list: Eine Liste von Tupeln, die alle Hände und deren Eigenschaften repräsentieren.
        """
        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {table_name}")
            return cursor.fetchall()

    def close(self):
        """
        Schließt die Verbindung zur Datenbank.
        """
        self.connection.close()
