#!/usr/bin/env python
# Author : Rohit Konda
# Copyright (c) 2020 Rohit Konda. All rights reserved.
# Licensed under the MIT License. See LICENSE file in the project root for full license information.

from games.types.congestion import CongestionGame, CongestionPlayer, MutableCGPlayer
from games.types.misc import PotentialGame
from games.types.factory import GFactory
from typing import List, Callable

        
class ShapleyCGame(CongestionGame, PotentialGame):
    def __init__(self, players: List[CongestionPlayer], r_m: int):
        CongestionGame.__init__(self, players, r_m)
        PotentialGame.__init__(self, players)

    def f_r(self, r: int, ncover: int) -> float:
        raise NotImplementedError

    def potential(self, play: List[int]) -> float:
        actions = self.all_play(play)
        return sum([sum([self.f_r(i, len(c)) for c in range(cov)]) for i, cov in self.pcover(actions)])


class MutableShapleyCGame(ShapleyCGame):
    def __init__(self, players: List[CongestionPlayer], r_m: int, f_r: Callable[[int, int], float]):
        CongestionGame.__init__(self, players, r_m)
        self._f_r : Callable[[int, int], float] = f_r

    def f_r(self, r: int, ncover: int) -> float:
        return self._f_r(r, ncover)


class ShapleyFactory(GFactory):    
    @classmethod
    def make_game(cls, all_actions: List[List[List[int]]], r_m: int, f_r: Callable[[int, List[int]], float]) -> MutableShapleyCGame:
        cls._check_args(all_actions, r_m, f_r)
        players = [cls._make_player(i, actions, f_r) for i, (actions, f_r) in enumerate(zip(all_actions, list_f_r))]
        return MutableShapleyCGame(players, r_m, f_r)

    @classmethod
    def _make_player(cls, ind: int, actions: List[List[int]], f_r: Callable[[int, List[int]], float]) -> MutableCGPlayer:
        name = str(ind)
        actions = FActions(actions)
        return MutableCGPlayer(name, ind, actions, f_r)

    @classmethod
    def _check_args(cls, all_actions: List[List[List[int]]], r_m: int, f_r: Callable[[int, List[int]], float]) -> None:
        pass