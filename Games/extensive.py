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


info_set = [[n1], [n2], [n3], [n4], [n5], [n6, n7], [n8, n9], [n10], [n11], [n12, n13], [n14, n15]]