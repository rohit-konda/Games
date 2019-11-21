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


w = [0] + [1]*len(players)
f = [0] + [factorial(j-1)/(exp(1) - 1)*(exp(1) - sum([1/factorial(i) for i in range(j)])) for j in range(len(players))]



'''
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
'''