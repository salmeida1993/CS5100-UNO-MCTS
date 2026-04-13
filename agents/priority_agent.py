from uno_card import COLORS, WILD_CARDS
import random

DEBUG = False

# A simple agent that prioritizes playing action cards (skip, reverse, draw2) and wild cards 
# over number cards. The action card picked is random. If no action cards are available,
# it just picks a random valid card to play.
class PriorityAgent:
    def select_action(self, state):
        valid_actions = state.get_legal_actions()
        # First, filter for action cards and wild cards from the set of valid actions
        priority_actions = []
        for action in valid_actions:
            if action.card and action.card.value in WILD_CARDS + ["skip", "reverse", "draw2"]:
                priority_actions.append(action)
    
        if DEBUG:
            print(f"Priority actions available: {priority_actions}")
        
        # If there are any priority actions available, randomly select one of them
        if priority_actions:
            action = random.choice(priority_actions)
            if action.card and action.card.value in WILD_CARDS:
                action.chosen_color = random.choice(COLORS)
            return action
        
        # If no priority actions are available, pick a random valid regular action (number card or draw)
        action = random.choice(valid_actions)
        return action