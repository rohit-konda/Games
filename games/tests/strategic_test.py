from games.types.strategic import *
import unittest as ut
import numpy as np


class SGFactory_Test(ut.TestCase):
	def setUp(self):
		self.fact = SGFactory()
		self.pay1 = [np.array([[2, 0], [3, 1]]), np.array([[2, 3], [0, 1]])]
		self.game = self.fact.make_game(self.pay1)

	def test_make_board(self):
		self.assertisNone(self.game.board.state)

	def test_make_players(self):
		pass

	def test_check_game(self):
		pass

	def test_make_game(self):
		pd = None 


if __name__ == '__main__':
	ut.main()