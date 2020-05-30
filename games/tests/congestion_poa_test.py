import unittest as ut
import numpy as np
from games.analysis.congestion_poa import CongestionPoA
from games.misc.solver import lp

class CongestionPoA_Test(ut.TestCase):
	def setUp(self):
		wr = [0, 1, 1, 1]
		fr = [0, 1, 0, 0]
		n = 3
		def w(players) : return wr[len(players)]
		def f(players) : return fr[len(players)]
		list_f = [f]*n
		self.args1 = [n, w, list_f]
		fr2 = [0., 1., .43, .29]
		def f2(players) : return fr2[len(players)]
		list_f2 = [f2]*n
		self.args2 = [n, w, list_f2]
		n = 2
		wr2 = [0, 1, 1]
		fr3 = [0, 1, 0]
		def w2(players) : return wr2[len(players)]
		def f3(players) : return fr3[len(players)]
		list_f3 = [f3]*n
		self.args3 = [n, w2, list_f3]

	def test_primal_poa(self):
		c, G, h, A, b = CongestionPoA.primal_poa(*self.args1)
		sol = lp('cvxopt', c, G, h, A, b)
		self.assertEqual(round(-1./sol['min'], 4), .5)
		
		c, G, h, A, b = CongestionPoA.primal_poa(*self.args2)
		sol2 = lp('cvxopt', c, G, h, A, b)
		self.assertEqual(round(-1./sol2['min'], 4), .6329)


	def test_worst_case(self):
		n = self.args3[0]
		c, G, h, A, b = CongestionPoA.primal_poa(*self.args3)
		theta = lp('cvxopt', c, G, h, A, b)['argmin']
		CongestionPoA.TOL = 4
		actions, values = CongestionPoA.worst_case(theta, n)
		self.assertEqual(actions, [[(0,), (1, 2)], [(1,), (0, 3)]])
		self.assertEqual(values, [0.5, 0.5, 0.5, 0.5])

	def test_check_args(self):
		n, w, list_f2 = tuple(self.args1)
		f2mod = list_f2 + list_f2
		self.assertRaises(ValueError, CongestionPoA.primal_poa, n, w, f2mod)


if __name__ == '__main__':
	ut.main()