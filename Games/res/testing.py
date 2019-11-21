#!/usr/bin/env python
"""
Tutorial example for computing price of anarchy for a class of resource allocation games
"""

from Games.basic import *
from resource import *

players = range(1, 5)
strategies = [[(), (0,), (2,)], [(), (1,), (2,)], [(), (2,), (3,), (4,)], [(), (2,), (3,), (4,)]]
res = [2, 1, 4, 2, 1]
w = [0, 1, 1, 1, 1]
f = [0, 1, 0, 0, 0]



game = DistResGame(players, strategies, res, w, f)

game.set_so()
game.set_posa()
#for i in np.ndenumerate(game.payoffs[0]):
#	print(i)
game.set_pnes()
print(game.pnes)
print(np.array([game.s_payoff[pne] for pne in game.pnes]))
print(game.so)
print(game.posa)
