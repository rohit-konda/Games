#!/usr/bin/env python
"""
Library for welfare resource games
R Chandan, D Paccagnan, JR Marden (2019) Optimal mechanisms for distributed resource-allocation.
"""

import numpy as np
from Games.res.resource import DistResGame
from cvxopt.solvers import lp
from cvxopt import matrix
from itertools import combinations
#from scipy.optimize import linprog


def I(n):
    """ generate all viable triples of (a, x, b) with 1 <= a + x + b <= n"""
    ind = []
    for i in range(1, n+1):
        all_i = [(j[0], j[1]-j[0]-1, i-j[1]+1) for j in combinations(range(i+2), 2)]
        ind += all_i
    return ind


def I_r(n):
    """ generate all viable triples of (a, x, b) of I with a + x + b = n 
    or any a, x, b = 0 """
    ind = []
    for i in range(0, n+1):
        not_a = [(0, j, i) for j in range(n+1-i)]
        not_x = [(j, 0, i) for j in range(n+1-i)]
        not_b = [(j, i, 0) for j in range(n+1-i)]
        ind = ind + not_a + not_b + not_x

    ind += [(j[0], j[1]-j[0]-1, n-j[1]+1) for j in combinations(range(n+2), 2)]
    return [j for j in list(set(ind)) if j != (0, 0, 0)]


class CompResourceGame(DistResGame):
    """ framework for resource games with computable price of anarchy """
    def __init__(self, players, strategies, values, w, f, solver='cvxopt'):
        DistResGame.__init__(self, players, strategies, values, w, f)
        self.I = I(self.n)
        self.I_r = I_r(self.n)
        self.solver = solver

    def function_poa(self):
        """ returns the distribution rule f for the optimal PoA """
        num = len(self.I_r)
        G = np.zeros((num+1, self.n+1), dtype='float')
        h = np.zeros((num+1, 1), dtype='float')
        h[num] = -1
        
        c = np.zeros((self.n+1, 1), dtype='float')
        c[0] = 1
        for i in range(num):
            a, x, b = self.I_r[i]
            G[i, a+x] = a
            if a+x < self.n:
                G[i, a+x+1] = -b
            G[i, 0] = -self.w[a+x]
            h[i] = -self.w[b+x]
        G[num][0] = -1

        sol = self.poa_solver(c, G, h, None, None)
        poa = 1/sol['primal objective']
        f = [0.] + list(sol['x'])[1:]
        return (poa, f)

    def dual_poa(self):
        """ dual formulation for calculation of Price of Anarchy"""  
        if self.f[1] <= 0:
            return 0
        num = len(self.I_r)

        G = np.zeros((num+1, 2), dtype='float')
        h = np.zeros((num+1, 1), dtype='float')
        c = np.array([[0], [1]], dtype='float')  # variables = [lambda , mu]

        for i in range(num):
            a, x, b = self.I_r[i]
            G[i, 0] = a*self.f[a+x] - b*self.f[a+x+1] if a+x < self.n else a*self.f[a+x]
            G[i, 1] = -self.w[a+x]
            h[i] = -self.w[b+x]
        G[num][0] = -1 

        sol = self.poa_solver(c, G, h, None, None)
        return 1/sol['primal objective']

    def primal_poa(self):     
        """ primal formulation for calculation of Price of Anarchy """
        if self.f[1] <= 0:
            return 0
        num = len(self.I)

        c = -np.array([self.w[b+x] for a, x, b in self.I], dtype='float')
        cons_1 = [a*self.f[a+x] - b*self.f[a+x+1] if a+x < self.n else a*self.f[a+x]
                 for a, x, b in self.I]
        cons_2 = np.identity(num)
        G = -np.vstack((cons_1, cons_2))
        A = np.array([[self.w[a+x] for a, x, b in self.I]], dtype='float')
        b = np.array([[1]], dtype='float')
        h = np.zeros((num+1, 1))

        sol = self.poa_solver(c, G, h, A, b)
        return -1/sol['primal objective']

    def poa_solver(self, c, G, h, A, b):
        """ function for solving the relevant optimization program"""
        if self.solver == 'cvxopt':
            sol = lp(matrix(c), matrix(G), matrix(h), matrix(A) if A else None, matrix(b) if b else None)
            if sol['status'] == 'optimal':
                return sol
            else:
                raise ValueError('no feasible solution found')
        else:
            raise ValueError('indicated a invalid solver name for self.solver')