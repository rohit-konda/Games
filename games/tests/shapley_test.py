from games.types.shapley import *
from games.tests.strategic_test import equalpayoffs
import unittest as ut
import numpy as np

class Congestion_Test(ut.TestCase):
	def setUp(self):
		def fcov(r, ncover): return 2*ncover
		self.args1 = [[[[0, 1], [1]], [[0], [1]]], 2, fcov]

	def test_make_game(self):
		game1 = S

if __name__ == '__main__':
	ut.main()