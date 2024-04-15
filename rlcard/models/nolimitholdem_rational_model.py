import rlcard
from rlcard.models.model import Model

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
            action (int): Predicted action as a numerical value
        '''
        legal_actions = state['raw_legal_actions']
        state = state['raw_obs']
        hand = state['hand']
        public_cards = state['public_cards']
        action = 0  # Default action is FOLD
        odds = state['odds']
        stage = state['stage'].name
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


        # When having only 2 hand cards at the game start, choose fold to drop terrible cards
        if stage == 'PREFLOP':
            if actions['CHECK_CALL'] in legal_actions:
                action = actions['CHECK_CALL']
        else:
            if odds >= 0.800:
                action = actions['ALL_IN']
            elif odds >= 0.700:
                action = actions['RAISE_POT']
            elif odds >= 0.600:
                action = actions['RAISE_HALF_POT']
            elif odds >= 0.400:
                action = actions['CHECK_CALL']
            else:
                action = actions['FOLD']

        if action not in legal_actions:
            # Adjust actions if they are not legal
            if action == actions['RAISE_HALF_POT']:  # RAISE_HALF_POT
                action = actions['CHECK_CALL']  # CHECK_CALL
            elif action == actions['RAISE_POT']:  # RAISE_POT
                action = actions['CHECK_CALL']  # CHECK_CALL
            elif action == actions['ALL_IN']:  # ALL_IN
                action = actions['CHECK_CALL']  # CHECK_CALL
            elif action == actions['CHECK_CALL']:  # CHECK_CALL
                action = actions['FOLD']  # FOLD

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
