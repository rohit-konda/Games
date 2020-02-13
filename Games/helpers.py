#!/usr/bin/env python
"""

Author : Rohit Konda

Helper functions
"""


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