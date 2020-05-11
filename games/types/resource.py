import numpy as np
from games.types.misc import WelfareGame, FActions
from games.types.congestion import CongestionGame, CongestionPlayer, ShapleyCGame
from games.types.factory import GFactory


class WelfareCongGame(CongestionGame, WelfareGame):
    def __init__(self, players, r_m):
        CongestionGame.__init__(self, players, r_m)
        WelfareGame.__init__(self, players)

    def w_r(self, r, players):
        raise NotImplementedError

    def welfare(self, play):
        all_play = self.all_play(play)
        pcover = self.pcover(all_play)
        return sum(map(self.w_r, range(self.r_m), pcover))


class MutableWCGame(WelfareCongGame):
    def __init__(self, players, r_m, w_r):
        WelfareCongGame.__init__(self, players, r_m)
        self._w_r = w_r

    def w_r(self, r, players):
        return self._w_r(r, players)


class ResourceFactory(GFactory):
    def make_game(cls, all_actions, values, w, f):
        cls._check_args(all_actions, values, w, f)
        players = [cls._make_player(i, actions, f, values) for i, actions in enumerate(all_actions)]
        return ResourceGame(players, values, w, f)

    def _make_player(cls, ind, actions, f, values):
        name = str(ind)
        actions = FActions(actions)
        return ResourcePlayer(name, ind, actions, f, values)

    def _check_args(cls, all_actions, values, w, f):
        if type(w) != list:
            raise TypeError('w must be a list.')
        if type(f) != list:
            raise TypeError('f must be a list.')
        if type(all_actions) != list:
            raise TypeError('all_actions must be a list.')
        if len(w) < 2:
            raise ValueError('w must be greater than length 2')
        if len(w) != len(f):
            raise ValueError('length of w must match f.')
        if len(all_actions) != len(w) - 1:
            raise ValueError('length of all_actions plus 1 must match w and f.')
        if type(all_actions[0]) != list:
            raise ValueError('actions in all_actions must be a list.')
        if type(all_actions[0][0]) != tuple:
            raise ValueError('actions for each player must be a tuple of resources.')


class DistResGame(ShapleyCGame):
    def __init__(self, players, values, f):
        ShapleyCGame.__init__(self, players, len(values))
        self.values = values
        self.f = f

    def f_r(self, r, ncover):
        raise self.values[r] * self.f[ncover]


class ResourceGame(DistResGame, WelfareCongGame):
    def __init__(self, players, values, w, f):
        DistResGame.__init__(self, players, values, f)
        WelfareCongGame.__init__(self, players, len(values))
        self.w = w

    def w_r(self, r, players):
        return self.values[r] * self.w[len(players)]


class ResourcePlayer(CongestionPlayer):
    def __init__(self, name, index, actions, f, values):
        CongestionPlayer.__init__(self, name, index, actions)
        self.values = values
        self.f = f

    def f_r(self, r, players):
        return self.values[r] * self.f[len(players)]