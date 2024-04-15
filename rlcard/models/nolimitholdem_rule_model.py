import rlcard
from rlcard.models.model import Model
from enum import Enum

class Action(Enum):
    FOLD = 0
    CHECK_CALL = 1
    RAISE_HALF_POT = 2
    RAISE_POT = 3
    ALL_IN = 4

class UnlimitedHoldemRuleAgentV1(object):
    ''' Unlimited Texas Hold'em Rule agent version 1
    '''

    def __init__(self):
        self.use_raw = True

    @staticmethod
    def step(state):
        ''' Predict the action when given raw state. A simple rule-based AI.
        Args:
            state (dict): Raw state from the game

        Returns:
            action (int): Predicted action as a numerical value
        '''

        legal_actions = state['raw_legal_actions']
        actions = {}
        for action in legal_actions:
            if action.name == 'FOLD':
                actions['FOLD'] = action
            elif action.name == 'CHECK_CALL':
                actions['CHECK_CALL'] = action
            elif action.name == 'RAISE_HALF_POT':
                actions['RAISE_HALF_POT'] = action
            elif action.name == 'RAISE_POT':
                actions['RAISE_POT'] = action
            elif action.name == 'ALL_IN':
                actions['ALL_IN'] = action
        state = state['raw_obs']
        hand = state['hand']
        public_cards = state['public_cards']
        action = actions['FOLD']  # Default action is FOLD


        # Calculate the strength of the hand
        hand_strength = calculate_hand_strength(hand, public_cards)

        # Decide actions based on the strength of the hand and current betting round
        if actions['FOLD'] in legal_actions:
            if hand_strength == 'HIGH_PAIR' or hand_strength == 'TWO_PAIR' or hand_strength == 'THREE_OF_A_KIND':
                action = actions['RAISE_POT']  # Raise with strong hands
            elif hand_strength == 'STRAIGHT' or hand_strength == 'FLUSH' or hand_strength == 'FULL_HOUSE' or hand_strength == 'FOUR_OF_A_KIND':
                action = actions['ALL_IN']  # Go all-in with very strong hands
            elif Action.RAISE_POT.value in legal_actions:
                action = actions['RAISE_HALF_POT']  # Raise if possible
            else:
                action = actions['CHECK_CALL']  # Otherwise, check or call

        if action not in legal_actions:
            # Adjust actions if they are not legal
            if action == actions['RAISE_HALF_POT']:
                action = actions['CHECK_CALL']
            elif action == actions['RAISE_POT']:
                action = actions['CHECK_CALL']
            elif action == actions['ALL_IN']:
                action = actions['CHECK_CALL']
            elif action == actions['CHECK_CALL']:
                action = actions['FOLD']

        return action


    def eval_step(self, state):
        ''' Step for evaluation. The same to step
        '''
        return self.step(state), []

# Helper function to calculate hand strength
def calculate_hand_strength(hand, public_cards):
    # Implement your hand strength calculation logic here
    pass

class UnlimitedHoldemRuleModelV1(Model):
    ''' Unlimited Texas Hold'em Rule Model version 1
    '''

    def __init__(self):
        ''' Load pretrained model
        '''
        env = rlcard.make('no-limit-holdem')

        rule_agent = UnlimitedHoldemRuleAgentV1()
        self.rule_agents = [rule_agent for _ in range(env.num_players)]

    @property
    def agents(self):
        ''' Get a list of agents for each position in the game

        Returns:
            agents (list): A list of agents

        Note: Each agent should be just like RL agent with step and eval_step
              functioning well.
        '''
        return self.rule_agents

    @property
    def use_raw(self):
        ''' Indicate whether to use raw state and action

        Returns:
            use_raw (boolean): True if using raw state and action
        '''
        return True
