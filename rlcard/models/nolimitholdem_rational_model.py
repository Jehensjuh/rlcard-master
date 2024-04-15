import rlcard
from rlcard.models.model import Model
from enum import Enum

class Action(Enum):
    FOLD = 0
    CHECK_CALL = 1
    RAISE_HALF_POT = 2
    RAISE_POT = 3
    ALL_IN = 4

class NolimitholdemRationalAgentV1(object):
    ''' No-limit Texas Hold'em Rational Agent version 1
    '''

    def __init__(self):
        self.use_raw = True

    @staticmethod
    def step(state):
        ''' Predict the action when given raw state. A simple rule-based AI.
        Args:
            state (dict): Raw state from the game

        Returns:
            action (Action): Predicted action
        '''
        legal_actions = state['raw_legal_actions']
        state = state['raw_obs']
        hand = state['hand']
        public_cards = state['public_cards']
        action = Action.FOLD  # Default action is FOLD
        odds = state['odds']
        stage = state['stage']['name']

        # When having only 2 hand cards at the game start, choose fold to drop terrible cards
        if stage == 'PREFLOP':
            action = Action.CHECK_CALL
        else:
            if odds >= 0.800:
                action = Action.ALL_IN
            elif odds >= 0.700:
                action = Action.RAISE_POT
            elif odds >= 0.600:
                action = Action.RAISE_HALF_POT
            elif odds >= 0.400:
                action = Action.CHECK_CALL
            else:
                action = Action.FOLD

        if action not in legal_actions:
            # Adjust actions if they are not legal
            if action == Action.RAISE_HALF_POT:
                action = Action.CHECK_CALL
            elif action == Action.RAISE_POT:
                action = Action.CHECK_CALL
            elif action == Action.ALL_IN:
                action = Action.CHECK_CALL
            elif action == Action.CHECK_CALL:
                action = Action.FOLD

        return action

    def eval_step(self, state):
        ''' Step for evaluation. The same to step
        '''
        return self.step(state), []

class LimitholdemRuleModelV1(Model):
    ''' Limit Texas Hold'em Rule Model version 1
    '''

    def __init__(self):
        ''' Load pretrained model
        '''
        env = rlcard.make('no-limit-holdem')

        rule_agent = NolimitholdemRationalAgentV1()
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
