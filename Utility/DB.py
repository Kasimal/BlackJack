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
                    hand_id INTEGER PRIMARY KEY AUTOINCREMENT, -- Eindeutige ID
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
                    frequency INTEGER                          -- Häufigkeit der Hand
                )
            '''
            print(f"Einheitliche Hände-Tabelle '{table_name}' wird erstellt.")

            # Ausführung der SQL-Anweisung
            cursor.execute(sql)
            print(f"Tabelle '{table_name}' wurde erfolgreich erstellt.")

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

    def save_hand(self, table_name, hands_type, hand, start_card=None, total_value=None, minimum_value=None,
                  is_blackjack=False, is_starthand=False, is_busted=False,
                  can_double=False, can_split=False, bust_chance=0, frequency=1):
        """
        Speichert eine Hand in der angegebenen Tabelle.

        Args:
            table_name (str): Name der Tabelle.
            hands_type (str): 'player' oder 'dealer'.
            hand (list): Die Karten in der Hand.
            start_card (int, optional): Die Startkarte des Dealers (nur für Dealerhände).
            total_value (int, optional): Der Gesamtwert der Hand.
            minimum_value (int, optional): Der Mindestwert der Hand (nur für Spielerhände).
            is_blackjack (bool, optional): Ob die Hand ein Blackjack ist.
            is_starthand (bool, optional): Ob die Hand eine Starthand ist.
            is_busted (bool, optional): Ob die Hand über 21 ist.
            can_double (bool, optional): Ob die Hand verdoppelt werden kann.
            can_split (bool, optional): Ob die Hand gesplittet werden kann.
            bust_chance (float, optional): Wahrscheinlichkeit, die Hand zu überbieten.
            frequency (int): Häufigkeit der Hand.
        """
        # Häufigkeiten der Kartenwerte (1 bis 10) in der Hand berechnen
        card_frequencies = [hand.count(i) for i in range(1, 11)]  # Liste mit Häufigkeiten von Kartenwerten 1-10

        # Erstelle Handtext
        hand_text = ",".join(map(str, hand))

        # Spalten und Werte vorbereiten
        columns = ["hand_type"] + [f"c{i}" for i in range(1, 11)]  # hand_type und c1 bis c10
        values = [hands_type] + card_frequencies  # hand_type und Kartenhäufigkeiten als Werte
        columns += ["hand_text", "start_card", "total_value", "minimum_value",
                    "is_blackjack", "is_starthand", "is_busted",
                    "can_double", "can_split", "bust_chance", "frequency"]
        values += [hand_text, start_card, total_value, minimum_value,
                   is_blackjack, is_starthand, is_busted,
                   can_double, can_split, bust_chance, frequency]

        # SQL-Anweisung dynamisch erstellen
        placeholders = ", ".join(["?"] * len(values))
        sql = f'''
            INSERT INTO {table_name} ({", ".join(columns)})
            VALUES ({placeholders})
        '''
        try:
            with self.connection as conn:
                conn.execute(sql, values)
            print(f"Hand {hand_text} erfolgreich in '{table_name}' gespeichert.")
        except sqlite3.IntegrityError as e:
            print(f"Fehler beim Speichern der Hand {hand_text}: {e}")

    # def save_hand(self, hand, total_value, minimum_value, is_blackjack, is_starthand, is_busted, can_double, can_split, bust_chance, frequency):
    #     """
    #     Speichert eine Hand in der Datenbank.
    #     Args:
    #         hand (list): Die aktuelle Hand als Liste der Kartenzahlen.
    #         total_value (int): Der Gesamtwert der Hand.
    #         minimum_value (int): Der Mindestwert der Hand.
    #         is_blackjack (bool): Ob die Hand ein Blackjack ist.
    #         is_starthand (bool): Ob die Hand eine Starthand ist.
    #         is_busted (bool): Ob die Hand über 21 ist.
    #         can_double (bool): Ob die Hand verdoppelt werden kann.
    #         can_split (bool): Ob die Hand gesplittet werden kann.
    #         bust_chance (float): Wahrscheinlichkeit mit der nächsten Karte zu überbieten
    #         frequency (int): Die Häufigkeit der Hand.
    #
    #     """
    #     card_counts = [hand.count(card) for card in range(1, 11)]  # Zähle jede Karte in der Hand
    #     hand_text = ",".join(map(str, hand))  # Wandelt die Hand in einen Textstring um
    #
    #     with self.connection as conn:
    #         cursor = conn.cursor()
    #
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
    #
    #         else:
    #             # Neue Hand einfügen
    #             #print(f"Columns: {len(self.card_columns) + 10}, Values: {len(card_counts + [hand_text, total_value, minimum_value, is_blackjack, is_starthand, is_busted, can_double, can_split, bust_chance, frequency])}")
    #             #print(f"Values: {card_counts + [hand_text, total_value, minimum_value, is_blackjack, is_starthand, is_busted, can_double, can_split, bust_chance, frequency]}")
    #             cursor.execute(f'''
    #                 INSERT INTO hands ({", ".join(self.card_columns)}, hand_text, total_value, minimum_value,
    #                                    is_blackjack, is_starthand, is_busted, can_double, can_split, bust_chance, frequency)
    #                 VALUES ({", ".join("?" for _ in range(len(self.card_columns) + 10))})
    #             ''', card_counts + [hand_text, total_value, minimum_value, is_blackjack, is_starthand, is_busted,
    #                                 can_double, can_split, bust_chance, frequency])
    #
    # def _generate_where_clause(self, card_counts):
    #     """
    #     Generiert eine WHERE-Bedingung für die Kartenzählungen.
    #
    #     Args:
    #         card_counts (list): Eine Liste mit der Anzahl der Karten (1 bis 10).
    #
    #     Returns:
    #         str: Die generierte WHERE-Bedingung.
    #     """
    #     conditions = []
    #     for i, count in enumerate(card_counts):
    #         conditions.append(f"c{i + 1} = ?")
    #     return " AND ".join(conditions)
    #
    # def save_dealer_hand(self, table_name, start_card, result):
    #     """
    #     Speichert die Dealer-Hand in der angegebenen Tabelle in der Datenbank.
    #     Jede Kombination von start_card und result wird als neuer Eintrag gespeichert.
    #
    #     Args:
    #         table_name (str): Der Name der Tabelle, in der die Hand gespeichert werden soll.
    #         start_card (int): Die Startkarte der Hand.
    #         result (str): Das Ergebnis der Hand (z. B. 'total_17', 'total_18', ..., 'blackjack', 'bust').
    #     """
    #     with self.connection as conn:
    #         cursor = conn.cursor()
    #
    #         # Überprüfen, ob das Ergebnis gültig ist
    #         valid_results = ["total_17", "total_18", "total_19", "total_20", "total_21", "blackjack", "bust"]
    #         if result not in valid_results:
    #             raise ValueError(
    #                 f"Ungültiges Ergebnis '{result}'. Erlaubte Ergebnisse sind: {', '.join(valid_results)}")
    #
    #         # Einfügen eines neuen Eintrags
    #         cursor.execute(f'''
    #             INSERT INTO {table_name} (start_card, {result})
    #             VALUES (?, 1)
    #         ''', (start_card,))
    #
    #         print(
    #             f"Neue Dealer-Hand mit Startkarte '{start_card}' und Ergebnis '{result}' in Tabelle '{table_name}' gespeichert.")


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
