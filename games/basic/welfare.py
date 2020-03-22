#!/usr/bin/env python
"""

Author : Rohit Konda

Defines welfare games, i.e. games that have a welfare function
that is dependent on player strategies
"""

from games.basic import Game, FiniteGame


class WelfareGame(Game):
    """
    Class definition for a welfare game, endowed with a welfare function

    Attributes:
        players (list(str)): list defining a string label for each player i.
        actions (list(obj)): list of action sets A_i for each player i.
    """
    def __init__(self, players, actions):
        Game.__init__(self, players, actions, payoffs)

    def welfare(self, a):
        """ welfare function when all players play according to action a

        Args:
            a (list(int)): list of which actions that each player plays

        Returns:
            (obj): social welfare value
        """
        raise NotImplementedError


class PotentialGame(WelfareGame):
    """
    Class definition for a potential game,
    endowed with a welfare function and a potential function

    Attributes:
        players (list(str)): list defining a string label for each player i.
        actions (list(obj)): list of action sets A_i for each player i.
    """
    def __init__(self, players, actions):
        WelfareGame.__init__(self, players, actions, payoffs)

    def potential(self, a):
        """ potential function when all players play according to action a

        Args:
            a (list(int)): list of which actions that each player plays

        Returns:
            (obj): potential function value
        """
        raise NotImplementedError


class FiniteWelfareGame(FiniteGame, WelfareGame):
    """
    Class definition for a finite player, finite strategy welfare game

    Attributes:
        players (list(str)): list defining a string label for each player i.
        actions (list(list(obj))): list of actions A_i for each player i.
        payoffs (list(array)): list of payoff matrices for each player i.
        welfare (array): array determining welfare for each action
        opt (tuple): index of an action that maximizes welfare
        poa (float): price of anarchy value
        pos (float): price of stability value
    """

    def __init__(self, players, actions, payoffs=None):
        Game.__init__(self, players, actions, payoffs)
        self.welfare = None
        self.opt = None
        self.poa = None
        self.pos = None

    def set_welfare(self):
        """ fill out welfare array using welfare function

        Note:
            setter method for self.welfare
        """
        pass

    def set_opt(self):
        """ find action that maximizes welfare

        Note:
            setter method for self.opt

        Raises:
            ValueError: if self.welfare is None
        """
        if self.welfare is None:
            raise ValueError('must set value of self.welfare')

        self.opt = np.unravel_index(np.argmax(self.welfare), self.welfare.shape)

    def set_poas(self):
        """ calculate price of anarchy and price of stability
        from all pure nash and social optimum

        Note:
            setter method for self.poa & self.pos

        Raises:
            ValueError: if self.welfare or self.pnes is None
        """
        if self.welfare is None:
            raise ValueError('must set value of self.welfare')

        if self.pnes is None:
            raise ValueError('must set value of self.pnes')

        pne_welfare = np.array([self.welfare[pne] for pne in self.pnes], dtype='float')
        price_ratios = list(pne_welfare/self.welfare[self.opt])
        self.poa, pos = min(price_ratios), max(price_ratios)
