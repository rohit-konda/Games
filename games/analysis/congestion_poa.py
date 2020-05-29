#!/usr/bin/env python
# Author : Rohit Konda
# Copyright (c) 2020 Rohit Konda. All rights reserved.
# Licensed under the MIT License. See LICENSE file in the project root for full license information.

import numpy as np
from typing import List, Callable, Tuple

class CongestionPoA:
    def primal_poa(cls, flist: List[Callable[[List[int]], float]], w: Callable[[List[int]], float]) -> Tuple[np.ndarray, ...]:
        def nash_func(j: int, Na: List[int], Nb: List[int], Nx: List[int]) -> int:
            if j in Na:
                return flist[j](Na + Nx)
            elif j in Nb:
                return -flist[j](Na + Nx + [j])
            else:
                return 0

        cls.check_args(w, flist)
        
        n = cls.n
        n_c = 4**n - 1
        partition = list(product([1, 2, 3, 4], repeat=n))[:-1]

        c = np.zeros((n_c,), dtype='float')
        cons_1 = np.zeros((n, n_c), dtype='float')
        A = np.zeros((1, n_c), dtype='float')
        for i, p in enumerate(partition):
            Na = [k for k in range(n) if p[k]==1]
            Nx = [k for k in range(n) if p[k]==2]
            Nb = [k for k in range(n) if p[k]==3]

            c[i] = -w(Nb + Nx)
            A[0, i] = w(Na + Nx)
            
            for j in range(n):
                cons_1[j][i] = nash_func(j, Na, Nb, Nx)

        cons_2 = np.identity(n_c)
        G = -np.vstack((cons_1, cons_2))
        h = np.zeros((n_c+n, 1))
        b = np.array([[1]], dtype='float')
        
        return c, G, h, A, b

    def check_args(cls, w: Callable[[List[int]], float], flist: List[Callable[[List[int]], float]]) -> None:
        pass


    def worst_case(cls, theta: List[float] , N: int) -> Tuple[List[float], List[List[tuple]]]:
        """ get worst case instance """
        values = []
        actions = [[(), ()] for _ in range(N)]
        partition = list(product([1, 2, 3, 4], repeat=n))[:-1]

        c = 0
        for i, t in enumerate(theta):
            val = round(t, 7) # round theta to avoid ~0 value resources
            if  val > 0:
                values.append(val)
                for j in range(N):
                    if partition[i][j] == 1:
                        strategies[j][0] += (c,)
                    elif partition[i][j] == 2:
                        strategies[j][0] += (c,)
                        strategies[j][1] += (c,)
                    elif partition[i][j] == 3:
                        strategies[j][1] += (c,)
                c += 1

        return values, actions
