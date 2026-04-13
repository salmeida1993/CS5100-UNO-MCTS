import math
import random
import sys
import copy
sys.path.insert(0, './')
from game_state import GameState, Card, Deck

DEBUG = False

class MCTSNode:
    def __init__(self, state, parent=None, action=None, exploration_weight=1.41):
        self.state = state
        self.parent= parent
        self.action = action
        self.children = []
        self.visits = 0
        self.exploration_weight = exploration_weight
        self.wins = 0

        self.player = state.current_player
        self.untried_actions = state.get_legal_actions()

        # For debugging purposes, we can track the depth of the node in the tree
        self.depth = parent.depth + 1 if parent else 0

# Upper confidence bound (UCB) forumla for trees (UCT)
def ucb(node):
    if node.visits == 0:
        return float('inf')  # Prioritize unvisited nodes
    
    parent_visits = node.parent.visits if node.parent.visits > 0 else 1
    c = node.exploration_weight
    exploit = node.wins / node.visits
    explore = c * math.sqrt(math.log(parent_visits) / node.visits)
    return exploit + explore

# Select the child with the highest UCB score
def select_child(node):
    return max(node.children, key=ucb)

# Expand the node by taking one of its untried actions and creating a new child node for that action
def expand(node):
    action = node.untried_actions.pop()
    next_state = node.state.use_action(action)
    child_node = MCTSNode(next_state, parent=node, action=action, exploration_weight=node.exploration_weight)
    node.children.append(child_node)

    # Debug print statemennt to verify who the child node belongs to
    if DEBUG:
        print(
            f"Depth {child_node.depth} | "
            f"Action: {action} | "
            f"Player BEFORE: {node.player} -> Player AFTER: {child_node.player}"
        )

    return child_node

# Simulate a random playout from the given state until the game is over, and return the result
def rollout(state, max_depth=100):
    current_state = copy.deepcopy(state)
    depth = 0

    while not current_state.is_game_over() and depth < max_depth:
        valid_actions = current_state.get_legal_actions()
        action = random.choice(valid_actions)
        current_state = current_state.use_action(action)
        depth += 1

    return current_state.get_winner()

# Backpropagate the result of the simulation up the tree, updating the visit and win 
# counts for each node
def backpropagate(node, winner, root_player):
    while node is not None:
        node.visits += 1
        if winner == root_player:
            if DEBUG:
                print(f"Winner: {winner}, Root: {root_player}, Node Player: {node.player}")
            node.wins += 1
        node = node.parent

# An MCTS agent that uses the Monte Carlo Tree Search algorithm to select actions. 
# It builds a search tree based on the game state, simulates random playouts, and 
# backpropagates the results to find the most promising action.
class MCTSAgent:
    def __init__(self, iterations, exploration_weight=1.41):
        self.iterations = iterations
        self.exploration_weight = exploration_weight

    def select_action(self, state):
        root = MCTSNode(state, exploration_weight=self.exploration_weight)
        root_player = state.current_player
        for _ in range(self.iterations):
            node = root

            #Step 1: Selection
            while node.children and not node.untried_actions:
                node = select_child(node)

            #Step 2: Expansion
            if node.untried_actions:
                node = expand(node)

            #Step 3: Simulation
            winner = rollout(node.state)

            #Step 4: Backpropagation
            backpropagate(node, winner, root_player)
        
        # After all iterations, select the child with the most visits (most promising action)
        best_child = max(root.children, key=lambda c: c.visits)
        if DEBUG:
            print(f"Selected action: {best_child.action} with {best_child.visits} visits and {best_child.wins} wins")
        return best_child.action
    

def main():
    state = GameState(
        hands=[
            [Card("red", "skip")],
            [Card("blue", "3")]
        ],
        draw_pile=Deck(),
        discard_pile=[Card("red", "5")],
        current_player=0
    )
    agent = MCTSAgent(iterations=5)
    agent.select_action(state)

if __name__ == "__main__":
    main()