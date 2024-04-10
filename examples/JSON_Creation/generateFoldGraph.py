# Load the JSON file
import json

from matplotlib import pyplot as plt
from matplotlib.ticker import MaxNLocator

with open('GameData.json', 'r') as json_file:
    data = json.load(json_file)

    # Initialize variables to store the total "FOLD" counts for each player
    player1_fold_count = 0
    player2_fold_count = 0

    # Iterate through the recorded actions for each game
    for game_data in data['recorded_actions']:
        for action_data in game_data['actions']:  # Access 'actions' list in each game_data
            action_name = action_data['action']['name']  # Access 'action' dictionary in each action_data
            if action_name == 'FOLD':
                if action_data['player'] == 0:
                    player1_fold_count += 1
                elif action_data['player'] == 1:
                    player2_fold_count += 1

    # Plot the total "FOLD" counts for each player
    plt.bar(['Player 1', 'Player 2'], [player1_fold_count, player2_fold_count])
    plt.xlabel('Player')
    plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.ylabel('Total Number of FOLD Actions')
    plt.title('Total FOLD Actions by Player')
    plt.show()
