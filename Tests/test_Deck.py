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

if __name__ == '__main__':
    unittest.main()



