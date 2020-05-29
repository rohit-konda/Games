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
		w = [0., 1, 1, 1]
		f = [0., 1, 0, 0]
		
		optf = [0., 1., .43, .29]
		c, G, h = ResourcePoA.function_poa(w)
		rpoaf = [0.] + lp('cvxopt', c, G, h)['argmin'][1:]
		rpoaf = [round(e, 2) for e in rpoaf]
		self.assertEqual(rpoaf, optf)

		c, G, h = ResourcePoA.dual_poa(f, w)
		d_poa = 1./lp('cvxopt', c, G, h)['min']
		self.assertEqual(round(d_poa, 3), .5)

		c, G, h, A, b = ResourcePoA.primal_poa(f, w)
		p_poa = -1./lp('cvxopt', c, G, h, A, b)['min']
		self.assertEqual(round(p_poa, 3), .5)

	def test_worst_case(self):
		w = [0., 1, 1]
		f = [0., 1, 0]
		c, G, h, A, b = ResourcePoA.primal_poa(f, w)
		theta = lp('cvxopt', c, G, h, A, b)['argmin']
		ResourcePoA.TOL =  5
		actions, values = ResourcePoA.worst_case(theta, 2)
		self.assertEqual(actions, [[(2,), (1, 3)], [(3,), (0, 2)]])
		self.assertEqual(values, [0.5, 0.5, 0.5, 0.5])


if __name__ == '__main__':
	ut.main()