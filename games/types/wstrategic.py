#!/usr/bin/env python
# Author : Rohit Konda
# Copyright (c) 2020 Rohit Konda. All rights reserved.
# Licensed under the MIT License. See LICENSE file in the project root for full license information.

"""
Definition for a Welfare Strategic Game, where the welfare function is defined by a welfare matrix.
"""

import numpy as np
from games.types.strategic import *
from games.types.misc import WelfareGame
from typing import Union, Any, List

class WStrategicGame(StrategicGame, WelfareGame):

    """Strategic Normal Form Game with an endowed welfare function.
    
    Args:
        players (List[StrategicPlayer]): List of players in the game.
    
    Attributes:
        wmatrix (np.ndarray): Welfare matrix.
    
    """
    def __init__(self, players: List[StrategicPlayer], wmatrix: np.ndarray):
        StrategicGame.__init__(self, players)
        WelfareGame.__init__(self, players)
        self.wmatrix: np.ndarray = wmatrix

    def welfare(self, play: list, *args) -> Union[float, Any]:
        """Welfare function arising from defined welfare matrix.
        
        Args:
            play (list): Which indexes of actions are played by each player.
            *args: Here for extendability of the class.
        
        Returns:
            Union[float, Any]: Welfare of the system.
        """
        return self.wmatrix[tuple(self.all_play(play))]


class WStrategicFactory(StrategicFactory):

    """Factory class for creating a normal form game from a list of payoff matrices.
    """
    
    @classmethod
    def make_game(cls, payoffs: List[np.ndarray], welfare: np.ndarray) -> WStrategicGame:
        """Main method for game creation
        
        Args:
            payoffs (List[np.ndarray]): Payoff matrix for each player. Shape matches the number of actions for each player.
            welfare (np.ndarray): Welfare matrix.
        
        Returns:
            WStrategicGame: Welfare Strategic Normal Form Game.
        """
        cls._check_args(payoffs, welfare)
        players = [cls._make_player(i, pay) for i, pay in enumerate(payoffs)]
        return WStrategicGame(players, welfare)

    @classmethod
    def _check_args(cls, payoffs: List[np.ndarray], welfare: np.ndarray) -> None:
        """Check strategic form game is created correctly
        
        Args:
            payoffs (List[np.ndarray]): payoff matrixes for game creation.
            welfare (np.ndarray): Welfare matrix.
        
        Raises:
            ValueError: If Welfare is not same shape as payoffs
        """
        StrategicFactory._check_args(payoffs)

        if np.shape(welfare) != np.shape(payoffs[0]):
            raise ValueError('Welfare must be same shape as payoffs.')