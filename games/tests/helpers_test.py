import unittest as ut
from games.misc.helpers import *


class Helpers_Test(ut.TestCase):
	def test_powerset(self):
		ps = [i for i in powerset((1, 2))]
		self.assertEqual(ps, [(), (1,), (2,), (1, 2)])

	def test_verify_game(self):
		

if __name__ == '__main__':
	ut.main()