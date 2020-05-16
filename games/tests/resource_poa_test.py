import unittest as ut
import numpy as np
from games.analysis.resource_poa import ResourcePoA
from games.misc.solver import lp


class ResourcePoA_Test(ut.TestCase):
	def test_I(self):
		self.assertEqual(ResourcePoA.I(0), [])
		self.assertListEqual(ResourcePoA.I(1), [(0, 0, 1), (0, 1, 0), (1, 0, 0)])
		self.assertEqual(len(ResourcePoA.I(4)), 34)

	def test_Ir(self):
		self.assertEqual(ResourcePoA.I_r(0), [])
		self.assertListEqual(ResourcePoA.I_r(2), [(0, 2, 0), (0, 1, 1), (1, 1, 0), (0, 0, 2), (1, 0, 0), (0, 0, 1), (1, 0, 1), (0, 1, 0), (2, 0, 0)])
		self.assertEqual(len(ResourcePoA.I_r(5)), 51)

	def test_check_w(self):
		self.assertRaises(ValueError, ResourcePoA._check_w, [])
		self.assertRaises(ValueError, ResourcePoA._check_w, [1, 1])
		self.assertRaises(ValueError, ResourcePoA._check_w, [0, 1, -1])

	def test_check_f(self):
		self.assertRaises(ValueError, ResourcePoA._check_args, [], [0, 1, 1])
		self.assertRaises(ValueError, ResourcePoA._check_args, [1, 1, 1], [0, 1, 1])
		self.assertRaises(ValueError, ResourcePoA._check_args, [0, -1, 1], [0, 1, 1])

	def test_poa(self):
		c, G, h = ResourcePoA.function_poa([0, 1, 1])
		print(lp('cvxopt', c, G, h)['argmin'])


if __name__ == '__main__':
	ut.main()