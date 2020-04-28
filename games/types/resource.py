import numpy as np
from games.types.misc import WelfareGame
from games.types.congestion import CongestionGame, CongestionPlayer
from games.types.factory import GFactory


class ResourceFactory(GFactory):
    def make_game(cls, all_actions, values, w, f):
        cls._check_args(actions, values, w, f)
        players = [cls._make_player(i, actions, f, values) for i, actions in enumerate(all_actions)]
        return ResourceGame(players, values, w)

    def _make_player(cls, ind, actions, f, values):
        name = str(ind)
        actions = FActions(name, actions)
        return ResourcePlayer(name, ind, actions, f, values)

    def _check_args(cls, all_actions, values, w, f):
        pass


class ResourceGame(CongestionGame):
    def __init__(self, players, values, w):
        CongestionGame.__init__(self, players, len(values))
        self.values = values
        self.w = w

    def w_r(self, r, players):
        return self.values[r] * self.w[len(players)]


class ResourcePlayer(CongestionPlayer):
    def __init__(self, name, index, actions, f, values):
        CongestionPlayer.__init__(name, index, actions)
        self.f = f
        self.values = values

    def f_r(self, r, players):
        return self.values[r] * self.f[len(players)]


class WelfareCongGame(CongestionGame, WelfareGame):
    def __init__(self, players, r_m):
        CongestionGame.__init__(self, players, r_m)
        WelfareGame.__init__(self, players)

    def w_r(self, r, players):
        raise NotImplementedError

    def welfare(self, play):
        pcover = self.pcover(play)
        return sum(map(self.w_r, range(self.r_m), pcover))


class MutableWCGame(WelfareCongGame):
    def __init__(self, players, r_m, w_r):
        WelfareCongGame.__init__(self, players, r_m)
        self._w_r = w_r

    def w_r(self, r, players):
        return self._w_r(r, players)