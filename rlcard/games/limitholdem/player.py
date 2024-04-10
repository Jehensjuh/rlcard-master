from enum import Enum

from rlcard.calculator import parallel_holdem_calc as pc


class PlayerStatus(Enum):
    ALIVE = 0
    FOLDED = 1
    ALLIN = 2


class Stage(Enum):
    PREFLOP = 0
    FLOP = 1
    TURN = 2
    RIVER = 3
    END_HIDDEN = 4
    SHOWDOWN = 5


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
        odds = []
        public_cards_s = []
        # create a list of the strings of the public cars
        if public_cards:
            public_cards_s = [c.get_index() for c in public_cards]

        # pre-flop
        # if stage == stage.PREFLOP:
        #     odds = pc.calculate(None, True, 1, None, [self.hand[0].get_index(), self.hand[1].get_index(), "?", "?"],
        #                         False)
        # flop
        if stage == stage.FLOP:
            odds = pc.calculate(public_cards_s, True, 1, None,
                                [self.hand[0].get_index(), self.hand[1].get_index(), "?", "?"], False)
        # turn
        elif stage == stage.TURN:
            odds = pc.calculate(public_cards_s, True, 1, None,
                                [self.hand[0].get_index(), self.hand[1].get_index(), "?", "?"], False)
        # river
        elif stage == stage.RIVER:
            odds = pc.calculate(public_cards_s, True, 1, None,
                                [self.hand[0].get_index(), self.hand[1].get_index(), "?", "?"], False)

        return {
            'hand': [c.get_index() for c in self.hand],
            'public_cards': [c.get_index() for c in public_cards],
            'all_chips': all_chips,
            'my_chips': self.in_chips,
            'legal_actions': legal_actions,
            'odds': odds
        }

    def newGet_state_training(self, public_cards, all_chips, legal_actions, stage, opponent_hand):
        # pc.calculate(community_cards,exact,amountofsimulations,input_file,(hand1,hand2),printoutresults)
        odds = []
        public_cards_s = []
        # create a list of the strings of the public cars
        if public_cards:
            public_cards_s = [c.get_index() for c in public_cards]

        # pre-flop
        if stage == stage.PREFLOP:
            odds = pc.calculate(None, True, 1, None, [self.hand[0].get_index(), self.hand[1].get_index(), opponent_hand[0][0].get_index(),  opponent_hand[0][1].get_index()],
                                 False)
        # flop
        if stage == stage.FLOP:
            odds = pc.calculate(public_cards_s, True, 1, None,
                                [self.hand[0].get_index(), self.hand[1].get_index(), opponent_hand[0][0].get_index(),  opponent_hand[0][1].get_index()], False)
        # turn
        elif stage == stage.TURN:
            odds = pc.calculate(public_cards_s, True, 1, None,
                                [self.hand[0].get_index(), self.hand[1].get_index(), opponent_hand[0][0].get_index(),  opponent_hand[0][1].get_index()], False)
        # river
        elif stage == stage.RIVER:
            odds = pc.calculate(public_cards_s, True, 1, None,
                                [self.hand[0].get_index(), self.hand[1].get_index(), opponent_hand[0][0].get_index(),  opponent_hand[0][1].get_index()], False)

        return {
            'hand': [c.get_index() for c in self.hand],
            'public_cards': [c.get_index() for c in public_cards],
            'all_chips': all_chips,
            'my_chips': self.in_chips,
            'legal_actions': legal_actions,
            'odds': odds
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
