import numpy as np
from itertools import product
from games.types.game import Game, Player
from games.types.misc import FActions
from games.types.factory import GFactory


class StrategicFactory(GFactory):
    def make_game(cls, payoffs):
        cls._check_args(payoffs)
        players = [cls._make_player(i, pay) for i, pay in enumerate(payoffs)]
        return StrategicGame(players)

    def _make_player(cls, ind, payoff):
        actions = FActions([i for i in range(np.shape(payoff)[ind])])
        return StrategicPlayer(str(ind), ind, actions, payoff)

    def _check_args(cls, payoffs):
        if type(payoffs) != list:
            raise TypeError('payoffs must be a list.')
        if not all([isinstance(pay, np.ndarray) for pay in payoffs]):
            raise ValueError('Each element in payoffs must be a numpy array.')
        if payoffs[0].ndim != len(payoffs):
            raise ValueError('Payoff array dimension must match number of elements in payoffs')
        if not all([np.shape(pay) == np.shape(payoffs[0]) for pay in payoffs]): 
            raise ValueError('Payoff arrays must be of the same shape.')


class StrategicGame(Game):
    def __init__(self, players):
        Game.__init__(self, players)


class StrategicPlayer(Player):
    def __init__(self, name, index, actions, payoff):
        Player.__init__(self, name, index, actions)
        self.payoff = payoff

    def U(self, play):
        return self.payoff[tuple(play)]
