DEBUG = False

# Class of the engine for running the Uno game
# Contains the main game loop and logic for executing player actions and updating the game state
def play_game(agents, state):
    turns = 0
    if DEBUG:
        print(state)
    while not state.is_game_over():
        #print(state)
        turns += 1
        if turns > 200:  # Safety check to prevent infinite loops
            print("Max turns reached.")
            return None
        player = state.current_player
        agent = agents[player]
        action = agent.select_action(state)

        if DEBUG:
            print(f"Player {player} takes action: {action}")
        state = state.use_action(action)
    if DEBUG:
        print(state)
    return state.get_winner()