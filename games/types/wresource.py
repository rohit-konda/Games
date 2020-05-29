#!/usr/bin/env python
# Author : Rohit Konda
# Copyright (c) 2020 Rohit Konda. All rights reserved.
# Licensed under the MIT License. See LICENSE file in the project root for full license information.

import numpy as np
from games.types.misc import FActions, WelfareGame
from games.types.congestion import CongestionGame, CongestionPlayer
from games.types.resource import ResourcePlayer, ResourceGame
from games.types.factory import GFactory
from typing import List, Tuple


class WelfareCongGame(CongestionGame, WelfareGame):
    def __init__(self, players: CongestionPlayer, r_m: int):
        CongestionGame.__init__(self, players, r_m)
        WelfareGame.__init__(self, players)

    def w_r(self, r: int, players: List[int]) -> float:
        raise NotImplementedError

    def welfare(self, play: List[int]) -> float:
        actions = self.all_play(play)
        pcover = [list(e) for e in zip(*self.pcover(actions))]
        return sum(map(self.w_r, *pcover))


class WResourceGame(ResourceGame, WelfareCongGame):
    def __init__(self, players: List[ResourcePlayer], values: List[float], w: List[float], f: List[float]):
        ResourceGame.__init__(self, players, values, f)
        WelfareCongGame.__init__(self, players, len(values))
        self.w: List[float]= w

    def w_r(self, r: int, players: List[int]) -> float:
        return self.values[r] * self.w[len(players)]


class WResourceFactory(GFactory):
    @classmethod
    def make_game(cls, all_actions: List[List[List[int]]], values: List[float], w: List[float], f: List[float]) -> WResourceGame:
        cls._check_args(all_actions, values, w, f)
        players = [cls._make_player(i, actions, f, values) for i, actions in enumerate(all_actions)]
        return WResourceGame(players, values, w, f)

    @classmethod
    def _make_player(cls, ind: int, actions: FActions, f: List[float], values: List[float]) -> ResourcePlayer:
        name = str(ind)
        actions = FActions(actions)
        return ResourcePlayer(name, ind, actions, f, values)

    @classmethod
    def _check_args(cls, all_actions: List[List[List[int]]], values: List[float], w: List[float], f: List[float]) -> None:
        if len(w) < 2:
            raise ValueError('w must be greater than length 2')
        if len(w) != len(f):
            raise ValueError('length of w must match f.')
        if len(all_actions) != len(w) - 1:
            raise ValueError('length of all_actions plus 1 must match w and f.')
