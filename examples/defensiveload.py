import os
import pprint
import random
import json
import os
from datetime import datetime
from enum import Enum

import numpy as np
import torch
import rlcard
from rlcard.agents import RandomAgent
from rlcard.games.nolimitholdem import Action
from rlcard.utils import reorganize

def convert_to_json_serializable(obj):
    if isinstance(obj, Action):
        return obj.name  # Convert Action to its name
    elif isinstance(obj, np.int32):
        return int(obj)  # Convert int32 to regular Python integer
    return obj

class ActionEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Enum):
            return obj.value
        return super().default(obj)

def extract_information(trajectories):
    for player_trajectory in trajectories:
        for transition in player_trajectory:
            raw_obs = transition['raw_obs']
            action_record = transition['action_record']
            print(f"Chips: {raw_obs['my_chips']}")
            print(f"Stakes: {raw_obs['stakes']}")
            print(f"Recorded Actions: {[action[1] for action in action_record]}")
            print(f"Hand: {raw_obs['hand']}")
            print(f"Public Cards: {raw_obs['public_cards']}")

def save_to_file(trajectories, player_wins):
    # Get current date and time
    current_datetime = datetime.now()
    # Format the datetime as desired for the filename
    filename ="gameoutputs/defensive/"+ current_datetime.strftime("%Y%m%d_%H%M%S") + ".txt"
    # Write trajectories and player wins to the file
    with open(filename, 'w') as file:
        file.write("Trajectories:\n")
        file.write(pprint.pformat(trajectories))  # Write trajectories
        file.write("\n\nPlayer Wins:\n")
        file.write(pprint.pformat(player_wins))  # Write player wins

def play_game():
    # Load the trained model
    agent = torch.load('C:/Users/jensv/OneDrive/Bureaublad/MasterProject/rlcard-master//examples/experiments/no-limit-holdem-defensive_dqn_results/20240322_111905/model.pth')

    # Generate a random seed value
    seed = random.randint(0, 1000)

    # Make an environment for playing
    env = rlcard.make('no-limit-holdem', config={'seed': seed})
    agents = [agent] + [RandomAgent(num_actions=env.num_actions) for _ in range(env.num_players - 1)]
    env.set_agents(agents)

    # Generate data from the environment
    trajectories, player_wins = env.run(is_training=False)
    # Print out the trajectories
    print('\nTrajectories:')
    print(trajectories)
    print('\nPlayer wins:')
    print(player_wins)
    save_to_file(trajectories, player_wins)


if __name__ == '__main__':
    play_game()