#!/usr/bin/env python
"""

Author : Rohit Konda

Helper functions
"""
from itertools import chain

def powerset(iterable):
    """ returns the powerset of an iterable object (as a list of tuples)"""
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))


def flatten(iterable):
    """ flatten a nested list into a single list """
    return [i for sublist in iterable for i in sublist]
