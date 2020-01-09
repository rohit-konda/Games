from Games.basic import *
from directPoA import *
from incomplete import *
from computable import *


n = 3
players = [i for i in range(n)]
strategies = [[(), ()] for _ in range(n)]
values = []
infograph = [[0], [1], []]
w = [0, 1, 1, 1, 1]
#f = [0, 1, .42, .25, .18]
# f = [0, 1, .33, .25, .2]
f = [0, 1, 0, 0, 0]

game = InfoPoaSumGame(players, strategies, values, w, f, infograph)
poa, sol = game.primal_poa()
print('computed', poa)
c = 0

gam = DistInfoGame(*sol)

gam.set_s_payoff()	
print('payoff', gam.s_payoff[(0, 0, 0)], gam.s_payoff[(1, 1, 1)])
print('values', gam.values)
print('strategies', gam.strategies)