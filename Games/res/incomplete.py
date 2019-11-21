#!/usr/bin/env python
"""
Library for welfare games that depend on information constraints
"""

from Games.res.resource import *
from Games.basic import Game
from math import factorial
from numpy import exp


class InfoGame(Game):
    """ Resource game with incomplete information of other agent strategies """
    def __init__(self, players, strategies, infograph):
        Game.__init__(self, None, players, strategies)
        self.infograph = infograph  # list of [list of index of players] that a player can sense which action

    def evaluator(self, i, strategy):
        """ evaluator function returns a modified strategy based on limited information"""
        pass

    def U_i(self, i, strategy):
        """ utility for the strategy for player with index i"""
        mod_strategy = self.evaluator(i, strategy)
        return Game.U_i(self, i, mod_strategy)

class DistInfoGame(InfoGame, DistResGame):
    """ Distributed Resource game with incomplete information of other agent strategies """
    def __init__(self, players, strategies, infograph, values, w, f):
        InfoGame.__init__(self, players, strategies, infograph)
        DistResGame.__init__(self, players, strategies, values, w, f)

    def evaluator(self, i, strategy):        
        """ evaluator function returns a modified strategy based on limited information"""
        info = self.infograph[i] + [i]  # knows its own strategy
        mod_str = tuple([strategy[j] if j in info else () for j in range(self.n)])
        return mod_str

    def U_i(self, i, strategy):
        """ utility for the strategy for player with index i"""
        mod_strategy = self.evaluator(i, strategy)
        return ResourceGame.U_i(self, i, mod_strategy)
