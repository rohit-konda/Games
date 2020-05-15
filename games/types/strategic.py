#!/usr/bin/env python
# Author : Rohit Konda
# Copyright (c) 2020 Rohit Konda. All rights reserved.
# Licensed under the MIT License. See LICENSE file in the project root for full license information.

"""
Object definitions for a strategic normal form game directly through payoff matrices.
Includes factory methods for normal form game creation.
"""
import numpy as np
from itertools import product
from games.types.game import Game, Player, Actions
from games.types.misc import FActions
from games.types.factory import GFactory
from typing import List


class StrategicGame(Game):

    """ Strategic Normal Form Game. Inherits from game.types.Game.

    Args:
        players (List[Player]): List of players in the game.
    """
    
    def __init__(self, players: List[Player]):
        Game.__init__(self, players)


class StrategicPlayer(Player):

    """ Player in a normal form game. Inherits from games.types.Player.
    
    Args:
        name (str): Label for the player.
        index (int): Index for the player for easy reference in a list of players in a game.
        actions (Actions): Actions object that the player can take.
        payoff (np.ndarray): Payoff matrix determining the utility function.

    Attributes:
        payoff (np.ndarray): Payoff matrix determining the utility function.
    """
    
    def __init__(self, name: str, index: int, actions: Actions, payoff: np.ndarray):
        Player.__init__(self, name, index, actions)
        self.payoff: np.ndarray = payoff

    def U(self, actions: list) -> float:
        """ Utility function based on a predefined payoff matrix.
        
        Args:
            actions (list): List of actions that each player in the game has taken.
        
        Returns:
            float: Utility of the player.
        """
        return self.payoff[tuple(actions)]


class StrategicFactory(GFactory):

    """ Factory class for creating a normal form game from a list of payoff matrices.
    """
    
    @classmethod
    def make_game(cls, payoffs: List[np.ndarray]) -> StrategicGame:
        """ Main method for game creation
        
        Args:
            payoffs (List[np.ndarray]): Payoff matrix for each player. Shape matches the number of actions for each player.
        
        Returns:
            StrategicGame: Strategic Normal Form Game.
        """
        cls._check_args(payoffs)
        players = [cls._make_player(i, pay) for i, pay in enumerate(payoffs)]
        return StrategicGame(players)
    
    @classmethod
    def _make_player(cls, ind: int, payoff: np.ndarray) -> StrategicPlayer:
        """ Method for creating players in a game.
        
        Args:
            ind (int): Index for each player.
            payoff (np.ndarray): Payoff matrix for defining the utility of the player.
        
        Returns:
            StrategicPlayer: Player in the strategic normal form game.
        """
        actions = FActions([i for i in range(np.shape(payoff)[ind])])
        return StrategicPlayer(str(ind), ind, actions, payoff)

    @classmethod
    def _check_args(cls, payoffs: List[np.ndarray]) -> None:
        """ Check strategic form game is created correctly
        
        Args:
            payoffs (List[np.ndarray]): payoff matrixes for game creation.
        
        Raises:
            ValueError: If payoffs length and dimension don't match or if the shapes of payoff matrices don't match.
        """
        if payoffs[0].ndim != len(payoffs):
            raise ValueError('Dimension of each payoff array in payoffs must equal len(payoffs).')
        if not all([np.shape(pay) == np.shape(payoffs[0]) for pay in payoffs]): 
            raise ValueError('Payoff arrays must be of the same shape.')