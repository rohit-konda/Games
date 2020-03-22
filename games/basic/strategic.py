class StrategicGame(FiniteGame):
    """
    Class definition for a classic strategic form game.

    Attributes:
        payoffs (list(array)): list of payoff arrays for each player i.
        players (Players): list defining a string label for each player i.
        actions (Actions): list of actions A_i for each player i.
    """

    def __init__(self, payoffs):
        players = players if players else [str(i) for i in range(len(payoffs))]
        actions = actions if actions else [[i for i in range(d)] for d in np.shape(payoffs[0])]
        Game.__init__(self, players, actions, payoffs)

    def U_i(self, i, a):
        """ utility function for player i,
        when all players play according to action a

        Args:
            i (int): which player to calculate payoff
            a (list(int)): list of which actions that each player plays

        Returns:
            (int): payoff to player i
        """
        return self.payoffs[i][tuple(a)]