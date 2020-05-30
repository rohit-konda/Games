import unittest as ut
from games.misc.helpers import *
from games.types.game import Game, Player, Actions


class Helpers_Test(ut.TestCase):
	def test_powerset(self):
		ps = [i for i in powerset((1, 2))]
		self.assertEqual(ps, [(), (1,), (2,), (1, 2)])

	def test_verify_game(self):
		self.assertRaises(ValueError, verify_player_list, Game([]))
		self.assertRaises(ValueError, verify_player_list, Game([Player('0', 0, Actions()), Player('1', 2, Actions())]))

if __name__ == '__main__':
	ut.main()