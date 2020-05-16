import numpy as np
from itertools import combinations, product
from games.types.resource import ResourceFactory

class ResourcePoA:
    @staticmethod
    def I(N):
        ind = []
        for i in range(1, N+1):
            all_i = [(j[0], j[1]-j[0]-1, i-j[1]+1) for j in combinations(range(i+2), 2)]
            ind += all_i
        return ind

    @staticmethod
    def I_r(N):
        ind = []
        for i in range(0, N+1):
            not_a = [(0, j, i) for j in range(N+1-i)]
            not_x = [(j, 0, i) for j in range(N+1-i)]
            not_b = [(j, i, 0) for j in range(N+1-i)]
            ind = ind + not_a + not_b + not_x

        ind += [(j[0], j[1]-j[0]-1, N-j[1]+1) for j in combinations(range(N+2), 2)]
        return [j for j in list(set(ind)) if j != (0, 0, 0)]

    @staticmethod
    def _check_w(w):
        if len(w) < 2:
            raise ValueError('w must be greater than length 2.')
        if w[0] != 0: 
            raise ValueError('Should input w with w[0] = 0.')
        if any([e <= 0 for e in w[1:]]):
            raise ValueError('Should input w with w[n] > 0 for all n > 0.')

    @classmethod
    def _check_args(cls, f, w):
        cls._check_w(w)
        
        if len(f) != len(w):
            raise ValueError('Should input f with length matching w.')
        if f[0] != 0: 
            raise ValueError('Should input f with f[0] = 0.')
        if f[1] <= 0:
            raise ValueError('PoA = 0 if f[1] <= 0.')

    @classmethod
    def function_poa(cls, w):
        cls._check_w(w)
        N = len(w)-1
        I_r = cls.I_r(N)
        num = len(I_r)

        G = np.zeros((num+1, N+1), dtype='float')
        h = np.zeros((num+1, 1), dtype='float')
        h[num] = -1
        c = np.zeros((N+1, 1), dtype='float')
        c[0] = 1

        for i, (a, x, b) in enumerate(I_r):
            G[i, a+x] = a
            if a+x < N:
                G[i, a+x+1] = -b
            G[i, 0] = -w[a+x]
            h[i] = -w[b+x]
        G[num][0] = -1
        
        return c, G, h

    @classmethod
    def dual_poa(cls, f, w): 
        cls._check_args(f, w)
        N = len(w)-1
        I_r = cls.I_r(N)
        num = len(I_r)

        G = np.zeros((num+1, 2), dtype='float')
        h = np.zeros((num+1, 1), dtype='float')
        c = np.array([[0], [1]], dtype='float')  # variables = [lambda , mu]

        for i, (a, x, b) in enumerate(I_r):
            G[i, 0] = a*f[a+x] - b*f[a+x+1] if a+x < N else a*f[a+x]
            G[i, 1] = -w[a+x]
            h[i] = -w[b+x]
        G[num][0] = -1

        return c, G, h

    @classmethod
    def primal_poa(cls, f, w):     
        cls._check_args(f, w)
        N = len(w)-1
        I = cls.I(N)
        num = len(I)

        c = -np.array([w[b+x] for a, x, b in I], dtype='float')
        cons_1 = [a*f[a+x] - b*f[a+x+1] if a+x < N else a*f[a+x] for a, x, b in I]
        cons_2 = np.identity(num)
        G = -np.vstack((cons_1, cons_2))
        A = np.array([[w[a+x] for a, x, b in I]], dtype='float')
        b = np.array([[1]], dtype='float')
        h = np.zeros((num+1, 1))

        return c, G, h, A, b

    @staticmethod
    def _worst_case(theta, N):
        values = []
        actions = [[(), ()] for _ in range(N)]
        I = cls.I(N)

        c = 0
        for j, (a, x, b) in enumerate(I):
                val = round(theta[j], 8)  # round theta to avoid ~0 value resources
                if val > 0:
                    values += [val/N]*N
                    ind = [(k % N) + c for k in range(2*N)]
                    for p in range(N):
                        strategies[p][0] = strategies[p][0] + tuple(ind[p:p+a+x])
                        strategies[p][1] = strategies[p][1] + tuple(ind[p+N-b:p+N+x])
                    c += N
        
        return actions, values

    @classmethod
    def worst_case_game(cls, theta, w, f):
        cls._check_args(f, w)
        actions, values = cls._worst_case(theta, len(w)-1)
        return ResourceFactory.make_game(actions, values, w, f)
