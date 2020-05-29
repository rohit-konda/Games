from games.types.congestion import *
from games.make_games import get_payoff
from games.tests.strategic_test import equalpayoffs
import unittest as ut
import numpy as np

class Congestion_Test(ut.TestCase):
	def setUp(self):
		def f_r(r, players): return len(players)
		self.game1 = {'all_actions' : [[[0, 1], [1]], [[0], [1]]],
		'r_m' : 2,
		'list_f_r' : [f_r, f_r]}

	def test_make_game(self):
		game = CongestionFactory.make_game(**self.game1)
		self.assertTrue(equalpayoffs(get_payoff(game), [np.array([[3., 3.], [1., 2.]]), np.array([[2., 2.], [1., 2.]])]))

	def test_pcover(self):
		game = CongestionFactory.make_game(**self.game1)
		self.assertEqual(game.pcover([[0], [0, 1]]), [(0, [0, 1]), (1, [1])])

	def test_make_players(self):
		g1 = self.game1
		player1 = CongestionFactory._make_player(0, g1['all_actions'][0], g1['list_f_r'][0])
		self.assertEqual(player1.name, '0')
		self.assertEqual(player1.index, 0)
		self.assertEqual(player1.actions.actions, [[0, 1], [1]])

	def test_cong_player(self):
		g1 = self.game1
		player = CongestionFactory._make_player(0, g1['all_actions'][0], g1['list_f_r'][0])
		actions  = [(0, 2), (0, 1)]
		self.assertEqual(player.pcover(actions), [(0, [0, 1]), (2, [0])])
		actions2 = [(0, 1, 2), (0, 1)] 
		self.assertEqual(player.pcover(actions2), [(0, [0, 1]), (1, [0, 1]), (2, [0])])
		self.assertEqual(player.U(actions), 3)
		self.assertEqual(player.U(actions2), 5)


if __name__ == '__main__':
	ut.main()