from CardDeck import CardDeck
from Hand import Hand


def Game():
    print("Willkommen zu Blackjack!")
    deck = CardDeck(num_decks=1)
    hand = Hand()

    # Initiale Hand
    hand.add_card(deck.draw_card())
    hand.add_card(deck.draw_card())
    print("Ihre Starthand:")
    print(hand)

    def display_probabilities():
        reach, exceed = hand.probability_to_reach_or_exceed(deck)
        print(f"Sie sollten eine weitere Karten nehmen: {reach:.2%} zu {exceed:.2%}")

    display_probabilities()

    # Spieler entscheidet, ob weitere Karten gezogen werden sollen
    while True:
        if hand.calculate_value() > 21:
            print("Sie haben verloren! Ihre Hand hat einen Wert von mehr als 21.")
            break

        choice = input("Möchten Sie eine weitere Karte ziehen? (j/n): ").lower()
        if choice == 'j':
            hand.add_card(deck.draw_card())
            print("Ihre aktuelle Hand:")
            print(hand)
            display_probabilities()
        elif choice == 'n':
            print("Spiel beendet. Ihre finale Hand:")
            print(hand)
            if hand.calculate_value() <= 21:
                print("Sie haben gewonnen! 🎉")
            break
        else:
            print("Ungültige Eingabe. Bitte 'j' oder 'n' eingeben.")

if __name__ == "__main__":
    Game()
