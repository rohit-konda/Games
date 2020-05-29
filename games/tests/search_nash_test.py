from games.analysis.search_nash import BruteNash, BrutePoA
from games.make_games import normal_form_game
import unittest as ut
import numpy as np

class BruteNash_Test(ut.TestCase):
	def setUp(self):
		self.prisoner_dilemma = [np.array([[2, 0], [3, 1]]), np.array([[2, 3], [0, 1]])]

	def test_game_to_payoffs(self):
		pd_game = normal_form_game(self.prisoner_dilemma)
		payoffs = BruteNash.game_to_payoffs(pd_game)
		self.assertTrue(self.equalpayoffs(payoffs, self.prisoner_dilemma))

	def test_find_nash(self):
		self.assertSequenceEqual(BruteNash.find_nash(self.prisoner_dilemma)[0].play, (1, 1))
	
	def equalpayoffs(self, payoffs_1, payoffs_2):
		return all([(p1 == p2).all() for p1, p2 in zip(payoffs_1, payoffs_2)])


class BrutePoA_Test(ut.TestCase):
	pass


if __name__ == '__main__':
	ut.main()