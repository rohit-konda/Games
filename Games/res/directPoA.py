#!/usr/bin/env python
"""
Library for computing PoA through linear program for loss of information
"""

import numpy as np
from Games.res.computable import CompResourceGame
from Games.res.incomplete import DistInfoGame
from itertools import product


class InfoPoaGame(CompResourceGame, DistInfoGame):
    """ framework for resource games with computable price of anarchy """
    def __init__(self, players, strategies, values, w, f, infograph, solver='cvxopt'):
        CompResourceGame.__init__(self, players, strategies, values, w, f, solver)
        DistInfoGame.__init__(self, players, strategies, values, w, f, infograph)
        self.partition = list(product([1, 2, 3, 4], repeat=self.n))

    def primal_poa(self):     
        """ primal formulation for calculation of Price of Anarchy """
        N = 4**self.n
        c = np.zeros((N,), dtype='float')
        cons_1 = np.zeros((self.n, N), dtype='float')
        A = np.zeros((1, N), dtype='float')
        for i in range(len(self.partition)):
            p = self.partition[i]
            opt = [k for k in range(self.n) if p[k]==2 or p[k]==3]
            nash = [k for k in range(self.n) if p[k]==1 or p[k]==2]
            c[i] = -self.w[len(opt)]
            A[0, i] = self.w[len(nash)]
            for j in range(self.n):
                nash_u = 0
                opt_u = 0
                if j in nash:
                    nash_u = self.f[len(self.viewed(nash, j))]
                if j in opt:
                    opt_u = self.f[len(self.viewed(opt, j))]
                cons_1[j][i] = nash_u - opt_u

        cons_2 = np.identity(N)
        G = -np.vstack((cons_1, cons_2))
        h = np.zeros((N+self.n, 1))
        b = np.array([[1]], dtype='float')
        obj, sol = self.poa_solver(c, G, h, A, b)
        game = self.worst_case(np.array(sol).flatten()) # worst case game instance
        return -1./obj, game 

    def viewed(self, covered, j):
        """ modify the outcome based on which other agents are viewed """
        return [k for k in covered if k in self.infograph[j] + [j]]

    def worst_case(self, theta):
        """ get worst case instance """
        players = [i for i in range(self.n)]
        values = []
        strategies = [[(), ()] for _ in players]
        c = 0
        for i in range(len(theta)):
            val = round(theta[i], 8) # round theta to avoid ~0 value resources
            if  val > 0:
                values.append(val)
                for j in range(n):
                    if self.partition[i][j] == 1:
                        strategies[j][0] += (c,)
                    elif self.partition[i][j] == 2:
                        strategies[j][0] += (c,)
                        strategies[j][1] += (c,)
                    elif self.partition[i][j] == 3:
                        strategies[j][1] += (c,)
                c += 1
        return players, strategies, values, self.w, self.f, self.infograph
