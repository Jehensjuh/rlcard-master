from rlcard.games.limitholdem import Player


class NolimitholdemPlayer(Player):
    def __init__(self, player_id, init_chips, np_random):
        """
        Initialize a player.

        Args:
            player_id (int): The id of the player
            init_chips (int): The number of chips the player has initially
        """
        super().__init__(player_id, np_random)
        self.timesFolded = 0
        self.timesRaised = 0
        self.timesAllIn = 0

        self.remained_chips = init_chips

    def bet(self, chips):
        quantity = chips if chips <= self.remained_chips else self.remained_chips
        self.in_chips += quantity
        self.remained_chips -= quantity

    def raised(self):
        self.timesRaised += 1

    def folded(self):
        self.timesFolded += 1

    def allIn(self):
        self.timesAllIn += 1

