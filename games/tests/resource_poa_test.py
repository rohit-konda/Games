import unittest as ut
import numpy as np
from games.analysis.resource_poa import ResourcePoA


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
		self.assertRaises(ValueError, ResourcePoA._check_f())

if __name__ == '__main__':
	ut.main()