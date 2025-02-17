import unittest
from collections import Counter
from Utility.DB import DatabaseManager

class TestBlackjackHands(unittest.TestCase):
    def setUp(self):
        db_path = "../Data/blackjack.db"  # Der relative Pfad von Tests zu Data
        self.db_manager = DatabaseManager(db_path)

    def count_n_card_hands(self, n):
        deck = [1, 2, 3, 4, 5, 6, 7, 8, 9] * 4 + [10] * 16
        deck_count = Counter(deck)

        def backtrack(remaining, current_sum, last_card):
            if remaining == 0:
                return 1 if current_sum <= 21 else 0
            count = 0
            for card in range(last_card, 11):
                if deck_count[card] > 0 and current_sum + card <= 21:
                    deck_count[card] -= 1
                    count += backtrack(remaining - 1, current_sum + card, card)
                    deck_count[card] += 1
            return count

        return backtrack(n, 0, 1)

    def test_hand_counts(self):
        for n in range(0, 14):  # für Hände mit 0 bis 13 Karten
            with self.subTest(n=n):
                calculated = self.count_n_card_hands(n)
                with self.db_manager.connection:
                    cursor = self.db_manager.connection.cursor()
                    cursor.execute(f'''
                        SELECT COUNT(*)
                        FROM hands
                        WHERE (c1 + c2 + c3 + c4 + c5 + c6 + c7 + c8 + c9 + c10) = {n}                    ''')
                    expected = cursor.fetchone()[0]
                print(f"Für n={n}: Berechnet {calculated}, Erwartet {expected}")
                self.assertEqual(calculated, expected, f"Für n={n}: Berechnet {calculated}, Erwartet {expected}")

    def tearDown(self):
        self.db_manager.connection.close()

if __name__ == '__main__':
    unittest.main()

