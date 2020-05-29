from games.types.misc import FActions
import unittest as ut


class TestFActions(ut.TestCase):
	def test_FActions(self):
		name = 'p1'
		actions = [1, 2]
		fact = FActions(actions)
		self.assertEqual(fact(0), 1)
		self.assertEqual(fact[0], 1)
		self.assertEqual([i for i in fact], actions)
		self.assertEqual(len(fact), 2)
		self.assertRaises(IndexError, fact, 2)

if __name__ == '__main__':
	ut.main()