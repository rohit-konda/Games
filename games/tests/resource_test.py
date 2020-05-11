from games.types.resource import ResourceFactory
from games.make_games import get_payoff
from games.tests.strategic_test import equalpayoffs
from games.analysis.search_nash import BrutePoA
import unittest as ut
import numpy as np


class ResourceFactory_Test(ut.TestCase):
	def setUp(self):
		def f_r(r, players): return len(players)
		self.rfac = ResourceFactory()
		self.game1 = {'all_actions' : [[(0, 1), (1,)], [(0,), (1,)]],
		'values' : [2, 1],
		'f' : [0, 1, 2],
		'w' : [0, 1, 1]}

	def test_make_game(self):
		g1 = self.game1
		game = self.rfac.make_game(**g1)
		self.assertTrue((np.array([[3., 3.], [3., 1.]]) == BrutePoA().game_to_welfare(game)).all())
		self.assertTrue(self.equalpayoffs(get_payoff(game), [np.array([[5., 4.], [1., 2.]]), np.array([[4., 2.], [2., 2.]])]))

	def test_make_players(self):
		'''
		g1 = self.game1
		player1 = self.rfac._make_player(0, g1['actions'][0], g1['f'][0])
		self.assertEqual(player1.name, '0')
		self.assertEqual(player1.index, 0)
		self.assertEqual(player1.actions.actions, [(0, 1), (1,)])
		'''

	def equalpayoffs(self, payoffs_1, payoffs_2):
		return all([(p1 == p2).all() for p1, p2 in zip(payoffs_1, payoffs_2)])

if __name__ == '__main__':
	ut.main()