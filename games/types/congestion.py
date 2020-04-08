import numpy as np
from games.types.game import Board, NCGame, PotentialGame
from games.types.players import FActions, Player, Actions
from games.types.factory import GFactory

class CongestionGame(NCGame, WelfareGame):
    def __init__(self, players, r_m):
        NCGame.__init__(self, players)
        WelfareGame.__init__(self, players, self.board)
        self.r_m = r_m

    def w_r(self, r, players):
        raise NotImplementedError

    def pcover(self, play):
        return [(r, [i if r in pl for i, pl in enumerate(play)]) for r in range(self.r_m)]

    def welfare(self, play):
        pcover = self.pcover(play)
        return sum(map(self.w_r, pcover))


class MutableCongestionGame(CongestionGame):
    def __init__(self, players, r_m, w_r)
        CongestionGame.__init__(players, r_m)
        self._w_r = w_r

    def w_r(self, r, players):
        return self._w_r(r, players)


class ResourceGame(CongestionGame):
    def __init__(self, players, values, w):
        CongestionGame.__init__(self, players, len(values))
        self.values = values
        self.w = w

    def w_r(self, r, players):
        return self.values[r] * self.w[len(players)]


class CongestionPlayer(Player):
    def __init__(self, name, index, actions):
        Player.__init__(self, name, index, actions)

    def f_r(self, r, players):
        raise NotImplementedError

    def pcover(self, play):
        return [(r, [i if r in pl for i, pl in enumerate(play)]) for r in play[self.index]]

    def U(self, play, board):
        pcover = self.pcover(play)
        return sum(map(self.f_r, pcover))

class MutableCongestionPlayer(CongestionPlayer):
    def __init__(self, name, index, actions, f_r):
        CongestionPlayer.__init__(name, index, actions)
        self._f_r = f_r

    def f_r(self, r, players):
        return self._f_r(r, players)


class ResourcePlayer(CongestionPlayer):
    def __init__(self, name, index, actions, f, values):
        CongestionPlayer.__init__(name, index, actions)
        self.f = f
        self.values

    def f_r(self, r, players):
        return self.values[r] * self.f[len(players)]


class CongestionFactory(GFactory):
    
    def make_game(cls, actions, r_m, w_r, list_f_r):
        cls._check_game(actions, r_m, w_r, list_f_r)
        players = [cls._make_player(i, actions, f_r) for i, actions, f_r in enumerate(zip(actions, list_f_r))]
        return MutableCongestionGame(players, r_m, w_r)

    def _make_player(cls, ind, actions, f_r):
        name = str(ind)
        actions = FActions(name, actions)
        return MutableCongestionPlayer(name, ind, actions, f_r)

    def _make_board(cls):
        pass

    def _check_game(cls, actions, w_r, list_f_r):
        pass



class ResourceFactory(GFactory):
    def make_game(cls, actions, values, w, f):
        cls._check_game(actions, values, w, f)
        board = cls._make_board()
        players = [cls._make_player(i, actions, f, values) for i, actions in enumerate(actions)]
        return ResourceGame(players, values, w)

    def _make_player(cls, ind, actions, f, values):
        name = str(ind)
        actions = FActions(name, actions)
        return ResourcePlayer(name, ind, actions, f, values)

    def _make_board(cls):
        pass

    def _check_game(cls, actions, w_r, list_f_r):
        pass
 