import os
import pprint
import random
import json
import os
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
def play_game():
    # Load the trained model
    agent = torch.load('C:/Users/jensv/OneDrive/Bureaublad/MasterProject/rlcard-master//examples/experiments/limit-holdem_dqn_results/20240322_130850/model.pth')

    # Generate a random seed value
    seed = random.randint(0, 1000)

    # Make an environment for playing
    env = rlcard.make('limit-holdem', config={'seed': seed})
    agents = [agent] + [RandomAgent(num_actions=env.num_actions) for _ in range(env.num_players - 1)]
    env.set_agents(agents)

    # Generate data from the environment
    trajectories, player_wins = env.run(is_training=False)
    # Print out the trajectories
    print('\nTrajectories:')
    print(trajectories)
    # print('\nSample raw observation:')
    # pprint.pprint(trajectories[0][0]['raw_obs'])
    # print('\nSample raw legal_actions:')
    # pprint.pprint(trajectories[0][0]['raw_legal_actions'])

    # Print out the trajectories with JSON serialization
    print('\nTrajectories:')
    print('\nTrajectories:')
    for player_id, player_trajectory in enumerate(trajectories):
        print(f"\nPlayer {player_id}'s Trajectory:")
        for round_idx, round_data in enumerate(player_trajectory):
            print(f"\nRound {round_idx + 1}:")
            print(round_data)

if __name__ == '__main__':
    play_game()