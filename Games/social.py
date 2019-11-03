#!/usr/bin/env python
"""
Zero Sum Game class definitions 
"""

from Games.basic_games import *


class SocialGame(Game):
    """ game with a social utility function"""
    def __init__(self, payoffs, players, strategies):
        Game.__init__(self, payoffs, players, strategies)
        self.s_payoff = None  # social payoff for each set of strategies
        self.so = None  # optimal social payoff
        self.posa = None  # (Price of Anarchy, Stability)

    def set_s_payoff(self):
        """ set social payoff matrix"""
        pass

    def set_so(self):
        """ get strategies for the optimal social payoff"""
        self.set_dependency(['s_payoff'])
        self.so = np.amax(self.s_payoff)

    def set_posa(self):
        """ set price of anarchy and stability """
        self.set_dependency(['pnes', 'so'])
        pne_values = np.array([self.s_payoff[pne] for pne in self.pnes])
        price_ratios = list(pne_values/self.so)
        self.posa = (min(price_ratios), max(price_ratios))  # poa, pos


class PotentialGame(SocialGame):
    """ framework for a potential game"""
    def __init__(self, payoffs, players, strategies):
        SocialGame.__init__(self, payoffs, players, strategies)