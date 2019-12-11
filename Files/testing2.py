#!/usr/bin/env python
"""
Tutorial example for computing price of anarchy for a class of resource allocation games
"""

from basic import *

players = [i for i in range(1, 5)]
strategies = [[(), (0,), (2,)], [(), (1,), (2,)], [(), (2,), (3,), (4,)], [(), (2,), (3,), (4,)]]

game = Game(None, players, strategies)
game.set_st_dict()

payoffs = [np.array([[3, 1], [4, 2]]), np.array([[3, 4], [1, 2]])]
g = FromPayoffGame(payoffs)
g.set_pnes()
print(g.strategies, g.pnes)


def set_pnes(self):
    """ set pure nash equilibria """
    self.set_dependency(['payoffs'])
    cpnes = list(np.argwhere(self.payoffs[0] == np.amax(self.payoffs[0], 0)))
    cpnes = [tuple(cpne) for cpne in cpnes]
    pnes = []
    #print(cpnes)
    #num_strat = [len(st) for st in self.strategies]
    #print(num_strat)
    for i in range(1, self.n):
        pm = self.payoffs[i]
        for cpne in cpnes[:]:
            #cpne = cpnes[j]
            #ind = cpne[:i] + (slice(num_strat[i]),) + cpne[i+1:]
            ind = cpne[:i] + (slice(None),) + cpne[i+1:]
            #print(pm[cpne], pm[ind])
            if pm[cpne] < np.max(pm[ind]):
                #print('godammit', cpnes)
                cpnes.pop(cpnes.index(cpne))
            #else:
            #    print(cpne, ind, pm[cpne], pm[ind])
    self.pnes = cpnes


n = 5  # number of players
m = 6  # number of resources
s = 3  # number of strategies for each player
players = [i for i in range(n)]
values = [randint(1, 5) for _ in range(m)]  # values in [1, 5]
strategies = [[()] + list(set([(randint(0, m-1),) for _ in range(s)])) for _ in range(n)]  # each player has at most s single resource strategies
infograph = [players[:] for i in range(n)]  # complete information
[infograph[i].pop(i) for i in range(n)]  # remove self loops
w = [0] + [1]*n  # welfare for covering games
gairing_f = [0] + [factorial(j-1)/(exp(1)-1)*(exp(1) - sum([1./factorial(i) for i in range(j)])) for j in range(1, n+1)]  # gairing distribution rule
marginal_f = [0, 1] + [0]*(n-1)  # marginal distribution rule
print 'values: ', values
print 'strategies: ', strategies
print 'info: ', infograph
