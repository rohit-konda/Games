from games.types.congestion import CongestionGame, CongestionPlayer
from games.types.misc import WelfareGame, PotentialGame


class MutableCGPlayer(CongestionPlayer):
    def __init__(self, name, index, actions, f_r):
        CongestionPlayer.__init__(self, name, index, actions)
        self._f_r = f_r

    def f_r(self, r, players):
        return self._f_r(r, players)

        
class ShapleyCGame(CongestionGame, PotentialGame):
    def __init__(self, players, r_m):
        CongestionGame.__init__(self, players, r_m)
        PotentialGame.__init__(self, players)

    def f_r(self, r, ncover):
        raise NotImplementedError

    def potential(self, play):
        actions = self.all_play(play)
        return sum([sum([self.f_r(i, len(c)) for c in range(cov)]) for i, cov in enumerate(self.pcover(actions))])


class DistResGame(ShapleyCGame):
    def __init__(self, players, values, f):
        ShapleyCGame.__init__(self, players, len(values))
        self.values = values
        self.f = f

    def f_r(self, r, ncover):
        raise self.values[r] * self.f[ncover]


class WelfareCongGame(CongestionGame, WelfareGame):
    def __init__(self, players, r_m):
        CongestionGame.__init__(self, players, r_m)
        WelfareGame.__init__(self, players)

    def w_r(self, r, players):
        raise NotImplementedError

    def welfare(self, play):
        actions = self.all_play(play)
        pcover = self.pcover(actions)
        return sum(map(self.w_r, range(self.r_m), pcover))



class MutableWCGame(WelfareCongGame):
    def __init__(self, players, r_m, w_r):
        WelfareCongGame.__init__(self, players, r_m)
        self._w_r = w_r

    def w_r(self, r, players):
        return self._w_r(r, players)