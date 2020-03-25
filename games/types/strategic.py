import numpy as np
from itertools import product
from games.types.game import Board, NCGame
from games.types.players import FActions, Player
from games.types.factory import GFactory

class SGFactory(GFactory):

    class SGGame(NCGame):
        def __init__(self, players, board):
            NCGame.__init__(self, players, board)

    def make_game(cls, payoffs):
        cls._check_game(payoffs)
        board = cls._make_board()
        players = [cls._make_player(i, pay) for i, pay in enumerate(payoffs)]
        return SGGame(players, board)

    def _make_player(cls, ind, payoff):
        name = str(ind)
        actions = FActions(name, [i for i in range(np.shape(payoff)[ind])])
        def util(play, Board):
            return payoff[tuple(play)]
        return Player(name, ind, actions, util)

    def _make_board(cls):
        return Board(None)

    def _check_game(cls, payoffs):
        try:
            iter(payoffs)
        except TypeError:
            raise TypeError('Payoffs must be of type iterable.')
        if not all([isinstance(pay, np.ndarray) for pay in payoffs]):
            raise ValueError('Each element in payoffs must be a numpy array.')
        if not all([np.shape(pay) == np.shape(payoffs[0]) for pay in payoffs]): 
            raise ValueError('Payoff arrays must be of the same shape.')