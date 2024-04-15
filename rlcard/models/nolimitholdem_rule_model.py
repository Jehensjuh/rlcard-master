import rlcard
from rlcard.models.model import Model

class UnlimitedHoldemRuleAgent(object):
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
            action (str): Predicted action
        '''
        legal_actions = state['raw_legal_actions']
        state = state['raw_obs']
        hand = state['hand']
        public_cards = state['public_cards']
        action = 'FOLD'

        # Calculate the strength of the hand
        hand_strength = calculate_hand_strength(hand, public_cards)

        # Decide actions based on the strength of the hand and current betting round
        if 'FOLD' in legal_actions:
            if hand_strength == 'HIGH_PAIR' or hand_strength == 'TWO_PAIR' or hand_strength == 'THREE_OF_A_KIND':
                action = 'RAISE_FULL_POT'  # Raise with strong hands
            elif hand_strength == 'STRAIGHT' or hand_strength == 'FLUSH' or hand_strength == 'FULL_HOUSE' or hand_strength == 'FOUR_OF_A_KIND':
                action = 'ALL_IN'  # Go all-in with very strong hands
            elif 'RAISE_FULL_POT' in legal_actions:
                action = 'RAISE_FULL_POT'  # Raise if possible
            else:
                action = 'CHECK_CALL'  # Otherwise, check or call

        return action

    def eval_step(self, state):
        ''' Step for evaluation. The same to step
        '''
        return self.step(state), []

# Helper function to calculate hand strength
def calculate_hand_strength(hand, public_cards):
    all_cards = hand + public_cards
    all_ranks = [card[1] for card in all_cards]
    all_suits = [card[0] for card in all_cards]

    if len(set(all_suits)) == 1:  # Flush
        return 'FLUSH'
    elif is_straight(all_ranks):  # Straight
        return 'STRAIGHT'
    elif len(set(all_ranks)) == 2:
        counts = [all_ranks.count(rank) for rank in set(all_ranks)]
        if 4 in counts:  # Four of a Kind
            return 'FOUR_OF_A_KIND'
        elif 3 in counts:  # Full House
            return 'FULL_HOUSE'
    elif len(set(all_ranks)) == 3:
        counts = [all_ranks.count(rank) for rank in set(all_ranks)]
        if 3 in counts:  # Three of a Kind
            return 'THREE_OF_A_KIND'
        elif counts.count(2) == 2:  # Two Pair
            return 'TWO_PAIR'
    elif len(set(all_ranks)) == 4 and max(all_ranks) == 'A':
        return 'HIGH_PAIR'
    return 'HIGH_CARD'

# Helper function to check if the cards form a straight
def is_straight(ranks):
    rank_values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
    sorted_ranks = sorted([rank_values[rank] for rank in ranks])
    straight = False
    if len(sorted_ranks) >= 5:
        for i in range(len(sorted_ranks) - 4):
            if sorted_ranks[i] + 4 == sorted_ranks[i + 4]:
                straight = True
                break
    return straight

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
