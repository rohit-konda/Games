#!/usr/bin/env python
"""
Library for welfare resource games
R Chandan, D Paccagnan, JR Marden (2019) Utility Design for Distributed Resource Allocation - Part I: Characterizing and Optimizing the Exact Price of Anarchy
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

        obj, sol = self.poa_solver(c, G, h)
        poa = 1./obj
        f = [0.] + list(sol)[1:]
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

        obj, sol = self.poa_solver(c, G, h)
        return 1./obj

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

        obj, sol = self.poa_solver(c, G, h, A, b)
        game = self.worst_case(sol) # worst case game instance
        return -1./obj, game

    def poa_solver(self, c, G, h, A=None, b=None):
        """ function for solving the relevant optimization program"""
        if self.solver == 'cvxopt':
            c = matrix(c)
            G = matrix(G)
            h = matrix(h)
            A = matrix(A) if A is not None else None
            b = matrix(b) if b is not None else None
            sol = lp(c, G, h, A, b)
            if sol['status'] == 'optimal':
                return sol['primal objective'], sol['x']
            else:
                print sol
                raise ValueError('no feasible solution found')
        else:
            raise ValueError('indicated a invalid solver name for self.solver')

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
        return (players, strategies, values, self.w, self.f)
