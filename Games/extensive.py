#!/usr/bin/env python
"""
Zero Sum Game class definitions 
"""

from Games.basic_games import *


class NetworkGame(Game):
    """ framework for games that are based on a network"""
    def __init__(self, payoffs, players, strategies, network):
        Game.__init__(self, payoffs, players, strategies)
        self.network = network  # directed network of the game (dictionary of {node: to other nodes})
