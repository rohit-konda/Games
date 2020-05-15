from games.types.strategic import StrategicFactory
from games.types.congestion import CongestionFactory
from games.types.resource import ResourceFactory
from games.analysis.search_nash	import BruteNash


def normal_form_game(payoffs):
	return StrategicFactory.make_game(payoffs)

def congestion_game(actions, r_m, w_r, list_f_r):
	return CongestionFactory.make_game(actions, r_m, w_r, list_f_r)

def resource_game(actions, values, w, f):
	return ResourceFactory.make_game(actions, values, w, f)

def get_payoff(Game):
	return BruteNash.game_to_payoffs(Game)

def to_normal_form(Game):
	return normal_form_game(get_payoff(Game))