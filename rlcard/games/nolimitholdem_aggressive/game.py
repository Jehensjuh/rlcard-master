from enum import Enum

import numpy as np
from copy import deepcopy
from rlcard.games.limitholdem import Game
from rlcard.games.limitholdem import PlayerStatus

from rlcard.games.nolimitholdem_aggressive import Dealer
from rlcard.games.nolimitholdem_aggressive import Player
from rlcard.games.nolimitholdem_aggressive import Judger
from rlcard.games.nolimitholdem_aggressive import Round, Action

from rlcard.calculator import parallel_holdem_calc as pc


class Stage(Enum):
    PREFLOP = 0
    FLOP = 1
    TURN = 2
    RIVER = 3
    END_HIDDEN = 4
    SHOWDOWN = 5


class NolimitholdemGame(Game):
    def __init__(self, allow_step_back=False, num_players=2):
        """Initialize the class no limit holdem Game"""
        super().__init__(allow_step_back, num_players)

        self.np_random = np.random.RandomState()

        # small blind and big blind
        self.small_blind = 1
        self.big_blind = 2 * self.small_blind

        # config players
        self.init_chips = [100] * num_players

        # If None, the dealer will be randomly chosen
        self.dealer_id = None

    def configure(self, game_config):
        """
        Specify some game specific parameters, such as number of players, initial chips, and dealer id.
        If dealer_id is None, he will be randomly chosen
        """
        self.num_players = game_config['game_num_players']
        # must have num_players length
        self.init_chips = [game_config['chips_for_each']] * game_config["game_num_players"]
        self.dealer_id = game_config['dealer_id']

    def init_game(self):
        """
        Initialize the game of not limit holdem

        This version supports two-player no limit texas holdem

        Returns:
            (tuple): Tuple containing:

                (dict): The first state of the game
                (int): Current player's id
        """
        if self.dealer_id is None:
            self.dealer_id = self.np_random.randint(0, self.num_players)

        # Initialize a dealer that can deal cards
        self.dealer = Dealer(self.np_random)

        # Initialize players to play the game
        self.players = [Player(i, self.init_chips[i], self.np_random) for i in range(self.num_players)]

        # Initialize a judger class which will decide who wins in the end
        self.judger = Judger(self.np_random)

        # Deal cards to each  player to prepare for the first round
        for i in range(2 * self.num_players):
            self.players[i % self.num_players].hand.append(self.dealer.deal_card())

        # Initialize public cards
        self.public_cards = []
        self.stage = Stage.PREFLOP

        # Big blind and small blind
        s = (self.dealer_id + 1) % self.num_players
        b = (self.dealer_id + 2) % self.num_players
        self.players[b].bet(chips=self.big_blind)
        self.players[s].bet(chips=self.small_blind)

        # The player next to the big blind plays the first
        self.game_pointer = (b + 1) % self.num_players

        # Initialize a bidding round, in the first round, the big blind and the small blind needs to
        # be passed to the round for processing.
        self.round = Round(self.num_players, self.big_blind, dealer=self.dealer, np_random=self.np_random)

        self.round.start_new_round(game_pointer=self.game_pointer, raised=[p.in_chips for p in self.players])

        # Count the round. There are 4 rounds in each game.
        self.round_counter = 0

        # Save the history for stepping back to the last state.
        self.history = []

        state = self.get_state(self.game_pointer)

        return state, self.game_pointer

    def get_legal_actions(self):
        """
        Return the legal actions for current player

        Returns:
            (list): A list of legal actions
        """
        return self.round.get_nolimit_legal_actions(players=self.players)

    def step(self, action):
        """
        Get the next state

        Args:
            action (str): a specific action. (call, raise, fold, or check)

        Returns:
            (tuple): Tuple containing:

                (dict): next player's state
                (int): next player id
        """

        if action not in self.get_legal_actions():
            print(action, self.get_legal_actions())
            print(self.get_state(self.game_pointer))
            raise Exception('Action not allowed')

        if self.allow_step_back:
            # First snapshot the current state
            r = deepcopy(self.round)
            b = self.game_pointer
            r_c = self.round_counter
            d = deepcopy(self.dealer)
            p = deepcopy(self.public_cards)
            ps = deepcopy(self.players)
            self.history.append((r, b, r_c, d, p, ps))

        # Then we proceed to the next round
        self.game_pointer = self.round.proceed_round(self.players, action)

        players_in_bypass = [1 if player.status in (PlayerStatus.FOLDED, PlayerStatus.ALLIN) else 0 for player in self.players]
        if self.num_players - sum(players_in_bypass) == 1:
            last_player = players_in_bypass.index(0)
            if self.round.raised[last_player] >= max(self.round.raised):
                # If the last player has put enough chips, he is also bypassed
                players_in_bypass[last_player] = 1

        # If a round is over, we deal more public cards
        if self.round.is_over():
            # Game pointer goes to the first player not in bypass after the dealer, if there is one
            self.game_pointer = (self.dealer_id + 1) % self.num_players
            if sum(players_in_bypass) < self.num_players:
                while players_in_bypass[self.game_pointer]:
                    self.game_pointer = (self.game_pointer + 1) % self.num_players

            # For the first round, we deal 3 cards
            if self.round_counter == 0:
                self.stage = Stage.FLOP
                self.public_cards.append(self.dealer.deal_card())
                self.public_cards.append(self.dealer.deal_card())
                self.public_cards.append(self.dealer.deal_card())
                if len(self.players) == np.sum(players_in_bypass):
                    self.round_counter += 1
            # For the following rounds, we deal only 1 card
            if self.round_counter == 1:
                self.stage = Stage.TURN
                self.public_cards.append(self.dealer.deal_card())
                if len(self.players) == np.sum(players_in_bypass):
                    self.round_counter += 1
            if self.round_counter == 2:
                self.stage = Stage.RIVER
                self.public_cards.append(self.dealer.deal_card())
                if len(self.players) == np.sum(players_in_bypass):
                    self.round_counter += 1

            self.round_counter += 1
            self.round.start_new_round(self.game_pointer)

        state = self.get_state(self.game_pointer)

        return state, self.game_pointer

    def calculate_odds(self):
        player_hands = [player.hand for player in self.players]
        public_cards = self.public_cards
        odds = []
        public_cards_s = []
        stage = self.stage
        # create a list of the strings of the public cars
        if public_cards:
            public_cards_s = [c.get_index() for c in public_cards]

        # pre-flop
        if stage == stage.PREFLOP:
            odds = pc.calculate(None, True, 1, None, [player_hands[0][0].get_index(), player_hands[0][1].get_index(), player_hands[1][0].get_index(),  player_hands[1][1].get_index()],
                                 False)
        # flop
        if stage == stage.FLOP:
            odds = pc.calculate(public_cards_s, True, 1, None,
                                [player_hands[0][0].get_index(), player_hands[0][1].get_index(), player_hands[1][0].get_index(),  player_hands[1][1].get_index()], False)
        # turn
        elif stage == stage.TURN:
            odds = pc.calculate(public_cards_s, True, 1, None,
                                [player_hands[0][0].get_index(), player_hands[0][1].get_index(), player_hands[1][0].get_index(),  player_hands[1][1].get_index()], False)
        # river
        elif stage == stage.RIVER:
            odds = pc.calculate(public_cards_s, True, 1, None,
                                [player_hands[0][0].get_index(), player_hands[0][1].get_index(), player_hands[1][0].get_index(),  player_hands[1][1].get_index()], False)
        return odds

    def get_state(self, player_id):
        """
        Return player's state

        Args:
            player_id (int): player id

        Returns:
            (dict): The state of the player
        """
        # test
        self.dealer.pot = np.sum([player.in_chips for player in self.players])

        chips = [self.players[i].in_chips for i in range(self.num_players)]
        legal_actions = self.get_legal_actions()
        state = self.players[player_id].get_state(self.public_cards, chips, legal_actions)
        state['stakes'] = [self.players[i].remained_chips for i in range(self.num_players)]
        state['current_player'] = self.game_pointer
        state['pot'] = self.dealer.pot
        state['stage'] = self.stage
        return state

    def step_back(self):
        """
        Return to the previous state of the game{

        Returns:
            (bool): True if the game steps back successfully
        """
        if len(self.history) > 0:
            self.round, self.game_pointer, self.round_counter, self.dealer, self.public_cards, self.players = self.history.pop()
            self.stage = Stage(self.round_counter)
            return True
        return False

    def get_num_players(self):
        """
        Return the number of players in no limit texas holdem

        Returns:
            (int): The number of players in the game
        """
        return self.num_players

    def get_payoffs(self):
        """
        Return the payoffs of the game

        Returns:
            (list): Each entry corresponds to the payoff of one player
        """
        hands = [p.hand + self.public_cards if p.status in (PlayerStatus.ALIVE, PlayerStatus.ALLIN) else None for p in self.players]
        chips_payoffs = self.judger.judge_game(self.players, hands)
        return chips_payoffs


    def risky_reward(self):
        """
        Reward function to incentivize raising more often and folding less often
        """

        hands = [p.hand + self.public_cards if p.status in (PlayerStatus.ALIVE, PlayerStatus.ALLIN) else None for p in
                 self.players]
        chips_payoffs = self.judger.judge_game(self.players, hands)
        chips_won_or_lost = np.array(chips_payoffs)

        # Calculate the reward based on chips won or lost compared to the big blind
        rewards = chips_won_or_lost / self.big_blind

        # Define parameters for adjusting rewards
        fold_penalty = 0
        raise_reward = 0
        allin_reward = 0
        max_reward = 30
        min_reward = -30
        max_penalty = -0.5  # Maximum penalty for folding
        fold_penalty_factor = 0.5  # Adjust this factor to control the severity of fold penalty
        raise_reward_factor = 10  # Adjust this factor to control the reward for raising


        # Fold penalty
        # fold_penalty = [min(p.timesFolded * fold_penalty_factor / (self.round_counter + 1), max_penalty) for p in
        #                 self.players]

        for idx, p in enumerate(self.players):
            if p.timesFolded > 0:
                fold_penalty = -10
            elif p.timesFolded == 0:
                fold_penalty = 5 # positive reward because they didn't fold

            # Raise reward
            # raise_reward = [min(p.amountOfTimesRaised * raise_reward_factor / self.dealer.pot, max_reward) for p in
            #                 self.players]
            if p.amountOfTimesRaised > 0:
                raise_reward = 15*p.amountOfTimesRaised
                if p.timesAllIn > 0:
                    allin_reward = 5
            elif p.amountOfTimesRaised == 0:
                raise_reward = -5 # negative reward because they didn't raise
                if p.timesAllIn > 0:
                    allin_reward = 2
            rewards[idx] += fold_penalty + raise_reward + allin_reward


        # Normalize rewards
       #  rewards = np.clip(rewards, min_reward, max_reward)

        return rewards


    @staticmethod
    def get_num_actions():
        """
        Return the number of applicable actions

        Returns:
            (int): The number of actions. There are 6 actions (call, raise_half_pot, raise_pot, all_in, check and fold)
        """
        return len(Action)
