#!/usr/bin/env python
# Author : Rohit Konda
# Copyright (c) 2020 Rohit Konda. All rights reserved.
# Licensed under the MIT License. See LICENSE file in the project root for full license information.


"""
Shapley congestion game as defined in 'Potential Games' by Monderer, Shapley.
Difference between Congestion Game is that covering utility function is not player dependent
and only depends on number of players covering, not who covers.
"""
from games.types.congestion import CongestionGame, CongestionPlayer, MutableCGPlayer
from games.types.misc import PotentialGame, FActions
from games.types.factory import GFactory
from typing import List, Callable


class ShapleyPlayer(CongestionPlayer):
    def __init__(self, name: str, index: int, actions: FActions, fcov: Callable[[int, int], float]):
        CongestionPlayer.__init__(self, name, index, actions)
        self.fcov = fcov

    def f_r(self, r: int, players: List[int]) -> float:
        return self.fcov(r, len(players))

        
class ShapleyCGame(CongestionGame, PotentialGame):
    def __init__(self, players: List[CongestionPlayer], r_m: int):
        CongestionGame.__init__(self, players, r_m)
        PotentialGame.__init__(self, players)

    def fcov(self, r: int, ncover: int) -> float:
        raise NotImplementedError

    def potential(self, play: List[int]) -> float:
        actions = self.all_play(play)
        return sum([sum([self.f_r(i, len(c)) for c in range(cov)]) for i, cov in self.pcover(actions)])


class MutableShapleyCGame(ShapleyCGame):
    def __init__(self, players: List[CongestionPlayer], r_m: int, fcov: Callable[[int, int], float]):
        CongestionGame.__init__(self, players, r_m)
        self._fcov : Callable[[int, int], float] = fcov

    def fcov(self, r: int, ncover: int) -> float:
        return self._fcov(r, ncover)


class ShapleyFactory(GFactory):    
    @classmethod
    def make_game(cls, all_actions: List[List[List[int]]], r_m: int, fcov: Callable[[int, int], float]) -> MutableShapleyCGame:
        cls._check_args(all_actions, r_m, fcov)
        players = [cls._make_player(i, actions, fcov) for i, actions in enumerate(all_actions)]
        return MutableShapleyCGame(players, r_m, fcov)

    @classmethod
    def _make_player(cls, ind: int, actions: List[List[int]], fcov: Callable[[int, int], float]) -> ShapleyPlayer:
        name = str(ind)
        actions = FActions(actions)
        return ShapleyPlayer(name, ind, actions, fcov)

    @classmethod
    def _check_args(cls, all_actions: List[List[List[int]]], r_m: int, fcov: Callable[[int, int], float]) -> None:
        pass