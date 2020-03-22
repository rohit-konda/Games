#!/usr/bin/env python
"""
Explicit construction for calculating PoA - derived from 
R Chandan, D Paccagnan, JR Marden (2019) Utility Design for Distributed Resource Allocation - Part I: Characterizing and Optimizing the Exact Price of Anarchy
"""

import numpy as np
from Games.res.resource import ResourceGame, DistResGame
from Games.res.incomplete import DistInfoGame
from itertools import product
from cvxopt.solvers import lp
from cvxopt import matrix


class CompPoaGame(ResourceGame):
    """ framework for resource games with computable price of anarchy """
    def __init__(self, players, strategies, values, solver='cvxopt'):
        ResourceGame.__init__(self, players, strategies, len(values))
        self.partition = list(product([1, 2, 3, 4], repeat=self.n))[:-1]
        self.solver = solver
        self.sol = None  # solver output

    def primal_poa(self):     
        """ primal formulation for calculation of Price of Anarchy """
        N = 4**self.n - 1
        c = np.zeros((N,), dtype='float')
        cons_1 = np.zeros((self.n, N), dtype='float')
        A = np.zeros((1, N), dtype='float')
        for i in range(len(self.partition)):
            p = self.partition[i]
            Na = [k for k in range(self.n) if p[k]==1]
            Nx = [k for k in range(self.n) if p[k]==2]
            Nb = [k for k in range(self.n) if p[k]==3]

            c[i] = -self.w_poa(Nb + Nx)
            A[0, i] = self.w_poa(Na + Nx)
            for j in range(self.n):
                cons_1[j][i] = self.nash_poa(j, Na, Nb, Nx)

        cons_2 = np.identity(N)
        G = -np.vstack((cons_1, cons_2))
        h = np.zeros((N+self.n, 1))
        b = np.array([[1]], dtype='float')
        
        self.lp_solver(c, G, h, A, b)
        game = self.worst_case(np.array(self.sol['x']).flatten()) # worst case game instance
        return -1./self.sol['primal objective'], game 

    def nash_poa(self, j, Na, Nb, Nx):
        """ define the nash constraint for the computable poa calculation """
        if j in Na:
            return self.f_poa(j, Na + Nx)
        elif j in Nb:
            return -self.f_poa(j, Na + Nx + [j])
        else:
            return 0

    def f_poa(self, i, players):
        """ design distribution function """
        pass

    def w_poa(self, players):
        """ welfare function """
        pass

    def f_r(self, i, res, players):
        """ function design for the utility function depends on what resource,
        and what players are covering it """
        return self.values[res] * self.f_poa(i, players)

    def w_r(self, res, players):
        """ welfare function, returns a scalar value dependent on the resource and which players select it """
        return self.values[res] * self.w_poa(players)

    def worst_case(self, theta):
        """ get worst case instance """
        players = [i for i in range(self.n)]
        values = []
        strategies = [[(), ()] for _ in players]
        c = 0
        for i in range(len(theta)):
            val = round(theta[i], 7) # round theta to avoid ~0 value resources
            if  val > 0:
                values.append(val)
                for j in range(self.n):
                    if self.partition[i][j] == 1:
                        strategies[j][0] += (c,)
                    elif self.partition[i][j] == 2:
                        strategies[j][0] += (c,)
                        strategies[j][1] += (c,)
                    elif self.partition[i][j] == 3:
                        strategies[j][1] += (c,)
                c += 1
        return players, strategies, values, self.w, self.f

    def lp_solver(self, c, G, h, A=None, b=None):
        """ LP solver method constructor"""
        if self.solver == 'cvxopt':
            c = matrix(c)
            G = matrix(G)
            h = matrix(h)
            A = matrix(A) if A is not None else None
            b = matrix(b) if b is not None else None
            self.sol = lp(c, G, h, A, b)
            if self.sol['status'] != 'optimal':
                raise ValueError('no feasible solution found')
        else:
            raise ValueError('indicated a invalid solver name for self.solver')


class ResPoaGame(CompPoaGame, DistResGame):
    """ framework for dist resource allocation games with computable price of anarchy """
    def __init__(self, players, strategies, values, w, f, solver='cvxopt'):
        CompPoaGame.__init__(self, players, strategies, values, solver)
        DistResGame.__init__(self, players, strategies, values, w, f)

    def f_r(self, i, res, players):
        """ function design for the utility function depends on what resource,
        and what players are covering it """
        return DistResGame.f_r(self, i, res, players)
    
    def w_r(self, res, players):
        """ welfare function, returns a scalar value dependent on the resource and which players select it """
        return DistResGame.w_r(self, res, players)  

    def f_poa(self, i, players):
        """ design distribution function """
        return self.f[len(players)]

    def w_poa(self, players):
        """ welfare function """
        return self.w[len(players)]


class ResInfoPoaGame(ResPoaGame, DistInfoGame):
    """ framework for information dependent resource allocation games with computable price of anarchy """
    def __init__(self, players, strategies, values, w, f, infograph, solver='cvxopt'):
        ResPoaGame.__init__(self, players, strategies, values, w, f, solver)
        DistInfoGame.__init__(self, players, strategies, values, w, f, infograph)

    def f_poa(self, i, players):
        """ design distribution function """
        return self.f[len([k for k in players if k in self.infograph[i] + [i]])]
