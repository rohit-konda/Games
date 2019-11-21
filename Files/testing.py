#!/usr/bin/env python
"""
Tutorial example for computing price of anarchy for a class of resource allocation games
"""

from Games.basic import *
from Games.res.resource import *
from Games.res.incomplete import *

players = [i for i in range(4)]
strategies = [[(), (0,), (2,)], [(), (1,), (2,)], [(), (2,), (3,), (4,)], [(), (2,), (3,), (4,)]]
res = [2, 1, 4, 2, 1]
w = [0, 1, 1, 1, 1]
f = [0, 1, 0, 0, 0]

game = DistResGame(players, strategies, res, w, f)


'''
game.set_posa()
print(game.pnes)
print(np.array([game.s_payoff[pne] for pne in game.pnes]))
print(game.so)
print(game.posa)
'''

players_2 = [i for i in range(4)]
strategies_2 = [[(), (0,), (1,)], [(), (1,)], [(), (1,), (2,)], [(), (3,)]]
res_2 = [1, 1, 1, 0]
info = [[], [0], [], [2]]

game_2 = DistInfoGame(players_2, strategies_2, info, res_2, w, f)

game_2.set_posa()
print(game_2.pnes)
print(np.array([game_2.s_payoff[pne] for pne in game_2.pnes]))
print(game_2.so)
print(game_2.posa)