import numpy as np
from games.types.game import Game, Player
from games.types.misc import FActions, PotentialGame, WelfareGame
from games.types.factory import GFactory


class CongestionFactory(GFactory):
    def make_game(cls, all_actions, r_m, list_f_r):
        cls._check_args(all_actions, r_m, list_f_r)
        players = [cls._make_player(i, actions, f_r) for i, actions, f_r in enumerate(zip(all_actions, list_f_r))]
        return MutableCongestionGame(players, r_m, w_r)

    def _make_player(cls, ind, actions, f_r):
        name = str(ind)
        actions = FActions(actions)
        return MutableCongestionPlayer(name, ind, actions, f_r)

    def _check_args(cls, all_actions, r_m, list_f_r):

        N = len(all_actions)


class CongestionGame(PotentialGame):
    def __init__(self, players, r_m):
        PotentialGame.__init__(self, players)
        self.r_m = r_m

    def pcover(self, play):
        return [[i for i, pl in enumerate(play) if r in pl] for r in range(self.r_m)]

    def potential(self, play):
        pass




class CongestionPlayer(Player):
    def __init__(self, name, index, actions):
        Player.__init__(self, name, index, actions)

    def f_r(self, r, players):
        raise NotImplementedError

    def pcover(self, play):
        return [(r, [i for i, pl in enumerate(play) if r in pl]) for r in play[self.index]]

    def U(self, play):
        pcover = zip(*self.pcover(play))
        return sum(map(self.f_r, *tuple([i for i in map(list, pcover)])))

class MutableCGPlayer(CongestionPlayer):
    def __init__(self, name, index, actions, f_r):
        CongestionPlayer.__init__(self, name, index, actions)
        self._f_r = f_r

    def f_r(self, r, players):
        return self._f_r(r, players)

"""
#all_actions = [, [(0,), (1,)]]
r_m = 2
def f_r(r, players): return len(players)

pl1 = MutableCGPlayer('1', 0, FActions([(0,), (1,)]), f_r)
pl2 = MutableCGPlayer('2', 1, FActions([(0,), (1,)]), f_r)
def w_r(r, players): return len(players)
c = MutableWCGame([pl1, pl2], 2, w_r)
print(pl1.U([(0, 1), (0,)]))
"""