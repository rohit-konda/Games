#!/usr/bin/env python
# Author : Rohit Konda
# Copyright (c) 2020 Rohit Konda. All rights reserved.
# Licensed under the MIT License. See LICENSE file in the project root for full license information.

from warnings import warn
from typing import Dict, Any
import numpy as np

def lp(solver, c: np.ndarray, G: np.ndarray, h: np.ndarray, A: np.ndarray=None, b: np.ndarray=None, progress: bool=False) -> Dict[str, Any]:
    wrapper = SolverWrapper(solver, progress)
    return wrapper.lp(c, G, h, A, b)


class SolverWrapper:
    SUPPORTED = ['cvxopt']
    LP_SUPPORTED = ['cvxopt']

    def __init__(self, solver: str, progress: bool):
        self.solver = solver
        self.check_solver(solver)
        self.progress = progress
        self.returnall = False
    
    def lp(self, c: np.ndarray, G: np.ndarray, h: np.ndarray, A: np.ndarray, b: np.ndarray) -> Dict[str, Any]:
        if self.solver == 'cvxopt':
            from cvxopt import matrix
            from cvxopt.solvers import lp
            
            c = matrix(c)
            G = matrix(G)
            h = matrix(h)
            A = matrix(A) if A is not None else None
            b = matrix(b) if b is not None else None
            sol = lp(c, G, h, A, b, options={'show_progress': self.progress})
            if sol['status'] != 'optimal':
                warn('no feasible solution found')
            else:
                if self.returnall:
                    return sol
                else:
                    return {'min': sol['primal objective'], 'argmin': list(sol['x'])}
        else:
            raise ImportError('Not a valid or implemented lp solver. Supported lp solvers include ' + ', '.join(self.LP_SUPPORTED) + '.')

    def check_solver(self, solver: str) -> None:
        if self.solver == 'cvxopt':
            pass
        else:
            raise ImportError('Not a valid or implemented solver. Supported solvers include ' + ', '.join(self.SUPPORTED) + '.')