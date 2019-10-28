#!/usr/bin/env python
"""
Basic library of game class definitions and relevant algorithms
"""

import numpy as np
from itertools import chain, combinations, product
from cvxopt import matrix, solvers
solvers.options['show_progress'] = False


#  Algorithms  #


def factorial(n):
    """ returns n factoral"""
    return n * factorial(n-1) if n > 1 else 1

def powerset(iterable):
    """ returns the powerset of an iterable object (as a list of tuples)"""
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

def flatten(iterable):
    """ flatten a nested list into a single list """
    return [i for sublist in iterable for i in sublist]

def to_dictstrat(players, strategies):
    """ return a dictionary of stratefies for each player from a list of strategies """
    strat = {}
    for k, v in zip(players, strategies):
        strat.update({k: v})
    return strat

def dict_nlist(dic):
    """ create a nested list from a dictionary of indices and values """
    lengths = [max(pos)+1 for pos in map(list, zip(*dic.keys()))]
    nestedlist = create_nlist(lengths)
    for k, v in dic.items():
        nlist_set(nestedlist, k, v)
    return nestedlist

def create_nlist(dim):
    """ recursively create a nested list according to dimensions dim """
    return [create_nlist(dim[1:]) if len(dim) > 1 else None for _ in range(dim[0])]

def nlist_set(nlist, ind, val, give=False):
    """ set or get a specific index ind from a nested list """
    sublist = nlist
    for i in ind[:-1]:
        sublist = sublist[i]
    if give:
        return sublist[ind[-1]]
    else:
        sublist[ind[-1]] = val


#  Game Frameworks  #


class Game():
    """ basic game class """
    def __init__(self, payoffs, players, strategies):
        self.players = players  # list of player labels
        self.n = len(players)  # number of players
        self.strategies = strategies  # dictionary of (player: list of possible strategies)
        self.payoffs = payoffs  # list of n payoff numpy arrays (A_1 x A_2 X ...)
        self.pnes = None  # list of pure nash equilibria (index of strategy for each player)
        self.mnes = None  # list of mixed nash equilibria (index of strategy for each player)
        self.st_dict = None  # dictionary of {(tuple of player labels): (tuple of player strategies)}

    def set_payoffs(self):
        """ set payoff matrices """
        pass

    def set_pnes(self):
        """ set pure nash equilibria """
        self.set_dependency(['payoffs'])
        cpnes = list(np.argwhere(self.payoffs[0] == np.amax(self.payoffs[0], 0)))
        cpnes = [tuple(cpne) for cpne in cpnes]
        num_strat = [len(st) for st in self.strategies.values()]

        for i in range(1, self.n):
            for cpne in cpnes:
                ind = cpne[:i] + (slice(num_strat[i]),) + cpne[i+1:]
                if self.payoffs[i][cpne] != np.amax(self.payoffs[i][ind]):
                    cpnes.pop(cpnes.index(cpne))
        self.pnes = cpnes

    def set_mnes(self):
        """ set mixed nash equilibria """
        pass

    def set_dependency(self, dependencies):
        """ set instance variables that are needed"""
        for dependency in dependencies:
            if eval('self.' + dependency) is None:
                eval('self.set_' + dependency + '()')

    def set_st_dict(self):
        """ set the dictionary of player labels and strategies """
        st = [self.strategies[pl] for pl in self.players]
        st_product = product(*st)
        labels = [j for j in product(*[[i for i in range(len(item))] for item in st])]
        st_dict = {}
        for k, v in zip(labels, st_product):
            st_dict.update({k: v})
        self.st_dict = st_dict


class FromPayoffGame(Game):
    """ define players and strategies through the given payoff matrix"""
    def __init__(self, payoffs):
        players = [i for i in range(len(payoffs))]  # player labels: 1 ... n
        strategies = {pl: [i for i in range(st)] for (pl, st) in zip(players, np.shape(payoffs[0]))}  # strategy labels: 1 ... m_i
        Game.__init__(self, payoffs, players, strategies)


class FromIndexGame(Game):
    """ define players through indexing the number of players and the number of strategies,
    no initialization of the payoff matrix"""
    def __init__(self, n, n_strat):
        players = [i for i in range(n)]  # player labels: 1 ... n
        strategies = {pl: [i for i in range(st)] for (pl, st) in zip(players, n_strat)}  # strategy labels: 1 ... m_i
        Game.__init__(self, None, players, strategies)


class NetworkGame(Game):
    """ framework for games that are based on a network"""
    def __init__(self, payoffs, players, strategies, network):
        Game.__init__(self, payoffs, players, strategies)
        self.network = network  # directed network of the game (dictionary of {node: to other nodes})


class ZeroSumGame(FromPayoffGame):
    """ zero sum game wituh two players"""
    def __init__(self, payoff):
        payoffs = [-payoff, payoff]  # 1st player minimizes, 2nd player maximizes
        FromPayoffGame.__init__(self, payoffs)
        self.psec = None  # define pure security policies dictionaries (V_underbar, p1_index), (V_overbar, p2_index)
        self.msec = None  # define mixed security policies dictionary (V_m, p1_policy, p2_policy)

    def set_sec(self):
        """ set pure security values and policies """
        max_first = np.max(self.payoffs[0], 1)
        V_underbar = np.min(max_first)
        p1_policy = np.nonzero(max_first == V_underbar)[0].tolist()
        min_first = np.min(self.payoffs[0], 0)
        V_overbar = np.max(min_first)
        p2_policy = np.nonzero(min_first == V_overbar)[0].tolist()
        self.sec = [(V_underbar, p1_policy), (V_overbar, p2_policy)]

    def set_msec(self):
        """ set mixed security values and policies """
        n = len(self.strategies[0])
        m = len(self.strategies[1])
        O_n = np.ones((n, 1))
        O_m = np.ones((m, 1))
        Z_n = np.zeros((n, 1))
        Z_m = np.zeros((m, 1))
        I_n = np.identity(n)
        I_m = np.identity(m)
        P = self.payoffs[1]

        c_n = matrix(np.hstack((np.array([1]), np.zeros((n,)))))
        G_n = matrix(np.vstack((np.hstack((-O_m, P.T)), np.hstack((Z_n, -I_n)))))
        h_n = matrix(np.vstack((Z_m, Z_n)))
        A_n = matrix(np.hstack((np.array([[0]]), O_n.T)))
        b_n = matrix(np.array([1.]))
        sol_n = solvers.lp(c_n, G_n, h_n, A_n, b_n)

        c_m = matrix(np.hstack((np.array([-1]), np.zeros((m,)))))
        G_m = matrix(np.vstack((np.hstack((O_n, -P)), np.hstack((Z_m, -I_m)))))
        h_m = matrix(np.vstack((Z_n, Z_m)))
        A_m = matrix(np.hstack((np.array([[0]]), O_m.T)))
        b_m = matrix(np.array([1.]))
        sol_m = solvers.lp(c_m, G_m, h_m, A_m, b_m)

        self.msec = (sol_n['x'][0], sol_n['x'][1:], sol_m['x'][1:])


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
