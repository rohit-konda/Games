#!/usr/bin/env python
"""
Library for welfare resource games
"""

from Games.social import *
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.colors as mcolors

class ResourceGame(SocialGame):
    """ framework for a resource game """
    def __init__(self, players, strategies, r_m):
        # strategies should be in the powerset of resources 2^r_m
        SocialGame.__init__(self, None, players, strategies)
        self.r_m = r_m  # number of resources

    def w_r(self, res, players):
        """ welfare function, returns a scalar value dependent on the resource and which players select it """
        pass

    def player_cover(self, strategies):
        """ returns list of which players are covering the resource """
        return [[j for j in range(self.n) if i in strategies[j]] for i in range(self.r_m)]

    def set_s_payoff(self):
        """ set social payoff matrix """
        self.set_dependency(['st_dict'])
        sp_dict = {}
        for k, v in self.st_dict.items():
            p_cover = self.player_cover(v)
            value = sum([self.w_r(i, p_cover[i]) for i in range(self.r_m)])
            sp_dict.update({k: value})
        self.s_payoff = np.array(dict_nlist(sp_dict))

    def U_i(self, i, strategy):
        """ utility for the strategy for player i """
        strategy_i = list(strategy[i])
        p_cover = self.player_cover(strategy)
        return sum([self.f_r(i, j, p_cover[j]) for j in strategy_i])

    def f_r(self, i, res, players):
        """ function design for the utility function depends on what resource,
        and what players are covering it """
        pass


class CongestionGame(ResourceGame):
    """ framework for a congestion game """
    def __init__(self, players, strategies, Wr, Fr):
        # strategies should be in the powerset of resources 2^r_m
        ResourceGame.__init__(self, players, strategies, len(Wr))
        self.Wr = Wr  # r_m x n+1 array to denote welfare associated with the number of players selecting a resource
        self.Fr = Fr  # r_m x n+1 array to denote utility associated with the number of players selecting a resource

    def w_r(self, res, players):
        """ welfare function, returns a scalar value dependent on the resource,
         and how many players select it """
        return self.Wr[res, len(players)]

    def f_r(self, i, res, players):
        """ function design for the utility function depends on what resource,
        and what players are covering it """
        return self.Fr[res, len(players)]


class DistResGame(CongestionGame):
    """ distributed resource allocation game where utility is gained for covering an array of resources """
    def __init__(self, players, strategies, values, w, f):
        Wr = np.dot(np.diag(values), np.array([w] * len(values)))  # Wr(j) = v_r * w(j)
        Fr = np.dot(np.diag(values), np.array([f] * len(values)))  # Fr(j) = v_r * f(j)
        CongestionGame.__init__(self, players, strategies, Wr, Fr)
        self.values = values  # values (v_r) associated with each resource
        self.w = w  # w(j) welfare basis function ((n+1,) np.array)
        self.f = f  # f(j) design function for the utility ((n+1,) np.array)

    def plot(self, strategies):
        """ matplotlib plot representation of the resource game """
        # Create figure and axes
        fig, ax = plt.subplots()
        pc = self.player_cover(strategies)
        colors = mcolors.cnames.keys()
        for i in range(self.r_m):
            width = 10
            height = len(pc[i])*10 + 4
            x, y = (15*i, 0)
            rect = patches.Rectangle((x, y), width, height, facecolor='none')
            for j in range(len(pc[i])):
                r = 4
                color = colors[pc[i][j]]
                circ = patches.Circle((x+5, 3 + r + (r+1)*2*j), r, color=color, ec=color)
                ax.add_patch(circ)
            ax.add_patch(rect)
        axwidth = 15*self.r_m + 5
        ax.set_xlim((-5, axwidth))
        ax.set_ylim((-5, max(10*self.n + 4, axwidth*.7)))
        plt.show()
