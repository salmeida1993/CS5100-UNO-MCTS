from agents.random_agent import RandomAgent
from agents.priority_agent import PriorityAgent
from agents.mcts_agent import MCTSAgent

from game_state import GameState
from engine import play_game

# This file is for running a single game between two agents, to test that things actually work
# and see an output to a game. The main evaluation loop is in evaluation.py, which runs many 
# games and collects statistics on win rates.
agents = [RandomAgent(), RandomAgent()]
prio_agents = [PriorityAgent(), PriorityAgent()]
mcts_agents = [MCTSAgent(iterations=50), RandomAgent()]
state = GameState.initial_state()
#winner = play_game(agents, state)
#winner = play_game(prio_agents, state)
winner = play_game(mcts_agents, state)
if winner is not None:
    print(f"Player {winner} wins!")
else:
    print("The game ended in a draw.")