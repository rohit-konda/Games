#!/usr/bin/env python
"""
Explicit construction for calculating PoA for 1 lost edge
"""

from Games.res.directPoA import *
from computable import *
from itertools import product
from math import factorial, exp


class OLE_Game(CompResourceGame):
    """ POA calculation for game with 1 lost edge """
    def __init__(self, players, strategies, values, w, f, solver='cvxopt'):
        CompResourceGame.__init__(self, players, strategies, values, w, f, solver='cvxopt')
        self.I = I(self.n-2) + [(0, 0, 0)]

    def primal_poa(self):     
        """ primal formulation for calculation of Price of Anarchy """
        l_i = len(self.I)
        N = 16*l_i
        f = self.f + [0]
        c = np.zeros((N,), dtype='float')
        cons_1 = np.zeros((N,), dtype='float')
        cons_2 = np.zeros((N,), dtype='float')
        cons_3 = np.zeros((N,), dtype='float')
        A = np.zeros((1, N), dtype='float')

        for i in range(l_i):
            a, x, b = self.I[i]
            for k in range(16):
                if k == 0:  # null, null
                    val = a*f[a+x] - b*f[a+x+1]
                    val2 = 0
                    val3 = 0
                    opt = b+x
                    nash = a+x
                elif k == 1:  # null, a
                    val = a*f[a+x+1] - b*f[a+x+2]
                    val2 = 0
                    val3 = f[a+x+1]
                    opt = b+x
                    nash = a+x+1
                elif k == 2:  # null, x
                    val = a*f[a+x+1] - b*f[a+x+2]
                    val2 = 0
                    val3 = 0
                    opt = b+x+1
                    nash = a+x+1
                elif k == 3:  # null, b
                    val = a*f[a+x] - b*f[a+x+1]
                    val2 = 0
                    val3 = -f[a+x+1]
                    opt = b+x+1
                    nash = a+x
                elif k == 4:  # a, null
                    val = a*f[a+x+1] - b*f[a+x+2]
                    val2 = f[a+x+1]
                    val3 = 0
                    opt = b+x
                    nash = a+x+1
                elif k == 5:  # a, a
                    val = a*f[a+x+2] - b*f[a+x+3]
                    val2 = f[a+x+1]
                    val3 = f[a+x+2]
                    opt = b+x
                    nash = a+x+2
                elif k == 6:  # a, x
                    val = a*f[a+x+2] - b*f[a+x+3]
                    val2 = f[a+x+1]
                    val3 = 0
                    opt = b+x+1
                    nash = a+x+2
                elif k == 7:  # a, b
                    val = a*f[a+x+1] - b*f[a+x+2]
                    val2 = f[a+x+1]
                    val3 = -f[a+x+2]
                    opt = b+x+1
                    nash = a+x+1
                elif k == 8:  # x, null
                    val = a*f[a+x+1] - b*f[a+x+2]
                    val2 = 0
                    val3 = 0
                    opt = b+x+1
                    nash = a+x+1
                elif k == 9:  # x, a
                    val = a*f[a+x+2] - b*f[a+x+3]
                    val2 = 0
                    val3 = f[a+x+2]
                    opt = b+x+1
                    nash = a+x+2
                elif k == 10:  # x, x
                    val = a*f[a+x+2] - b*f[a+x+3]
                    val2 = 0
                    val3 = 0
                    opt = b+x+2
                    nash = a+x+2
                elif k == 11:  # x, b
                    val = a*f[a+x+1] - b*f[a+x+2]
                    val2 = 0
                    val3 = -f[a+x+2]
                    opt = b+x+2
                    nash = a+x+1
                elif k == 12:  # b, null
                    val = a*f[a+x] - b*f[a+x+1]
                    val2 = -f[a+x+1]
                    val3 = 0
                    opt = b+x+1
                    nash = a+x
                elif k == 13:  # b, a
                    val = a*f[a+x+1] - b*f[a+x+2]
                    val2 = -f[a+x+1]
                    val3 = f[a+x+1]
                    opt = b+x+1
                    nash = a+x+1
                elif k == 14:  # b, x
                    val = a*f[a+x+1] - b*f[a+x+2]
                    val2 = -f[a+x+1]
                    val3 = 0
                    opt = b+x+2
                    nash = a+x+1
                elif k == 15:  # b, b
                    val = a*f[a+x] - b*f[a+x+1]
                    val2 = -f[a+x+1]
                    val3 = -f[a+x+1]
                    opt = b+x+2
                    nash = a+x
                
                ind = k*l_i + i
                cons_1[ind] = val
                cons_2[ind] = val2
                cons_3[ind] = val3
                c[ind] = -self.w[opt]
                A[0, ind] = self.w[nash]

        cons_I = np.identity(N)
        G = -np.vstack((cons_1, cons_2, cons_3, cons_I))                                        
        h = np.zeros((N+3, 1))
        b = np.array([[1]], dtype='float')
        self.lp_solver(c, G, h, A, b)
        game = self.worst_case(np.array(self.sol['x']).flatten()) # worst case game instance
        return -1./self.sol['primal objective'], game 

    def worst_case(self, theta):
        """ get worst case poa instance, returns a resource game outlined in Theorem 2 in Paper """
        players = [i for i in range(self.n)]
        values = []
        strategies = [[(), ()] for _ in players]
        c = 0
        for j in range(len(self.I)):
                a, x, b = self.I[j]
                val = round(theta[j], 8)  # round theta to avoid ~0 value resources
                if val > 0:
                    values += [val/self.n]*self.n
                    ind = [(k % self.n) + c for k in range(2*self.n)]
                    for p in players:
                        strategies[p][0] = strategies[p][0] + tuple(ind[p:p+a+x])
                        strategies[p][1] = strategies[p][1] + tuple(ind[p+self.n-b:p+self.n+x])
                    c += self.n
        return #(players, strategies, values, self.w, self.f)





## TEST  ## 

# gairing distribution rule for finite n
def gnf(n):
    def c2(j): return sum([1./factorial(i) for i in range(j, n)])
    c1 = 1./(factorial(n-1)*(n-1))
    return [0] + [factorial(j-1)*(c1 + c2(j))/(c1 + c2(1)) for j in range(1, n+1)]

w = [0, 1, 1, 1]
f = [0, 1, .5, .3]
print(f)
gm = OLE_Game([1, 2, 3], None, [0], w, f)
game = ResInfoPoaGame([1, 2, 3], None, [0], w, f, [[2], [0, 2], [0, 1]])

print(gm.primal_poa()[0])
print(game.primal_poa()[0])