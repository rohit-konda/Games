from games.types.strategic import SGFactory
from games.types.congestion import CongestionFactory, ResourceFactory


def payoff_game(payoffs):
	return SGFactory().make_game(payoffs)

def congestion_game(actions, r_m, w_r, list_f_r):
	return CongestionFactory().make_game(actions, r_m, w_r, list_f_r)

def resource_game(actions, values, w, f):
	return ResourceFactory.make_game(actions, values, w, f)