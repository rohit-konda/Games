#!/usr/bin/env python
# Author : Rohit Konda
# Copyright (c) 2020 Rohit Konda. All rights reserved.
# Licensed under the MIT License. See LICENSE file in the project root for full license information.

"""
Module for creating a Congestion Game with relevant player definitions.
"""
import numpy as np
from games.types.game import Game, Player
from games.types.misc import FActions
from games.types.factory import GFactory
from typing import List, Tuple, Callable


class CongestionPlayer(Player):

    """ A player in a congestion game. 

    Args:
        name (str): Label for the player.
        index (int): Index for the player for easy reference in a list of players in a game.
        actions (FActions): Actions object that the player can take. Action is subset of power set of {1, ..., number of resources}.
    """
    
    def __init__(self, name: str, index: int, actions: FActions):
        Player.__init__(self, name, index, actions)

    def f_r(self, r: int, players: List[int]) -> float:
        """Utility given if covering the resource r when others are covering the resource as well.
        
        Args:
            r (int): Which resource under consideration.
            players (List[int]): Players including self that are covering resource r.
        
        Raises:
            NotImplementedError: Needs to be implemented.

        Returns:
            float: Utility gained from the covering that resource.
        """
        raise NotImplementedError

    def pcover(self, actions: List[List[int]]) -> List[Tuple[int, List[int]]]:
        return [(r, [i for i, ac in enumerate(actions) if r in ac]) for r in actions[self.index]]

    def U(self, actions: List[List[int]]) -> float:
        pcover = [list(e) for e in zip(*self.pcover(actions))]
        return sum(map(self.f_r, *pcover))


class MutableCGPlayer(CongestionPlayer):
    def __init__(self, name: str, index: int, actions: FActions, f_r: List[float]):
        CongestionPlayer.__init__(self, name, index, actions)
        self._f_r = f_r

    def f_r(self, r: int, players: List[int]) -> float:
        return self._f_r(r, players)


class CongestionGame(Game):    
    def __init__(self, players: List[CongestionPlayer], r_m: int):
        Game.__init__(self, players)
        self.r_m = r_m

    def pcover(self, actions: List[List[int]]) -> List[Tuple[int, List[int]]]:
        return [(r, [i for i, pl in enumerate(actions) if r in pl]) for r in range(self.r_m)]


class CongestionFactory(GFactory):
    @classmethod
    def make_game(cls, all_actions: List[List[List[int]]], r_m: int, list_f_r: List[Callable[[int, List[int]], float]]) -> CongestionGame:

        cls._check_args(all_actions, r_m, list_f_r)
        players = [cls._make_player(i, actions, f_r) for i, (actions, f_r) in enumerate(zip(all_actions, list_f_r))]
        return CongestionGame(players, r_m)

    @classmethod
    def _make_player(cls, ind: int, actions: List[List[int]], f_r: Callable[[int, List[int]], float]) -> MutableCGPlayer:
        name = str(ind)
        actions = FActions(actions)
        return MutableCGPlayer(name, ind, actions, f_r)

    @classmethod
    def _check_args(cls, all_actions: List[List[List[int]]], r_m: int, list_f_r: List[Callable[[int, List[int]], float]]) -> None:
        if len(list_f_r) != len(all_actions):
            raise ValueError('Length of all_actions must match the length of list_f_r.')
