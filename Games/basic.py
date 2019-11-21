#!/usr/bin/env python
"""
Basic library of game class definitions and relevant helper functions
"""

import numpy as np
from itertools import chain, combinations, product
from cvxopt import matrix, solvers
solvers.options['show_progress'] = False  # remove print output of cvxopt


#  Algorithms  #


def powerset(iterable):
    """ returns the powerset of an iterable object (as a list of tuples)"""
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))


def flatten(iterable):
    """ flatten a nested list into a single list """
    return [i for sublist in iterable for i in sublist]


def dict_nlist(dic):
    """ create a nested list from a dictionary of indices and values """

    def create_nlist(dim):
        """ recursively create a nested list according to a list of dimensions dim """
        return [create_nlist(dim[1:]) if len(dim) > 1 else None for _ in range(dim[0])]

    def nlist_set(nlist, ind, val):
        """ set a specific list of indexes ind from a nested list """
        sublist = nlist
        for i in ind[:-1]:
            sublist = sublist[i]
        sublist[ind[-1]] = val

    lengths = [max(pos)+1 for pos in map(list, zip(*dic.keys()))]
    nestedlist = create_nlist(lengths)
    for k, v in dic.items():
        nlist_set(nestedlist, k, v)
    return nestedlist


#  Game Frameworks  #


class Game:
    """ basic game class """
    def __init__(self, payoffs, players, strategies):
        self.players = players  # list of player labels (use the same ordering for indexing as in this list)
        self.n = len(players)  # number of players
        self.strategies = strategies  # list of player's list of strategies
        self.payoffs = payoffs  # list of n payoff numpy arrays (A_1 x A_2 X ...)
        self.pnes = None  # list of pure nash equilibria (index of strategy for each player)
        self.mnes = None  # list of mixed nash equilibria (index of strategy for each player)
        self.st_dict = None  # dictionary of {(tuple of player labels): (tuple of player strategies)}

    def U_i(self, i, strategy):
        """ utility for the strategy for player i"""
        pass

    def set_payoffs(self):
        """ set payoff matrices """
        self.set_dependency(['st_dict'])
        payoffs = [None]*self.n
        for i in range(self.n):
            s_dict_i = {}
            for k, v in self.st_dict.items():
                s_dict_i.update({k: self.U_i(i, v)})
            payoff_i = np.array(dict_nlist(s_dict_i))
            payoffs[i] = payoff_i
        self.payoffs = payoffs

    def set_mnes(self):
        """ set mixed nash equilibria """
        pass

    def set_pnes(self):
        """ set pure nash equilibria """
        self.set_dependency(['payoffs'])
        cpnes = list(np.argwhere(self.payoffs[0] == np.amax(self.payoffs[0], 0)))
        cpnes = [tuple(cpne) for cpne in cpnes]
        pnes = []
        for i in range(1, self.n):
            pm = self.payoffs[i]
            for cpne in cpnes[:]:
                ind = cpne[:i] + (slice(None),) + cpne[i+1:]
                if pm[cpne] < np.max(pm[ind]):
                    cpnes.pop(cpnes.index(cpne))
        self.pnes = cpnes

    def set_st_dict(self):
        """ set the dictionary of player labels and strategies """
        st_product = product(*self.strategies)
        labels = [j for j in product(*[[i for i in range(len(item))] for item in self.strategies])]
        st_dict = {}
        for k, v in zip(labels, st_product):
            st_dict.update({k: v})
        self.st_dict = st_dict

    def set_dependency(self, dependencies):
        """ set instance variables that are needed"""
        for dependency in dependencies:
            if eval('self.' + dependency) is None:
                eval('self.set_' + dependency + '()')

    def check_game(self):
        """ function for enforcing correct construction of a game definition """
        if self.n != len(self.strategies):
            raise ValueError('mismatch in length of self.strategies and number of players')
        if self.payoffs and len(self.payoffs) != self.n:
            raise ValueError('mismatch in length of self.payoffs and number of players')
        if self.payoffs and list(np.shape(self.payoffs[0])) != [len(s) for s in self.strategies]:
            raise ValueError('payoff matrix not set to right dimensions according to strategy set')


class FromPayoffGame(Game):
    """ define players and strategies through the given payoff matrix"""
    def __init__(self, payoffs):
        players = [i for i in range(len(payoffs))]  # player labels: 1 ... n
        strategies = [[i for i in range(d)] for d in np.shape(payoffs[0])]  # strategy labels: 1 ... m_i
        Game.__init__(self, payoffs, players, strategies)


class FromIndexGame(Game):
    """ define players through indexing the number of players and the number of strategies,
    no initialization of the payoff matrix"""
    def __init__(self, n, n_strat):
        players = [i for i in range(n)]  # player labels: 1 ... n
        strategies = [[i for i in range(num)] for num in n_strat]  # strategy labels: 1 ... m_i
        Game.__init__(self, None, players, strategies)
