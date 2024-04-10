import json
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MaxNLocator

# Load the JSON file
with open('GameData.json', 'r') as json_file:
    data = json.load(json_file)

# Initialize dictionaries to store total "ALL_IN" counts for each player
player1_all_in_counts = {'ALL_IN': 0}
player2_all_in_counts = {'ALL_IN': 0}

# Iterate through the recorded actions for each game
for game_data in data['recorded_actions']:
    for action_data in game_data['actions']:
        if action_data['action']['name'] == 'ALL_IN':
            player = action_data['player']
            if player == 0:
                player1_all_in_counts['ALL_IN'] += 1
            elif player == 1:
                player2_all_in_counts['ALL_IN'] += 1

# Plot the total "ALL_IN" counts for each player
bar_width = 0.35
index = np.arange(len(player1_all_in_counts))

plt.bar(index, player1_all_in_counts.values(), bar_width, label='Player 1')
plt.bar(index + bar_width, player2_all_in_counts.values(), bar_width, label='Player 2')

# Set plot labels and title
plt.xlabel('Action')
plt.ylabel('Total Number of ALL_IN Actions')
plt.title('Total Number of ALL_IN Actions by Player')
plt.xticks(index + bar_width / 2, player1_all_in_counts.keys())
plt.legend()
plt.grid(True)

# Ensure y-axis ticks are integers
plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))

plt.show()
