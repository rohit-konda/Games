import numpy as np
from games.types.misc import FActions
from games.types.congestion import CongestionPlayer
from games.types.cong_extensions import DistResGame, WelfareCongGame
from games.types.factory import GFactory
from typing import List

class ResourcePlayer(CongestionPlayer):
    def __init__(self, name: str, index: int, actions: FActions, f: List[float], values: List[float]):
        CongestionPlayer.__init__(self, name, index, actions)
        self.f: List[float] = f
        self.values: List[float] = values

    def f_r(self, r: int, players: List[int]) -> float:
        return self.values[r] * self.f[len(players)]


class ResourceGame(DistResGame, WelfareCongGame):
    def __init__(self, players: List[ResourcePlayer], values: List[float], w: List[float], f: List[float]):
        DistResGame.__init__(self, players, values, f)
        WelfareCongGame.__init__(self, players, len(values))
        self.w: List[float]= w

    def w_r(self, r: int, players: List[int]) -> float:
        return self.values[r] * self.w[len(players)]


class ResourceFactory(GFactory):
    @classmethod
    def make_game(cls, all_actions: List[List[tuple]], values: List[float], w: List[float], f: List[float]) -> ResourceGame:
        cls._check_args(all_actions, values, w, f)
        players = [cls._make_player(i, actions, f, values) for i, actions in enumerate(all_actions)]
        return ResourceGame(players, values, w, f)

    @classmethod
    def _make_player(cls, ind: int, actions: FActions, f: List[float], values: List[float]) -> ResourcePlayer:
        name = str(ind)
        actions = FActions(actions)
        return ResourcePlayer(name, ind, actions, f, values)

    @classmethod
    def _check_args(cls, all_actions: List[List[tuple]], values: List[float], w: List[float], f: List[float]) -> None:
        if len(w) < 2:
            raise ValueError('w must be greater than length 2')
        if len(w) != len(f):
            raise ValueError('length of w must match f.')
        if len(all_actions) != len(w) - 1:
            raise ValueError('length of all_actions plus 1 must match w and f.')
