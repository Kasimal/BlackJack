import sqlite3
import sys

from Models.Deck import Deck
import Utility.Calculations as calc

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

    def create_table_full_player_hands(self, table_name="Full_player_hands"):
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
                    hand_type TEXT NOT NULL,                   -- Typ der Hand: 'player' oder 'dealer'
                    {", ".join(f"{col} INTEGER" for col in self.card_columns)},
                    hand_text VARCHAR,                         -- Textuelle Darstellung der Hand
                    dealer_start TEXT NOT NULL,                -- Differenzierung nach Dealer-Karten
                    total_value INTEGER,                       -- Gesamtwert der Hand
                    minimum_value INTEGER,                     -- Minimalwert der Hand
                    is_blackjack BOOLEAN,                      -- Ob die Hand ein Blackjack ist
                    is_starthand BOOLEAN,                      -- Ob die Hand eine Starthand ist
                    can_double BOOLEAN DEFAULT 0,              -- Ob die Hand verdoppelt werden kann
                    can_split BOOLEAN DEFAULT 0,               -- Ob die Hand gesplittet werden kann
                    frequency INTEGER,                         -- Häufigkeit der Hand
                    probability FLOAT,                         -- Relative Wahrscheinlichkeit der Hand
                    
                    -- Wahrscheinlichkeiten für verschiedene Endwerte
                    prob_16 FLOAT,                             -- Wahrscheinlichkeit für ≤16
                    prob_17 FLOAT,                             -- Wahrscheinlichkeit für genau 17
                    prob_18 FLOAT,                             -- Wahrscheinlichkeit für genau 18
                    prob_19 FLOAT,                             -- Wahrscheinlichkeit für genau 19
                    prob_20 FLOAT,                             -- Wahrscheinlichkeit für genau 20
                    prob_21 FLOAT,                             -- Wahrscheinlichkeit für genau 21 (kein Blackjack)
                    prob_blackjack FLOAT,                      -- Wahrscheinlichkeit für Blackjack (nur mit zwei Karten)
                    prob_bust FLOAT,                           -- Wahrscheinlichkeit für Bust (>21)
                
                    -- Sieg- und Verlustwahrscheinlichkeiten abhängig von der Dealer-Startkarte
                    win_hit FLOAT,                             -- Wahrscheinlichkeit zu gewinnen bei Hit
                    loss_hit FLOAT,                            -- Wahrscheinlichkeit zu verlieren bei Hit
                    win_stand FLOAT,                           -- Wahrscheinlichkeit zu gewinnen bei Stand
                    loss_stand FLOAT,                          -- Wahrscheinlichkeit zu verlieren bei Stand
                    hit_stand FLOAT,                           -- Differenz Hit-chance und Stand-chance  
                    action VARCHAR,                            -- Empfohlene Aktion, 'hit', 'stand' eventuell auch 'split' oder 'double'
                    ev FLOAT                                   -- Erwartungswert 
                )
            '''
            print(f"Volle Spieler-Hände-Tabelle '{table_name}' wird erstellt.")

            # Ausführung der SQL-Anweisung
            cursor.execute(sql)
            print(f"Tabelle '{table_name}' wurde erfolgreich erstellt.")

    def create_stats_table(self):
        """Erstellt die Tabelle für die Dealerhand-Statistiken mit relativen Häufigkeiten, falls sie nicht existiert."""
        cursor = self.connection.cursor()
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
        self.connection.commit()

    def update_dealer_hand_statistics(self):
        """Berechnet die relativen Häufigkeiten der Dealerhände nach Startkarte."""
        cursor = self.connection.cursor()

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

        self.connection.commit()

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
                hand_data["hand_type"],
                hand_data["start_card"] if hand_data["hand_type"] == "dealer" else None,
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

    def save_full_hands(self, table_name, hands):
        """
        Speichert mehrere Hände auf einmal in der angegebenen Tabelle (Batch-Insert).

        Args:
            table_name (str): Name der Tabelle.
            hands (list of dict): Eine Liste von Händen mit ihren Attributen.
        """
        if not hands:
            return  # Falls keine Hände übergeben wurden, nichts tun

        # Spalten definieren
        columns = [
                      "hand_type"
                  ] + [f"c{i}" for i in range(1, 11)] + [
                      "hand_text", "dealer_start", "total_value", "minimum_value",
                      "is_blackjack", "is_starthand",
                      "can_double", "can_split", "frequency", "probability",
                      "prob_16", "prob_17", "prob_18", "prob_19", "prob_20", "prob_21",
                      "prob_blackjack", "prob_bust",
                      "win_hit", "loss_hit", "win_stand", "loss_stand",
                      "hit_stand", "action", "ev"
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
                hand_data["hand_type"],
                *card_frequencies,
                hand_text,
                ",".join(map(str, hand_data["dealer_start"])),  # Liste in String umwandeln
                hand_data["total_value"],
                hand_data["minimum_value"],
                hand_data["is_blackjack"],
                hand_data["is_starthand"],
                hand_data["can_double"],
                hand_data["can_split"],
                hand_data["frequency"],
                hand_data["probability"],
                hand_data["probabilities"]["<=16"],
                hand_data["probabilities"]["17"],
                hand_data["probabilities"]["18"],
                hand_data["probabilities"]["19"],
                hand_data["probabilities"]["20"],
                hand_data["probabilities"]["21"],
                hand_data["probabilities"]["Blackjack"],
                hand_data["probabilities"]["Bust"],
                hand_data.get("win_hit", 0),
                hand_data.get("loss_hit", 0),
                hand_data.get("win_stand", 0),
                hand_data.get("loss_stand", 0),
                hand_data.get("hit_stand"),
                hand_data.get("action"),
                hand_data.get("ev", 0)
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
        cursor = self.connection.cursor()

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
        return results

    def create_player_dealer_startcard_overview(self, table_name):
        # Bestehende Tabelle löschen
        self.drop_table("Player_dealer_startcard_overview")
        cursor = self.connection.cursor()

        # SQL-Query mit formatiertem Tabellen-Namen
        query = f"""
            CREATE TABLE Player_dealer_startcard_overview AS
            SELECT 
                total_value,
                minimum_value,
                ev,
                dealer_start AS start_card,
                CASE 
                    WHEN total_value = minimum_value THEN 'hard'
                    ELSE 'soft'
                END AS hand_type,
                MIN(hit_stand) AS min_hit_stand,
                MAX(hit_stand) AS max_hit_stand,
                AVG(hit_stand) AS avg_hit_stand,
                CASE 
                    WHEN MIN(hit_stand) < 0 AND MAX(hit_stand) > 0 THEN 'undecided'
                    WHEN AVG(hit_stand) >= 0 THEN 'hit'
                    ELSE 'stand'
                END AS recommended_action
            FROM {table_name}
            WHERE dealer_start GLOB '[0-9]*'  -- Nur numerische Werte zulassen
            GROUP BY total_value, minimum_value, start_card
            ORDER BY hand_type DESC, total_value, start_card;
        """

        cursor.execute(query)
        self.connection.commit()

    def get_ev_for_hands(self, table_name):
        try:
            print("Starte get_ev_for_hands Methode")
            cursor = self.connection.cursor()

            # Spalte 'ev' hinzufügen, falls nicht vorhanden
            cursor.execute(f"PRAGMA table_info({table_name})")
            if "ev" not in {row[1] for row in cursor.fetchall()}:
                cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN ev FLOAT")

            # Einfache Fälle direkt berechnen
            cursor.execute(f"""
                UPDATE {table_name}
                SET ev = win_stand - loss_stand
                WHERE action = 'Stand'
            """)

            cursor.execute(f"""
                UPDATE {table_name}
                SET ev = 
                    CASE
                        WHEN dealer_start = 'Blackjack' AND is_blackjack = 1 THEN 0
                        WHEN is_blackjack = 1 THEN 1.5
                        WHEN dealer_start = 'Blackjack' THEN -1
                    END
                WHERE dealer_start = 'Blackjack' OR is_blackjack = 1
            """)

            # Cache aller Hände aufbauen
            cursor.execute(f"""
                SELECT c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,
                       minimum_value, dealer_start, ev
                FROM {table_name}
                --WHERE (c1 = 4 OR c2 = 4)  --# debugging
            """)
            hand_cache = {
                (c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, min_val, dealer): ev
                for c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, min_val, dealer, ev in cursor.fetchall()
            }
            print(f"Anzahl der gefundenen Hände: {len(hand_cache)}")

            # Hände mit 'Hit' verarbeiten
            cursor.execute(f"""
                SELECT hand_id, minimum_value, dealer_start, 
                       c1,c2,c3,c4,c5,c6,c7,c8,c9,c10
                FROM {table_name}
                WHERE action = 'Hit'
                ORDER BY (c1+c2+c3+c4+c5+c6+c7+c8+c9+c10) DESC
            """)

            for hand in cursor.fetchall():
                hand_id, min_value, dealer_start, *card_counts = hand

                # Deck-Status zurücksetzen
                deck = Deck()

                # Dealer-Karte entfernen
                deck.remove_card(int(dealer_start))

                # Karten aus dem Deck entfernen basierend auf der aktuellen Hand
                for card_value, count in enumerate(card_counts, start=1):
                    for _ in range(count):
                        try:
                            deck.remove_card(card_value)
                        except ValueError:
                            print(f"Ungültige Hand {hand_id}: Zu viele Karten des Werts {card_value}")
                            continue

                # Wahrscheinlichkeiten korrekt berechnen
                total_cards = deck.total_cards()
                probabilities = {}
                for card in range(1, 11):
                    available = deck.card_frequencies[card]
                    probabilities[card] = available / total_cards if total_cards > 0 else 0

                expected_value = 0.0

                # for card in range(1, 11):
                #     if deck.card_frequencies[card] == 0:
                #         continue  # Karte nicht verfügbar
                #
                #     # Neue Kartenverteilung simulieren
                #     new_counts = list(card_counts)
                #     new_counts[card - 1] += 1
                #
                #     # Prüfe Kartenlimit
                #     if new_counts[card - 1] > 4 * deck.deck_count:
                #         new_min = min_value + card
                #         if new_min > 21:
                #             expected_value += probabilities[card] * (-1)
                #         continue
                #
                #     # Restliche Logik...
                #     new_min = min_value + card
                #     if new_min > 21:
                #         expected_value += probabilities[card] * (-1)
                #         continue
                #
                #     # Cache-Key erstellen
                #     cache_key = tuple(int(count) for count in new_counts[:10]) + (int(new_min),) + ((dealer_start,) if isinstance(dealer_start, str) else dealer_start)
                #     next_ev = hand_cache.get(cache_key, 0)
                #     expected_value += probabilities[card] * next_ev

                for card in range(1, 11):
                    if deck.card_frequencies[card] == 0:
                        continue  # Karte nicht mehr verfügbar

                    new_min = min_value + card
                    if new_min > 21:
                        expected_value += probabilities[card] * (-1)  # Bust
                        continue


                    new_counts = list(card_counts)
                    new_counts[card - 1] += 1
                    cache_key = tuple(int(count) for count in new_counts[:10]) + (int(new_min),) + ((dealer_start,) if isinstance(dealer_start, str) else dealer_start)
                    # cache_key = tuple(new_counts + [new_min, dealer_start])

                    # Hier beginnen die Debugging-Ausgaben

                    sys.stdout.flush()

                    if cache_key not in hand_cache:
                        print("Debug-Ausgabe")
                        print(f"Original new_counts: {new_counts}")
                        print(f"Processed new_counts: {tuple(int(count) for count in new_counts[:10])}")
                        print(f"new_min: {new_min}")
                        print(f"dealer_start: {dealer_start}")
                        print(f"Final cache_key: {cache_key}")
                        print(f"Is key in cache: {cache_key in hand_cache}")
                        print("Key not found in cache!")

                    if cache_key in hand_cache:
                        next_ev = hand_cache[cache_key]
                    else:
                        print(f"Warnung: Folgehand nicht im Cache: {cache_key}")
                        next_ev = -1  # Pessimistische Annahme, wenn die Hand fehlt

                    expected_value += probabilities[card] * next_ev

                    #print(f"Nach Ziehen von Karte {card}: EV = {expected_value:.4f}")

                #print(f"Finale EV für diese Hand: {expected_value:.4f}")

                # Update der Datenbank
                cursor.execute(f"""
                    UPDATE {table_name}
                    SET ev = ?
                    WHERE hand_id = ?
                """, (expected_value, hand_id))

            self.connection.commit()

        except sqlite3.Error as e:
            print(f"Datenbankfehler: {e}")
            self.connection.rollback()
        finally:
            if self.connection:
                self.connection.close()

    # def get_ev_for_hands(self, table_name):
    #     try:
    #         cursor = self.connection.cursor()
    #
    #         # Spalte 'ev' hinzufügen, falls nicht vorhanden
    #         cursor.execute(f"PRAGMA table_info({table_name})")
    #         if "ev" not in {row[1] for row in cursor.fetchall()}:
    #             cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN ev FLOAT")
    #
    #         # Einfache Fälle direkt berechnen
    #         cursor.execute(f"""
    #             UPDATE {table_name}
    #             SET ev = win_stand - loss_stand
    #             WHERE action = 'Stand'
    #         """)
    #
    #         cursor.execute(f"""
    #             UPDATE {table_name}
    #             SET ev =
    #                 CASE
    #                     WHEN dealer_start = 'Blackjack' AND is_blackjack = 1 THEN 0
    #                     WHEN is_blackjack = 1 THEN 1.5
    #                     WHEN dealer_start = 'Blackjack' THEN -1
    #                 END
    #             WHERE dealer_start = 'Blackjack' OR is_blackjack = 1
    #         """)
    #
    #         # Cache aller Hände aufbauen
    #         cursor.execute(f"""
    #             SELECT c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,
    #                    minimum_value, dealer_start, ev
    #             FROM {table_name}
    #         """)
    #         hand_cache = {
    #             (c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, min_val, dealer): ev
    #             for c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, min_val, dealer, ev in cursor.fetchall()
    #         }
    #
    #         # Hände mit 'Hit' verarbeiten (sortiert nach Kartenanzahl)
    #         cursor.execute(f"""
    #             SELECT hand_id, minimum_value, dealer_start,
    #                    c1,c2,c3,c4,c5,c6,c7,c8,c9,c10
    #             FROM {table_name}
    #             WHERE action = 'HIT'
    #             ORDER BY (c1+c2+c3+c4+c5+c6+c7+c8+c9+c10) DESC
    #         """)
    #
    #         for hand in cursor.fetchall():
    #             hand_id, min_value, dealer_start, *card_counts = hand
    #             hand_cards = []
    #             for value, count in enumerate(card_counts, start=1):
    #                 hand_cards.extend([value] * count)
    #
    #             probabilities = calc.card_draw_probabilities(hand_cards, dealer_start)
    #             expected_value = 0.0
    #
    #             for card in range(1, 11):
    #                 card_prob = probabilities[card]
    #                 new_min = min_value + card  # Neuer minimaler Wert
    #
    #                 if new_min > 21:  # Bust-Fall direkt behandeln
    #                     expected_value += card_prob * (-1)
    #                     continue
    #
    #                 # Neue Kartenverteilung erstellen
    #                 new_counts = list(card_counts)
    #                 new_counts[card - 1] += 1
    #                 cache_key = tuple(int(count) for count in new_counts[:10]) + (int(new_min),) + (
    #                     (dealer_start,) if isinstance(dealer_start, str) else dealer_start)
    #
    #                 if cache_key in hand_cache:
    #                     next_ev = hand_cache[cache_key]
    #                 else:
    #                     print(f"Warnung: Hand {cache_key} nicht gefunden (min={new_min})")
    #                     next_ev = -1 if new_min > 21 else 0  # Fallback für fehlende Daten
    #
    #                 expected_value += card_prob * next_ev
    #
    #             # EV in die Datenbank schreiben
    #             cursor.execute(f"""
    #                 UPDATE {table_name}
    #                 SET ev = ?
    #                 WHERE hand_id = ?
    #             """, (expected_value, hand_id))
    #
    #         self.connection.commit()
    #
    #     except sqlite3.Error as e:
    #         print(f"Datenbankfehler: {e}")
    #         self.connection.rollback()
    #     finally:
    #         if self.connection:
    #             self.connection.close()

    def create_and_fill_player_dealer_strategy_table(self):
        self.drop_table("Player_dealer_strategy_table")
        cursor = self.connection.cursor()

        query = """
            CREATE TABLE Player_dealer_strategy_table AS
            SELECT 
                total_value,
                MAX(CASE WHEN start_card = 1 THEN decision END) AS dealer_Ass,
                MAX(CASE WHEN start_card = 2 THEN decision END) AS dealer_2,
                MAX(CASE WHEN start_card = 3 THEN decision END) AS dealer_3,
                MAX(CASE WHEN start_card = 4 THEN decision END) AS dealer_4,
                MAX(CASE WHEN start_card = 5 THEN decision END) AS dealer_5,
                MAX(CASE WHEN start_card = 6 THEN decision END) AS dealer_6,
                MAX(CASE WHEN start_card = 7 THEN decision END) AS dealer_7,
                MAX(CASE WHEN start_card = 8 THEN decision END) AS dealer_8,
                MAX(CASE WHEN start_card = 9 THEN decision END) AS dealer_9,
                MAX(CASE WHEN start_card = 10 THEN decision END) AS dealer_10
            FROM (
                SELECT 
                    total_value,
                    start_card,
                    CASE 
                        WHEN min_hit_stand < 0 AND max_hit_stand > 0 THEN 'undecided'
                        WHEN avg_hit_stand >= 0 THEN 'Hit'
                        ELSE 'Stand'
                    END AS decision
                FROM Player_dealer_startcard_overview
                WHERE hand_type = 'hard'
            ) subquery
            GROUP BY total_value
            ORDER BY total_value;
        """

        cursor.execute(query)
        self.connection.commit()

    def create_and_fill_player_dealer_strategy_table_soft(self):
        self.drop_table("Player_dealer_strategy_table_soft")
        cursor = self.connection.cursor()

        query = """
            CREATE TABLE Player_dealer_strategy_table_soft AS
            SELECT 
                total_value,
                MAX(CASE WHEN start_card = 1 THEN decision END) AS dealer_Ass,
                MAX(CASE WHEN start_card = 2 THEN decision END) AS dealer_2,
                MAX(CASE WHEN start_card = 3 THEN decision END) AS dealer_3,
                MAX(CASE WHEN start_card = 4 THEN decision END) AS dealer_4,
                MAX(CASE WHEN start_card = 5 THEN decision END) AS dealer_5,
                MAX(CASE WHEN start_card = 6 THEN decision END) AS dealer_6,
                MAX(CASE WHEN start_card = 7 THEN decision END) AS dealer_7,
                MAX(CASE WHEN start_card = 8 THEN decision END) AS dealer_8,
                MAX(CASE WHEN start_card = 9 THEN decision END) AS dealer_9,
                MAX(CASE WHEN start_card = 10 THEN decision END) AS dealer_10
            FROM (
                SELECT 
                    total_value,
                    start_card,
                    CASE 
                        WHEN min_hit_stand < 0 AND max_hit_stand > 0 THEN 'undecided'
                        WHEN avg_hit_stand >= 0 THEN 'Hit'
                        ELSE 'Stand'
                    END AS decision
                FROM Player_dealer_startcard_overview
                WHERE hand_type = 'soft'
            ) subquery
            GROUP BY total_value
            ORDER BY total_value;
        """

        cursor.execute(query)
        self.connection.commit()

    def create_and_fill_double_overview(self):
        """
        Erstellt die Tabelle 'Double_overview' und füllt sie basierend auf den Daten in 'Full_player_hands'.
        Double gilt, wenn (win_hit - loss_hit) * 2 größer ist als ev. Andernfalls wird die ursprüngliche Aktion übernommen.

        Die Tabelle enthält jede einzelne Starthand als Zeile und die Dealer-Startkarte als Spalte.
        """
        cursor = self.connection.cursor()

        # Tabelle erstellen
        dealer_columns = ", ".join([f"'Dealer_{i}' TEXT" for i in range(1, 11)])
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS Double_overview (
                hand_text VARCHAR PRIMARY KEY,
                {dealer_columns}
            )
        """)

        # Alle Starthände und Dealer-Karten abrufen
        cursor.execute("SELECT DISTINCT hand_text FROM Full_player_hands WHERE is_starthand = 1")
        hands = [row[0] for row in cursor.fetchall()]

        for hand_text in hands:
            values = []
            for dealer_card in range(1, 11):
                # Dealer-Karte als String für die Abfrage
                dealer_card_str = str(dealer_card)

                # Erwartungswert und Wahrscheinlichkeiten abrufen
                cursor.execute("""
                    SELECT action, ev, win_hit, loss_hit 
                    FROM Full_player_hands 
                    WHERE hand_text = ? AND dealer_start = ?
                """, (hand_text, dealer_card_str))
                result = cursor.fetchone()

                if result:
                    action, ev, win_hit, loss_hit = result

                    # Überprüfen auf None und Standardaktion verwenden, wenn nötig
                    if ev is None or win_hit is None or loss_hit is None:
                        values.append(f"'{action}'")
                    else:
                        # Double-Bedingung prüfen
                        if (win_hit - loss_hit) * 2 > max(ev,0):
                            values.append("'Double'")
                        else:
                            values.append(f"'{action}'")
                else:
                    values.append("NULL")

            # Einfügen oder Aktualisieren
            cursor.execute(f"""
                INSERT INTO Double_overview (hand_text, {', '.join([f"'Dealer_{i}'" for i in range(1, 11)])})
                VALUES (?, {', '.join(values)})
                ON CONFLICT(hand_text) DO UPDATE SET
                {', '.join([f"'Dealer_{i}'=excluded.'Dealer_{i}'" for i in range(1, 11)])}
            """, (hand_text,))

        self.connection.commit()
        print("Tabelle 'Double_overview' erfolgreich erstellt und gefüllt.")
