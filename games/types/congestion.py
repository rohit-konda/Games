import numpy as np
from games.types.game import Board, NCGame
from games.types.players import FActions, Player
from games.types.factory import GFactory

class CongestionFactory(GFactory):

    class CongestionGame(NCGame):
        def __init__(self, players, board, r_m):
            NCGame.__init__(self, players, board)
            self.r_m = r_m
	
	def make_game(cls, F, W, ):
	    cls._check_game(F, W)
	    board = cls._make_board()
	    players = [cls._make_player(i)]
	    return Game(players, board)

    def _make_player(cls, ind):
		pass

    def _make_board(cls):
        return Board(None)

    def _check_game(cls):
		if not (isinstance(F, np.ndarray) and isinstance(W, np.ndarray)):
            raise TypeError('Each element in payoffs must be a numpy array.')




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
            raise TypeError('Each element in payoffs must be a numpy array.')
        if not all([np.shape(pay) == np.shape(payoffs[0]) for pay in payoffs]): 
            raise ValueError('Payoff arrays must be of the same shape.')








    def player_cover(self, strategies):
        """ returns list of which players are covering the resource """
        return [[j for j in range(self.n) if i in strategies[j]] for i in range(self.r_m)]



def U_i(self, i, strategy):
    """ utility for the strategy for player i """
    strategy_i = list(strategy[i])
    p_cover = self.player_cover(strategy)
    return sum([self.f_r(i, j, p_cover[j]) for j in strategy_i])

def f_r(self, i, res, players):
    """ function design for the utility function depends on what resource,
    and what players are covering it """
    pass

self.w = w  # w(j) welfare basis function ((n+1,) np.array)
self.f = f  # f(j) design function for the utility ((n+1,) np.array)

self.values = values  # values (v_r) associated with each resource

Wr = np.dot(np.diag(values), np.array([w] * len(values)))  # Wr(j) = v_r * w(j)
Fr = np.dot(np.diag(values), np.array([f] * len(values)))  # Fr(j) = v_r * f(j)

def w_r(self, res, players):
    """ welfare function, returns a scalar value dependent on the resource and which players select it """
    pass
