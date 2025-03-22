import unittest
import Utility.Calculations as calc

class DeckTest(unittest.TestCase):
    def test_frequencies(self):
        cards_1_2 = [1, 2]  # Ass und 2
        cards_1_1 = [1, 1]  # Ass Ass
        cards_1_1_1 = [1, 1, 1]  # Ass Ass Ass
        cards_1_1_2 = [1, 1, 2]  # Ass Ass 2
        cards_1_10_10 = [1, 10, 10]  # Ass Zehn Zehn, Trickfrage, weil hier nicht alle Möglichkeiten valide sind,
        # Ass Zehn dann Zehn ist unmöglich, nur Zehn Zehn Ass ist möglich

        frequency_1_2 = calc.hand_frequency(cards_1_2)
        frequency_1_1 = calc.hand_frequency(cards_1_1)
        frequency_1_1_1 = calc.hand_frequency(cards_1_1_1)
        frequency_1_1_2 = calc.hand_frequency(cards_1_1_2)
        frequency_1_10_10 = calc.hand_frequency(cards_1_10_10)

        print(f"Häufigkeit von Ass 2: {frequency_1_2} Erwartet: 16")
        print(f"Häufigkeit von Ass Ass: {frequency_1_1} Erwartet: 6")
        print(f"Häufigkeit von Ass Ass Ass: {frequency_1_1_1} Erwartet: 4")
        print(f"Häufigkeit von 10 10 9: {frequency_1_1_2} Erwartet: 24")
        print(f"Häufigkeit von Ass 10 10: {frequency_1_10_10} Erwartet: 480")

        self.assertEqual(frequency_1_2, 16)
        self.assertEqual(frequency_1_1, 6)
        self.assertEqual(frequency_1_1_1, 4)
        self.assertEqual(frequency_1_1_2, 24)
        self.assertEqual(frequency_1_10_10, 480)

    def test_calculate_bust_probability(self):
        cards_5_7 = [5, 7]          # 12, nur 10er überbieten
        cards_3_8 = [3, 8]          # 11, nichts überbietet
        cards_2_9_10 = [2, 9, 10]   # 21, alles überbietet
        cards_10_10 = [10, 10]      # 20, alles außer Asse überbieten

        bust_probability = calc.bust_probability(cards_5_7)
        print(f"Wahrscheinlichkeit bei {cards_5_7} zu überbieten: {bust_probability} Erwartet: 0.32")
        self.assertEqual(bust_probability, 0.32)

        bust_probability = calc.bust_probability(cards_3_8)
        print(f"Wahrscheinlichkeit bei {cards_3_8} zu überbieten: {bust_probability} Erwartet: 0.0")
        self.assertEqual(bust_probability, 0.0)

        bust_probability = calc.bust_probability(cards_2_9_10)
        print(f"Wahrscheinlichkeit bei {cards_2_9_10} zu überbieten: {bust_probability} Erwartet: 1.0")
        self.assertEqual(bust_probability, 1.0)

        bust_probability = calc.bust_probability(cards_10_10)
        print(f"Wahrscheinlichkeit bei {cards_10_10} zu überbieten: {bust_probability} Erwartet: 0.92")
        self.assertEqual(bust_probability, 0.92)

    def test_probability_distribution(self):
        hand = [1, 1, 5]
        expected_probabilities = {
            "<=16": 0.3878,
            "17": 0.3265,
            "18": 0.0408,
            "19": 0.0816,
            "20": 0.0816,
            "21": 0.0816,
            "Blackjack": 0.0,
            "Bust": 0.0,
        }
        probabilities = calc.probability_distribution(hand)

        for key, expected_value in expected_probabilities.items():
            actual_value = float(probabilities.get(key, 0.0))  # Sicherstellen, dass es ein Float ist
            print(f"{key}: Erwartet {expected_value:.4f}, Berechnet {actual_value:.4f}")
            self.assertAlmostEqual(actual_value, expected_value, places=4)

    def test_card_draw_probabilities(self):
        """
        Testet verschiedene Fälle für die card_draw_probabilities Methode:
        - Gültige Eingaben mit Integer und String
        - Ungültige dealer_start-Werte
        - Fehlerhafte Eingaben
        """

        # 1. Gültige Eingaben
        expected_probabilities_1 = {
            1: 0.0816, 2: 0.0816, 3: 0.0816, 4: 0.0816,
            5: 0.0612, 6: 0.0816, 7: 0.0612, 8: 0.0816,
            9: 0.0816, 10: 0.3061
        }
        probabilities = calc.card_draw_probabilities([10, 5], 7)
        for card, expected in expected_probabilities_1.items():
            self.assertAlmostEqual(probabilities[card], expected, places=4)

        expected_probabilities_2 = {
            1: 0.0816, 2: 0.0612, 3: 0.0612, 4: 0.0816,
            5: 0.0816, 6: 0.0816, 7: 0.0816, 8: 0.0816,
            9: 0.0612, 10: 0.3265
        }
        probabilities = calc.card_draw_probabilities([2, 3], "9")
        for card, expected in expected_probabilities_2.items():
            self.assertAlmostEqual(probabilities[card], expected, places=4)

        # 2. Ungültige dealer_start: 'Blackjack'
        with self.assertRaises(ValueError):
            calc.card_draw_probabilities([], "Blackjack")

        # 3. Ungültige dealer_start außerhalb von 1-10
        with self.assertRaises(ValueError):
            calc.card_draw_probabilities([], 12)

        # 4. Ungültige dealer_start als nicht-konvertierbarer Wert
        with self.assertRaises(ValueError):
            calc.card_draw_probabilities([], "abc")

        # 5. Test mit leerer Hand und dealer_start = 1
        probabilities = calc.card_draw_probabilities([], 1)
        self.assertAlmostEqual(float(sum(probabilities.values())), 1.0, places=4)


if __name__ == '__main__':
    unittest.main()



