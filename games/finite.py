#!/usr/bin/env python
"""

Author : Rohit Konda
Copyright (c) 2020 Rohit Konda. All rights reserved.
Licensed under the MIT License. See LICENSE file in the project root for full license information.


Defines a noncooperative game with a finite number of players and a finite number of actions

"""
from itertools import ff

class FiniteGame(Game):
    """
    Class definition for a finite player, finite strategy set game

    Attributes:
        players (list(str)): list defining a string label for each player i.
        N (int): number of players in the game.
        actions (list()): list of actions A_i for each player i.
        num_act (list(int)): list of number of actions for each player i.
        payoffs (list(array)): list of payoff arrays for each player i.
    """

    def __init__(self, players, actions, payoffs=None):
        Game.__init__(self, players, actions)
        self.N = len(players)
        self.num_act = [len(A_i) for A_i in actions]
        self.payoffs = payoffs
        self.eq = None
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

    def fill_payoffs(self):
        """ fill out payoff arrays using utility functions (if not given in construction)

        Returns:
            (list(array)): list of payoff arrays based on the output of the utility functions
        """
        payoffs = [None]*self.N
        for i in range(self.N):
            payoff_i = np.zeros(self.num_act)
            # generate all possible types of action indices
            for a in product(*[range(n_i) for n_i in self.num_act]):
                payoff_i[a] = self.U_i(i, list(a))
            payoffs[i] = payoff_i
        return payoffs

    def find_des(self):
        """ find dominated equilibria for the defined strategic form game
        through a brute force search through self.payoffs

        Raises:
            ValueError: if self.payoffs is None

        Returns:
            des (list(tuple)): list of all strictly dominated equilbria
        """
        if self.payoffs is None:
            raise ValueError('must set value of self.payoffs')
        pass

    def find_pnes(self):
        """ find pure nash equilibria for the defined strategic form game
        through a brute force search through self.payoffs

        Raises:
            ValueError: if self.payoffs is None

        Returns:
            pnes (list(tuple)): list of all pure nash equilibria
        """
        if self.payoffs is None:
            raise ValueError('must set value of self.payoffs')

        tolerance = 10**-8  # numerical tolerance for comparing floats
        # candidate pure nash equilibria
        cpnes = list(np.argwhere(self.payoffs[0] > np.amax(self.payoffs[0], 0) - tolerance))
        cpnes = [tuple(cpne) for cpne in cpnes]
        for i in range(1, self.N):
            pm = self.payoffs[i]
            for cpne in cpnes[:]:
                ind = cpne[:i] + (slice(None),) + cpne[i+1:]
                if pm[cpne] < np.max(pm[ind]) - tolerance:
                    cpnes.pop(cpnes.index(cpne))
        return cpnes