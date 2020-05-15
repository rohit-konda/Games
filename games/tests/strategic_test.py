from games.types.strategic import *
import unittest as ut
import numpy as np
from games.make_games import get_payoff


def equalpayoffs(payoffs_1, payoffs_2):
	return all([(p1 == p2).all() for p1, p2 in zip(payoffs_1, payoffs_2)])


class StrategicFactory_Test(ut.TestCase):
	def setUp(self):
		self.pay1 = [np.array([[2, 0], [3, 1]]), np.array([[2, 3], [0, 1]])]
		self.game1 = StrategicFactory.make_game(self.pay1)

	def test_several_payoffs(self):
		pay2 = [np.array([[2, 0, 1], [3, 1, 0]]), np.array([[2, 3, 1], [0, 1, 0]])]
		game2 = StrategicFactory.make_game(pay2)
		self.assertTrue(equalpayoffs(get_payoff(game2), pay2))
		self.assertTrue([ac.actions for ac in game2.actions] == [[0, 1], [0, 1, 2]])
		pay3 = [np.array([[2, 0, 1], [3, 1, 0], [2, 3, 4]]), np.array([[2, 3, 1], [0, 1, 0], [4, 3, 2]])]
		game3 = StrategicFactory.make_game(pay3)
		self.assertTrue(equalpayoffs(get_payoff(game3), pay3))


	def test_players(self):
		players = self.game1.players
		self.assertEqual([p.name for p in players], ['0', '1'])
		self.assertEqual([a for p in players for a in p.actions], [0, 1, 0, 1])
		self.assertTrue(equalpayoffs(get_payoff(self.game1), self.pay1))
		for i in [0, 1]:
			for j in [0, 1]:
				self.assertEqual(self.game1.U_i(0, [i, j]), self.pay1[0][i, j])
				self.assertEqual(self.game1.U_i(1, [i, j]), self.pay1[1][i, j])

	def test_check_game(self):
		self.assertRaises(ValueError, StrategicFactory.make_game, [np.array([[1]]), np.array([[1, 2]])])
		self.assertRaises(ValueError, StrategicFactory.make_game, [np.array([1, 2]), np.array([1, 2])])


if __name__ == '__main__':
	ut.main()