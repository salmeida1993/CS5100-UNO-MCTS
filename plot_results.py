import pandas as pd
import matplotlib.pyplot as plt

def plot_results(csv_file = 'evaluation_results.csv'):
    df = pd.read_csv(csv_file)
    df = df[df['Matchup'].isin(['Random vs Priority', 'Random vs MCTS', 'Priority vs MCTS'])]
    # Plotting win rates for each matchup
    plt.figure(figsize=(12, 6))
    for matchup in df['Matchup'].unique():
        subset = df[df['Matchup'] == matchup]
        plt.bar(matchup, subset['Agent 1 Win Rate'].values[0], label=f"{subset['Agent 1 Type'].values[0]} Win Rate")
        plt.bar(matchup, subset['Agent 2 Win Rate'].values[0], bottom=subset['Agent 1 Win Rate'].values[0], label=f"{subset['Agent 2 Type'].values[0]} Win Rate")

    plt.ylabel('Win Rate')
    plt.title('Agent Win Rates by Matchup')
    plt.xticks(rotation=0)
    plt.legend()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    plot_results()