from enum import Enum

from rlcard.calculator import parallel_holdem_calc as pc


class PlayerStatus(Enum):
    ALIVE = 0
    FOLDED = 1
    ALLIN = 2


class LimitHoldemPlayer:

    def __init__(self, player_id, np_random):
        """
        Initialize a player.

        Args:
            player_id (int): The id of the player
        """
        self.np_random = np_random
        self.player_id = player_id
        self.hand = []
        self.status = PlayerStatus.ALIVE
        self.amountOfTimesRaised = 0
        self.amountOfTimesAlin = 0
        self.amountOfTimesFolded = 0

        # The chips that this player has put in until now
        self.in_chips = 0

    def calculate_odds(self, public_cards):
        """
        Calculate the odds of winning the game

        Args:
            public_cards (list): A list of public cards that seen by all the players

        Returns:
            (float): The odds of winning the game
        """
        pass

    def newGet_state(self, public_cards, all_chips, legal_actions, stage):
        # pc.calculate(community_cards,exact,amountofsimulations,input_file,(hand1,hand2),printoutresults)
        odds = 0
        # pre-flop
        if stage == 0:
            odds = pc.calculate(None, True, 1, None, [self.hand[0], self.hand[1], "?", "?"], False)
        # flop
        elif stage == 1:
            odds = pc.calculate(public_cards, True, 1, None, [self.hand[0], self.hand[1], "?", "?"], False)
        # turn
        elif stage == 2:
            odds = pc.calculate(public_cards, True, 1, None, [self.hand[0], self.hand[1], public_cards[0], "?"], False)
        # river
        elif stage == 3:
            odds = pc.calculate(public_cards, True, 1, None, [self.hand[0], self.hand[1], public_cards[0], public_cards[1]], False)


        return {
            'hand': [c.get_index() for c in self.hand],
            'public_cards': [c.get_index() for c in public_cards],
            'all_chips': all_chips,
            'my_chips': self.in_chips,
            'legal_actions': legal_actions,
            'odds': odds[1]
        }

    def get_state(self, public_cards, all_chips, legal_actions):
        """
        Encode the state for the player

        Args:
            public_cards (list): A list of public cards that seen by all the players
            all_chips (int): The chips that all players have put in

        Returns:
            (dict): The state of the player
        """


        return {
            'hand': [c.get_index() for c in self.hand],
            'public_cards': [c.get_index() for c in public_cards],
            'all_chips': all_chips,
            'my_chips': self.in_chips,
            'legal_actions': legal_actions
        }

    def get_player_id(self):
        return self.player_id
