from games.types.congestion import *
from games.make_games import get_payoff
from games.tests.strategic_test import equalpayoffs
import unittest as ut
import numpy as np

class CongestionFactory_Test(ut.TestCase):
	def setUp(self):
		def f_r(r, players): return len(players)
		self.cfac = CongestionFactory()
		self.game1 = {'all_actions' : [[(0, 1), (1,)], [(0,), (1,)]],
		'r_m' : 2,
		'list_f_r' : [f_r, f_r]}

	def test_make_game(self):
		g1 = self.game1
		game = self.cfac.make_game(**g1)
		self.assertTrue(equalpayoffs(get_payoff(game), [np.array([[3., 3.], [1., 2.]]), np.array([[2., 2.], [1., 2.]])]))

	def test_make_players(self):
		g1 = self.game1
		player1 = self.cfac._make_player(0, g1['all_actions'][0], g1['list_f_r'][0])
		self.assertEqual(player1.name, '0')
		self.assertEqual(player1.index, 0)
		self.assertEqual(player1.actions.actions, [(0, 1), (1,)])

if __name__ == '__main__':
	ut.main()