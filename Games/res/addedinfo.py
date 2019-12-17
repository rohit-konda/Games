#!/usr/bin/env python
"""
Distributed Resource allocation games with added information on the utilities.
"""


class AddedInfoGame(DistResGame):
    """ Distributed Resource game with incomplete information of other agent strategies """
    def __init__(self, players, strategies, infograph, values, w, f):
        InfoGame.__init__(self, players, strategies, infograph)
        DistResGame.__init__(self, players, strategies, values, w, f)

    def evaluator(self, i, strategy):        
        """ evaluator function returns a modified strategy based on limited information """
        info = self.infograph[i] + [i]  # knows its own strategy
        mod_str = tuple([strategy[j] if j in info else () for j in range(self.n)])  # assume that players it sees does nothing
        return mod_str

    def U_i(self, i, strategy):
        """ utility for the strategy for player with index i """
        mod_strategy = self.evaluator(i, strategy)
        return ResourceGame.U_i(self, i, mod_strategy)
