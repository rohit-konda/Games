from Games.basic import *
from Games.res.directPoA import *
from Games.res.incomplete import *
from Games.res.resource import *
from prettytable import PrettyTable
from itertools import product
from math import factorial, exp

# functions 

def w(n): return [0] + [1]*n  # welfare for covering games
def mf(n): return [0, 1] + [0]*(n-1)  # marginal distribution rule
def sf(n): return [0] + [1./j for j in range(1,n+1)]  # Shapley distribution rule
# gairing distribution rule for infinite n
def gf(n): return [0] + [factorial(j-1)/(exp(1)-1)*(exp(1) - sum([1./factorial(i) for i in range(j)])) for j in range(1, n+1)]
# gairing distribution rule for finite n
def gnf(n):
	def c2(j): return sum([1./factorial(i) for i in range(j, n)])
	c1 = 1./(factorial(n-1)*(n-1))
	return [0] + [factorial(j-1)*(c1 + c2(j))/(c1 + c2(1)) for j in range(1, n+1)]


# set up calculation 

games = []
functions = [mf, sf, gf, gnf]
fnames = ['Marginal', 'Shapley', 'Gairing', 'Finite_Gairing']
graphs = [
[[1], [0]],
[[1], []],
[[], []],
[[1, 2], [0, 2], [0, 1]],
[[1], [0, 2], [0, 1]],
[[], [0, 2], [0, 1]],
[[1], [0], [0, 1]],
[[1], [2], [0, 1]],
[[2], [2], [0, 1]],
[[2], [0], [0, 1]],
[[1], [0], [1]],
[[1], [2], [1]],
[[2], [0], [0]],
[[2], [0], []],
[[], [2], [0]],
[[], [2], [1]],
[[1], [], []],
[[], [], []],
[[1, 2, 3], [0, 2, 3], [0, 1, 3], [0, 1, 2]],
[[2, 3], [0, 2, 3], [0, 1, 3], [0, 1, 2]],
[[3], [0, 2, 3], [0, 1, 3], [0, 1, 2]],
[[2, 3], [0, 2, 3], [0, 3], [0, 1, 2]],
[[2, 3], [2, 3], [0, 1, 3], [0, 1, 2]],
[[], [0, 2, 3], [0, 1, 3], [0, 1, 2]],
[[1, 2], [0, 2, 3], [1, 3], [0, 1, 2]],
[[1, 2], [0, 2], [0, 3], [0, 1, 2]],
[[2, 3], [0, 2, 3], [0, 3], [0, 2]],
[[1, 2], [0, 3], [3], [0, 1, 2]],
[[1], [0, 2, 3], [0, 1], [0, 2]],
[[1], [0, 3], [0, 1], [1, 2]],
[[1], [0, 3], [0, 1], []],
[[2], [2, 3], [3], [2]],
[[1, 2], [], [], []],
[[1], [0], [], []],
[[1], [], [], []],
[[], [], [], []],
[[1, 2, 3, 4], [0, 2, 3, 4], [0, 1, 3, 4], [0, 1, 2, 4], [0, 1, 2, 3]],
[[2, 3, 4], [2, 3, 4], [0, 1, 3, 4],  [0, 1, 2, 4], [0, 1, 2, 3]],
[[1, 2, 3, 4], [2, 3, 4], [1, 3, 4], [0, 1, 2, 4], [1, 2, 3]],
[[3, 4], [2, 3, 4], [0, 1, 3, 4], [0, 1, 2, 4], [0, 1, 2, 3]],
[[1, 2, 3], [2, 3, 4], [3, 4], [0, 1, 2, 4], [0, 1, 3]],
[[1, 2, 3, 4], [0, 4], [0, 1, 3, 4], [0, 1], [0, 1, 2, 3]],
[[1, 2, 3, 4,], [0, 2, 3, 4], [0, 1, 3], [0, 1, 2], [3]],
[[1, 2, 3], [0, 2], [0, 1], [1, 2], [0, 1]],
[[1, 2, 3], [0, 2], [0, 1], [], []],
[[1, 2], [0], [], [], []],
[[1], [0], [], [], [0]],
[[], [], [], [], []],
]

graphs = [
[[1, 2], [0, 2], [0, 1]],
[[1], [0, 2], [0, 1]],
[[], [0, 2], [0, 1]],
[[1], [0], [0, 1]],
[[1], [2], [0, 1]],
[[2], [2], [0, 1]],
[[2], [0], [0, 1]],
[[1], [0], [1]],
[[1], [2], [1]],
[[2], [0], [0]],
[[2], [0], []],
[[], [2], [0]],
[[], [2], [1]],
[[1], [], []],
[[], [], []],
]

types = product(graphs, [0])

#t = PrettyTable(['n', 'graph', 'dist_func', 'PoA', 'values', 'strategies'])
t = PrettyTable(['n', 'graph', 'dist_func', 'PoA'])

for e in types:
	graph = e[0]
	N = len(graph)
	dist = functions[e[1]](N)
	fname = fnames[e[1]]
	welfare = w(N)
	game = ResInfoPoaGame([i for i in range(N)], [[(), ()] for _ in range(N)], [0], welfare, dist, graph)
	#print(graph)
	try:
		poa, sol = game.primal_poa()
		gam = DistResGame(*sol)
		val = gam.values
		strat = gam.strategies
		#t.add_row([N, graph, fname, poa, val, strat])
		t.add_row([N, graph, fname, poa])
	except Exception as e:
		#t.add_row([N, graph, fname, '-', '-', '-'])
		t.add_row([N, graph, fname, '-'])
print(t)
