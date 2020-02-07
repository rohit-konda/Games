#!/usr/bin/env python
"""
Tutorial example for computing price of anarchy for a class of resource allocation games
"""

from Games.basic import *
from Games.res.resource import *
from Games.res.incomplete import *
from math import factorial, exp
from random import randint
import matplotlib.pyplot as plt


def pr_gm(gm):
	gm.set_posa()  # calculate PoA and PoS
	print(gm.pnes)  # pure nash equilibria
	print(np.array([gm.s_payoff[pne] for pne in gm.pnes]))  # payoff 
	print(gm.so)  # social optimal
	print(gm.posa)  # social poa


## First Example in Submod paper (Matches)


players = [i for i in range(4)]
strategies = [[(), (0,), (2,)], [(), (1,), (2,)], [(), (2,), (3,), (4,)], [(), (2,), (3,), (4,)]]
res = [2, 1, 4, 2, 1]
w = [0, 1, 1, 1, 1]
f = [0, 1, 0, 0, 0]

game = DistResGame(players, strategies, res, w, f)

#pr_gm(game)


## Second Example in Submod Paper (Matches)


players_2 = [i for i in range(4)]
strategies_2 = [[(), (0,), (1,)], [(), (1,)], [(), (1,), (2,)], [(), (3,)]]
res_2 = [1, 1, 1, 0]
info = [[], [0], [], [2]]

#game_2 = DistInfoGame(players_2, strategies_2, info, res_2, w, f)
strategy = [(0,), (1,), (1,), (3,)]

#pr_gm(game_2)

n = 5
c1 = 1./(factorial(n-1)*(n-1))
def c2(j): return sum([1./factorial(i) for i in range(j, n)])
gairing_n_f = [0] + [factorial(j-1)*(c1 + c2(j))/(c1 + c2(1)) for j in range(1, n+1)]  # gairing distribution rule for finite n

def gnf(n):
	def c2(j): return sum([1./factorial(i) for i in range(j, n)])
	c1 = 1./(factorial(n-1)*(n-1))
	return [0] + [factorial(j-1)*(c1 + c2(j))/(c1 + c2(1)) for j in range(1, n+1)]

g = gnf(100)
num = 1 + g[3]
den = 2 + g[2] + g[3] - g[2]*g[3]
print num/den
g3 = 2 * (np.exp(1) - 5./2) / (np.exp(1) -1.)
g2 = (np.exp(1) - 2.) / (np.exp(1) - 1.)
val = (1. + g3)/(2. + g2 + g3 - g2*g3)
print g2, g3, val
e = np.exp(1)
e1 = e - 1.
e3 = 2*e - 5.
e2 = e - 2.
print (e1**2 + e3*e1)/(2*e1**2 + e2*e1 + e3)
print (2*e1**2 + e2*e1 + e3)
print 3*e**2 - 5*e - 1
#print ()/()
