#!/usr/bin/env python
"""
Basic library of game class definitions and relevant algorithms
"""

from Games.basic_games import *


class ResourceGame(SocialGame):
    """ framework for a resource game """
    def __init__(self, players, strategies, r_m):
        # strategies should be in the powerset of resources 2^R_m
        SocialGame.__init__(self, None, players, strategies)
        self.r_m = r_m  # number of resources
        self.W_r = None  # local welfare function: array of (r_m x n)

    def set_W_r(self):
        """ set local welfare function, return a (r_m x n) array """
        pass

    def res_dist(self, strategies):
        """ return distribution of resources from list of player strategies """
        return [np.sum(np.array(flatten(strategies)) == i) for i in range(self.r_m)]

    def set_s_payoff(self):
        """ set social payoff matrix"""
        self.set_dependency(['st_dict', 'W_r'])
        sp_dict = {}
        for k, v in self.st_dict.items():
            res_d = self.res_dist(v)
            value = sum([self.W_r[i, res_d[i]] for i in range(len(res_d))])
            sp_dict.update({k: value})
        self.s_payoff = np.array(dict_nlist(sp_dict))

    def U_i(self, i, strategies):
        """ utility for the strategy for player i"""
        p_i = list(strategies[i])
        res_d = self.res_dist(strategies)
        return sum([self.f_r(res_d[j], j) for j in p_i])

    def f_r(self, num, r):
        """ function design for the utility function depends on what resource,
        and what players are covering it"""
        pass

    def set_payoffs(self):
        """ set payoff matrices """
        self.set_dependency(['st_dict'])
        payoffs = [None]*self.n
        for i in range(self.n):
            s_dict_i = {}
            for k, v in self.st_dict.items():
                s_dict_i.update({k: self.U_i(i, v)})
                return
            payoff_i = np.array(dict_nlist(s_dict_i))
            payoffs[i] = payoff_i
        self.payoffs = payoffs


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


class SetCoverGame(ResourceGame):
    """ game where utility is gained for covering an array of resources """
    def __init__(self, payoffs, players, strategies, resources, w, f):
        ResourceGame.__init__(self, payoffs, players, strategies, len(resources))
        self.resources = resources  # values (v_r) associated with each resource 
        self.w = w  # w(j) welfare basis function ((self.n+1,) np.array)
        self.f = f  # f(j) design function for the utility ((self.n+1,) np.array)

    def set_W_r(self):
        """ set local welfare function, return a (r_m x n) array
        W_r(j) = v_r * w(j) """
        W_r = np.zeros((self.r_m, self.n+1))
        for i in range(self.r_m):
            W_r[i, :] = self.resources[i]*np.array(self.w)
        self.W_r = W_r

    def f_r(self, num, r=None):
        """ function design for the utility function depends on what resource,
        and what players are covering it"""
        return self.f[num]


class MaxInfoSetCoverGame(InfoResourceGame, SetCoverGame):
    """ """
    def __init__(self, payoffs, players, strategies, resources, w, f, network):
        InfoResourceGame.__init__(self, payoffs, players, strategies, len(resources), network)
        SetCoverGame.__init__(self, payoffs, players, strategies, resources, w, f)

    def evaluator(self, i, mod_strategy):
        """ A valid evaluator functions that returns a possible total strategy """
        return [() if j is None else j for j in mod_strategy]
