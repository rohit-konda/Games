#!/usr/bin/env python
# Author : Rohit Konda
# Copyright (c) 2020 Rohit Konda. All rights reserved.
# Licensed under the MIT License. See LICENSE file in the project root for full license information.

"""
Class definitions for a distributed resource allocation game.
Utility is defined as sum over resources covered (value of resource * f(number of players covering))
"""
from games.types.congestion import CongestionPlayer
from games.types.shapley import ShapleyCGame
from games.types.factory import GFactory
from typing import List, Tuple
import numpy as np
from games.types.misc import FActions


class ResourcePlayer(CongestionPlayer):
    def __init__(self, name: str, index: int, actions: FActions, f: List[float], values: List[float]):
        CongestionPlayer.__init__(self, name, index, actions)
        self.f: List[float] = f
        self.values: List[float] = values

    def f_r(self, r: int, players: List[int]) -> float:
        return self.values[r] * self.f[len(players)]


class ResourceGame(ShapleyCGame):
    def __init__(self, players: List[CongestionPlayer], values: List[float], f: List[float]):
        ShapleyCGame.__init__(self, players, len(values))
        self.values = values
        self.f = f

    def fcov(self, r: int, ncover: int) -> float:
        raise self.values[r] * self.f[ncover]


class ResourceFactory(GFactory):
    @classmethod
    def make_game(cls, all_actions: List[List[List[int]]], values: List[float], f: List[float]) -> ResourceGame:
        cls._check_args(all_actions, values, f)
        players = [cls._make_player(i, actions, f, values) for i, actions in enumerate(all_actions)]
        return ResourceGame(players, values, f)

    @classmethod
    def _make_player(cls, ind: int, actions: FActions, f: List[float], values: List[float]) -> ResourcePlayer:
        name = str(ind)
        actions = FActions(actions)
        return ResourcePlayer(name, ind, actions, f, values)

    @classmethod
    def _check_args(cls, all_actions: List[List[List[int]]], values: List[float], f: List[float]) -> None:
        if len(all_actions) != len(f) - 1:
            raise ValueError('length of all_actions plus 1 must match f.')