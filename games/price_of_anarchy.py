from games.analysis.congestion_poa import *
from games.analysis.search_nash import *
from games.misc.solver import lp


def find_nash(game):
	return BruteNash.find_NCnash(game)


def brute_argopt(game):
	welfare = BrutePoA.game_to_welfare(game)
	return BrutePoA.get_argopt(welfare)


def brute_opt(game):
	return np.max(BrutePoA.game_to_welfare(game))


def brute_poa(game):
	nash = BruteNash.find_nash(game)
	welfare = BrutePoA.game_to_welfare(game)
	return BrutePoA.set_poas(nash, welfare)


def res_poa(f, w, solver):
	return 1./lp(solver, ResourcePoA.dual_poa(f, w))['min']


def res_opt_f(w, solver):
	sol = lp(solver, ResourcePoA.function_poa(w))
	f = [0.] + sol['argmin'][1:]
	poa = 1./sol['min']
	return poa, f


def worst_game(f, w, solver):
	theta = lp(solver, ResourcePoA.primal_poa(f, w))['argmin']
	N = len(f)
	actions, values = ResourcePoA.worst_case(theta, N)
	return 


def cong_poa(flist, w, solver):
	return 1./lp(solver, CongestionPoA.primal_poa(flist, w))['min']


def cong_worst_game(flist, w, solver):
	theta = lp(solver, CongestionPoA.primal_poa(flist, w))['argmin']
	N = len(w)
	return CongestionPoA.worst_case(theta, N)