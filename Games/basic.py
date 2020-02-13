#!/usr/bin/env python
"""

Author : Rohit Konda

Defines the basic strategic form game construction
"""

import numpy as np
from itertools import product


class Game:
    """
    Class definition for the most basic form of a game.
    Parent class for all other game constructions.

    Attributes:
        players (list(str)): list defining a string label for each player i.
        actions (list(obj)): list of action sets A_i for each player i.
    """

    def __init__(self, players, actions, payoffs=None):
        self.players = players
        self.actions = actions

        self.check_game()

    def check_game(self):
        """ check if game construction is valid

        Raises:
            ValueError
        """
        raise NotImplementedError

    def U_i(self, i, a):
        """ utility function for player i,
        when all players play according to action a

        Args:
            i (int): which player to calculate payoff
            a (list(obj)): list of which actions that each player plays

        Returns:
            (obj): payoff to player i
        """
        raise NotImplementedError


class FiniteGame(Game):
    """
    Class definition for a finite player, finite strategy set game

    Attributes:
        players (list(str)): list defining a string label for each player i.
        N (int): number of players in the game.
        actions (list(list(obj))): list of actions A_i for each player i.
        num_act (list(int)): list of number of actions for each player i.
        payoffs (list(array)): list of payoff arrays for each player i.
        des (list(tuple)): list of all dominated equilibria (tuple of each player's strategy index a_i).
        pnes (list(tuple)): list of all pure nash equilibria (tuple of each player's strategy index a_i).
        mnes (list(array)): list of mixed nash equilibria (array defining prob distribution over strategy set A).
        ces (list(array)): list of correlated nash equilibria (array defining prob distribution over strategy set A).
        cces (list(array)): list of coarse correlated nash equilibria (array defining prob distribution over strategy set A).
    """

    def __init__(self, players, actions, payoffs=None):
        Game.__init__(self, players, actions)
        self.N = len(players)
        self.num_act = [len(A_i) for A_i in actions]
        self.payoffs = payoffs
        self.des = None
        self.pnes = None
        self.mnes = None
        self.ces = None
        self.cces = None

        self.check_game()

    def check_game(self):
        """ check if game construction is valid

        Raises:
            ValueError
        """
        if self.N != len(self.actions):
            raise ValueError('mismatch in number of self.players and A_i in self.actions')

        if self.payoffs and len(self.payoffs) != self.N:
            raise ValueError('mismatch in number of self.players and length of self.payoffs')

        if self.payoffs and list(np.shape(self.payoffs[0])) != self.num_act:
            raise ValueError('shape of payoff arrays must match self.num_act')

        if self.payoffs and any([np.shape(self.payoffs[0]) != np.shape(pay) for pay in self.payoffs]):
            raise ValueError('shape of arrays in self.payoffs must match each other')

    def set_payoffs(self):
        """ fill out payoff matrices using utility functions (if not given in construction)

        Note:
            setter method for self.payoffs
        """
        payoffs = [None]*self.N
        for i in range(self.N):
            payoff_i = np.zeros(self.num_act)
            # generate all possible types of action indices
            for a in product(*[range(n_i) for n_i in self.num_act]):
                payoff_i[a] = self.U_i(i, list(a))
            payoffs[i] = payoff_i
        self.payoffs = payoffs

    def set_des(self):
        """ find dominated equilibria for the defined strategic form game

        Note:
            setter method for self.mnes
        """
        pass

    def set_pnes(self):
        """ find pure nash equilibria for the defined strategic form game
        through a brute force search through self.payoffs

        Note:
            setter method for self.pnes

        Raises:
            ValueError: if self.payoffs is None
        """
        if self.payoffs is None:
            raise ValueError('must set value of self.payoffs')

        tolerance = 10**-8  # numerical tolerance for comparing floats
        # candidate pure nash equilibria
        cpnes = list(np.argwhere(self.payoffs[0] > np.amax(self.payoffs[0], 0) - tolerance))
        cpnes = [tuple(cpne) for cpne in cpnes]
        pnes = []
        for i in range(1, self.N):
            pm = self.payoffs[i]
            for cpne in cpnes[:]:
                ind = cpne[:i] + (slice(None),) + cpne[i+1:]
                if pm[cpne] < np.max(pm[ind]) - tolerance:
                    cpnes.pop(cpnes.index(cpne))
        self.pnes = cpnes

    def set_mnes(self):
        """ find mixed nash equilibria for the defined strategic form game

        Note:
            setter method for self.mnes
        """
        pass

    def set_ces(self):
        """ find correlated equilibria for the defined strategic form game

        Note:
            setter method for self.ces
        """
        pass

    def set_cces(self):
        """ find coarse correlated equilibria for the defined strategic form game

        Note:
            setter method for self.cces
        """
        pass


class StrategicGame(Game):
    """
    Class definition for a classic strategic form game.

    Attributes:
        payoffs (list(array)): list of payoff arrays for each player i.
        players (list(str)): list defining a string label for each player i.
        actions (list(list(obj))): list of actions A_i for each player i.
    """

    def __init__(self, payoffs, players=None, actions=None):
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
