import json
import pprint

import torch
import rlcard
from rlcard.agents import RandomAgent
import numpy as np

from rlcard.games.nolimitholdem import Action

# elif isinstance(data, dict):
# converted_dict = {}
# for k, v in data.items():
#     if k == 'my_chips':  # Check for 'my_chips' key
#         if isinstance(v, np.int32):
#             v = int(v)  # Convert int32 numpy scalar to Python int

def play_games(num_games):
    # Load the trained model
    agent1 = torch.load('C:/Users/jensv/OneDrive/Bureaublad/MasterProject/rlcard-master/examples/experiments/no-limit-holdem-aggressive_dqn_results/20240328_152907/model.pth') # aggressive agent
    agent2 = torch.load('C:/Users/jensv/OneDrive/Bureaublad/MasterProject/rlcard-master/examples/experiments/no-limit-holdem_dqn_results/Rational/model.pth') # aggressive agent
    # Make an environment for playing
    env = rlcard.make('no-limit-holdem', config={'seed': 167})

    all_trajectories = []

    for _ in range(num_games):
        agents = [agent1, agent2]
        env.set_agents(agents)

        # Generate data from the environment
        trajectories, player_wins = env.run(is_training=False)

        all_trajectories.extend(trajectories)

    return all_trajectories



class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, rlcard.games.nolimitholdem.game.Stage):
            return {'name': obj.name, 'value': obj.value}
        elif isinstance(obj, tuple) and len(obj) == 2 and isinstance(obj[1], Action):
            player_id, action = obj
            return {'player': player_id, 'action': {'name': action.name, 'value': action.value}}
        elif isinstance(obj, Action):
            return {'name': obj.name, 'value': obj.value}
        return super().default(obj)


def convert_to_json_serializable(data):
    if isinstance(data, np.ndarray):
        if data.dtype == np.int32:
            return int(data.item())  # Convert int32 numpy array to Python int
        elif data.dtype == np.float32:
            return float(data.item())  # Convert float32 numpy array to Python float
    elif isinstance(data, dict):
        converted_dict = {}
        for k, v in data.items():
            if k == 'my_chips' and isinstance(v, np.int32):  # Check for 'my_chips' key
                 v = int(v)  # Convert int32 numpy scalar to Python int

            if k == 'all_chips':  # Check for specific keys
                v = [int(item) if isinstance(item, np.int32) else item for item in v]

            if k == 'stakes':
                if isinstance(v, np.ndarray):
                    v = v.astype(int).tolist()  # Convert int32 numpy array to Python int list
                else:
                    v = [int(item) if isinstance(item, np.int32) else item for item in v]

            if isinstance(v, np.ndarray):
                if v.dtype == np.int32:
                    converted_dict[k] = v.astype(int).tolist()  # Convert int32 numpy array to Python int list
                elif v.dtype == np.float32:
                    converted_dict[k] = v.astype(float).tolist()  # Convert float32 numpy array to Python float list
                else:
                    converted_dict[k] = v.tolist() if isinstance(v, np.ndarray) else v
            else:
                converted_dict[k] = convert_to_json_serializable(v)
        return converted_dict
    elif isinstance(data, list):
        return [convert_to_json_serializable(item) for item in data]
    return data





if __name__ == '__main__':
    # Play 10 games and get trajectories
    trajectories = play_games(10)

    # Extract raw observations from trajectories
    raw_observations = []
    legal_actions = []
    recorded_actions = []
    game_actions = {}
    # Initialize a dictionary to store raw observations per game
    raw_observations_per_game = {}
    game = 0 # Game counter
    counter = 0

    for player_trajectories in trajectories:
        game_actions[game] = []  # Initialize an empty list for each game
        temptransition = player_trajectories[0]
        recorded_action = temptransition.get('action_record')
        #         if recorded_action is not None:
        #             recorded_actions.append(
        #                 [{'player': player_id, 'action': action} for player_id, action in recorded_action])
        # Append game information to each recorded action dictionary
        # Append game information to each recorded action dictionary
        modified_recorded_action = [{'player': player_id, 'action': action} for player_id, action in recorded_action]
        recorded_actions.extend(modified_recorded_action)
        # Add recorded actions to the corresponding game_actions list
        game_actions[game].extend(modified_recorded_action)
        for transition in player_trajectories:
            if isinstance(transition, dict):
                raw_observation = transition.get('raw_obs')
                if raw_observation is not None:
                    # Convert int32 arrays to Python lists and filter out 'pot'
                    raw_observation['game'] = game
                    raw_observation.pop('legal_actions', None)
                    raw_observation.pop('pot', None)
                    raw_observation = convert_to_json_serializable(raw_observation)
                    raw_observations.append(raw_observation)


                legal_action = transition.get('raw_legal_actions')
                if legal_action is not None:
                    legal_actions.append(legal_action)
        counter += 1
        if(counter % 2 == 0):
            game += 1
    grouped_recorded_actions = [{"game": game, "actions": actions} for game, actions in game_actions.items()]
    # Combine all data into a single dictionary
    combined_data = {
        "raw_observations": raw_observations,
        "legal_actions": legal_actions,
 #       "recorded_actions": recorded_actions
        "recorded_actions": grouped_recorded_actions
    }

    with open('C:/Users/jensv/OneDrive/Bureaublad/MasterProject/rlcard-master/examples/JSON_Creation/TournamentData.json', 'w') as json_file:
        json.dump(combined_data, json_file, indent=4, cls=CustomEncoder)
