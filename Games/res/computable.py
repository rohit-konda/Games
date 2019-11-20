#!/usr/bin/env python
"""
Library for welfare resource games
R Chandan, D Paccagnan, JR Marden (2019) Optimal mechanisms for distributed resource-allocation.
"""

from Games.basic import *
from Games.res.resource import DistResGame
from cvxopt.solvers import lp
#from scipy.optimize import linprog


def I(n):
    """ generate all viable triples of (a, x, b) with 1 <= a + x + b <= n"""
    ind = []
    for i in range(1, n+1):
        all_i = [[j[0], j[1]-j[0]-1, i-j[1]+1] for j in combinations(range(i+2), 2)]
        ind += all_i
    return ind


def I_r(n):
    """ generate all viable triples of (a, x, b) of I with a + x + b = n 
    or any a, x, b = 0 """
    ind = []
    for i in range(0, n+1):
        not_a = [(0, j, i) for j in range(n+1-i)]
        not_b = [(j, 0, i) for j in range(n+1-i)]
        not_x = [(j, i, 0) for j in range(n+1-i)]
        ind = ind + not_a + not_b + not_x

    ind += [(j[0], j[1]-j[0]-1, n-j[1]+1) for j in combinations(range(n+2), 2)]
    return [j for j in list(set(ind)) if j != (0, 0, 0)]


class CompResourceGame(DistResGame):
    """ framework for resource games with computable price of anarchy """
    def __init__(self, players, strategies, values, w, f, solver='cvxopt'):
        DistResGame.__init__(self, players, strategies, values, w, f)
        self.I = I(self.n)
        self.I_r = I_r(self.n)

    def PoAfunction(self):
        """ returns optimal function for the best Price of Anarchy """
    
        num = len(self.I_r)
        G = np.zeros((num+1, self.n+1))
        h = np.zeros((num+1,))
        h[num] = 1
        
        c = np.zeros((self.n+1,))
        c[0] = 1

        for i in range(num):
            a, b, x = self.I_r[i]

            G[i, a+x] = a
            G[i, a+x+1] = -b if a+x+1 <= self.n else 0
            G[i, 1] = -self.W_r[0, a+x]
            h[i] = -self.W_r[0, b+x]
        
        G[num][2] = 1
        
        solution = self.solver(c, G, h, None, None)
        return solution

    def primalPoA(self):     
        """ primal formulation for calculation of Price of Anarchy """

        if self.f_r(1) <= 0:
            return 0

        num = len(self.I)

        c = [self.W_r[0, b+x] for a, b, x in self.I]

        cons_1 = [a*self.f_r(a+x) - b*self.f_r(a+x+1) if a+x <= self. n else a*self.f_r(a+x)
            for a, b, x in self.I]

        cons_2 = np.identity(num)
        
        G = np.vstack((cons_1, cons_2))
        A = [self.W_r[0, a+x] for a, x, b in self.I]
        b = np.ones((num,))
        h = np.zeros(num+1,)
        
        return (c, G, h, A, b)

    def dualPoA(self):
        """ dual formulation for calculation of Price of Anarchy"""  

        if self.f_r(1) <= 0:
            return 0

        num = len(self.I_r)
        G = np.zeros((num+1, 2))
        h = np.zeros((num+1,))
        
        c = np.array([0., 1])

        for i in range(num):
            a, b, x = self.I_r[i]

            G[i, 0] = a*self.f_r(a+x) - b*self.f_r(a+x+1) if a+x+1 <= self.n else a*self.f_r(a+x)
            G[i, 1] = -self.W_r[0, a+x]
            h[i] = -self.W_r[0, b+x]
        
        G[num][0] = 1 
        
        solution = self.solver(c, G, h, None, None)
        return solution

    def f_r(self, num):
        a = [0, 1, 2, 3]
        try:
            return a[num]
        except Exception as e:
            print(num)
            raise e

    def solver(self, c, G, h, A, b):
        if self.solver == 'cvxopt':
            return lp(c, G, h, A, b)
        else:
            raise ValueError('indicated a invalid solver name for self.solver')