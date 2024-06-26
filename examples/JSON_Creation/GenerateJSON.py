import json
import pprint

import torch
import rlcard
from rlcard.agents import RandomAgent
import numpy as np

from rlcard.games.nolimitholdem import Action


def play_games(num_games):
    # Load the trained model
    agent = torch.load('../experiments/no-limit-holdem_dqn_results/Rational/model.pth')

    # Make an environment for playing
    env = rlcard.make('no-limit-holdem', config={'seed': 42})

    all_trajectories = []

    for _ in range(num_games):
        agents = [agent] + [RandomAgent(num_actions=env.num_actions) for _ in range(env.num_players - 1)]
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
        elif isinstance(obj, np.int32):
            return int(obj)  # Convert np.int32 to Python int
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
                if isinstance(v, np.int64):
                    v = int(v)  # Convert numpy.int64 to Python int
                elif isinstance(v, np.int32):
                    v = int(v)
                else:
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
    game = 0  # Game counter
    counter = 0

    for player_trajectories in trajectories:
        game_actions[game] = []  # Initialize an empty list for each game
        temptransition = player_trajectories[0]
        recorded_action = temptransition.get('action_record')
        modified_recorded_action = [{'player': player_id, 'action': action} for player_id, action in recorded_action]
        recorded_actions.extend(modified_recorded_action)
        # Add recorded actions to the corresponding game_actions list
        game_actions[game].extend(modified_recorded_action)
        # Initialize list to store observations for each game
        raw_observations_per_game[game] = []
        for transition in player_trajectories:
            if isinstance(transition, dict):
                raw_observation = transition.get('raw_obs')
                if raw_observation is not None:
                    # Convert int32 arrays to Python lists and filter out 'pot'
                    raw_observation.pop('legal_actions', None)
                    raw_observation.pop('pot', None)
                    # raw_observation['game'] = game
                    raw_observation = convert_to_json_serializable(raw_observation)
                    # raw_observations.append(raw_observation)
                    raw_observations_per_game[game].append(raw_observation)

                # Extract myObs data
                myob = transition.get('myObs')
                myob = convert_to_json_serializable(myob)
                myObs = {}
                myObs['chips'] = myob['chips']
                myObs['total_chips'] = myob['total_chips']
                myObs['public_card'] = myob['public_card']
                myObs['hand_cards'] = myob['hand_cards']
                myObs['current_player'] = myob['current_player']
                myObs['odds'] = myob['odds']
                # Add myObs to the raw observation
                raw_observation['myObs'] = myObs

        counter += 1
        if counter % 2 == 0:
            game += 1

    grouped_recorded_actions = [{"game": game, "actions": actions} for game, actions in game_actions.items()]
    grouped_raw_observations = [{"game": game_num, "observations": observations} for game_num, observations in
                                raw_observations_per_game.items()]

    # Combine all data into a single dictionary
    combined_data = {
        "raw_observations": grouped_raw_observations,
        "legal_actions": legal_actions,
        "recorded_actions": grouped_recorded_actions
    }

    with open('TestData.json', 'w') as json_file:
        json.dump(combined_data, json_file, indent=4, cls=CustomEncoder)
