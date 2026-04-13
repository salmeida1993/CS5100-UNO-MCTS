from agents.random_agent import RandomAgent
from agents.mcts_agent import MCTSAgent
from evaluation import evaluate_agents
import csv
import matplotlib.pyplot as plt
import numpy as np


def mcts_evaluation():
    iteration_values = [10, 50, 100]
    weights = [0.5, 1.0, 1.41, 2.0]

    results = []

    opponent = RandomAgent()

    for i in iteration_values:
        for w in weights:
            print(f"\nTesting Iterations: {i}, Exploration Weight: {w}")
            mcts_agent = MCTSAgent(iterations=i, exploration_weight=w)
            wins, draws = evaluate_agents(mcts_agent, opponent, num_games=100)
            total = sum(wins) + draws
            win_rate = wins[0] / total if total > 0 else 0
            results.append((i, w, win_rate))
            print(f"Win Rate: {win_rate:.2%}")

    return results
    

def plot_heatmap(results):
    # Convert results to a 2D array for heatmap
    iterations = sorted(set(i for i, w, r in results))
    weights = sorted(set(w for i, w, r in results))
    win_rates = np.zeros((len(iterations), len(weights)))

    for i, w, r in results:
        win_rates[iterations.index(i), weights.index(w)] = r

    plt.figure(figsize=(10, 6))
    plt.imshow(win_rates, cmap='viridis', aspect='auto')
    plt.colorbar(label='MCTS Win Rate')
    plt.xlabel('Exploration Weight')
    plt.ylabel('Iterations')
    plt.title('MCTS Evaluation Results')
    plt.xticks(np.arange(len(weights)), weights)
    plt.yticks(np.arange(len(iterations)), iterations)
    plt.show()


if __name__ == "__main__":
    results = mcts_evaluation()

    with open('mcts_evaluation_results.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Iterations", "Exploration Weight", "MCTS Win Rate"])
        for row in results:
            writer.writerow(row)

    print("\nFinal Results:")
    for i, w, win_rate in results:
        print(f"Iterations: {i}, Exploration Weight: {w}, MCTS Win Rate: {win_rate:.2%}")

    plot_heatmap(results)