from games.types.strategic import *
import unittest as ut
import numpy as np


class SGFactory_Test(ut.TestCase):
	def setUp(self):
		self.fact = SGFactory()
		self.pay1 = [np.array([[2, 0], [3, 1]]), np.array([[2, 3], [0, 1]])]

	def test_make_board(self):
		board = self.fact._make_board()
		self.assertTrue(board.state is None)
		

	def test_make_game(self):
		pd = self.fact.make_game(self.pay1)


if __name__ == '__main__':
	ut.main()