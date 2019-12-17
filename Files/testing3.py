#!/usr/bin/env python
"""
Testing Gairing's distribution rule
"""

from Games.basic import *
from Games.res.resource import *
from Games.res.incomplete import *
from Games.res.computable import CompResourceGame
from math import factorial, exp
from random import randint
import matplotlib.pyplot as plt
import json


def pr_gm(gm):
	gm.set_posa()  # calculate PoA and PoS
	print 'pnes', gm.pnes  # pure nash equilibria
	print 'payoffs', np.array([gm.s_payoff[pne] for pne in gm.pnes])  # payoff 
	print 'so', gm.so  # social optimal
	print 'posa', gm.posa  # social poa


def get_gm(n, m, s):
	""" produce a game instance """
	values = [randint(1, 100) for _ in range(m)]  # values in [1, 5]
	single = randint(1, s)
	strategies = [[()] + list(set([(randint(0, m-1),) for _ in range(single)])) for _ in range(n)]  # each player has at most s single resource strategies
	return (strategies, values)


n = 5  # number of players
m = 8  # number of resources
s = 3  # number of strategies for each player
players = [i for i in range(n)]

w = [0] + [1]*n  # welfare for covering games
marginal_f = [0, 1] + [0]*(n-1)  # marginal distribution rule
gairing_f = [0] + [factorial(j-1)/(exp(1)-1)*(exp(1) - sum([1./factorial(i) for i in range(j)])) for j in range(1, n+1)]  # gairing distribution rule for infinite n

c1 = 1./(factorial(n-1)*(n-1))
def c2(j): return sum([1./factorial(i) for i in range(j, n)])
gairing_n_f = [0] + [factorial(j-1)*(c1 + c2(j))/(c1 + c2(1)) for j in range(1, n+1)]  # gairing distribution rule for finite n

marg = 1./2
gair = 1./(exp(1) - 1)
gair_n = 1 - 1./(c1 + c2(0))
print 'm, g, g_n', marg, gair, gair_n
print 'gairing', gairing_n_f

# infographs
# complete
complete = [[j for j in range(n) if j != i] for i in range(n)]
# take one edge out
min_1_edge = [[j for j in range(n) if j != i] for i in range(n)]
min_1_edge[0].pop(0)
# take 2 edges out
both_in = [[j for j in range(n) if j != i] for i in range(n)]
both_in[0] = both_in[0][2:]
both_out = [[j for j in range(n) if j != i] for i in range(n)]
both_out[1].pop(0)
both_out[2].pop(0)
in_out = [[j for j in range(n) if j != i] for i in range(n)]
in_out[0].pop(0)
in_out[1].pop(0)
in_out_2 = [[j for j in range(n) if j != i] for i in range(n)]
in_out_2[0].pop(0)
in_out_2[2].pop(0)
#different_2 = [[j for j in range(n) if j != i] for i in range(n)]
#different_2[0].pop(0)
#different_2[2].pop(3)
# complete DAG
#complete_DAG = [[j for j in range(n) if j > i] for i in range(n)]
#empty
#empty = [[] for i in range(n)]

#print 'complete', complete
#print 'min1edge', min_1_edge
#print 'bothin', both_in
#print 'bothout', both_out
#print 'inout', in_out
#print 'inout2', in_out_2
#print 'different2', different_2
#print 'completeDAG', complete_DAG
#print 'empty', empty

cycle = [[3], [0], [1], [2]]

'''
plyers = [i for i in range(3)]
gm = DistInfoGame(plyers, [[(), (3,), (1,), (4,)], [(), (2,), (3,), (1,)], [(), (7,), (2,), (3,)]], cycle, [43, 49, 19, 56, 27, 42, 43, 37], w, gairing_n_f)
gm.set_pnes()
print gm.payoffs[1]
for (k, v) in np.ndenumerate(gm.payoffs[1]):
	print k, v
#pr_gm(gm)
'''
plyers = [i for i in range(4)]
gm = DistInfoGame(plyers, [[(), (0,), (1,)], [(), (1,), (2,)], [(), (2,), (3,)], [(), (3,), (1,)]], cycle, [1, 2, 3, 4], w, marginal_f)
gm.set_pnes()
print gm.pnes
#print gm.payoffs[0]
#for (k, v) in np.ndenumerate(gm.payoffs[0]):
# 	print k, v


'''
poa = []
games = []
for i in range(3000):
	try:
		st, v = get_gm(n, m, s)
		gm = DistInfoGame(players, st, in_out_2, v, w, marginal_f)
		gm.set_posa()
		poa.append(gm.posa[0])
		games.append([gm.players, gm.strategies, gm.values])
		if gm.posa[0] < .55:
			print st, v
			print gm.posa[0], gm.pnes
			print gm.so, np.array([gm.s_payoff[pne] for pne in gm.pnes])
	except:
		print 'what happened!', st, v
		print gm.pnes
	else:
		print i

#json.dump(games, open('margempty.json', 'w'))

plt.hist(poa, 100)
plt.axvline(1./2, color='k')
plt.axvline(1, color='k')
plt.axvline(0, color='k')
plt.axvline(gair, color='b')
plt.axvline(gair_n, color='r')
plt.axhline(color='k')
plt.gca().set_xlim([0, 1])
plt.show()
'''

