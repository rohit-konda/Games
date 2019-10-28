#!/usr/bin/env python
"""
Library for welfare games that depend on information constraints
"""

from Games.basic_games import *

class InfoResourceGame(ResourceGame, NetworkGame):
    """ Resource game with incomplete information of other agent strategies """
    def __init__(self, payoffs, players, strategies, r_m, network):
        ResourceGame.__init__(self, payoffs, players, strategies, r_m)
        NetworkGame.__init__(self, payoffs, players, strategies, network)

    def U_i(self, i, strategies):
        """ utility for the strategies for player i"""
        info = self.network[self.players[i]]
        p_i = list(strategies[i])
        known_st = [strategies[self.players.index(pl)] for pl in info]
        known_st_rel = [j if j in set(known_st) else None for j in strategies]
        mod_pi = self.evaluator(i, known_st_rel)
        res_d = self.res_dist(mod_pi)
        return sum([self.f_r(res_d[j], j) for j in p_i])

    def evaluator(self, i, mod_strategy):
        """ A valid evaluator functions that returns a possible total strategy """
        pass

class MaxInfoSetCoverGame(InfoResourceGame, SetCoverGame):
    """ """
    def __init__(self, payoffs, players, strategies, resources, w, f, network):
        InfoResourceGame.__init__(self, payoffs, players, strategies, len(resources), network)
        SetCoverGame.__init__(self, payoffs, players, strategies, resources, w, f)

    def evaluator(self, i, mod_strategy):
        """ A valid evaluator functions that returns a possible total strategy """
        return [() if j is None else j for j in mod_strategy]
