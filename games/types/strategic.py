import numpy as np
from itertools import product
from games.types.game import Board, FiniteGame
from games.types.players import FActions, Player
from games.types.factory import GFactory


class SGGame(NCGame):
    def __init__(self, players, board):
        NCGame.__init__(self, players, board)

class SGFactory(GFactory):
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


def game_to_payoffs(game):
    if not isinstance(game, NCGame):
        raise ValueError('game must be of type NCGame')

    num_act = [len(p.actions) for p in game.players]
    payoffs = [None]*game.N
    for i, player in enumerate(game.players):
        payoff_i = np.zeros(num_act)
        # generate all possible types of action indices
        for a in product(*[range(n_i) for n_i in num_act]):
            play = [game.players[i].actions[j] for i, j in enumerate(a)]
            payoff_i[a] = game.U_i(i, play)
        payoffs[i] = payoff_i
    return payoffs