from games.analysis.search_nash import BruteNash, BrutePoA
from games.make_games import normal_form_game
from games.tests.strategic_test import equalpayoffs
from games.types.wstrategic import WStrategicFactory
from games.types.equilibrium import PureEq
import unittest as ut
import numpy as np

class BruteNash_Test(ut.TestCase):
	def setUp(self):
		self.prisoner_dilemma = [np.array([[2, 0], [3, 1]]), np.array([[2, 3], [0, 1]])]

	def test_game_to_payoffs(self):
		pd_game = normal_form_game(self.prisoner_dilemma)
		payoffs = BruteNash.game_to_payoffs(pd_game)
		self.assertTrue(equalpayoffs(payoffs, self.prisoner_dilemma))

	def test_find_nash(self):
		self.assertSequenceEqual(BruteNash.find_nash(self.prisoner_dilemma)[0].play, (1, 1))


class BrutePoA_Test(ut.TestCase):
	def setUp(self):
		self.prisoner_dilemma = [np.array([[2, 0], [3, 1]]), np.array([[2, 3], [0, 1]])]
		self.pd_welfare = np.array([[4, 3], [3, 2]])
		self.game1 = WStrategicFactory.make_game(self.prisoner_dilemma, self.pd_welfare)

	def test_game_to_welfare(self):
		self.assertTrue(equalpayoffs([BrutePoA.game_to_welfare(self.game1)], [np.array([[4., 3.], [3., 2.]])]))

	def test_set_poas(self):
		self.assertEqual(BrutePoA.set_poas([PureEq([1, 1]), PureEq([0, 1])], self.pd_welfare), (.5, .75))

	def test_get_arg_opt(self):
		self.assertEqual(BrutePoA.get_argopt(self.pd_welfare), (0, 0))

if __name__ == '__main__':
	ut.main()