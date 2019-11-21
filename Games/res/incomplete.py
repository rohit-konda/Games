#!/usr/bin/env python
"""
Library for welfare games that depend on information constraints
"""

from Games.res.resource import DistResGame
from Games.basic import Game
from math import factorial
from numpy import exp


class InfoGame(ResourceGame):
    """ Resource game with incomplete information of other agent strategies """
    def __init__(self, players, strategies, r_m, infograph):
        ResourceGame.__init__(self, players, strategies, r_m)
        self.infograph = infograph  # list of [list of index of players] that a player can sense which action

    def evaluator(self, i, strategy):
        """ utility for the strategies for player with index i"""
        info = self.infograph[i]
        mod_str = [strategy[p] if j in info else () for j in range(self.n)]  # put modified stategy here
        return mod_str

    def U_i(self, i, strategy):
        """ utility for the strategy for player i"""
        mod_strategy = self.evaluator(i, strategy)
        return ResourceGame.U_i(i, mod_strategy)

