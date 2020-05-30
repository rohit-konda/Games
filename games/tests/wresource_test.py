from games.types.wresource import WResourceFactory
from games.make_games import get_payoff
from games.tests.strategic_test import equalpayoffs
from games.analysis.search_nash import BrutePoA
import unittest as ut
import numpy as np


class WResourceFactory_Test(ut.TestCase):
	def setUp(self):
		def f_r(r, players): return len(players)
		game1_kwargs = {'all_actions' : [[[0, 1], [1]], [[0], [1]]],
		'values' : [2, 1],
		'f' : [0, 1, 2],
		'w' : [0, 1, 1]}
		self.game1 = WResourceFactory.make_game(**game1_kwargs)

	def test_make_game(self):
		g1 = self.game1
		w1 = np.array([[3., 3.], [3., 1.]])
		pay1 = [np.array([[5., 4.], [1., 2.]]), np.array([[4., 2.], [2., 2.]])]
		self.assertTrue((w1 == BrutePoA.game_to_welfare(g1)).all())
		self.assertTrue(equalpayoffs(get_payoff(g1), pay1))

	def test_make_players(self):
		p_gm1 = self.game1.players[0]
		self.assertEqual(p_gm1.name, '0')
		self.assertListEqual(p_gm1.actions.actions, [[0, 1], [1]])
		self.assertEqual(p_gm1.f, self.game1.f)
		self.assertEqual(p_gm1.values, self.game1.values)

	def test_resource_player(self):
		p_gm1 = self.game1.players[0]
		self.assertEqual(p_gm1.f_r(0, [0, 1]), 4)
		self.assertEqual(p_gm1.f_r(1, [0]), 1)
		self.assertEqual(p_gm1.U([(0, 1), (0, 1)]), 6)
		self.assertEqual(p_gm1.U([(0,), (0, 1)]), 4)
		self.assertEqual(p_gm1.U([(0,), (1,)]), 2)
		self.assertEqual(p_gm1.U([(0, 1), (1,)]), 4)

	def test_welfare(self):
		gm1 = self.game1
		self.assertEqual(gm1.w_r(0, [0, 1]), 2)
		self.assertEqual(gm1.w_r(1, [0]), 1)
		self.assertEqual(gm1.welfare([0, 1]), 3)
		self.assertEqual(gm1.welfare([1, 0]), 3)
		self.assertEqual(gm1.welfare([1, 1]), 1)

	def test_check_args(self):
		gmargs = [[[()], [()]], [0], [0], [0, 1, 2]]
		self.assertRaises(ValueError, WResourceFactory.make_game, *gmargs)
		gmargs[2] = [0, 1]
		self.assertRaises(ValueError, WResourceFactory.make_game, *gmargs)
		gmargs[2] = [0, 1, 2]
		gmargs[0] += [[()]]
		self.assertRaises(ValueError, WResourceFactory.make_game, *gmargs)

if __name__ == '__main__':
	ut.main()