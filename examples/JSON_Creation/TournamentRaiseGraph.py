import json
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

# Load the JSON file containing recorded actions
with open('C:/Users/jensv/OneDrive/Bureaublad/MasterProject/rlcard-master/examples/JSON_Creation/TournamentData.json', 'r') as json_file:
    data = json.load(json_file)

# Initialize lists to store raise counts for each player in each game
player1_raise_counts = []
player2_raise_counts = []

# Iterate through the recorded actions for each game
for game_data in data['recorded_actions']:
    player1_raise_count = 0
    player2_raise_count = 0
    for action_data in game_data['actions']:
        action_name = action_data['action']['name']
        if action_name in ['RAISE_POT', 'RAISE_HALF_POT']:
            if action_data['player'] == 0:
                player1_raise_count += 1
            elif action_data['player'] == 1:
                player2_raise_count += 1
    player1_raise_counts.append(player1_raise_count)
    player2_raise_counts.append(player2_raise_count)

# Plot the raise counts for each player
plt.plot(range(1, len(player1_raise_counts) + 1), player1_raise_counts, label='Aggressive agent')
plt.plot(range(1, len(player2_raise_counts) + 1), player2_raise_counts, label='Rational agent')

# Set plot labels and title
plt.xlabel('Game Number')
plt.ylabel('Number of Raise Actions')
plt.title('Raise Actions by Player and Game')
plt.legend()
plt.grid(True)
# Adjust x-axis to show only natural numbers
# plt.xticks(range(1, len(player1_raise_counts) + 1))
plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
plt.show()
