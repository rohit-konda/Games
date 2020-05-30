#!/usr/bin/env python
# Author : Rohit Konda
# Copyright (c) 2020 Rohit Konda. All rights reserved.
# Licensed under the MIT License. See LICENSE file in the project root for full license information.

"""
Module for calculating price of anarchy for a general class of congestion games, where 
U_i(a) = sum over resources ( value of resource * C_i(players that cover resource r))
"""

import numpy as np
from itertools import product
from typing import List, Callable, Tuple

class CongestionPoA:

    """ PoA Calculation for a general class of congestion games. 
    Results in an LP with 4^n constraints, with n being the number of players.
    
    Attributes:
        TOL (int): Significant figure for rounding to 0.
    """
    
    TOL = 8

    @classmethod
    def primal_poa(cls, n: int, w: Callable[[List[int]], float], flist: List[Callable[[List[int]], float]]) -> Tuple[np.ndarray, ...]:
        """ Primal program for calculating the price of anarcy in a congestion game.
        
        Args:
            n (int): Number of players in game.
            w (Callable[[List[int]], float]): What players are covering resource -> utility for the system.
            flist (List[Callable[[List[int]], float]]): What players are covering resource -> Utility for player i, for i in the list.
        
        Returns:
            Tuple[np.ndarray, ...]: LP Parameters for getting PoA calculations.
        """
        def nash_func(j: int, Na: List[int], Nb: List[int], Nx: List[int]) -> float:
            """Used to define the nash constraints for the LP Program.
            
            Args:
                j (int): Which player under consideration
                Na (List[int]): What players are covering in nash allocation.
                Nb (List[int]): What players are covering in the optimal allocation.
                Nx (List[int]): What players are covering in both allocations.
            
            Returns:
                float: Utility gained from covering.
            """
            if j in Na:
                return flist[j](Na + Nx)
            elif j in Nb:
                return -flist[j](Na + Nx + [j])
            else:
                return 0

        cls._check_args(n, w, flist)
        
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

    @classmethod
    def _check_args(cls, n: int, w: Callable[[List[int]], float], flist: List[Callable[[List[int]], float]]) -> None:
        """check given parameters to see if they are valid.
        
        Args:
            n (int): Number of players in game.
            w (Callable[[List[int]], float]): What players are covering resource -> utility for the system.
            flist (List[Callable[[List[int]], float]]): What players are covering resource -> Utility for player i, for i in the list.
        
        Raises:
            ValueError: if the length of the flist doesn't match number of players.
        """
        if n != len(flist):
            raise ValueError('flist must have length matching n.')

    @classmethod
    def worst_case(cls, theta: List[float], N: int) -> Tuple[List[float], List[List[tuple]]]:
        """Gives list of player actions and values of the worst case congestion game that attains PoA.
        
        Args:
            theta (List[float]): values associated with each allocation type - given by the primal program for PoA.
            N (int): Number of players.
        
        Returns:
            Tuple[List[float], List[List[tuple]]]: (actions: list of possible actions for each player, values: value of each resource in list)
        """
        values = []
        actions = [[(), ()] for _ in range(N)]
        partition = list(product([1, 2, 3, 4], repeat=N))[:-1]

        c = 0
        for i, t in enumerate(theta):
            val = round(t, cls.TOL) # round theta to avoid ~0 value resources
            if  val > 0:
                values.append(val)
                for j in range(N):
                    if partition[i][j] == 1:
                        actions[j][0] += (c,)
                    elif partition[i][j] == 2:
                        actions[j][0] += (c,)
                        actions[j][1] += (c,)
                    elif partition[i][j] == 3:
                        actions[j][1] += (c,)
                c += 1

        return actions, values
