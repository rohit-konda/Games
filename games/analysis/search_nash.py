#!/usr/bin/env python
# Author : Rohit Konda
# Copyright (c) 2020 Rohit Konda. All rights reserved.
# Licensed under the MIT License. See LICENSE file in the project root for full license information.

import numpy as np
from itertools import product
from games.types.equilibrium import PureEq
from games.types.game import Game
from games.types.misc import WelfareGame
import numpy as np
from typing import List


class BruteNash:

    """Collection of methods for brute force calculation of Nash equilibrium in noncooperative games.
    
    Attributes:
        TOLERANCE (float): Numerical tolerance for float point comparisons.
    """
    
    TOLERANCE = 10**-8

    @staticmethod
    def game_to_payoffs(game: Game) -> List[np.ndarray]:
        """Turn a noncooperative game into strategic form through calculation of payoff arrays.
        
        Args:
            game (Game): Noncooperative game, all players must have a finite number of actioms.
        
        Returns:
            List[np.ndarray]: List of payoff arrays defining the game.
        """
        num_act = [len(ac) for ac in game.actions]
        payoffs = [None]*game.N
        for i, player in enumerate(game.players):
            payoff_i = np.zeros(num_act)
            # generate all possible types of action indices
            for a in product(*[range(n_i) for n_i in num_act]):
                payoff_i[a] = game.U_i(i, a)
            payoffs[i] = payoff_i
        return payoffs

    @classmethod
    def find_NCnash(cls, game: Game, add=True) -> List[PureEq]:
        """Find nash equilibrium of a specified noncooperative game through brute force search.
        
        Args:
            game (Game): Noncooperative Game with finite action sets.
            add (bool, optional): Whether to add the calculated equilibrium to Game.eq member.
        
        Returns:
            List[PureEq]: List of calculated Nash equilibrium.
        """
        eq = find_nash(cls.game_to_payoffs(game))
        if add:
            game.eq += eq
        return eq

    @classmethod
    def find_nash(cls, payoffs: List[np.ndarray]) -> List[PureEq]:
        """Find nash equilibrium of specified list of payoff matrices through brute force search.
        
        Args:
            payoffs (List[np.ndarray]): List of payoff arrays defining the utilities of the game.
        
        Returns:
            List[PureEq]: List of calculated Nash equilibrium.
        """
        cpnes = list(np.argwhere(payoffs[0] > np.amax(payoffs[0], 0) - cls.TOLERANCE))
        cpnes = [tuple(cpne) for cpne in cpnes]
        N = len(payoffs)
        
        for i in range(1, N):
            pm = payoffs[i]
            for cpne in cpnes[:]:
                ind = cpne[:i] + (slice(None),) + cpne[i+1:]
                if pm[cpne] < np.max(pm[ind]) - cls.TOLERANCE:
                    cpnes.pop(cpnes.index(cpne))
        
        return [PureEq(cpne) for cpne in cpnes]


class BrutePoA:
    @staticmethod
    def game_to_welfare(game: WelfareGame):
        num_act = [len(ac) for ac in game.actions]
        welfare = np.zeros(num_act)
        # generate all possible types of action indices
        for a in product(*[range(n_i) for n_i in num_act]):
            welfare[a] = game.welfare(a)
        return welfare

    @staticmethod
    def set_poas(list_pureeq, welfare):
        pne_welfare = [welfare[pne.play] for pne in list_pureeq]
        opt = np.max(welfare)
        price_ratios = [float(pne)/opt for pne in pne_welfare]
        return min(price_ratios), max(price_ratios)

    @staticmethod
    def get_argopt(welfare): 
        return np.unravel_index(np.argmax(welfare), welfare.shape)
