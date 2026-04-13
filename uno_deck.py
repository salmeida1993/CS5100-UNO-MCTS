from uno_card import Card, COLORS, VALUES, WILD_CARDS
import random

class Deck:
    def __init__(self):
        self.cards = []
        self.generate_deck()
        self.shuffle()

    # Generate a standard Uno deck
    # Each color has 1 zero card, 2 of each number/action card,
    # and 8 total wild cards (4 wild, 4 wild draw 4)
    def generate_deck(self):
        for color in COLORS:
            for value in VALUES:
                self.cards.append(Card(color, value)) #Add one of each card
                if value !=0: #Add a second card for all cards except 0
                    self.cards.append(Card(color, value))

        for x in range(4):
            self.cards.append(Card("wild", "wild"))
            self.cards.append(Card("wild", "wild_draw4"))

    # Randomly shuffling the deck
    def shuffle(self):
        random.shuffle(self.cards)

    # Draw a card from the deck, checking if the deck is empty first
    def draw_card(self, discard_pile=None):
        if len(self.cards) == 0:
            if discard_pile and len(discard_pile) > 1:
                top_card = discard_pile.pop()  # Keep the top card on the discard pile
                self.cards = discard_pile[:] # Take all cards from discard pile except top card, add them back to deck
                self.shuffle()
                discard_pile.clear()
                discard_pile.append(top_card)  # Put the top card back on the discard pile
            else:
                raise StopIteration("Deck is empty! Cannot draw a card.")
        return self.cards.pop()
    
    # Check if the deck is empty
    def is_empty(self):
        return len(self.cards) == 0