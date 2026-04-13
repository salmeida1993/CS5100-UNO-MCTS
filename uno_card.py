# Uno Card Class
# Outlines the structure of a Uno card (value, color)
# as well as general rules if a card can be played on top of another card

COLORS = ["red", "green", "blue", "yellow"]
VALUES = [
    0, 1, 2, 3, 4, 5, 6, 7, 8, 9,
    "skip", "reverse", "draw2"
]
WILD_CARDS = ["wild", "wild_draw4"]

class Card:
    def __init__(self, color, value):
        self.color = color
        self.value = value
    
    def __str__(self):
        return f"{self.color} {self.value}"
    
    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, other):
        return self.color == other.color and self.value == other.value
    
    def is_playable(self, other_card):
        if self.color == other_card.color:
            return True
        if self.value == other_card.value:
            return True
        if self.value in WILD_CARDS:
            return True
        return False