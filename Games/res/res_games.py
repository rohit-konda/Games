#!/usr/bin/env python
"""
Library for welfare resource games
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


class SetCoverGame(ResourceGame):
    """ game where utility is gained for covering an array of resources """
    def __init__(self, players, strategies, resources, w, f):
        ResourceGame.__init__(self, players, strategies, len(resources))
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
