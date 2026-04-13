from uno_card import COLORS, WILD_CARDS
import random

# A simple agent that picks a random valid action from the current game state.
class RandomAgent:
    def select_action(self, state):
        valid_actions = state.get_legal_actions()
        action = random.choice(valid_actions)
        if action.card and action.card.value in WILD_CARDS:
            action.chosen_color = random.choice(COLORS)
        return action
