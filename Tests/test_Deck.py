import unittest
from Models.Deck import Deck

class FrequencyTest(unittest.TestCase):
    def test_frequencies(self):
        deck_count = 1  # Anzahl der Decks
        deck = Deck(deck_count)  # Ein Deck
        cards_1_2 = [1, 2]  # Ass und 2
        cards_1_1 = [1, 1]  # Ass Ass
        cards_1_1_1 = [1, 1, 1]  # Ass Ass Ass
        cards_1_1_2 = [1, 1, 2]  # Ass Ass 2
        cards_1_10_10 = [1, 10, 10] # Ass Zehn Zehn, Trickfrage, weil hier nicht alle Möglichkeiten valide sind,
                                    # Ass Zehn dann Zehn ist unmöglich, nur Zehn Zehn Ass ist möglich

        frequency_1_2 = deck.calculate_hand_frequency(cards_1_2)
        frequency_1_1 = deck.calculate_hand_frequency(cards_1_1)
        frequency_1_1_1 = deck.calculate_hand_frequency(cards_1_1_1)
        frequency_1_1_2 = deck.calculate_hand_frequency(cards_1_1_2)
        frequency_1_10_10 = deck.calculate_hand_frequency(cards_1_10_10)

        print(f"Häufigkeit von Ass 2: {frequency_1_2} Erwartet: 16")
        print(f"Häufigkeit von Ass Ass: {frequency_1_1} Erwartet: 6")
        print(f"Häufigkeit von Ass Ass Ass: {frequency_1_1_1} Erwartet: 4")
        print(f"Häufigkeit von 10 10 9: {frequency_1_1_2} Erwartet: 24")
        print(f"Häufigkeit von Ass 10 10: {frequency_1_10_10} Erwartet: 480")

        self.assertEqual(frequency_1_2,16)
        self.assertEqual(frequency_1_1, 6)
        self.assertEqual(frequency_1_1_1, 4)
        self.assertEqual(frequency_1_1_2,24)
        self.assertEqual(frequency_1_10_10, 480)

if __name__ == '__main__':
    unittest.main()
