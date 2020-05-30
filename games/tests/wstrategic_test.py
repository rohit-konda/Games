from games.types.wstrategic import WStrategicFactory
import unittest as ut
import numpy as np

class WStrategicFactory_Test(ut.TestCase):
	def test_welfare(self):
		pay1 = [np.array([[2, 0], [3, 1]]), np.array([[2, 3], [0, 1]])]
		welfare = np.array([[4, 3], [3, 2]])
		game1 = WStrategicFactory.make_game(pay1, welfare)
		
		self.assertEqual(4, game1.welfare([0, 0]))
		self.assertEqual(3, game1.welfare([0, 1]))
		self.assertEqual(3, game1.welfare([1, 0]))
		self.assertEqual(2, game1.welfare([1, 1]))

	def test_check_game(self):
		self.assertRaises(ValueError, WStrategicFactory.make_game, [np.array([[1]]), np.array([[1, 2]])], np.array([[1]]))
		self.assertRaises(ValueError, WStrategicFactory.make_game, [np.array([[1, 2]]), np.array([[1, 2]])], np.array([[1, 2, 3]]))


if __name__ == '__main__':
	ut.main()