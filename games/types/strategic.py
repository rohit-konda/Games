import numpy as np
from itertools import product
from games.types.game import Board, NCGame
from games.types.players import FActions, Player
from games.types.factory import GFactory


class SGGame(NCGame):
    def __init__(self, players):
        NCGame.__init__(self, players)

    def __repr__(self):
        return 'Strategic ' + NCGame.__repr__(self)


class SGPlayer(Player):
    def __init__(self, name, index, actions, payoff):
        Player.__init__(self, name, index, actions)
        self.payoff = payoff

    def U(self, play, board):
        return self.payoff[tuple(play)]


class SGFactory(GFactory):

    def make_game(cls, payoffs):
        cls._check_game(payoffs)
        players = [cls._make_player(i, pay) for i, pay in enumerate(payoffs)]
        return SGGame(players)

    def _make_board(cls):
        pass

    def _make_player(cls, ind, payoff):
        name = str(ind)
        actions = FActions(name, [i for i in range(np.shape(payoff)[ind])])
        return SGPlayer(name, ind, actions, payoff)

    def _check_game(cls, payoffs):
        try:
            iter(payoffs)
        except TypeError:
            raise TypeError('Payoffs must be of type iterable.')
        if not all([isinstance(pay, np.ndarray) for pay in payoffs]):
            raise ValueError('Each element in payoffs must be a numpy array.')
        if payoffs[0].ndim != len(payoffs):
            raise ValueError('Payoff array dimension must match number of elements in payoffs')
        if not all([np.shape(pay) == np.shape(payoffs[0]) for pay in payoffs]): 
            raise ValueError('Payoff arrays must be of the same shape.')
