#!/usr/bin/env python
"""
Tutorial example for computing price of anarchy for a class of resource allocation games
"""

#from computable import *
from resource import *


players = ['Alice', 'Bob', 'Carolyn', 'Dmitri']
res = [4, 9, 2, 5, 8, 7, 9, 3, 6, 7]
r_m = len(res)
n = len(players)
strategies = [[(), (1, 2, 4), (3, 6), (0, 9), (7, 8)], [(), (2, 8, 9), (3, 4, 5), (6, 7, 9), (0, 4)], [(), (5, 7), (0, 6), (3, 6, 9), (1, 2, 6)], [(), (2, 3), (4, 8), (1, 3)]]

players = ['Alice', 'Bob']
strategies = [[(3, 2), (1, 2), (3, 4)], [(), (3, 4, 5),  (0, 4)]]
r_m = 6

# Vehicle Target Assignment
p = .5
w = [1 - (1-p)**j for j in range(n+1)]
f = [0] + [p*(1-p)**(j-1) for j in range(1, n+1)]

game = DistrResGame(players, to_dictstrat(players, strategies))
#game.set_s_payoff()


