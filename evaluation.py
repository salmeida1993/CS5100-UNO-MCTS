from agents.random_agent import RandomAgent
from agents.priority_agent import PriorityAgent
from agents.mcts_agent import MCTSAgent

from game_state import GameState
from engine import play_game
import csv

def evaluate_agents(agent1, agent2, num_games):
    wins = [0, 0]  # wins[0] for agent1, wins[1] for agent2
    draws = 0

    for i in range(num_games):
        state = GameState.initial_state()

        # Alternate which agent goes first to help remove 1st player bias
        if i % 2 == 0:
            agents = [agent1, agent2]
            flip = False
        else:
            agents = [agent2, agent1]
            flip = True

        winner = play_game(agents, state)

        if winner is not None:
           if flip:
               winner = 1 - winner  # Flip winner back to original agent indexing
           wins[winner] += 1 
        else:
            draws += 1
    total = sum(wins) + draws

    return wins, draws, total


def run_evaluation():
    matchups = [
        ("Random vs Priority", RandomAgent(), PriorityAgent()),
        ("Random vs MCTS", RandomAgent(), MCTSAgent(iterations=50, exploration_weight=1)),
        ("Priority vs MCTS", PriorityAgent(), MCTSAgent(iterations=50, exploration_weight=1)),
    ]

    results = []

    for name, agent1, agent2 in matchups:
        print(f"\nSHOWDOWN: {name}")
        wins, draws, total = evaluate_agents(agent1, agent2, num_games=100)
        
        win_rate1 = wins[0] / total
        win_rate2 = wins[1] / total

        print(f"Agent 1 wins: {wins[0]}")
        print(f"Agent 2 wins: {wins[1]}")
        print(f"Draws: {draws}")
        
        results.append([
            name,
            type(agent1).__name__,
            type(agent2).__name__,
            wins[0],
            wins[1],
            draws,
            win_rate1,
            win_rate2
        ])
    
    with open('evaluation_results.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Matchup", "Agent 1 Type", "Agent 2 Type", "Agent 1 Wins", "Agent 2 Wins", "Draws", "Agent 1 Win Rate", "Agent 2 Win Rate"])
        for row in results:
            writer.writerow(row)
    
    print(f"\nEvaluation complete. Results saved to evaluation_results.csv")




if __name__ == "__main__":
    run_evaluation()