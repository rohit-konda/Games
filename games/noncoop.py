#!/usr/bin/env python
"""

Author : Rohit Konda
Copyright (c) 2020 Rohit Konda. All rights reserved.
Licensed under the MIT License. See LICENSE file in the project root for full license information.

Summary:
    Class definition for the basic noncooperative game with finite players
"""

from games._abc import *


class NonCoopGame(Game):
    """
    Class definition for a finite player game

    Attributes:
        _players (list(Players)): list of players.
        _actions (list(set(Action))): list of actions sets for each player.
        _N (int): number of players in the game.
        _util (func): optional interface for assigning utility function.
    """

    def __init__(self, players, util=None):
        Game.__init__(self, players)
        self._N = len(players)
        self._actions = [p.actions for p in self.players]
        self._util = util

    def U(self, p, a):
        """ 
        utility function for player p,
        when all players play according to joint action a

        Args:
            p (Player): which player to calculate payoff
            a (set(Action)): joint action enacted by all of the players

        Raises:
            ValueError: if player p is not in the set of Players
            NotImplementedError: if self._util is not defined

        Returns:
            (obj): payoff object that should satisfy all of the von Neumann and Morgenstern axioms
        """
        Game.U(self, p, a)
        if self._util: 
            try:
                val = self._util(p, a)
            except Exception as e:
                raise e
            return val
        else:
            raise NotImplementedError('self._util was not set')


class StrategicGameFactory(GameFactory):
    """
    Creates a strategic form game based on a payoff matrix
    """

    def make_game(self, payoffs):
        """
        constructor for a strategic form game

        Args:
            payoffs (list(np.array)): list of payoff matrix for each player

        Raises:
            ValueError: if there is an error in construction

        Returns:
            (Game): A valid game construction
        """
        self._check_game(payoffs)

        players = self._make_players(payoffs)

        util = self._make_utility(payoffs)

        return NonCoopGame(players, util)

    def _make_players(self, payoffs):
        players = []
        for ind, dim in enumerate(np.shape(payoffs)):
            actions = [Action(str(ind) + str(i), i) for i in range(dim)] 
            players.append(Player(str(ind), ind, actions))
        return players

    def _make_utility(self, payoffs):
        class _util:
            def __init__(self, payoffs): self.payoffs = payoffs
            def __call__(self, p, a): return payoffs[p.name][tuple(a)]
        return _util(payoffs)

    def _check_game(self, payoffs):
        """
        check if game construction is valid

        Raises:
            ValueError: if game not valid.
        """
        if not [isinstance(pay, np.array) for pay in payoffs].all():
            raise ValueError('payoffs must be a numpy array')
        if not [shape(pay) == shape(payoffs[0]) for pay in payoffs].all(): 
            raise ValueError('payoff matrices must be the same shape')


class NCNashEq(NashEq):

    def __init__(self, ind):
        self.ind = ind


class NCEqFinder:

    def __init__(self, game, payoffs=None):
        self.game = game
        self.payoffs = payoffs
        self.eq = []


    def set_payoffs(self):
        """ generate payoff arrays using utility functions (if not given in construction)

        Returns:
            (list(array)): list of payoff arrays based on the output of the utility functions
        """
        payoffs = [None]*self.N
        for i in range(self.N):
            payoff_i = np.zeros(self.num_act)
            # generate all possible types of action indices
            for a in product(*[range(n_i) for n_i in self.num_act]):
                payoff_i[a] = self.U(i, list(a))
            payoffs[i] = payoff_i
        self.payoffs = payoffs

    def find_eq(self):
        pass


class NCNashFinder(NCEqFinder):

    def __init__(self, game, payoffs=None):
        self.game = game
        self.payoffs = payoffs
        self.eq = []

    def find_eq(self):
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
        
        self.eq = cpnes