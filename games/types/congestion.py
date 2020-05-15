import numpy as np
from games.types.game import Game, Player
from games.types.misc import FActions
from games.types.factory import GFactory


class CongestionPlayer(Player):
    def __init__(self, name, index, actions):
        Player.__init__(self, name, index, actions)

    def f_r(self, r, players):
        raise NotImplementedError

    def pcover(self, actions):
        return [(r, [i for i, ac in enumerate(actions) if r in ac]) for r in actions[self.index]]

    def U(self, actions):
        pcover = zip(*self.pcover(actions))
        return sum(map(self.f_r, *tuple([i for i in map(list, pcover)])))


class CongestionGame(Game):
    def __init__(self, players, r_m):
        Game.__init__(self, players)
        self.r_m = r_m

    def pcover(self, actions):
        return [[i for i, pl in enumerate(actions) if r in pl] for r in range(self.r_m)]


class CongestionFactory(GFactory):
    @classmethod
    def make_game(cls, all_actions, r_m, list_f_r):
        cls._check_args(all_actions, r_m, list_f_r)
        players = [cls._make_player(i, actions, f_r) for i, (actions, f_r) in enumerate(zip(all_actions, list_f_r))]
        return CongestionGame(players, r_m)

    @classmethod
    def _make_player(cls, ind, actions, f_r):
        name = str(ind)
        actions = FActions(actions)
        return MutableCGPlayer(name, ind, actions, f_r)

    @classmethod
    def _check_args(cls, all_actions, r_m, list_f_r):
        N = len(list_f_r)


