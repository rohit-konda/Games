from games.types.resource import ResourceFactory
from games.make_games import get_payoff
from games.tests.strategic_test import equalpayoffs
import unittest as ut
import numpy as np


class ResourceFactory_Test(ut.TestCase):
	def setUp(self):
		game1_kwargs = {'all_actions' : [[[0, 1], [1]], [[0], [1]]],
		'values' : [2, 1],
		'f' : [0, 1, 2]}
		self.game1 = ResourceFactory.make_game(**game1_kwargs)

	def test_make_game(self):
		g1 = self.game1
		pay1 = [np.array([[5., 4.], [1., 2.]]), np.array([[4., 2.], [2., 2.]])]
		self.assertTrue(equalpayoffs(get_payoff(g1), pay1))

	def test_make_players(self):
		p_gm1 = self.game1.players[0]
		self.assertEqual(p_gm1.name, '0')
		self.assertListEqual(p_gm1.actions.actions, [[0, 1], [1]])
		self.assertEqual(p_gm1.f, self.game1.f)
		self.assertEqual(p_gm1.values, self.game1.values)

	def test_resource_player(self):
		p_gm1 = self.game1.players[0]
		self.assertEqual(p_gm1.f_r(0, [0, 1]), 4)
		self.assertEqual(p_gm1.f_r(1, [0]), 1)
		self.assertEqual(p_gm1.U([(0, 1), (0, 1)]), 6)
		self.assertEqual(p_gm1.U([(0,), (0, 1)]), 4)
		self.assertEqual(p_gm1.U([(0,), (1,)]), 2)
		self.assertEqual(p_gm1.U([(0, 1), (1,)]), 4)

	def test_check_args(self):
		gmargs = [[[()], [()]], [0], [0]]
		self.assertRaises(ValueError, ResourceFactory.make_game, *gmargs)
		gmargs[2] = [0, 1]
		self.assertRaises(ValueError, ResourceFactory.make_game, *gmargs)
		gmargs[2] = [0, 1, 2]
		gmargs[0] += [[()]]
		self.assertRaises(ValueError, ResourceFactory.make_game, *gmargs)
		gmargs[2] = [0, 1, 2, 3]
		try:
			ResourceFactory.make_game(*gmargs)
		except Exception as e:
			self.fail('make game failed with correct all_actions and f')


if __name__ == '__main__':
	ut.main()