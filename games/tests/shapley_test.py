from games.types.shapley import *
from games.tests.strategic_test import equalpayoffs
from games.make_games import get_payoff
import unittest as ut
import numpy as np

class Shapley_Test(ut.TestCase):
	def setUp(self):
		def fcov(r, ncover): return 2*ncover
		self.args1 = [[[[0, 1], [1]], [[0], [1]]], 2, fcov]

	def test_make_game(self):
		game1 = ShapleyFactory.make_game(*self.args1)
		self.assertTrue(equalpayoffs(get_payoff(game1), [np.array([[6., 6.], [2., 4.]]), np.array([[4., 4.], [2., 4.]])]))

	def test_potential(self):
		game1 = ShapleyFactory.make_game(*self.args1)
		# test alignment of potential function
		self.assertEqual(game1.potential([0, 0]) - game1.potential([1, 0]), game1.U_i(0, [0, 0]) - game1.U_i(0, [1, 0]))
		self.assertEqual(game1.potential([0, 1]) - game1.potential([1, 1]), game1.U_i(0, [0, 1]) - game1.U_i(0, [1, 1]))
		self.assertEqual(game1.potential([0, 0]) - game1.potential([0, 1]), game1.U_i(1, [0, 0]) - game1.U_i(1, [0, 1]))
		self.assertEqual(game1.potential([1, 0]) - game1.potential([1, 1]), game1.U_i(1, [1, 0]) - game1.U_i(1, [1, 1]))

	def test_make_players(self):
		p1 = ShapleyFactory._make_player(0, self.args1[0][0], self.args1[2])
		self.assertEqual(p1.name, '0')
		self.assertEqual(p1.index, 0)
		self.assertEqual(p1.actions.actions, [[0, 1], [1]])
		self.assertListEqual([p1.fcov(0, e) for e in range(4)], [0, 2, 4, 6])

if __name__ == '__main__':
	ut.main()