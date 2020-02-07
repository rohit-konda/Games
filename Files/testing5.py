#!/usr/bin/env python
"""
Tutorial example for computing price of anarchy for a class of resource allocation games
"""

from Games.basic import *
#from resource import *
from directPoA import *
from incomplete import *
from computable import *

'''
## First Example in Submod paper (Matches)


players = [i for i in range(4)]
strategies = [[(), (0,), (2,)], [(), (1,), (2,)], [(), (2,), (3,), (4,)], [(), (2,), (3,), (4,)]]
res = [2, 1, 4, 2, 1]
w = [0, 1, 1, 1, 1]
f = [0, 1, 0, 0, 0]

game = DistResGame(players, strategies, res, w, f)
game.plot([s[1] for s in strategies])
#pr_gm(game)

'''
## Second Example in Submod Paper (Matches)

'''
players_2 = [i for i in range(4)]
strategies_2 = [[(), (0,), (1,)], [(), (1,)], [(), (1,), (2,)], [(), (3,)]]
res_2 = [1, 1, 1, 0]
info = [[], [0], [], [2]]

game_2 = DistInfoGame(players_2, strategies_2, info, res_2, w, f)
strategy = [(0,), (1,), (1,), (3,)]

#pr_gm(game_2)

n = 5
c1 = 1./(factorial(n-1)*(n-1))
def c2(j): return sum([1./factorial(i) for i in range(j, n)])
gairing_n_f = [0] + [factorial(j-1)*(c1 + c2(j))/(c1 + c2(1)) for j in range(1, n+1)]  # gairing distribution rule for finite n
'''