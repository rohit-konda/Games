from games.types.congestion import *
import unittest as ut
import numpy as np


class CongestionFactory_Test(ut.TestCase):
	def setUp(self):
		all_actions = [[(0,), (1,)], [(0,), (1,)]]
		r_m = 2
		def f_r(r, players): return len(players)
		list_of_f_r = [f_r, f_r]
		w_r

	def test_make_game(self):
		pass

	def test_make_players(self):
		pass


if __name__ == '__main__':
	ut.main()