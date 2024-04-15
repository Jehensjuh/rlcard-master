''' Limit Hold 'em rule model
'''
import rlcard
from rlcard.models.model import Model

class NolimitholdemRuleAggressiveAgent(object):
    ''' Limit Hold 'em Rule agent version 1
    '''

    def __init__(self):
        self.use_raw = True

    @staticmethod
    def step(state):
        ''' Predict the action when given raw state. A simple rule-based AI.
        Args:
            state (dict): Raw state from the game

        Returns:
            action (str): Predicted action
        '''
        legal_actions = state['raw_legal_actions']
        state = state['raw_obs']
        hand = state['hand']
        public_cards = state['public_cards']
        action = 'fold'
        odds = state['odds']
        stage = state['stage']['name']
        # When having only 2 hand cards at the game start, choose fold to drop terrible cards:
        # Acceptable hand cards:
        # Pairs
        # AK, AQ, AJ, AT
        # A9s, A8s, ... A2s(s means flush)
        # KQ, KJ, QJ, JT
        # Fold all hand types except those mentioned above to save money
        if stage == 'PREFLOP':
            action = 'CHECK_CALL'
        else:
            if odds >= 0.700:
                action = 'ALL_IN'
            if odds >= 0.500:
                action = 'RAISE_FULL_POT'
            if odds >= 0.400:
                action = 'RAISE_HALF_POT'
            if odds >= 0.100:
                action = 'CHECK_CALL'
            if odds < 0.100:
                action = 'FOLD'
        #return action
        if action in legal_actions:
            return action
        else:
            if action == 'RAISE_HALF_POT':
                return 'CHECK_CALL'
            elif action == 'RAISE_FULL_POT':
                return 'CHECK_CALL'
            elif action == 'ALL_IN':
                return 'CHECK_CALL'
            elif action == 'CHECK_CALL':
                return 'FOLD'
            else:
                return action

    def eval_step(self, state):
        ''' Step for evaluation. The same to step
        '''
        return self.step(state), []

class LimitholdemRuleModelV1(Model):
    ''' Limitholdem Rule Model version 1
    '''

    def __init__(self):
        ''' Load pretrained model
        '''
        env = rlcard.make('no-limit-holdem-defensive')

        rule_agent = NolimitholdemRuleAggressiveAgent()
        self.rule_agents = [rule_agent for _ in range(env.num_players)]

    @property
    def agents(self):
        ''' Get a list of agents for each position in a the game

        Returns:
            agents (list): A list of agents

        Note: Each agent should be just like RL agent with step and eval_step
              functioning well.
        '''
        return self.rule_agents

    @property
    def use_raw(self):
        ''' Indicate whether use raw state and action

        Returns:
            use_raw (boolean): True if using raw state and action
        '''
        return True
