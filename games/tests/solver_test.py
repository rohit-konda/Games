import unittest as ut
from games.misc.solver import *


class LP_Test(ut.TestCase):
	def test_lp(self):
		c = [-4., -5.]
		G = [[2., 1., -1., 0.], [1., 2., 0., -1.]]
		h = [3., 3., 0., 0.]
		self.assertEqual(round(lp('cvxopt', c, G, h)['min']), -9)
		c = [1.]
		G = [-1.]
		h = [0.]
		self.assertEqual(round(lp('cvxopt', c, G, h)['min']), 0)
		G = [-1. , 1]
		h = [0., -1]
		self.assertWarns(Warning, lp, 'cvxopt', c, G, h)

class SolverWrapper_Test(ut.TestCase):
	def test_check_solver(self):
		def nosolver(): SolverWrapper('', False)
		self.assertRaises(ImportError, nosolver)
		cvxsol = SolverWrapper('cvxopt', False)
		self.assertEqual(cvxsol.solver, 'cvxopt')

	def test_lp(self):
		cvxsol = SolverWrapper('cvxopt', False)
		c = [-4., -5.]
		G = [[2., 1., -1., 0.], [1., 2., 0., -1.]]
		h = [3., 3., 0., 0.]
		self.assertEqual(round(cvxsol.lp(c, G, h, None, None)['min']), -9)

if __name__ == '__main__':
	ut.main()