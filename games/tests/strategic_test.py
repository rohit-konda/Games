from games.types.strategic import *
import unittest as ut
import numpy as np


class SGFactory_Test(ut.TestCase):
	def setUp(self):
		self.fact = SGFactory()
		self.pay1 = [np.array([[2, 0], [3, 1]]), np.array([[2, 3], [0, 1]])]
		self.game = self.fact.make_game(self.pay1)

	def test_make_board(self):
		self.assertIsNone(self.game._board.state)

	def test_players(self):
		players = self.game.players
		self.assertEqual([p.name for p in players], ['0', '1'])
		self.assertEqual([a for p in players for a in p.actions], [0, 1, 0, 1])
		for i in [0, 1]:
			for j in [0, 1]:
				self.assertEqual(self.game.U_i(0, [i, j]), self.pay1[0][i, j])
				self.assertEqual(self.game.U_i(1, [i, j]), self.pay1[1][i, j])

	def test_check_game(self):
		self.assertRaises(TypeError, self.fact.make_game, None)
		self.assertRaises(ValueError, self.fact.make_game, [1, 1, 1])
		self.assertRaises(ValueError, self.fact.make_game, [np.array([[1]]), np.array([[1, 2]])])
		self.assertRaises(ValueError, self.fact.make_game, [np.array([1, 2]), np.array([1, 2])])


if __name__ == '__main__':
	ut.main()