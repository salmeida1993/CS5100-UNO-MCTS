from uno_deck import Deck
from uno_card import Card, COLORS
import copy
import random

DEBUG = False

class Action:
    def __init__(self, type, card=None, chosen_color=None):
        self.type = type  # 3 general action types: play a card, draw a card, or pass
        self.card = card  # Card to play if action type is "play"
        self.chosen_color = chosen_color  # Color chosen for wild cards if action type is "play" and card is a wild card
        
    # Debugging print statement to verify action creation
    def __str__(self):
        return f"Action: {self.type}, Card: {self.card}, Chosen Color: {self.chosen_color}"
        
    def __repr__(self):
        return self.__str__()

class GameState:
    def __init__(self, hands, draw_pile, discard_pile, current_player):
        self.hands = hands
        self.draw_pile = draw_pile
        self.discard_pile = discard_pile
        self.current_player = current_player

        self.direction = 1  # 1 for clockwise, -1 for counterclockwise
        self.chosen_color = None  # For wild card color choice
    
    # Get the legal actions for the current player based on their hand and the current
    # top card of the discard pile. No valid actions requires a draw.
    def get_legal_actions(self):
        player = self.current_player
        hand = self.hands[player]
        top_card = self.discard_pile[-1]
        legal_actions = []

        # If the top card is a wild card, we need to factor in the chosen color
        # A wild card's "color" depends on the color chosen by who played it,
        # so we create an "effective" card to check playability against.
        # Note that a wild card normally has "wild" as its color.
        if top_card.color == "wild" and self.chosen_color:
            effective_color = self.chosen_color
        else:
            effective_color = top_card.color

        effective_card = Card(effective_color, top_card.value)
        
        for card in hand:
            if (card.is_playable(effective_card)):
                legal_actions.append(Action("play", card))
        
        if not legal_actions:
            legal_actions.append(Action("draw"))
        
        #legal_actions.append(Action("pass"))
        
        return legal_actions

    # Outlining all of the actions that can be taken and how they affect the game state
    # The actual logic behind each card is implemented below: normal play, skip, reverse, draw2,
    # wild, and wild draw 4. Logic for drawing and passing are also included.
    # Note, this is currently set for 2 players - reverse, draw2, and wild_draw4 skip
    # the next player's turn.
    def use_action(self, action):
        temp_state = copy.deepcopy(self)
        player = temp_state.current_player

        if action.type == "play":
            played_card = action.card
            if played_card.color != "wild":
                temp_state.chosen_color = None  # Reset chosen color if a non-wild card is played
            temp_state.hands[player].remove(action.card)
            temp_state.discard_pile.append(action.card)

            if played_card.value == "wild":
                temp_state.chosen_color = action.chosen_color

            elif played_card.value == "skip":
                temp_state.advance_turn()

            elif played_card.value == "reverse":
                temp_state.advance_turn()  # Skip the next player's turn
                # temp_state.direction *= -1 # Commented out to maintain consistent turn order for 2 players
            
            elif played_card.value == "draw2":
                temp_state.advance_turn() # Move to the next player who will draw cards
                next_player = temp_state.current_player
                for _ in range(2):
                    try:
                        drawn_card = temp_state.draw_pile.draw_card(temp_state.discard_pile)
                        temp_state.hands[next_player].append(drawn_card)
                    except StopIteration:
                        break  # If the deck is empty and we can't draw more cards, just break out of the loop

            elif played_card.value == "wild_draw4":
                temp_state.chosen_color = action.chosen_color
                temp_state.advance_turn()
                next_player = temp_state.current_player
                for _ in range(4):
                    try:
                        drawn_card = temp_state.draw_pile.draw_card(temp_state.discard_pile)
                        temp_state.hands[next_player].append(drawn_card)
                    except StopIteration:
                        break  # If the deck is empty and we can't draw more cards, just break out of the loop
        
        # If a player has to draw a card, we check whether the drawn card can be played immediately.
        # If yes, we follow the same actions listed above, but we remove the card from their hand
        # and add it to the discard pile. If not, we just add the card to their hand and continue.
        elif action.type == "draw":
            try:
                 drawn_card = temp_state.draw_pile.draw_card(temp_state.discard_pile)
            except StopIteration:
                temp_state.advance_turn()
                return temp_state

            top_card = temp_state.discard_pile[-1]
            if top_card.color == "wild" and temp_state.chosen_color:
                effective_color = temp_state.chosen_color
            else:
                effective_color = top_card.color

            effective_card = Card(effective_color, top_card.value)

            if drawn_card.is_playable(effective_card):
                if drawn_card.color == "wild":
                    temp_state.chosen_color = random.choice(COLORS)
                else:
                    temp_state.chosen_color = None  # Reset chosen color if a non-wild card is played
                
                if drawn_card.value == "skip":
                    temp_state.advance_turn()

                elif drawn_card.value == "reverse":
                    temp_state.advance_turn()  # Skip the next player's turn
                    # temp_state.direction *= -1 # Commented out to maintain consistent turn order for 2 players
                
                elif drawn_card.value == "draw2":
                    temp_state.advance_turn() # Move to the next player who will draw cards
                    next_player = temp_state.current_player
                    for _ in range(2):
                        try:
                            penalty_card = temp_state.draw_pile.draw_card(temp_state.discard_pile)
                            temp_state.hands[next_player].append(penalty_card)
                        except StopIteration:
                            break

                elif drawn_card.value == "wild_draw4":
                    temp_state.chosen_color = random.choice(COLORS)
                    temp_state.advance_turn()
                    next_player = temp_state.current_player
                    for _ in range(4):
                        try:
                            penalty_card = temp_state.draw_pile.draw_card(temp_state.discard_pile)
                            temp_state.hands[next_player].append(penalty_card)
                        except StopIteration:
                            break

                if DEBUG:
                    print(f"Player {player} drew and played: {drawn_card}")
                   
            else:
                temp_state.discard_pile.append(drawn_card)

        elif action.type == "pass":
            temp_state.advance_turn()
        
        # After processing the action, we move to the next player's turn.
        # For some cards like skip and reverse, we have initially advance the turn in the play logic
        # to now skip the player affected.
        temp_state.advance_turn()
        return temp_state
    
    # Helper function to advance the turn to the next player, factoring in the direction of play.
    def advance_turn(self):
        num_players = len(self.hands)
        self.current_player = (self.current_player + self.direction) % num_players

    # Game over check - if any player has 0 cards in their hand, we end the game.
    def is_game_over(self):
        for hand in self.hands:
            if len(hand) == 0:
                return True
        return False

    # Get the winner of the game, being the player with 0 cards in their hand.
    def get_winner(self):
        for i, hand in enumerate(self.hands):
            if len(hand) == 0:
                return i
        return None
    
    # Function to create the initial game state with a shuffled deck, 7 cards in each player's hand,
    # and one card in the discard pile.
    def initial_state(num_players = 2):
        deck = Deck()
        # print(f"Initial deck has {len(deck.cards)} cards.")
        hands = [[] for _ in range(num_players)]

        # Dealing 7 cards to each player, one at a time.
        # To deal 7 cards to one player, swap the inner and outer loops.
        for _ in range(7):
            for hand in hands:
                hand.append(deck.draw_card())
        discard_pile = [deck.draw_card()]
        return GameState(hands, deck, discard_pile, 0)
    
    def __str__(self):
        return f"Current Player: {self.current_player}\n Top Card: {self.discard_pile[-1]}\n Hands: {[len(hand) for hand in self.hands]}\n"
    
    def __repr__(self):
        return self.__str__()

# Testing the playability logic of cards, especially with wild cards and chosen colors.
def main():
    top_card = Card("red", 5)
    print(top_card)
    test_card1 = Card("red", 7)
    test_card2 = Card("green", 5)
    test_card3 = Card("blue", "skip")
    test_card4 = Card("wild", "wild")
    print(test_card1.is_playable(top_card))  # True (same color)
    print(test_card2.is_playable(top_card))  # True (same value)
    print(test_card3.is_playable(top_card))  # False (different color and value)
    print(test_card4.is_playable(top_card))  # True (wild card)

if __name__ == "__main__":
    main()