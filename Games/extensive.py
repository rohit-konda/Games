#!/usr/bin/env python
"""
Network and Extensive Form Games class definitions 
"""

from Games.basic import *


class NetworkGame(Game):
    """ framework for games that are based on a network"""
    def __init__(self, payoffs, players, strategies, network):
        Game.__init__(self, payoffs, players, strategies)
        self.network = network  # directed network of the game (dictionary of {node: to other nodes})


class ExtensiveGame(Game):
	"""Extensive Form of a Game"""
	def __init__(self, game_tree, players, info_set):
		Game.__init__(self, None, players, None)
		self.game_tree = game_tree
		self.info_set = info_set
		self.set_strategies()

	def set_strategies(self):
		"""set strategies based on the extensive form """
		strategies = {}
		for player in self.players:
			info_i = [i[0] for i in self.info_set if i[0].player == player]
			options = []
			for info in info_i:
			 	option = [item[1] for item in self.game_tree if item[0].label == info.label]
				options.append(option)
			strategies.update({player: [i for i in product(*options)]})
		self.strategies = strategies

	def set_payoffs(self):
	    """ set payoff matrices """
	    length = tuple([len(self.strategies[pl]) for pl in self.players])
	    strat_i = self.strategies['P1']
	    strat_j = self.strategies['P2']
	    payoff = np.zeros(length)
	    for i in range(length[0]):
	    	for j in range(length[1]):
	    		payoff[i, j] = self.traverse(strat_i[i] + strat_j[j])
	    return payoff
	
	def traverse(self, strat):
		node=self.game_tree[0][0]
		# [strat[0][i/2] if i % 2 == 0 else strat[1][(i+1)/2] for i in range(2*len(strat[0]))]
		val = True
		while val:
			nums = [i for i in range(len(self.info_set)) if node in self.info_set[i]]
			act = strat[nums[0]]
			nodes = [item[2] for item in self.game_tree if item[0].label == node.label and item[1] == act]
			node = nodes[0]
			if node.value:
				val = False
				return node.value[0]


class Node:
	""" simple node class for a graph"""
	def __init__(self, label, player=None,  value=None):
		self.label = label
		self.value = value
		self.player = player

players = ['P1', 'P2']
n1 = Node('a1', player=players[0])
n2 = Node('a2', player=players[0])
n3 = Node('a3', player=players[0])
n4 = Node('a4', player=players[0])
n5 = Node('a5', player=players[0])
n6 = Node('b1', player=players[1])
n7 = Node('b2', player=players[1])
n8 = Node('b3', player=players[1])
n9 = Node('b4', player=players[1])
n10 = Node('b5', player=players[1])
n11 = Node('b6', player=players[1])
n12 = Node('b7', player=players[1])
n13 = Node('b8', player=players[1])
n14 = Node('b9', player=players[1])
n15 = Node('b10', player=players[1])
n16 = Node('v1', value=(-1, 1))
n17 = Node('v2', value=(1, -1))
n18 = Node('v3', value=(-1, 1))
n19 = Node('v4', value=(1, -1))
n20 = Node('v5', value=(2, -2))
n21 = Node('v6', value=(1, -1))
n22 = Node('v7', value=(-1, 1))
n23 = Node('v8', value=(1, -1))
n24 = Node('v9', value=(1, -1))
n25 = Node('v10', value=(3, -3))
n26 = Node('v11', value=(3, -3))
n27 = Node('v12', value=(1, -1))
n28 = Node('v13', value=(1, -1))
n29 = Node('v14', value=(-2, 2))
n30 = Node('v15', value=(1, -1))
n31 = Node('v16', value=(-2, 2))
game_tree = [
	(n1, 'T', n6),
	(n2, 'T', n8),
	(n3, 'T', n10),
	(n4, 'T', n12),
	(n5, 'T', n14),
	(n1, 'B', n7),
	(n2, 'B', n9),
	(n3, 'B', n11),
	(n4, 'B', n13),
	(n5, 'B', n15),
	(n6, 'L', n2),
	(n7, 'L', n4),
	(n8, 'L', n16),
	(n9, 'L', n18),
	(n10, 'L', n20),
	(n11, 'L', n22),
	(n12, 'L', n24),
	(n13, 'L', n26),
	(n14, 'L', n28),
	(n15, 'L', n30),
	(n6, 'R', n3),
	(n7, 'R', n5),
	(n8, 'R', n17),
	(n9, 'R', n19),
	(n10, 'R', n21),
	(n11, 'R', n23),
	(n12, 'R', n25),
	(n13, 'R', n27),
	(n14, 'R', n29),
	(n15, 'R', n31)
	]

info_set = [[n1], [n2], [n3], [n4], [n5], [n6, n7], [n8, n9], [n10], [n11], [n12, n13], [n14, n15]]